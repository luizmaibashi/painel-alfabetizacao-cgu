"""
Teste de unidade para src/preprocessing/06_agregar_censo_escolar.py.

POR QUE ESTE ARQUIVO EXISTE
----------------------------
O GATE ML de cobertura minima (.claude/rules/dados.md) exige teste que varia
o parametro e verifica que o resultado muda de acordo — a regra nasceu de dois
bugs reais deste projeto: `calcular_historico_t1()` ignorava o caminho
recebido, e a imputacao por mediana de UF tinha condicao estruturalmente
sempre falsa. Ambos sobreviveram ate revisao manual de numeros.

As funcoes aqui decidem QUAIS escolas entram e COM QUE PESO — errar nisso nao
quebra nada visivelmente: o agregado sai plausivel e o modelo treina normal.
Por isso cada filtro e cada regra de ponderacao tem teste proprio.
"""
import importlib.util
from pathlib import Path

import pandas as pd
import pytest

BASE = Path(__file__).resolve().parents[1]

spec = importlib.util.spec_from_file_location(
    "agregar_censo_escolar",
    BASE / "src" / "preprocessing" / "06_agregar_censo_escolar.py")
ace = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ace)


def _escola(co_municipio="1100205", entidade=1, situacao=1, dependencia=3,
            mat_2ano=10, **indicadores):
    """Uma linha de Censo sintetica, com os defaults ja passando nos filtros."""
    linha = {
        "CO_MUNICIPIO": co_municipio,
        "SG_UF": "RO",
        "CO_ENTIDADE": entidade,
        "TP_SITUACAO_FUNCIONAMENTO": situacao,
        "TP_DEPENDENCIA": dependencia,
        "TP_LOCALIZACAO": 1,
        "QT_MAT_FUND_AI_2": mat_2ano,
    }
    for col in ace.TODOS_INDICADORES:
        linha[col] = indicadores.get(col, 1)
    return linha


# --- filtrar_escolas_relevantes: cada filtro precisa remover o que promete ---

def test_filtro_remove_escola_paralisada():
    df = pd.DataFrame([_escola(entidade=1, situacao=1),
                        _escola(entidade=2, situacao=3)])  # 3 = paralisada
    out = ace.filtrar_escolas_relevantes(df)
    assert list(out.CO_ENTIDADE) == [1]


def test_filtro_remove_escola_privada():
    df = pd.DataFrame([_escola(entidade=1, dependencia=3),   # municipal
                        _escola(entidade=2, dependencia=4)])  # privada
    out = ace.filtrar_escolas_relevantes(df)
    assert list(out.CO_ENTIDADE) == [1]


def test_filtro_mantem_federal_e_estadual():
    """Publica != so municipal — o indicador cobre a rede publica inteira."""
    df = pd.DataFrame([_escola(entidade=1, dependencia=1),
                        _escola(entidade=2, dependencia=2),
                        _escola(entidade=3, dependencia=3)])
    out = ace.filtrar_escolas_relevantes(df)
    assert sorted(out.CO_ENTIDADE) == [1, 2, 3]


def test_filtro_remove_escola_sem_matricula_no_2o_ano():
    """Escola sem 2o ano nao descreve a populacao que o alvo mede."""
    df = pd.DataFrame([_escola(entidade=1, mat_2ano=30),
                        _escola(entidade=2, mat_2ano=0),
                        _escola(entidade=3, mat_2ano=None)])
    out = ace.filtrar_escolas_relevantes(df)
    assert list(out.CO_ENTIDADE) == [1]


def test_filtro_levanta_erro_se_coluna_sumir():
    """Falha explicita, nao filtro silenciosamente ignorado (guarda silenciosa)."""
    df = pd.DataFrame([_escola()]).drop(columns=["TP_DEPENDENCIA"])
    with pytest.raises(ValueError, match="TP_DEPENDENCIA"):
        ace.filtrar_escolas_relevantes(df)


# --- agregar_por_municipio: a ponderacao precisa realmente ponderar ---------

def test_agregacao_e_ponderada_pela_matricula_nao_media_simples():
    """
    Escola grande (90 alunos) COM internet + escola pequena (10) SEM.
    Media simples daria 0,50; ponderada da 0,90. O teste falha se alguem
    trocar a ponderacao por `.mean()` — que foi a razao de existir da funcao.
    """
    df = pd.DataFrame([
        _escola(entidade=1, mat_2ano=90, IN_INTERNET=1),
        _escola(entidade=2, mat_2ano=10, IN_INTERNET=0),
    ])
    out = ace.agregar_por_municipio(df, indicadores=["IN_INTERNET"])
    assert out.loc[0, "IN_INTERNET"] == pytest.approx(0.90)


