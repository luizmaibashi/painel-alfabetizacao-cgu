"""Backtest prospectivo do ranking municipal intra-UF.

Congela a decisão tomada antes de ler o alvo de 2025: treina somente na
transição 2023->2024 e pontua 2025 com taxa de 2024 e metas já publicadas.
Não atualiza o produto nem o painel; produz evidência para decidir isso.
"""
import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.metrics import roc_auc_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import RobustScaler

BASE = Path(__file__).resolve().parents[2]
ICA_2025 = BASE / "dados_externos" / "resultados_e_metas_municipios_2025_3.xlsx"
TERRITORIO = BASE / "data" / "territorio_local.parquet"
SAIDA = BASE / "reports" / "backtest_prospectivo_2025.json"

RANDOM_STATE = 42
N_BOOT = 1000
MIN_MUNICIPIOS = 40
FEATURES = ["taxa_base", "meta_alvo", "meta_seguinte", "populacao_total"]

COLUNAS_ICA = {
    "CO_MUNICIPIO": "id_municipio",
    "SG_UF": "sigla_uf",
    "NO_MUNICIPIO": "nome_municipio",
    "PC_ALUNO_ALFABETIZADO_2023": "taxa23",
    "PC_ALUNO_ALFABETIZADO_2024": "taxa24",
    "PC_ALUNO_ALFABETIZADO_2025": "taxa25",
    "META_FINAL_2024": "meta24",
    "META_FINAL_2025": "meta25",
    "META_FINAL_2026": "meta26",
    "PC_AVALIADOS_LP": "participacao_2025",
}


def hash_arquivo(caminho: Path) -> str:
    return hashlib.sha256(caminho.read_bytes()).hexdigest()


def carregar_ica(caminho: Path = ICA_2025) -> pd.DataFrame:
    """Lê a planilha oficial e rejeita linhas que não são municípios."""
    bruto = pd.read_excel(caminho, sheet_name=0, header=1,
                          dtype={"CO_MUNICIPIO": "string"})
    faltantes = set(COLUNAS_ICA) - set(bruto.columns)
    if faltantes:
        raise ValueError(f"Planilha ICA sem colunas esperadas: {sorted(faltantes)}")
    df = bruto.dropna(subset=["CO_MUNICIPIO"]).rename(columns=COLUNAS_ICA).copy()
    df["id_municipio"] = df["id_municipio"].astype(str).str.zfill(7)
    if df.id_municipio.duplicated().any():
        raise ValueError("A fonte ICA contém código municipal duplicado")
    for coluna in [c for c in COLUNAS_ICA.values() if c.startswith(("taxa", "meta", "participacao"))]:
        df[coluna] = pd.to_numeric(df[coluna], errors="coerce")
    return df[list(COLUNAS_ICA.values())]


