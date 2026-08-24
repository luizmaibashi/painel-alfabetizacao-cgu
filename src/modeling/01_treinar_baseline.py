"""
Treina e valida o modelo baseline de predição de alfabetização por aluno.

IMPORTANTE: roda sobre o snapshot --local-only (sem território/socioeconômico
— essas features dependem de acesso ao GCS, ver ADR-0001). Isto é um baseline
parcial para validar a pipeline (leakage, encoding, split, métricas), não o
modelo final — métricas aqui NÃO são o número de referência para o README.

Validação dupla (ADR-0001, seção 2.4):
  1. Split aleatório estratificado por classe (principal)
  2. Split temporal 2023(treino)->2024(teste) (checagem secundária, viés
     conhecido: treino fica com histórico t-1 majoritariamente imputado)
"""
import sys
from pathlib import Path

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.inspection import permutation_importance
from sklearn.metrics import (
    accuracy_score, classification_report, confusion_matrix,
    f1_score, precision_score, recall_score, roc_auc_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

BASE = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(BASE / "src" / "preprocessing"))
from pipeline_preprocessamento import (  # noqa: E402
    COLUNA_TARGET, colunas_feature, construir_preprocessador, descrever_features,
    validar_cobertura_colunas,
)

RANDOM_STATE = 42


def carregar_snapshot() -> pd.DataFrame:
    df = pd.read_parquet(BASE / "data" / "snapshot_modelagem.parquet")
    # Coluna nova no snapshot para aqui, em vez de sair do modelo em silêncio.
    validar_cobertura_colunas(df)
    # 1 = "Não" (classe de risco, a que o Recall precisa capturar -
    # ADR-0001 seção 5). Inverter isso por engano faria o Recall reportado
    # medir a classe errada sem nenhum erro visível (métrica roda normal,
    # só mede a coisa errada).
    df[COLUNA_TARGET] = (df[COLUNA_TARGET] == "Não").astype(int)
    return df


def montar_X_y(df: pd.DataFrame):
    return df[colunas_feature(df)], df[COLUNA_TARGET]


def treinar_e_avaliar(X_train, y_train, X_test, y_test, nome_split: str) -> dict:
    pipeline = Pipeline([
        ("preprocessador", construir_preprocessador(X_train)),
        ("modelo", RandomForestClassifier(
            n_estimators=200, max_depth=8, min_samples_leaf=20,
            class_weight="balanced", random_state=RANDOM_STATE,
        )),
    ])
    # fit só no treino (aula Otimização, slide 37) -> Pipeline garante isso:
    # o ColumnTransformer só vê X_train aqui, nunca X_test.
    pipeline.fit(X_train, y_train)

    y_pred = pipeline.predict(X_test)
    y_proba = pipeline.predict_proba(X_test)[:, 1]

    metrics = {
        "split": nome_split,
        "n_treino": len(X_train),
        "n_teste": len(X_test),
        "accuracy": accuracy_score(y_test, y_pred),
        "precision": precision_score(y_test, y_pred),
        "recall": recall_score(y_test, y_pred),  # métrica principal (ADR-0001)
        "f1": f1_score(y_test, y_pred),
        "roc_auc": roc_auc_score(y_test, y_proba),
        "matriz_confusao": confusion_matrix(y_test, y_pred).tolist(),
        "relatorio_classificacao": classification_report(y_test, y_pred, output_dict=True),
    }

    # Permutation Importance (aula Otimização, slide 58) -> checagem cruzada
    # de qual feature realmente move a métrica, não só a impureza da árvore.
    perm = permutation_importance(
        pipeline, X_test, y_test, n_repeats=10, random_state=RANDOM_STATE,
        scoring="recall",
    )
    metrics["permutation_importance"] = dict(
        sorted(zip(X_test.columns, perm.importances_mean.round(4)),
               key=lambda kv: -kv[1])
    )
    return metrics, pipeline


def main():
    df = carregar_snapshot()
    X, y = montar_X_y(df)

    print(f"Snapshot: {len(df)} linhas, target balanceado em "
          f"{y.mean():.1%} (classe 'Sim').")
    print(descrever_features(df))

    resultados = {}

    # --- Split 1: aleatório estratificado por classe (principal) ---
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=RANDOM_STATE,
    )
    metrics_random, _ = treinar_e_avaliar(
        X_train, y_train, X_test, y_test, "aleatorio_estratificado"
    )
    resultados["split_aleatorio"] = metrics_random

    # --- Split 2: temporal 2023->2024 (secundário, viés conhecido) ---
    treino_mask = df["ano"] == 2023
    teste_mask = df["ano"] == 2024
    if treino_mask.sum() > 0 and teste_mask.sum() > 0:
        metrics_temporal, _ = treinar_e_avaliar(
            X[treino_mask], y[treino_mask], X[teste_mask], y[teste_mask],
            "temporal_2023_treino_2024_teste",
        )
        resultados["split_temporal"] = metrics_temporal

    for nome, m in resultados.items():
        print(f"\n=== {nome} ({m['split']}) ===")
        print(f"n_treino={m['n_treino']} n_teste={m['n_teste']}")
        print(f"Recall (classe 'Não', a de risco)={m['recall']:.3f} "
              f"Precision={m['precision']:.3f} F1={m['f1']:.3f} "
              f"ROC-AUC={m['roc_auc']:.3f}")
        print("Permutation importance:", m["permutation_importance"])

    import json
    out_dir = BASE / "reports"
    out_dir.mkdir(exist_ok=True)
    with open(out_dir / "metrics_baseline.json", "w", encoding="utf-8") as f:
        json.dump(resultados, f, ensure_ascii=False, indent=2, default=float)
    print(f"\nMétricas salvas em {out_dir / 'metrics_baseline.json'}")


if __name__ == "__main__":
    main()
