# ADR-0006: Ceiling analysis como gate pré-treino

**Data**: 2026-08-22
**Status**: Accepted com correção (ver Seção 7) — o MECANISMO original tinha
um defeito de método, corrigido no mesmo dia após teste empírico. O VEREDITO
prático (modelo aluno-nível não supera o baseline) sobrevive à correção,
agora confirmado por um caminho independente e mais rigoroso — ver Seção 7.
**Proposto por**: Luiz Maibashi
**Contexto**: Recomeço pedagógico da Fase 3 (2026-08-22) — objetivo de
dominar o método a ponto de explicar para o Renan, não só entregar. Antes de
reescrever qualquer pipeline, a pergunta era: "com todo o know-how já
acumulado, existe algum ajuste de técnica que faria o modelo aluno-nível
encontrar sinal individual?"

---

## 🤔 1. CONTEXTO (O QUÊ?)

A rodada 1 respondeu "o modelo aluno-nível supera o baseline municipal?"
treinando o pipeline inteiro: extração → guarda de leakage → tournament de 3
algoritmos com `GridSearchCV` → SHAP → teste de falsificação → teste de
resíduo. Cinco capítulos do HANDOFF, semanas de trabalho, para chegar em
**0,6013 contra 0,6331** do baseline (README §7.2).

**Pergunta de origem desta sessão:** dado que temos agora domínio maduro de
leakage, validação e teste de falsificação, será que um recomeço com mais
rigor técnico — outro algoritmo, outra formulação, mais feature engineering
— encontraria o sinal que a rodada 1 não achou?

**Restrição de método:** um classificador é uma função `f(x) → p`. Se dois
alunos têm vetor de features idêntico, `f` produz a mesma predição para os
dois — por definição de função, não por limitação de algoritmo. Logo, o
poder discriminante máximo de qualquer modelo treinado sobre um espaço de
features `X` tem um teto matemático, calculável **sem treinar nada**: a taxa
de base de cada grupo de features idênticas, medida fora da amostra (para
não vazar o próprio rótulo do aluno para sua própria predição).

**Dependências afetadas:** ordem canônica do pipeline (README §4, passos
1-8), decisão de prosseguir ou não com o entregável 1 no recomeço.

---

## ⚙️ 2. DECISÃO (POR QUÊ?)

**O que escolhemos:** medir o teto de AUC do espaço de features **antes** de
qualquer tournament, como gate 0 do pipeline — não como auditoria posterior.

### 2.1 Método (`src/evaluation/00_ceiling_analysis.py`)

1. Agrupar alunos por vetor de features idêntico (excluindo leakage, chaves
   e colunas constantes).
2. Para cada grupo, estimar a taxa de risco **out-of-fold** (`StratifiedKFold`,
   k=5): a taxa que prediz um aluno nunca inclui o próprio aluno, nem
   qualquer aluno do mesmo fold de teste.
3. `roc_auc_score(y, taxa_oof)` é o teto: nenhum classificador treinado sobre
   este espaço de features pode superá-lo, porque o oráculo (que já vê o
   grupo de cada aluno) representa o limite superior de qualquer estimador.
4. Comparar o teto contra o baseline de negócio já estabelecido (meta do PDE,
   0,6331). Se o teto está abaixo do baseline, nenhuma técnica de modelagem
   resolve — é o espaço de features que está insuficiente, não o algoritmo.

### 2.2 Armadilha descartada — por que não é leave-one-out simples

A correção ingênua `p_i = (soma_grupo − y_i)/(n_grupo − 1)` é inválida aqui:
dentro de um grupo ela produz só dois valores possíveis de score — um para
`y_i=0`, outro sempre menor para `y_i=1` — o que **inverte** a ordenação por
construção. Primeira execução do script mediu isso: teto caiu para 0,3750
(abaixo do acaso) no espaço cru, contra 0,5099 do teto ingênuo. Era artefato
da fórmula, não achado sobre o dado — o mesmo gênero de erro do ADR-0005
(AUC antissimétrica lida sem checar a direção). Corrigido para OOF k=5, que
não tem esse viés porque a taxa do fold de teste nunca usa alunos do próprio
fold de teste.

### 2.3 Diagnóstico de proxy municipal

O script também reporta `pct_grupos_de_um_municipio`: a fração de grupos de
features cujos alunos pertencem todos ao mesmo município. Perto de 100%
significa que o espaço de features é, na prática, um identificador de
município — o modelo não está aprendendo sobre o aluno, está reconstruindo o
município a partir de proxies.

---

## 3. CONSEQUÊNCIAS

**Positivas:**
- Responde "vale a pena treinar?" em segundos, com `groupby` + `roc_auc_score`,
  antes de gastar o custo de tournament + SHAP + teste de resíduo.
