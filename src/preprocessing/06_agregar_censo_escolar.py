"""
AGREGACAO DO CENSO ESCOLAR 2023 POR MUNICIPIO (ADR-0011)

POR QUE ESTE SCRIPT EXISTE
--------------------------
O Censo Escolar publica uma linha por ESCOLA. O produto deste projeto decide
por MUNICIPIO (ranking intra-UF, ADR-0004/0005). Este script faz a ponte:
agrega os indicadores de infraestrutura escolar para o grao municipal, do
mesmo jeito que `dados_externos/idhm_municipio_2010.csv` ja serve o IDHM.

POR QUE O ANO E 2023, E NAO 2024 (validade temporal)
----------------------------------------------------
O alvo do ranking e `y = (taxa24 < meta_alfabetizacao_2024)` — desfecho do
ciclo 2024. O Censo Escolar 2024 EXISTE (verificado em 2026-08-31,
HTTP 200), mas tem `Last-Modified: 2026-07-08` no servidor do Inep: usa-lo
para prever o desfecho de 2024 daria ao modelo informacao que nao existia no
momento da decisao — o mesmo skew treino-servico do ADR-0008, e exatamente o
"tratamento de data leakage" que o enunciado da Fase 3 exige (pag. 3).

O Censo 2023 tem data de referencia maio/2023 e foi publicado em fev/2024
(datas internas do zip): precede o desfecho e estava disponivel na epoca.

LIMITACAO A NAO ESQUECER: se este enriquecimento for promovido ao backtest
prospectivo 2025, a escolha do ano precisa ser refeita PARA AQUELE CICLO —
2023 nao serve automaticamente para tudo.

POR QUE O RECORTE DE ESCOLA E ESTE
-----------------------------------
O Indicador Crianca Alfabetizada mede alunos do 2o ano do fundamental da
rede publica. Agregar a infraestrutura de TODAS as escolas do municipio
(incluindo creche, medio, privada) descreveria uma populacao diferente da
que o alvo mede. O filtro reproduz a populacao do indicador:

  1. `TP_SITUACAO_FUNCIONAMENTO == 1`  — escola em atividade
  2. `TP_DEPENDENCIA in (1, 2, 3)`     — federal/estadual/municipal (publica)
  3. `QT_MAT_FUND_AI_2 > 0`            — tem matricula no 2o ano

POR QUE PONDERAR POR MATRICULA, E NAO MEDIA SIMPLES
----------------------------------------------------
Media simples trata uma escola de 400 alunos igual a uma de 12. Um municipio
onde a escola grande tem internet e cinco pequenas nao tem NAO e o mesmo que
o inverso — e a diferenca importa exatamente para o aluno medio, que e a
unidade que o indicador mede. A ponderacao usa `QT_MAT_FUND_AI_2` (matricula
do 2o ano), a populacao do proprio alvo.

SAIDA
-----
    dados_externos/censo_escolar_municipio_2023.csv  — uma linha por municipio

USO
    python src/preprocessing/06_agregar_censo_escolar.py
"""
import sys
import warnings
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BASE = Path(__file__).resolve().parents[2]
URL_CENSO = ("https://download.inep.gov.br/dados_abertos/"
             "microdados_censo_escolar_2023.zip")
SHA256_ESPERADO = "8ed0db8c557137593727b0574d5c99d0abb52491cd7c5769f8cefa98e1fa9e66"
CACHE_ZIP = BASE / "dados_externos" / "_cache_censo_escolar_2023.zip"
CSV_DENTRO_DO_ZIP = "microdados_censo_escolar_2023/dados/microdados_ed_basica_2023.csv"
SAIDA = BASE / "dados_externos" / "censo_escolar_municipio_2023.csv"

# Coluna que define a populacao do Indicador Crianca Alfabetizada (2o ano do
# fundamental) — serve de filtro E de peso da agregacao.
COL_PESO = "QT_MAT_FUND_AI_2"
COL_MUNICIPIO = "CO_MUNICIPIO"

