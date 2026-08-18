# EDA — Alunos.csv (amostra, n=5000)

Gerado a partir de `data/Alunos_amostra.csv` (cópia de `dados_sample/Alunos.csv` da Fase 2, regra AI Jail).

## Colunas e tipos

|                       | 0       |
|:----------------------|:--------|
| ano                   | int64   |
| id_municipio          | int64   |
| id_municipio_nome     | object  |
| id_escola             | int64   |
| id_aluno              | int64   |
| caderno               | int64   |
| serie                 | object  |
| rede                  | object  |
| presenca              | object  |
| preenchimento_caderno | object  |
| alfabetizado          | object  |
| proficiencia          | float64 |
| peso_aluno            | float64 |

## Checklist obrigatório CRISP-DM (.claude/rules/dados.md)

### 1. Duplicatas

- Linha inteira: 0

- `id_aluno` (sozinho): 1 — investigado: reaparece em ano diferente (0 duplicatas em `id_aluno`+`ano`), não é erro de chave, é o mesmo aluno em dois anos letivos.

### 2. Colunas constantes/quase-constantes

- `serie`: 100.0% concentrado em `'2° ano do Ensino Fundamental'` — sem variância, não serve como feature preditiva.

### 3. Valores sentinela em numéricas

- `proficiencia`: min=588.7892388, max=903.60064 — sem valor implausível óbvio (ex.: 9999, -1).

- `peso_aluno`: min=0.1548171, max=12.0113505 — sem valor implausível óbvio (ex.: 9999, -1).

- `caderno`: min=1, max=12 — sem valor implausível óbvio (ex.: 9999, -1).

### 4. Códigos de ausência mascarados em categóricas

- Nenhum código de ausência mascarada encontrado nas categóricas checadas.

### 5. Outliers implausíveis (critério relacional)

- `peso_aluno`: mediana=1.09, 7/4165 alunos com peso > 3× a mediana (0.17%) — plausível para peso amostral de pós-estratificação em estratos pequenos, não tratado como erro (regra: erro implausível vira nulo, não teto — aqui não há evidência de erro, só variância normal do desenho amostral).

### 6. Perfil de nulos por coluna (%)

|                       |    0 |
|:----------------------|-----:|
| proficiencia          | 16.7 |
| peso_aluno            | 16.7 |
| id_municipio_nome     |  0   |
| id_municipio          |  0   |
| ano                   |  0   |
| id_aluno              |  0   |
| id_escola             |  0   |
| caderno               |  0   |
| serie                 |  0   |
| presenca              |  0   |
| rede                  |  0   |
| alfabetizado          |  0   |
| preenchimento_caderno |  0   |

### 7. Redundância entre colunas

- `id_municipio` ↔ `id_municipio_nome`: mapeamento 1:1 (confirmado), esperado, sem ação necessária.

- `presenca` ↔ `preenchimento_caderno`: **redundância real encontrada** (ver Seção 8 abaixo) — mesmo evento, motivou exclusão de `preenchimento_caderno` da política de leakage (ADR-0001).

### 8. Relação de cada bloco com o alvo `alfabetizado`

#### `presenca` × `alfabetizado`

| presenca   |   Não |   Sim |
|:-----------|------:|------:|
| Ausente    |   834 |     0 |
| Presente   |  1708 |  2458 |


**100.0% dos alunos 'Ausente' têm `alfabetizado = Não`** — confirma leakage direto (ADR-0001).

#### `preenchimento_caderno` × `alfabetizado`

| preenchimento_caderno   |   Não |   Sim |
|:------------------------|------:|------:|
| Prova não preenchida    |   100 |     0 |
| Prova preenchida        |    41 |    59 |

834 dos 835 casos de `preenchimento_caderno='Prova não preenchida'` são exatamente os mesmos alunos de `presenca='Ausente'` — confirma a redundância do item 7, motivou excluir `preenchimento_caderno` também (ADR-0001).

#### `proficiencia` × `alfabetizado` (sanity check do corte 743 pts)

| alfabetizado   |   count |    mean |     std |     min |     25% |     50% |     75% |     max |
|:---------------|--------:|--------:|--------:|--------:|--------:|--------:|--------:|--------:|
| Não            |    1707 | 704.463 | 30.7459 | 588.789 | 683.454 | 712.354 | 731.005 | 742.97  |
| Sim            |    2458 | 779.949 | 27.5025 | 743.023 | 758.582 | 774.33  | 795.048 | 903.601 |

Máximo de quem é 'Não' (742,97) < mínimo de quem é 'Sim' (743,02) — corte perfeitamente determinístico, confirma exclusão obrigatória de `proficiencia` como feature.

#### `caderno` × `alfabetizado` — cardinalidade e achado novo

- Valores distintos: 4 (baixa cardinalidade, seguro para one-hot — resolve o blind spot levantado no Grill with Docs).

|   caderno |   Não |   Sim |
|----------:|------:|------:|
|         1 |  50.5 |  49.5 |
|        10 |  47.4 |  52.6 |
|        11 |  48.7 |  51.3 |
|        12 |  86.9 |  13.1 |

**Achado a investigar**: `caderno=12` (236 alunos, ver contagem abaixo) tem 86,9% de `Não`, bem acima dos ~50% dos outros cadernos. Se caderno é só versão anti-cola (aleatória), essa discrepância não deveria existir — hipótese a checar antes de treinar: caderno 12 pode ser versão adaptada/especial (ex.: acessibilidade), o que mudaria sua leitura de 'metadado neutro' para 'proxy de necessidade especial', não necessariamente leakage, mas precisa de decisão explícita, não assumida. Ver `## Conexão com objetivo de negócio` no dicionário.

|   caderno |   count |
|----------:|--------:|
|         1 |    1925 |
|        11 |    1436 |
|        10 |    1403 |
|        12 |     236 |

#### `peso_aluno` × `alfabetizado`

| alfabetizado   |   peso_aluno |
|:---------------|-------------:|
| Não            |      1.16728 |
| Sim            |      1.13157 |

~~Sem diferença relevante entre classes — peso amostral não carrega sinal do target, comportamento esperado (é peso de desenho amostral, não de desempenho).~~

> ⚠️ **CORREÇÃO (2026-08-18) — esta conclusão estava errada.** O SHAP mostrou que
> `peso_aluno` concentra **70,6% da influência** do modelo, e a ablação confirmou:
> sem ele o ROC-AUC cai de 0,669 para 0,530 (≈ aleatório).
>
> **Por que o erro aconteceu:** comparar médias entre classes só detecta relação
> **linear**. Duas distribuições podem ter médias quase idênticas (1,167 vs 1,132)
> e ainda assim diferir muito em faixas específicas — que é exatamente o que um
> modelo de árvore explora, porque ele corta o espaço em faixas em vez de traçar
> uma reta. **Teste de média não é teste de poder preditivo.**
>
> **O que o dado é de fato:** `peso_aluno` é ~constante por escola (0,89 valores
> distintos por escola), ou seja, funciona como identificador da escola, não como
> atributo do aluno. Ver Cap. 9.3 do `docs/HANDOFF_RENAN.md`.

## Cobertura temporal, rede e município (contexto, não gate)

### ano
|   ano |   count |
|------:|--------:|
|  2023 |    2480 |
|  2024 |    2520 |

### rede
| rede      |   count |
|:----------|--------:|
| Municipal |    4486 |
| Estadual  |     514 |

### municípios distintos
- 1905 municípios distintos na amostra
