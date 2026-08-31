"""
EXPERIMENTO — a infraestrutura escolar fecha alguma UF inconclusiva? (ADR-0011)

POR QUE ESTE SCRIPT EXISTE (e nao apenas alterar 04_ranking_intra_uf.py)
--------------------------------------------------------------------------
Mesmo padrao de 06_experimento_idhm.py: aqui e onde MEDIMOS se o
enriquecimento vale a pena, antes de promover a mudanca ao script de
producao. 04_ranking_intra_uf.py so muda se o resultado justificar, e o
backtest prospectivo 2025 (ADR-0010, imutavel) NAO e tocado por este script.

CRITERIO DE SUCESSO (ADR-0011 SS2) — duas metricas, nunca uma so
--------------------------------------------------------------------------
Mesma decisao do ADR-0005/0009 (ganho medio escondendo que vem de poucos
casos, ou escondendo regressao em UF individual):

  1. IC95% bootstrap pareado do AUC ponderado, COM infra vs SEM infra.
  2. Contagem de UFs que mudam de veredito — nas DUAS direcoes, nao so a
     favoravel.

PREDICAO REGISTRADA ANTES DA MEDICAO (AGENTS.md)
--------------------------------------------------------------------------
Registrada em reports/dicionario_censo_escolar.md em 2026-08-31, antes da
primeira execucao:

  - Evidencia previa (EDA SS8): AUC intra-UF isolada dos 3 indices entre
    0,4885 e 0,4981 — colada em 0,5. Informacao genuinamente nova
    (r ~ 0,02-0,08 com populacao_total), mas sem sinal univariado.
  - Predicao do Luiz: POSITIVO — ao menos 1 UF sai de inconclusivo para
    modelo_vence, nenhuma regride.

CRITERIO DE FALSIFICACAO
--------------------------------------------------------------------------
Se o IC bootstrap pareado nao for positivo com significancia E nenhuma UF
sair de 'inconclusivo', o achado e NEGATIVO — registrado como tal, mesmo
tratamento dado ao modelo aluno-nivel e ao IDHM (resultado negativo e
entregavel valido neste projeto).

USO
    python src/modeling/08_experimento_infra_escolar.py
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

# Ordem de forca de veredito (pior -> melhor). Existe para classificar QUALQUER
# mudanca, nao so o caso feliz "inconclusivo -> vence". O bug corrigido em
# 2026-08-29 no experimento do IDHM (so contava melhora, deixava passar
# "inconclusivo -> perde") e o mesmo genero de erro que o ADR-0005 pegou uma
# vez: metrica agregada escondendo o que acontece UF a UF.
FORCA = {"modelo_perde": 0, "inconclusivo": 1, "modelo_vence": 2}


def comparar_pareado_entre_modelos(ranked_a: pd.DataFrame, ranked_b: pd.DataFrame,
                                    n_boot: int = N_BOOT, seed: int = RANDOM_STATE
                                    ) -> dict[str, dict]:
    """
    IC95% bootstrap PAREADO de (modelo_b - modelo_a), por UF — mesma logica de
    riu.comparar_pareado(), mas comparando dois MODELOS entre si (com e sem
    infra) em vez de modelo vs baseline trivial.

    Pareado importa: os dois modelos pontuam os MESMOS municipios, entao a
    reamostragem precisa sortear o municipio uma vez e avaliar os dois nele —
    comparar dois IC independentes esconderia a correlacao e daria intervalo
    mais largo que o real.
    """
    rng = np.random.default_rng(seed)
    resultado = {}
    a_por_uf = {uf: g for uf, g in ranked_a.groupby("sigla_uf")}
    b_por_uf = {uf: g for uf, g in ranked_b.groupby("sigla_uf")}
    for uf in a_por_uf:
        if uf not in b_por_uf:
            continue
        ga = a_por_uf[uf].set_index("id_municipio")
        gb = b_por_uf[uf].set_index("id_municipio")
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
            "auc_sem_infra": round(float(roc_auc_score(y, sa)), 4),
            "auc_com_infra": round(float(roc_auc_score(y, sb)), 4),
            "diferenca_ic95": [round(float(lo), 4), round(float(hi), 4)],
            "veredito_infra": ("infra_ajuda" if lo > 0 else
                                "infra_atrapalha" if hi < 0 else "sem_diferenca"),
        }
    return resultado


def classificar_resultado(melhorou: dict, piorou: dict) -> str:
    """
    MISTO e categoria legitima — nao forcar positivo/negativo quando ha melhora
    E piora ao mesmo tempo. Foi o desfecho real do IDHM (ADR-0009 SS8), e a
    formulacao binaria original nao cobria.
    """
    if melhorou and not piorou:
        return "positivo"
    if piorou and not melhorou:
        return "negativo"
    if melhorou and piorou:
        return "misto"
    return "negativo"  # nenhuma mudanca de veredito


def main():
    print("=" * 74)
    print("EXPERIMENTO — infraestrutura escolar fecha UFs inconclusivas? (ADR-0011)")
    print("=" * 74)
    print("\nPREDICAO REGISTRADA ANTES (reports/dicionario_censo_escolar.md):")
    print("  Luiz previu POSITIVO — ao menos 1 UF sai de inconclusivo para")
    print("  modelo_vence, nenhuma regride.")
    print("  Evidencia previa da EDA: AUC intra-UF isolada dos 3 indices entre")
    print("  0,4885 e 0,4981 (colada em 0,5).")

    print("\n[1/4] Montando dataset SEM infra (baseline atual)...")
    m_sem = riu.montar_dataset(com_infra=False)
    ranked_sem, metricas_sem = riu.treinar_por_uf(m_sem, features=riu.FEATURES_BASE)
    riu.prever_direcao_loo(metricas_sem)
    riu.comparar_pareado(ranked_sem, metricas_sem)

    print("\n[2/4] Montando dataset COM infra...")
    m_com = riu.montar_dataset(com_infra=True)
    features_com = riu.FEATURES_BASE + riu.FEATURES_INFRA
    ranked_com, metricas_com = riu.treinar_por_uf(m_com, features=features_com)
    riu.prever_direcao_loo(metricas_com)
    riu.comparar_pareado(ranked_com, metricas_com)

    print("\n[3/4] Comparando os dois modelos, pareado por UF...")
    comparacao = comparar_pareado_entre_modelos(ranked_sem, ranked_com)

    print("\n[4/4] Apurando resultado...\n")
    vereditos_sem = {m["uf"]: m["veredito"] for m in metricas_sem}
    vereditos_com = {m["uf"]: m["veredito"] for m in metricas_com}

    todas_mudancas = {uf: (vereditos_sem[uf], vereditos_com[uf])
                       for uf in vereditos_sem
                       if vereditos_sem[uf] != vereditos_com.get(uf)}
    melhorou = {uf: (a, b) for uf, (a, b) in todas_mudancas.items()
                if FORCA[b] > FORCA[a]}
    piorou = {uf: (a, b) for uf, (a, b) in todas_mudancas.items()
              if FORCA[b] < FORCA[a]}
    mudou_para_vence = [uf for uf, (a, b) in melhorou.items() if b == "modelo_vence"]
    mudou_para_perde = [uf for uf, (a, b) in piorou.items() if b == "modelo_perde"]

    infra_ajuda = [uf for uf, r in comparacao.items()
                   if r["veredito_infra"] == "infra_ajuda"]
    infra_atrapalha = [uf for uf, r in comparacao.items()
                       if r["veredito_infra"] == "infra_atrapalha"]

    dfm_sem = pd.DataFrame(metricas_sem)
    dfm_com = pd.DataFrame(metricas_com)
    peso = dfm_sem.n_municipios
    auc_pond_sem = float(np.average(dfm_sem.auc_modelo, weights=peso))
    auc_pond_com = float(np.average(
        dfm_com.set_index("uf").loc[dfm_sem.uf, "auc_modelo"], weights=peso))

    print(f"  AUC ponderado SEM infra: {auc_pond_sem:.4f}")
    print(f"  AUC ponderado COM infra: {auc_pond_com:.4f}")
    print(f"  Diferenca: {auc_pond_com - auc_pond_sem:+.4f}")
    print()
    print(f"  UFs onde infra ajuda (IC positivo):     {len(infra_ajuda)}  "
          f"{' '.join(infra_ajuda)}")
    print(f"  UFs onde infra atrapalha (IC negativo): {len(infra_atrapalha)}  "
          f"{' '.join(infra_atrapalha)}")
    print(f"  UFs sem diferenca detectavel:           "
          f"{len(comparacao) - len(infra_ajuda) - len(infra_atrapalha)}")
    print()
    print(f"  TODAS as mudancas de veredito ({len(todas_mudancas)} UFs):")
    if not todas_mudancas:
        print("    (nenhuma)")
    for uf, (a, b) in sorted(todas_mudancas.items()):
        seta = "melhora" if uf in melhorou else "piora"
        print(f"    {uf}: {a} -> {b}  ({seta})")
    print()
    print(f"  Fechou (inconclusivo -> modelo_vence): {len(mudou_para_vence)}  "
          f"{' '.join(mudou_para_vence)}")
    print(f"  Regrediu para modelo_perde:            {len(mudou_para_perde)}  "
          f"{' '.join(mudou_para_perde)}")
    print()

    resultado = classificar_resultado(melhorou, piorou)
    rotulo = {
        "positivo": "POSITIVO — so melhoras, nenhuma UF piorou de veredito.",
        "negativo": "NEGATIVO — sem melhora liquida (ADR-0011, criterio de "
                    "falsificacao).",
        "misto": "MISTO — melhora em algumas UFs, piora em outras. Nao e "
                 "vitoria limpa nem derrota limpa.",
    }
    print(f"  RESULTADO: {rotulo[resultado]}")
    print(f"  PREDICAO ERA: positivo  ->  "
          f"{'ACERTOU' if resultado == 'positivo' else 'ERROU'}")

    saida = {
        "adr": "ADR-0011",
        "criterio_sucesso": "duas metricas separadas, nunca uma so",
        "predicao_registrada_antes": {
            "quem": "Luiz",
            "valor": "positivo",
            "onde": "reports/dicionario_censo_escolar.md",
            "evidencia_previa": "AUC intra-UF isolada dos indices 0,4885-0,4981",
            "acertou": resultado == "positivo",
        },
        "features_infra": riu.FEATURES_INFRA,
        "auc_ponderado_sem_infra": round(auc_pond_sem, 4),
        "auc_ponderado_com_infra": round(auc_pond_com, 4),
        "diferenca_auc_ponderado": round(auc_pond_com - auc_pond_sem, 4),
        "ufs_infra_ajuda": infra_ajuda,
        "ufs_infra_atrapalha": infra_atrapalha,
        "todas_mudancas_de_veredito": {uf: {"antes": a, "depois": b}
                                        for uf, (a, b) in todas_mudancas.items()},
        "ufs_mudou_para_vence": mudou_para_vence,
        "ufs_mudou_para_perde": mudou_para_perde,
        "resultado": resultado,
        "comparacao_por_uf": comparacao,
        "metricas_sem_infra": metricas_sem,
        "metricas_com_infra": metricas_com,
    }
    out = BASE / "reports" / "experimento_infra_escolar.json"
    out.write_text(json.dumps(saida, ensure_ascii=False, indent=2, default=float),
                    encoding="utf-8")
    print(f"\n  {out}")


if __name__ == "__main__":
    main()
