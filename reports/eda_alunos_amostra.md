# EDA — alunos_amostra (n=5.000)
**Origem:** `data/Alunos_subconjunto_teste_local.csv` (renomeado 2026-08-30,
path no momento em que este relatório rodou era `data/Alunos_amostra.csv`)
**Gerado por:** `src/preprocessing/01_eda_alunos.py`
**Alvo:** `alfabetizado` · classe de risco `"Não"` = 50.8% das linhas

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
- `id_aluno` sozinho: **1** — mas `id_aluno`+`ano`: **0**. O aluno reaparece em ano diferente; a chave real inclui `ano`.

### 2. Colunas constantes / quase-constantes

- `serie`: **100.0%** concentrado em `'2° ano do Ensino Fundamental'` — sem variância útil.

### 3. Valores sentinela em numéricas

- Nenhum valor sentinela clássico com frequência relevante.

Faixas das numéricas:

|              |            min |            50% |            max |
|:-------------|---------------:|---------------:|---------------:|
| ano          | 2023           | 2024           | 2024           |
| id_municipio |    1.10002e+06 |    3.17125e+06 |    5.30011e+06 |
| id_escola    |    6e+07       |    6.00224e+07 |    6.00428e+07 |
| id_aluno     |    1.10007e+07 |    3.12074e+07 |    5.30274e+07 |
| caderno      |    1           |   10           |   12           |
| proficiencia |  588.789       |  752.55        |  903.601       |
| peso_aluno   |    0.1548      |    1.09        |   12.0114      |

### 4. Códigos de ausência mascarados em categóricas

- Nenhum código de ausência mascarado encontrado.

### 5. Outliers implausíveis (critério relacional)

| coluna       |       mediana |           p99 |           max |   max/p99 |
|:-------------|--------------:|--------------:|--------------:|----------:|
| id_municipio |   3.17125e+06 |   5.22045e+06 |   5.30011e+06 |    1.0153 |
| id_escola    |   6.00224e+07 |   6.00424e+07 |   6.00428e+07 |    1      |
| id_aluno     |   3.12074e+07 |   5.20769e+07 |   5.30274e+07 |    1.0183 |
| caderno      |  10           |  12           |  12           |    1      |
| proficiencia | 752.55        | 852.965       | 903.601       |    1.0594 |
| peso_aluno   |   1.09        |   2           |  12.0114      |    6.0057 |

Razão `max/p99` alta indica cauda desproporcional — não é prova de erro, é candidato a checar contra a metodologia da fonte antes de usar sem tratamento.

### 6. Perfil de nulos por coluna

|              |   nulos |    % |
|:-------------|--------:|-----:|
| proficiencia |     835 | 16.7 |
| peso_aluno   |     835 | 16.7 |

### 7. Redundância entre colunas

- `id_municipio` ↔ `id_escola`: correlação 0.980
- `id_municipio` ↔ `id_aluno`: correlação 1.000
- `id_escola` ↔ `id_aluno`: correlação 0.980

### 8. Relação de cada coluna com o alvo


**`ano`**

|   ano |    n |   % risco |
|------:|-----:|----------:|
|  2023 | 2480 |      51.5 |
|  2024 | 2520 |      50.2 |

**`id_municipio`** — mediana: risco=3167504.0000 · não-risco=3201308.0000

**`id_escola`** — mediana: risco=60021846.5000 · não-risco=60022704.0000

**`id_aluno`** — mediana: risco=31187439.5000 · não-risco=32022877.0000

**`caderno`**

|   caderno |    n |   % risco |
|----------:|-----:|----------:|
|         1 | 1925 |      50.5 |
|        10 | 1403 |      47.4 |
|        11 | 1436 |      48.7 |
|        12 |  236 |      86.9 |

**`serie`**

| serie                        |    n |   % risco |
|:-----------------------------|-----:|----------:|
| 2° ano do Ensino Fundamental | 5000 |      50.8 |

**`rede`**

| rede      |    n |   % risco |
|:----------|-----:|----------:|
| Estadual  |  514 |      47.7 |
| Municipal | 4486 |      51.2 |

**`presenca`**

| presenca   |    n |   % risco |
|:-----------|-----:|----------:|
| Ausente    |  834 |       100 |
| Presente   | 4166 |        41 |

**`preenchimento_caderno`**

| preenchimento_caderno   |    n |   % risco |
|:------------------------|-----:|----------:|
| Prova não preenchida    |  835 |       100 |
| Prova preenchida        | 4165 |        41 |

**`proficiencia`** — mediana: risco=712.3543 · não-risco=774.3300

**`peso_aluno`** — mediana: risco=1.1000 · não-risco=1.0834

### 9. A NULIDADE de cada coluna prediz o alvo? (item novo — não estava no checklist)

Item acrescentado em 2026-08-18. O item 6 conta nulos mas nunca os cruza com o alvo — e foi por essa fresta que `peso_aluno` passou: 835 nulos que eram os alunos ausentes, todos com alvo "Não". Ver Cap. 9 do `docs/HANDOFF_RENAN.md`.

- `proficiencia`: 835 nulos (16.7%) — risco entre nulos **100.0%** vs **41.0%** no resto 🔴 **VAZAMENTO**
- `peso_aluno`: 835 nulos (16.7%) — risco entre nulos **100.0%** vs **41.0%** no resto 🔴 **VAZAMENTO**

## Contexto estrutural (não é gate, mas decide o que é possível)

- **escolas**: 4.475 · 1.12 alunos por escola · 89.4% com 1 aluno só
- **municípios**: 1.905 · 2.62 alunos por município · 57.0% com 1 aluno só
- **anos**: [2023, 2024]
- **escolas em 2023 e 2024**: 98 (4.1% das de 2024) — limita qualquer feature histórica por escola
