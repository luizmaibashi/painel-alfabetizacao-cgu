# Auditoria linha a linha do enunciado — Fase 3

> **Pra que serve este documento:** duas das cinco críticas da Fase 2 foram
> literalmente "o enunciado pede X e X não existe" (estimativa de custo da
> arquitetura; 3 dos 4 itens de monitoramento). A defesa contra isso não é
> lembrar melhor — é **cruzar cada linha do PDF contra o que existe, por
> escrito, com evidência de onde está**.
>
> **Renan:** a coluna "Status" é o que importa. 🔴 = não existe, 🟡 = parcial,
> ✅ = feito com evidência apontável. Tudo 🔴/🟡 é trabalho ou decisão pendente.
> As linhas com ❓ precisam da sua opinião.

**Fonte:** `[IAST] - Tech Challenge - Fase 3.pdf` (commitado no repo).
**Auditado em:** 2026-08-18.
**Estado geral:** projeto em fase de modelagem; nada aqui é entrega final.

---

## 1. Pipeline de ML — "Sua pipeline deve conter" (PDF, p. 3)

O enunciado lista 6 itens explícitos. Esta é a lista mais literal do PDF e a
mais fácil de deixar buraco:

| # | Item exigido | Status | Onde está / o que falta |
|---|---|---|---|
| 1 | Imputação de valores faltantes para variáveis numéricas | ✅ | `pipeline_preprocessamento.py` (`SimpleImputer`) + imputação de `absenteismo_historico_t1` por mediana de UF em `02_extrair_snapshot.py`. ADR-0001 §2.3 |
| 2 | Técnicas de transformação de variáveis numéricas e categóricas | ✅ | `ColumnTransformer`: Robust Scaling (numéricas) + One-Hot (categóricas), `pipeline_preprocessamento.py` |
| 3 | Tratamento de data leakage | ✅ | Política fechada e documentada: ADR-0001 §2.2, aplicada em código (`COLUNAS_LEAKAGE` no extrator). 3 colunas excluídas com justificativa empírica |
| 4 | Integração do pré-processamento diretamente ao modelo | ✅ | `Pipeline` do sklearn com pré-processamento + estimador num objeto só |
| 5 | Treinamento e validação do modelo | 🟡 | Baseline RandomForest treinado (`01_treinar_baseline.py`). **Falta o tournament de 3 modelos** (Seção 3 do plano de refinamento) e a escolha final |
| 6 | Validação garantindo replicabilidade e generalização | 🟡 | Validação dupla implementada (split aleatório estratificado + temporal 2023→2024), seeds fixos. **Falta:** cross-validation k-fold explícita — hoje é split único por estratégia. Ver §5.1 |

## 2. Etapas esperadas — Análise Exploratória (PDF, p. 4)

| Item exigido | Status | Onde está / o que falta |
|---|---|---|
| Compreender o comportamento dos dados | ✅ | `reports/eda_alunos.md` — checklist de 8 itens |
| Identificar padrões | ✅ | EDA §8 (relação de cada bloco com o alvo) |
| Avaliar distribuições | ✅ | EDA §3, §5 (sentinelas, outliers relacionais) |
| Detectar correlações | 🟡 | EDA cobre redundância entre colunas (§7) e relação com alvo (§8). **Não há matriz de correlação numérica explícita** — provavelmente vale adicionar, é barato e o enunciado nomeia "correlações" |
| Analisar variáveis relevantes | ✅ | `reports/dicionario_alunos.md` — toda coluna com decisão de uso |
| Formular hipóteses analíticas | ✅ | Hipótese do `caderno=12` (EDA §8) + tese de falsificação do ADR-0001 §5 |
| "A EDA deve apoiar diretamente as decisões de modelagem" | ✅ | Rastro explícito: EDA achou `preenchimento_caderno` redundante → ADR-0001 excluiu; EDA achou `serie` constante → removida do modelo |

## 3. Modelagem supervisionada (PDF, p. 5)

| Item exigido | Status | Onde está / o que falta |
|---|---|---|
| Demonstrar a pipeline completa | ✅ | Código versionado, roda ponta a ponta |
| Feature engineering | ✅ | `absenteismo_historico_t1`, `possui_historico_t1`, `meta_is_imputada` (novo) |
| Feature encoding | ✅ | One-Hot, documentado |
| Tratamento de valores faltantes | ✅ | Ver §1 item 1 |
| Separação adequada treino/validação/teste | 🟡 | Hoje: treino/teste. **O enunciado cita três conjuntos** (treino, validação, teste) — com tuning de hiperparâmetro no tournament, isso vira necessário de fato. Ver §5.1 |
| Estratégias de otimização (reduzir overfitting) | 🔴 | **Não existe ainda.** Baseline usou hiperparâmetros default. Tournament precisa incluir tuning (GridSearch/RandomizedSearch) e regularização — senão este item fica vazio |
| Interpretabilidade: Feature Importance | ✅ | Permutation Importance no baseline, com 3 achados reais |
| Interpretabilidade: SHAP | 🔴 | **Não existe ainda.** Planejado, não implementado. Enunciado recomenda explicitamente |

## 4. Aplicação estratégica — 5 perguntas de negócio (PDF, p. 5)

Cruzado com o que a Fase 2 já entregou em produção (evita reconstruir o que
existe — e evita o erro oposto, de esquecer que existe):

