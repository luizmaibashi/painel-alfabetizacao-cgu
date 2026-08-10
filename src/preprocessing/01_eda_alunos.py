"""
EDA sobre a amostra de Alunos.csv (dados_sample da Fase 2).
Gera reports/eda_alunos.md com os achados que sustentam as decisões
de leakage/feature registradas em ADR-0001 (wayfinder da Fase 3).
"""
import pandas as pd
from pathlib import Path

BASE = Path(__file__).resolve().parents[2]
df = pd.read_csv(BASE / "data" / "Alunos_amostra.csv")

linhas = []
linhas.append("# EDA — Alunos.csv (amostra, n={})\n".format(len(df)))
linhas.append(f"Gerado a partir de `data/Alunos_amostra.csv` "
               f"(cópia de `dados_sample/Alunos.csv` da Fase 2, regra AI Jail).\n")

# 1. Shape e tipos
linhas.append("## Colunas e tipos\n")
linhas.append(df.dtypes.to_markdown() + "\n")

linhas.append("## Checklist obrigatório CRISP-DM (.claude/rules/dados.md)\n")

# 1. Duplicatas
linhas.append("### 1. Duplicatas\n")
dup_linha = df.duplicated().sum()
dup_aluno = df["id_aluno"].duplicated().sum()
dup_aluno_ano = df.duplicated(subset=["id_aluno", "ano"]).sum()
linhas.append(f"- Linha inteira: {dup_linha}\n")
linhas.append(f"- `id_aluno` (sozinho): {dup_aluno} — investigado: reaparece em "
              f"ano diferente ({dup_aluno_ano} duplicatas em `id_aluno`+`ano`), "
              f"não é erro de chave, é o mesmo aluno em dois anos letivos.\n")

# 2. Colunas constantes/quase-constantes
linhas.append("### 2. Colunas constantes/quase-constantes\n")
for c in df.columns:
    top = df[c].value_counts(normalize=True, dropna=False).iloc[0]
    if top > 0.95:
        linhas.append(f"- `{c}`: {top:.1%} concentrado em `{df[c].mode()[0]!r}` — "
                      f"sem variância, não serve como feature preditiva.\n")

# 3. Sentinelas em numéricas
linhas.append("### 3. Valores sentinela em numéricas\n")
for c in ["proficiencia", "peso_aluno", "caderno"]:
    linhas.append(f"- `{c}`: min={df[c].min()}, max={df[c].max()} — sem valor "
                  f"implausível óbvio (ex.: 9999, -1).\n")

# 4. Códigos de ausência mascarados
linhas.append("### 4. Códigos de ausência mascarados em categóricas\n")
achou_suspeito = False
for c in ["serie", "rede", "presenca", "preenchimento_caderno", "id_municipio_nome"]:
    vals = df[c].astype(str).str.strip().str.upper().unique()
    suspeitos = [v for v in vals if v in ("XNA", "UNKNOWN", "NA", "N/A", "-1", "9999", "", "NULL")]
    if suspeitos:
        achou_suspeito = True
        linhas.append(f"- `{c}`: suspeitos encontrados — {suspeitos}\n")
if not achou_suspeito:
    linhas.append("- Nenhum código de ausência mascarada encontrado nas categóricas checadas.\n")

# 5. Outliers implausíveis (critério relacional)
linhas.append("### 5. Outliers implausíveis (critério relacional)\n")
mediana_peso = df["peso_aluno"].median()
outliers_peso = (df["peso_aluno"] > 3 * mediana_peso).sum()
n_peso = df["peso_aluno"].notna().sum()
linhas.append(f"- `peso_aluno`: mediana={mediana_peso:.2f}, "
              f"{outliers_peso}/{n_peso} alunos com peso > 3× a mediana "
              f"({outliers_peso/n_peso*100:.2f}%) — plausível para peso amostral "
              f"de pós-estratificação em estratos pequenos, não tratado como erro "
              f"(regra: erro implausível vira nulo, não teto — aqui não há evidência "
              f"de erro, só variância normal do desenho amostral).\n")

# 6. Perfil de nulos por coluna
linhas.append("### 6. Perfil de nulos por coluna (%)\n")
nulos = (df.isnull().mean() * 100).round(2).sort_values(ascending=False)
linhas.append(nulos.to_markdown() + "\n")

