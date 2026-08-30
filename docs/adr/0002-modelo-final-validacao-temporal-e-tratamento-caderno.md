# ADR-0002: Modelo final em aberto, validação temporal e tratamento condicional de `caderno`

**Data**: 2026-08-18
**Status**: Proposed (as 3 decisões desta ADR ficam explicitamente em aberto
para o Renan revisar/aprovar/reajustar na call — nenhuma é unilateral do
Luiz, ao contrário do ADR-0001)
**Proposto por**: Luiz Maibashi
**Contexto**: Sessão de refinamento pós-Fase-3 (`PLANO_REFINAMENTO_CONCEITOS.md`,
Seção 2 — ADRs e decisões arquiteturais), 2026-08-17/18.

> **Atualização (2026-08-30):** a premissa de §2.2 foi superada. O Inep
> publicou a planilha municipal oficial de 2025; o backtest prospectivo do
> produto intra-UF foi executado e fechado no ticket 0018. O resultado é uso
> condicional (14 UFs vencem, CE perde, 8 são inconclusivas), documentado em
> `reports/backtest_prospectivo_2025.json` e
> `reports/decisao_produto_pos_backtest_2025.md`. Esta ADR preserva a decisão
> original e não deve mais ser lida como limitação vigente de ausência de
> dado temporal.

---

## 🤔 1. CONTEXTO (O QUÊ?)

