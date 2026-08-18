# EDA — snapshot_modelagem (n=48.055)
**Origem:** `C:/Users/Luiz Maibashi/Base_de_Conhecimento/PROJETOS/01_PRIORITY/tech-challenge-fase3-alfabetizacao/data/snapshot_modelagem.parquet`
**Gerado por:** `src/preprocessing/01_eda_alunos.py`
**Alvo:** `alfabetizado` · classe de risco `"Não"` = 41.2% das linhas

## Colunas e tipos

|                               | tipo    |
|:------------------------------|:--------|
| ano                           | int64   |
| id_municipio                  | str     |
| id_municipio_nome             | str     |
| id_escola                     | int64   |
| id_aluno                      | int64   |
| caderno                       | int64   |
| rede                          | str     |
| alfabetizado                  | str     |
| _ausente_no_exame             | int64   |
| _peso_amostral                | float64 |
| absenteismo_hist_escola_t1    | float64 |
| n_alunos_hist_escola_t1       | float64 |
| possui_hist_escola_t1         | int64   |
| absenteismo_hist_municipio_t1 | float64 |
| n_alunos_hist_municipio_t1    | float64 |
| possui_hist_municipio_t1      | int64   |

## Checklist CRISP-DM (`.claude/rules/dados.md`)

### 1. Duplicatas

- Linha inteira: **0**
- `id_aluno` sozinho: **235** — mas `id_aluno`+`ano`: **0**. O aluno reaparece em ano diferente; a chave real inclui `ano`.

### 2. Colunas constantes / quase-constantes

- `_ausente_no_exame`: **100.0%** concentrado em `np.int64(0)` — sem variância útil.
- `absenteismo_hist_escola_t1`: **96.1%** concentrado em `np.float64(0.0)` — sem variância útil.

### 3. Valores sentinela em numéricas

- Nenhum valor sentinela clássico com frequência relevante.

Faixas das numéricas:

|                               |        min |            50% |            max |
|:------------------------------|-----------:|---------------:|---------------:|
| ano                           | 2023       | 2024           | 2024           |
| id_escola                     |    6e+07   |    6.00219e+07 |    6.00428e+07 |
| id_aluno                      |    1.1e+07 |    3.11812e+07 |    5.30276e+07 |
| caderno                       |    1       |   10           |   12           |
| _ausente_no_exame             |    0       |    0           |    0           |
| _peso_amostral                |    0.1548  |    1.09        |   23.268       |
| absenteismo_hist_escola_t1    |    0       |    0           |    1           |
| n_alunos_hist_escola_t1       |    1       |    2           |   12           |
| possui_hist_escola_t1         |    0       |    0           |    1           |
| absenteismo_hist_municipio_t1 |    0       |    0.1579      |    1           |
| n_alunos_hist_municipio_t1    |    1       |   19           |  801           |
| possui_hist_municipio_t1      |    0       |    0           |    1           |

### 4. Códigos de ausência mascarados em categóricas

- Nenhum código de ausência mascarado encontrado.

### 5. Outliers implausíveis (critério relacional)

| coluna                        |      mediana |           p99 |           max |   max/p99 |
|:------------------------------|-------------:|--------------:|--------------:|----------:|
| id_escola                     |  6.00219e+07 |   6.00424e+07 |   6.00428e+07 |    1      |
| id_aluno                      |  3.11812e+07 |   5.20734e+07 |   5.30276e+07 |    1.0183 |
| caderno                       | 10           |  12           |  12           |    1      |
| _peso_amostral                |  1.09        |   1.9938      |  23.268       |   11.67   |
| absenteismo_hist_escola_t1    |  0           |   0.6667      |   1           |    1.5    |
| n_alunos_hist_escola_t1       |  2           |   9           |  12           |    1.3333 |
| absenteismo_hist_municipio_t1 |  0.1579      |   0.5         |   1           |    2      |
| n_alunos_hist_municipio_t1    | 19           | 801           | 801           |    1      |

Razão `max/p99` alta indica cauda desproporcional — não é prova de erro, é candidato a checar contra a metodologia da fonte antes de usar sem tratamento.

### 6. Perfil de nulos por coluna

|                            |   nulos |     % |
|:---------------------------|--------:|------:|
| n_alunos_hist_escola_t1    |   42725 | 88.91 |
| n_alunos_hist_municipio_t1 |   30531 | 63.53 |
| _peso_amostral             |      29 |  0.06 |

### 7. Redundância entre colunas

- `id_escola` ↔ `id_aluno`: correlação 0.979

### 8. Relação de cada coluna com o alvo


**`ano`**

|   ano |     n |   % risco |
|------:|------:|----------:|
|  2023 | 23550 |      42.1 |
|  2024 | 24505 |      40.4 |

**`id_escola`** — mediana: risco=60020796.5000 · não-risco=60022558.0000

**`id_aluno`** — mediana: risco=31122350.5000 · não-risco=32008459.0000

**`caderno`**

|   caderno |     n |   % risco |
|----------:|------:|----------:|
|         1 | 19254 |      41.4 |
|        10 | 14168 |      40.9 |
|        11 | 14115 |      41.4 |
|        12 |   518 |      37.3 |

**`rede`**

| rede      |     n |   % risco |
|:----------|------:|----------:|
| Estadual  |  5272 |      38.3 |
| Municipal | 42783 |      41.6 |

**`_ausente_no_exame`**

|   _ausente_no_exame |     n |   % risco |
|--------------------:|------:|----------:|
|                   0 | 48055 |      41.2 |

**`_peso_amostral`** — mediana: risco=1.1034 · não-risco=1.0800

**`absenteismo_hist_escola_t1`** — mediana: risco=0.0000 · não-risco=0.0000

**`possui_hist_escola_t1`**

|   possui_hist_escola_t1 |     n |   % risco |
|------------------------:|------:|----------:|
|                       0 | 42725 |      41.4 |
|                       1 |  5330 |      40   |

**`absenteismo_hist_municipio_t1`** — mediana: risco=0.1579 · não-risco=0.1579

**`n_alunos_hist_municipio_t1`** — mediana: risco=23.0000 · não-risco=18.0000

**`possui_hist_municipio_t1`**

|   possui_hist_municipio_t1 |     n |   % risco |
|---------------------------:|------:|----------:|
|                          0 | 30531 |      41.9 |
|                          1 | 17524 |      40   |

### 9. A NULIDADE de cada coluna prediz o alvo? (item novo — não estava no checklist)

Item acrescentado em 2026-08-18. O item 6 conta nulos mas nunca os cruza com o alvo — e foi por essa fresta que `peso_aluno` passou: 835 nulos que eram os alunos ausentes, todos com alvo "Não". Ver Cap. 9 do `docs/HANDOFF_RENAN.md`.

- `n_alunos_hist_escola_t1`: 42725 nulos (88.9%) — risco entre nulos **41.4%** vs **40.0%** no resto
- `n_alunos_hist_municipio_t1`: 30531 nulos (63.5%) — risco entre nulos **41.9%** vs **40.0%** no resto

## Contexto estrutural (não é gate, mas decide o que é possível)

- **escolas**: 22.259 · 2.16 alunos por escola · 46.9% com 1 aluno só
- **municípios**: 4.478 · 10.73 alunos por município · 18.9% com 1 aluno só
- **anos**: [2023, 2024]
- **escolas em 2023 e 2024**: 3.361 (20.2% das de 2024) — limita qualquer feature histórica por escola
