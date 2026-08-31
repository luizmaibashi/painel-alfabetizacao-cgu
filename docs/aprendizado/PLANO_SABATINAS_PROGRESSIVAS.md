# Plano de Sabatinas Progressivas — Fase 3

**Objetivo:** Você aprende TUDO da Fase 3 através de uma escada: O quê → Por quê → Como → Exemplos → Sabatina → Integração.

---

## Estrutura das Sabatinas

Cada módulo vai seguir este fluxo:

### 1. **LEITURA** (você lê a trilha)
- Conceitos fundamentais
- Trade-offs explícitos
- Exemplos práticos
- Conexões com o projeto

### 2. **COMPREENSÃO** (você anota)
- Anotações em `NOTAS_APRENDIZADO.md`
- Dúvidas abertas
- Conexões com seu projeto (Tech Challenge Fase 3)

### 3. **SABATINA** (você responde 1-2 perguntas)
- Pergunta 1: Conceitual (O quê? Por quê?)
- Pergunta 2: Prática (Como? Quando usar?)
- Sem aviso prévio, contexto do seu projeto

### 4. **INTEGRAÇÃO** (você implementa)
- Se passou na sabatina
- Adiciona nova técnica ao código
- Atualiza documentação (ADR novo se decisão arquitetural)

---

## Sequência de Módulos (Recomendada)

### **BLOCO 1: Fundações (Sem integração de código — só aprendizado)**

#### Módulo 1.1: Aprendizagem Supervisionada — Fundamentos
**Duração:** 2-3h leitura + 1h sabatina

**O que você vai aprender:**
- Diferença entre regressão e classificação
- Métricas para cada tipo (MSE vs Cross-Entropy, Accuracy vs Recall)
- Validação cruzada e split train/test
- Overfitting vs Underfitting

**Por que importa pro seu projeto:**
- Seu Tech Challenge é **classificação binária** (alfabetizado Sim/Não)
- Recall é a métrica principal (não perder alunos em risco)
- Você já faz validação dupla (aleatória + temporal) — entender **por quê** isso funciona

**Sabatina 1.1a (Conceitual):**
> "Qual é a diferença FUNDAMENTAL entre regressão e classificação? Por que a saída de uma regressão logística é probabilidade, não classificação direto?"

**Sabatina 1.1b (Prática):**
> "No seu projeto, por que Recall é a métrica principal e não Accuracy? Se o modelo tiver Recall 0.34 mas Precision 0.83, o que isso significa em termos de alunos reais?"

---

#### Módulo 1.2: Métricas e Validação
**Duração:** 1-2h leitura + 1h sabatina

**O que você vai aprender:**
- Matriz de confusão, TP/TN/FP/FN
- ROC-AUC, Precision-Recall, F1
- Cross-validation strategies (K-fold, stratified, temporal)

**Por que importa:**
- Seu baseline atual tem Recall 0.34 — sabe o que significa?
- Validação temporal (2023→2024) é CRÍTICA — precisa entender **por quê**

**Sabatina 1.2a:**
> "Sua matriz de confusão tem TP=100, FN=200, FP=20, TN=680. Qual é o Recall? O que aqueles 200 FN significam?"

**Sabatina 1.2b:**
> "Validação temporal 2023→2024 vs aleatória deram Recall diferentes (0.417 vs 0.344). Qual é válido? Por quê?"

---

### **BLOCO 2: Modelos Clássicos (Com integração de código)**

#### Módulo 2.1: Regressão Logística como Baseline
**Duração:** 1-2h leitura + 2-3h código + 1h sabatina

**O que você vai aprender:**
- Regressão Logística vs Random Forest (trade-offs)
- Probabilidade vs decisão binária
- Interpretabilidade (coeficientes importam!)
- Threshold tuning (ajustar cutoff de decisão)

**Por que importa:**
- Regressão Logística é seu **modelo baseline interpretável**
- Você vai comparar: Logística vs RF vs Boosting
- Entender threshold = controlar recall vs precision

**Sabatina 2.1a:**
> "Sua Regressão Logística tem coeficiente 0.5 pra `absenteismo_historico_t1` e -0.1 pra `caderno`. Qual feature empurra aluno pro "risco de não-alfabetizado" mais forte?"

**Sabatina 2.1b:**
> "Se o threshold padrão é 0.5 de probabilidade, e você quer Recall > 0.7, como ajusta o threshold? Qual é o trade-off?"

**Integração de Código 2.1:**
- Arquivo novo: `src/modeling/02_treinar_logistica.py`
- Comparação: Logística vs RandomForest em métricas
- Visualização: Coeficientes interpretáveis

---

#### Módulo 2.2: Feature Encoding em Profundidade
**Duração:** 1-2h leitura + 1-2h código + 1h sabatina

**O que você vai aprender:**
- Label vs One-Hot vs Ordinal vs Target Encoding
- Leakage em Target Encoding (por quê é perigoso)
- Dimensionalidade e curse of dimensionality

**Por que importa:**
- Seu projeto tem `caderno` (4 valores) — qual encoding?
- `rede` pode ter alta cardinalidade — One-Hot explode dimensionalidade?
- Target Encoding sem split treino/teste é leakage direto

**Sabatina 2.2a:**
> "Se você aplicar Target Encoding em `rede` (Municipal/Estadual) ANTES de fazer train/test split, qual é o risco? Como isso afeta as métricas reportadas?"

**Sabatina 2.2b:**
> "Você tem 5500 municípios possíveis. Como encoda isso sem explodir dimensionalidade? Qual é o trade-off?"

