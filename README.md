# Tech Challenge Fase 3 — Predição e Inteligência Analítica para Alfabetização no Brasil

> Modelo supervisionado que prevê se um **aluno** será considerado
> alfabetizado, testado contra o próprio critério de sucesso que o projeto
> definiu antes de treinar qualquer coisa. **Veredito: o modelo não supera o
> melhor baseline municipal.** Este README existe para mostrar como
> chegamos lá, por que isso é o resultado certo a reportar, e o que fazer
> com ele.

---

## 1. Contexto do problema

A alfabetização infantil é um dos indicadores mais diretos do
desenvolvimento educacional brasileiro, e o Indicador Criança Alfabetizada
(INEP/Pesquisa Alfabetiza Brasil) é a régua oficial usada para medi-la.

Na **Fase 2** deste desafio, construímos a pipeline de engenharia de dados
que trata esse indicador em nível **município**: um painel que responde
"qual município está em risco, e onde investir". Esse é o problema do
Secretário/Prefeito — decisão macro, orçamento, priorização territorial.

A **Fase 3** muda o grão e o cliente. Agora o problema é do **Diretor ou
Coordenador Pedagógico**, que já sabe em qual escola está e precisa saber
**qual aluno específico** vai precisar de intervenção. Descer de município
para aluno não é o mesmo problema em escala menor — é decidir sobre um
indivíduo, não sobre uma média. Essa mudança de grão é o eixo que atravessa
todas as decisões técnicas deste projeto: a maior parte do trabalho foi
distinguir "isso é informação real do aluno" de "isso é informação do
município disfarçada de individual".

## 2. Objetivo analítico

Desenvolver um modelo supervisionado que prevê se um aluno será
`alfabetizado` (Sim/Não) — corte oficial de 743 pontos na escala do exame —
usando variáveis educacionais, territoriais e socioeconômicas disponíveis
**antes** do resultado do próprio aluno, para alimentar ação de busca ativa
na ponta escolar.

**Critério de sucesso definido antes de qualquer treino** ([`ADR-0001`](../../docs/wayfinder/tech_challenge_fase3/adr/0001-pipeline-sklearn-snapshot-e-politica-leakage.md) §5):
o modelo aluno-nível só se justifica se **superar** o baseline trivial de
aplicar um risco já calculado por município (Fase 2) igualmente a todos os
alunos daquele município. Um modelo que não bate esse baseline está apenas
reproduzindo, com mais complexidade e mais risco de erro, uma informação
que já existia pronta. Essa é a pergunta que decide o projeto — não "o
modelo prevê bem?", mas "o modelo prevê melhor do que eu não fazer nada de
novo?".

## 3. Descrição da base utilizada

### 3.1 Por que não é a camada Gold (divergência do enunciado, justificada)

O enunciado pede dados "provenientes da camada Gold desenvolvida na Fase 2".
Auditamos os dois geradores de Gold que existem no repositório da Fase 2 —
o script local (`src/gold/01_gerar_marts_gold.py`, 9 marts) **e** o script
que roda de fato no GCP (`src/cloud/dataproc_03_gold.py`, 15 marts,
Dataproc/GCS/BigQuery) — e confirmamos que **nenhum mart da Gold, em nenhuma
das duas versões, tem grão de aluno**. Todos são `groupBy` em
município/UF/rede/ano, inclusive o único que usa Machine Learning
(`agg_vulnerabilidade_ml`, K-Means, que agrega para município antes de
clusterizar). Detalhe completo, com citação de linha de código, em
[`ADR-0003`](../../docs/wayfinder/tech_challenge_fase3/adr/0003-gold-vs-silver-fonte-de-dados.md).

Não é uma lacuna de extração desta fase — é uma característica de como a
Gold foi desenhada na Fase 2, para consumo de BI município-nível. Usar a
Gold para o problema aluno-nível exigiria inventar linhas que não existem
nela; e as poucas colunas município que poderiam ser juntadas por aluno
(`taxa_alfabetizacao`, `gap_meta`, `deficit_absoluto_proxy`) são todas
funções agregadas do próprio desempenho dos alunos sendo preditos —
vazamento circular por construção do mart, não escolha de modelagem.