# Indicadores binarios (1/0) de infraestrutura, agrupados por dimensao. Todos
# sao salvos individualmente na saida: a decisao de quais viram feature do
# modelo e tomada DEPOIS da EDA, com numero na mao (nao a priori).
INDICADORES = {
    "saneamento": ["IN_AGUA_POTAVEL", "IN_ESGOTO_REDE_PUBLICA",
                    "IN_ENERGIA_REDE_PUBLICA", "IN_LIXO_SERVICO_COLETA"],
    "conectividade": ["IN_INTERNET", "IN_INTERNET_ALUNOS", "IN_COMPUTADOR",
                       "IN_DESKTOP_ALUNO"],
    "pedagogico": ["IN_BIBLIOTECA", "IN_BIBLIOTECA_SALA_LEITURA",
                    "IN_SALA_LEITURA", "IN_LABORATORIO_INFORMATICA"],
}
TODOS_INDICADORES = [c for grupo in INDICADORES.values() for c in grupo]

COLUNAS_LIDAS = ([COL_MUNICIPIO, "SG_UF", "CO_ENTIDADE", "TP_DEPENDENCIA",
                   "TP_SITUACAO_FUNCIONAMENTO", "TP_LOCALIZACAO", COL_PESO]
                  + TODOS_INDICADORES)


def baixar_censo_se_preciso(destino: Path = CACHE_ZIP, url: str = URL_CENSO) -> Path:
    """
    Baixa o zip do Inep so se ainda nao existir em cache. O zip (32 MB) e o CSV
    extraido (210 MB) ficam FORA do git — a saida versionada e o agregado
    municipal, pequeno, mesmo padrao do IDHM (`.gitignore`).
    """
    if destino.exists():
        print(f"  cache: {destino.name} ({destino.stat().st_size / 1e6:.1f} MB)")
        return destino
    import urllib.request
    print(f"  baixando {url} ...")
    destino.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=600) as r, open(destino, "wb") as f:
        f.write(r.read())
    print(f"  salvo: {destino.name} ({destino.stat().st_size / 1e6:.1f} MB)")
    return destino


def carregar_censo(zip_path: Path = CACHE_ZIP,
                    colunas: list[str] | None = None) -> pd.DataFrame:
    """Le so as colunas necessarias de dentro do zip, sem extrair 210 MB no disco."""
    colunas = colunas if colunas is not None else COLUNAS_LIDAS
    with zipfile.ZipFile(zip_path) as z, z.open(CSV_DENTRO_DO_ZIP) as f:
        return pd.read_csv(f, sep=";", encoding="latin1", usecols=colunas,
                            low_memory=False)


def filtrar_escolas_relevantes(df: pd.DataFrame) -> pd.DataFrame:
    """
    Reduz o Censo a populacao que o Indicador Crianca Alfabetizada mede:
    escola em atividade, da rede publica, com matricula no 2o ano do
    fundamental. Ver docstring do modulo para o porque de cada filtro.

    Cada filtro e aplicado em separado (e nao numa expressao unica) para que
    a contagem de quanto cada um remove seja observavel — a EDA precisa desse
    numero, e um filtro que remove muito mais do que se espera e sinal de
    coluna mal interpretada, nao de dado ruim.
    """
    faltando = [c for c in ("TP_SITUACAO_FUNCIONAMENTO", "TP_DEPENDENCIA", COL_PESO)
                if c not in df.columns]
    if faltando:
        raise ValueError(f"colunas de filtro ausentes no Censo: {faltando}")

    ativa = df["TP_SITUACAO_FUNCIONAMENTO"] == 1
    publica = df["TP_DEPENDENCIA"].isin([1, 2, 3])
    tem_2ano = df[COL_PESO].fillna(0) > 0
    return df[ativa & publica & tem_2ano].copy()


