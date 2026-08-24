"""
TESTE DE RESÍDUO — existe sinal de aluno DEPOIS de controlar pelo melhor
baseline municipal, ou toda a "influência do modelo" já era o baseline
disfarçado?

POR QUE ESTE SCRIPT EXISTE
---------------------------
O teste de falsificação (02_teste_falsificacao.py) compara duas coisas que
competem: "modelo aluno-nível" vs "baseline municipal", como se fossem dois
jeitos independentes de responder a mesma pergunta. O modelo perde — mas ele
também JÁ TEM acesso à meta municipal como feature, então essa comparação
não isola se sobra alguma coisa depois de admitir que o município já é a
melhor resposta.

Aqui a pergunta muda: dado que você VAI usar o melhor baseline municipal de
qualquer forma, adicionar `caderno`, `rede` e o histórico de ESCOLA (não
município) melhora a separação, de forma estatisticamente significativa?

Se a resposta for não, fecha em definitivo a Opção A (checar resíduo) — não
é "não achamos ainda", é "testamos o residual e não há nada lá".

DESENHO
-------
Modelo A: só o melhor baseline municipal (a mesma pontuação usada em
          02_teste_falsificacao.py), sem nenhuma feature de aluno.
Modelo B: o mesmo baseline, ENTRE as features, mais tudo que já tínhamos
          (caderno, rede, histórico escola/município, flags) — XGBoost forte
          (800 árvores, depth 8, lambda 1.0).

Comparação: IC95% bootstrap pareado da diferença de ROC-AUC (mesma função
usada no teste de falsificação, para manter o método idêntico).
"""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score
from sklearn.pipeline import Pipeline
from xgboost import XGBClassifier

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BASE = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(BASE / "src" / "preprocessing"))
sys.path.insert(0, str(BASE / "src" / "evaluation"))
from pipeline_preprocessamento import (  # noqa: E402
    COLUNA_TARGET, colunas_feature, construir_preprocessador,
    validar_cobertura_colunas,
)

import importlib.util
spec = importlib.util.spec_from_file_location(
    "teste_falsificacao", BASE / "src" / "evaluation" / "02_teste_falsificacao.py")
tf = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tf)  # reaproveita baselines_municipais() e ic_diferenca_auc()

RANDOM_STATE = 42
ANO_TREINO, ANO_TESTE = 2023, 2024

PARAMS_XGB = dict(
    n_estimators=800, max_depth=8, learning_rate=0.03,
    subsample=0.8, colsample_bytree=0.8, min_child_weight=3,
    reg_lambda=1.0, random_state=RANDOM_STATE, eval_metric="logloss",
    tree_method="hist", n_jobs=-1,
)


def main():
    df = pd.read_parquet(BASE / "data" / "snapshot_modelagem.parquet")
    # Antes de criar `_y`/`_score_baseline`: valida o snapshot como veio do
    # disco. Coluna de apoio criada aqui dentro não passa por este gate.
    validar_cobertura_colunas(df)
    df["_y"] = (df[COLUNA_TARGET] == "Não").astype(int)

    treino = df[df["ano"] == ANO_TREINO].copy()
    teste = df[df["ano"] == ANO_TESTE].copy()

    print("=" * 74)
    print("TESTE DE RESIDUO — sobra sinal de aluno depois do melhor baseline?")
    print("=" * 74)
    print(f"Treino: {len(treino):,} alunos de {ANO_TREINO}".replace(",", "."))
    print(f"Teste:  {len(teste):,} alunos de {ANO_TESTE}".replace(",", "."))

    # --- baseline (mesmo do teste de falsificacao) ---
    bl = tf.baselines_municipais(df)
    melhor_nome = max(bl, key=lambda k: roc_auc_score(teste["_y"], bl[k].loc[teste.index]))
    print(f"\nBaselines testados: {list(bl)} -> mais forte: {melhor_nome}")
    df["_score_baseline"] = bl[melhor_nome]
    treino["_score_baseline"] = df.loc[treino.index, "_score_baseline"]
    teste["_score_baseline"] = df.loc[teste.index, "_score_baseline"]

    auc_baseline_sozinho = roc_auc_score(teste["_y"], teste["_score_baseline"])
    print(f"Modelo A (so baseline):                    ROC-AUC {auc_baseline_sozinho:.4f}")

    # --- Modelo B: baseline COMO feature + tudo que ja tinhamos ---
    feats = colunas_feature(df) + ["_score_baseline"]
    feats = [f for f in feats if f in df.columns]
    pipe = Pipeline([
        ("preprocessador", construir_preprocessador(treino[feats])),
        ("modelo", XGBClassifier(**PARAMS_XGB)),
    ])
    pipe.fit(treino[feats], treino["_y"])
    score_b = pipe.predict_proba(teste[feats])[:, 1]
    auc_b = roc_auc_score(teste["_y"], score_b)
    print(f"Modelo B (baseline + features de aluno):   ROC-AUC {auc_b:.4f}")
    print(f"Features do Modelo B: {feats}")

    ic = tf.ic_diferenca_auc(teste["_y"].to_numpy(), score_b, teste["_score_baseline"].to_numpy())

    print("\n" + "=" * 74)
    print("VEREDITO DO RESIDUO")
    print("=" * 74)
    print(f"Diferenca (B - A): {ic['diferenca_observada']:+.4f}  "
          f"IC95%=[{ic['ic95_inferior']:+.4f}, {ic['ic95_superior']:+.4f}]  n={ic['n_teste']:,}"
          .replace(",", "."))

    if ic["ic95_superior"] < 0:
        veredito = "SEM RESIDUO — modelo B PERDE do baseline sozinho, com significancia"
        leitura = ("Adicionar caderno/rede/historico de escola ao baseline nao so nao "
                   "ajuda: PIORA a separacao. As features de aluno introduzem ruido "
                   "que o XGBoost aprende a usar mal, sem sinal real por tras.")
    elif ic["significativo"]:
        veredito = "HA RESIDUO — modelo B supera o baseline sozinho, com significancia"
        leitura = ("Depois de admitir o baseline municipal, ainda sobra sinal real nas "
                   "features de aluno. Vale investigar quais delas carregam esse ganho.")
    else:
        veredito = "SEM RESIDUO — diferenca nao distinguivel de ruido amostral (IC cruza zero)"
        leitura = ("Adicionar as features de aluno ao baseline nao muda a separacao de "
                   "forma que se possa distinguir de acaso. Nao ha evidencia de sinal "
                   "individual alem do que o municipio ja carrega.")

    print(f"\n>> {veredito}")
    print(f"   {leitura}")

    saida = {
        "desenho": {
            "treino": f"alunos de {ANO_TREINO}", "n_treino": int(len(treino)),
            "teste": f"alunos de {ANO_TESTE}", "n_teste": int(len(teste)),
            "baseline_usado": melhor_nome,
            "features_modelo_b": feats,
        },
        "roc_auc": {"modelo_a_so_baseline": float(auc_baseline_sozinho),
                    "modelo_b_baseline_mais_features": float(auc_b)},
        "ic_diferenca_b_menos_a": ic,
        "veredito": veredito,
        "leitura": leitura,
    }
    out = BASE / "reports" / "teste_residuo.json"
    out.write_text(json.dumps(saida, ensure_ascii=False, indent=2, default=float), encoding="utf-8")
    print(f"\nRelatorio salvo em {out}")


if __name__ == "__main__":
    main()