- Separa dois modos de falha que a rodada 1 misturou: "modelo mal treinado"
  (technique) vs. "espaço de features insuficiente" (specification). O
  primeiro se resolve com mais esforço de modelagem; o segundo não.
- Dá o número exato para justificar pedido de dado novo (questionário
  contextual do INEP): "o teto atual é 0,6017, abaixo do baseline; um
  questionário que trouxesse variação intra-município poderia mudar isso,
  mas não sabemos quanto até medir."
- Vira ativo transferível: qualquer projeto futuro (churn, crédito, evasão)
  aplica o mesmo teste antes de comprometer orçamento de modelagem.

**Negativas:**
- Teto in-sample-por-fold ainda é otimista frente a um modelo real: o
  oráculo vê o grupo completo do fold de treino, um modelo real vê só as
  features, não o grupo. O teto é limite superior, não previsão do
  desempenho real — por isso o script reporta também a leitura ingênua, para
  deixar essa diferença visível.
- Não substitui o teste de falsificação — decide se vale a pena chegar até
  ele, não fecha o veredito sozinho (o gate 0 barra pipeline caro; a decisão
  final de entregar ainda passa pelo teste com IC bootstrap).

---

## 4. ALTERNATIVAS DESCARTADAS

| Opção | Por quê foi rejeitada |
|-------|----------------------|
| Repetir o tournament completo com mais algoritmos (redes neurais, ensemble stacking) | Custo alto para responder uma pergunta que um `groupby` responde em segundos; três algoritmos já convergiram no mesmo teto na rodada 1 |
| Feature engineering adicional sobre as mesmas 12 colunas (interações, polinômios) | Não cria variação intra-município onde não existe — o teto de um espaço de features é invariante a transformações que não introduzem informação nova |
| Leave-one-out simples como correção do teto ingênuo | Inverte a ordenação por construção em grupos pequenos — medido, descartado (Seção 2.2) |
| Confiar no teto ingênuo (0,8579) sem correção out-of-fold | Conta o próprio rótulo do aluno na taxa que o prediz — vazamento estrutural, não achado |

---

## 5. IMPACTO ROI

- **Métrica de sucesso:** o gate está implementado e produz o identificador
  `auc_oof` em `reports/ceiling_analysis.md`, comparado contra
  `AUC_BASELINE_PDE` (0,6331) e `AUC_MODELO_RODADA1` (0,6013), ambos
  constantes citáveis em `src/evaluation/00_ceiling_analysis.py`.
- **Resultado medido nesta sessão:** teto OOF do snapshot de modelagem
  (12 features) = **0,6017** — folga de **+0,0004** sobre o modelo real da
  rodada 1 (XGBoost + tournament), e **abaixo** do baseline municipal
  (0,6331). 99,1% dos grupos de features pertencem a um único município.
- **Timeline:** gate roda em segundos sobre a base completa (48.055 alunos);
  vira passo 0 do pipeline do README, antes do passo 1 (extração completa).
- **Risco de regressão:** se features novas entrarem no snapshot (ex.:
  questionário contextual do INEP), o script precisa rodar de novo antes de
  reautorizar treino — caso contrário o gate vira decoração, o mesmo padrão
  do gate "lista de cobertura falha aberta" já registrado em
  `AGENTS.md` da base de conhecimento.

---

## 7. CORREÇÃO (2026-08-22, mesmo dia) — o teto de 0,6017 estava errado, o veredito não

**Como foi achado:** Luiz perguntou, com razão, se um modelo mais forte (mais
árvores, outra família de algoritmo) não encontraria sinal que o teto dizia
não existir. Testado (`00b_verificacao_teto_modelo_forte.py`): XGBoost forte
e MLP **superaram** o teto e o baseline (~0,66). Isso não deveria ser
matematicamente possível se o teto fosse um limite real — então não era.

**Causa raiz do teto errado:** o `groupby` por tupla exata das 12 features
tratava `caderno` (4 valores) e `rede` (2 valores) — ruído administrativo,
sem sinal — como se dividissem informação de verdade, fragmentando cada
**4.478 municípios reais** em **15.652 grupos**, tamanho mediano caindo de
28 para 5. Além disso, duas features contínuas (`meta_alfabetizacao_2024_imputada`,
`populacao_total`) quase nunca repetem valor exato entre municípios
diferentes — o oráculo por tupla não consegue **suavizar** entre municípios
parecidos, mas um XGBoost consegue (aprende uma função contínua, não uma
tabela de contagem exata). O princípio "`f(x)` idêntico → mesma predição"
continua válido; a implementação (agrupar por tupla discreta, incluindo
ruído) não media esse princípio corretamente.

