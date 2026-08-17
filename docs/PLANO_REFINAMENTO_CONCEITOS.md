# Plano de Refinamento de Conceitos — Dados, CRISP-DM, Modelagem

**Sessão:** 2026-08-17 (Fase 3 completa)  
**Status:** Pausa deliberada para aprofundamento antes de implementação  
**Objetivo:** Elevar nível de confiança nos 3 pilares antes do handoff ao Renan

---

## CONCEITO 1: Dados (EDA, Qualidade, Auditoria)

### Nível Atual
✅ Você fez EDA básica (`reports/eda_alunos.md`)  
✅ Checklist CRISP-DM (8 itens)  
✅ Identificou anomalias (`caderno=12`, `absenteismo_historico_t1`)  
✅ Conhece leakage por teoria  

### Falta Aprofundar
❓ **Auditoria de dados:** Como você saberia se o dado está "errado" sistematicamente?  
❓ **Proveniência:** De onde vem cada arquivo? Quando foi atualizado?  
❓ **Anomalias causais:** `caderno=12` é erro de dados ou padrão real de acessibilidade?  
❓ **Qualidade em produção:** Como monitorar drift de dados quando modelo está ativo?

### Roadmap Prático (3-5h)

**Semana 1:**
1. Ler gate de proveniência em `.claude/rules/dados.md` (temos um!)
2. Preencher `reports/proveniencia_alunos.md`:
   - De onde vem Alunos.csv? (sistema, export, pessoa)
   - Quando foi última atualização REAL?
   - Qual query/tela/comando gerou o arquivo?
3. Investigar `caderno=12`:
   - É erro de digitação? Caderno adaptado? Amostra pequena?
   - Cruzar com metadados do INEP (se público)

**Semana 2:**
4. Desenhar "Anomalia Esperada vs Inesperada":
   - Esperada: absenteismo sobe em período de chuvas (normal)
   - Inesperada: taxa de alfabetização cai 50% de repente sem motivo (RED FLAG)
5. Planejar monitoramento pós-deploy:
   - Quais métricas vigiar todo mês?
   - Qual é o threshold de "drift" que aciona retrain?

**Recursos:**
- `.claude/rules/dados.md` (local, já tem gate de proveniência)
- `HANDOFF_RENAN.md` (seção "Dados e Proveniência")
- Seu próprio EDA (já fez, só refinar)

---

## CONCEITO 2: CRISP-DM (Fases, Gates, Decisões)

### Nível Atual
✅ Conhece as 6 fases (Business Understanding → Deployment)  
✅ Passou nos gates de EDA e Dicionário  
✅ Identificou leakage (política clara)  
✅ Validação temporal implementada  

### Falta Aprofundar
❓ **Decisões não-triviais:** Quais são as 3-4 decisões arquiteturais do projeto?  
❓ **Trade-offs registrados:** Por que Recall é métrica principal, não Accuracy?  
❓ **Comunicação de risco:** Como documentar "essa feature tem risco X mas achei que vale"?  
❓ **Iteração:** Se metrics ficarem ruins no `--full`, qual é o plano B?

### Roadmap Prático (2-3h)

**Atividade 1: Mapeie as 3 Decisões Arquiteturais**
```
Decisão 1: Qual é o modelo final? (Logística? RF? XGBoost?)
  → Por quê essa escolha?
  → Qual era a alternativa rejeitada?
  → Que métrica decidiu?

Decisão 2: Como validar temporalmente?
  → Split 2023→2024, mas e se dados mudarem em 2025?

Decisão 3: Como tratar `caderno=12`?
  → Remover? Investigar? Flagar como risco?
```

**Atividade 2: Escrever ADR (Architecture Decision Record)**
- `docs/adr/0002-modelo-principal-xgboost-vs-randomforest.md`
- Estrutura: Contexto → Alternativas → Decisão → Consequências

**Atividade 3: Risk Register**
- Listar 5 riscos:
  1. "Recall baixo sem território (0.34) → pode não valer o esforço"
  2. "Dados faltando em produção → caderno não preenche 30% das vezes"
  3. "Drift temporal → modelo 2024 não funciona bem em 2025"
  4. ...

**Recursos:**
- `HANDOFF_RENAN.md` (já tem decisões documentadas)
- `docs/wayfinder/tech_challenge_fase3/adr/0001-*.md` (ADR existente)
- `.claude/rules/dados.md` (gates)