### 3.2 O que usamos de fato

| Fonte | O que traz | Onde |
|---|---|---|
| Microdados `Alunos.csv` | 57.781 alunos (2023-2024), grão individual — nunca processado além de Bronze→Silver pela Fase 2 | `dados/` (herdado da Fase 2) |
| Silver `alfabetizacao_municipios_obt_com_metas_imputadas` | Meta do PDE por município (KNN, ADR-004 da Fase 2) | GCS (`--full`) |
| IBGE SIDRA (API pública) | População total por município | `src/preprocessing/05_montar_territorio.py` |
| Metas do PDE (arquivo local) | Meta oficial 2024 por município/rede | idem |

Dicionário completo, coluna a coluna, com decisão de uso e justificativa:
[`reports/dicionario_alunos.md`](reports/dicionario_alunos.md).
EDA (3 datasets — alunos completo, amostra histórica, snapshot de
modelagem): [`reports/eda_alunos.md`](reports/eda_alunos.md),
[`reports/eda_snapshot_modelagem.md`](reports/eda_snapshot_modelagem.md).

### 3.3 População de modelagem — alinhada à metodologia oficial

Validamos nosso cálculo de taxa de alfabetização contra o número publicado
pelo INEP usando a mesma metodologia que a Fase 2 já implementava e
validava: **apenas alunos avaliados, ponderados pelo peso amostral**
(`peso_aluno` como peso estatístico — nunca como feature, ver §9). Alunos
ausentes têm rótulo por convenção ("não fez prova ⇒ não alfabetizado"), não
por medição, e por isso saem da população de modelagem: **57.782 → 48.055
alunos avaliados**.

## 4. Etapas de modelagem

Pipeline scikit-learn completa, com pré-processamento integrado ao modelo
(`Pipeline` único, não etapas soltas):

1. **Extração** (`src/preprocessing/02_extrair_snapshot.py`) — junta
   microdados + histórico t-1 + território, nos modos `--local-only` e
   `--full`.
2. **Guarda de vazamento** (`src/preprocessing/03_guarda_leakage.py`) —
   testa toda feature candidata por nulidade prediz o alvo, valor isola o
   alvo, e poder isolado suspeito. Sai com código 1 em suspeita ALTA — roda
   como gate antes de qualquer treino.
3. **Pipeline de pré-processamento** (`src/preprocessing/pipeline_preprocessamento.py`)
   — `ColumnTransformer`: `SimpleImputer` (mediana) + Robust Scaling para
   numéricas, One-Hot para categóricas. Adaptativa: descobre as colunas
   disponíveis em vez de lista fixa (evitava descartar território em
   silêncio quando o `--full` trouxesse features novas).
4. **Baseline** (`src/modeling/01_treinar_baseline.py`) — RandomForest,
   validação dupla (aleatória + temporal), Permutation Importance.
5. **Tournament** (`src/modeling/02_tournament_modelos.py`) — 3 candidatos,
   `GridSearchCV` + `StratifiedKFold(5)` só dentro do treino, teste tocado
   uma única vez no fim. Split temporal (treina 2023, testa 2024) como
   checagem separada.
6. **Interpretabilidade** (`src/evaluation/01_shap_interpretabilidade.py`) —
   SHAP sobre o vencedor do tournament, com gates automáticos derivados do
   ADR-0001 §5.
7. **Teste de falsificação** (`src/evaluation/02_teste_falsificacao.py`) — o
   script que decide se o projeto se justifica (§7 e §8 abaixo).

### Tratamento de data leakage

Cinco colunas foram identificadas como vazamento do mesmo evento (aluno
faltou à prova) por caminhos diferentes — três por **valor**
(`proficiencia`, `presenca`, `preenchimento_caderno`), duas por **ausência
de valor** (`peso_aluno`, cuja nulidade coincidia 100% com faltosos;
`caderno=12`, que tinha 79,7% de ausentes disfarçados de categoria de
risco). Todas as cinco estão fora do modelo. Detalhe em
[`docs/HANDOFF_RENAN.md`](docs/HANDOFF_RENAN.md) Caps. 9 e 11.