**Segunda pista falsa, no mesmo dia:** a primeira tentativa de verificação
usou `StratifiedKFold` sobre 2023+2024 **misturados**. Como `meta`/`população`
são quase constantes por município entre os dois anos, esse desenho deixa o
modelo "espiar" o outro ano do mesmo município durante o treino — vazamento
temporal disfarçado de vitória. Isso inflou tudo pra ~0,66, **inclusive o
baseline** (0,6588, contra o 0,6331 já publicado no README para o mesmo
baseline) — o próprio número do baseline divergindo do já validado foi o
sinal de que a metodologia, não o achado, estava errada.

**Teste correto, refeito** (`00c_teste_residuo_modelo_forte.py`): mesma
metodologia canônica do projeto — split temporal (treina 2023, testa 2024),
mesmo baseline de `02_teste_falsificacao.py` (o melhor entre taxa t-1 e meta
do PDE) — com um XGBoost **muito mais forte** que o da rodada 1 (800 árvores/
profundidade 8, contra 300/4):

| | AUC |
|---|---|
| A — baseline (meta do PDE) | **0,6331** — idêntico ao README, confirma que a metodologia está certa agora |
| B — XGBoost forte, só features municipais | 0,6101 |
| **C — XGBoost forte, município + aluno (12 features)** | **0,6026** — quase idêntico ao 0,6013 da rodada 1 |
| C vs B (decide sinal individual) | **−0,0075**, IC95% [−0,0122, −0,0027] — features de aluno **pioram**, com significância |

**Veredito da correção:** um modelo muito mais forte que o da rodada 1,
avaliado com a metodologia correta, chega em **praticamente o mesmo lugar**
(0,6026 vs 0,6013). O achado central do projeto (modelo aluno-nível não
supera o baseline municipal, sem sinal individual a extrair) fica **mais
confirmado, não menos** — agora por dois caminhos independentes (tournament
fraco da rodada 1, modelo forte + validação rigorosa de hoje).

**O que muda de fato:**
- O número "0,6017" e a leitura "teto matemático do espaço de features" da
  Seção 5 **não são confiáveis** como estavam escritas — deixados no
  documento por transparência (mesmo padrão do ADR-0005 do próprio
  projeto), mas não devem ser citados como teto real.
- `00_ceiling_analysis.py` **não é um gate confiável quando o espaço de
  features mistura contínuas com categóricas de baixa cardinalidade e
  baixo sinal** (o caso deste projeto). Fica como ferramenta válida só para
  espaços de feature puramente categóricos de alta granularidade, ou como
  primeira pista barata a ser **sempre** confirmada por um teste como o
  Passo C acima antes de virar conclusão.
- O gate pré-treino real e confiável passa a ser: **modelo forte + split
  temporal correto + baseline mais forte disponível + IC bootstrap** — mais
  caro que um `groupby`, mas sem o vício de método que o atalho barato
  escondia. Esse padrão foi absorvido em `02_teste_falsificacao.py` e
  `03_teste_residuo.py` (upgrade de hiperparâmetro em 2026-08-22, mesmo dia).
  `00_ceiling_analysis.py`, `00b_verificacao_teto_modelo_forte.py` e
  `00c_teste_residuo_modelo_forte.py` cumpriram o papel de investigação
  pontual e foram **removidos** depois de confirmado que 02/03 com o modelo
  forte chegam no mesmo número (0,6026) — as tabelas desta seção preservam
  o achado, o código exploratório não precisava sobreviver a ele.
- Isso é o mesmo tipo de correção que o ADR-0005 já registrou uma vez
  (métrica lida sem checar a direção/metodologia) — outra instância da
  regra "confiar em métrica sem entender a fórmula é como confiar em régua
  sem saber se está em cm ou polegada".

## 8. LINKS RELACIONADOS

- [[docs/adr/0001-pipeline-sklearn-snapshot-e-politica-leakage.md]] — política
  de leakage que define as colunas excluídas do espaço de features testado.
- [[docs/adr/0005-correcao-da-regua-do-baseline-intra-uf.md]] — mesmo gênero
  de erro (métrica lida sem checar metodologia/direção), duas vezes no mesmo
  projeto: lá era AUC antissimétrica, aqui foi teto por tupla discreta +
  vazamento temporal em k-fold aleatório.
- `src/evaluation/02_teste_falsificacao.py` e `03_teste_residuo.py` — testes
  canônicos que herdaram o modelo forte e a metodologia validados nesta ADR
  (00/00b/00c removidos após confirmação, ver Seção 7).
- `reports/dicionario_alunos.md` — origem do contrato de colunas usado em
  `EXCLUSOES`/`CHAVES` do script original.
