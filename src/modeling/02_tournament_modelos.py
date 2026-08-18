"""
Tournament de modelos: Regressão Logística vs Random Forest vs XGBoost.

POR QUE ESTE SCRIPT EXISTE (ver Cap. 7 do docs/HANDOFF_RENAN.md)
----------------------------------------------------------------
A auditoria do enunciado achou 3 lacunas que este script fecha de uma vez:

  1. "Escolha do algoritmo" (seção exigida no README) — não havia comparação,
     só um baseline RandomForest.
  2. "Estratégias de otimização ... reduzir overfitting" (enunciado, p.5) —
     não existia nenhum tuning; o baseline rodava com hiperparâmetro fixo.
  3. "Validação garantindo replicabilidade e generalização" + os TRÊS conjuntos
     citados no enunciado (treino/validação/teste) — havia só split único.

A PARTE QUE MAIS IMPORTA: por que k-fold, e não mais um split
-------------------------------------------------------------
Com tuning entrando em cena, usar o conjunto de TESTE para escolher
hiperparâmetro vaza o teste: escolheríamos o modelo que melhor se ajusta
justamente aos dados que deveriam medir generalização. O número final sairia
otimista e nada quebraria.

Por isso o desenho é:

    [ 100% do snapshot ]
        |
        +-- 80% TREINO --> StratifiedKFold(5) --> GridSearchCV escolhe
        |                  (o "conjunto de validação" do enunciado aparece
        |                   aqui, 5x, sempre dentro do treino)
        |
        +-- 20% TESTE  --> tocado UMA VEZ, no fim, com o modelo já escolhido

Cada candidato recebe exatamente o mesmo split e o mesmo k-fold (mesmo
random_state), senão a comparação seria injusta.

MÉTRICA DE DECISÃO
------------------
Recall da classe "Não" (aluno em risco) — ADR-0001 §5. Falso negativo (aluno em
risco não identificado) é o erro caro no caso de uso de busca ativa. Precision
entra como contrapeso: Recall alto com Precision no chão significa marcar todo
mundo como risco, o que não prioriza nada.

ATENÇÃO AO LER OS NÚMEROS: roda sobre o snapshot --local-only (5.000 linhas,
sem território/socioeconômico/meta). NÃO são números de README — servem para
escolher o algoritmo e como base de comparação para quando o --full rodar.
"""
import argparse
import json
import sys
import time
from pathlib import Path

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score, confusion_matrix, f1_score, precision_score,
    recall_score, roc_auc_score,
)
from sklearn.model_selection import GridSearchCV, StratifiedKFold, train_test_split
from sklearn.pipeline import Pipeline
from xgboost import XGBClassifier

BASE = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(BASE / "src" / "preprocessing"))
from pipeline_preprocessamento import (  # noqa: E402
    COLUNA_TARGET, colunas_feature, construir_preprocessador, descrever_features,
)

RANDOM_STATE = 42
N_FOLDS = 5
TEST_SIZE = 0.2

# Grids deliberadamente modestos e de tamanho comparável: o objetivo é comparar
# algoritmos sob tuning equivalente, não espremer a última casa decimal de um
# deles. Grid grande num modelo e pequeno noutro enviesaria o torneio.
CANDIDATOS = {
    "regressao_logistica": {
        "estimador": LogisticRegression(
            class_weight="balanced", random_state=RANDOM_STATE, max_iter=2000,
        ),
        "grid": {
            "modelo__C": [0.01, 0.1, 1.0, 10.0],
        },
        "papel": "baseline interpretavel - se ganhar, explicar custa menos",
    },
    "random_forest": {
        "estimador": RandomForestClassifier(
            class_weight="balanced", random_state=RANDOM_STATE, n_jobs=-1,
        ),
        "grid": {
            "modelo__n_estimators": [200, 400],
            "modelo__max_depth": [6, 8, 12],
            "modelo__min_samples_leaf": [10, 20],
        },
        "papel": "ensemble paralelo (bagging) - o baseline atual do projeto",
    },
    "xgboost": {
        "estimador": XGBClassifier(
            random_state=RANDOM_STATE, eval_metric="logloss",
            tree_method="hist", n_jobs=-1,
        ),
        "grid": {
            "modelo__n_estimators": [200, 400],
            "modelo__max_depth": [3, 6],
            "modelo__learning_rate": [0.05, 0.1],
        },
        "papel": "ensemble sequencial (boosting) - costuma ganhar em tabular",
    },
}


