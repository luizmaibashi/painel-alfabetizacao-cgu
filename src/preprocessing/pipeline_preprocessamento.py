"""
Define o pré-processamento como ColumnTransformer, integrado ao modelo via
Pipeline (requisito do enunciado: "integração do pré-processamento
diretamente ao modelo"). Ver ADR-0001 para a política de leakage que decide
quais colunas entram aqui.

Import este módulo em vez de duplicar a lógica — evita divergência entre
o que foi usado no treino e o que seria usado em produção (training-serving
skew, ver .claude/rules/dados.md).

ADAPTATIVO POR SNAPSHOT (correção de 2026-08-18)
-------------------------------------------------
As listas de colunas eram FIXAS e cobriam só o modo `--local-only`. Território,
socioeconômico e meta (que só existem no snapshot `--full`) NÃO estavam em
nenhuma lista — o extrator os traria e o preprocessador os descartaria em
silêncio, sem erro nenhum. O `--full` rodaria e daria quase o mesmo resultado
ruim do `--local-only`, sem explicação visível.

É o mesmo padrão que o avaliador da Fase 2 apontou no streaming ("o evento
chega, é validado, é persistido, e para ali") — ver Cap. 6 do HANDOFF_RENAN.md.

Agora as colunas são resolvidas a partir do que o snapshot realmente contém:
`colunas_feature(df)` e `construir_preprocessador(df)` recebem o dataframe.
Colunas declaradas mas ausentes são ignoradas; colunas presentes mas não
declaradas são REPORTADAS (`colunas_ignoradas`), para nunca mais uma feature
entrar no snapshot e sumir sem ninguém ver.
"""
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, RobustScaler

# Colunas fora do modelo, sempre (ADR-0001): proficiencia, presenca,
# preenchimento_caderno já nem existem no snapshot (removidas na extração).
# Identificadores não são feature (mas seguem no dataframe para split/auditoria).
COLUNAS_ID = ["ano", "id_municipio", "id_municipio_nome", "id_escola", "id_aluno",
               "_ausente_no_exame"]  # `_` = auditoria, nunca feature
COLUNA_TARGET = "alfabetizado"

# --- Catálogo de features candidatas (nem todas existem em todo snapshot) ---

# --- POR QUE `peso_aluno` NÃO ESTÁ AQUI (removido em 2026-08-18) ---
# A NULIDADE de `peso_aluno` codifica o evento "aluno faltou à prova": os 835
# nulos da amostra têm alfabetizado="Não" em 100% dos casos (contra 41% no
# resto), e 834 deles são exatamente os `presenca="Ausente"`. Depois do
# SimpleImputer(median), todos recebem o mesmo valor exato — e "peso_aluno ==
# mediana" vira bandeira de ausência, com pureza de 94,7%.
#
# É o MESMO vazamento que o ADR-0001 §2.2 já removeu ao excluir `presenca` e
# `preenchimento_caderno`; ele apenas entrava pela ausência do valor, não pelo
# valor. Excluir aqui é aplicar a política existente, não criar política nova.
#
# Efeito medido: uma regra única "peso_aluno é nulo -> risco" atinge
# Precision 1,000. Sem essa coluna e sem os alunos ausentes, o ROC-AUC do
# modelo cai para 0,497 — ou seja, todo o desempenho aparente vinha daqui.
# Detalhe completo no Cap. 9 do docs/HANDOFF_RENAN.md.
#
# Numéricas restantes -> Robust Scaling, não Standardization (aula 6:
# mediana/IQR, não sensível a outlier). Protege `populacao_total`, que é
# fortemente assimétrica (São Paulo vs. município rural).
CANDIDATAS_NUMERICAS = [
    # Histórico t-1 em dois níveis (2026-08-18). O nível ESCOLA é estruturalmente
    # frágil nesta base amostral (49,9% dos grupos escola-ano têm 1 aluno só, e
    # só 22,4% das escolas de 2024 aparecem em 2023); o nível MUNICÍPIO tem
    # 65,2% de cobertura. Mantemos os dois para o SHAP mostrar qual carrega
    # sinal, em vez de escolhermos no palpite.
    "absenteismo_hist_escola_t1",
    "absenteismo_hist_municipio_t1",
    # Quantos alunos sustentam cada taxa acima — uma taxa vinda de 1 aluno vale
    # 0% ou 100% e não é taxa. Entra como feature para o modelo poder distinguir
    # taxa confiável de taxa frágil.
    "n_alunos_hist_escola_t1",
    "n_alunos_hist_municipio_t1",
    # Só existem no snapshot --full (território/socioeconômico via GCS):
    "populacao_total",
    "gasto_por_habitante_educacao",
    # Só existe no --full: meta do PDE, imputada por KNN na Fase 2 (ADR-004).
    # NÃO é leakage: definida externamente por política pública, não deriva do
    # desempenho do aluno predito (ver Cap. 6.3 do HANDOFF_RENAN.md).
    "meta_alfabetizacao_2024_imputada",
]

