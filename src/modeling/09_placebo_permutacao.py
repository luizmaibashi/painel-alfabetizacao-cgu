"""
PLACEBO — as mudancas de veredito sobrevivem a features SEM informacao?

POR QUE ESTE SCRIPT EXISTE
--------------------------
Dois enriquecimentos sem relacao entre si produziram o MESMO padrao:

  | UF | IDHM (socioeconomico, 2010)  | INFRA (escolar, 2023)        |
  |----|------------------------------|------------------------------|
  | BA | inconclusivo -> modelo_perde | inconclusivo -> modelo_perde |
  | PE | inconclusivo -> modelo_vence | inconclusivo -> modelo_vence |

IDHM e infra correlacionam r ~ 0,02-0,08 entre si — carregam informacao
diferente. Se mesmo assim mexem nas MESMAS UFs, a hipotese incomoda e que a
mudanca nao vem da INFORMACAO das variaveis, e sim do ato de ADICIONAR
DIMENSAO: UFs cujo IC bootstrap ja estava encostado no zero atravessam a
fronteira com qualquer perturbacao.

Se for isso, o "PE fechou" de AMBOS os experimentos e artefato, nao achado —
e promover qualquer um dos dois a producao seria vender ruido como sinal.

O DESENHO DO NULO (por que permutacao, e nao ruido gaussiano)
--------------------------------------------------------------
Ruido gaussiano testaria um nulo mais fraco: features com distribuicao
diferente das reais. A permutacao DENTRO DA UF preserva exatamente:

  - a distribuicao marginal de cada indice (mesmos valores, so trocados);
  - a correlacao ENTRE os 3 indices (mesma permutacao aplicada as 3 colunas);
  - a estrutura entre UFs (permuta so dentro de cada estado).

E destroi exatamente uma coisa: o vinculo municipio -> y. E o nulo certo para
a pergunta "a informacao importa, ou so a dimensao?".

O que varia entre replicacoes e SO a permutacao. O `random_state` do
RandomForest fica fixo — senao a estocasticidade do modelo se confundiria
com o efeito que estamos medindo.

CORRECAO DE COMPARACOES MULTIPLAS
----------------------------------
23 UFs testadas simultaneamente (gate de `.claude/rules/dados.md`). A taxa de
flip por UF sai com Benjamini-Hochberg (FDR) alem do p bruto — sem isso,
alguma UF apareceria "significativa" so por rodar 23 testes.

USO
    python src/modeling/09_placebo_permutacao.py [n_replicacoes]
"""
import importlib.util
import json
import sys
import time
import warnings
from collections import Counter
from pathlib import Path

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BASE = Path(__file__).resolve().parents[2]

_spec = importlib.util.spec_from_file_location(
    "ranking_intra_uf", BASE / "src" / "modeling" / "04_ranking_intra_uf.py")
riu = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(riu)

FORCA = {"modelo_perde": 0, "inconclusivo": 1, "modelo_vence": 2}
N_REPLICACOES_PADRAO = 20


def permutar_dentro_da_uf(m: pd.DataFrame, colunas: list[str],
                           seed: int) -> pd.DataFrame:
    """
    Embaralha as colunas dentro de cada UF, mantendo o bloco de colunas junto.

    A MESMA permutacao vale para todas as colunas da lista: embaralhar cada
    uma por conta propria destruiria tambem a correlacao ENTRE os indices, o
    que testaria um nulo diferente (e mais facil de rejeitar) do pretendido.
    """
    rng = np.random.default_rng(seed)
    out = m.copy()
    for _, idx in out.groupby("sigla_uf").groups.items():
        idx = np.asarray(idx)
        if len(idx) < 2:
            continue
        perm = rng.permutation(len(idx))
        out.loc[idx, colunas] = out.loc[idx[perm], colunas].to_numpy()
    return out


def apurar_mudancas(vereditos_base: dict, vereditos_novo: dict) -> dict:
    """Mudancas de veredito nas DUAS direcoes (nunca so a favoravel)."""
    return {uf: (vereditos_base[uf], vereditos_novo[uf])
            for uf in vereditos_base
            if uf in vereditos_novo and vereditos_base[uf] != vereditos_novo[uf]}