Com o baseline RandomForest rodado (`--local-only`, Recall 0,34–0,42) e a
EDA/dicionário fechados, restam 3 decisões que o enunciado oficial
(`[IAST] - Tech Challenge - Fase 3.pdf`) exige tornar explícitas no README
final (seções "Escolha do algoritmo", "Limitações do projeto", "Insights
encontrados") mas que ainda não estão fechadas — e não devem ser fechadas
sozinho, porque o Renan avalia/ajusta na call de alinhamento.

---

## ⚙️ 2. DECISÃO (POR QUÊ?)

### 2.1 Modelo final — EM ABERTO, tournament rodado (atualizado 2026-08-18)

**Tournament executado** (`src/modeling/02_tournament_modelos.py`): os 3
candidatos treinados sobre o mesmo split, com `GridSearchCV` +
`StratifiedKFold(5)` no treino e teste tocado uma vez só.

⚠️ **Números refeitos em 2026-08-18** após a descoberta do vazamento por
`peso_aluno` (Cap. 9 do HANDOFF_RENAN.md). A tabela abaixo é a versão válida:

| Modelo | Recall | Precision | F1 | ROC-AUC | gap treino-val |
|---|---|---|---|---|---|
| Regressão Logística | 0,423 | 0,543 | 0,476 | 0,537 | +0,005 |
| Random Forest | 0,423 | 0,543 | 0,476 | 0,526 | +0,015 |
| XGBoost | 0,657 | 0,512 | 0,576 | 0,530 | +0,009 |

Os três convergem para ROC-AUC ≈ 0,53 (moeda = 0,50). A versão anterior desta
tabela (XGBoost com ROC-AUC 0,669) media a detecção de ausência à prova, não
risco de não-alfabetização.

**A decisão continua EM ABERTO — e agora por um motivo mais forte: não há o que
decidir ainda.** Com ROC-AUC ≈ 0,53 nos três, "escolher o vencedor" seria
escolher entre três moedas. A comparação só passa a significar algo depois do
`--full`.

O que sobrou de "influência" no modelo é 84,8% `caderno`, concentrado na
categoria 12 — a anomalia que 3 tentativas de validação não explicaram (§2.3).
Ou seja, o pouco que o modelo usa é justamente o que menos entendemos.

**Proposta levada pra call:** não escolher modelo agora. Reexecutar o tournament
quando houver `--full` e decidir com número que signifique alguma coisa. O
desenho da comparação (k-fold, teste tocado uma vez, grids comparáveis) está
pronto e validado — só falta dado.

### 2.2 Validação temporal sem dado de 2025 — decisão histórica, superada

Na data desta decisão, o projeto não tinha acesso ao resultado municipal de
2025; por isso, a escolha correta era documentar a lacuna em vez de simular
monitoramento de produção. Essa condição foi superada em 2026-08-30 pelo
backtest prospectivo 2023→2024→2025 do ticket 0018. A limitação vigente não é
mais ausência total de ano futuro, mas haver apenas **uma** transição temporal
validada e efeito heterogêneo por UF; a recomendação atual exige atualização
anual antes de alterar a regra de cada estado.

### 2.3 Tratamento de `caderno=12` — feature condicional, com risco registrado

`caderno=12` (236 alunos, 86,9% "Não" vs. ~50% dos demais) segue como
**feature "com ressalva"** no `reports/dicionario_alunos.md`. Hipótese de
caderno adaptado/acessibilidade reforçada por analogia geral com avaliações
do INEP em larga escala, mas **não confirmada** — 3 tentativas de validação
nesta sessão (portal INEP restrito por login; basedosdados.org sem
dicionário de valores pra coluna; PDF do relatório técnico com erro de
certificado) não resolveram. Decisão prática: manter a feature, exigir
checagem explícita no SHAP (Seção 3/Atividade 3 do plano) se `caderno`
domina de forma suspeita, e levar a decisão final (manter/remover/flagar)
pro Renan aprovar na call — não é decisão unilateral.

**Razão principal:**
"Se NÃO deixarmos essas 3 decisões explicitamente em aberto pro Renan: ele
chega na call sem contexto pra avaliar, e qualquer ajuste que ele pedir
depois vira retrabalho tardio em vez de decisão conjunta a tempo. Se
deixarmos: a call vira revisão de propostas já fundamentadas, não
brainstorm do zero — mais rápida e com decisão de fato compartilhada."

---

## 📊 3. CONSEQUÊNCIAS

**Positivas (Wins):**
- README final já nasce com a estrutura que o enunciado pede
  (`Escolha do algoritmo`, `Limitações do projeto`) preenchida com decisão
  fundamentada, não texto de preenchimento.
- Risco de `caderno=12` documentado desde já, então o SHAP (quando rodar)
  já sabe o que checar — não é análise cega.
- Renan entra na call com decisões pré-mastigadas pra aprovar/ajustar, não
  pra descobrir do zero.

**Negativas (Custo/Risco):**
- Modelo final ainda não escolhido — qualquer material de apresentação
  gerado antes do tournament (Seção 3) fica provisório e pode precisar
  retrabalho se o vencedor mudar a narrativa dos insights.
- Hipótese de `caderno=12` continua sem confirmação real — se o Renan tiver
  acesso ao pacote de microdados original do INEP (fora do portal restrito
  que travou Luiz), essa validação pode se resolver rápido na própria call.
- Decisão de não monitorar é específica **para esta entrega acadêmica** —
  se o projeto virar algo real (não é o caso aqui), essa decisão precisaria
  ser revisitada.

**Timeline:**
- Tournament de 3 modelos: ✅ rodado em 2026-08-18 (`--local-only`); re-rodar quando o `--full` existir.
- Call com Renan: pendente, sem data marcada ainda.

---

## 🎯 4. ALTERNATIVAS DESCARTADAS

| Opção | Vantagem | Por quê rejeitada |
|-------|----------|--------------------|
| Fechar o modelo final agora com RandomForest (já rodado) | Evita esperar o tournament | ❌ Decisão precipitada — Logística e XGBoost ainda não testados, e o enunciado valoriza comparação explícita de algoritmos |
| Construir pipeline de monitoramento de drift agora | Mais robusto, "parece" produção real | ❌ Enunciado não exige; consumiria tempo do prazo real sem melhorar a nota, que pesa 90% da fase |
| Remover `caderno` do modelo por precaução, sem confirmar a hipótese | Elimina o risco de proxy de necessidade especial | ❌ Descarta um achado real da EDA sem evidência definitiva — decisão também deveria ser do Renan, não unilateral |
| Não levar as 3 decisões pra call, resolver tudo sozinho antes | Menos dependência de agenda do Renan | ❌ Contraria o próprio objetivo desta ADR (decisão compartilhada) e o enunciado, que valoriza discussão com terceiros ("discutir suas ideias com os professores ao longo do processo") |

---

## 💰 5. IMPACTO ROI & VALIDAÇÃO

**Métrica de sucesso:**
- Tournament decide o modelo final por Recall da classe "Não" (principal),
  Precision (contrapeso), tempo de treino (desempate).
- Critério de falsificação da decisão de `caderno`: se o SHAP mostrar
  `caderno=12` dominando a predição de forma desproporcional (fora do
  padrão das outras features de metadado), a feature deve ser removida ou
  flagada explicitamente no relatório, mesmo sem confirmação externa.

**Cenários de regressão (quando falha silenciosamente):**
1. Tournament roda só em `--local-only` (sem território) e o vencedor muda
   quando o Renan rodar `--full` — decisão desta ADR pode precisar reabrir.
2. `caderno=12` nunca é confirmado nem desconfirmado, e o relatório final
   trata a feature como neutra sem repetir a ressalva — silenciosamente
   reintroduz o risco que esta ADR documentou.
3. A call com Renan não acontece a tempo do prazo de entrega — as 3
   decisões precisam de um dono de fallback (Luiz decide sozinho, registra
   que não houve tempo de validação cruzada).

**Monitoramento (a checar no relatório final):**
```
- checar: os 3 modelos do tournament rodaram com o MESMO split (comparação justa)
- checar: SHAP de caderno=12 comentado explicitamente no relatório, não omitido
- checar: seção "Limitações do projeto" do README menciona ausência de dado 2025
- checar: as 3 decisões desta ADR aparecem no HANDOFF_RENAN.md antes da call
```

---

## 🔗 6. REFERÊNCIAS & LINKS

**Relacionados:**
- `ADR-0001` (pipeline sklearn, política de leakage) — decisões desta ADR
  não alteram nada do ADR-0001, só adicionam as 3 pendências novas.
- `PROJETOS/01_PRIORITY/tech-challenge-fase3-alfabetizacao/docs/aprendizado/PLANO_REFINAMENTO_CONCEITOS.md`
  (Seção 2, origem desta ADR).
- `PROJETOS/01_PRIORITY/tech-challenge-fase3-alfabetizacao/reports/proveniencia_alunos.md`
  (investigação completa de `caderno=12`, 3 tentativas de validação).
- `PROJETOS/01_PRIORITY/tech-challenge-fase3-alfabetizacao/reports/dicionario_alunos.md`
  (linha `caderno`, decisão CONDICIONAL).
- `PROJETOS/01_PRIORITY/tech-challenge-fase3-alfabetizacao/docs/HANDOFF_RENAN.md`
  — **documento vivo único do projeto** (a partir de 2026-08-18 consolidou o
  feedback da Fase 2, a auditoria do enunciado e o Risk Register, que antes
  eram arquivos separados). As 3 decisões desta ADR aparecem nos Capítulos 4,
  6 e 8.
- `[IAST] - Tech Challenge - Fase 3.pdf` (enunciado oficial, seções README e
  Vídeo Executivo usadas para descartar a alternativa de monitoramento).

**Pendência formal resolvida em 2026-08-20:** mesma do ADR-0001 — arquivo
já migrado para este `docs/adr/`.

---

## ✅ CRITÉRIA DE ACEITAÇÃO

- [x] Trade-offs documentados com justificativa (credibilidade técnica da
      entrega + tempo real de prazo, projeto acadêmico).
- [x] Alternativas rejeitadas com motivo técnico (Seção 4).
- [x] Impacto quantificado onde possível (Recall, cardinalidade de `caderno`).
- [x] Métricas de sucesso definidas e testáveis (Seção 5).
- [x] Plano de checagem descrito (checklist Seção 5).
- [x] Riscos/edge cases identificados (3 cenários de falha silenciosa).