### Validação e generalização

`StratifiedKFold(5)` faz o papel do conjunto de validação do enunciado,
sempre dentro do treino; o conjunto de teste é tocado uma única vez, depois
do tuning de hiperparâmetro escolhido — usar o teste para tuning vazaria
generalização de forma silenciosa. Split temporal (2023→2024) roda em
paralelo como segunda checagem, mais próxima do uso real. `requirements.txt`
com versões pinadas garante replicabilidade — o próprio scikit-learn 1.8→1.9
mudou o Recall do baseline em 1,6 pontos percentuais com o mesmo seed.

## 5. Escolha do algoritmo

Três candidatos comparados no mesmo split e mesmo k-fold: Regressão
Logística, Random Forest e XGBoost.

| Modelo | Recall | Precision | F1 | ROC-AUC | gap treino-val |
|---|---|---|---|---|---|
| Regressão Logística | 0,694 | 0,433 | 0,533 | 0,533 | +0,002 |
| Random Forest | 0,729 | 0,431 | 0,542 | 0,537 | +0,013 |
| **XGBoost** | 0,725 | 0,441 | **0,548** | **0,554** | +0,043 |

*(Base completa, 48.055 alunos avaliados, população oficial, sem
território — ver §7 para os números finais com território.)*

XGBoost lidera nas três métricas de decisão e sustenta a liderança na
checagem temporal. A Regressão Logística — quase cega (ROC-AUC 0,533,
próximo de moeda) — não é descartada por ser "modelo ruim": é diagnóstico de
que as features disponíveis não têm relação **linear** forte com o alvo, e
esse achado permanece no relatório em vez de ser omitido.

**Métrica de decisão**: Recall da classe "Não" (aluno em risco). Falso
negativo — aluno em risco não identificado — é o erro caro para busca
ativa; Precision entra como contrapeso para não degenerar em marcar todo
mundo como risco.

## 6. Métricas de avaliação

| Métrica | Por quê |
|---|---|
| **Recall (classe "Não")** — principal | Custo de um falso negativo (aluno em risco não identificado) é maior que o de um falso positivo (visita desnecessária) |
| Precision | Contrapeso — evita que o modelo maximize Recall marcando quase todo mundo |
| ROC-AUC | Mede separação global, usado para comparar contra o baseline no teste de falsificação |
| Recall@K / Precision@K (busca ativa) | Métrica de negócio real: "se posso visitar K alunos, quantos em risco eu encontro?" |
| **IC95% bootstrap pareado** | Toda comparação modelo vs. baseline reporta intervalo de confiança — nunca diferença pontual sem incerteza (regra da base de conhecimento) |

## 7. Interpretação dos resultados

### 7.1 SHAP — o que o modelo de fato usa

Com o vazamento removido e a população correta, a influência se concentra
em **agregados de município**:

| Bloco de features | Influência (SHAP) |
|---|---|
| Histórico municipal (absenteísmo t-1 + contador + flag) | **60,9%** |
| `rede` | 13,3% |
| `caderno` (efeito residual, sem o artefato de ausência) | 11,6% |
| Histórico de escola (4 features) | 14,2% |

### 7.2 O teste de falsificação — o resultado que decide o projeto

Território (população, meta do PDE, UF) foi integrado **sem depender de
credencial GCP** — o dado é público (API do IBGE + arquivo de metas já em
disco). Isso mudou o modelo de aleatório para algo com sinal real:

| Abordagem | ROC-AUC |
|---|---|
| Baseline: taxa de não-alfabetização municipal t-1 | 0,5816 |
| **Baseline: meta do PDE, aplicada uniformemente a todos os alunos do município** | **0,6331** |
| **Modelo aluno-nível completo (12 features)** | **0,6013** |

Diferença modelo − melhor baseline: **−0,0318**, IC95% bootstrap pareado
**[−0,0374, −0,0261]** — inteiramente negativo. O modelo perde em **5 de 5**
orçamentos de busca ativa testados (5% a 50% dos alunos).

