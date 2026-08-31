"""
A infraestrutura explica o NIVEL de alfabetizacao, ou o FURO DA META? (ADR-0011)

POR QUE ESTE SCRIPT EXISTE
--------------------------
O experimento (`08_experimento_infra_escolar.py`) mediu se a infraestrutura
ajuda a prever `y = (taxa24 < meta_2024)` e deu MISTO/negativo. Mas
"nao ajuda a prever o furo da meta" NAO e o mesmo que "nao tem relacao com
alfabetizacao" — sao alvos diferentes:

  - `taxa23` e o NIVEL de alfabetizacao do municipio.
  - `y` e furar uma meta MOVEL, que o ADR-0005 mostrou depender de mecanismo
    estadual (regressao a media em MG, teto de 80,0 no CE). Um municipio com
    alfabetizacao alta pode furar a meta por ela ter subido junto.

Confundir os dois seria concluir "infraestrutura escolar nao importa para
alfabetizacao" a partir de um teste que nunca perguntou isso. Este script
separa as duas perguntas.

O QUE ELE MEDE, E POR QUE INTRA-UF TAMBEM
------------------------------------------
A mesma armadilha que derrubou o modelo municipal NACIONAL do projeto
(README: "Leave-One-UF-Out em 0,4800, abaixo do acaso: o 'sinal' era a regua
estadual") vale aqui. Correlacao nacional entre infra e alfabetizacao pode
ser efeito ECOLOGICO: estados mais ricos tem, ao mesmo tempo, melhor
infraestrutura E maior alfabetizacao — sem que uma coisa explique a outra
DENTRO do estado. Por isso toda medida sai duas vezes: nacional e intra-UF.

CORRECAO DE COMPARACOES MULTIPLAS
----------------------------------
6 testes de hipotese (3 indices x 2 alvos) informando a mesma conclusao.
Gate de `.claude/rules/dados.md`: p-valor sai com correcao de Holm ao lado do
bruto.

USO
    python src/evaluation/06_infra_nivel_vs_meta.py
"""
import importlib.util
import json
import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats
from sklearn.linear_model import LinearRegression

warnings.filterwarnings("ignore")
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BASE = Path(__file__).resolve().parents[2]
_spec = importlib.util.spec_from_file_location(
    "ranking_intra_uf", BASE / "src" / "modeling" / "04_ranking_intra_uf.py")
riu = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(riu)


def fmt_p(p: float) -> str:
    """
    p=0.0 exato e underflow de ponto flutuante, nao um p-valor. Reportar
    "0.00e+00" afirmaria certeza que a aritmetica nao sustenta.
    """
    return "<1e-300" if p < 1e-300 else f"{p:.2e}"


def holm(pvals: list[float]) -> list[float]:
    """Holm-Bonferroni: p ajustado, controla FWER sem assumir independencia."""
    n = len(pvals)
    ordem = list(np.argsort(pvals))
    ajust = [0.0] * n
    maior = 0.0
    for rank, i in enumerate(ordem, start=1):
        maior = max(maior, pvals[i] * (n - rank + 1))
        ajust[i] = round(min(1.0, maior), 6)
    return ajust


def correlacoes_intra_uf(j: pd.DataFrame, col: str, alvo: str,
                          binario: bool) -> tuple[float, int]:
    """
    Media das correlacoes calculadas DENTRO de cada UF, ponderada por n.

    Nao e a correlacao nacional: a nacional mistura variacao entre estados
    (efeito ecologico) com variacao entre municipios do mesmo estado, e so a
    segunda e acionavel para o produto, que decide intra-UF.
    """
    rs, pesos = [], []
    for _, g in j.groupby("sigla_uf"):
        if len(g) < riu.MIN_MUNICIPIOS_POR_UF or g[alvo].nunique() < 2:
            continue
        r = (stats.pointbiserialr(g[alvo], g[col])[0] if binario
             else stats.pearsonr(g[col], g[alvo])[0])
        if np.isfinite(r):
            rs.append(r)
            pesos.append(len(g))
    return float(np.average(rs, weights=pesos)), len(rs)


def r2_intra_uf(j: pd.DataFrame, features: list[str], alvo: str) -> float:
    """R2 de um linear com os 3 indices, medido dentro de cada UF."""
    r2s, pesos = [], []
    for _, g in j.groupby("sigla_uf"):
        if len(g) < riu.MIN_MUNICIPIOS_POR_UF or g[alvo].nunique() < 2:
            continue
        X = g[features].to_numpy()
        r2s.append(LinearRegression().fit(X, g[alvo]).score(X, g[alvo]))
        pesos.append(len(g))
    return float(np.average(r2s, weights=pesos))


