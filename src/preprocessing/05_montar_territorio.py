"""
Monta a tabela de território/socioeconômico SEM depender de GCP nem de Spark.

POR QUE ESTE SCRIPT EXISTE
--------------------------
O modo `--full` do extrator lê a Silver de um bucket GCS, e o projeto tratou
isso por semanas como "depende da credencial do Renan". Rastreando a origem dos
dados em 2026-08-18, descobri que **o dado é público** — o que está no GCS é o
Parquet já processado, não a fonte:

| Feature | Fonte real | Custo |
|---|---|---|
| `sigla_uf` | prefixo do código IBGE do município | zero, sem API |
| `meta_alfabetizacao_*` | `dados/br_inep_..._meta_..._municipio.csv.gz` | zero, no disco |
| `populacao_total` | API pública do IBGE SIDRA | 1 requisição |
| `gasto_por_habitante_educacao` | API pública do SICONFI/Tesouro | ~9.000 requisições |

Foi a terceira dependência do projeto que se revelou falsa (as outras: a base
completa de alunos e a regra "AI Jail"). Ver Cap. 10 do docs/HANDOFF_RENAN.md.

O QUE ESTE SCRIPT FAZ E O QUE NÃO FAZ
-------------------------------------
Monta as TRÊS features baratas. **Não** busca o SICONFI: são ~9 mil chamadas a
uma API pública do governo, e a decisão registrada foi medir primeiro se
território move o resultado, antes de gastar isso. Se mover, aí sim vale.

Também NÃO é a Silver da Fase 2 — é um substituto local e reduzido, e a
diferença está declarada na coluna `_origem` do Parquet gerado e no relatório.

LEAKAGE — O QUE FOI DELIBERADAMENTE DEIXADO DE FORA
---------------------------------------------------
O arquivo de metas traz duas colunas tentadoras que **não entram**:

  * `taxa_alfabetizacao`     — desempenho do próprio ano, circular (ADR-0001 §2.2)
  * `percentual_participacao` — taxa de participação do município no ano; como
    ausência determina o rótulo por convenção, isso é o vazamento de ausência
    em nível municipal. Foi o erro que custou cinco capítulos deste projeto.

Entram apenas as metas do PDE, que são política pública definida externamente e
não derivam do desempenho do aluno predito.

USO
    python src/preprocessing/05_montar_territorio.py
    python src/preprocessing/02_extrair_snapshot.py --full --silver data/territorio_local.parquet
"""
import gzip
import io
import json
import urllib.request
from pathlib import Path

import pandas as pd

BASE = Path(__file__).resolve().parents[2]
FASE2 = BASE.parent / "tech-challenge-fase2-alfabetizacao"
METAS = FASE2 / "dados" / "br_inep_avaliacao_alfabetizacao_meta_alfabetizacao_municipio.csv.gz"
SAIDA = BASE / "data" / "territorio_local.parquet"

IBGE_URL = ("https://servicodados.ibge.gov.br/api/v3/agregados/6579/periodos/2021"
            "/variaveis/9324?localidades=N6[all]")

# Prefixo do código IBGE -> UF. Os dois primeiros dígitos do código de município
# identificam a unidade federativa; é definição do IBGE, não heurística.
UF_POR_PREFIXO = {
    11: "RO", 12: "AC", 13: "AM", 14: "RR", 15: "PA", 16: "AP", 17: "TO",
    21: "MA", 22: "PI", 23: "CE", 24: "RN", 25: "PB", 26: "PE", 27: "AL",
    28: "SE", 29: "BA", 31: "MG", 32: "ES", 33: "RJ", 35: "SP", 41: "PR",
    42: "SC", 43: "RS", 50: "MS", 51: "MT", 52: "GO", 53: "DF",
}

# Do arquivo de metas, SÓ estas. Ver bloco LEAKAGE na docstring.
COLUNAS_META = ["ano", "id_municipio", "rede", "meta_alfabetizacao_2024"]