def auc_ponderado(metricas: list[dict]) -> float:
    df = pd.DataFrame(metricas)
    return float(np.average(df.auc_modelo, weights=df.n_municipios))


def rodar_uma_replicacao(m_com_infra: pd.DataFrame, vereditos_base: dict,
                          seed: int) -> dict:
    """Uma permutacao -> um conjunto de mudancas de veredito."""
    m_perm = permutar_dentro_da_uf(m_com_infra, riu.FEATURES_INFRA, seed)
    features = riu.FEATURES_BASE + riu.FEATURES_INFRA
    ranked, metricas = riu.treinar_por_uf(m_perm, features=features)
    riu.prever_direcao_loo(metricas)
    riu.comparar_pareado(ranked, metricas)

    vereditos = {x["uf"]: x["veredito"] for x in metricas}
    mud = apurar_mudancas(vereditos_base, vereditos)
    return {
        "seed": seed,
        "auc_ponderado": round(auc_ponderado(metricas), 4),
        "mudancas": {uf: {"antes": a, "depois": b} for uf, (a, b) in mud.items()},
        "n_mudancas": len(mud),
        "n_melhora": sum(1 for a, b in mud.values() if FORCA[b] > FORCA[a]),
        "n_piora": sum(1 for a, b in mud.values() if FORCA[b] < FORCA[a]),
    }


def bh_fdr(pvals: list[float]) -> list[float]:
    """Benjamini-Hochberg: p-valor ajustado por FDR."""
    n = len(pvals)
    ordem = list(np.argsort(pvals))
    ajust = [1.0] * n
    menor = 1.0
    for rank, i in enumerate(reversed(ordem), start=1):
        pos = n - rank + 1
        menor = min(menor, pvals[i] * n / pos)
        ajust[i] = round(min(1.0, menor), 4)
    return ajust