**Isso não foi a primeira medição.** Uma versão anterior do teste, usando a
taxa bruta municipal como baseline, tinha *passado* (0,6013 vs 0,5816,
IC95% [+0,0129, +0,0263]). Investigar de onde vinha essa vitória mostrou que
ela dependia quase inteiramente de uma única feature — a meta do PDE — que
correlaciona 0,979 com a taxa de alfabetização do próprio ano. Ou seja: a
meta *é* um número município tão forte que comparar o modelo contra um
baseline mais fraco não provava nada. Corrigimos o teste para usar **o
melhor baseline disponível**, não o primeiro que passasse — e o veredito
inverteu. Ver [`docs/HANDOFF_RENAN.md`](docs/HANDOFF_RENAN.md) Cap. 14 para
a sequência completa, incluindo o bug de leitura do intervalo de confiança
que também foi corrigido nesse processo.

### 7.3 Leitura honesta

O modelo aprendeu algo real — saiu de ROC-AUC aleatório (0,507, antes do
território) para 0,601. Mas o sinal que ele capturou é fundamentalmente
municipal (SHAP confirma: histórico de município soma 60,9% da influência).
**Usar esse sinal diretamente, sem passá-lo por um modelo de aluno, funciona
melhor do que o modelo.** É exatamente o cenário de regressão previsto no
ADR-0001 §5 ("o modelo é o baseline municipal disfarçado") — agora medido,
não hipotético.

## 8. Insights encontrados

**Cinco caminhos de vazamento levaram ao mesmo evento.** `proficiencia`,
`presenca`, `preenchimento_caderno`, `peso_aluno` e `caderno=12` — três por
valor, duas por ausência de valor — todos codificavam "o aluno faltou à
prova", que por convenção do indicador vira "não alfabetizado". Um modelo
treinado com qualquer uma dessas colunas presentes media detecção de
ausência, não risco de não-alfabetização — e o ROC-AUC "bonito" de versões
iniciais (0,669) desaparecia por completo ao removê-las (0,497, abaixo de
moeda). Guarda automatizado criado (`03_guarda_leakage.py`) para não
depender de inspeção manual — funciona como gate de CI, portável para
outros projetos.

**A pesquisa é amostral, e isso restringe o nível de agregação viável.** Com
2,37 alunos por escola em média e 49,9% dos grupos escola-ano com um único
aluno, uma "taxa de absenteísmo por escola" não é estatisticamente viável —
só pode valer 0% ou 100%. Por município a cobertura é robusta (65,2% entre
anos). O SHAP confirmou empiricamente essa decisão de desenho: nível
município pesa 4,5× mais que nível escola.

**Uma meta de política pública é um preditor melhor que o modelo.** A meta
do PDE, aplicada uniformemente a todos os alunos do município, sozinha —
sem nenhuma feature de aluno — supera o modelo completo de 12 features. Não
é uma limitação do algoritmo (testamos três, todos convergem para o mesmo
teto); é limitação do que os dados atualmente disponíveis conseguem
diferenciar dentro de um mesmo município.

### 8.4 A reformulação do alvo, e o achado de maior valor do projeto

Com o modelo aluno-nível reprovado, testamos se o problema era o **alvo**, não
o algoritmo — atacando a única das cinco perguntas de negócio do enunciado
ainda sem resposta: *"como prever municípios que podem não atingir metas
futuras?"*. Código: `src/modeling/03_experimento_municipio_meta.py`.

Antes, três hipóteses de "faltava dado" foram **medidas e fechadas**:

| Hipótese | Resultado |
|---|---|
| Existe questionário socioeconômico do aluno? | Sem evidência (5ª tentativa de acesso ao INEP; todas as fontes descrevem só a prova) |
| Enriquecer com Censo Escolar | **0% de cobertura** — nosso `id_escola` é sequencial (60000002–60042811); o `CO_ENTIDADE` oficial usa prefixo de UF (11–53). É identificador sintético, sem tabela de correspondência |
| Sobra sinal de aluno depois do baseline? | **−0,0318**, IC95% [−0,0374, −0,0261] — dar o baseline ao modelo *como feature* e somar as features de aluno **piora** o resultado (`src/evaluation/03_teste_residuo.py`) |

