"""
TESTE DE FALSIFICAÇÃO — o modelo aluno-nível vale mais que o baseline municipal?

POR QUE ESTE SCRIPT EXISTE
--------------------------
O ADR-0001 §5 define o critério que decide se a Fase 3 se justifica:

    "o modelo aluno-nível precisa SUPERAR o baseline trivial de aplicar
     `agg_priorizacao` (risco município-nível já existente na Fase 2)
     igualmente a todos os alunos do mesmo município. Sem superar esse
     baseline, o esforço técnico desta ADR não se justifica."

Esse critério foi escrito, documentado, citado em três lugares — e **nunca foi
executado**. É a quarta vez que o projeto encontra o mesmo padrão: a peça certa
existe e nada a consome. Este script é a peça que faltava.

A TESE SENDO TESTADA
--------------------
A Fase 2 respondia "quais MUNICÍPIOS priorizar" (cliente: Secretário/Prefeito).
A Fase 3 promete descer para "quais ALUNOS priorizar" (cliente: Coordenador
Pedagógico). Se o modelo de aluno não separa melhor que repetir o número do
município para todos os seus alunos, a promessa de descer de granularidade não
se sustenta — e a resposta honesta é continuar usando o mart da Fase 2.

O BASELINE
----------
`agg_priorizacao` é mart Gold da Fase 2, gerado por PySpark e mantido fora do
git (saída regenerável). Em vez de exigir o pipeline inteiro ou credencial GCP,
reconstruo aqui o **mesmo princípio** a partir dos próprios microdados:

    risco(aluno) = taxa de não-alfabetização do MUNICÍPIO dele no ano ANTERIOR

Usa t-1, então não vaza o ano sendo predito. É um proxy explícito do mart, não
o mart — e a diferença está declarada no relatório de saída.

O DESENHO
---------
Treina em 2023, prediz 2024 — o cenário real de uso (decidir hoje com o que se
sabia do ano passado), e o único em que o baseline municipal existe.

    treino:  alunos de 2023
    teste:   alunos de 2024
    modelo:  XGBoost com os hiperparâmetros vencedores do tournament
    baseline: taxa municipal de 2023, aplicada a todo aluno de 2024

COMO SE COMPARA
---------------
1. **ROC-AUC** — independente de corte, é a comparação mais limpa de "quem
   separa melhor".
2. **Recall@K (orçamento de busca ativa)** — a comparação que o negócio faz:
   *se dá para visitar K alunos, quantos em risco cada abordagem encontra?*
   Comparar Recall com corte fixo em 0,5 seria injusto, porque baseline e
   modelo produzem escalas diferentes; fixar K põe os dois no mesmo orçamento.
"""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score
from sklearn.pipeline import Pipeline
from xgboost import XGBClassifier

BASE = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(BASE / "src" / "preprocessing"))
from pipeline_preprocessamento import (  # noqa: E402
    COLUNA_TARGET, colunas_feature, construir_preprocessador,
)

RANDOM_STATE = 42
ANO_TREINO, ANO_TESTE = 2023, 2024
ORCAMENTOS = [0.05, 0.10, 0.20, 0.30, 0.50]  # fração dos alunos que dá para visitar

PARAMS_XGB = dict(
    n_estimators=400, max_depth=6, learning_rate=0.1,
    random_state=RANDOM_STATE, eval_metric="logloss", tree_method="hist", n_jobs=-1,
)


def carregar() -> pd.DataFrame:
    df = pd.read_parquet(BASE / "data" / "snapshot_modelagem.parquet")
    df["_y"] = (df[COLUNA_TARGET] == "Não").astype(int)
    return df


def baseline_municipal(df: pd.DataFrame) -> pd.Series:
    """
    Taxa de não-alfabetização do município no ano ANTERIOR, aplicada a cada
    aluno. Município sem dado de t-1 recebe a taxa global de t-1 (é o que um
    gestor faria: sem número local, usa a média nacional).
    """
    taxa_t1 = (
        df[df["ano"] == ANO_TREINO]
        .groupby("id_municipio")["_y"].mean()
        .rename("risco_municipal")
    )
    global_t1 = df.loc[df["ano"] == ANO_TREINO, "_y"].mean()
    return df["id_municipio"].map(taxa_t1).fillna(global_t1)


def recall_no_orcamento(y: np.ndarray, score: np.ndarray, fracao: float) -> dict:
    """Ordena por score decrescente, 'visita' os K primeiros, mede o que achou."""
    k = max(1, int(round(len(y) * fracao)))
    ordem = np.argsort(-score, kind="stable")[:k]
    achados = int(y[ordem].sum())
    total_risco = int(y.sum())
    return {
        "k": k,
        "achados": achados,
        "recall": achados / total_risco if total_risco else float("nan"),
        "precision": achados / k,
    }


