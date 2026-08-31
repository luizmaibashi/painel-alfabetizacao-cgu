# EDA — territorio_local (n=10.704)
**Origem:** `data/territorio_local.parquet`
**Gerado por:** `src/preprocessing/01_eda_alunos.py`

## Colunas e tipos

|                                  | tipo    |
|:---------------------------------|:--------|
| ano                              | int64   |
| id_municipio                     | str     |
| rede                             | str     |
| meta_alfabetizacao_2024          | float64 |
| populacao_total                  | float64 |
| sigla_uf                         | str     |
| meta_alfabetizacao_2024_imputada | float64 |
| _origem                          | str     |

## Checklist CRISP-DM (`.claude/rules/dados.md`)

### 1. Duplicatas

- Linha inteira: **0**

### 2. Colunas constantes / quase-constantes

- `rede`: **100.0%** concentrado em `'Municipal'` — sem variância útil.
- `_origem`: **100.0%** concentrado em `'local_reduzido: IBGE SIDRA + metas do disco + UF por prefixo. SEM gasto_por_habitante_educacao (SICONFI nao buscado). Meta imputada por mediana de UF, NAO pelo KNN da Fase 2.'` — sem variância útil.

### 3. Valores sentinela em numéricas

- Nenhum valor sentinela clássico com frequência relevante.

Faixas das numéricas:

|                                  |     min |       50% |            max |
|:---------------------------------|--------:|----------:|---------------:|
| ano                              | 2023    |  2023.5   | 2024           |
| meta_alfabetizacao_2024          |    7.94 |    64.095 |   80           |
| populacao_total                  |  771    | 11965.5   |    1.23964e+07 |
| meta_alfabetizacao_2024_imputada |    7.94 |    64.095 |   80           |

### 4. Códigos de ausência mascarados em categóricas

- Nenhum código de ausência mascarado encontrado.

### 5. Outliers implausíveis (critério relacional)

| coluna                           |   mediana |    p99 |          max |   max/p99 |
|:---------------------------------|----------:|-------:|-------------:|----------:|
| meta_alfabetizacao_2024          |    64.095 |     80 | 80           |     1     |
| populacao_total                  | 11965.5   | 426711 |  1.23964e+07 |    29.051 |
| meta_alfabetizacao_2024_imputada |    64.095 |     80 | 80           |     1     |

Razão `max/p99` alta indica cauda desproporcional — não é prova de erro, é candidato a checar contra a metodologia da fonte antes de usar sem tratamento.

### 6. Perfil de nulos por coluna

|                         |   nulos |    % |
|:------------------------|--------:|-----:|
| meta_alfabetizacao_2024 |     240 | 2.24 |

### 7. Redundância entre colunas

- `meta_alfabetizacao_2024` ↔ `meta_alfabetizacao_2024_imputada`: correlação 1.000

### 8. Relação de cada coluna com o alvo

- Coluna `alfabetizado` ausente neste dataset.

### 9. A NULIDADE de cada coluna prediz o alvo? (item novo — não estava no checklist)

Item acrescentado em 2026-08-18. O item 6 conta nulos mas nunca os cruza com o alvo — e foi por essa fresta que `peso_aluno` passou: 835 nulos que eram os alunos ausentes, todos com alvo "Não". Ver Cap. 9 do diário de bordo interno (não publicado).

- Sem alvo neste dataset, item não aplicável.

## Contexto estrutural (não é gate, mas decide o que é possível)

- **municípios**: 5.352 · 2.00 alunos por município · 0.0% com 1 aluno só
- **anos**: [2023, 2024]