def montar_janelas(ica: pd.DataFrame, territorio: Path = TERRITORIO) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Monta treino 2023->2024 e teste prospectivo 2024->2025."""
    pop = pd.read_parquet(territorio)
    pop = pop[pop.ano == 2023][["id_municipio", "populacao_total"]].drop_duplicates("id_municipio")
    dados = ica.merge(pop, on="id_municipio", how="left")

    treino = dados.rename(columns={
        "taxa23": "taxa_base", "meta24": "meta_alvo", "meta25": "meta_seguinte"
    }).copy()
    treino["y"] = (treino.taxa24 < treino.meta_alvo).astype("int8")
    treino = treino.dropna(subset=["taxa_base", "meta_alvo", "meta_seguinte"])

    teste = dados.rename(columns={
        "taxa24": "taxa_base", "meta25": "meta_alvo", "meta26": "meta_seguinte"
    }).copy()
    teste["y"] = (teste.taxa25 < teste.meta_alvo).astype("int8")
    teste = teste.dropna(subset=["taxa_base", "meta_alvo", "meta_seguinte", "taxa25"])
    return treino.reset_index(drop=True), teste.reset_index(drop=True)


def pipeline() -> Pipeline:
    pre = ColumnTransformer([("num", Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", RobustScaler()),
    ]), FEATURES)])
    return Pipeline([("prep", pre), ("modelo", RandomForestClassifier(
        n_estimators=200, max_depth=6, random_state=RANDOM_STATE, n_jobs=-1
    ))])


def direcoes_persistentes(treino: pd.DataFrame) -> dict[str, str]:
    """Usa em 2025 a direção observada no próprio estado em 2024.

    É mais forte que prever a direção por outras UFs e ainda é legítimo: o
    resultado 2024 já estava disponível antes do alvo 2025. Se o modelo não o
    superar, não há razão para manter uma alternativa mais complexa.
    """
    direcoes = {}
    for uf, grupo in treino.groupby("sigla_uf"):
        if len(grupo) < MIN_MUNICIPIOS or grupo.y.nunique() < 2:
            continue
        auc_melhor = roc_auc_score(grupo.y, grupo.taxa_base)
        direcoes[uf] = "melhor_primeiro" if auc_melhor > 0.5 else "pior_primeiro"
    return direcoes


def _auc_por_pesos(y: np.ndarray, scores: np.ndarray, pesos: np.ndarray) -> np.ndarray:
    """AUC por reamostragem representada pelas contagens de cada linha.

    As contagens multinomiais são equivalentes a sortear ``n`` linhas com
    reposição. A forma vetorizada conserva o pareamento modelo/baseline e
    permite calcular 1.000 reamostragens para todas as UFs rapidamente.
    """
    ordem = np.argsort(scores, kind="stable")
    y_ord = y[ordem]
    score_ord = scores[ordem]
    pesos_ord = pesos[:, ordem]
    inicio = np.flatnonzero(np.r_[True, score_ord[1:] != score_ord[:-1]])
    fim = np.r_[inicio[1:], len(score_ord)]

    positivos = np.zeros(len(pesos), dtype=float)
    negativos = np.zeros(len(pesos), dtype=float)
    concordancias = np.zeros(len(pesos), dtype=float)
    for primeiro, ultimo in zip(inicio, fim):
        grupo = pesos_ord[:, primeiro:ultimo]
        pos = grupo[:, y_ord[primeiro:ultimo] == 1].sum(axis=1)
        neg = grupo[:, y_ord[primeiro:ultimo] == 0].sum(axis=1)
        concordancias += pos * (negativos + 0.5 * neg)
        positivos += pos
        negativos += neg

    denominador = positivos * negativos
    aucs = np.full(len(pesos), np.nan)
    validos = denominador > 0
    aucs[validos] = concordancias[validos] / denominador[validos]
    return aucs


def bootstrap_ganho(y: np.ndarray, modelo: np.ndarray, baseline: np.ndarray,
                    n_boot: int = N_BOOT, seed: int = RANDOM_STATE) -> list[float]:
    """IC bootstrap pareado para AUC(modelo) - AUC(baseline)."""
    y = np.asarray(y)
    rng = np.random.default_rng(seed)
    tamanho = len(y)
    pesos = rng.multinomial(tamanho, np.full(tamanho, 1 / tamanho), size=n_boot)
    ganhos = _auc_por_pesos(y, np.asarray(modelo), pesos) - _auc_por_pesos(y, np.asarray(baseline), pesos)
    ganhos = ganhos[~np.isnan(ganhos)]
    lo, hi = np.percentile(ganhos, [2.5, 97.5])
    return [round(float(lo), 4), round(float(hi), 4)]


def executar_backtest(treino: pd.DataFrame, teste: pd.DataFrame,
                      n_boot: int = N_BOOT) -> tuple[pd.DataFrame, list[dict]]:
    direcoes = direcoes_persistentes(treino)
    rankings, metricas = [], []
    for uf, tr in treino.groupby("sigla_uf"):
        te = teste[teste.sigla_uf == uf].copy()
        if len(tr) < MIN_MUNICIPIOS or len(te) < MIN_MUNICIPIOS:
            continue
        if tr.y.nunique() < 2 or te.y.nunique() < 2:
            continue
        modelo = pipeline().fit(tr[FEATURES], tr.y)
        te["score_modelo"] = modelo.predict_proba(te[FEATURES])[:, 1]
        direcao = direcoes[uf]
        te["score_baseline"] = te.taxa_base if direcao == "melhor_primeiro" else -te.taxa_base
        auc_modelo = roc_auc_score(te.y, te.score_modelo)
        auc_baseline = roc_auc_score(te.y, te.score_baseline)
        ic = bootstrap_ganho(te.y.to_numpy(), te.score_modelo.to_numpy(),
                              te.score_baseline.to_numpy(), n_boot=n_boot)
        veredito = "modelo_vence" if ic[0] > 0 else "modelo_perde" if ic[1] < 0 else "inconclusivo"
        te["rank_modelo"] = te.score_modelo.rank(ascending=False, method="first").astype(int)
        rankings.append(te)
        metricas.append({
            "uf": uf, "n_municipios": int(len(te)), "direcao_prevista": direcao,
            "taxa_falha_2025": round(float(te.y.mean()), 4),
            "auc_modelo": round(float(auc_modelo), 4),
            "auc_baseline": round(float(auc_baseline), 4),
            "ganho_sobre_baseline": round(float(auc_modelo - auc_baseline), 4),
            "ganho_ic95": ic, "veredito": veredito,
        })
    return pd.concat(rankings, ignore_index=True), metricas


def main() -> None:
    ica = carregar_ica()
    treino, teste = montar_janelas(ica)
    n_boot = N_BOOT
    ranking, metricas = executar_backtest(treino, teste, n_boot=n_boot)
    dfm = pd.DataFrame(metricas)
    pesos = dfm.n_municipios
    resultado = {
        "fonte": {
            "arquivo": str(ICA_2025.relative_to(BASE)), "sha256": hash_arquivo(ICA_2025),
            "url": "https://download.inep.gov.br/avaliacao_da_alfabetizacao/resultados/resultados_e_metas_municipios_2025_3.xlsx",
        },
        "desenho": "Treina 2023->2024 e testa prospectivamente 2024->2025; sem tuning ou alvo de 2025 no treino.",
        "resumo": {
            "ufs": int(len(dfm)), "municipios": int(len(ranking)),
            "auc_modelo_ponderado": round(float(np.average(dfm.auc_modelo, weights=pesos)), 4),
            "auc_baseline_ponderado": round(float(np.average(dfm.auc_baseline, weights=pesos)), 4),
            "ganho_ponderado": round(float(np.average(dfm.ganho_sobre_baseline, weights=pesos)), 4),
            "ufs_modelo_vence": int((dfm.veredito == "modelo_vence").sum()),
            "ufs_inconclusivo": int((dfm.veredito == "inconclusivo").sum()),
            "ufs_modelo_perde": int((dfm.veredito == "modelo_perde").sum()),
            "reamostragens_bootstrap": n_boot,
        },
        "metricas_por_uf": metricas,
    }
    SAIDA.write_text(json.dumps(resultado, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(resultado["resumo"], ensure_ascii=False, indent=2))
    print(f"Relatório: {SAIDA.relative_to(BASE)}")


if __name__ == "__main__":
    main()
