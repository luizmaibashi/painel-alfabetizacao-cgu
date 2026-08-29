"""
Teste de unidade para a guarda de cobertura de colunas em
src/preprocessing/pipeline_preprocessamento.py.

POR QUE ESTE ARQUIVO EXISTE
----------------------------
Achado do teste de aplicacao dos gates manuais (2026-08-24, ver
docs/debitos_minerados.md): `colunas_ignoradas()` foi escrita com o proposito
declarado de "nunca mais uma feature entrar no snapshot e sumir sem ninguem
ver" — mas o resultado dela so era IMPRESSO por `descrever_features`, nunca
bloqueava nada, e NENHUM teste chamava a funcao.

E o antipadrao "lista de cobertura falha aberta" do AGENTS.md: o
comportamento default da lista desatualizada era PERMISSIVO. Coluna nova fora
de `TODAS_CANDIDATAS` saia do modelo em silencio, e o unico obstaculo era
alguem reparar numa linha de log no meio de um treino.

O checklist daquela regra pede exatamente o teste que faltava:
"existe teste que adiciona um item ficticio fora da lista e confirma que o
gate REJEITA ou avisa, nao aprova?" — e o
`test_validar_cobertura_colunas_rejeita_coluna_nao_declarada` abaixo.
"""
import importlib.util
from pathlib import Path

import pandas as pd
import pytest

BASE = Path(__file__).resolve().parents[1]

spec = importlib.util.spec_from_file_location(
    "pipeline_preprocessamento",
    BASE / "src" / "preprocessing" / "pipeline_preprocessamento.py")
pp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pp)


def _snapshot_valido() -> pd.DataFrame:
    """Snapshot minimo em que TODA coluna esta declarada em alguma lista."""
    return pd.DataFrame({
        "id_aluno": ["A1", "A2"],
        "id_municipio": ["1100015", "1100015"],
        "ano": [2024, 2024],
        pp.COLUNA_TARGET: ["Sim", "Não"],
        "caderno": ["12", "13"],
        "rede": ["Municipal", "Estadual"],
        "sigla_uf": ["RO", "RO"],
        "absenteismo_hist_municipio_t1": [0.1, 0.2],
        "possui_hist_municipio_t1": [1, 1],
    })


# --- colunas_ignoradas: a consulta pura -----------------------------------

def test_colunas_ignoradas_vazio_quando_tudo_declarado():
    assert pp.colunas_ignoradas(_snapshot_valido()) == []


def test_colunas_ignoradas_encontra_coluna_fora_das_listas():
    df = _snapshot_valido()
    df["renda_familiar_media"] = [1000.0, 2000.0]
    assert pp.colunas_ignoradas(df) == ["renda_familiar_media"]


def test_colunas_ignoradas_nao_confunde_identificador_com_descarte():
    """COLUNAS_ID nao sao feature, mas TAMBEM nao sao descarte — se caissem em
    `colunas_ignoradas` o gate viveria disparando e seria removido."""
    df = _snapshot_valido()
    df["_peso_amostral"] = [1.0, 1.0]
    df["id_escola"] = ["E1", "E2"]
    assert pp.colunas_ignoradas(df) == []


# --- validar_cobertura_colunas: o gate fail-closed ------------------------

def test_validar_cobertura_colunas_aceita_snapshot_todo_declarado():
    pp.validar_cobertura_colunas(_snapshot_valido())  # nao levanta


def test_validar_cobertura_colunas_rejeita_coluna_nao_declarada():
    """
    O TESTE QUE FALTAVA (AGENTS.md, "lista de cobertura falha aberta"):
    adiciona uma coluna ficticia fora de toda lista e confirma que o gate
    REJEITA, em vez de aprovar por omissao.

    Antes da correcao de 2026-08-24 nada aqui falharia: a coluna era
    silenciosamente descartada e o treino seguia normal.
    """
    df = _snapshot_valido()
    df["indice_vulnerabilidade_novo"] = [0.3, 0.7]

    with pytest.raises(pp.ColunaNaoDeclaradaError) as erro:
        pp.validar_cobertura_colunas(df)

    # a mensagem precisa NOMEAR a coluna, senao o erro nao ajuda a corrigir
    assert "indice_vulnerabilidade_novo" in str(erro.value)


def test_validar_cobertura_colunas_reporta_todas_as_nao_declaradas():
    """Falhar na primeira esconderia as demais e exigiria N rodadas."""
    df = _snapshot_valido()
    df["coluna_a"] = [1, 2]
    df["coluna_b"] = [3, 4]

    with pytest.raises(pp.ColunaNaoDeclaradaError) as erro:
        pp.validar_cobertura_colunas(df)

    assert "coluna_a" in str(erro.value)
    assert "coluna_b" in str(erro.value)