def buscar_populacao_ibge() -> pd.DataFrame:
    """Uma requisição à API pública do SIDRA devolve todos os municípios."""
    print("Buscando populacao na API do IBGE SIDRA (1 requisicao)...")
    req = urllib.request.Request(IBGE_URL, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=120) as r:
        bruto = r.read()
        if r.info().get("Content-Encoding") == "gzip":
            bruto = gzip.GzipFile(fileobj=io.BytesIO(bruto)).read()

    series = json.loads(bruto.decode("utf-8"))[0]["resultados"][0]["series"]
    linhas = []
    for s in series:
        valor = s["serie"]["2021"]
        linhas.append({
            "id_municipio": str(s["localidade"]["id"]).zfill(7),
            # '-' e '...' aparecem quando o IBGE nao informou: viram nulo, nao zero
            "populacao_total": int(valor) if str(valor).isnumeric() else None,
        })
    df = pd.DataFrame(linhas)
    print(f"  {len(df)} municipios | {df['populacao_total'].isna().sum()} sem populacao informada")
    return df


def carregar_metas() -> pd.DataFrame:
    print(f"Lendo metas de {METAS.name}...")
    df = pd.read_csv(METAS, usecols=COLUNAS_META)
    df["id_municipio"] = df["id_municipio"].astype(str).str.zfill(7)
    n_antes = len(df)
    df = df.drop_duplicates(subset=["id_municipio", "ano", "rede"])
    if len(df) < n_antes:
        print(f"  {n_antes - len(df)} duplicatas de (municipio, ano, rede) removidas")
    cob = df["meta_alfabetizacao_2024"].notna().mean()
    print(f"  {len(df)} linhas | meta oficial presente em {cob:.1%} "
          f"(o resto e rede sem meta do PDE — ADR-004 da Fase 2)")
    return df


def main():
    metas = carregar_metas()
    pop = buscar_populacao_ibge()

    df = metas.merge(pop, on="id_municipio", how="left")

    prefixo = df["id_municipio"].str[:2].astype(int)
    df["sigla_uf"] = prefixo.map(UF_POR_PREFIXO)
    sem_uf = df["sigla_uf"].isna().sum()
    if sem_uf:
        print(f"  ATENCAO: {sem_uf} linhas com prefixo de UF desconhecido")

    # Imputação da meta. NÃO é o KNN da Fase 2 (ADR-004), que precisa de Spark —
    # é mediana por UF, declarada como substituto simplificado. A diferença
    # importa e por isso está registrada aqui e na coluna `_origem`.
    mediana_uf = df.groupby("sigla_uf")["meta_alfabetizacao_2024"].transform("median")
    df["meta_alfabetizacao_2024_imputada"] = (
        df["meta_alfabetizacao_2024"]
        .fillna(mediana_uf)
        .fillna(df["meta_alfabetizacao_2024"].median())
    )

    df["_origem"] = ("local_reduzido: IBGE SIDRA + metas do disco + UF por prefixo. "
                     "SEM gasto_por_habitante_educacao (SICONFI nao buscado). "
                     "Meta imputada por mediana de UF, NAO pelo KNN da Fase 2.")

    SAIDA.parent.mkdir(exist_ok=True)
    df.to_parquet(SAIDA, index=False)

    print("\n" + "=" * 70)
    print(f"Territorio salvo em {SAIDA}")
    print(f"  {len(df)} linhas | colunas: {[c for c in df.columns if not c.startswith('_')]}")
    print(f"  populacao presente em {df['populacao_total'].notna().mean():.1%}")
    print(f"  anos: {sorted(df['ano'].unique().tolist())}")
    print("\nAUSENTE de proposito: gasto_por_habitante_educacao (SICONFI, ~9k")
    print("requisicoes). Buscar so se este teste mostrar que territorio importa.")
    print("=" * 70)


if __name__ == "__main__":
    main()
