"""
RANKING INTRA-UF — o produto que sobreviveu a todos os testes do projeto.

POR QUE ESTE SCRIPT EXISTE
--------------------------
Três formulações foram testadas e duas morreram:

  1. Modelo aluno-nível            -> perde da meta do PDE (Cap. 14)
  2. Modelo município NACIONAL     -> Leave-One-UF-Out em 0,4800, abaixo do
                                      acaso: o "sinal" era a régua estadual
                                      (Cap. 16.3)
  3. Modelo município INTRA-UF     -> 0,6478 contra 0,4032 do baseline
                                      intuitivo, vencendo em 18 de 23 UFs
                                      (piso de 40 municipios/UF, dobras
                                      adaptativas + IC95% bootstrap desde
                                      2026-08-20 -- ver ADR-0002 addendum)

Este script produtiza a nº 3. Ele NÃO é o experimento (esse é
`03_experimento_municipio_meta.py`, que mede e compara): aqui o objetivo é
gerar a saída que um gestor consome — um ranking de risco por município,
dentro do seu estado, com o nome do município e o motivo do score.

A REGRA QUE O PRODUTO PRECISA CARREGAR
--------------------------------------
Comparação ENTRE estados é inválida: cada UF aplica sua própria avaliação, e a
variação estadual entre anos chega a ±20pp (RS caiu 20,0; MG subiu 12,3). Um
ranking nacional compara réguas diferentes. Por isso a saída é **particionada
por UF** e o JSON carrega o aviso — para nenhum consumidor conseguir ordenar
nacionalmente sem ver a advertência.

O BASELINE QUE ESTE MODELO DERRUBA
----------------------------------
A intuição corrente — "priorize quem estava pior em 2023" — tem AUC 0,4032
(média ponderada), ou seja, é PIOR que sortear. Regressão à média somada à
meta progressiva do PDE faz municípios com taxa baixa melhorarem mais e
baterem a meta com mais frequência. É o principal valor prático do modelo:
ele corrige um erro que a priorização por intuição cometeria
sistematicamente.

SAÍDA
-----
    reports/ranking_intra_uf.json  — ranking por UF, pronto para consumo
    reports/ranking_intra_uf.csv   — mesma coisa, formato tabular
"""
import gzip
import io
import json
import sys
import urllib.request
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import StratifiedKFold
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import RobustScaler

warnings.filterwarnings("ignore")
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BASE = Path(__file__).resolve().parents[2]
FASE2 = BASE.parent / "tech-challenge-fase2-alfabetizacao"

# UF_POR_PREFIXO vive em 05_montar_territorio.py. Importado, nao duplicado:
# duas copias da mesma regra divergem em silencio (.claude/rules/dados.md).
# importlib porque o modulo comeca com digito e nao e importavel por `import`.
import importlib.util  # noqa: E402
_spec = importlib.util.spec_from_file_location(
    "montar_territorio", BASE / "src" / "preprocessing" / "05_montar_territorio.py")
_territorio = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_territorio)
UF_POR_PREFIXO = _territorio.UF_POR_PREFIXO
METAS = FASE2 / "dados" / "br_inep_avaliacao_alfabetizacao_meta_alfabetizacao_municipio.csv.gz"
TERRITORIO = BASE / "data" / "territorio_local.parquet"
IBGE_MUNICIPIOS = "https://servicodados.ibge.gov.br/api/v1/localidades/municipios"

RANDOM_STATE = 42
N_FOLDS_MAX = 5
N_BOOT = 1000
# Piso absoluto (2026-08-20, decisao registrada no ADR-0002 addendum): abaixo
# disso nem dobra reduzida nem IC bootstrap tornam o AUC informativo. AP tem
# 16 municipios no Brasil inteiro -- e o unico excluido por este piso; os
# outros 6 que ficavam de fora do piso antigo (100) agora entram com dobras
# adaptativas + IC bootstrap explicito (ver `amostra_pequena` na saida).
MIN_MUNICIPIOS_POR_UF = 40
FEATURES = ["taxa23", "meta_alfabetizacao_2024", "meta_alfabetizacao_2025",
            "populacao_total"]


def bootstrap_ic_auc(y: np.ndarray, score: np.ndarray, n_boot: int = N_BOOT,
                      seed: int = RANDOM_STATE) -> list[float]:
    """
    IC95% do AUC por bootstrap (reamostra municipios com reposicao). Existe
    pra nao reportar um AUC pontual de estado pequeno como se tivesse a mesma
    confianca de um estado grande -- o numero sozinho nao mostra isso, o
    intervalo mostra.
    """
    rng = np.random.default_rng(seed)
    n = len(y)
    aucs = []
    for _ in range(n_boot):
        idx = rng.integers(0, n, n)
        if len(np.unique(y[idx])) < 2:
            continue
        aucs.append(roc_auc_score(y[idx], score[idx]))
    lo, hi = np.percentile(aucs, [2.5, 97.5])
    return [round(float(lo), 4), round(float(hi), 4)]

