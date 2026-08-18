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

# ATENÇÃO (correção de 2026-08-18, motivada pelo feedback oficial da Fase 2 —
# ver docs/HANDOFF_RENAN.md, Capítulo 6):
# Apontamos para a OBT *com metas imputadas*, não para a OBT base. A imputação
# KNN de metas (dataproc_05_knn_metas.py, ADR-004 da Fase 2) foi o primeiro
# ponto forte citado pelo avaliador — cobertura 43,6% → 100%, holdout MAE
# 5,12pp — e estava sendo ignorada por esta extração. O enunciado da Fase 3
# pede explicitamente "metas estaduais e municipais" entre as variáveis.
BUCKET_SILVER = ("gs://tc-alfabetizacao-fiap-879273/silver/"
                  "alfabetizacao_municipios_obt_com_metas_imputadas")

# `meta_alfabetizacao_2024` (original, com NULLs) vem junto NÃO como feature,
# mas para derivar o flag `meta_is_imputada` — a tabela do KNN não grava esse
# flag, e usar meta imputada sem marcar que é imputada repete exatamente o erro
# de rotulagem que o avaliador apontou no dashboard da Fase 2 (crítica (b) do
# Cap. 1.2 do HANDOFF_RENAN.md). O flag é descartado do modelo se a cobertura
# real de meta original for baixa demais para ele significar algo.
COLUNAS_TERRITORIO = ["id_municipio", "ano", "rede", "populacao_total",
                       "gasto_por_habitante_educacao", "sigla_uf",
                       "meta_alfabetizacao_2024", "meta_alfabetizacao_2024_imputada"]


def carregar_alunos(caminho_csv: Path) -> pd.DataFrame:
    df = pd.read_csv(caminho_csv)
    df["id_municipio"] = df["id_municipio"].astype(str).str.zfill(7)  # ADR-005 Fase 2

    # Coluna de AUDITORIA (2026-08-18), nunca feature — prefixo `_` marca isso.
    # Motivo: 100% dos alunos ausentes têm alfabetizado="Não" por CONVENÇÃO do
    # dado (não fez prova => não alfabetizado), não por medição. São 16,7% da
    # amostra. Manter ou remover essas linhas da população de modelagem é uma
    # decisão em aberto (Cap. 10.2 do HANDOFF_RENAN.md) — e ela só pode ser
    # analisada se soubermos QUEM são, mesmo depois de `presenca` sair por
    # leakage. Daí registrar aqui, explicitamente fora do modelo.
    if "presenca" in df.columns:
        df["_ausente_no_exame"] = (df["presenca"] == "Ausente").astype(int)

    df = df.drop(columns=[c for c in COLUNAS_LEAKAGE + COLUNAS_SEM_USO if c in df.columns])
    return df


def calcular_historico_t1(caminho_csv: Path) -> pd.DataFrame:
    """
    Absenteísmo histórico por escola, agregado do ano anterior.
    Recalculado a partir do PRÓPRIO Alunos.csv (não precisa de Silver/GCS
    para essa parte) — mas usa a coluna `presenca` do ANO ANTERIOR, que
    não é leakage porque não inclui o aluno do ano sendo predito.

    Atenção: `presenca` já foi removida do dataframe principal (leakage do
    ano atual) — recalcular aqui a partir do CSV bruto, antes do drop.

    CORREÇÃO (2026-08-18): esta função lia `data/Alunos_amostra.csv` FIXO,
    ignorando o arquivo passado em `--input`. Rodar com a base completa
    (57.781 linhas) calcularia o histórico sobre a amostra de 5.000 e faria o
    join na base inteira — silenciosamente errado, sem erro nenhum.
    """
    bruto = pd.read_csv(caminho_csv)
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
    """Só faz o join e marca disponibilidade. A imputação vem depois (ver abaixo)."""
    out = alunos.merge(historico, on=["id_escola", "ano"], how="left")
    out["possui_historico_t1"] = out["absenteismo_historico_t1"].notna().astype(int)
    return out