# Categóricas de baixa cardinalidade -> One-Hot, seguro (aula 6).
# sigla_uf tem 27 valores: cardinalidade média, aceitável para One-Hot com
# handle_unknown="ignore", mas vale checar no SHAP se domina (ADR-0001 §5,
# cenário de regressão 1: modelo virar "o baseline municipal disfarçado").
CANDIDATAS_CATEGORICAS = ["caderno", "rede", "sigla_uf"]

# Binárias já numéricas (0/1) -> passthrough.
# Ambas marcam DISPONIBILIDADE DE DADO, não característica do aluno. São
# necessárias (usar valor imputado sem sinalizar que é imputado esconde o
# artefato), mas se aparecerem no topo do SHAP é sinal de que o modelo está
# lendo o artefato de imputação, não sinal real (ADR-0001 §5, cenário 3).
CANDIDATAS_PASSTHROUGH = ["possui_hist_escola_t1", "possui_hist_municipio_t1",
                           "meta_is_imputada"]

TODAS_CANDIDATAS = (
    CANDIDATAS_NUMERICAS + CANDIDATAS_CATEGORICAS + CANDIDATAS_PASSTHROUGH
)


def _presentes(candidatas: list[str], df: pd.DataFrame) -> list[str]:
    return [c for c in candidatas if c in df.columns]


def colunas_por_tipo(df: pd.DataFrame) -> dict[str, list[str]]:
    """Resolve quais features existem de fato neste snapshot."""
    return {
        "numericas": _presentes(CANDIDATAS_NUMERICAS, df),
        "categoricas": _presentes(CANDIDATAS_CATEGORICAS, df),
        "passthrough": _presentes(CANDIDATAS_PASSTHROUGH, df),
    }


def colunas_feature(df: pd.DataFrame) -> list[str]:
    """Colunas de entrada do preprocessador, na ordem que ele espera."""
    tipos = colunas_por_tipo(df)
    return tipos["numericas"] + tipos["categoricas"] + tipos["passthrough"]


def colunas_ignoradas(df: pd.DataFrame) -> list[str]:
    """
    Colunas do snapshot que NÃO são feature, target nem identificador.

    Existe para tornar visível o erro que esta refatoração corrigiu: uma coluna
    nova entrar no snapshot e ser descartada em silêncio. Quem treina deve
    imprimir isso e conferir que cada nome ali é descarte intencional.
    """
    conhecidas = set(TODAS_CANDIDATAS) | set(COLUNAS_ID) | {COLUNA_TARGET}
    return [c for c in df.columns if c not in conhecidas]


def construir_preprocessador(df: pd.DataFrame) -> ColumnTransformer:
    tipos = colunas_por_tipo(df)

    pipeline_numerica = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", RobustScaler()),
    ])
    pipeline_categorica = Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("onehot", OneHotEncoder(handle_unknown="ignore")),
    ])

    blocos = []
    if tipos["numericas"]:
        blocos.append(("num", pipeline_numerica, tipos["numericas"]))
    if tipos["categoricas"]:
        blocos.append(("cat", pipeline_categorica, tipos["categoricas"]))
    if tipos["passthrough"]:
        blocos.append(("bin", "passthrough", tipos["passthrough"]))

    if not blocos:
        raise ValueError(
            "Nenhuma feature conhecida encontrada no snapshot. Colunas "
            f"disponíveis: {list(df.columns)}"
        )
    return ColumnTransformer(blocos)


def descrever_features(df: pd.DataFrame) -> str:
    """Resumo legível para log de treino — o que entrou e o que ficou de fora."""
    tipos = colunas_por_tipo(df)
    ignoradas = colunas_ignoradas(df)
    ausentes = [c for c in TODAS_CANDIDATAS if c not in df.columns]

    linhas = [
        f"Features numéricas ({len(tipos['numericas'])}): {tipos['numericas']}",
        f"Features categóricas ({len(tipos['categoricas'])}): {tipos['categoricas']}",
        f"Features binárias ({len(tipos['passthrough'])}): {tipos['passthrough']}",
    ]
    if ausentes:
        linhas.append(
            f"Candidatas AUSENTES neste snapshot ({len(ausentes)}): {ausentes}"
            "  <- rode --full para incluí-las"
        )
    if ignoradas:
        linhas.append(
            f"ATENÇÃO — colunas no snapshot e fora do modelo ({len(ignoradas)}): "
            f"{ignoradas}. Confirme que cada uma é descarte intencional."
        )
    return "\n".join(linhas)
