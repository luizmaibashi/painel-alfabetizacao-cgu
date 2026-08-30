# Conteúdo das aulas da Fase 3 aplicável a este projeto

Escopo: só o que este projeto (classificação binária aluno-nível, sem
clustering, sem série temporal, sem RL) realmente usa — módulos
**Supervisionado** e **Otimização/Avaliação de modelos**. Cada tópico vem
com a ponte direta pra uma decisão já tomada ou pendente no ADR-0001/spec.

## Módulo Supervisionado

### Aula 1 — Fundamentos
Features (X) vs. target (y); o modelo aprende a função que liga um ao
outro minimizando erro. **Ponte**: nosso X é o snapshot (`Alunos` × features
estruturais × histórico t-1), nosso y é `alfabetizado`. Nada de novo
conceitualmente, mas vale lembrar na call: **o algoritmo não cria dado, só
consome** — se a política de leakage (seção 3.2 do handoff) deixar passar
algo, o modelo "aprende" um atalho que não existe fora do dataset.

### Aula 6 — Escalonamento de dados (Feature Scaling) + Encoding
Três técnicas: **Min-Max** (sensível a outlier, usa min/max), **Standardization**
(z-score, sensível moderado, usa média/desvio — padrão pra regressão
logística/SVM), **Robust Scaling** (usa mediana/IQR, não sensível a outlier
— recomendado quando há assimetria/outliers).

**Ponte com o projeto**: `peso_aluno` teve 7 outliers (>3× mediana) na EDA —
plausíveis (peso de pós-estratificação, não erro), mas isso é exatamente o
cenário onde Robust Scaling bate Standardization. Decisão pendente pra
`ColumnTransformer`: qual scaler usar em cada variável numérica — provável
Robust Scaling dado o achado da EDA.

Encoding: Label/Ordinal (quando há ordem natural ou pra modelos em árvore),
One-Hot/Dummy (sem ordem, poucas categorias), Frequency/Count/Target/Hash
(alta cardinalidade). **Ponte**: `caderno` tem só 4 valores → One-Hot é
seguro. `rede` (Municipal/Estadual, possivelmente Federal/Privada na base
completa) → também One-Hot, poucas categorias. Nenhuma variável nossa tem
alta cardinalidade a ponto de precisar Target/Hash Encoding — mas se
`id_municipio`/`id_escola` entrarem como feature categórica direta (não
deveriam, é melhor usar as features estruturais derivadas), aí sim seria
problema.

### Aula 7 — Métricas de avaliação
Classificação: Acurácia (só boa se balanceado — nosso caso está ~51/49%,
então não é totalmente enganosa, mas não é o critério certo mesmo assim),
**Precisão** (foco em não gerar falso positivo — custoso quando alarme falso
é caro), **Recall** (foco em não perder falso negativo — crítico quando
"deixar passar" é caro, como diagnóstico de doença), **F1** (equilíbrio
harmônico dos dois).

**Ponte direta com a Sabatina que já fizemos**: o critério de sucesso do
ADR-0001 (seção 3.5 do handoff) já escolheu **Recall da classe "Não"** como
métrica principal — exatamente o racional da aula: "deixar passar um aluno
em risco impede ação preventiva" é o mesmo exemplo de churn/diagnóstico
citado no material. F1 entra como métrica de suporte pra não deixar
Precisão desabar (não queremos alarme falso em excesso, sobrecarrega o
coordenador).

### Aula 8 — Causalidade (a mais importante pra não prometer demais no vídeo)
Predição ≠ causalidade. Um modelo pode prever bem "quem vai ficar em risco"
sem saber **por que**, e sem saber o que aconteceria se a escola intervisse.
Viés de seleção: comparar grupos que já eram diferentes antes de qualquer
"tratamento" gera conclusão errada (exemplo do case Target: prever gravidez
≠ saber o efeito de mandar a campanha).

**Ponte crítica com o nosso vídeo executivo**: o modelo que vamos entregar é
**preditivo**, não causal. Ele responde "quem está em risco", não "o que
acontece se a escola intervier no aluno X". Isso já está implícito na
decisão de Questão 1 da Sabatina (ação = "priorizar busca ativa com base no
sinal", não "provar que a intervenção funciona") — mas vale deixar
explícito no README/vídeo pra não prometer causalidade que o projeto não
entrega. Se o SHAP apontar "absenteísmo histórico" como fator de risco,
isso é correlação estrutural, não prova de que reduzir o absenteísmo causa
alfabetização — é exatamente o erro do case Target.

## Módulo Otimização e Avaliação de Modelos (aula 1 — slides)

**Data leakage no pipeline (slide 37)**: regra de ouro — `fit_transform`
**só no treino**, `transform` no teste. Nunca dar fit em todos os dados
juntos. **Ponte**: isso é literalmente o requisito "integração do
pré-processamento diretamente ao modelo" do enunciado — o `Pipeline` do
sklearn resolve isso automaticamente (o `fit` do Pipeline inteiro só vê
treino), mas se alguém pré-processar fora do Pipeline (ex: normalizar antes
do `train_test_split`), o leakage volta pela porta dos fundos. Checar isso
no code review antes de qualquer PR.

**Feature Importance / Permutation Importance (slides 56-58)**: importância
nativa de árvores (Random Forest/XGBoost) mede quanto cada feature reduz
impureza; Permutation Importance embaralha uma feature por vez e mede quanto
a métrica piora — mais robusto, não enviesado por cardinalidade.

**Ponte**: essa é a técnica de interpretabilidade que o enunciado pede
("Feature Importance e SHAP Values"). Recomendo usar Permutation Importance
como checagem cruzada do SHAP — se os dois discordarem muito sobre qual
feature mais importa, é sinal de instabilidade no modelo, vale investigar
antes de apresentar no vídeo.

**Comparação de métodos de seleção de features (slide 60)**: Filter (ANOVA),
Wrapper (RFE), Embedded (Random Forest, L1/Lasso) — cada um com trade-off de
custo computacional vs. qualidade. **Ponte**: nosso conjunto de features já
é pequeno (não chega a 15-20 colunas após o snapshot), então feature
selection formal provavelmente não é necessária — mas se `caderno=12` for
confirmado como problemático (achado pendente, seção 3.2 do handoff), pode
valer rodar Embedded (Random Forest) pra ver se ele domina a importância de
forma desproporcional, o que reforçaria a suspeita.

## O que NÃO entra (fora do escopo deste projeto, não ler pra economizar
tempo antes de sábado)

- **Não-Supervisionado** (K-Means, DBSCAN, redução de dimensionalidade) —
  já resolvido pela Fase 2 (`agg_vulnerabilidade_ml`), citado no README mas
  não recriado aqui.
- **Aprendizagem por Reforço** (Bandits, Q-Learning, PPO, RLHF) — sem
  aplicação neste projeto de classificação estática.
- **Séries Temporais** — o enunciado não pede previsão temporal; "prever
  municípios que não atingirão metas futuras" foi decidido como fora de
  escopo (ticket 0006 do wayfinder), fica só como "evolução futura" no
  README.
