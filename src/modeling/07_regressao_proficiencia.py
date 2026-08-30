"""
Regressao sobre `proficiencia` (escala Saeb continua) -- ticket 0013.

POR QUE ESTE SCRIPT EXISTE (docs/wayfinder/tech_challenge_fase3/0013)
-----------------------------------------------------------------------
O enunciado NAO exige regressao (pede so classificacao binaria). Este script
e item de APRENDIZADO, decisao (B) do ticket 0013: roda com proposito
analitico, nao so pedagogico descartavel. `proficiencia` e leakage como
FEATURE (ADR-0001) mas e alvo legitimo de regressao -- nao se vaza o que se
esta tentando prever.

A HIPOTESE QUE ESTE SCRIPT TESTA
---------------------------------
Mesmo espaco de features do tournament de classificacao (`X` identico, `y`
diferente). O argumento do ticket 0010 (chave de join e so `id_municipio`,
toda feature disponivel e constante dentro do municipio) vale igual aqui: o
modelo nao consegue separar dois alunos do mesmo municipio, entao o erro da
regressao mede quanto da variancia de `proficiencia` e INTRA-municipal --
nao explicavel por nenhuma feature disponivel.

PREDICAO REGISTRADA ANTES DE RODAR (2026-08-30, docs/wayfinder/.../0013):
    R^2 esperado ~= 0,10 (faixa 0,05-0,25 para efeito geografico
    fraco/moderado; AUC do classificador ~0,6167, perto do chute, sugere
    lado baixo da faixa).
O numero medido abaixo E o dado pedagogico -- o erro de predicao ensina,
nao o acerto (AGENTS.md, regra "predicao antes da medicao").

MERGE DE `proficiencia` (nao duplica feature engineering, GATE dados.md)
---------------------------------------------------------------------------
`proficiencia` sai do snapshot em `02_extrair_snapshot.py` (COLUNAS_LEAKAGE,
linha 128) antes de salvar o parquet -- correto para o classificador, mas
significa que nao esta em `data/snapshot_modelagem.parquet`. Em vez de
duplicar a logica de extracao, este script LE o snapshot ja processado
(mesmas features, mesma limpeza) e faz merge só da coluna `proficiencia`
vinda do CSV bruto, por `id_aluno`+`ano` (chave granular, id_aluno sozinho
nao e garantido unico entre anos).

MESMO DESENHO DO TOURNAMENT (02_tournament_modelos.py)
---------------------------------------------------------
Split unico compartilhado entre candidatos, tuning via k-fold (nunca toca o
teste), grids modestos e comparaveis. Sem threshold/calibracao de
probabilidade -- sao conceitos de classificacao, nao se aplicam aqui.
"""
import json
import sys
import time
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import GridSearchCV, KFold, train_test_split
from sklearn.pipeline import Pipeline
from xgboost import XGBRegressor

BASE = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(BASE / "src" / "preprocessing"))
from pipeline_preprocessamento import (  # noqa: E402
    colunas_feature, construir_preprocessador, descrever_snapshot,
    validar_cobertura_colunas,
)

RANDOM_STATE = 42
N_FOLDS = 5
TEST_SIZE = 0.2

R2_PREVISTO = 0.10  # predicao registrada em 0013, ANTES de rodar

# Grids modestos e comparaveis -- mesmo principio do tournament de
# classificacao: comparar algoritmo sob tuning equivalente, nao espremer a
# ultima casa decimal de um deles.
CANDIDATOS = {
    "ridge": {
        "estimador": Ridge(random_state=RANDOM_STATE),
        "grid": {"modelo__alpha": [0.1, 1.0, 10.0, 100.0]},
        "papel": "baseline linear regularizado - interpretavel",
    },
    "random_forest": {
        "estimador": RandomForestRegressor(random_state=RANDOM_STATE, n_jobs=-1),
        "grid": {
            "modelo__n_estimators": [200, 400],
            "modelo__max_depth": [6, 8, 12],
            "modelo__min_samples_leaf": [10, 20],
        },
        "papel": "ensemble paralelo (bagging)",
    },
    "xgboost": {
        # n_jobs=1 pelo mesmo motivo do tournament de classificacao: ordem de
        # soma em ponto flutuante muda com contagem de threads em
        # tree_method="hist", quebrando reproducibilidade entre maquinas
        # mesmo com random_state fixo (ver 02_tournament_modelos.py).
        "estimador": XGBRegressor(
            random_state=RANDOM_STATE, tree_method="hist", n_jobs=1,
        ),
        "grid": {
            "modelo__n_estimators": [200, 400],
            "modelo__max_depth": [3, 6],
            "modelo__learning_rate": [0.05, 0.1],
        },
        "papel": "ensemble sequencial (boosting)",
    },
}