| Pergunta do enunciado | Status | Fonte |
|---|---|---|
| Quais fatores mais impactam a alfabetização? | 🟡 | SHAP do modelo novo (🔴 pendente) + `agg_correlacoes_uf` da Fase 2 (✅ existe). Combinar leitura aluno + município |
| Quais municípios apresentam maior risco educacional? | ✅ | `agg_priorizacao` / `agg_municipio_ranking` (Fase 2, produção) — reaproveitar e citar |
| Quais regiões possuem padrões semelhantes? | ✅ | `agg_vulnerabilidade_ml` (K-Means, Fase 2, produção) — reaproveitar e citar |
| Como prever municípios que podem não atingir metas futuras? | 🔴 | **Não existe.** Decisão registrada no `SPEC_FINAL.md`: fora do escopo (sem componente temporal), vai como "evolução futura" no README. ❓ **Renan: concorda em deixar fora?** É a única das 5 perguntas sem resposta |
| Quais variáveis possuem maior influência nos modelos? | 🔴 | Depende do SHAP (pendente) |

⚠️ **Risco de repetir a Fase 2 aqui:** os marts da Fase 2 respondem 2 das 5
perguntas e estão prontos — mas se o README da Fase 3 não os **citar
explicitamente**, o avaliador lê como "não respondido". Foi exatamente assim
que o streaming da Fase 2 "não alimentou nada": a peça existia, a ligação não
estava visível.

## 5. Lacunas que a auditoria revelou (o valor real deste documento)

### 5.1 Validação: split único ≠ "replicabilidade e generalização" 🟡

O enunciado pede duas coisas nominalmente (item 6 da pipeline) e cita três
conjuntos (treino/validação/teste). Hoje temos split único por estratégia, sem
k-fold e sem conjunto de validação separado. Com tuning de hiperparâmetro
entrando no tournament, usar o teste para escolher hiperparâmetro **vaza o
teste** — problema real, não formalidade.

**Proposta:** k-fold estratificado no treino para tuning, teste tocado uma vez
só no fim. Para o split temporal, manter 2023→2024 como checagem separada.

### 5.2 Otimização/anti-overfitting não existe 🔴

Baseline rodou com defaults. É um item explícito do enunciado e hoje está
vazio. Entra no escopo do tournament (Seção 3 do plano de refinamento).

### 5.3 SHAP não existe 🔴

Recomendado explicitamente pelo enunciado, e é a única fonte para 2 das 5
perguntas de negócio. Também é o mecanismo de checagem do risco do `caderno=12`
e agora do `meta_is_imputada` — sem SHAP, esses riscos ficam sem verificação.

### 5.4 Matriz de correlação ausente na EDA 🟡

Barato de adicionar, nomeado no enunciado.

### 5.5 Metas: corrigido nesta sessão ✅

O enunciado lista "metas nacionais e estaduais" e "metas municipais" entre os
dados da base. Não estavam sendo extraídas. Corrigido em
`02_extrair_snapshot.py` — ver `FEEDBACK_FASE2_E_LICOES.md` §4.1.

## 6. Entregáveis finais (PDF, p. 6-8) — nenhum começou

Todos dependem da modelagem fechar. Registrados aqui para não sumirem:

| Entregável | Status | Nota |
|---|---|---|
| Repositório Git completo | 🟡 | Estrutura existe localmente. **Repo novo em `alfabetizacao-datateam` ainda não criado** (ticket 0004) |
| Git flow: branches, PRs, histórico | 🔴 | Enunciado pede explicitamente **branches e pull requests**. Hoje: commits diretos na base de conhecimento. ❓ **Renan: como fazemos PR cruzada de verdade nesta fase?** |
| README de 11 seções | 🔴 | Estrutura conhecida, conteúdo depende do modelo final |
| Documentação técnica | 🟡 | ADR-0001, ADR-0002, Risk Register, este documento |
| Vídeo executivo (5 min) | 🔴 | Simula reunião com gestores públicos |
| Pipeline reproduzível | 🟡 | Roda em `--local-only`; `--full` nunca foi executado (credencial GCP) |
| Análises e visualizações | 🔴 | Pasta `images/` vazia |

## 7. Resumo pro Renan — o que decidir na call

**Trabalho técnico pendente e claro (não precisa de decisão, só de execução):**
1. Tournament de 3 modelos **com tuning** (resolve §1.5, §3 otimização, §5.2)
2. SHAP (resolve §3, 2 perguntas de negócio, verificação de 2 riscos)
3. K-fold + conjunto de validação separado (§5.1)
4. Matriz de correlação na EDA (§5.4)

**Decisões que preciso de você:**
1. ❓ `meta_alfabetizacao_2024_imputada` como feature **não é leakage** — concorda?
2. ❓ Deixar a pergunta "prever municípios que não atingirão metas futuras" fora
   do escopo (como "evolução futura")?
3. ❓ Como fazer **branches + PRs de verdade**, já que o enunciado cobra isso e
   hoje trabalho sozinho e commito direto?
4. ❓ `caderno=12` — ver `ADR-0002` e `reports/proveniencia_alunos.md`
5. ❓ Os 5 riscos do `RISK_REGISTER.md` (Aceito / Mitigar / Escalar)

**Bloqueio operacional:** `--full` depende da sua credencial GCP. Enquanto não
rodar, todo número aqui é de amostra (5.000 linhas) sem território nem meta.