def agregar_por_municipio(df: pd.DataFrame,
                           indicadores: list[str] | None = None,
                           coluna_peso: str = COL_PESO) -> pd.DataFrame:
    """
    Media PONDERADA pela matricula do 2o ano, por municipio.

    Retorna, por municipio: um percentual por indicador (0 a 1), o total de
    matriculas do 2o ano e a contagem de escolas. As duas ultimas colunas nao
    sao decorativas — sem elas, um municipio com 1 escola e outro com 80 tem
    a mesma aparencia na tabela, e a diferenca de confianca some.

    Indicador nulo e excluido do peso daquele indicador (nao vira zero): tratar
    ausencia de resposta como "nao tem" inventaria um dado que o Censo nao
    afirma. Se TODAS as escolas do municipio tem nulo num indicador, o
    resultado e NaN — e o `SimpleImputer` do pipeline decide, como ja faz com
    o IDHM (ADR-0009).
    """
    indicadores = indicadores if indicadores is not None else TODOS_INDICADORES
    if coluna_peso not in df.columns:
        raise ValueError(f"coluna de peso ausente: {coluna_peso}")

    peso = df[coluna_peso].fillna(0).astype(float)
    saida = {}
    for col in indicadores:
        valores = pd.to_numeric(df[col], errors="coerce")
        valido = valores.notna()
        num = (valores.fillna(0) * peso * valido).groupby(df[COL_MUNICIPIO]).sum()
        den = (peso * valido).groupby(df[COL_MUNICIPIO]).sum()
        # np.nan, nao pd.NA: pd.NA quebra o astype(float) seguinte (pego por
        # test_municipio_com_indicador_todo_nulo_vira_nan_nao_zero).
        saida[col] = (num / den.replace(0, np.nan)).astype(float)

    agg = pd.DataFrame(saida)
    agg["mat_2ano_total"] = peso.groupby(df[COL_MUNICIPIO]).sum().astype(int)
    agg["n_escolas_2ano"] = df.groupby(COL_MUNICIPIO).size().astype(int)
    agg.index.name = COL_MUNICIPIO
    return agg.reset_index()


def criar_indices_compostos(agg: pd.DataFrame,
                             grupos: dict[str, list[str]] | None = None
                             ) -> pd.DataFrame:
    """
    Reduz os indicadores individuais a um indice por dimensao (media simples
    dos indicadores do grupo).

    POR QUE: `FEATURES_BASE` tem 4 colunas e varias UFs treinam com 40-100
    municipios (piso do ADR-0004). Somar 12 features individuais nesse regime
    e convite a overfitting — 3 indices mantem a dimensionalidade na mesma
    ordem de grandeza do enriquecimento anterior (`FEATURES_IDHM`, 4 colunas).
    Os indicadores individuais continuam na saida para a EDA e para a
    interpretacao; o indice e o que o modelo consome.
    """
    grupos = grupos if grupos is not None else INDICADORES
    out = agg.copy()
    for nome, colunas in grupos.items():
        presentes = [c for c in colunas if c in out.columns]
        if not presentes:
            raise ValueError(f"nenhuma coluna do grupo '{nome}' presente")
        out[f"infra_{nome}"] = out[presentes].mean(axis=1, skipna=True).round(4)
    return out


def main():
    print("=" * 74)
    print("AGREGACAO — Censo Escolar 2023 por municipio (ADR-0011)")
    print("=" * 74)

    print("\n[1/4] Fonte...")
    baixar_censo_se_preciso()

    print("\n[2/4] Lendo o Censo (so as colunas necessarias)...")
    df = carregar_censo()
    print(f"  {len(df):,} escolas no arquivo".replace(",", "."))

    print("\n[3/4] Filtrando a populacao do indicador...")
    ativa = int((df["TP_SITUACAO_FUNCIONAMENTO"] == 1).sum())
    publica = int(((df["TP_SITUACAO_FUNCIONAMENTO"] == 1)
                   & df["TP_DEPENDENCIA"].isin([1, 2, 3])).sum())
    rel = filtrar_escolas_relevantes(df)
    print(f"  em atividade:                      {ativa:,}".replace(",", "."))
    print(f"  + rede publica:                    {publica:,}".replace(",", "."))
    print(f"  + com matricula no 2o ano:         {len(rel):,}".replace(",", "."))
    print(f"  matriculas de 2o ano cobertas:     "
          f"{int(rel[COL_PESO].sum()):,}".replace(",", "."))

    print("\n[4/4] Agregando por municipio (ponderado por matricula)...")
    agg = agregar_por_municipio(rel)
    agg = criar_indices_compostos(agg)
    agg[COL_MUNICIPIO] = agg[COL_MUNICIPIO].astype(str).str.zfill(7)
    agg = agg.rename(columns={COL_MUNICIPIO: "id_municipio"})

    print(f"  municipios com dado: {len(agg):,}".replace(",", "."))
    print(f"  (universo do Censo 2023: {df[COL_MUNICIPIO].nunique():,} municipios)"
          .replace(",", "."))

    SAIDA.parent.mkdir(parents=True, exist_ok=True)
    agg.to_csv(SAIDA, index=False, encoding="utf-8")
    print(f"\n  {SAIDA}")

    print("\n  Indices compostos (media entre municipios):")
    for nome in INDICADORES:
        col = f"infra_{nome}"
        print(f"    {col:<24} {agg[col].mean():.3f}")


if __name__ == "__main__":
    main()