AVISO_VALIDADE = (
    "Este ranking so e valido DENTRO de cada UF. As avaliacoes do Compromisso "
    "Nacional Crianca Alfabetizada sao aplicadas pelos estados, e a variacao "
    "estadual entre 2023 e 2024 chega a 20 pontos percentuais (RS -20,0; "
    "MG +12,3). Ordenar municipios de UFs diferentes na mesma escala compara "
    "reguas distintas, nao desempenho educacional."
)


def buscar_nomes_ibge() -> pd.DataFrame:
    """
    Uma requisição à API pública de localidades devolve os 5.571 municípios.

    A UF NÃO vem do payload: alguns municípios têm `microrregiao` nula (o IBGE
    migrou para regiões imediatas/intermediárias e nem todo registro traz a
    estrutura antiga). O prefixo de 2 dígitos do código IBGE identifica a UF
    por definição — é determinístico e cobre 100%, então é a fonte usada aqui.
    Da API vem só o nome.
    """
    print("Buscando nomes de municipio na API do IBGE (1 requisicao)...")
    req = urllib.request.Request(IBGE_MUNICIPIOS, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=120) as r:
        bruto = r.read()
        if r.info().get("Content-Encoding") == "gzip":
            bruto = gzip.GzipFile(fileobj=io.BytesIO(bruto)).read()
    dados = json.loads(bruto.decode("utf-8"))
    df = pd.DataFrame([{"id_municipio": str(d["id"]).zfill(7),
                         "nome_municipio": d["nome"]} for d in dados])
    print(f"  {len(df)} municipios com nome")
    return df


def montar_dataset() -> pd.DataFrame:
    df = pd.read_csv(METAS)
    df["id_municipio"] = df["id_municipio"].astype(str).str.zfill(7)
    d23 = df[df.ano == 2023][["id_municipio", "taxa_alfabetizacao",
                               "meta_alfabetizacao_2024", "meta_alfabetizacao_2025"]] \
        .rename(columns={"taxa_alfabetizacao": "taxa23"})
    d24 = df[df.ano == 2024][["id_municipio", "taxa_alfabetizacao"]] \
        .rename(columns={"taxa_alfabetizacao": "taxa24"})
    m = d23.merge(d24, on="id_municipio").dropna(
        subset=["taxa23", "taxa24", "meta_alfabetizacao_2024"])

    terr = pd.read_parquet(TERRITORIO)
    t23 = terr[terr.ano == 2023][["id_municipio", "populacao_total"]] \
        .drop_duplicates("id_municipio")
    m = m.merge(t23, on="id_municipio", how="left")
    m = m.merge(buscar_nomes_ibge(), on="id_municipio", how="left")
    m["nome_municipio"] = m["nome_municipio"].fillna("(nome nao encontrado)")

    # UF pelo prefixo do codigo IBGE — definicao, nao heuristica (ver docstring
    # de buscar_nomes_ibge e o mesmo mapa em 05_montar_territorio.py).
    m["sigla_uf"] = m["id_municipio"].str[:2].astype(int).map(UF_POR_PREFIXO)
    sem_uf = int(m["sigla_uf"].isna().sum())
    if sem_uf:
        print(f"  ATENCAO: {sem_uf} municipios com prefixo de UF desconhecido")
        m = m[m["sigla_uf"].notna()]

    m["y"] = (m.taxa24 < m.meta_alfabetizacao_2024).astype(int)
    m["gap_meta"] = (m.meta_alfabetizacao_2024 - m.taxa24).round(2)
    return m.reset_index(drop=True)


