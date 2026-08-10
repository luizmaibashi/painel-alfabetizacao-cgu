"""
Extração do snapshot de modelagem: Alunos x território/socioeconômico x
histórico t-1. Ver ADR-0001 (docs/wayfinder/tech_challenge_fase3/adr/) para
o racional completo da política de leakage e da decisão de arquitetura.

IMPORTANTE (achado de 2026-08-10, corrige a premissa original do ADR-0001):
- `Alunos` nunca entrou no pipeline cloud da Fase 2 — só existe localmente
  (dados/Alunos.csv, produção completa, 57.781 linhas). Não precisa de GCP.
- Território/socioeconômico (populacao_total, gasto_por_habitante_educacao,
  sigla_uf) vive na Silver (`alfabetizacao_municipios_obt`), Parquet no GCS —
  NUNCA foi carregada no BigQuery (só a Gold vai lá). Precisa de acesso ao
  GCS (bucket `tc-alfabetizacao-fiap-879273`, ver ADR-015 da Fase 2), não a
  BigQuery.

Este script assume dois modos de execução:
  --local-only : só processa Alunos.csv (funciona sem nenhuma credencial)
  --full       : também baixa/lê a Silver do GCS e faz o join completo
                 (precisa de `gcsfs` e credenciais GCP configuradas — não
                 executável neste ambiente de trabalho, rodar com Luiz/Renan)

Regra AI Jail (AGENTS.md da Fase 2): este script lê apenas dados_sample ou
Gold quando rodado por IA. Rodar contra `dados/Alunos.csv` completo (produção)
é responsabilidade humana (Luiz/Renan), fora do escopo de execução da IA.
"""
import argparse
from pathlib import Path

import pandas as pd

BASE = Path(__file__).resolve().parents[2]

# Colunas excluídas por política de leakage (ADR-0001) — nunca entram no snapshot
COLUNAS_LEAKAGE = ["proficiencia", "presenca", "preenchimento_caderno"]

# Colunas sem variância/sem uso como feature (EDA, reports/eda_alunos.md item 2)
COLUNAS_SEM_USO = ["serie"]

BUCKET_SILVER = "gs://tc-alfabetizacao-fiap-879273/silver/alfabetizacao_municipios_obt"
COLUNAS_TERRITORIO = ["id_municipio", "ano", "rede", "populacao_total",
                       "gasto_por_habitante_educacao", "sigla_uf"]


def carregar_alunos(caminho_csv: Path) -> pd.DataFrame:
    df = pd.read_csv(caminho_csv)
    df["id_municipio"] = df["id_municipio"].astype(str).str.zfill(7)  # ADR-005 Fase 2
    df = df.drop(columns=[c for c in COLUNAS_LEAKAGE + COLUNAS_SEM_USO if c in df.columns])
    return df


def calcular_historico_t1(alunos: pd.DataFrame) -> pd.DataFrame:
    """
    Absenteísmo histórico por escola, agregado do ano anterior.
    Recalculado a partir do PRÓPRIO Alunos.csv (não precisa de Silver/GCS
    para essa parte) — mas usa a coluna `presenca` do ANO ANTERIOR, que
    não é leakage porque não inclui o aluno do ano sendo predito.

    Atenção: `presenca` já foi removida do dataframe principal (leakage do
    ano atual) — recalcular aqui a partir do CSV bruto, antes do drop.
    """
    bruto = pd.read_csv(BASE / "data" / "Alunos_amostra.csv")
    bruto["id_municipio"] = bruto["id_municipio"].astype(str).str.zfill(7)
    absenteismo_ano = (
        bruto.groupby(["id_escola", "ano"])["presenca"]
        .apply(lambda s: (s == "Ausente").mean())
        .rename("absenteismo_historico_t1")
        .reset_index()
    )
    absenteismo_ano["ano"] = absenteismo_ano["ano"] + 1  # vira feature do ano SEGUINTE
    return absenteismo_ano


def juntar_historico(alunos: pd.DataFrame, historico: pd.DataFrame) -> pd.DataFrame:
    out = alunos.merge(historico, on=["id_escola", "ano"], how="left")
    out["possui_historico_t1"] = out["absenteismo_historico_t1"].notna().astype(int)
    mediana_por_uf = out.groupby("sigla_uf")["absenteismo_historico_t1"].transform("median") \
        if "sigla_uf" in out.columns else out["absenteismo_historico_t1"].median()
    out["absenteismo_historico_t1"] = out["absenteismo_historico_t1"].fillna(mediana_por_uf)
    return out


def juntar_territorio_gcs(alunos: pd.DataFrame) -> pd.DataFrame:
    """Requer gcsfs + credenciais GCP — não executável neste ambiente."""
    silver = pd.read_parquet(BUCKET_SILVER, columns=COLUNAS_TERRITORIO)
    silver["id_municipio"] = silver["id_municipio"].astype(str).str.zfill(7)
    silver = silver.drop_duplicates(subset=["id_municipio", "ano", "rede"])
    return alunos.merge(silver, on=["id_municipio", "ano", "rede"], how="left")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--full", action="store_true",
                         help="Inclui join com Silver no GCS (requer credenciais GCP)")
    parser.add_argument("--input", default=str(BASE / "data" / "Alunos_amostra.csv"),
                         help="CSV de Alunos a processar (default: amostra local)")
    args = parser.parse_args()

    alunos = carregar_alunos(Path(args.input))
    historico = calcular_historico_t1(alunos)
    snapshot = juntar_historico(alunos, historico)

    if args.full:
        snapshot = juntar_territorio_gcs(snapshot)
    else:
        print("Rodando --local-only: sem features de território/socioeconômico "
              "(populacao_total, gasto_por_habitante_educacao, sigla_uf). "
              "Rode com --full (e credenciais GCP) para o snapshot completo.")

    out_path = BASE / "data" / "snapshot_modelagem.parquet"
    snapshot.to_parquet(out_path, index=False)
    print(f"Snapshot salvo em {out_path} — {len(snapshot)} linhas, "
          f"{snapshot.shape[1]} colunas.")


if __name__ == "__main__":
    main()