**Integração de Código 2.2:**
- Testar Target Encoding vs One-Hot pra `caderno`
- Comparar performance vs interpretabilidade
- Documentar decisão em ADR novo

---

### **BLOCO 3: Modelos Avançados (Com integração e comparação)**

#### Módulo 3.1: Gradient Boosting (XGBoost/LightGBM)
**Duração:** 2-3h leitura + 3-4h código + 1h sabatina

**O que você vai aprender:**
- Por que Boosting funciona (reduz bias e variância)
- XGBoost vs Random Forest (trade-offs)
- Hyperparameter tuning (learning rate, depth, regularization)
- Early stopping (quando parar de treinar)

**Por que importa:**
- Seu RandomForest tem Recall 0.34 — XGBoost deve melhorar
- Boosting é estado-da-arte, mas mais complexo
- Entender **por quê** funciona melhor

**Sabatina 3.1a:**
> "Random Forest treina 200 árvores INDEPENDENTES. XGBoost treina 200 árvores SEQUENCIAIS. Por quê XGBoost é mais poderoso? Qual é o cost?"

**Sabatina 3.1b:**
> "Learning rate no XGBoost = 0.1 vs 0.01. Qual vai ter melhor Recall? Qual vai ser mais lento?"

**Integração de Código 3.1:**
- Arquivo novo: `src/modeling/03_treinar_xgboost.py`
- Comparação: RandomForest vs XGBoost vs LightGBM
- Curva de learning (treino vs teste)
- Reportar qual dataset é used (baseline sem território vs full com território)

---

#### Módulo 3.2: Interpretabilidade (SHAP)
**Duração:** 1-2h leitura + 2-3h código + 1h sabatina

**O que você vai aprender:**
- Diferença: Feature Importance (global) vs SHAP (local)
- SHAP para Random Forest vs SHAP para XGBoost
- Interpretação: Por que modelo prevê cada aluno

**Por que importa:**
- Seu o diário de bordo interno (não publicado) já menciona "SHAP ainda não implementado"
- **CRÍTICO** pra enviar ao Renan (ele vai perguntar "por que esse aluno?")
- Feature Importance negativa (`caderno = -0.038`) — SHAP explica por quê

**Sabatina 3.2a:**
> "Permutation Importance diz `caderno = -0.038`. SHAP vai concordar? Por quê ou por que não?"

**Sabatina 3.2b:**
> "Usando SHAP, você nota que `caderno=12` empurra forte pro "risco". Qual é sua ação: remover feature, investigar dado, ou manter?"

**Integração de Código 3.2:**
- Script novo: `src/visualization/shap_analysis.py`
- SHAP summary plot + dependence plot
- Investigar `caderno=12` com SHAP (tem realmente o padrão anormal?)

---

### **BLOCO 4: Validação Avançada (Sem código novo — refinamento)**

#### Módulo 4.1: Validação Completa
**Duração:** 1-2h leitura + 1h sabatina

**O que você vai aprender:**
- Cross-validation além de temporal/aleatório
- Stratified K-fold pra dados desbalanceados
- Backtesting pra modelos séries temporais

**Por que importa:**
- Seu split temporal tem viés (2023 = sem histórico imputado)
- Validação desbalanceada precisa preservar proporção de classes

**Sabatina 4.1a:**
> "Seu target tem 50% Sim, 50% Não. Ao fazer train/test split 80/20, o split aleatório garantir 50/50 em ambos? Como?"

**Integração de Código 4.1:**
- Adicionar Stratified K-Fold ao baseline
- Comparar: aleatório vs estratificado vs temporal

---

## Cronograma de Execução

| Bloco | Módulo | Duração | Quando |
|-------|--------|---------|--------|
| **1** | 1.1 Fundações | 3-4h | Hoje/amanhã |
| **1** | 1.2 Métricas | 2-3h | Amanhã |
| **2** | 2.1 Logística | 4-5h | 3º dia |
| **2** | 2.2 Encoding | 3-4h | 4º dia |
| **3** | 3.1 XGBoost | 6-7h | 5-6º dia |
| **3** | 3.2 SHAP | 4-5h | 7º dia |
| **4** | 4.1 Validação | 3-4h | 8º dia |
| | | **~35-40h** | **2 semanas** |

---

## Comece Aqui: Módulo 1.1

### Leitura (30-60 min)

Abra `TRILHA_APRENDIZADO_FASE3.md` e leia:
1. Seção "VISAO GERAL"
2. Seção "Trade-offs Fundamentais"
3. Modulo 01 (Aula 2: Classificação vs Regressão)

### Anotações (30 min)

Crie arquivo `NOTAS_APRENDIZADO.md`:

```markdown
# Notas de Aprendizado — Fase 3

## Módulo 1.1: Fundamentos

### O que entendi
[Seus conceitos principais, com suas palavras]

### Exemplo do projeto
[Como conecta com Tech Challenge Fase 3]

### Dúvidas abertas
[O que ficou confuso]
```

### Sabatina 1.1 (Comigo agora)

Pronto pra responder as 2 perguntas acima? (Conceitual + Prática)

---

## Próximos Passos

1. **Você lê Módulo 1.1** (trilha + anotações)
2. **Você responde Sabatina 1.1** (aqui no chat)
3. **Eu faço Sabatina 1.2** se passou
4. **Você avança pra 1.2** ou repete se precisar

Quer começar agora ou prefere se organizar e volta amanhã?