def carregar_dados_regressao() -> pd.DataFrame:
    """Snapshot processado (mesmas features do classificador) + proficiencia
    mergeada do CSV bruto por id_aluno+ano. Nao duplica feature engineering:
    so recupera a coluna-alvo que 02_extrair_snapshot.py descarta a proposito
    para o caso de uso de classificacao."""
    df = pd.read_parquet(BASE / "data" / "snapshot_modelagem.parquet")
    validar_cobertura_colunas(df)

    bruto = pd.read_csv(
        BASE / "data" / "Alunos_amostra.csv",
        usecols=["ano", "id_aluno", "proficiencia"],
    )
    n_antes = len(df)
    df = df.merge(bruto, on=["ano", "id_aluno"], how="inner", validate="one_to_one")
    perdidos = n_antes - len(df)
    if perdidos:
        print(f"AVISO: {perdidos} linhas do snapshot fora do merge -- "
              f"data/Alunos_amostra.csv ({len(bruto)} linhas) e SUBCONJUNTO "
              f"do snapshot completo ({n_antes} linhas, varias fontes/anos), "
              f"nao a fonte inteira. `n` real da regressao e menor que o do "
              f"classificador (ver contexto.n_linhas na saida).")

    # 1 caso residual: presenca="Presente" mas proficiencia NaN no CSV bruto
    # -- anomalia de dado (nao e o padrao "ausente" ja tratado na extracao,
    # ver EDA item 6). Dropar aqui, documentado, nao silencioso (GATE dados.md
    # -- nulo nunca vira default sem log).
    n_com_nan = df["proficiencia"].isna().sum()
    if n_com_nan:
        print(f"AVISO: {n_com_nan} linha(s) com proficiencia NaN mesmo apos "
              f"filtro de populacao avaliada (anomalia de dado, nao o padrao "
              f"'ausente') -- removida(s) do treino/teste da regressao.")
        df = df.dropna(subset=["proficiencia"])
    return df


def avaliar(pipeline, X_test, y_test) -> dict:
    y_pred = pipeline.predict(X_test)
    return {
        "r2": float(r2_score(y_test, y_pred)),
        "mae": float(mean_absolute_error(y_test, y_pred)),
        "rmse": float(np.sqrt(mean_squared_error(y_test, y_pred))),
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
        pipeline, config["grid"], scoring="r2", cv=cv,
        n_jobs=-1, refit=True, return_train_score=True,
    )

    inicio = time.perf_counter()
    busca.fit(X_train, y_train)  # o conjunto de teste NAO entra aqui
    tempo_tuning = time.perf_counter() - inicio

    idx = busca.best_index_
    r2_cv = busca.cv_results_["mean_test_score"][idx]
    desvio_cv = busca.cv_results_["std_test_score"][idx]
    r2_treino_cv = busca.cv_results_["mean_train_score"][idx]
    gap = r2_treino_cv - r2_cv

    print(f"Combinacoes testadas: {len(busca.cv_results_['params'])} x {N_FOLDS} "
          f"folds | tuning levou {tempo_tuning:.1f}s")
    print(f"Melhores hiperparametros: {busca.best_params_}")
    print(f"R2 em validacao cruzada: {r2_cv:.3f} (+/- {desvio_cv:.3f})")

    alerta = "  <- ATENCAO: gap alto, sinal de overfit" if gap > 0.10 else ""
    print(f"R2 no treino (mesmos folds): {r2_treino_cv:.3f} "
          f"-> gap treino-validacao = {gap:+.3f}{alerta}")

    metricas_teste = avaliar(busca.best_estimator_, X_test, y_test)
    print(f"TESTE (tocado uma vez): R2={metricas_teste['r2']:.3f} "
          f"MAE={metricas_teste['mae']:.2f} RMSE={metricas_teste['rmse']:.2f}")

    resultado = {
        "papel": config["papel"],
        "melhores_params": {k: str(v) for k, v in busca.best_params_.items()},
        "n_combinacoes": len(busca.cv_results_["params"]),
        "tempo_tuning_seg": round(tempo_tuning, 1),
        "r2_cv_media": float(r2_cv),
        "r2_cv_desvio": float(desvio_cv),
        "r2_treino_cv": float(r2_treino_cv),
        "gap_treino_validacao": float(gap),
        "teste": metricas_teste,
    }
    return resultado, busca.best_estimator_