def imputar_historico(snapshot: pd.DataFrame) -> pd.DataFrame:
    """
    Imputa `absenteismo_historico_t1` pela mediana da UF (ADR-0001 §2.3), com
    fallback para mediana global quando a UF não está disponível.

    CORREÇÃO (2026-08-18): a imputação estava dentro de `juntar_historico`,
    que roda ANTES do join de território — e `sigla_uf` só chega nesse join.
    Resultado: a condição `if "sigla_uf" in out.columns` era sempre falsa e a
    mediana-por-UF documentada no ADR-0001 NUNCA executou, nem no `--full`.
    Caía sempre no fallback global, sem aviso. Agora a imputação é um passo
    separado, chamado depois do território.
    """
    col = "absenteismo_historico_t1"
    if "sigla_uf" in snapshot.columns:
        mediana = snapshot.groupby("sigla_uf")[col].transform("median")
        # UF inteira sem histórico -> transform devolve NaN; completa com global
        mediana = mediana.fillna(snapshot[col].median())
        origem = "mediana da UF (ADR-0001 2.3)"
    else:
        mediana = snapshot[col].median()
        origem = "mediana GLOBAL (sem sigla_uf -- modo --local-only)"
    n_imp = int(snapshot[col].isna().sum())
    snapshot[col] = snapshot[col].fillna(mediana)
    print(f"Historico t-1: {n_imp} de {len(snapshot)} linhas imputadas "
          f"({n_imp / len(snapshot):.1%}) por {origem}.")
    return snapshot


def juntar_territorio_gcs(alunos: pd.DataFrame) -> pd.DataFrame:
    """
    Requer gcsfs + credenciais GCP — não executável neste ambiente.

    Traz território/socioeconômico + a meta imputada (ADR-004 da Fase 2).
    A meta é feature legítima (não leakage): é definida externamente pelo PDE,
    não deriva do desempenho do aluno sendo predito — mesmo raciocínio que
    validou populacao_total/gasto_por_habitante_educacao no ADR-0001. Já
    `gap_meta` e `taxa_alfabetizacao` continuam FORA (circulares, calculadas a
    partir do desempenho do próprio ano).
    """
    silver = pd.read_parquet(BUCKET_SILVER, columns=COLUNAS_TERRITORIO)
    silver["id_municipio"] = silver["id_municipio"].astype(str).str.zfill(7)
    silver = silver.drop_duplicates(subset=["id_municipio", "ano", "rede"])

    # Flag de imputação derivado: a tabela do KNN não grava essa marcação.
    # Meta imputada sem rótulo = o erro de rotulagem apontado na Fase 2.
    silver["meta_is_imputada"] = silver["meta_alfabetizacao_2024"].isna().astype(int)
    silver = silver.drop(columns=["meta_alfabetizacao_2024"])

    out = alunos.merge(silver, on=["id_municipio", "ano", "rede"], how="left")

    cobertura = out["meta_alfabetizacao_2024_imputada"].notna().mean()
    pct_imputada = out["meta_is_imputada"].mean()
    print(f"Meta: cobertura {cobertura:.1%} das linhas | "
          f"{pct_imputada:.1%} vêm de imputação KNN (não de meta oficial do PDE).")
    if pct_imputada > 0.5:
        print("  ATENÇÃO: maioria das metas é imputada — checar no SHAP se o "
              "modelo está aprendendo o artefato de imputação, não a meta real.")

    return out


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--full", action="store_true",
                         help="Inclui join com Silver no GCS (requer credenciais GCP)")
    parser.add_argument("--input", default=str(BASE / "data" / "Alunos_amostra.csv"),
                         help="CSV de Alunos a processar (default: amostra local)")
    args = parser.parse_args()

    alunos = carregar_alunos(Path(args.input))
    historico = calcular_historico_t1(Path(args.input))
    snapshot = juntar_historico(alunos, historico)

    if args.full:
        snapshot = juntar_territorio_gcs(snapshot)

    # Só aqui `sigla_uf` existe, se existir (ver imputar_historico).
    snapshot = imputar_historico(snapshot)

    if not args.full:
        print("Rodando --local-only: sem território/socioeconômico "
              "(populacao_total, gasto_por_habitante_educacao, sigla_uf) e "
              "SEM META (meta_alfabetizacao_2024_imputada, meta_is_imputada). "
              "Rode com --full (e credenciais GCP) para o snapshot completo.")

    out_path = BASE / "data" / "snapshot_modelagem.parquet"
    snapshot.to_parquet(out_path, index=False)
    print(f"Snapshot salvo em {out_path} — {len(snapshot)} linhas, "
          f"{snapshot.shape[1]} colunas.")


if __name__ == "__main__":
    main()
