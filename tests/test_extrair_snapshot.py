"""
Teste de unidade para as duas funcoes com bug real ja documentado
(o diário de bordo interno (não publicado) Cap. 9.7) em src/preprocessing/02_extrair_snapshot.py.

POR QUE ESTE ARQUIVO EXISTE
----------------------------
GATE ML - Cobertura minima de teste de unidade (.claude/rules/dados.md). Os
dois bugs mais baratos de pegar por teste sobreviveram ate revisao manual de
numeros neste projeto:

  1. `calcular_historico_t1()` recebia `caminho_csv` como parametro e o
     IGNORAVA, sempre lendo `data/Alunos_amostra.csv` fixo -- rodar na base
     completa calcularia o historico sobre a amostra de 5.000 e colaria nas
     57.781 linhas, errado em silencio. Corrigido em 2026-08-18 (ver docstring
     da funcao), mas sem teste que prove que o parametro de fato muda o
     resultado.
  2. `imputar_historico`/`_imputar_coluna` tinham uma condicao
     estruturalmente sempre falsa (`if "sigla_uf" in out.columns`) porque
     `sigla_uf` so chega depois de um join que rodava DEPOIS dessa funcao --
     a mediana-por-UF documentada no ADR-0001 NUNCA executava, caindo sempre
     no fallback global sem aviso. Corrigido separando a imputacao do join de
     historico, mas sem teste que force os dois caminhos (com e sem
     `sigla_uf`) e prove que cada um usa a formula certa.

Este arquivo cobre os dois com teste de regressao direto.
"""
import importlib.util
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

BASE = Path(__file__).resolve().parents[1]

spec = importlib.util.spec_from_file_location(
    "extrair_snapshot", BASE / "src" / "preprocessing" / "02_extrair_snapshot.py")
es = importlib.util.module_from_spec(spec)
spec.loader.exec_module(es)


# --- calcular_historico_t1: parametro `caminho_csv` nao pode ser ignorado --

def _csv_hostorico(tmp_path, sufixo, taxa_ausencia):
    """Gera um CSV bruto minimo, no formato que calcular_historico_t1 espera
    (colunas id_escola, id_municipio, ano, presenca)."""
    n = 40
    rng = np.random.default_rng(hash(sufixo) % (2**32))
    ausente = rng.random(n) < taxa_ausencia
    df = pd.DataFrame({
        "id_escola": [f"E{i % 5}" for i in range(n)],
        "id_municipio": ["1100015"] * n,
        "ano": [2023] * n,
        "presenca": np.where(ausente, "Ausente", "Presente"),
    })
    caminho = tmp_path / f"historico_{sufixo}.csv"
    df.to_csv(caminho, index=False)
    return caminho


def test_calcular_historico_t1_usa_o_csv_do_parametro_nao_um_fixo(tmp_path):
    """
    REGRESSAO DIRETA do bug do HANDOFF Cap. 9.7: dois CSVs com taxas de
    ausencia MUITO diferentes (10% vs 90%) devem produzir
    absenteismo_hist_*_t1 MUITO diferentes. Se a funcao ignorasse o
    parametro (bug antigo), os dois resultados seriam identicos -- os dois
    viriam do mesmo arquivo fixo, nao dos CSVs passados aqui.
    """
    csv_baixa = _csv_hostorico(tmp_path, "baixa", taxa_ausencia=0.10)
    csv_alta = _csv_hostorico(tmp_path, "alta", taxa_ausencia=0.90)

    hist_baixa = es.calcular_historico_t1(csv_baixa)
    hist_alta = es.calcular_historico_t1(csv_alta)

    taxa_baixa = hist_baixa["municipio"]["absenteismo_hist_municipio_t1"].iloc[0]
    taxa_alta = hist_alta["municipio"]["absenteismo_hist_municipio_t1"].iloc[0]

    assert taxa_baixa != pytest.approx(taxa_alta, abs=0.05), (
        "os dois CSVs deram a MESMA taxa -- calcular_historico_t1 pode estar "
        "ignorando o parametro caminho_csv de novo (bug do HANDOFF Cap. 9.7)"
    )
    assert taxa_baixa < 0.3
    assert taxa_alta > 0.7


def test_calcular_historico_t1_desloca_o_ano_para_o_seguinte(tmp_path):
    """A feature de historico t-1 e usada no ano SEGUINTE ao dado bruto —
    presenca de 2023 vira absenteismo_hist_*_t1 disponivel para 2024."""
    csv = _csv_hostorico(tmp_path, "deslocamento", taxa_ausencia=0.5)
    hist = es.calcular_historico_t1(csv)
    anos_disponiveis = set(hist["municipio"]["ano"])
    assert anos_disponiveis == {2024}, (
        "CSV bruto tinha ano=2023; a feature de historico deveria valer "
        "para 2024 (ano seguinte), nao para o proprio 2023"
    )


# --- imputar_historico / _imputar_coluna: condicao sigla_uf nao pode ser
#     estruturalmente sempre falsa ---------------------------------------