No grão município (5.232 casos, alvo `taxa_2024 < meta_2024`), o modelo
**passou** no teste de falsificação — AUC 0,7709 contra 0,7294 de um lookup de
UF, IC95% [+0,0320, +0,0516]. Mas a ablação mostrou que o ganho era quase todo
da **UF** (+0,21 de AUC ao adicioná-la), e o k-fold aleatório deixa municípios
do mesmo estado no treino e no teste — o modelo aprendia a taxa do estado
olhando vizinhos do mesmo ano.

**Leave-One-UF-Out (a UF de teste nunca vista no treino): AUC 0,4800** —
abaixo do acaso. O mesmo padrão que derrubou o modelo aluno-nível, um nível de
agregação acima.

**Por quê:** as avaliações do CNCA são aplicadas **pelos estados**. RS caiu 20
pontos percentuais em um ano (73,1 → 53,1; 90,5% dos municípios falharam a
meta), enquanto MG subiu 12,3 (62,8 → 75,1; 20,5% falharam). A correlação entre
variação da UF e taxa de falha é **−0,651**, mais forte que a correlação com o
nível de 2023 (−0,431) — não é artefato mecânico da fórmula da meta, é o choque
do ano. Uma variação de ±20pp em um ano não é aprendizado real: é mudança de
régua na aplicação da prova.

**O que funciona:** rodando o modelo dentro de cada UF (17 estados com n≥100),
AUC **0,6496** contra **0,4015** do baseline intuitivo, vencendo em **14 de 17**
UFs. E o baseline intuitivo — *"quem estava pior em 2023 falha mais"* — é
**ativamente errado** (abaixo do acaso): por regressão à média e pela meta
progressiva do PDE, municípios com taxa baixa melhoram mais e batem a meta com
mais frequência.

## 9. Limitações do projeto

⚠️ **A limitação mais consequente: comparação entre estados não é válida.**
Como cada estado aplica sua própria avaliação e a variação estadual entre anos
chega a ±20pp, ordenar municípios de UFs diferentes na mesma escala compara
réguas distintas. Um gestor que lesse esse ranking direcionaria recursos para
municípios gaúchos ("90% falharam a meta") quando parte substancial do efeito
é como o estado aplicou a prova, não a política municipal. Isso vale inclusive
para os marts `agg_municipio_ranking` e `agg_priorizacao` da nossa própria
Fase 2 — não invalida a engenharia daqueles marts, invalida a **leitura
nacional** que se faz em cima deles, e por isso está registrado aqui em vez de
omitido.

- **O modelo aluno-nível não supera o melhor baseline municipal** — ver §7.
  Segunda limitação mais importante para qualquer decisão de uso.
- **`peso_aluno`** (peso amostral) foi excluído como feature — seu uso
  correto é exclusivamente estatístico, para ponderar cálculos de
  população, nunca como entrada de modelo.
- **`caderno`** carrega um resíduo de influência (11,6%) sem explicação
  causal confirmada. Três tentativas de acessar o dicionário oficial de
  valores do INEP (portal restrito, basedosdados.org sem essa informação,
  PDF técnico com erro de certificado) não resolveram a categoria 12 —
  resolvida por análise de dados própria (crosstab), não por documentação
  externa.
- **Sem dado de 2025** — o modelo nunca foi validado contra o ano de uso
  real. Decisão registrada em [`ADR-0002`](../../docs/wayfinder/tech_challenge_fase3/adr/0002-modelo-final-validacao-temporal-e-tratamento-caderno.md):
  documentar como limitação, não construir infraestrutura de monitoramento
  que o enunciado não exige.
- **SICONFI** (`gasto_por_habitante_educacao`, ~9 mil requisições a API
  pública) não foi buscado — o teste barato (população + meta) já mostrou
  que o problema é o modelo tentar ser um baseline municipal, não falta de
  mais uma feature municipal.