def main():
    print("=" * 74)
    print("INFRA explica o NIVEL de alfabetizacao, ou o FURO DA META? (ADR-0011)")
    print("=" * 74)

    m = riu.montar_dataset(com_infra=True)
    j = m.dropna(subset=riu.FEATURES_INFRA).copy()
    idx = riu.FEATURES_INFRA
    print(f"\nn = {len(j):,} municipios".replace(",", "."))

    linhas, pvals_brutos = [], []
    for c in idx:
        r_nivel, p_nivel = stats.pearsonr(j[c], j.taxa23)
        r_furo, p_furo = stats.pointbiserialr(j.y, j[c])
        linhas.append({"indice": c, "alvo": "nivel (taxa23)",
                        "r_nacional": round(float(r_nivel), 4), "p": float(p_nivel)})
        linhas.append({"indice": c, "alvo": "furo da meta (y)",
                        "r_nacional": round(float(r_furo), 4), "p": float(p_furo)})
        pvals_brutos += [float(p_nivel), float(p_furo)]

    p_holm = holm(pvals_brutos)
    for linha, ph in zip(linhas, p_holm):
        linha["p_holm"] = ph
        linha["p_holm_fmt"] = fmt_p(ph)

    for linha in linhas:
        col, alvo = linha["indice"], ("taxa23" if "nivel" in linha["alvo"] else "y")
        r_uf, n_uf = correlacoes_intra_uf(j, col, alvo, binario=(alvo == "y"))
        linha["r_intra_uf"] = round(r_uf, 4)
        linha["ufs_usadas"] = n_uf

    print("\nCORRELACAO — nacional vs intra-UF")
    print("-" * 74)
    print(f"{'indice':<22} {'alvo':<18} {'r nac.':>8} {'p(Holm)':>10} {'r intra-UF':>11}")
    print("-" * 74)
    for linha in linhas:
        print(f"{linha['indice']:<22} {linha['alvo']:<18} "
              f"{linha['r_nacional']:>+8.3f} {fmt_p(linha['p_holm']):>10} "
              f"{linha['r_intra_uf']:>+11.3f}")

    r2_nivel = r2_intra_uf(j, idx, "taxa23")
    r2_furo = r2_intra_uf(j, idx, "y")
    print("\nR2 intra-UF de um linear com os 3 indices:")
    print(f"  NIVEL (taxa23):     {r2_nivel:.4f}")
    print(f"  FURO DA META (y):   {r2_furo:.4f}")

    # queda da correlacao nacional -> intra-UF = tamanho do efeito ecologico
    quedas = [(l["indice"], l["r_nacional"], l["r_intra_uf"])
              for l in linhas if "nivel" in l["alvo"]]
    print("\nEFEITO ECOLOGICO (quanto da correlacao nacional some dentro da UF):")
    for nome, rn, ru in quedas:
        perda = (1 - abs(ru) / abs(rn)) if rn else float("nan")
        print(f"  {nome:<22} nacional {rn:+.3f} -> intra-UF {ru:+.3f} "
              f"({perda:.0%} do sinal era entre estados)")

    saida = {
        "adr": "ADR-0011",
        "pergunta": "infra explica o NIVEL de alfabetizacao ou o FURO DA META?",
        "n_municipios": int(len(j)),
        "correcao_multiplas": "Holm-Bonferroni, 6 testes (3 indices x 2 alvos)",
        "correlacoes": linhas,
        "r2_intra_uf": {"nivel_taxa23": round(r2_nivel, 4),
                         "furo_da_meta_y": round(r2_furo, 4)},
        "efeito_ecologico": [
            {"indice": n, "r_nacional": rn, "r_intra_uf": ru,
             "fracao_do_sinal_entre_estados": round(1 - abs(ru) / abs(rn), 4)}
            for n, rn, ru in quedas],
    }
    out = BASE / "reports" / "infra_nivel_vs_meta.json"
    out.write_text(json.dumps(saida, ensure_ascii=False, indent=2, default=float),
                    encoding="utf-8")
    print(f"\n  {out}")


if __name__ == "__main__":
    main()
