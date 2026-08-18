# EDA — snapshot_modelagem (n=57.782)
**Origem:** `C:/Users/Luiz Maibashi/Base_de_Conhecimento/PROJETOS/01_PRIORITY/tech-challenge-fase3-alfabetizacao/data/snapshot_modelagem.parquet`
**Gerado por:** `src/preprocessing/01_eda_alunos.py`
**Alvo:** `alfabetizado` · classe de risco `"Não"` = 51.1% das linhas

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
| peso_aluno                    | float64 |
| _ausente_no_exame             | int64   |
| absenteismo_hist_escola_t1    | float64 |
| n_alunos_hist_escola_t1       | float64 |
| possui_hist_escola_t1         | int64   |
| absenteismo_hist_municipio_t1 | float64 |
| n_alunos_hist_municipio_t1    | float64 |
| possui_hist_municipio_t1      | int64   |

## Checklist CRISP-DM (`.claude/rules/dados.md`)

### 1. Duplicatas

- Linha inteira: **0**
- `id_aluno` sozinho: **333** — mas `id_aluno`+`ano`: **0**. O aluno reaparece em ano diferente; a chave real inclui `ano`.

### 2. Colunas constantes / quase-constantes

- `absenteismo_hist_escola_t1`: **95.9%** concentrado em `np.float64(0.0)` — sem variância útil.

### 3. Valores sentinela em numéricas

- Nenhum valor sentinela clássico com frequência relevante.

Faixas das numéricas:

|                               |        min |            50% |            max |
|:------------------------------|-----------:|---------------:|---------------:|
| ano                           | 2023       | 2024           | 2024           |
| id_escola                     |    6e+07   |    6.00223e+07 |    6.00428e+07 |
| id_aluno                      |    1.1e+07 |    3.1201e+07  |    5.30276e+07 |
| caderno                       |    1       |   10           |   12           |
| peso_aluno                    |    0.1548  |    1.09        |   23.268       |
| _ausente_no_exame             |    0       |    0           |    1           |
| absenteismo_hist_escola_t1    |    0       |    0           |    1           |
| n_alunos_hist_escola_t1       |    1       |    2           |   12           |
| possui_hist_escola_t1         |    0       |    0           |    1           |
| absenteismo_hist_municipio_t1 |    0       |    0.1667      |    1           |
| n_alunos_hist_municipio_t1    |    1       |   21           |  801           |
| possui_hist_municipio_t1      |    0       |    0           |    1           |

### 4. Códigos de ausência mascarados em categóricas

- Nenhum código de ausência mascarado encontrado.

### 5. Outliers implausíveis (critério relacional)

| coluna                        |      mediana |           p99 |           max |   max/p99 |
|:------------------------------|-------------:|--------------:|--------------:|----------:|
| id_escola                     |  6.00223e+07 |   6.00424e+07 |   6.00428e+07 |    1      |
| id_aluno                      |  3.1201e+07  |   5.20746e+07 |   5.30276e+07 |    1.0183 |
| caderno                       | 10           |  12           |  12           |    1      |
| peso_aluno                    |  1.09        |   1.9938      |  23.268       |   11.67   |
| absenteismo_hist_escola_t1    |  0           |   0.8         |   1           |    1.25   |
| n_alunos_hist_escola_t1       |  2           |   9           |  12           |    1.3333 |
| absenteismo_hist_municipio_t1 |  0.1667      |   0.5         |   1           |    2      |
| n_alunos_hist_municipio_t1    | 21           | 801           | 801           |    1      |

Razão `max/p99` alta indica cauda desproporcional — não é prova de erro, é candidato a checar contra a metodologia da fonte antes de usar sem tratamento.

### 6. Perfil de nulos por coluna

|                            |   nulos |     % |
|:---------------------------|--------:|------:|
| n_alunos_hist_escola_t1    |   51258 | 88.71 |
| n_alunos_hist_municipio_t1 |   36442 | 63.07 |
| peso_aluno                 |    9756 | 16.88 |

### 7. Redundância entre colunas

- `id_escola` ↔ `id_aluno`: correlação 0.980

### 8. Relação de cada coluna com o alvo


**`ano`**

|   ano |     n |   % risco |
|------:|------:|----------:|
|  2023 | 28295 |      51.8 |
|  2024 | 29487 |      50.5 |

**`id_escola`** — mediana: risco=60021974.0000 · não-risco=60022558.0000

**`id_aluno`** — mediana: risco=31187434.0000 · não-risco=32008459.0000

**`caderno`**

|   caderno |     n |   % risco |
|----------:|------:|----------:|
|         1 | 22831 |      50.6 |
|        10 | 16246 |      48.4 |
|        11 | 16154 |      48.8 |
|        12 |  2551 |      87.3 |

**`rede`**

| rede      |     n |   % risco |
|:----------|------:|----------:|
| Estadual  |  6327 |      48.6 |
| Municipal | 51455 |      51.4 |

**`peso_aluno`** — mediana: risco=1.1034 · não-risco=1.0800

**`_ausente_no_exame`**

|   _ausente_no_exame |     n |   % risco |
|--------------------:|------:|----------:|
|                   0 | 48055 |      41.2 |
|                   1 |  9727 |     100   |

**`absenteismo_hist_escola_t1`** — mediana: risco=0.0000 · não-risco=0.0000

**`possui_hist_escola_t1`**

|   possui_hist_escola_t1 |     n |   % risco |
|------------------------:|------:|----------:|
|                       0 | 51258 |      51.1 |
|                       1 |  6524 |      51   |

**`absenteismo_hist_municipio_t1`** — mediana: risco=0.1667 · não-risco=0.1667

**`n_alunos_hist_municipio_t1`** — mediana: risco=26.0000 · não-risco=18.0000

**`possui_hist_municipio_t1`**

|   possui_hist_municipio_t1 |     n |   % risco |
|---------------------------:|------:|----------:|
|                          0 | 36442 |      51.3 |
|                          1 | 21340 |      50.7 |

### 9. A NULIDADE de cada coluna prediz o alvo? (item novo — não estava no checklist)

Item acrescentado em 2026-08-18. O item 6 conta nulos mas nunca os cruza com o alvo — e foi por essa fresta que `peso_aluno` passou: 835 nulos que eram os alunos ausentes, todos com alvo "Não". Ver Cap. 9 do `docs/HANDOFF_RENAN.md`.

- `peso_aluno`: 9756 nulos (16.9%) — risco entre nulos **100.0%** vs **41.2%** no resto 🔴 **VAZAMENTO**
- `n_alunos_hist_escola_t1`: 51258 nulos (88.7%) — risco entre nulos **51.1%** vs **51.0%** no resto
- `n_alunos_hist_municipio_t1`: 36442 nulos (63.1%) — risco entre nulos **51.3%** vs **50.7%** no resto

## Contexto estrutural (não é gate, mas decide o que é possível)

- **escolas**: 24.346 · 2.37 alunos por escola · 42.8% com 1 aluno só
- **municípios**: 4.591 · 12.59 alunos por município · 16.8% com 1 aluno só
- **anos**: [2023, 2024]
- **escolas em 2023 e 2024**: 4.188 (22.4% das de 2024) — limita qualquer feature histórica por escola