- **Reprodutibilidade de versão**: scikit-learn 1.8→1.9 mudou o Recall do
  baseline em ~1,6pp com o mesmo seed e dado — `requirements.txt` pinado
  mitiga, mas não elimina esse tipo de variação entre ambientes.

## 10. Aplicação prática para políticas públicas

**Duas recomendações, ambas sustentadas por evidência estatística com
intervalo de confiança:**

1. **Para busca ativa de alunos**, usar a **meta do PDE do município** como
   critério de priorização, não um modelo aluno-nível. Mais simples de
   explicar, mais barata de manter (nenhum pipeline de ML em produção), e
   estatisticamente mais eficaz com os dados disponíveis.
2. **Para priorização entre municípios**, comparar **dentro do estado**, nunca
   entre estados — e usar o modelo intra-UF (AUC 0,6496), porque a intuição
   corrente ("priorizar quem estava pior") tem desempenho **abaixo do acaso**
   neste alvo.

Isso não diminui o valor da Fase 3 — o projeto define um critério de sucesso
antes de medir, executa o teste, desconfia do próprio resultado quando ele
parece bom demais, corrige a régua e reporta o resultado desfavorável com
significância. Essa é a forma madura de responder "os modelos poderiam apoiar
políticas públicas educacionais?": às vezes a resposta certa é *"não desse
jeito, e aqui está a prova — mas deste outro jeito, sim."*

## 11. Possíveis evoluções futuras

- **Feature verdadeiramente individual do aluno** — depois de remover
  vazamento, nenhuma feature restante descreve o aluno em si (todas são
  metadado administrativo ou agregado de município/escola). O teste de resíduo
  confirmou que não há sinal incremental; sem uma variável genuinamente
  individual, é improvável que qualquer modelo supere o baseline municipal.
- **Harmonizar as réguas estaduais** — a maior alavanca analítica identificada.
  Sem um fator de equalização entre avaliações estaduais, comparação nacional
  continua inválida e nenhum modelo nacional generaliza.
- **Modelo intra-UF por estado**, com dados socioeconômicos municipais
  (SICONFI, Atlas do Desenvolvimento Humano) — é onde há sinal legítimo e
  ainda não exploramos features além das quatro atuais.
- **Resolver `caderno=12`** com acesso ao dicionário oficial do INEP — hoje o
  resíduo de 11,6% de influência fica sem explicação causal.
- **Re-executar com dado de 2025** para checar se o efeito de régua estadual
  persiste ou se foi específico do ciclo 2024.

---

## Estrutura do repositório

```
tech-challenge-fase3-alfabetizacao/
├── data/                    Snapshots processados (território local, etc.)
├── docs/
│   └── HANDOFF_RENAN.md     Documento vivo — narrativa completa capítulo a capítulo
├── images/                  Gráficos SHAP
├── reports/                 EDA, dicionário, métricas, proveniência
├── src/
│   ├── preprocessing/       Extração, guarda de leakage, pipeline, território
│   ├── modeling/            Baseline, tournament
│   └── evaluation/          SHAP, teste de falsificação
├── requirements.txt
└── README.md                Este arquivo
```

## Reprodutibilidade

```bash
pip install -r requirements.txt
python src/preprocessing/03_guarda_leakage.py       # gate: falha se houver vazamento
python src/preprocessing/01_eda_alunos.py --dataset snapshot
python src/modeling/02_tournament_modelos.py --temporal
python src/evaluation/01_shap_interpretabilidade.py
python src/evaluation/02_teste_falsificacao.py      # o teste que decide o projeto
```

Decisões técnicas completas, incluindo a sequência de correções (vazamentos
achados, escala corrigida, régua de teste recalibrada), em
[`docs/HANDOFF_RENAN.md`](docs/HANDOFF_RENAN.md) e nos ADRs em
[`docs/wayfinder/tech_challenge_fase3/adr/`](../../docs/wayfinder/tech_challenge_fase3/adr/)
(migração para `docs/adr/` deste repositório pendente — ver Cap. 15 do
documento vivo).
