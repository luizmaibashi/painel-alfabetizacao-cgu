"""
EXPERIMENTO — o IDHM-M fecha alguma das 17 UFs inconclusivas? (ADR-0009)

POR QUE ESTE SCRIPT EXISTE (e nao apenas alterar 04_ranking_intra_uf.py)
--------------------------------------------------------------------------
Mesmo padrao de 03_experimento_municipio_meta.py: aqui e onde MEDIMOS se o
enriquecimento vale a pena, antes de promover a mudanca ao script de
producao. 04_ranking_intra_uf.py so muda se o resultado justificar.

CRITERIO DE SUCESSO (ADR-0009 SS2) — duas metricas, nunca uma so
--------------------------------------------------------------------------
Decisao explicita para nao repetir o erro que o ADR-0005 ja corrigiu uma vez
neste projeto (ganho medio escondendo que vem de poucos casos):

  1. IC95% bootstrap pareado do AUC ponderado, modelo COM IDHM vs modelo
     ATUAL (sem IDHM) — mesma UF, mesmo split, mesma metodologia de
     comparar_pareado() de 04_ranking_intra_uf.py.
  2. Contagem de UFs que mudam de veredito 'inconclusivo' -> 'modelo_vence'
     (e o inverso, se acontecer — perder cobertura seria regressao).

CRITERIO DE FALSIFICACAO
--------------------------------------------------------------------------
Se o IC bootstrap pareado nao for positivo com significancia E nenhuma UF
sair de 'inconclusivo', o achado e NEGATIVO — registrado como tal, mesmo
tratamento dado ao modelo aluno-nivel (resultado negativo e entregavel
valido neste projeto).

USO
    python src/modeling/06_experimento_idhm.py
"""
import importlib.util
import json
import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score

warnings.filterwarnings("ignore")
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BASE = Path(__file__).resolve().parents[2]

_spec = importlib.util.spec_from_file_location(
    "ranking_intra_uf", BASE / "src" / "modeling" / "04_ranking_intra_uf.py")
riu = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(riu)

RANDOM_STATE = riu.RANDOM_STATE
N_BOOT = riu.N_BOOT


def comparar_pareado_entre_modelos(ranked_a: pd.DataFrame, ranked_b: pd.DataFrame,
                                    n_boot: int = N_BOOT, seed: int = RANDOM_STATE
                                    ) -> dict[str, dict]:
    """
    IC95% bootstrap PAREADO de (modelo_b - modelo_a), por UF — mesma logica
    de riu.comparar_pareado(), mas comparando dois MODELOS entre si (com e
    sem IDHM) em vez de modelo vs baseline trivial.
    """
    rng = np.random.default_rng(seed)
    resultado = {}
    a_por_uf = {uf: g for uf, g in ranked_a.groupby("sigla_uf")}
    b_por_uf = {uf: g for uf, g in ranked_b.groupby("sigla_uf")}
    for uf in a_por_uf:
        if uf not in b_por_uf:
            continue
        ga, gb = a_por_uf[uf], b_por_uf[uf]
        # mesma ordem de municipios nos dois (garantido por id_municipio)
        ga = ga.set_index("id_municipio")
        gb = gb.set_index("id_municipio")
        idx_comum = ga.index.intersection(gb.index)
        ga, gb = ga.loc[idx_comum], gb.loc[idx_comum]
        y = ga["y"].values
        sa, sb = ga["score_risco"].values, gb["score_risco"].values
        difs = []
        for _ in range(n_boot):
            i = rng.integers(0, len(y), len(y))
            if len(np.unique(y[i])) < 2:
                continue
            difs.append(roc_auc_score(y[i], sb[i]) - roc_auc_score(y[i], sa[i]))
        lo, hi = np.percentile(difs, [2.5, 97.5])
        resultado[uf] = {
            "auc_sem_idhm": round(float(roc_auc_score(y, sa)), 4),
            "auc_com_idhm": round(float(roc_auc_score(y, sb)), 4),
            "diferenca_ic95": [round(float(lo), 4), round(float(hi), 4)],
            "veredito_idhm": ("idhm_ajuda" if lo > 0 else
                               "idhm_atrapalha" if hi < 0 else "sem_diferenca"),
        }
    return resultado


