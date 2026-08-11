"""
Define o pré-processamento como ColumnTransformer, integrado ao modelo via
Pipeline (requisito do enunciado: "integração do pré-processamento
diretamente ao modelo"). Ver ADR-0001 para a política de leakage que decide
quais colunas entram aqui.

Import este módulo em vez de duplicar a lógica — evita divergência entre
o que foi usado no treino e o que seria usado em produção (training-serving
skew, ver .claude/rules/dados.md).
"""
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, RobustScaler

# Colunas fora do modelo, sempre (ADR-0001): proficiencia, presenca,
# preenchimento_caderno já nem existem no snapshot (removidas na extração).
# Identificadores não são feature (mas seguem no dataframe para split/auditoria).
COLUNAS_ID = ["ano", "id_municipio", "id_municipio_nome", "id_escola", "id_aluno"]
COLUNA_TARGET = "alfabetizado"

# Numéricas: peso_aluno tem outliers plausíveis (peso amostral de
# pós-estratificação, EDA item 5) -> Robust Scaling, não Standardization
# (aula 6: mediana/IQR, não sensível a outlier).
COLUNAS_NUMERICAS = ["peso_aluno", "absenteismo_historico_t1"]

# Categóricas de baixa cardinalidade (caderno: 4 valores, rede: 2-4 valores
# na base completa) -> One-Hot, seguro (aula 6).
COLUNAS_CATEGORICAS = ["caderno", "rede"]

# Binária já numérica (0/1), não precisa de transformação -> passthrough.
COLUNAS_PASSTHROUGH = ["possui_historico_t1"]


def construir_preprocessador() -> ColumnTransformer:
    pipeline_numerica = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", RobustScaler()),
    ])
    pipeline_categorica = Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("onehot", OneHotEncoder(handle_unknown="ignore")),
    ])

    return ColumnTransformer([
        ("num", pipeline_numerica, COLUNAS_NUMERICAS),
        ("cat", pipeline_categorica, COLUNAS_CATEGORICAS),
        ("bin", "passthrough", COLUNAS_PASSTHROUGH),
    ])


def colunas_feature() -> list[str]:
    """Todas as colunas de entrada do preprocessador, na ordem que ele espera."""
    return COLUNAS_NUMERICAS + COLUNAS_CATEGORICAS + COLUNAS_PASSTHROUGH
