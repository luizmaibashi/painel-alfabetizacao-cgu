"""
Teste de unidade para a imputacao da meta em
src/preprocessing/05_montar_territorio.py.

POR QUE ESTE ARQUIVO EXISTE
----------------------------
Achado do teste de aplicacao dos gates manuais (2026-08-24, ver
docs/debitos_minerados.md): a cascata de `fillna` que preenche
`meta_alfabetizacao_2024_imputada` rodava em silencio — nenhum numero dizia
quantas linhas foram imputadas, nem por qual degrau da cascata.

E o antipadrao "guarda silenciosa" do AGENTS.md: um default aplicado sem log
nem erro. Os dois degraus nao tem o mesmo risco — cair na mediana da propria
UF e razoavel; cair na mediana GLOBAL significa que a UF INTEIRA estava sem
meta, correcao muito mais grosseira. Sem contagem separada, ninguem sabe se o
degrau grosseiro atingiu 2 linhas ou 200.

Nos dados reais de 2026-08-24 sao 240 imputadas de 10.704 (2,2%), das quais
44 caem na mediana global. Esses 44 eram invisiveis.

O item 3 do checklist do GATE ML de cobertura de teste (.claude/rules/dados.md)
pede exatamente isto: "o fallback (imputacao, valor default) loga quantas
linhas foram afetadas?"
"""
import importlib.util
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

BASE = Path(__file__).resolve().parents[1]

spec = importlib.util.spec_from_file_location(
    "montar_territorio", BASE / "src" / "preprocessing" / "05_montar_territorio.py")
mt = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mt)


def _territorio(metas_por_uf: dict[str, list]) -> pd.DataFrame:
    """Monta um territorio minimo; `None` na lista = meta ausente."""
    linhas = []
    for uf, metas in metas_por_uf.items():
        for i, meta in enumerate(metas):
            linhas.append({
                "id_municipio": f"{uf}{i:05d}",
                "sigla_uf": uf,
                "meta_alfabetizacao_2024": np.nan if meta is None else float(meta),
            })
    return pd.DataFrame(linhas)


# --- o valor imputado: cada degrau usa a formula certa --------------------

def test_imputa_com_a_mediana_da_propria_uf_quando_a_uf_tem_meta():
    # SP tem metas 60/70/80 -> mediana 70. MG serve so para deslocar a global.
    df = _territorio({"SP": [60, 70, 80, None], "MG": [10, 10, 10, 10]})

    out = mt.imputar_meta(df.copy())

    imputada = out.loc[out["meta_alfabetizacao_2024"].isna(),
                       "meta_alfabetizacao_2024_imputada"]
    assert imputada.iloc[0] == pytest.approx(70.0), (
        "linha de SP deveria receber a mediana de SP (70), nao a global"
    )


def test_cai_na_mediana_global_quando_a_uf_inteira_esta_sem_meta():
    """O degrau grosseiro: RR nao tem NENHUMA meta, entao a mediana por UF e
    NaN e a linha desce para a mediana global."""
    df = _territorio({"SP": [60, 70, 80], "RR": [None, None]})

    out = mt.imputar_meta(df.copy())

    imputadas = out.loc[out["sigla_uf"] == "RR", "meta_alfabetizacao_2024_imputada"]
    assert imputadas.eq(70.0).all(), "RR deveria cair na mediana global (70)"


def test_nao_altera_as_linhas_que_ja_tinham_meta():
    """A imputacao e observabilidade, nao mudanca de valor — o modelo canonico
    ja foi validado sobre estes numeros."""
    df = _territorio({"SP": [60, 70, 80, None]})

    out = mt.imputar_meta(df.copy())

    tinha = out["meta_alfabetizacao_2024"].notna()
    assert (out.loc[tinha, "meta_alfabetizacao_2024_imputada"]
            == out.loc[tinha, "meta_alfabetizacao_2024"]).all()


# --- O LOG: o que a correcao de 2026-08-24 acrescentou --------------------

def test_loga_o_n_de_cada_degrau_da_cascata(capsys):
    """
    REGRESSAO DIRETA da guarda silenciosa: a saida precisa separar quantas
    linhas foram pela mediana da UF e quantas pela mediana GLOBAL. Reportar
    so o total esconderia exatamente a informacao que decide se a imputacao
    foi razoavel ou grosseira.
    """
    # SP: 2 nulos com meta disponivel na UF -> degrau 1
    # RR: 3 nulos e nenhuma meta na UF      -> degrau 2 (global)
    df = _territorio({"SP": [60, 70, 80, None, None], "RR": [None, None, None]})

    mt.imputar_meta(df.copy())
    saida = capsys.readouterr().out

    assert "5 de 8" in saida, f"total de imputadas ausente do log: {saida!r}"
    assert "2 pela mediana da UF" in saida, f"degrau 1 ausente do log: {saida!r}"
    assert "3 pela mediana GLOBAL" in saida, f"degrau 2 ausente do log: {saida!r}"


def test_loga_explicitamente_quando_nada_foi_imputado(capsys):
    """Silencio ambiguo e o problema: 'nao imprimiu nada' nao distingue
    'nenhuma imputacao' de 'o log sumiu'."""
    df = _territorio({"SP": [60, 70, 80]})

    mt.imputar_meta(df.copy())
    saida = capsys.readouterr().out

    assert "nenhuma linha imputada" in saida


# --- fail-closed: cascata que nao consegue imputar nao pode passar --------

def test_levanta_quando_a_coluna_inteira_esta_nula():
    """
    Com a meta 100% nula, a mediana global tambem e NaN: a cascata entrega uma
    feature inteiramente nula ao modelo sem quebrar nada. Falhar alto e o
    comportamento certo — e dado AUSENTE, nao dado imputado.
    """
    df = _territorio({"SP": [None, None], "RR": [None]})

    with pytest.raises(ValueError, match="seguem sem meta"):
        mt.imputar_meta(df.copy())