---

## CONCEITO 3: Modelagem (Escolha, Trade-offs, Produção)

### Nível Atual
✅ Entende 6 modelos (Logística, RF, XGBoost, K-Means, ARIMA, RL)  
✅ Sabe trade-offs (Interpretabilidade vs Acurácia, Velocidade vs Precisão)  
✅ Conhece validação (K-Fold, Temporal, Stratified)  
✅ SHAP e Threshold Tuning planejados  

### Falta Aprofundar
❓ **Seleção pragmática:** 3 modelos candidatos. Como escolhe um pra produção?  
❓ **Monitoramento pós-deploy:** Modelo está degradando? Como saber?  
❓ **Retraining:** Quando retreinar? A cada mês? Apenas se AUC cair 5%?  
❓ **Fallback:** Se modelo falha, qual é o plano B? (baseline simples? regras?)

### Roadmap Prático (4-5h)

**Atividade 1: Tournament de Modelos (Implementar 3, comparar)**
```
Rodada 1: Logística vs RandomForest (baseline vs ensemble)
Rodada 2: RandomForest vs XGBoost (paralelo vs sequencial)
Métrica: Recall (principal), Precision, F1, Tempo de treino

Vencedor: aquele que melhor Recall COM Precision aceitável
```

**Atividade 2: Desenhe Pipeline de Produção**
```
[Dados Crus] 
  → [Gate de Proveniência] 
  → [EDA Automática] 
  → [Preprocessing] 
  → [Modelo] 
  → [SHAP Explicação] 
  → [Threshold Tuning] 
  → [Saída: Aluno + Risco + Por Quê]
```

**Atividade 3: Plano de Monitoramento**
- Métrica 1: ROC-AUC cai abaixo de 0.65? → alerta
- Métrica 2: Recall fica abaixo de 0.35? → retrain
- Métrica 3: Cobertura: % de municípios no modelo
- Métrica 4: Drift: distribuição de features mudou? (KL-divergence)

**Atividade 4: Documento "Model Card"**
```
Nome: XGBoost Alfabetização
Versão: 1.0
Data: 2026-08-XX

Performance (no --local-only):
- Recall: 0.45 ± 0.05 (5-Fold Temporal)
- Precision: 0.70 ± 0.03

Limitações:
- Sem território/socioeconômico
- Dados de 2023-2024 apenas
- Não testado em municípios rurais isolados

Próximas Iterações:
- Rodar --full com território
- Comparar SHAP vs Permutation Importance
- A/B test com baseline Regressão Logística
```

**Recursos:**
- `TRILHA_APRENDIZADO_FASE3.md` (modelos, trade-offs)
- `docs/PLANO_SABATINAS_PROGRESSIVAS.md` (sabatinas por modelo)
- Seu próprio código em `src/modeling/` (executar, comparar)

---

## Timeline Sugerido pra Refinamento

| Semana | Atividade | Tempo | Bloqueador |
|--------|-----------|-------|-----------|
| **1** | Proveniência de dados | 3h | — |
| **1** | Investigar `caderno=12` | 2h | — |
| **2** | Mapeador decisões + ADRs | 2h | — |
| **2** | Risk Register | 1h | — |
| **3** | Tournament de 3 modelos | 4h | `--full` dados (Renan) |
| **3** | Pipeline de Produção | 2h | — |
| **4** | Monitoramento | 2h | — |
| **4** | Model Card | 1h | — |
| | **Total** | **~17h** | |

---

## Como Usar Este Plano

1. **Faça uma atividade por vez** (não todas de uma vez)
2. **Documente cada descoberta** em markdown
3. **Cruze com HANDOFF_RENAN.md** — não deixe nada desalinhado
4. **Quando terminar cada seção, commit:**
   ```
   git add docs/
   git commit -m "chore: refinamento de conceitos — proveniência de dados"
   ```

5. **Depois de tudo, prepare a call com Renan** com slides mostrando:
   - Decisões arquiteturais (ADRs)
   - Comparação de modelos
   - Plano de monitoramento
   - Risk register e mitigações

---

## Próximo Passo (Depois do Refinamento)

1. ✅ Passar por este plano (17h)
2. ✅ Rodar `--full` com Renan (dados com território)
3. ✅ Retreinar os 3 modelos com dados completos
4. ✅ Generar SHAP + Model Card final
5. ✅ Apresentação executiva pro Renan

