"""
RANKING INTRA-UF — o produto que sobreviveu a todos os testes do projeto.

POR QUE ESTE SCRIPT EXISTE
--------------------------
Três formulações foram testadas e duas morreram:

  1. Modelo aluno-nível            -> perde da meta do PDE (Cap. 14)
  2. Modelo município NACIONAL     -> Leave-One-UF-Out em 0,4800, abaixo do
                                      acaso: o "sinal" era a régua estadual
                                      (Cap. 16.3)
  3. Modelo município INTRA-UF     -> 0,6478 contra 0,6209 do baseline
                                      HONESTO (regra trivial com a direção
                                      prevista pelas outras UFs), diferença
                                      +0,027 com IC95% [+0,007, +0,048].
                                      Piso de 40 municípios/UF e dobras
                                      adaptativas: ADR-0004. Correção da
                                      régua do baseline: ADR-0005.

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

O BASELINE — E A CORREÇÃO DE RÉGUA DE 2026-08-20 (ADR-0005)
-----------------------------------------------------------
Até 2026-08-20 este script comparava o modelo contra "priorize quem estava
pior em 2023" (AUC 0,4032) e reportava vitória em 18 de 23 UFs. **Essa
comparação era inválida.** AUC é antissimétrica: AUC(-s) = 1 - AUC(s), então
0,4032 significa que a regra INVERTIDA vale 0,5968 — de graça, lendo a mesma
coluna ao contrário. Era o mesmo erro que o Cap. 4.6 do projeto já tinha
pego uma vez no modelo aluno-nível: comparar contra um baseline mais fraco
que o melhor disponível.

O baseline honesto é construído aqui em três níveis:

  1. as duas direções fixas (`auc_dir_pior` e `auc_dir_melhor`);
  2. a DIREÇÃO PREVISTA para cada UF a partir das OUTRAS UFs (leave-one-UF-out
     sobre `folga_media` = média de taxa23 - meta2024), que é o baseline que
     um gestor conseguiria montar sem conhecer o resultado do próprio estado;
  3. o IC95% bootstrap PAREADO da diferença modelo - baseline(2).

Resultado medido: modelo 0,6478 contra 0,6209 do baseline honesto,
diferença +0,027 com IC95% [+0,007, +0,048] — positivo, mas MUITO menor que
os +0,245 que a régua invertida sugeria.

POR QUE A DIREÇÃO INVERTE ENTRE ESTADOS (o achado principal)
------------------------------------------------------------
"Quem estava pior falha mais" vale em 7 UFs; o OPOSTO vale em 16. A média
nacional de 0,4032 era esses dois grupos se cancelando, não um erro
sistemático único. Dois mecanismos medidos:

  - MG (meta acompanha o município): regressão à média. O pior quartil subiu
    +23,9pp e passou; o melhor caiu -2,4pp e perdeu a meta que superava por
    só 3,6pp. => "melhor primeiro" funciona.
  - CE (meta satura em 80,0 para 82% dos municípios): os melhores já estavam
    +19,1pp acima da meta e não têm como falhar. => "pior primeiro" funciona.

O VALOR REAL DO MODELO
----------------------
Não é ranquear melhor: é NÃO PRECISAR SABER A DIREÇÃO DE ANTEMÃO. Toda a
vantagem está nas 7 UFs em que a direção não é previsível de fora
(+0,155, IC95% [+0,082, +0,226]); nas 16 previsíveis o modelo empata com a
regra trivial (-0,010, IC cruza zero). Ele funciona como seguro contra errar
a direção, não como ranqueador superior.

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
from sklearn.linear_model import LinearRegression
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
# ADR-0009: IDHM-M constante (sem serie anual, 2010 e o ano mais recente com
# cobertura municipal completa). Ver reports/proveniencia_idhm.md,
# reports/eda_idhm.md e reports/dicionario_idhm.md para o gate CRISP-DM.
IDHM = BASE / "dados_externos" / "idhm_municipio_2010.csv"

RANDOM_STATE = 42
N_FOLDS_MAX = 5
N_BOOT = 1000
# Piso absoluto (2026-08-20, decisao registrada no ADR-0002 addendum): abaixo
# disso nem dobra reduzida nem IC bootstrap tornam o AUC informativo. AP tem
# 16 municipios no Brasil inteiro -- e o unico excluido por este piso; os
# outros 6 que ficavam de fora do piso antigo (100) agora entram com dobras
# adaptativas + IC bootstrap explicito (ver `amostra_pequena` na saida).
MIN_MUNICIPIOS_POR_UF = 40
FEATURES_BASE = ["taxa23", "meta_alfabetizacao_2024", "meta_alfabetizacao_2025",
                  "populacao_total"]
# ADR-0009: features de enriquecimento municipal, testadas em separado do
# baseline acima (FEATURES_BASE) para poder reportar as duas metricas de
# sucesso definidas no ADR sem misturar contribuicao de cada fonte:
#   1. IC95% bootstrap pareado do AUC ponderado, com vs sem enriquecimento.
#   2. Contagem de UFs que mudam de veredito (inconclusivo -> modelo_vence).
# FUNDEB adiado (ADR-0009 SS7) -- so IDHM nesta rodada.
FEATURES_IDHM = ["idhm", "idhm_e", "idhm_l", "idhm_r"]
FEATURES = FEATURES_BASE  # default: comportamento antigo preservado


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


def montar_dataset(com_idhm: bool = False) -> pd.DataFrame:
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

    if com_idhm:
        # ADR-0009: IDHM constante (ano 2010, unico com serie municipal
        # completa) -- mesmo valor aplicado a 2023/2024, nao e vazamento
        # temporal porque a fonte nao tem granularidade anual pra vazar.
        idhm = pd.read_csv(IDHM, usecols=["id_municipio"] + FEATURES_IDHM)
        idhm["id_municipio"] = idhm["id_municipio"].astype(str).str.zfill(7)
        cobertura_antes = len(m)
        m = m.merge(idhm, on="id_municipio", how="left")
        cobertura_idhm = m["idhm"].notna().sum()
        print(f"  IDHM: {cobertura_idhm}/{cobertura_antes} municipios com "
              f"match ({cobertura_idhm / cobertura_antes:.1%}) — sem piso "
              f"minimo (ADR-0009), SimpleImputer cobre o resto")

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


def _pipeline(features: list[str]) -> Pipeline:
    pre = ColumnTransformer([("num", Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", RobustScaler())]), features)])
    return Pipeline([("prep", pre), ("modelo", RandomForestClassifier(
        n_estimators=200, max_depth=6, random_state=RANDOM_STATE, n_jobs=-1))])


def treinar_por_uf(m: pd.DataFrame, features: list[str] = FEATURES
                    ) -> tuple[pd.DataFrame, list[dict]]:
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
        X, y = g[features], g.y.values

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
            pipe = _pipeline(features)
            pipe.fit(X.iloc[tr], y[tr])
            oof[te] = pipe.predict_proba(X.iloc[te])[:, 1]

        g["score_risco"] = oof.round(4)
        g["rank_uf"] = g.score_risco.rank(ascending=False, method="first").astype(int)
        auc_modelo = float(roc_auc_score(y, oof))

        # AS DUAS DIREÇÕES da mesma regra trivial. Reportar só uma delas foi o
        # erro corrigido pelo ADR-0005: como AUC(-s) = 1 - AUC(s), dizer que
        # "pior primeiro" vale 0,40 é dizer que "melhor primeiro" vale 0,60.
        t = g.taxa23.values
        auc_dir_pior = float(roc_auc_score(y, -t))
        auc_dir_melhor = float(roc_auc_score(y, t))
        direcao_real = "melhor_primeiro" if auc_dir_melhor > 0.5 else "pior_primeiro"

        saidas.append(g)
        metricas.append({
            "uf": uf, "n_municipios": int(len(g)), "n_folds": n_folds,
            "amostra_pequena": bool(len(g) < 100),
            "taxa_falha_observada": round(float(g.y.mean()), 4),
            "auc_modelo": round(auc_modelo, 4),
            "auc_modelo_ic95": bootstrap_ic_auc(y, oof),
            "auc_dir_pior": round(auc_dir_pior, 4),
            "auc_dir_melhor": round(auc_dir_melhor, 4),
            "direcao_real": direcao_real,
            # folga = quanto a UF ja esta acima da propria meta. E o preditor
            # da direcao, e usa SO dado pre-2024 (taxa23 e meta2024).
            "folga_media": round(float((g.taxa23 - g.meta_alfabetizacao_2024).mean()), 3),
        })
        print(f"  {uf}  n={len(g):>3}  folds={n_folds}  AUC modelo {auc_modelo:.4f}  "
              f"| direcao que funciona: {direcao_real} ({max(auc_dir_pior, auc_dir_melhor):.4f})")

    return pd.concat(saidas, ignore_index=True), metricas


def prever_direcao_loo(metricas: list[dict]) -> None:
    """
    Para cada UF, prevê a direção da regra trivial usando SÓ as outras UFs
    (leave-one-UF-out sobre `folga_media`). É o baseline honesto: um gestor
    que nunca viu o resultado do próprio estado ainda conseguiria montá-lo,
    extrapolando dos estados vizinhos.

    Sem isso a comparação vira oráculo — escolher a direção olhando o
    resultado de 2024 entrega ao baseline uma informação que ninguém tem na
    hora de decidir.
    """
    ufs = [m["uf"] for m in metricas]
    folga = {m["uf"]: m["folga_media"] for m in metricas}
    alvo = {m["uf"]: m["auc_dir_melhor"] for m in metricas}
    for m in metricas:
        outros = [u for u in ufs if u != m["uf"]]
        X = np.array([[folga[u]] for u in outros])
        yv = np.array([alvo[u] for u in outros])
        pred = float(LinearRegression().fit(X, yv).predict([[folga[m["uf"]]]])[0])
        m["direcao_prevista"] = "melhor_primeiro" if pred > 0.5 else "pior_primeiro"
        m["direcao_previsivel"] = bool(m["direcao_prevista"] == m["direcao_real"])
        m["auc_baseline_honesto"] = round(
            m["auc_dir_melhor"] if pred > 0.5 else m["auc_dir_pior"], 4)
        m["ganho_sobre_baseline"] = round(
            m["auc_modelo"] - m["auc_baseline_honesto"], 4)


def comparar_pareado(ranked: pd.DataFrame, metricas: list[dict],
                      n_boot: int = N_BOOT, seed: int = RANDOM_STATE) -> None:
    """IC95% bootstrap PAREADO de (modelo - baseline honesto), por UF."""
    rng = np.random.default_rng(seed)
    por_uf = {m["uf"]: m for m in metricas}
    for uf, g in ranked.groupby("sigla_uf"):
        m = por_uf[uf]
        y = g.y.values
        sm = g.score_risco.values
        sb = g.taxa23.values if m["direcao_prevista"] == "melhor_primeiro" else -g.taxa23.values
        difs = []
        for _ in range(n_boot):
            i = rng.integers(0, len(y), len(y))
            if len(np.unique(y[i])) < 2:
                continue
            difs.append(roc_auc_score(y[i], sm[i]) - roc_auc_score(y[i], sb[i]))
        lo, hi = np.percentile(difs, [2.5, 97.5])
        m["ganho_ic95"] = [round(float(lo), 4), round(float(hi), 4)]
        m["veredito"] = ("modelo_vence" if lo > 0 else
                         "modelo_perde" if hi < 0 else "inconclusivo")


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

    print("\nPrevendo a direcao de cada UF a partir das OUTRAS (leave-one-UF-out)...")
    prever_direcao_loo(metricas)
    print("Bootstrap pareado modelo vs baseline honesto...")
    comparar_pareado(ranked, metricas)

    dfm = pd.DataFrame(metricas)
    peso = dfm.n_municipios
    auc_pond = float(np.average(dfm.auc_modelo, weights=peso))
    honesto_pond = float(np.average(dfm.auc_baseline_honesto, weights=peso))
    pior_pond = float(np.average(dfm.auc_dir_pior, weights=peso))
    melhor_pond = float(np.average(dfm.auc_dir_melhor, weights=peso))
    prev = dfm[dfm.direcao_previsivel]
    naoprev = dfm[~dfm.direcao_previsivel]

    print("\n" + "=" * 74)
    print("RESUMO")
    print("=" * 74)
    print(f"  UFs no produto:                    {len(dfm)}")
    print(f"  Municipios pontuados:              {len(ranked):,}".replace(",", "."))
    print()
    print("  AS TRES BARRAS (media ponderada):")
    print(f"    regra trivial 'pior primeiro'      {pior_pond:.4f}   <- a regua INVALIDA (ADR-0005)")
    print(f"    regra trivial 'melhor primeiro'    {melhor_pond:.4f}   (a mesma regra, invertida)")
    print(f"    baseline HONESTO (direcao por LOO) {honesto_pond:.4f}   <- a comparacao valida")
    print(f"    MODELO                             {auc_pond:.4f}   ({auc_pond - honesto_pond:+.4f})")
    print()
    print("  DE ONDE VEM A VANTAGEM:")
    print(f"    direcao previsivel de fora   {len(prev):>2} UFs, "
          f"ganho medio {np.average(prev.ganho_sobre_baseline, weights=prev.n_municipios):+.4f}")
    print(f"    direcao NAO previsivel       {len(naoprev):>2} UFs, "
          f"ganho medio {np.average(naoprev.ganho_sobre_baseline, weights=naoprev.n_municipios):+.4f}")
    print()
    print("  VEREDITO POR UF (IC95% pareado):")
    for v in ["modelo_vence", "inconclusivo", "modelo_perde"]:
        ufs_v = dfm[dfm.veredito == v].uf.tolist()
        print(f"    {v:<15} {len(ufs_v):>2}  {' '.join(ufs_v)}")

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
            "baseline_honesto": (
                "regra trivial sobre taxa23 com a DIRECAO prevista para cada UF "
                "a partir das outras (leave-one-UF-out sobre folga_media). "
                "Substitui o baseline 'pior primeiro' usado ate 2026-08-20, que "
                "era a mesma regra na direcao errada — ver ADR-0005."
            ),
        },
        "resumo": {
            "ufs": int(len(dfm)),
            "municipios": int(len(ranked)),
            "auc_modelo_ponderado": round(auc_pond, 4),
            "auc_baseline_honesto_ponderado": round(honesto_pond, 4),
            "auc_dir_pior_ponderado": round(pior_pond, 4),
            "auc_dir_melhor_ponderado": round(melhor_pond, 4),
            "ganho_sobre_baseline": round(auc_pond - honesto_pond, 4),
            "ufs_modelo_vence": int((dfm.veredito == "modelo_vence").sum()),
            "ufs_inconclusivo": int((dfm.veredito == "inconclusivo").sum()),
            "ufs_modelo_perde": int((dfm.veredito == "modelo_perde").sum()),
            "ufs_direcao_previsivel": int(dfm.direcao_previsivel.sum()),
            "ufs_direcao_melhor_primeiro": int((dfm.direcao_real == "melhor_primeiro").sum()),
            "ufs_direcao_pior_primeiro": int((dfm.direcao_real == "pior_primeiro").sum()),
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