def main():
    df = carregar_dados_regressao()
    X = df[colunas_feature(df)]
    y = df["proficiencia"]

    print(f"Snapshot: {len(df)} linhas | proficiencia media={y.mean():.1f} "
          f"desvio={y.std():.1f}")
    print(f"R2 PREVISTO (registrado antes de rodar, ticket 0013): {R2_PREVISTO}")

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE,
    )
    cv = KFold(n_splits=N_FOLDS, shuffle=True, random_state=RANDOM_STATE)
    print(f"\nTreino={len(X_train)} (tuning por {N_FOLDS}-fold) | "
          f"Teste={len(X_test)} (tocado uma vez, no fim)")

    resultados, melhores = {}, {}
    for nome, config in CANDIDATOS.items():
        resultados[nome], melhores[nome] = rodar_candidato(
            nome, config, X_train, y_train, X_test, y_test, cv
        )

    print("\n" + "=" * 72)
    print("QUADRO COMPARATIVO (metrica de decisao: R2 no teste)")
    print("=" * 72)
    cab = f"{'modelo':<22}{'R2':>9}{'MAE':>9}{'RMSE':>9}{'gap':>8}{'tuning':>9}"
    print(cab)
    print("-" * len(cab))
    for nome, r in resultados.items():
        t = r["teste"]
        print(f"{nome:<22}{t['r2']:>9.3f}{t['mae']:>9.2f}{t['rmse']:>9.2f}"
              f"{r['gap_treino_validacao']:>+8.3f}{r['tempo_tuning_seg']:>8.1f}s")

    vencedor = max(resultados, key=lambda k: resultados[k]["teste"]["r2"])
    r2_vencedor = resultados[vencedor]["teste"]["r2"]
    erro_predicao = r2_vencedor - R2_PREVISTO
    print(f"\nMaior R2 no teste: {vencedor} ({r2_vencedor:.3f})")
    print(f"Predicao registrada era {R2_PREVISTO:.3f} -> erro de predicao "
          f"{erro_predicao:+.3f}")

    saida = {
        "contexto": {
            "snapshot": descrever_snapshot(df),
            "n_linhas": int(len(df)),
            "n_treino": int(len(X_train)),
            "n_teste": int(len(X_test)),
            "n_folds": N_FOLDS,
            "alvo": "proficiencia (escala Saeb continua, leakage como feature "
                    "-- ADR-0001 -- mas alvo legitimo de regressao)",
            "features_usadas": colunas_feature(df),
            "proposito": "ticket 0013, decisao (B): erro mede variancia "
                         "intra-municipal inexplicada pelas features "
                         "disponiveis (chave de join = so id_municipio)",
        },
        "predicao_registrada_antes_de_rodar": {
            "r2_previsto": R2_PREVISTO,
            "raciocinio": "AUC do classificador (0,6167) perto do chute "
                           "(0,5); features constantes dentro do municipio "
                           "-> teto estrutural de R2. Faixa 0,05-0,25 para "
                           "efeito geografico fraco/moderado, aposta no lado "
                           "baixo.",
        },
        "resultados": resultados,
        "maior_r2_no_teste": vencedor,
        "erro_de_predicao": {
            "previsto": R2_PREVISTO,
            "medido": r2_vencedor,
            "diferenca": erro_predicao,
        },
    }

    out = BASE / "reports" / "metrics_regressao_proficiencia.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(
        json.dumps(saida, ensure_ascii=False, indent=2, default=float),
        encoding="utf-8",
    )
    print(f"\nMetricas salvas em {out}")


if __name__ == "__main__":
    main()