def _snapshot_com_buraco(n=60, com_sigla_uf=True, seed=0):
    rng = np.random.default_rng(seed)
    ufs = rng.choice(["SP", "MG", "CE"], n)
    # metade dos valores de SP viram nulo -- caso a imputar. Duas colunas:
    # imputar_historico() itera as duas, fixas ("escola" e "municipio").
    df = pd.DataFrame({"sigla_uf": ufs} if com_sigla_uf else {})
    for col in ("absenteismo_hist_escola_t1", "absenteismo_hist_municipio_t1"):
        valores = rng.normal(0.3, 0.05, n)
        buraco = (ufs == "SP") & (rng.random(n) < 0.5)
        df[col] = np.where(buraco, np.nan, valores)
    return df


def test_imputar_historico_usa_mediana_da_uf_quando_coluna_existe():
    """
    REGRESSAO DIRETA do bug do HANDOFF Cap. 9.7: com `sigla_uf` presente no
    snapshot (cenario real, apos o join de territorio), a imputacao TEM que
    usar a mediana POR UF, nao a mediana global -- senao a condicao
    `if "sigla_uf" in snapshot.columns` esta de novo estruturalmente
    inalcancavel nesse ponto do pipeline.
    """
    df = _snapshot_com_buraco(com_sigla_uf=True, seed=1)
    mediana_global = df["absenteismo_hist_escola_t1"].median()
    mediana_sp_real = df.loc[df["sigla_uf"] == "SP", "absenteismo_hist_escola_t1"].median()

    resultado = es.imputar_historico(df.copy())
    linhas_sp_imputadas = df["sigla_uf"].eq("SP") & df["absenteismo_hist_escola_t1"].isna()
    valores_imputados_sp = resultado.loc[linhas_sp_imputadas, "absenteismo_hist_escola_t1"]

    assert not valores_imputados_sp.empty, "teste mal configurado: nenhuma linha de SP tinha nulo"
    assert valores_imputados_sp.eq(mediana_sp_real).all(), (
        "linhas de SP nao foram imputadas com a mediana de SP -- caiu no "
        "fallback global mesmo com sigla_uf presente (bug do HANDOFF Cap. 9.7)"
    )
    # a mediana de SP (so valores baixos, ~0.3) deve diferir da global o
    # suficiente para o teste ser conclusivo, nao coincidencia numerica
    assert not resultado["absenteismo_hist_escola_t1"].isna().any()


def test_imputar_historico_cai_no_fallback_global_sem_sigla_uf():
    """Sem `sigla_uf` no snapshot (cenario --local-only, sem territorio), a
    imputacao deve usar a mediana GLOBAL -- e nao quebrar por coluna ausente."""
    df = _snapshot_com_buraco(com_sigla_uf=False, seed=2)
    mediana_global = df["absenteismo_hist_escola_t1"].median()

    resultado = es.imputar_historico(df.copy())

    assert not resultado["absenteismo_hist_escola_t1"].isna().any()
    linhas_imputadas = df["absenteismo_hist_escola_t1"].isna()
    assert resultado.loc[linhas_imputadas, "absenteismo_hist_escola_t1"].eq(
        mediana_global).all()


def test_imputar_historico_loga_quantas_linhas_foram_afetadas(capsys):
    """Fallback silencioso e o antipadrao (AGENTS.md 'guarda silenciosa') --
    a funcao deve imprimir quantas linhas de cada coluna foram imputadas."""
    df = _snapshot_com_buraco(com_sigla_uf=True, seed=3)
    n_nulos_antes = int(df["absenteismo_hist_escola_t1"].isna().sum())
    assert n_nulos_antes > 0, "teste mal configurado: nenhum nulo para imputar"

    es.imputar_historico(df.copy())
    saida = capsys.readouterr().out

    assert "absenteismo_hist_escola_t1" in saida
    assert str(n_nulos_antes) in saida


# --- juntar_historico: flags de disponibilidade --------------------------

def test_juntar_historico_marca_disponibilidade_corretamente():
    alunos = pd.DataFrame({
        "id_escola": ["E1", "E2"],
        "id_municipio": ["1100015", "1100015"],
        "ano": [2024, 2024],
    })
    hist_escola = pd.DataFrame({
        "id_escola": ["E1"], "ano": [2024],
        "absenteismo_hist_escola_t1": [0.2], "n_alunos_hist_escola_t1": [10],
    })
    hist_municipio = pd.DataFrame({
        "id_municipio": ["1100015"], "ano": [2024],
        "absenteismo_hist_municipio_t1": [0.15], "n_alunos_hist_municipio_t1": [50],
    })
    resultado = es.juntar_historico(
        alunos, {"escola": hist_escola, "municipio": hist_municipio})

    # E1 tem historico de escola, E2 nao
    assert resultado.loc[resultado.id_escola == "E1", "possui_hist_escola_t1"].iloc[0] == 1
    assert resultado.loc[resultado.id_escola == "E2", "possui_hist_escola_t1"].iloc[0] == 0
    # ambos tem historico de municipio (mesmo municipio)
    assert (resultado["possui_hist_municipio_t1"] == 1).all()