def main():
    print("=" * 74)
    print("EXPERIMENTO — IDHM-M fecha UFs inconclusivas? (ADR-0009)")
    print("=" * 74)

    print("\n[1/4] Montando dataset SEM IDHM (baseline atual)...")
    m_sem = riu.montar_dataset(com_idhm=False)
    ranked_sem, metricas_sem = riu.treinar_por_uf(m_sem, features=riu.FEATURES_BASE)
    riu.prever_direcao_loo(metricas_sem)
    riu.comparar_pareado(ranked_sem, metricas_sem)

    print("\n[2/4] Montando dataset COM IDHM...")
    m_com = riu.montar_dataset(com_idhm=True)
    features_com = riu.FEATURES_BASE + riu.FEATURES_IDHM
    ranked_com, metricas_com = riu.treinar_por_uf(m_com, features=features_com)
    riu.prever_direcao_loo(metricas_com)
    riu.comparar_pareado(ranked_com, metricas_com)

    print("\n[3/4] Comparando os dois modelos, pareado por UF...")
    comparacao = comparar_pareado_entre_modelos(ranked_sem, ranked_com)

    print("\n[4/4] Apurando resultado...\n")
    vereditos_sem = {m["uf"]: m["veredito"] for m in metricas_sem}
    vereditos_com = {m["uf"]: m["veredito"] for m in metricas_com}

    # ORDEM de forca de veredito (pior -> melhor) para classificar QUALQUER
    # mudanca, nao so o caso feliz "inconclusivo -> vence". Bug corrigido em
    # 2026-08-29: a versao anterior so contava "vence->pior" como regressao e
    # deixava passar batido "inconclusivo->perde" (caso real do BA) — o
    # mesmo genero de erro que o ADR-0005 ja pegou uma vez neste projeto
    # (metrica agregada escondendo o que acontece UF a UF).
    FORCA = {"modelo_perde": 0, "inconclusivo": 1, "modelo_vence": 2}
    todas_mudancas = {uf: (vereditos_sem[uf], vereditos_com[uf])
                       for uf in vereditos_sem
                       if vereditos_sem[uf] != vereditos_com.get(uf)}
    melhorou = {uf: (a, b) for uf, (a, b) in todas_mudancas.items()
                if FORCA[b] > FORCA[a]}
    piorou = {uf: (a, b) for uf, (a, b) in todas_mudancas.items()
              if FORCA[b] < FORCA[a]}
    mudou_para_vence = [uf for uf, (a, b) in melhorou.items() if b == "modelo_vence"]
    mudou_para_perde = [uf for uf, (a, b) in piorou.items() if b == "modelo_perde"]

    idhm_ajuda = [uf for uf, r in comparacao.items() if r["veredito_idhm"] == "idhm_ajuda"]
    idhm_atrapalha = [uf for uf, r in comparacao.items() if r["veredito_idhm"] == "idhm_atrapalha"]

    dfm_sem = pd.DataFrame(metricas_sem)
    dfm_com = pd.DataFrame(metricas_com)
    peso = dfm_sem.n_municipios
    auc_pond_sem = float(np.average(dfm_sem.auc_modelo, weights=peso))
    auc_pond_com = float(np.average(dfm_com.set_index("uf").loc[dfm_sem.uf, "auc_modelo"],
                                     weights=peso))

    print(f"  AUC ponderado SEM IDHM: {auc_pond_sem:.4f}")
    print(f"  AUC ponderado COM IDHM: {auc_pond_com:.4f}")
    print(f"  Diferenca: {auc_pond_com - auc_pond_sem:+.4f}")
    print()
    print(f"  UFs onde IDHM ajuda (IC positivo):     {len(idhm_ajuda)}  {' '.join(idhm_ajuda)}")
    print(f"  UFs onde IDHM atrapalha (IC negativo): {len(idhm_atrapalha)}  {' '.join(idhm_atrapalha)}")
    print(f"  UFs sem diferenca detectavel:          "
          f"{len(comparacao) - len(idhm_ajuda) - len(idhm_atrapalha)}")
    print()
    print(f"  TODAS as mudancas de veredito ({len(todas_mudancas)} UFs):")
    for uf, (a, b) in sorted(todas_mudancas.items()):
        seta = "🟢 melhora" if uf in melhorou else "🔴 piora"
        print(f"    {uf}: {a} -> {b}  ({seta})")
    print()
    print(f"  Fechou (inconclusivo -> modelo_vence): {len(mudou_para_vence)}  "
          f"{' '.join(mudou_para_vence)}")
    print(f"  Regrediu para modelo_perde: {len(mudou_para_perde)}  "
          f"{' '.join(mudou_para_perde)}")
    print()

    # resultado MISTO e uma categoria legitima -- nao forcar positivo/negativo
    # quando ha melhora E piora ao mesmo tempo (ADR-0005: nunca esconder que
    # o ganho medio pode vir as custas de casos individuais piorando).
    if melhorou and not piorou:
        resultado = "positivo"
    elif piorou and not melhorou:
        resultado = "negativo"
    elif melhorou and piorou:
        resultado = "misto"
    else:
        resultado = "negativo"  # nenhuma mudanca de veredito

    rotulo = {"positivo": "POSITIVO — só melhoras, nenhuma UF piorou de veredito.",
              "negativo": "NEGATIVO — sem melhora líquida (ADR-0009, critério de falsificação).",
              "misto": "MISTO — melhora em algumas UFs, piora em outras. Não é "
                       "vitória limpa nem derrota limpa (ver tabela de mudanças acima)."}
    print(f"  RESULTADO: {rotulo[resultado]}")

    saida = {
        "criterio_sucesso": "ADR-0009 SS2 — duas metricas separadas, nunca uma so",
        "auc_ponderado_sem_idhm": round(auc_pond_sem, 4),
        "auc_ponderado_com_idhm": round(auc_pond_com, 4),
        "diferenca_auc_ponderado": round(auc_pond_com - auc_pond_sem, 4),
        "ufs_idhm_ajuda": idhm_ajuda,
        "ufs_idhm_atrapalha": idhm_atrapalha,
        "todas_mudancas_de_veredito": {uf: {"antes": a, "depois": b}
                                        for uf, (a, b) in todas_mudancas.items()},
        "ufs_mudou_para_vence": mudou_para_vence,
        "ufs_mudou_para_perde": mudou_para_perde,
        "resultado": resultado,
        "comparacao_por_uf": comparacao,
        "metricas_sem_idhm": metricas_sem,
        "metricas_com_idhm": metricas_com,
    }
    out = BASE / "reports" / "experimento_idhm.json"
    out.write_text(json.dumps(saida, ensure_ascii=False, indent=2, default=float),
                    encoding="utf-8")
    print(f"\n  {out}")


if __name__ == "__main__":
    main()
