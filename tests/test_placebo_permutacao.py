"""
Teste de unidade para src/modeling/09_placebo_permutacao.py.

POR QUE ESTE ARQUIVO EXISTE
----------------------------
`permutar_dentro_da_uf` define o NULO do teste de placebo. Se ela permutar
errado, o placebo mede outra coisa e o veredito sobre os enriquecimentos
(ADR-0009/0011) fica sem base — e nada quebra visivelmente: a saida continua
plausivel. Os modos de falha silenciosa que os testes abaixo cobrem:

  - permutar ENTRE UFs (destruiria a estrutura estadual, nulo errado);
  - permutar cada coluna em separado (destruiria a correlacao entre os
    indices, testando um nulo mais fraco que o pretendido);
  - nao permutar nada (placebo sempre "confirma" que ruido nao muda nada).
"""
import importlib.util
from pathlib import Path

import numpy as np
import pandas as pd

BASE = Path(__file__).resolve().parents[1]

spec = importlib.util.spec_from_file_location(
    "placebo_permutacao", BASE / "src" / "modeling" / "09_placebo_permutacao.py")
pp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pp)

COLS = ["a", "b"]


def _df(n_por_uf=6):
    linhas = []
    for uf in ("SP", "MG"):
        for i in range(n_por_uf):
            linhas.append({"sigla_uf": uf, "id": f"{uf}{i}",
                            "a": float(i), "b": float(i * 10)})
    return pd.DataFrame(linhas)


def test_permutacao_preserva_o_conjunto_de_valores_dentro_da_uf():
    """Mesmos valores, so trocados de lugar — marginal intacta por UF."""
    df = _df()
    out = pp.permutar_dentro_da_uf(df, COLS, seed=1)
    for uf in ("SP", "MG"):
        for c in COLS:
            antes = sorted(df.loc[df.sigla_uf == uf, c])
            depois = sorted(out.loc[out.sigla_uf == uf, c])
            assert antes == depois


def test_permutacao_nao_move_valor_entre_ufs():
    """
    SP tem a=0..5 e MG tambem; para detectar vazamento entre UFs, usa faixas
    disjuntas — se um valor de MG aparecer em SP, o nulo estaria errado.
    """
    df = _df()
    df.loc[df.sigla_uf == "MG", "a"] += 100
    out = pp.permutar_dentro_da_uf(df, COLS, seed=2)
    assert (out.loc[out.sigla_uf == "SP", "a"] < 100).all()
    assert (out.loc[out.sigla_uf == "MG", "a"] >= 100).all()


def test_permutacao_mantem_as_colunas_juntas():
    """
    b = a * 10 por construcao. Se cada coluna fosse permutada em separado, a
    relacao se romperia — e o nulo testaria algo mais facil de rejeitar.
    """
    df = _df()
    out = pp.permutar_dentro_da_uf(df, COLS, seed=3)
    assert np.allclose(out["b"].to_numpy(), out["a"].to_numpy() * 10)


def test_permutacao_realmente_embaralha():
    """Guarda contra o pior modo de falha: placebo que nao permuta nada."""
    df = _df(n_por_uf=30)
    out = pp.permutar_dentro_da_uf(df, COLS, seed=4)
    assert not np.allclose(df["a"].to_numpy(), out["a"].to_numpy())


def test_permutacao_e_deterministica_com_mesma_seed():
    df = _df()
    a = pp.permutar_dentro_da_uf(df, COLS, seed=7)
    b = pp.permutar_dentro_da_uf(df, COLS, seed=7)
    assert a.equals(b)


def test_seeds_diferentes_dao_permutacoes_diferentes():
    df = _df(n_por_uf=30)
    a = pp.permutar_dentro_da_uf(df, COLS, seed=7)
    b = pp.permutar_dentro_da_uf(df, COLS, seed=8)
    assert not a.equals(b)


def test_uf_com_um_municipio_nao_quebra():
    df = pd.DataFrame([{"sigla_uf": "AP", "id": "x", "a": 1.0, "b": 10.0}])
    out = pp.permutar_dentro_da_uf(df, COLS, seed=9)
    assert out.loc[0, "a"] == 1.0


def test_colunas_fora_da_lista_nao_sao_tocadas():
    df = _df()
    out = pp.permutar_dentro_da_uf(df, ["a"], seed=5)
    assert list(out["b"]) == list(df["b"])
    assert list(out["id"]) == list(df["id"])


# --- apurar_mudancas: as duas direcoes, nunca so a favoravel ---------------

def test_apurar_mudancas_conta_melhora_e_piora():
    base = {"SP": "inconclusivo", "MG": "modelo_vence", "BA": "inconclusivo"}
    novo = {"SP": "modelo_vence", "MG": "inconclusivo", "BA": "inconclusivo"}
    mud = pp.apurar_mudancas(base, novo)
    assert mud == {"SP": ("inconclusivo", "modelo_vence"),
                    "MG": ("modelo_vence", "inconclusivo")}


def test_apurar_mudancas_ignora_uf_ausente_no_novo():
    base = {"SP": "inconclusivo", "AP": "inconclusivo"}
    novo = {"SP": "modelo_vence"}
    assert set(pp.apurar_mudancas(base, novo)) == {"SP"}


# --- bh_fdr ----------------------------------------------------------------

def test_bh_fdr_nao_diminui_p_valor():
    """Correcao para comparacoes multiplas so pode aumentar (ou manter) o p."""
    p = [0.01, 0.04, 0.03, 0.20]
    ajust = pp.bh_fdr(p)
    assert all(a >= b - 1e-9 for a, b in zip(ajust, p))


def test_bh_fdr_preserva_ordem():
    p = [0.001, 0.5, 0.02]
    ajust = pp.bh_fdr(p)
    assert np.argsort(ajust).tolist() == np.argsort(p).tolist()


def test_bh_fdr_limita_em_1():
    assert all(a <= 1.0 for a in pp.bh_fdr([0.9, 0.95, 0.99]))
