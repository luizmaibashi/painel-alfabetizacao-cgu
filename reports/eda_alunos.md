# EDA — alunos (n=57.782)
**Origem:** `C:/Users/Luiz Maibashi/Base_de_Conhecimento/PROJETOS/01_PRIORITY/tech-challenge-fase2-alfabetizacao/dados/Alunos.csv`
**Gerado por:** `src/preprocessing/01_eda_alunos.py`
**Alvo:** `alfabetizado` · classe de risco `"Não"` = 51.1% das linhas

## Colunas e tipos

|                       | tipo    |
|:----------------------|:--------|
| ano                   | int64   |
| id_municipio          | int64   |
| id_municipio_nome     | str     |
| id_escola             | int64   |
| id_aluno              | int64   |
| caderno               | int64   |
| serie                 | str     |
| rede                  | str     |
| presenca              | str     |
| preenchimento_caderno | str     |
| alfabetizado          | str     |
| proficiencia          | float64 |
| peso_aluno            | float64 |

## Checklist CRISP-DM (`.claude/rules/dados.md`)

### 1. Duplicatas

- Linha inteira: **0**
- `id_aluno` sozinho: **333** — mas `id_aluno`+`ano`: **0**. O aluno reaparece em ano diferente; a chave real inclui `ano`.

### 2. Colunas constantes / quase-constantes

- `serie`: **100.0%** concentrado em `'2° ano do Ensino Fundamental'` — sem variância útil.

### 3. Valores sentinela em numéricas

- Nenhum valor sentinela clássico com frequência relevante.

Faixas das numéricas:

|              |            min |            50% |            max |
|:-------------|---------------:|---------------:|---------------:|
| ano          | 2023           | 2024           | 2024           |
| id_municipio |    1.10002e+06 |    3.1704e+06  |    5.30011e+06 |
| id_escola    |    6e+07       |    6.00223e+07 |    6.00428e+07 |
| id_aluno     |    1.1e+07     |    3.1201e+07  |    5.30276e+07 |
| caderno      |    1           |   10           |   12           |
| proficiencia |  580.56        |  752.7         |  903.601       |
| peso_aluno   |    0.1548      |    1.09        |   23.268       |

### 4. Códigos de ausência mascarados em categóricas

- Nenhum código de ausência mascarado encontrado.

### 5. Outliers implausíveis (critério relacional)

| coluna       |       mediana |           p99 |           max |   max/p99 |
|:-------------|--------------:|--------------:|--------------:|----------:|
| id_municipio |   3.1704e+06  |   5.22045e+06 |   5.30011e+06 |    1.0153 |
| id_escola    |   6.00223e+07 |   6.00424e+07 |   6.00428e+07 |    1      |
| id_aluno     |   3.1201e+07  |   5.20746e+07 |   5.30276e+07 |    1.0183 |
| caderno      |  10           |  12           |  12           |    1      |
| proficiencia | 752.7         | 851.597       | 903.601       |    1.0611 |
| peso_aluno   |   1.09        |   1.9938      |  23.268       |   11.67   |

Razão `max/p99` alta indica cauda desproporcional — não é prova de erro, é candidato a checar contra a metodologia da fonte antes de usar sem tratamento.

### 6. Perfil de nulos por coluna

|              |   nulos |     % |
|:-------------|--------:|------:|
| proficiencia |    9756 | 16.88 |
| peso_aluno   |    9756 | 16.88 |

### 7. Redundância entre colunas

- `id_municipio` ↔ `id_escola`: correlação 0.980
- `id_municipio` ↔ `id_aluno`: correlação 1.000
- `id_escola` ↔ `id_aluno`: correlação 0.980

### 8. Relação de cada coluna com o alvo


**`ano`**

|   ano |     n |   % risco |
|------:|------:|----------:|
|  2023 | 28295 |      51.8 |
|  2024 | 29487 |      50.5 |

**`id_municipio`** — mediana: risco=3168705.0000 · não-risco=3201209.0000

**`id_escola`** — mediana: risco=60021974.0000 · não-risco=60022558.0000

**`id_aluno`** — mediana: risco=31187434.0000 · não-risco=32008459.0000

**`caderno`**

|   caderno |     n |   % risco |
|----------:|------:|----------:|
|         1 | 22831 |      50.6 |
|        10 | 16246 |      48.4 |
|        11 | 16154 |      48.8 |
|        12 |  2551 |      87.3 |

**`serie`**

| serie                        |     n |   % risco |
|:-----------------------------|------:|----------:|
| 2° ano do Ensino Fundamental | 57782 |      51.1 |

**`rede`**

| rede      |     n |   % risco |
|:----------|------:|----------:|
| Estadual  |  6327 |      48.6 |
| Municipal | 51455 |      51.4 |

**`presenca`**

| presenca   |     n |   % risco |
|:-----------|------:|----------:|
| Ausente    |  9727 |     100   |
| Presente   | 48055 |      41.2 |

**`preenchimento_caderno`**

| preenchimento_caderno   |     n |   % risco |
|:------------------------|------:|----------:|
| Prova não preenchida    |  9756 |     100   |
| Prova preenchida        | 48026 |      41.2 |

**`proficiencia`** — mediana: risco=709.8800 · não-risco=774.2690

**`peso_aluno`** — mediana: risco=1.1034 · não-risco=1.0800

### 9. A NULIDADE de cada coluna prediz o alvo? (item novo — não estava no checklist)

Item acrescentado em 2026-08-18. O item 6 conta nulos mas nunca os cruza com o alvo — e foi por essa fresta que `peso_aluno` passou: 835 nulos que eram os alunos ausentes, todos com alvo "Não". Ver Cap. 9 do `docs/HANDOFF_RENAN.md`.

- `proficiencia`: 9756 nulos (16.9%) — risco entre nulos **100.0%** vs **41.2%** no resto 🔴 **VAZAMENTO**
- `peso_aluno`: 9756 nulos (16.9%) — risco entre nulos **100.0%** vs **41.2%** no resto 🔴 **VAZAMENTO**

## Contexto estrutural (não é gate, mas decide o que é possível)

- **escolas**: 24.346 · 2.37 alunos por escola · 42.8% com 1 aluno só
- **municípios**: 4.591 · 12.59 alunos por município · 16.8% com 1 aluno só
- **anos**: [2023, 2024]
- **escolas em 2023 e 2024**: 4.188 (22.4% das de 2024) — limita qualquer feature histórica por escola