def test_agregacao_separa_municipios():
    df = pd.DataFrame([
        _escola(co_municipio="1100205", entidade=1, IN_INTERNET=1),
        _escola(co_municipio="3550308", entidade=2, IN_INTERNET=0),
    ])
    out = ace.agregar_por_municipio(df, indicadores=["IN_INTERNET"]) \
        .set_index("CO_MUNICIPIO")
    assert out.loc["1100205", "IN_INTERNET"] == pytest.approx(1.0)
    assert out.loc["3550308", "IN_INTERNET"] == pytest.approx(0.0)


def test_indicador_nulo_nao_vira_zero():
    """
    Nulo = "o Censo nao afirma", nao "a escola nao tem". Tratar como zero
    inventaria dado. Aqui a escola com nulo sai do peso, e o resultado e 1,0
    (so a escola que respondeu conta), nao 0,5.
    """
    df = pd.DataFrame([
        _escola(entidade=1, mat_2ano=50, IN_INTERNET=1),
        _escola(entidade=2, mat_2ano=50, IN_INTERNET=None),
    ])
    out = ace.agregar_por_municipio(df, indicadores=["IN_INTERNET"])
    assert out.loc[0, "IN_INTERNET"] == pytest.approx(1.0)


def test_municipio_com_indicador_todo_nulo_vira_nan_nao_zero():
    """NaN deixa o SimpleImputer decidir (ADR-0009); zero seria uma afirmacao."""
    df = pd.DataFrame([_escola(entidade=1, IN_INTERNET=None)])
    out = ace.agregar_por_municipio(df, indicadores=["IN_INTERNET"])
    assert pd.isna(out.loc[0, "IN_INTERNET"])


def test_agregacao_reporta_matricula_e_contagem_de_escolas():
    df = pd.DataFrame([_escola(entidade=1, mat_2ano=30),
                        _escola(entidade=2, mat_2ano=20)])
    out = ace.agregar_por_municipio(df, indicadores=["IN_INTERNET"])
    assert out.loc[0, "mat_2ano_total"] == 50
    assert out.loc[0, "n_escolas_2ano"] == 2


def test_agregacao_levanta_erro_se_peso_sumir():
    df = pd.DataFrame([_escola()]).drop(columns=["QT_MAT_FUND_AI_2"])
    with pytest.raises(ValueError, match="QT_MAT_FUND_AI_2"):
        ace.agregar_por_municipio(df, indicadores=["IN_INTERNET"])


# --- criar_indices_compostos ------------------------------------------------

def test_indice_composto_e_media_dos_indicadores_do_grupo():
    agg = pd.DataFrame([{"CO_MUNICIPIO": "1100205",
                          "IN_INTERNET": 1.0, "IN_COMPUTADOR": 0.0}])
    out = ace.criar_indices_compostos(
        agg, grupos={"conectividade": ["IN_INTERNET", "IN_COMPUTADOR"]})
    assert out.loc[0, "infra_conectividade"] == pytest.approx(0.5)


def test_indice_composto_ignora_nan_sem_zerar_o_indice():
    agg = pd.DataFrame([{"CO_MUNICIPIO": "1100205",
                          "IN_INTERNET": 1.0, "IN_COMPUTADOR": None}])
    out = ace.criar_indices_compostos(
        agg, grupos={"conectividade": ["IN_INTERNET", "IN_COMPUTADOR"]})
    assert out.loc[0, "infra_conectividade"] == pytest.approx(1.0)


def test_indice_composto_levanta_erro_se_grupo_nao_existe():
    agg = pd.DataFrame([{"CO_MUNICIPIO": "1100205", "IN_INTERNET": 1.0}])
    with pytest.raises(ValueError, match="inexistente"):
        ace.criar_indices_compostos(agg, grupos={"inexistente": ["IN_NADA"]})


def test_grupos_declarados_cobrem_todos_os_indicadores():
    """
    Guarda contra o modo de falha 'lista manual fail-open' (AGENTS.md):
    indicador novo em INDICADORES que ninguem poe num grupo sairia da
    agregacao em silencio.
    """
    do_mapa = [c for g in ace.INDICADORES.values() for c in g]
    assert sorted(do_mapa) == sorted(ace.TODOS_INDICADORES)
    assert len(do_mapa) == len(set(do_mapa)), "indicador repetido entre grupos"