def carregar_snapshot() -> pd.DataFrame:
    df = pd.read_parquet(BASE / "data" / "snapshot_modelagem.parquet")
    # 1 = "Não" (classe de risco, a que o Recall precisa capturar - ADR-0001 §5).
    # Inverter isso por engano faria o Recall medir a classe errada sem nenhum
    # erro visível: a métrica roda normal, só mede a coisa errada.
    df[COLUNA_TARGET] = (df[COLUNA_TARGET] == "Não").astype(int)
    return df


def avaliar(pipeline, X_test, y_test) -> dict:
    y_pred = pipeline.predict(X_test)
    y_proba = pipeline.predict_proba(X_test)[:, 1]
    return {
        "recall": recall_score(y_test, y_pred),
        "precision": precision_score(y_test, y_pred, zero_division=0),
        "f1": f1_score(y_test, y_pred),
        "roc_auc": roc_auc_score(y_test, y_proba),
        "accuracy": accuracy_score(y_test, y_pred),
        "matriz_confusao": confusion_matrix(y_test, y_pred).tolist(),
    }


def rodar_candidato(nome, config, X_train, y_train, X_test, y_test, cv):
    print("\n" + "=" * 72)
    print(f"{nome.upper()}  ({config['papel']})")
    print("=" * 72)

    pipeline = Pipeline([
        ("preprocessador", construir_preprocessador(X_train)),
        ("modelo", config["estimador"]),
    ])

    busca = GridSearchCV(
        pipeline, config["grid"], scoring="recall", cv=cv,
        n_jobs=-1, refit=True, return_train_score=True,
    )

    inicio = time.perf_counter()
    busca.fit(X_train, y_train)  # o conjunto de teste NAO entra aqui
    tempo_tuning = time.perf_counter() - inicio

    idx = busca.best_index_
    recall_cv = busca.cv_results_["mean_test_score"][idx]
    desvio_cv = busca.cv_results_["std_test_score"][idx]
    recall_treino_cv = busca.cv_results_["mean_train_score"][idx]
    gap = recall_treino_cv - recall_cv

    print(f"Combinacoes testadas: {len(busca.cv_results_['params'])} x {N_FOLDS} "
          f"folds | tuning levou {tempo_tuning:.1f}s")
    print(f"Melhores hiperparametros: {busca.best_params_}")
    print(f"Recall em validacao cruzada: {recall_cv:.3f} (+/- {desvio_cv:.3f})")

    # Diagnostico de overfitting: distancia entre treino e validacao DENTRO do
    # k-fold. O enunciado pede "reduzir overfitting" - este numero e o que
    # mostra se a regularizacao escolhida pelo tuning de fato funcionou.
    alerta = "  <- ATENCAO: gap alto, sinal de overfit" if gap > 0.10 else ""
    print(f"Recall no treino (mesmos folds): {recall_treino_cv:.3f} "
          f"-> gap treino-validacao = {gap:+.3f}{alerta}")

    metricas_teste = avaliar(busca.best_estimator_, X_test, y_test)
    print(f"TESTE (tocado uma vez): Recall={metricas_teste['recall']:.3f} "
          f"Precision={metricas_teste['precision']:.3f} "
          f"F1={metricas_teste['f1']:.3f} ROC-AUC={metricas_teste['roc_auc']:.3f}")

    resultado = {
        "papel": config["papel"],
        "melhores_params": {k: str(v) for k, v in busca.best_params_.items()},
        "n_combinacoes": len(busca.cv_results_["params"]),
        "tempo_tuning_seg": round(tempo_tuning, 1),
        "recall_cv_media": float(recall_cv),
        "recall_cv_desvio": float(desvio_cv),
        "recall_treino_cv": float(recall_treino_cv),
        "gap_treino_validacao": float(gap),
        "teste": metricas_teste,
    }
    return resultado, busca.best_estimator_


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--temporal", action="store_true",
                        help="Roda tambem a checagem temporal 2023->2024")
    args = parser.parse_args()

    df = carregar_snapshot()
    X, y = df[colunas_feature(df)], df[COLUNA_TARGET]

    print(f"Snapshot: {len(df)} linhas | classe de risco ('Nao') = {y.mean():.1%}")
    print(descrever_features(df))

    # Split unico, compartilhado por TODOS os candidatos (comparacao justa).
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=TEST_SIZE, stratify=y, random_state=RANDOM_STATE,
    )
    cv = StratifiedKFold(n_splits=N_FOLDS, shuffle=True, random_state=RANDOM_STATE)
    print(f"\nTreino={len(X_train)} (tuning por {N_FOLDS}-fold estratificado) | "
          f"Teste={len(X_test)} (tocado uma vez, no fim)")

    resultados, melhores = {}, {}
    for nome, config in CANDIDATOS.items():
        resultados[nome], melhores[nome] = rodar_candidato(
            nome, config, X_train, y_train, X_test, y_test, cv
        )

    print("\n" + "=" * 72)
    print("QUADRO COMPARATIVO (metrica de decisao: Recall no teste)")
    print("=" * 72)
    cab = (f"{'modelo':<22}{'Recall':>9}{'Precis.':>9}{'F1':>8}"
           f"{'ROC-AUC':>9}{'gap':>8}{'tuning':>9}")
    print(cab)
    print("-" * len(cab))
    for nome, r in resultados.items():
        t = r["teste"]
        print(f"{nome:<22}{t['recall']:>9.3f}{t['precision']:>9.3f}"
              f"{t['f1']:>8.3f}{t['roc_auc']:>9.3f}"
              f"{r['gap_treino_validacao']:>+8.3f}"
              f"{r['tempo_tuning_seg']:>8.1f}s")

    vencedor = max(resultados, key=lambda k: resultados[k]["teste"]["recall"])
    print(f"\nMaior Recall no teste: {vencedor} "
          f"({resultados[vencedor]['teste']['recall']:.3f})")
    print("NAO e decisao final - ver ressalvas no relatorio e no HANDOFF_RENAN.md")

    saida = {
        "contexto": {
            "snapshot": "local-only (sem territorio/socioeconomico/meta)",
            "n_linhas": int(len(df)),
            "n_treino": int(len(X_train)),
            "n_teste": int(len(X_test)),
            "n_folds": N_FOLDS,
            "metrica_decisao": "recall da classe 'Nao' (ADR-0001 secao 5)",
            "features_usadas": colunas_feature(df),
        },
        "resultados": resultados,
        "maior_recall_no_teste": vencedor,
    }

    if args.temporal:
        print("\n" + "=" * 72)
        print("CHECAGEM TEMPORAL (treina em 2023, testa em 2024)")
        print("=" * 72)
        print("Viés conhecido (ADR-0001 §2.4): o treino de 2023 fica com "
              "histórico t-1 majoritariamente imputado.")
        m_treino, m_teste = df["ano"] == 2023, df["ano"] == 2024
        temporais = {}
        for nome, estimador in melhores.items():
            # Reusa os hiperparametros vencedores do k-fold, refitando na
            # janela temporal. Sem re-tuning: o objetivo aqui e checar
            # estabilidade no tempo, nao escolher modelo de novo.
            estimador.fit(X[m_treino], y[m_treino])
            temporais[nome] = avaliar(estimador, X[m_teste], y[m_teste])
            print(f"{nome:<22} Recall={temporais[nome]['recall']:.3f} "
                  f"Precision={temporais[nome]['precision']:.3f} "
                  f"ROC-AUC={temporais[nome]['roc_auc']:.3f}")
        saida["checagem_temporal"] = temporais

    out = BASE / "reports" / "metrics_tournament.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(
        json.dumps(saida, ensure_ascii=False, indent=2, default=float),
        encoding="utf-8",
    )
    print(f"\nMetricas salvas em {out}")


if __name__ == "__main__":
    main()
