# Preparação de Aprendizado — Tech Challenge Fase 3

**Objetivo:** Mapear o conhecimento da Fase 3 (Pós-Tech FIAP) de forma estruturada, sabatinar o usuário, depois incorporar ao projeto.

---

## Estado Atual do Projeto

### ✅ Artefatos Gerados
- **EDA:** `reports/eda_alunos.md` (checklist CRISP-DM completo)
- **Dicionário de Dados:** `reports/dicionario_alunos.md` (conexão com objetivo, features planejadas)
- **Pipeline sklearn:** `src/preprocessing/pipeline_preprocessamento.py` (ColumnTransformer)
- **Baseline:** `src/modeling/01_treinar_baseline.py` (RandomForest, Permutation Importance)
- **Métricas:** `reports/metrics_baseline.json` (Recall principal, F1, ROC-AUC)

### 🔵 Técnicas Implementadas
| Técnica | Módulo | Implementado | Status |
|---------|--------|--------------|--------|
| Classificação binária | Aula 2 | ✅ | RandomForestClassifier(200, max_depth=8) |
| Validação temporal | Aula 3 | ✅ | Split 2023→2024 + aleatório estratificado |
| Permutation Importance | Aula 3 | ✅ | `scoring="recall"` (métrica principal) |
| Tratamento de leakage | Aula 2-4 | ✅ | ADR-0001 detalhado |
| Imputação com flag | Aula 5 | ✅ | Mediana UF + `possui_historico_t1` |
| One-Hot Encoding | Aula 5 | ✅ | ColumnTransformer pra categóricas |

### ❌ Gaps — Não Implementado (Esperando Trilha)
| Técnica | Módulo | Por quê importa | Plano |
|---------|--------|-----------------|-------|
| Gradient Boosting (XGBoost, LightGBM) | Aula 3 | Estado da arte, potencial melhor Recall | Sabatina + implementar após aprendizado |
| Regressão Logística | Aula 4 | Baseline simples + interpretabilidade (probabilidade) | Comparar vs RF |
| SVM + Naive Bayes | Aula 4 | Cobertura de algoritmos supervisados | Experimentar se tempo |
| Threshold Tuning | Aula 4 | Classificação binary: ajustar cutoff do recall | Otimizar pra minimizar falsos negativos |
| SHAP | Aula 5 | Explicabilidade local + global (criação do modelo) | Implementar ANTES de enviar pra Renan |
| Target Encoding | Aula 5 | Alternativa one-hot pra categorias de alta cardinalidade | Checar se `rede`/município precisam |
| Cross-Validation Avançada | Aula 3 | Além de temporal/aleatório: estratégias customizadas | Baixa prioridade |

---

## Estrutura de Aprendizado (Esperando Trilha)

Quando `TRILHA_APRENDIZADO_FASE3.md` chegar, a gente vai:

### Fase 1: Estudo + Sabatinas Progressivas
1. **Módulo 1 (O quê, Como, Por quê)**
   - Você lê a trilha deste módulo
   - Sabatina rápida (1 pergunta, contexto do projeto)
   - Anotações em `NOTAS_APRENDIZADO.md`

2. **Módulo 2-5 (repetir)**

### Fase 2: Incorporação Técnica (Depois das Sabatinas)
1. Escolher qual gap do quadro acima atacar primeiro (sugestão: XGBoost → SHAP)
2. Escrever código novo em branch `feat/modelo-xgboost`
3. Comparar métricas (Recall, F1, ROC-AUC) com RandomForest
4. Documentar decisão em ADR novo (ex: ADR-0002-xgboost-vs-randomforest)

### Fase 3: Entrega Documentada
1. Atualizar HANDOFF_RENAN.md com novas técnicas
2. Gerar visualizações (SHAP, Feature Importance comparado)
3. README completo (11 seções, conforme enunciado)
4. Enviar pra Renan validar (sem call — só entrega + feedback async)

---

## Métricas Baseline (Pra Comparar Depois)

**Snapshot --local-only (sem território):**

| Split | Recall | Precision | F1 | ROC-AUC |
|-------|--------|-----------|----|---------| 
| Aleatório Estratificado | 0.344 | 0.833 | 0.487 | 0.657 |
| Temporal 2023→2024 | 0.417 | 0.793 | 0.547 | 0.675 |

**Achados de Permutation Importance:**
- `absenteismo_historico_t1` → 0.000 (baixa cobertura, só 4% com histórico real)
- `caderno` → -0.038 (importância negativa, suspeita: caderno=12 pode ser adaptado)
- `peso_aluno` → 0.085 (domina, mas é apenas amostral, não de negócio)

**Conclusão:** Sem território/socioeconômico, modelo não generalize bem. Gap = features ainda faltam. Depois do `--full`, devemos voltar a esse baseline e comparar.

---

## Cronograma Estimado

| Fase | Tarefa | Tempo | Bloqueador |
|------|--------|-------|-----------|
| Aprendizado | Ler + sabatinar trilha completa | 4-6h | Trilha chegar |
| Incorporação | Implementar XGBoost + SHAP | 2-3h | Aprendizado ok |
| Documentação | ADR novo + HANDOFF atualizado | 1-2h | Código testado |
| **Total** | | **7-11h** | |

---

## Próximo Passo

⏳ **Aguardando:** `TRILHA_APRENDIZADO_FASE3.md` (agente compilando 27 PDFs)

Quando chegar:
1. Você lê o módulo 1 (fundamentals)
2. Anotações em `NOTAS_APRENDIZADO.md`
3. Sabatina 1
4. Repete pra módulos 2-5
5. Depois decide: XGBoost? SHAP? Threshold tuning? Qual primeiro?

---

**Artefatos relacionados:**
- `docs/wayfinder/tech_challenge_fase3/SPEC_FINAL.md` — spec completa
- `docs/adr/0001-*.md` — decisões de leakage
- `HANDOFF_RENAN.md` — brief pra Renan (atualizado em tempo real)