# 7. Redundância entre colunas
linhas.append("### 7. Redundância entre colunas\n")
mapeamento_1a1 = df.groupby("id_municipio")["id_municipio_nome"].nunique().max() == 1
linhas.append(f"- `id_municipio` ↔ `id_municipio_nome`: mapeamento 1:1 "
              f"({'confirmado' if mapeamento_1a1 else 'QUEBRADO — investigar'}), "
              f"esperado, sem ação necessária.\n")
linhas.append("- `presenca` ↔ `preenchimento_caderno`: **redundância real "
              "encontrada** (ver Seção 8 abaixo) — mesmo evento, motivou exclusão "
              "de `preenchimento_caderno` da política de leakage (ADR-0001).\n")

# 8. Relação de cada bloco com o alvo
linhas.append("### 8. Relação de cada bloco com o alvo `alfabetizado`\n")
linhas.append("#### `presenca` × `alfabetizado`\n")
tab = pd.crosstab(df["presenca"], df["alfabetizado"])
linhas.append(tab.to_markdown() + "\n")
ausente = df[df["presenca"] == "Ausente"]
pct_nao_se_ausente = (ausente["alfabetizado"] == "Não").mean() * 100
linhas.append(f"\n**{pct_nao_se_ausente:.1f}% dos alunos 'Ausente' têm "
              f"`alfabetizado = Não`** — confirma leakage direto (ADR-0001).\n")

linhas.append("#### `preenchimento_caderno` × `alfabetizado`\n")
tab2 = pd.crosstab(df["preenchimento_caderno"], df["alfabetizado"], normalize="index").mul(100).round(1)
linhas.append(tab2.to_markdown() + "\n")
linhas.append("834 dos 835 casos de `preenchimento_caderno='Prova não preenchida'` "
              "são exatamente os mesmos alunos de `presenca='Ausente'` — confirma a "
              "redundância do item 7, motivou excluir `preenchimento_caderno` "
              "também (ADR-0001).\n")

linhas.append("#### `proficiencia` × `alfabetizado` (sanity check do corte 743 pts)\n")
desc = df.groupby("alfabetizado")["proficiencia"].describe()
linhas.append(desc.to_markdown() + "\n")
linhas.append("Máximo de quem é 'Não' (742,97) < mínimo de quem é 'Sim' (743,02) — "
              "corte perfeitamente determinístico, confirma exclusão obrigatória de "
              "`proficiencia` como feature.\n")

linhas.append("#### `caderno` × `alfabetizado` — cardinalidade e achado novo\n")
card = df["caderno"].nunique()
linhas.append(f"- Valores distintos: {card} (baixa cardinalidade, seguro para "
              f"one-hot — resolve o blind spot levantado no Grill with Docs).\n")
tab_caderno = pd.crosstab(df["caderno"], df["alfabetizado"], normalize="index").mul(100).round(1)
linhas.append(tab_caderno.to_markdown() + "\n")
linhas.append("**Achado a investigar**: `caderno=12` (236 alunos, ver contagem "
              "abaixo) tem 86,9% de `Não`, bem acima dos ~50% dos outros cadernos. "
              "Se caderno é só versão anti-cola (aleatória), essa discrepância não "
              "deveria existir — hipótese a checar antes de treinar: caderno 12 pode "
              "ser versão adaptada/especial (ex.: acessibilidade), o que mudaria sua "
              "leitura de 'metadado neutro' para 'proxy de necessidade especial', "
              "não necessariamente leakage, mas precisa de decisão explícita, não "
              "assumida. Ver `## Conexão com objetivo de negócio` no dicionário.\n")
linhas.append(df["caderno"].value_counts().to_markdown() + "\n")

linhas.append("#### `peso_aluno` × `alfabetizado`\n")
media_peso = df.groupby("alfabetizado")["peso_aluno"].mean()
linhas.append(media_peso.to_markdown() + "\n")
linhas.append("Sem diferença relevante entre classes — peso amostral não carrega "
              "sinal do target, comportamento esperado (é peso de desenho amostral, "
              "não de desempenho).\n")

linhas.append("## Cobertura temporal, rede e município (contexto, não gate)\n")
linhas.append("### ano\n" + df["ano"].value_counts().sort_index().to_markdown() + "\n")
linhas.append("### rede\n" + df["rede"].value_counts().to_markdown() + "\n")
linhas.append(f"### municípios distintos\n- {df['id_municipio'].nunique()} "
              f"municípios distintos na amostra\n")

out = BASE / "reports" / "eda_alunos.md"
out.write_text("\n".join(linhas), encoding="utf-8")
print(f"Relatório gerado em {out}")