def avaliar_populacao(df_pop: pd.DataFrame, df_ref: pd.DataFrame, rotulo: str) -> dict:
    """Roda o teste sobre uma população específica e devolve o resultado."""
    treino = df_pop[df_pop["ano"] == ANO_TREINO]
    teste = df_pop[df_pop["ano"] == ANO_TESTE].copy()
    feats = colunas_feature(df_pop)

    pipe = Pipeline([
        ("preprocessador", construir_preprocessador(treino[feats])),
        ("modelo", XGBClassifier(**PARAMS_XGB)),
    ])
    pipe.fit(treino[feats], treino["_y"])

    taxa_t1 = df_pop[df_pop["ano"] == ANO_TREINO].groupby("id_municipio")["_y"].mean()
    global_t1 = df_pop.loc[df_pop["ano"] == ANO_TREINO, "_y"].mean()

    y = teste["_y"].to_numpy()
    scores = {
        "modelo_aluno": pipe.predict_proba(teste[feats])[:, 1],
        "baseline_municipal": teste["id_municipio"].map(taxa_t1).fillna(global_t1).to_numpy(),
    }
    aucs = {n: float(roc_auc_score(y, sc)) for n, sc in scores.items()}
    return {"rotulo": rotulo, "n_treino": int(len(treino)), "n_teste": int(len(teste)),
            "taxa_risco": float(y.mean()), "roc_auc": aucs, "y": y, "scores": scores}