def main():
    n_rep = int(sys.argv[1]) if len(sys.argv) > 1 else N_REPLICACOES_PADRAO
    print("=" * 74)
    print(f"PLACEBO — permutacao dentro da UF, {n_rep} replicacoes")
    print("=" * 74)

    print("\n[1/3] Baseline SEM infra (referencia de veredito)...")
    m_sem = riu.montar_dataset(com_infra=False)
    ranked_base, metricas_base = riu.treinar_por_uf(m_sem, features=riu.FEATURES_BASE)
    riu.prever_direcao_loo(metricas_base)
    riu.comparar_pareado(ranked_base, metricas_base)
    vereditos_base = {x["uf"]: x["veredito"] for x in metricas_base}
    n_inconc = sum(1 for v in vereditos_base.values() if v == "inconclusivo")
    print(f"  {len(vereditos_base)} UFs, {n_inconc} inconclusivas")

    print("\n[2/3] Dataset com infra (valores reais, a permutar)...")
    m_com = riu.montar_dataset(com_infra=True)

    print(f"\n[3/3] Rodando {n_rep} permutacoes...")
    reps, t0 = [], time.time()
    for i in range(n_rep):
        r = rodar_uma_replicacao(m_com, vereditos_base, seed=1000 + i)
        reps.append(r)
        ufs_str = " ".join(sorted(r["mudancas"])) or "-"
        print(f"  rep {i+1:>2}/{n_rep}  AUC={r['auc_ponderado']:.4f}  "
              f"mudancas={r['n_mudancas']} (+{r['n_melhora']}/-{r['n_piora']})  "
              f"{ufs_str:<20} [{time.time()-t0:.0f}s]")

    n_mud = [r["n_mudancas"] for r in reps]
    aucs = [r["auc_ponderado"] for r in reps]
    flips: Counter = Counter()
    flips_direcao: dict = {}
    for r in reps:
        for uf, d in r["mudancas"].items():
            flips[uf] += 1
            chave = f"{d['antes']}->{d['depois']}"
            flips_direcao.setdefault(uf, Counter())[chave] += 1

    obs = json.loads((BASE / "reports" / "experimento_infra_escolar.json")
                      .read_text(encoding="utf-8"))
    obs_mud = obs["todas_mudancas_de_veredito"]
    obs_n = len(obs_mud)
    obs_auc = obs["auc_ponderado_com_infra"]

    p_n = float(np.mean([x >= obs_n for x in n_mud]))
    p_auc = float(np.mean([a >= obs_auc for a in aucs]))

    ufs = sorted(set(flips) | set(obs_mud))
    # p com correcao de continuidade (+1): com n_rep finito, p=0 exato afirmaria
    # impossibilidade que 20 replicacoes nao sustentam.
    pvals = [(flips[uf] + 1) / (n_rep + 1) for uf in ufs]
    padj = bh_fdr(pvals)

    print("\n" + "=" * 74)
    print("DISTRIBUICAO NULA vs OBSERVADO")
    print("=" * 74)
    print(f"\n  Mudancas de veredito sob permutacao (n={n_rep}):")
    print(f"    media {np.mean(n_mud):.2f}   mediana {np.median(n_mud):.1f}   "
          f"min {min(n_mud)}   max {max(n_mud)}")
    print(f"    distribuicao: {dict(sorted(Counter(n_mud).items()))}")
    print(f"\n  OBSERVADO com infra REAL: {obs_n} mudancas")
    print(f"    P(>= {obs_n} mudancas | sem informacao) = {p_n:.3f}")
    print(f"\n  AUC ponderado sob permutacao: media {np.mean(aucs):.4f}  "
          f"[{min(aucs):.4f}, {max(aucs):.4f}]")
    print(f"  AUC ponderado com infra REAL: {obs_auc:.4f}")
    print(f"    P(AUC do nulo >= AUC observado) = {p_auc:.3f}")

    print(f"\n  FLIP POR UF ({n_rep} replicacoes):")
    print(f"    {'UF':<4} {'flips':>5} {'taxa':>6} {'p':>6} {'p(BH)':>7}  "
          f"{'observado c/ infra real':<30} dominante sob nulo")
    for uf, p, pa in sorted(zip(ufs, pvals, padj), key=lambda t: -flips[t[0]]):
        o = (f"{obs_mud[uf]['antes']}->{obs_mud[uf]['depois']}"
             if uf in obs_mud else "-")
        dom, qtd = (flips_direcao[uf].most_common(1)[0]
                    if uf in flips_direcao else ("-", 0))
        print(f"    {uf:<4} {flips[uf]:>5} {flips[uf]/n_rep:>5.0%} "
              f"{p:>6.3f} {pa:>7.3f}  {o:<30} {dom} ({qtd}x)")

    saida = {
        "desenho": "permutacao dentro da UF; mesma permutacao para as 3 colunas",
        "n_replicacoes": n_rep,
        "features_permutadas": riu.FEATURES_INFRA,
        "nulo": {
            "n_mudancas_por_replicacao": n_mud,
            "media_n_mudancas": round(float(np.mean(n_mud)), 3),
            "auc_ponderado_por_replicacao": aucs,
            "media_auc": round(float(np.mean(aucs)), 4),
            "flips_por_uf": dict(flips),
            "direcao_por_uf": {u: dict(c) for u, c in flips_direcao.items()},
        },
        "observado_infra_real": {"n_mudancas": obs_n, "mudancas": obs_mud,
                                  "auc_ponderado": obs_auc},
        "p_valores": {
            "p_n_mudancas": round(p_n, 4),
            "p_auc": round(p_auc, 4),
            "por_uf": {uf: {"p": round(p, 4), "p_bh": pa}
                        for uf, p, pa in zip(ufs, pvals, padj)},
            "correcao": "Benjamini-Hochberg (FDR); p com correcao de continuidade",
        },
    }
    out = BASE / "reports" / "placebo_permutacao.json"
    out.write_text(json.dumps(saida, ensure_ascii=False, indent=2, default=float),
                    encoding="utf-8")
    print(f"\n  {out}")


if __name__ == "__main__":
    main()