def test_validar_cobertura_colunas_aceita_descarte_explicito():
    """`permitidas` e a saida para descarte INTENCIONAL — exige digitar o nome
    na chamada, o que mantem a decisao visivel no codigo em vez de num log."""
    df = _snapshot_valido()
    df["coluna_de_auditoria"] = [1, 2]

    pp.validar_cobertura_colunas(df, permitidas=("coluna_de_auditoria",))  # nao levanta


def test_permitidas_nao_libera_outras_colunas():
    """Descarte explicito de UMA coluna nao pode abrir a porta para as outras —
    seria reintroduzir o fail-open por outro caminho."""
    df = _snapshot_valido()
    df["coluna_de_auditoria"] = [1, 2]
    df["coluna_esquecida"] = [3, 4]

    with pytest.raises(pp.ColunaNaoDeclaradaError) as erro:
        pp.validar_cobertura_colunas(df, permitidas=("coluna_de_auditoria",))

    assert "coluna_esquecida" in str(erro.value)
    assert "coluna_de_auditoria" not in str(erro.value)


# --- o gate esta de fato ligado no pipeline real --------------------------

def test_descrever_features_continua_reportando_sem_levantar():
    """`descrever_features` e log, nao gate: precisa continuar descrevendo um
    snapshot com coluna estranha sem quebrar (quem bloqueia e o validar)."""
    df = _snapshot_valido()
    df["coluna_estranha"] = [1, 2]

    texto = pp.descrever_features(df)

    assert "coluna_estranha" in texto
    assert "ATENÇÃO" in texto


# --- descrever_snapshot: o rotulo tem que seguir o DADO, nao uma constante ---
#
# POR QUE ESTES TESTES EXISTEM (2026-08-29)
# ------------------------------------------
# `02_tournament_modelos.py` gravava em reports/metrics_tournament.json a
# string literal "local-only (sem territorio/socioeconomico/meta)" — constante
# hardcoded, nao leitura do estado. O MESMO json listava populacao_total,
# meta_alfabetizacao_2024_imputada e sigla_uf em features_usadas. Quem lesse o
# relatorio concluiria que o ROC-AUC ~0,68 vinha de sinal puramente local,
# quando ele vem do bloco municipal (SHAP: 85,3% da influencia).
#
# Mesma classe da "guarda silenciosa" do AGENTS.md: o rotulo errado nao quebra
# nada, so convence. O teste que fecha a classe (nao a instancia) e o
# `test_descrever_snapshot_muda_quando_o_dado_muda`: obriga o rotulo a variar
# junto com as colunas, entao uma string fixa reprova por construcao.

def test_descrever_snapshot_local_only_quando_nao_ha_territorio():
    """Snapshot sem nenhuma coluna de territorio e legitimamente local-only."""
    rotulo = pp.descrever_snapshot(_snapshot_valido())
    assert "local-only" in rotulo


def test_descrever_snapshot_nao_diz_local_only_com_territorio_presente():
    """O bug real: rotulo dizia 'sem territorio' com territorio no dataframe."""
    df = _snapshot_valido()
    df["populacao_total"] = [50000, 50000]
    df["meta_alfabetizacao_2024_imputada"] = [0.7, 0.7]
    rotulo = pp.descrever_snapshot(df)
    assert "local-only" not in rotulo
    assert "populacao_total" in rotulo


def test_descrever_snapshot_marca_parcial_quando_falta_alguma():
    """Territorio incompleto e um terceiro estado — nao pode virar 'full'."""
    df = _snapshot_valido()
    df["populacao_total"] = [50000, 50000]
    rotulo = pp.descrever_snapshot(df)
    assert "parcial" in rotulo
    # A que falta precisa aparecer: 'parcial' sem dizer o que falta nao ajuda.
    assert "gasto_por_habitante_educacao" in rotulo


def test_descrever_snapshot_full_quando_territorio_completo():
    df = _snapshot_valido()
    for coluna in pp.COLUNAS_TERRITORIO:
        df[coluna] = [1.0, 1.0]
    rotulo = pp.descrever_snapshot(df)
    assert "full" in rotulo
    assert "parcial" not in rotulo


def test_descrever_snapshot_muda_quando_o_dado_muda():
    """
    A guarda de classe: uma constante literal passaria em qualquer teste que
    so checasse UM caso. Este exige que o rotulo seja funcao do dataframe.
    """
    sem = pp.descrever_snapshot(_snapshot_valido())
    com = _snapshot_valido()
    for coluna in pp.COLUNAS_TERRITORIO:
        com[coluna] = [1.0, 1.0]
    assert sem != pp.descrever_snapshot(com)


def test_colunas_territorio_sao_todas_candidatas_declaradas():
    """
    COLUNAS_TERRITORIO nao pode divergir do catalogo de features: se alguem
    renomear uma candidata e esquecer desta lista, o rotulo volta a mentir —
    silenciosamente, que e exatamente o modo de falha que originou o bug.
    """
    assert set(pp.COLUNAS_TERRITORIO) <= set(pp.TODAS_CANDIDATAS)