def main():
    df = carregar()
    treino = df[df["ano"] == ANO_TREINO]
    teste = df[df["ano"] == ANO_TESTE].copy()

    print("=" * 74)
    print("TESTE DE FALSIFICACAO (ADR-0001 secao 5)")
    print("=" * 74)
    print(f"Treino: {len(treino):,} alunos de {ANO_TREINO}".replace(",", "."))
    print(f"Teste:  {len(teste):,} alunos de {ANO_TESTE}".replace(",", "."))
    print(f"Taxa de risco no teste: {teste['_y'].mean():.1%}")

    # --- baseline: risco do municipio em t-1 ---
    teste["score_baseline"] = baseline_municipal(df).loc[teste.index]
    mun_t1 = set(df.loc[df["ano"] == ANO_TREINO, "id_municipio"])
    cobertos = teste["id_municipio"].isin(mun_t1)
    print(f"\nBaseline municipal: {cobertos.sum():,} de {len(teste):,} alunos "
          f"({cobertos.mean():.1%}) em municipio com dado de {ANO_TREINO}; "
          f"o resto recebe a taxa global.".replace(",", "."))

    # --- modelo aluno-nivel ---
    feats = colunas_feature(df)
    pipe = Pipeline([
        ("preprocessador", construir_preprocessador(treino[feats])),
        ("modelo", XGBClassifier(**PARAMS_XGB)),
    ])
    pipe.fit(treino[feats], treino["_y"])
    teste["score_modelo"] = pipe.predict_proba(teste[feats])[:, 1]

    # --- referencia trivial: ninguem discrimina nada ---
    rng = np.random.default_rng(RANDOM_STATE)
    teste["score_aleatorio"] = rng.random(len(teste))

    y = teste["_y"].to_numpy()
    abordagens = {
        "modelo_aluno (XGBoost)": teste["score_modelo"].to_numpy(),
        "baseline_municipal (taxa t-1)": teste["score_baseline"].to_numpy(),
        "aleatorio (referencia)": teste["score_aleatorio"].to_numpy(),
    }

    print("\n" + "=" * 74)
    print("1) PODER DE SEPARACAO (ROC-AUC, independente de corte)")
    print("=" * 74)
    aucs = {}
    for nome, score in abordagens.items():
        aucs[nome] = float(roc_auc_score(y, score))
        print(f"  {nome:<32} {aucs[nome]:.4f}")

    print("\n" + "=" * 74)
    print("2) BUSCA ATIVA: se da para visitar K alunos, quantos em risco se acha?")
    print("=" * 74)
    total_risco = int(y.sum())
    print(f"(alunos em risco no teste: {total_risco:,})\n".replace(",", "."))
    cab = f"{'orcamento':<12}{'K alunos':>10}" + "".join(
        f"{n.split(' ')[0][:14]:>16}" for n in abordagens)
    print(cab)
    print("-" * len(cab))
    por_orcamento = {}
    for frac in ORCAMENTOS:
        linha = {}
        for nome, score in abordagens.items():
            linha[nome] = recall_no_orcamento(y, score, frac)
        por_orcamento[f"{frac:.0%}"] = linha
        k = list(linha.values())[0]["k"]
        print(f"{frac:>10.0%}  {k:>10,}".replace(",", ".")
              + "".join(f"{v['recall']:>15.1%} " for v in linha.values()))

    # --- A ANALISE QUE DECIDE: so quem fez a prova ---
    # 16,8% da base tem rotulo por CONVENCAO (faltou => "Nao"), nao por medicao.
    # Incluir essas linhas mede a capacidade de detectar ausencia, nao de prever
    # alfabetizacao. A populacao honesta e a de quem foi avaliado.
    print(chr(10) + "=" * 74)
    print("3) A ANALISE QUE DECIDE: so alunos que FIZERAM a prova")
    print("=" * 74)
    print("Nos demais, o rotulo e convencao ('faltou => nao alfabetizado'), nao")
    print("medicao. Incluir essas linhas mede deteccao de ausencia." + chr(10))

    if "_ausente_no_exame" in df.columns:
        presentes = df[df["_ausente_no_exame"] == 0]
        r_pres = avaliar_populacao(presentes, df, "so presentes")
        print(f"  n_teste={r_pres['n_teste']:,} | risco={r_pres['taxa_risco']:.1%}"
              .replace(",", "."))
        for n, v in r_pres["roc_auc"].items():
            print(f"    {n:<24} ROC-AUC {v:.4f}")
        saida_presentes = {k: v for k, v in r_pres.items() if k not in ("y", "scores")}
    else:
        saida_presentes = None
        print("  coluna `_ausente_no_exame` ausente — rode a extracao de novo.")

    # --- veredito ---
    auc_modelo = aucs["modelo_aluno (XGBoost)"]
    auc_base = aucs["baseline_municipal (taxa t-1)"]
    delta = auc_modelo - auc_base
    vence_auc = auc_modelo > auc_base

    vitorias = sum(
        1 for l in por_orcamento.values()
        if l["modelo_aluno (XGBoost)"]["recall"] > l["baseline_municipal (taxa t-1)"]["recall"]
    )

    print("\n" + "=" * 74)
    print("VEREDITO")
    print("=" * 74)
    print(f"ROC-AUC: modelo {auc_modelo:.4f} vs baseline {auc_base:.4f} "
          f"(diferenca {delta:+.4f})")
    print(f"Busca ativa: o modelo vence em {vitorias} de {len(ORCAMENTOS)} orcamentos.")
    # O veredito usa a populacao HONESTA (so presentes) quando ela existe.
    if saida_presentes:
        am = saida_presentes["roc_auc"]["modelo_aluno"]
        ab = saida_presentes["roc_auc"]["baseline_municipal"]
        print(chr(10) + f"So entre quem fez a prova: modelo {am:.4f} vs baseline {ab:.4f}")
        vence_auc = am > ab

    if vence_auc and vitorias >= len(ORCAMENTOS) / 2:
        veredito = "PASSOU"
        txt = ("O modelo aluno-nivel supera o baseline municipal. A tese de descer "
               "de granularidade se sustenta, dentro das limitacoes do dado atual.")
    elif vence_auc:
        veredito = "PARCIAL"
        txt = ("O modelo separa melhor no agregado (ROC-AUC), mas nao converte isso "
               "em vantagem consistente na busca ativa -- que e como o resultado "
               "seria usado. Vantagem real duvidosa.")
    else:
        veredito = "FALHOU"
        txt = ("O modelo aluno-nivel NAO supera repetir a taxa do municipio para "
               "todos os seus alunos. Pelo criterio do proprio ADR-0001 secao 5, o "
               "esforco tecnico da Fase 3 nao se justifica com o dado atual -- a "
               "resposta honesta e continuar usando o mart da Fase 2.")
    print(f"\n>> {veredito}: {txt}")

    saida = {
        "desenho": {
            "treino": f"alunos de {ANO_TREINO}", "n_treino": int(len(treino)),
            "teste": f"alunos de {ANO_TESTE}", "n_teste": int(len(teste)),
            "taxa_risco_teste": float(teste["_y"].mean()),
            "features": feats,
            "baseline": ("taxa de nao-alfabetizacao do municipio em t-1, aplicada "
                          "uniformemente. PROXY explicito de agg_priorizacao (mart "
                          "Gold da Fase 2, fora do git por ser saida regeneravel)."),
            "cobertura_baseline": float(cobertos.mean()),
        },
        "roc_auc": aucs,
        "busca_ativa": {
            k: {n: v for n, v in l.items()} for k, l in por_orcamento.items()
        },
        "so_presentes": saida_presentes,
        "veredito": veredito,
        "leitura": txt,
    }
    out = BASE / "reports" / "teste_falsificacao.json"
    out.write_text(json.dumps(saida, ensure_ascii=False, indent=2, default=float),
                   encoding="utf-8")
    print(f"\nRelatorio salvo em {out}")


if __name__ == "__main__":
    main()
