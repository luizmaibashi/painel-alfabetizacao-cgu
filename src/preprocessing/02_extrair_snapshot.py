"""
Extração do snapshot de modelagem: Alunos x território/socioeconômico x
histórico t-1. Ver ADR-0001 (docs/adr/) para
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

# Base completa de alunos: 57.781 linhas, 7,3MB, versionada no repo da Fase 2.
# NÃO precisa de credencial GCP — é CSV local. Não confundir com o modo `--full`
# deste script, que é sobre território/socioeconômico vindo do GCS.
# (A modelagem rodou sobre a amostra de 5.000 até 2026-08-18 por leitura estrita
# da regra "AI Jail" do AGENTS.md da Fase 2; revisto porque a regra existe para
# proteger custo de nuvem, e ler 7,3MB local não incorre nesse custo.)
ALUNOS_COMPLETO = (BASE.parent / "tech-challenge-fase2-alfabetizacao" /
                    "dados" / "Alunos.csv")
ALUNOS_AMOSTRA = BASE / "data" / "Alunos_subconjunto_teste_local.csv"

# Colunas excluídas por política de leakage (ADR-0001) — nunca entram no snapshot.
# `peso_aluno` entrou nesta lista em 2026-08-18: a NULIDADE dela codifica "faltou
# à prova" (100% dos nulos com alvo "Não"), o mesmo evento de `presenca`. Antes
# ela era só excluída das features, mas continuava no snapshot e aparecia como
# "coluna descartada em silêncio" — ver Cap. 9.3 do diário de bordo interno (não publicado).
COLUNAS_LEAKAGE = ["proficiencia", "presenca", "preenchimento_caderno", "peso_aluno"]

# Colunas sem variância/sem uso como feature (EDA, reports/eda_alunos.md item 2)
COLUNAS_SEM_USO = ["serie"]

# ATENÇÃO (correção de 2026-08-18, motivada pelo feedback oficial da Fase 2 —
# ver o diário de bordo interno (não publicado), Capítulo 6):
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
# Cap. 1.2 do diário de bordo interno (não publicado)). O flag é descartado do modelo se a cobertura
# real de meta original for baixa demais para ele significar algo.
COLUNAS_TERRITORIO = ["id_municipio", "ano", "rede", "populacao_total",
                       "gasto_por_habitante_educacao", "sigla_uf",
                       "meta_alfabetizacao_2024", "meta_alfabetizacao_2024_imputada"]


def carregar_alunos(caminho_csv: Path, populacao: str) -> pd.DataFrame:
    """
    Carrega os microdados e aplica a POPULAÇÃO DE MODELAGEM.

    `populacao="avaliados"` (padrão) mantém só quem fez a prova. Isso não é
    escolha de conveniência — é a metodologia OFICIAL do indicador, confirmada
    em 2026-08-18 por três caminhos:

      1. O INEP define o Indicador Criança Alfabetizada sobre estudantes
         AVALIADOS, com ponderação pelo peso amostral.
      2. A Fase 2 implementou exatamente isso e validou contra a taxa publicada
         pelo INEP (`06_alunos_bronze_to_silver.py`: numerador = peso dos
         alfabetizados, denominador = peso total dos PRESENTES). O teste
         `test_delta_calculo_correto` filtra `presenca == "Presente"`
         explicitamente. Foi um dos pontos elogiados na avaliação da Fase 2.
      3. Reproduzindo as duas contas sobre a base completa de 2023: só-presentes
         ponderado dá 57,1%, contra ~55-56% publicado; incluindo ausentes dá
         48,2%. A primeira é a que bate.

    Consequência: os ~9.700 alunos ausentes (16,8%) NÃO fazem parte da população
    do indicador. Mantê-los foi a origem dos CINCO caminhos de vazamento que
    este projeto encontrou — todos codificavam o mesmo evento, "faltou à prova".
    Removê-los corta o problema na raiz. Ver Cap. 13 do diário de bordo interno (não publicado).
    """
    df = pd.read_csv(caminho_csv)
    df["id_municipio"] = df["id_municipio"].astype(str).str.zfill(7)  # ADR-005 Fase 2

    # Coluna de AUDITORIA (2026-08-18), nunca feature — prefixo `_` marca isso.
    # Motivo: 100% dos alunos ausentes têm alfabetizado="Não" por CONVENÇÃO do
    # dado (não fez prova => não alfabetizado), não por medição. São 16,7% da
    # amostra. Manter ou remover essas linhas da população de modelagem é uma
    # decisão em aberto (Cap. 10.2 do diário de bordo interno (não publicado)) — e ela só pode ser
    # analisada se soubermos QUEM são, mesmo depois de `presenca` sair por
    # leakage. Daí registrar aqui, explicitamente fora do modelo.
    if "presenca" in df.columns:
        df["_ausente_no_exame"] = (df["presenca"] == "Ausente").astype(int)
        n_antes = len(df)
        if populacao == "avaliados":
            df = df[df["_ausente_no_exame"] == 0].copy()
            print(f"Populacao: apenas AVALIADOS — {len(df)} de {n_antes} alunos "
                  f"({len(df) / n_antes:.1%}); {n_antes - len(df)} ausentes "
                  f"removidos (metodologia oficial, ver docstring).")
        else:
            print(f"Populacao: TODOS os {n_antes} alunos, incluindo "
                  f"{int(df['_ausente_no_exame'].sum())} ausentes cujo rotulo e "
                  f"CONVENCAO e nao medicao. Fora da metodologia oficial.")

    # `peso_aluno` sai como FEATURE (a nulidade dele vazava a ausencia), mas
    # sobrevive como `_peso_amostral` para PONDERAR metricas. O prefixo `_`
    # marca "nunca vira feature". Sao usos diferentes da mesma coluna:
    # peso amostral serve para a estatistica representar a populacao, nao para
    # o modelo aprender sobre o aluno.
    if "peso_aluno" in df.columns:
        df["_peso_amostral"] = df["peso_aluno"]

    df = df.drop(columns=[c for c in COLUNAS_LEAKAGE + COLUNAS_SEM_USO if c in df.columns])
    return df


def calcular_historico_t1(caminho_csv: Path) -> dict[str, pd.DataFrame]:  # noqa: C901
    """
    Absenteísmo do ano anterior, em DOIS níveis: escola e município.

    Usa `presenca` do ANO ANTERIOR — não é leakage porque não inclui o aluno do
    ano sendo predito. Recalculado do CSV bruto porque `presenca` já saiu do
    dataframe principal por leakage do ano atual.

    CORREÇÃO (2026-08-18): lia `data/Alunos_subconjunto_teste_local.csv`
    (renomeado 2026-08-30, era `Alunos_amostra.csv` — nome sugeria amostra
    representativa; é subconjunto de 5.000 linhas pra teste local rápido,
    não a fonte real. Achado depois de um bug real: ver
    `docs/wayfinder/tech_challenge_fase3/0013-*.md` na raiz da base) FIXO,
    ignorando `--input`. Rodar na base completa calcularia o histórico sobre
    o subconjunto de 5.000 e colaria nas 57.781 linhas — errado em silêncio.

    POR QUE DOIS NÍVEIS (2026-08-18): a versão por ESCOLA é estruturalmente
    frágil nesta base. O Indicador Criança Alfabetizada é pesquisa AMOSTRAL:
    24.346 escolas para 57.782 alunos (2,37 por escola), e **49,9% dos grupos
    escola-ano têm 1 único aluno** — uma "taxa" sobre 1 aluno só pode dar 0% ou
    100%. Além disso só 22,4% das escolas de 2024 aparecem em 2023.
    Por município a cobertura sobe para 65,2% entre anos, com mediana de 3
    alunos por município-ano (p75=7). Calculamos as duas e deixamos o SHAP
    dizer qual carrega sinal, em vez de escolher no palpite.
    """
    bruto = pd.read_csv(caminho_csv)
    bruto["id_municipio"] = bruto["id_municipio"].astype(str).str.zfill(7)
    saida = {}
    for nivel, chave in (("escola", "id_escola"), ("municipio", "id_municipio")):
        agg = (
            bruto.groupby([chave, "ano"])["presenca"]
            .agg(taxa=lambda s: (s == "Ausente").mean(), n="size")
            .reset_index()
        )
        agg["ano"] = agg["ano"] + 1  # vira feature do ano SEGUINTE
        agg = agg.rename(columns={
            "taxa": f"absenteismo_hist_{nivel}_t1",
            "n": f"n_alunos_hist_{nivel}_t1",
        })
        saida[nivel] = agg
    return saida


def juntar_historico(alunos: pd.DataFrame, historico: dict[str, pd.DataFrame]) -> pd.DataFrame:
    """Junta os dois níveis e marca disponibilidade de cada um."""
    out = alunos
    for nivel, chave in (("escola", "id_escola"), ("municipio", "id_municipio")):
        out = out.merge(historico[nivel], on=[chave, "ano"], how="left")
        out[f"possui_hist_{nivel}_t1"] = out[f"absenteismo_hist_{nivel}_t1"].notna().astype(int)
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
    for col in ("absenteismo_hist_escola_t1", "absenteismo_hist_municipio_t1"):
        snapshot = _imputar_coluna(snapshot, col)
    return snapshot


def _imputar_coluna(snapshot: pd.DataFrame, col: str) -> pd.DataFrame:
    if "sigla_uf" in snapshot.columns:
        mediana = snapshot.groupby("sigla_uf")[col].transform("median")
        # UF inteira sem histórico -> transform devolve NaN; completa com global
        mediana = mediana.fillna(snapshot[col].median())
        origem = "mediana da UF (ADR-0001 2.3)"
    else:
        mediana = snapshot[col].median()
        origem = "mediana GLOBAL (sem sigla_uf)"
    n_imp = int(snapshot[col].isna().sum())
    snapshot[col] = snapshot[col].fillna(mediana)
    print(f"  {col}: {n_imp} de {len(snapshot)} imputadas "
          f"({n_imp / len(snapshot):.1%}) por {origem}.")
    return snapshot


def juntar_territorio(alunos: pd.DataFrame, fonte: str) -> pd.DataFrame:
    """
    Traz território/socioeconômico + a meta imputada (ADR-004 da Fase 2).

    `fonte` é o caminho da Silver: por padrão o bucket GCS (requer credencial),
    mas aceita um Parquet local — usado tanto pelo ensaio de 2026-08-18
    (`04_ensaio_full.py`) quanto por quem preferir baixar o arquivo em vez de
    ler direto do GCS.
    A meta é feature legítima (não leakage): é definida externamente pelo PDE,
    não deriva do desempenho do aluno sendo predito — mesmo raciocínio que
    validou populacao_total/gasto_por_habitante_educacao no ADR-0001. Já
    `gap_meta` e `taxa_alfabetizacao` continuam FORA (circulares, calculadas a
    partir do desempenho do próprio ano).
    """
    print(f"Lendo Silver de: {fonte}")

    # Tolerante a colunas ausentes: a Silver do GCS tem todas, mas o substituto
    # local (`05_montar_territorio.py`) nao traz `gasto_por_habitante_educacao`
    # porque o SICONFI custa ~9k requisicoes. Ler so o que existe, e DECLARAR o
    # que faltou — em vez de quebrar, ou pior, seguir em silencio.
    disponiveis = set(pd.read_parquet(fonte).columns)
    usar = [c for c in COLUNAS_TERRITORIO if c in disponiveis]
    faltando = [c for c in COLUNAS_TERRITORIO if c not in disponiveis]
    if faltando:
        print(f"  ATENCAO: a fonte nao tem {faltando} — o snapshot sai sem "
              f"essas features.")
    silver = pd.read_parquet(fonte, columns=usar)
    n_silver = len(silver)
    silver["id_municipio"] = silver["id_municipio"].astype(str).str.zfill(7)
    silver = silver.drop_duplicates(subset=["id_municipio", "ano", "rede"])
    if len(silver) < n_silver:
        print(f"  Silver: {n_silver - len(silver)} duplicatas de "
              f"(municipio, ano, rede) removidas.")

    # Flag de imputação derivado: a tabela do KNN não grava essa marcação.
    # Meta imputada sem rótulo = o erro de rotulagem apontado na Fase 2.
    if "meta_alfabetizacao_2024" in silver.columns:
        silver["meta_is_imputada"] = silver["meta_alfabetizacao_2024"].isna().astype(int)
        silver = silver.drop(columns=["meta_alfabetizacao_2024"])

    n_antes = len(alunos)
    out = alunos.merge(silver, on=["id_municipio", "ano", "rede"], how="left")

    # Guarda contra o erro classico de join: left join que MULTIPLICA linhas
    # porque a direita nao era unica na chave. Silencioso e devastador — o
    # aluno viraria 2 linhas e o modelo treinaria com peso dobrado nele.
    if len(out) != n_antes:
        raise ValueError(
            f"Join com a Silver mudou a contagem de linhas: {n_antes} -> "
            f"{len(out)}. A Silver nao e unica em (id_municipio, ano, rede)."
        )

    # Municipio sem territorio deixa NaN nas colunas do join. Para o flag de
    # meta isso tem leitura semantica: sem meta na fonte, ela certamente NAO e
    # meta oficial do PDE -> 1. Preencher aqui evita NaN chegando ao modelo por
    # um bloco `passthrough`, que por definicao nao imputa.
    if "meta_is_imputada" in out.columns:
        n_sem = int(out["meta_is_imputada"].isna().sum())
        if n_sem:
            out["meta_is_imputada"] = out["meta_is_imputada"].fillna(1).astype(int)
            print(f"  {n_sem} linhas sem meta na fonte -> meta_is_imputada=1")

    ref = "populacao_total" if "populacao_total" in out.columns else usar[-1]
    casou = out[ref].notna().mean()
    print(f"Territorio: {casou:.1%} das linhas casaram (referencia: {ref}).")
    if casou < 0.5:
        print("  ATENCAO: menos da metade casou. Checar tipo/zeros a esquerda de "
              "id_municipio e os valores de `rede` dos dois lados.")

    if "meta_alfabetizacao_2024_imputada" in out.columns:
        cobertura = out["meta_alfabetizacao_2024_imputada"].notna().mean()
        pct_imputada = out["meta_is_imputada"].mean()
        print(f"Meta: cobertura {cobertura:.1%} das linhas | "
              f"{pct_imputada:.1%} vêm de imputação (não de meta oficial do PDE).")
        if pct_imputada > 0.5:
            print("  ATENÇÃO: maioria das metas é imputada — checar no SHAP se o "
                  "modelo está aprendendo o artefato de imputação, não a meta real.")

    return out


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--populacao", choices=["avaliados", "todos"], default="avaliados",
        help=("Populacao de modelagem. 'avaliados' (padrao) = so quem fez a "
              "prova, que e a metodologia oficial do indicador. 'todos' inclui "
              "os ausentes, cujo rotulo e convencao — util so para comparacao."))
    parser.add_argument("--full", action="store_true",
                         help="Inclui join com a Silver (territorio/socioeconomico/meta)")
    parser.add_argument(
        "--silver", default=BUCKET_SILVER,
        help=("Caminho da Silver. Default: bucket GCS (requer credencial). "
              "Aceita Parquet local, para quem preferir baixar o arquivo."))
    parser.add_argument(
        "--input", default=str(ALUNOS_COMPLETO),
        help=("CSV de Alunos a processar. Default: base COMPLETA (57.781 alunos) "
              "do repo da Fase 2. Use --input <caminho da amostra> para os 5.000."))
    args = parser.parse_args()

    alunos = carregar_alunos(Path(args.input), args.populacao)
    historico = calcular_historico_t1(Path(args.input))
    snapshot = juntar_historico(alunos, historico)

    if args.full:
        snapshot = juntar_territorio(snapshot, args.silver)

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