def _pipeline() -> Pipeline:
    pre = ColumnTransformer([("num", Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", RobustScaler())]), FEATURES)])
    return Pipeline([("prep", pre), ("modelo", RandomForestClassifier(
        n_estimators=200, max_depth=6, random_state=RANDOM_STATE, n_jobs=-1))])


def treinar_por_uf(m: pd.DataFrame) -> tuple[pd.DataFrame, list[dict]]:
    """
    Um modelo por UF. As predições são OUT-OF-FOLD: cada município é pontuado
    por um modelo que não o viu no treino — senão o score do produto seria
    otimista e não representaria o que o gestor receberia num município novo.
    """
    saidas, metricas = [], []
    for uf, g in m.groupby("sigla_uf"):
        if len(g) < MIN_MUNICIPIOS_POR_UF or g.y.nunique() < 2:
            continue
        g = g.copy().reset_index(drop=True)
        X, y = g[FEATURES], g.y.values

        # Validacao adaptativa: estado grande mantem 5-fold (piso antigo,
        # inalterado); estado pequeno reduz dobras pra nao deixar fold sem
        # as duas classes nem com meia duzia de casos. O preco da amostra
        # pequena aparece no IC bootstrap abaixo, nao e escondido.
        classe_minoritaria = int(np.bincount(y).min())
        n_folds = max(2, min(N_FOLDS_MAX, len(g) // 20, classe_minoritaria))

        oof = np.zeros(len(g))
        for tr, te in StratifiedKFold(n_folds, shuffle=True,
                                       random_state=RANDOM_STATE).split(X, y):
            if len(np.unique(y[tr])) < 2:
                continue
            pipe = _pipeline()
            pipe.fit(X.iloc[tr], y[tr])
            oof[te] = pipe.predict_proba(X.iloc[te])[:, 1]

        g["score_risco"] = oof.round(4)
        g["rank_uf"] = g.score_risco.rank(ascending=False, method="first").astype(int)
        auc_modelo = float(roc_auc_score(y, oof))
        # baseline que o produto precisa derrubar: "priorize quem estava pior"
        score_intuicao = -g.taxa23.values
        auc_intuicao = float(roc_auc_score(y, score_intuicao))
        ic_modelo = bootstrap_ic_auc(y, oof)
        ic_intuicao = bootstrap_ic_auc(y, score_intuicao)

        saidas.append(g)
        metricas.append({
            "uf": uf, "n_municipios": int(len(g)), "n_folds": n_folds,
            "amostra_pequena": bool(len(g) < 100),
            "taxa_falha_observada": round(float(g.y.mean()), 4),
            "auc_modelo": round(auc_modelo, 4),
            "auc_modelo_ic95": ic_modelo,
            "auc_baseline_intuicao": round(auc_intuicao, 4),
            "auc_intuicao_ic95": ic_intuicao,
            "ganho_sobre_intuicao": round(auc_modelo - auc_intuicao, 4),
            "modelo_vence": bool(auc_modelo > auc_intuicao),
        })
        print(f"  {uf}  n={len(g):>3}  folds={n_folds}  "
              f"AUC modelo {auc_modelo:.4f} [{ic_modelo[0]:.3f},{ic_modelo[1]:.3f}]  "
              f"vs intuicao {auc_intuicao:.4f}  "
              f"{'OK' if auc_modelo > auc_intuicao else 'PERDE'}")

    return pd.concat(saidas, ignore_index=True), metricas


def main():
    print("=" * 74)
    print("RANKING INTRA-UF — risco de nao atingir a meta do PDE")
    print("=" * 74)
    m = montar_dataset()
    print(f"\nDataset: {len(m):,} municipios com taxa medida em 2023 e 2024"
          .replace(",", "."))
    print(f"UFs com n >= {MIN_MUNICIPIOS_POR_UF}: treinando um modelo por estado "
          f"(dobras adaptativas, IC95% por bootstrap)\n")

    ranked, metricas = treinar_por_uf(m)
    dfm = pd.DataFrame(metricas)
    peso = dfm.n_municipios
    auc_pond = float(np.average(dfm.auc_modelo, weights=peso))
    base_pond = float(np.average(dfm.auc_baseline_intuicao, weights=peso))

    print("\n" + "=" * 74)
    print("RESUMO")
    print("=" * 74)
    print(f"  UFs no produto:                    {len(dfm)}")
    print(f"  Municipios pontuados:              {len(ranked):,}".replace(",", "."))
    print(f"  AUC do modelo (media ponderada):   {auc_pond:.4f}")
    print(f"  AUC da intuicao corrente:          {base_pond:.4f}  (abaixo do acaso)")
    print(f"  UFs em que o modelo vence:         {int(dfm.modelo_vence.sum())} de {len(dfm)}")

    cols = ["sigla_uf", "rank_uf", "id_municipio", "nome_municipio", "score_risco",
            "taxa23", "taxa24", "meta_alfabetizacao_2024", "gap_meta", "y"]
    tabela = ranked[cols].sort_values(["sigla_uf", "rank_uf"])
    tabela.to_csv(BASE / "reports" / "ranking_intra_uf.csv", index=False,
                  encoding="utf-8")

    saida = {
        "aviso_validade": AVISO_VALIDADE,
        "gerado_por": "src/modeling/04_ranking_intra_uf.py",
        "desenho": {
            "alvo": "taxa_alfabetizacao_2024 < meta_alfabetizacao_2024",
            "features": FEATURES,
            "predicoes": "out-of-fold (StratifiedKFold adaptativo, 2 a 5 dobras "
                         "conforme n da UF), um modelo por UF",
            "min_municipios_por_uf": MIN_MUNICIPIOS_POR_UF,
            "intervalo_confianca": "bootstrap 95%, 1000 reamostragens",
        },
        "resumo": {
            "ufs": int(len(dfm)),
            "municipios": int(len(ranked)),
            "auc_modelo_ponderado": round(auc_pond, 4),
            "auc_intuicao_ponderado": round(base_pond, 4),
            "ufs_modelo_vence": int(dfm.modelo_vence.sum()),
        },
        "metricas_por_uf": metricas,
        "ranking": {
            uf: g.drop(columns=["sigla_uf"]).to_dict(orient="records")
            for uf, g in tabela.groupby("sigla_uf")
        },
    }
    out = BASE / "reports" / "ranking_intra_uf.json"
    out.write_text(json.dumps(saida, ensure_ascii=False, indent=2, default=float),
                   encoding="utf-8")
    print(f"\n  {out}")
    print(f"  {BASE / 'reports' / 'ranking_intra_uf.csv'}")
    print(f"\n  AVISO NA SAIDA: {AVISO_VALIDADE[:70]}...")


if __name__ == "__main__":
    main()
