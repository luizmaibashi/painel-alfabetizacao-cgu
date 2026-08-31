# Painel de Priorização Municipal de Alfabetização — Reúso de Dados Abertos

> **[Abrir o painel ao vivo →](https://luizmaibashi.github.io/painel-alfabetizacao-cgu/)**
> Ferramenta gratuita e de código aberto que cruza dados públicos federais
> (INEP + IBGE) para dizer a um gestor municipal, estado por estado, se um
> modelo estatístico consegue apontar quais municípios correm risco de não
> atingir a meta de alfabetização infantil no próximo ciclo — **e onde a
> resposta honesta é "os dados não sustentam essa afirmação ali"**.

## Por que isto é reúso de dados abertos, e por que importa

A alfabetização infantil (Indicador Criança Alfabetizada, INEP) é medida e
publicada oficialmente todo ano, por município. O dado existe e é público —
mas chega ao gestor como uma tabela crua de milhares de linhas, sem dizer
**onde o histórico permite antecipar risco** e onde não permite. Este
projeto cruza três fontes públicas para transformar essa tabela em uma
ferramenta de priorização, com o cuidado adicional de **nunca afirmar mais
do que os dados sustentam**:

| Fonte pública | O que traz | Onde |
|---|---|---|
| **INEP — Resultados da Avaliação da Alfabetização** | Taxas municipais de alfabetização e metas do PDE, 2023–2026 | [gov.br/inep — resultados 2025](https://www.gov.br/inep/pt-br/areas-de-atuacao/avaliacao-e-exames-educacionais/avaliacao-da-alfabetizacao/resultados/2025) |
| **IBGE — SIDRA (API pública)** | População municipal | [sidra.ibge.gov.br](https://sidra.ibge.gov.br/) |
| **INEP — Censo Escolar 2023** | Infraestrutura escolar por município (testado como enriquecimento) | [gov.br/inep — microdados](https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/microdados/censo-escolar) |

Nenhuma dessas fontes exige credencial paga ou acesso restrito. O download
da planilha de resultados é verificado por hash (SHA-256, registrado em
[`reports/proveniencia_ica_2025.md`](reports/proveniencia_ica_2025.md)) —
qualquer pessoa pode refazer o mesmo download e confirmar que os dados que
alimentam o painel são exatamente os publicados pelo INEP.

**Relevância e impacto potencial.** O painel serve à decisão concreta de um
gestor de secretaria estadual ou municipal de educação: em qual município
investir busca ativa e acompanhamento pedagógico primeiro, dado orçamento
limitado. Ele evita dois erros de uso de dado público — (1) comparar
municípios de estados diferentes numa régua nacional única, quando cada
estado aplica sua própria prova (efeito medido, não hipotético — ver
`§9`), e (2) apresentar um "score de IA" onde o histórico simplesmente não
sustenta a afirmação, em vez de dizer isso abertamente.

**Benefício para a sociedade.** Uso responsável de dado público para apoiar
uma política de primeira infância (alfabetização até o 2º ano do
fundamental é meta nacional do PDE) sem custo de licença, sem coleta de
dado pessoal identificável, e com o código de geração do painel público —
qualquer secretaria de educação pode adaptar o mesmo pipeline para seu
próprio estado.

## O que este projeto entrega

| # | Entregável | Resultado |
|---|---|---|
| 1 | **Painel de priorização municipal** (`reports/painel_intra_uf.html`, [ao vivo aqui](https://luizmaibashi.github.io/painel-alfabetizacao-cgu/)) | Testado contra o resultado real de 2025 em **5.285 municípios de 23 estados**: o modelo acerta **65,3%** das vezes contra **45,2%** de um método simples de comparação — ganho de **16,4 pontos percentuais**. A decisão é por estado, não nacional: o modelo vence em 14 estados, o método simples vence em 1 (Ceará) e em 8 o painel se abstém — mostra o diagnóstico, não esconde a incerteza atrás de uma média nacional |
| 2 | **A descoberta de que não existe uma regra nacional única** | "Quem estava melhor em 2023 falha mais a meta no ano seguinte" vale em 16 estados; o **oposto** vale em 7. Dois mecanismos diferentes por trás disso — por isso um modelo nacional único não funciona, e o painel é sempre por estado |
| 3 | **Advertência de validade sobre comparação entre estados** | Um ranking nacional de municípios compararia réguas de avaliação distintas — o painel é dividido por estado por causa deste achado, de propósito |
| 4 | **Modelo por aluno** (exigência da fase acadêmica de origem, mantido por transparência) | Testado com o mesmo rigor e **reprovado no próprio critério que definimos antes de testar**: 60,5% de acerto contra 63,3% de aplicar a meta oficial a todos os alunos do município. Resultado negativo, medido e mantido no relatório — evidência do padrão de honestidade que sustenta o painel acima |

A narrativa curta: **testamos onde os dados permitiam testar, dissemos com
rigor onde não funcionava, e entregamos, sem exagero, onde funcionava.**

### As 5 perguntas de negócio da fase acadêmica de origem

| Pergunta | Onde está respondida |
|---|---|
| Quais fatores mais impactam a alfabetização? | §7.1 (SHAP) |
| Quais municípios apresentam maior risco educacional? | Entregável 3 — modelo intra-UF + painel |
| **Quais regiões possuem padrões semelhantes?** | **Herdada da Fase 2**: `agg_vulnerabilidade_ml` (K-Means, mart em produção) já responde isso a nível município. Não foi refeita nesta fase — a Fase 3 focou no eixo aluno-nível que a Fase 2 não cobria (§1); reutilizar o mart existente é a resposta honesta, não construir um clustering novo para dizer a mesma coisa |
| Como prever municípios que podem não atingir metas futuras? | Entregável 2 — a resposta que a Fase 3 de fato desenvolveu |
| Quais variáveis possuem maior influência nos modelos? | §7.1 (SHAP) |

## Origem e licença

Este repositório é um recorte, com narrativa reorientada, do projeto
[**Tech Challenge Fase 3 — Predição e Inteligência Analítica para
Alfabetização**](https://github.com/luizmaibashi/tech-challenge-fase3-alfabetizacao)
(Pós-Tech em Data Analytics, FIAP). O trabalho técnico — modelagem, testes
estatísticos, ADRs — é o mesmo; o que muda aqui é o produto em destaque (o
painel, não o modelo aluno-nível) e o público-alvo (gestor público, não
avaliador acadêmico). Enviado ao **2º Concurso de Reúso de Dados Abertos da
CGU**. Código sob licença [MIT](LICENSE) — reúso e adaptação livres, inclusive
por outras secretarias de educação.

Caso de reúso cadastrado no Portal Brasileiro de Dados Abertos:
`[link a preencher após homologação]`.

---

## Como funciona, em linguagem simples

### Primeiro tentamos prever aluno por aluno — e não funcionou

O pedido original (fase acadêmica de origem) era prever, **para cada aluno**,
se ele seria alfabetizado ou não, usando dados disponíveis antes da prova.
Construímos esse modelo com todo o cuidado — removendo qualquer coluna que
"entregasse a resposta de graça" (por exemplo, uma coluna que só existe
quando o aluno faltou à prova, o que já revela o resultado por outro
caminho) — e testamos contra a régua mais simples possível: **aplicar a
meta oficial do governo para aquele município a todos os alunos dele,
igualzinho, sem olhar nada do aluno individualmente.**

O modelo perdeu dessa régua simples. Não por pouco, e não por azar: perdeu
de forma consistente, com três algoritmos diferentes, com folga estatística
segura. A causa, uma vez investigada, foi simples de entender: **os dados
disponíveis não descrevem o aluno — descrevem o município dele.** Depois de
tirar tudo que era "cola", o que sobra sobre cada aluno é, na prática, uma
cópia do dado do município onde ele estuda. E um número que já existe de
graça (a meta oficial) prevê isso tão bem quanto, ou melhor, do que um
modelo caro de treinar e manter.

**Essa é uma vitória para o gestor, não uma derrota do projeto.** Significa
que não é preciso pagar por infraestrutura de IA para saber quais alunos
priorizar — a meta oficial, que o governo já publica, já cumpre esse papel.

### O que funciona: priorizar município, dentro do próprio estado

Com o aluno descartado, testamos o mesmo tipo de pergunta um nível acima:
**dá para prever quais municípios vão ficar abaixo da meta no próximo
ano?** Aqui, sim, havia sinal real — mas só quando comparamos municípios
**do mesmo estado entre si**. Cada estado brasileiro aplica sua própria
prova de alfabetização, com sua própria dificuldade a cada ano — comparar
municípios de estados diferentes na mesma régua seria como comparar notas
de provas diferentes como se fossem a mesma prova.

Para provar que o modelo funciona de verdade — e não é sorte de ajuste —
nós o "congelamos" com dados até 2024 e o usamos para prever 2025 **sem
deixá-lo ver esse resultado antes**. Só depois comparamos a previsão com o
que de fato aconteceu. É o teste mais rigoroso disponível: prever o futuro
de verdade, não reencontrar um padrão já visto.

### Os números, traduzidos

| Pergunta | Resposta |
|---|---|
| Em quantos municípios o modelo foi testado de verdade (não simulado)? | **5.285**, em 23 estados |
| Em quantos estados o modelo provou apontar risco melhor que um método simples e gratuito? | **14 de 23** |
| Em quantos estados o método simples continua sendo a melhor escolha? | **1** (Ceará) |
| Em quantos estados os dados não são suficientes para afirmar qualquer coisa com segurança? | **8** — e o painel avisa isso abertamente, em vez de arriscar um palpite |
| Se eu sortear dois municípios ao acaso — um que ficou abaixo da meta, outro que não —, qual a chance de o modelo apontar corretamente qual dos dois estava em mais risco? | **65,3%**, contra **45,2%** de um método simples de comparação (sortear ao acaso daria 50%) |
| E o modelo por aluno, o que a fase acadêmica de origem pedia? | **Perdeu** do método simples (60,5% de acerto contra 63,3%) — resultado negativo, medido e mantido no relatório, não escondido |

### Limitações, sem rodeio

- **Não compara municípios de estados diferentes, de propósito.** Cada
  estado aplica sua própria prova; a variação de um ano para outro dentro
  do mesmo estado já chega a 20 pontos percentuais. Colocar municípios de
  estados diferentes na mesma lista seria enganoso — por isso o painel é
  sempre filtrado por estado, sem ranking nacional.
- **Não serve para decisão sobre um aluno específico.** É uma ferramenta de
  priorização municipal, para orientar onde alocar apoio pedagógico e
  orçamento — nunca para rotular ou negar direito a uma criança.
- **Só existe um "teste no mundo real" completo até agora** (previsão de
  2025, conferida contra o resultado real de 2025). Com o tempo, cada novo
  ciclo aumenta a confiança — ou revela se algo precisa mudar.
- **Nos 8 estados sem sinal suficiente, o painel prefere dizer "não
  sabemos" a inventar uma resposta.** Isso é decisão de desenho, não falha:
  uma ferramenta pública que finge certeza onde não há é mais perigosa do
  que uma que admite o limite.

### O que fazer com isso — recomendação prática

1. **Para priorizar alunos dentro de uma escola**, use a meta oficial do
   PDE do município, aplicada a todos os alunos dele — é mais simples,
   mais barata (nenhum modelo em produção) e, pelos nossos testes, tão ou
   mais eficaz que um modelo de IA.
2. **Para priorizar municípios dentro do seu estado**, use o painel — mas
   só onde ele mostra o "ranking do modelo" (14 estados). Onde mostra
   "método simples" (Ceará) ou "sem recomendação" (8 estados), siga o que
   o painel indica: nunca compare municípios de estados diferentes numa
   régua única.

---

<details>
<summary><strong>Detalhamento técnico completo</strong> — metodologia, testes estatísticos e decisões registradas em ADR, para quem quer reproduzir ou avaliar o rigor da análise (clique para expandir)</summary>

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

**Objetivo primário (o que o enunciado pede).** Desenvolver um modelo
supervisionado que prevê se um aluno será `alfabetizado` (Sim/Não) — corte
oficial de 743 pontos na escala do exame — usando variáveis educacionais,
territoriais e socioeconômicas disponíveis **antes** do resultado do próprio
aluno, para alimentar ação de busca ativa na ponta escolar.

**Critério de sucesso definido antes de qualquer treino** ([`ADR-0001`](docs/adr/0001-pipeline-sklearn-snapshot-e-politica-leakage.md) §5):
o modelo aluno-nível só se justifica se **superar** o baseline trivial de
aplicar um risco já calculado por município (Fase 2) igualmente a todos os
alunos daquele município. Um modelo que não bate esse baseline está apenas
reproduzindo, com mais complexidade e mais risco de erro, uma informação
que já existia pronta. Essa é a pergunta que decide o projeto — não "o
modelo prevê bem?", mas "o modelo prevê melhor do que eu não fazer nada de
novo?".

**Objetivo secundário (derivado do resultado do primário).** Quando o modelo
aluno-nível reprovou e o teste de resíduo mostrou que não há sinal individual
a extrair (§8), a pergunta passou a ser se o problema era o **alvo**, não o
algoritmo. Daí o segundo objetivo: prever, no grão em que o dado nasce,
**quais municípios não atingirão a meta do PDE no ciclo seguinte** — que é
literalmente a pergunta de negócio nº 4 do enunciado, a única das cinco que
seguia sem resposta.

Os dois objetivos usam o mesmo rigor e o mesmo critério: nenhum modelo entra
como entregável sem superar um baseline trivial explícito, com intervalo de
confiança.

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
[`ADR-0003`](docs/adr/0003-gold-vs-silver-fonte-de-dados.md).

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
8. **Teste de resíduo** (`src/evaluation/03_teste_residuo.py`) — dá o baseline
   ao modelo *como feature* e mede o incremento. É o método correto para
   "sobra sinal individual?", e a resposta foi não (§8).

### Pipeline do segundo entregável — priorização municipal intra-UF

9. **Experimento de reformulação** (`src/modeling/03_experimento_municipio_meta.py`)
   — 5 etapas em ordem deliberada: tournament binário vs contínuo, ablação,
   falsificação contra lookup de UF, **Leave-One-UF-Out** e modelo dentro de
   cada UF. A etapa 4 é a que decide: as três primeiras produzem um resultado
   que parece vitória (AUC 0,77) e a quarta mostra que ela dependia de
   informação contemporânea do estado.
10. **Modelo produtizado** (`src/modeling/04_ranking_intra_uf.py`) — um modelo
    por UF, predições **out-of-fold** (cada município pontuado por um modelo
    que não o viu no treino), nome do município via API pública do IBGE.
    Saída: `reports/ranking_intra_uf.{json,csv}`, 5.216 municípios.
11. **Painel** (`src/visualization/01_gerar_painel_intra_uf.py`) — gera
    `reports/painel_intra_uf.html`, autocontido, particionado por UF, a partir
    de `reports/ranking_prospectivo_2025.json` (saída do backtest, passo 12).
    Cada UF exibe um de três modos, conforme o veredito prospectivo: ranking do
    modelo (14 UFs), regra simples (CE) ou abstenção diagnóstica (8 UFs).
12. **Backtest prospectivo** (`src/evaluation/05_backtest_prospectivo_2025.py`)
    — congela o modelo em 2023→2024, testa em 2024→2025 sem tuning nem alvo de
    2025. Grava `reports/backtest_prospectivo_2025.json` (métricas) e
    `reports/ranking_prospectivo_2025.json` (listas municipais + contrato de
    uso + rastreabilidade da fonte).

### Tratamento de data leakage

Cinco colunas foram identificadas como vazamento do mesmo evento (aluno
faltou à prova) por caminhos diferentes — três por **valor**
(`proficiencia`, `presenca`, `preenchimento_caderno`), duas por **ausência
de valor** (`peso_aluno`, cuja nulidade coincidia 100% com faltosos;
`caderno=12`, que tinha 79,7% de ausentes disfarçados de categoria de
risco). Todas as cinco estão fora do modelo. Detalhe no diário de bordo interno (não publicado), Caps. 9 e 11.

### Validação e generalização

`StratifiedKFold(5)` faz o papel do conjunto de validação do enunciado,
sempre dentro do treino; o conjunto de teste é tocado uma única vez, depois
do tuning de hiperparâmetro escolhido — usar o teste para tuning vazaria
generalização de forma silenciosa. Split temporal (2023→2024) roda em
paralelo como segunda checagem, mais próxima do uso real. `requirements.txt`
com versões pinadas garante replicabilidade — o próprio scikit-learn 1.8→1.9
mudou o Recall do baseline em 1,6 pontos percentuais com o mesmo seed.

## 5. Escolha do algoritmo

### 5.1 Modelo aluno-nível

Três candidatos comparados no mesmo split e mesmo k-fold: Regressão
Logística, Random Forest e XGBoost.

| Modelo | Recall | Precision | F1 | ROC-AUC | gap treino-val |
|---|---|---|---|---|---|
| Regressão Logística | 0,593 | 0,538 | 0,564 | 0,676 | **+0,001** |
| **Random Forest** | **0,648** | 0,529 | **0,582** | 0,676 | +0,006 |
| XGBoost | 0,615 | **0,541** | 0,575 | **0,683** | +0,030 |

*(48.055 alunos avaliados, população oficial, split aleatório 80/20 **com**
território. Fonte: `reports/metrics_tournament.json`.)*

**Nenhum candidato vence em tudo, e isso é o achado.** Pela métrica de decisão
declarada — Recall da classe "Não", ADR-0001 §5 — quem lidera é o **Random
Forest** (0,648). O XGBoost leva ROC-AUC e Precision, e tem o **maior gap
treino-validação dos três** (+0,030, cinco vezes o do RF), sinal de que ajusta
mais o treino do que os outros.

E a Regressão Logística, com apenas 4 hiperparâmetros e uma fronteira linear,
**empata em ROC-AUC com os dois ensembles**. Isso é diagnóstico, não
decepção: se um modelo linear alcança gradient boosting, não existe estrutura
complexa a aprender — o sinal disponível é essencialmente um número por
município, aplicado a todos os seus alunos. É a mesma conclusão da §7.2, vista
pelo lado do algoritmo.

> **Correção de 2026-08-29.** Esta tabela reportava `0,533 / 0,537 / 0,554` de
> ROC-AUC e a frase *"XGBoost lidera nas três métricas de decisão"*. Os números
> eram de uma execução anterior à integração de território, e a liderança
> declarada contradizia o próprio artefato — `metrics_tournament.json` grava
> `maior_recall_no_teste: "random_forest"`. A leitura antiga também chamava a
> Logística de "quase cega (0,533)" e concluía que as features não tinham
> relação linear com o alvo; com 0,676 medido, a conclusão se inverte.

**A escolha de algoritmo não decide o veredito.** Testados os três no split
temporal contra o baseline municipal, nenhum o supera — ver §7.3.

**Métrica de decisão**: Recall da classe "Não" (aluno em risco). Falso
negativo — aluno em risco não identificado — é o erro caro para busca
ativa; Precision entra como contrapeso para não degenerar em marcar todo
mundo como risco.

**Nota de 2026-08-22 (recomeço pedagógico):** Os scripts de avaliação
(`01_shap_interpretabilidade.py`, `02_teste_falsificacao.py`,
`03_teste_residuo.py`) agora usam XGBoost com hiperparâmetros forte
(800 árvores, depth 8, lambda 1.0), a mesma metodologia canônica (split
temporal 2023/2024, baseline municipal, IC bootstrap) validada pela
investigação registrada em [`ADR-0006`](docs/adr/0006-ceiling-analysis-como-gate-pre-treino.md).
O veredito da ADR-0001 §5 mantém-se: modelo aluno-nível não supera o baseline,
agora confirmado com modelo mais robusto (**AUC 0,6047 vs 0,6331**, IC95%
[-0,0342, -0,0228]).

> **Correção de 2026-08-25.** Esta linha reportava `AUC 0,6026, IC95%
> [-0,0364, -0,0248]`. Aquele número **não era reprodutível**: com
> `tree_method="hist"` + `n_jobs=-1`, o AUC variava entre **0,6025 e 0,6061**
> apenas com a contagem de threads disponível na máquina (mesma seed, mesmo
> dado, mesmo código) — a redução paralela do histograma altera a ordem de
> soma em ponto flutuante. `n_jobs=1` foi fixado nos scripts de avaliação e o
> valor passou a ser estável em 0,6047. **O veredito não muda em nenhum ponto
> da faixa** — o modelo perde do baseline 0,6331 com folga em todos eles.
> Detalhe em [`ADR-0006 §7.1`](docs/adr/0006-ceiling-analysis-como-gate-pre-treino.md).

### 5.2 Modelo municipal intra-UF

Duas decisões separadas aqui — **formulação do alvo** e **algoritmo**.

**Formulação**: binária (`atinge a meta? sim/não`) vs contínua (gap em pontos
percentuais até a meta). Empate técnico — melhor binária 0,7738 contra melhor
contínua 0,7673 de AUC equivalente, com R² de 0,36 no contínuo. Escolhemos
**binária**, não pela métrica (que empata), mas pelo uso: a decisão do gestor
é "entra ou não na lista de prioridade", e um score de probabilidade é mais
direto de ordenar e explicar que uma magnitude em pp.

**Algoritmo**: Random Forest, `n_estimators=200`, `max_depth=6`. Com quatro
features e amostras pequenas por estado (n de 48 a 801), profundidade curta e
ensemble moderado importam mais que capacidade — XGBoost não ganhou nada aqui,
e Logística não capta a não-linearidade da regressão à média que é justamente o
sinal do problema.

**Predições out-of-fold, sempre.** No produto, cada município é pontuado por
um modelo que não o viu no treino. Um ranking gerado com predições in-sample
pareceria melhor e enganaria quem o usasse.

### 5.3 Técnicas de feature encoding comparadas

O enunciado (p.5) pede "técnicas de feature **encoding**", no plural. Três
foram aplicadas e comparadas no split temporal, contra o mesmo baseline
(`src/modeling/05_comparar_encodings.py` →
[`comparacao_encodings.json`](reports/comparacao_encodings.json)).

**Categóricas atuais** (`caderno` 12 valores, `rede` 2, `sigla_uf` 27):

| Encoding | ROC-AUC | Colunas geradas | vs baseline 0,6331 |
|---|---|---|---|
| OneHot | 0,6047 | 36 | −0,0284 [−0,0342, −0,0228] |
| **Target** (cross-fit `cv=5`) | **0,6096** | **10** | −0,0235 [−0,0289, −0,0181] |
| Frequency | 0,6032 | 10 | −0,0299 [−0,0357, −0,0241] |

**A diferença de AUC é desprezível — e era a previsão, registrada antes de
rodar.** Encoding não cria informação: é a mesma variável escrita de outro
jeito. O ganho real do Target está na outra coluna: **o mesmo resultado com 10
features em vez de 36**. Esse é o motivo de existir da técnica — controlar
dimensionalidade em categórica de cardinalidade média —, não separação melhor.

**Alta cardinalidade** — `id_municipio`, 4.478 valores, onde OneHot é inviável
e Target/Frequency justificam sua existência:

| Encoding | ROC-AUC | Ganho ao adicionar `id_municipio` |
|---|---|---|
| Target | 0,6123 | **+0,0027** |
| Frequency | 0,5915 | −0,0117 |

Dar ao modelo a identidade dos 4.478 municípios rende **+0,003**. A identidade
municipal é **redundante**: o sinal do município já entrava por `meta do PDE` e
`população`. É a tese do projeto confirmada por um quarto caminho independente
— depois do SHAP (§7.1), do teste de resíduo (§8) e do teste de robustez a
algoritmo (§7.3).

Frequency **piora** com `id_municipio` porque a frequência de um município é
quantos alunos foram amostrados nele — proxy ruidoso de população, variável que
o modelo já tem de forma direta.

**Contenção de vazamento.** Target encoding sem fold interno vaza o alvo — é o
modo de falha clássico da técnica. Aqui o `TargetEncoder` roda com `cv=5`
(cada linha de treino é codificada por folds que não a contêm), `fit` só no
treino, e o split é temporal. O critério de suspeita foi declarado antes de
rodar — *"melhora relevante é suspeita de vazamento antes de ser descoberta"* —
e **não disparou**: a maior variação foi +0,005, ordem de grandeza incompatível
com vazamento, que levaria o AUC para perto de 1,0.

**Nenhum encoding supera o baseline.** Os cinco resultados seguem
significativamente abaixo de 0,6331.

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

Duas execuções, porque **o desenho do split muda o modelo** (ver §7.4). A
coluna que vale para interpretar o veredito é a **temporal**, porque é o
desenho que o teste de falsificação usa.

| Bloco de features | Split temporal *(alinhado ao veredito)* | Split aleatório |
|---|---|---|
| **Município** — `sigla_uf` 46,5%, meta do PDE 18,0%, flag de imputação 7,1%, população 6,1%, absenteísmo t-1 3,7%, contador 0,0% | **81,3%** | 85,3% |
| Aluno/turma — `caderno` 9,1%, `rede` 2,1% | 11,2% | 10,0% |
| **Escola** — absenteísmo t-1 7,5%, contador 0,0%, flag 0,0% | **7,5%** | 4,7% |

*Fontes:
[`shap_interpretabilidade_temporal.json`](reports/shap_interpretabilidade_temporal.json)
e [`shap_interpretabilidade.json`](reports/shap_interpretabilidade.json) —
XGBoost forte (800 árvores, depth 8, `n_jobs=1`). Métrica: |SHAP| médio
normalizado. Mede o quanto a variável move a predição, não se o efeito é bom
ou ruim.*

**Município domina nos dois desenhos** — 81,3% e 85,3%. É o número que
sustenta o veredito da §7.2: o modelo não lê o aluno nem a escola dele, lê o
município. E a meta do PDE, sozinha, é exatamente o baseline que vence o
modelo inteiro logo abaixo.

**Quatro features valem exatamente 0,0% no split temporal**:
`n_alunos_hist_municipio_t1` (6,3% no aleatório), `possui_hist_municipio_t1`
(2,2%), `n_alunos_hist_escola_t1` (1,5%) e `possui_hist_escola_t1` (1,4%) —
11,4% de influência que simplesmente evapora. Não é ruído: são precisamente as
features que o ano de treino não tem (§7.4). Em compensação `sigla_uf` salta
de 20,4% para **46,5%**, absorvendo o que o histórico deixou de explicar.

> **Correção de 2026-08-29.** Esta seção reportava `60,9% / 13,3% / 11,6% /
> 14,2%`, de um modelo superado (400 árvores, depth 3, antes de território — os
> blocos nem incluíam meta do PDE, `sigla_uf` e população). O diário de bordo interno (não publicado), Cap. 10.3, carrega um terceiro par
> (`45,1% / 9,9%`), de outra execução intermediária.
>
> Na mesma revisão descobriu-se que esta seção e a §7.2 descreviam **modelos
> diferentes**: o SHAP rodava em split aleatório e o veredito em split
> temporal. Daí a coluna dupla acima. A conclusão — município domina — é
> robusta a todas as leituras.

### 7.2 O teste de falsificação — o resultado que decide o projeto

Território (população, meta do PDE, UF) foi integrado **sem depender de
credencial GCP** — o dado é público (API do IBGE + arquivo de metas já em
disco). Isso mudou o modelo de aleatório para algo com sinal real:

| Abordagem | ROC-AUC |
|---|---|
| Referência aleatória | 0,5039 |
| Baseline: taxa de não-alfabetização municipal t-1 | 0,5816 |
| **Modelo aluno-nível completo (12 features)** | **0,6047** |
| **Baseline: meta do PDE, aplicada uniformemente a todos os alunos do município** | **0,6331** |

Diferença modelo − melhor baseline: **−0,0284**, IC95% bootstrap pareado
**[−0,0342, −0,0228]** (n = 24.505, 2.000 reamostragens) — inteiramente
negativo. Não é empate: é derrota com significância. O modelo perde também em
**5 de 5** orçamentos de busca ativa testados (5% a 50% dos alunos).

*Números de [`reports/teste_falsificacao.json`](reports/teste_falsificacao.json),
regenerado em 2026-08-25 com `n_jobs=1` (ver ADR-0007). A ordem da tabela é
proposital: o modelo fica **entre** o baseline fraco e o forte.*

**Isso não foi a primeira medição.** Uma versão anterior do teste, usando a
taxa bruta municipal como baseline, tinha *passado* (0,6013 vs 0,5816,
IC95% [+0,0129, +0,0263] — valores medidos à época, antes da correção de
determinismo do ADR-0007). Investigar de onde vinha essa vitória mostrou que
ela dependia quase inteiramente de uma única feature — a meta do PDE — que
correlaciona 0,979 com a taxa de alfabetização do próprio ano. Ou seja: a
meta *é* um número município tão forte que comparar o modelo contra um
baseline mais fraco não provava nada. Corrigimos o teste para usar **o
melhor baseline disponível**, não o primeiro que passasse — e o veredito
inverteu. Ver o diário de bordo interno (não publicado), Cap. 14, para
a sequência completa, incluindo o bug de leitura do intervalo de confiança
que também foi corrigido nesse processo.

### 7.3 O veredito depende do algoritmo escolhido? (não)

A objeção óbvia contra a §7.2 é *"vocês perderam porque escolheram o algoritmo
errado"*. `src/evaluation/04_robustez_algoritmo.py` responde rodando os **três
candidatos do torneio** no mesmo split temporal, com o mesmo baseline
(reusado por import do teste canônico, não recalculado — ver ADR-0005).

São 3 comparações informando uma decisão, então o veredito usa intervalo
**corrigido por Bonferroni** (α 0,05/3 → IC de 98,33%):

| Candidato | ROC-AUC | Diferença vs baseline 0,6331 | IC 98,33% | Veredito |
|---|---|---|---|---|
| XGBoost (canônico) | 0,6047 | −0,0284 | [−0,0354, −0,0217] | **perde** com significância |
| Random Forest | 0,6322 | −0,0009 | [−0,0042, +0,0024] | equivalente ao baseline |
| Regressão Logística | 0,6325 | −0,0006 | [−0,0034, +0,0021] | equivalente ao baseline |

**Nenhum supera o baseline** — a recomendação de negócio não muda: use a meta
do PDE, que é gratuita. Mas a *magnitude* da derrota era artefato do XGBoost:
−0,0284 contra −0,0009 do Random Forest, ~30× de diferença.

**"Equivalente" aqui é afirmação forte, não desculpa.** O IC do Random Forest
tem largura 0,0066 e está inteiramente contido numa faixa desprezível em torno
de zero — isso *limita* a diferença, não apenas deixa de detectá-la. É o
oposto das 17 UFs inconclusivas do ranking intra-UF (§8), onde os intervalos
passam de 0,3 de largura: lá o dado não sabe, aqui o dado sabe que não há
diferença material. Só se pode chamar de empate quando o intervalo é estreito;
com intervalo largo, o nome honesto é *inconclusivo*.

**E empatar não é "quase lá".** 0,632 contra 0,6331 significa que os dois
modelos **re-derivaram o baseline** — chegaram ao mesmo lugar por um caminho
caro. Um modelo que iguala uma regra de uma linha não justifica existir.

### 7.4 Por que o XGBoost cai, e o que isso revela sobre o dado

Investigando a diferença, apareceu um defeito estrutural que nenhuma EDA do
projeto tinha pego — porque todas rodaram sobre o dataset inteiro, e este só
aparece **dentro do split de treino**.

No ano de treino (2023), as 6 features de histórico t-1 estão assim:

| Feature | 2023 (treino) | 2024 (scoring) |
|---|---|---|
| `n_alunos_hist_escola_t1` | **100% nula** → descartada em silêncio | 78,2% nula |
| `n_alunos_hist_municipio_t1` | **100% nula** → descartada em silêncio | 28,5% nula |
| `possui_hist_escola_t1` | **constante 0** | 0/1 |
| `possui_hist_municipio_t1` | **constante 0** | 0/1 |
| `absenteismo_hist_escola_t1` | **1 valor único por UF** | 3 a 21 por UF |
| `absenteismo_hist_municipio_t1` | **1 valor único por UF** | até 50 por UF |

A causa é aritmética simples: **a base tem 2 anos, e o t-1 de 2023 seria 2022**.
A imputação preenche o absenteísmo pela mediana da UF — o que torna a coluna
uma cópia de `sigla_uf`, já presente no modelo — e não toca nos contadores,
que ficam nulos e são descartados pelo `SimpleImputer` com apenas um
`UserWarning`.

**O modelo declara 12 features e treina com 10.** É *training-serving skew*: o
que ele vê no treino não é o que recebe no scoring.

Isso explica a §7.3 sem precisar de nenhuma hipótese extra. O XGBoost tem
capacidade para ajustar esse mapeamento degenerado de 2023 — e era o candidato
com maior gap treino-validação (+0,030, §5.1). Esse mapeamento não vale em
2024. Random Forest e Logística não se agarram a ele e pousam no que sobra:
o sinal municipal, que **é** o baseline.

**Isto muda o argumento do projeto, para melhor.** A conclusão deixa de ser
"aluno não tem sinal" e passa a ser mais precisa e mais defensável:

> Com 2 anos de dado, **não é possível testar** se o nível aluno tem sinal. O
> desenho de validação temporal consome o único ano de histórico disponível, e
> o que resta para o modelo aprender é exatamente o baseline municipal.

Ou seja: **um terceiro ano não é melhoria incremental, é pré-condição** para a
pergunta do enunciado ser respondível com validação temporal. Detalhe completo
e alternativas descartadas em
[`ADR-0008`](docs/adr/0008-skew-treino-servico-nas-features-de-historico.md).

### 7.5 Leitura honesta

O modelo aprendeu algo real — saiu de ROC-AUC aleatório (0,507, antes do
território) para 0,605. Mas o sinal que ele capturou é fundamentalmente
municipal (SHAP confirma: features de município somam **81,3%** da influência
no split temporal, contra 7,5% das de escola).
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
município pesa **10,8×** mais que nível escola no split temporal
(81,3% contra 7,5%) e 18× no aleatório — ver §7.1.

**A chave de join fecha a questão de enriquecimento externo.** O enunciado
autoriza enriquecer com IBGE, Censo Escolar, FUNDEB, PNAD, Atlas do
Desenvolvimento Humano, Cadastro Único e dados socioeconômicos regionais. Mas
só se enriquece na granularidade de uma chave que seja **real** e
**compartilhada** com a fonte externa — e nesta base:

| Chave | Natureza | Fontes externas que entram |
|---|---|---|
| `id_municipio` | ✅ código IBGE real | todas as municipais |
| `id_escola` | ❌ sequencial sintético | **nenhuma** (0% de cobertura, testado) |
| `id_aluno` | ❌ sintético | nenhuma |

Consequência lógica, não empírica: **todo enriquecimento possível nesta base é
constante dentro do município.** E variável constante dentro do município não
distingue dois alunos do mesmo município — por construção de função, não por
limitação de algoritmo. Ela só distingue municípios, que é exatamente o que a
meta do PDE já faz melhor.

Resumindo em uma frase: **o projeto foi pedido para prever indivíduos a partir
de uma base que nunca observou indivíduos.**

**Uma meta de política pública é um preditor melhor que o modelo.** A meta
do PDE, aplicada uniformemente a todos os alunos do município, sozinha —
sem nenhuma feature de aluno — supera o modelo completo de 12 features.

Não é limitação do algoritmo, e isso agora está **medido**, não afirmado: os
três candidatos rodados no mesmo split temporal contra o mesmo baseline
convergem para o mesmo teto — Random Forest 0,6322 e Regressão Logística
0,6325 contra 0,6331 do baseline, com intervalos que os declaram equivalentes
a ele (§7.3). É limitação do que os dados disponíveis conseguem diferenciar
dentro de um mesmo município.

### A reformulação do alvo, e o achado de maior valor do projeto

Com o modelo aluno-nível reprovado, testamos se o problema era o **alvo**, não
o algoritmo — atacando a única das cinco perguntas de negócio do enunciado
ainda sem resposta: *"como prever municípios que podem não atingir metas
futuras?"*. Código: `src/modeling/03_experimento_municipio_meta.py`.

Antes, três hipóteses de "faltava dado" foram **medidas e fechadas**:

| Hipótese | Resultado |
|---|---|
| Existe questionário socioeconômico do aluno? | Sem evidência (5ª tentativa de acesso ao INEP; todas as fontes descrevem só a prova) |
| Enriquecer com Censo Escolar | **0% de cobertura** — nosso `id_escola` é sequencial (60000002–60042811); o `CO_ENTIDADE` oficial usa prefixo de UF (11–53). É identificador sintético, sem tabela de correspondência |
| Sobra sinal de aluno depois do baseline? | **−0,0284**, IC95% [−0,0342, −0,0228] — dar o baseline ao modelo *como feature* e somar as features de aluno **piora** o resultado (`src/evaluation/03_teste_residuo.py`) |

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

**O que funciona — e a correção de régua do ADR-0005.** Até 2026-08-20 este
README comparava o modelo contra *"priorize quem estava pior em 2023"*
(AUC 0,4032) e reportava vitória de +0,245 em 18 de 23 UFs. **Essa comparação
era inválida:** AUC é antissimétrica, então 0,4032 significa que a mesma regra
**invertida** vale 0,5968 — de graça. Era o mesmo erro do Cap. 4.6, corrigido
no modelo aluno-nível e não aplicado aqui.

Contra o baseline honesto — a regra trivial com a **direção prevista a partir
das outras UFs** (leave-one-UF-out, sem olhar o resultado do próprio estado):

| | AUC ponderado |
|---|---|
| regra trivial "pior primeiro" | 0,4032 *(a régua inválida)* |
| regra trivial "melhor primeiro" | 0,5968 *(a mesma regra, invertida)* |
| **baseline honesto (direção por LOO)** | **0,6209** |
| **modelo** | **0,6478** — ganho **+0,027**, IC95% [+0,007, +0,048] |

Veredito por UF com IC95% pareado: o modelo **vence em 3** (PR, RJ, RS),
**perde em 3** (MG, RN, TO) e fica **inconclusivo em 17**.

*"Inconclusivo" não é "empata".* Um IC que cruza o zero é **ausência de
evidência**, não evidência de equivalência — nessas 17 UFs o dado não permite
afirmar nem negar vantagem, e a recomendação prática é usar a regra trivial,
que é mais barata. O campo `veredito` de
[`ranking_intra_uf.json`](reports/ranking_intra_uf.json) grava `inconclusivo`
exatamente por isso.

**De onde vem a vantagem:** das 7 UFs onde a direção *não* é previsível de
fora (+0,155, IC95% [+0,082, +0,226]). Nas 16 previsíveis, empate técnico
(−0,010, IC cruza zero). O modelo é um **seguro contra errar a direção**, não
um ranqueador superior.

### O enriquecimento com infraestrutura escolar — e o efeito ecológico

O enunciado autoriza enriquecer a base com Censo Escolar (pág. 3-4). Foi feito,
medido e **não promovido a produção** ([ADR-0011](docs/adr/0011-enriquecimento-infraestrutura-censo-escolar.md)).
O caminho até a decisão vale mais que a decisão.

**O que foi construído.** Censo Escolar 2023 (217.625 escolas) agregado por
município, filtrado à população que o indicador de fato mede — escola em
atividade, rede pública, com matrícula no 2º ano — e ponderado por
`QT_MAT_FUND_AI_2`, não por média simples entre escolas. Sobram 73.660
escolas e 2.357.055 matrículas, cobrindo **5.231/5.232 municípios (100,0%)**
do dataset canônico.

**Por que 2023 e não 2024.** O Censo 2024 existe, mas o servidor do Inep o
publica com `Last-Modified` de julho/2026 — depois do desfecho que o alvo
mede. Usá-lo daria ao modelo informação indisponível no momento da decisão:
o mesmo skew treino-serviço do [ADR-0008](docs/adr/0008-skew-treino-servico-nas-features-de-historico.md).
A escolha do ano aqui é tratamento de leakage, não disponibilidade.

**O resultado: não ajuda.** AUC ponderado 0,6478 → 0,6456 (−0,0022). O IC
bootstrap pareado não identifica **nenhuma** UF em que a infraestrutura ajude,
e identifica **duas** em que atrapalha (PR, RJ). A previsão registrada antes
de rodar era de resultado positivo — errou, e o registro do erro está no
[dicionário](reports/dicionario_censo_escolar.md).

**O achado que salva o esforço.** "Não prevê o furo da meta" não é "não tem
relação com alfabetização" — são alvos diferentes, e confundir os dois seria
concluir algo que o teste nunca perguntou. Medindo contra o **nível** de
alfabetização (`taxa23`), a associação existe e é forte. Mas quase toda ela
desaparece dentro do estado:

| Índice | r nacional | r intra-UF | fração do sinal que era entre estados |
|---|---:|---:|---:|
| `infra_pedagogico` | +0,258 | +0,074 | **71%** |
| `infra_conectividade` | +0,204 | +0,087 | 58% |
| `infra_saneamento` | +0,101 | −0,000 | **100%** |

*(n = 5.231; p com correção de Holm para as 6 comparações;
[`06_infra_nivel_vs_meta.py`](src/evaluation/06_infra_nivel_vs_meta.py))*

Isto é **efeito ecológico**: estados com melhor infraestrutura escolar têm,
simultaneamente, maior alfabetização — sem que uma coisa explique a outra
entre municípios do mesmo estado. É exatamente o mecanismo que já tinha
derrubado o modelo municipal nacional deste projeto (§5.2: "o sinal era a
régua estadual"), agora **reproduzido de forma independente** com uma fonte de
dado que o projeto nunca tinha usado.

A leitura de política pública que decorre daí é contraintuitiva e é o ponto:
um ranking nacional de municípios por infraestrutura escolar pareceria
explicar alfabetização (r = +0,26) e estaria, em 71% do efeito, apenas
reordenando estados.

### O placebo que invalidou a própria métrica de sucesso do projeto

Dois enriquecimentos **sem correlação entre si** (IDHM socioeconômico de 2010
e infraestrutura escolar de 2023, r ≈ 0,02–0,08) moveram as **mesmas** UFs na
**mesma** direção: BA de `inconclusivo` para `modelo_perde`, PE de
`inconclusivo` para `modelo_vence`. Se a mudança viesse da informação de cada
fonte, isso não deveria acontecer.

A hipótese alternativa — de que a mudança vem do simples ato de **adicionar
dimensão** — foi testada por permutação dentro da UF: os índices são
embaralhados entre municípios do mesmo estado, o que preserva a distribuição
marginal e a correlação entre eles e destrói só o vínculo com o alvo
([`09_placebo_permutacao.py`](src/modeling/09_placebo_permutacao.py), 20
replicações).

| Métrica | Sob ruído (features sem informação) | Com dado real | p |
|---|---|---|---:|
| Mudanças de veredito | mediana 3 (faixa 1–6) | 4 | 0,400 |
| AUC ponderado | 0,6445 [0,6359; 0,6511] | 0,6456 | 0,350 |

**As quatro mudanças observadas com dado real são reproduzidas por ruído puro,
sempre na mesma direção** — BA em 10 de 20 permutações (50%), PE em 7 de 20
(35%), GO e TO em 3 de 20. Nenhuma UF sobrevive à correção de
Benjamini-Hochberg.

O mecanismo é simples e vale para qualquer enriquecimento: uma UF cujo
intervalo de confiança já está encostado no zero atravessa a fronteira com
**qualquer** coluna a mais, e sempre para o lado de que já estava mais perto.

A consequência é desconfortável e está registrada: **a métrica "contagem de
UFs que mudam de veredito", usada como critério de sucesso desde o
[ADR-0009](docs/adr/0009-enriquecimento-municipal-fundeb-idhm.md), mede
instabilidade de fronteira, não ganho de informação.** O "PE fechou" celebrado
no experimento com IDHM é o mesmo flip que o acaso entrega em 35% das
permutações. A decisão de não promover aquele enriquecimento continua certa —
o raciocínio que a sustentava, não. A nota retroativa está no próprio ADR-0009
§9, em vez de silenciosamente corrigida.

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
- **Com 2 anos de dado, a validação temporal não consegue testar o nível
  aluno.** O t-1 de 2023 seria 2022, que não existe: no ano de treino as 6
  features de histórico são nulas, constantes ou cópias de `sigla_uf`, e o
  modelo treina com 10 das 12 features declaradas (§7.4). Quatro delas valem
  **0,0%** de influência (§7.1). Não é bug de código — é consequência
  aritmética do tamanho da série. **Um terceiro ano é pré-condição, não
  melhoria incremental.** Ver
  [`ADR-0008`](docs/adr/0008-skew-treino-servico-nas-features-de-historico.md).
- **`peso_aluno`** (peso amostral) foi excluído como feature — seu uso
  correto é exclusivamente estatístico, para ponderar cálculos de
  população, nunca como entrada de modelo.
- **`caderno`** carrega um resíduo de influência (6,7%) sem explicação
  causal confirmada. Três tentativas de acessar o dicionário oficial de
  valores do INEP (portal restrito, basedosdados.org sem essa informação,
  PDF técnico com erro de certificado) não resolveram a categoria 12 —
  resolvida por análise de dados própria (crosstab), não por documentação
  externa.
- **Há apenas uma transição temporal validada (2024 → 2025)** — o backtest
  prospectivo elimina a lacuna de "nenhum ano futuro", mas ainda não prova
  estabilidade entre ciclos nem substitui monitoramento anual. Além disso, o
  efeito é heterogêneo: CE favorece a regra simples e 8 UFs permanecem
  inconclusivas. Ver `reports/backtest_prospectivo_2025.json` e
  `reports/decisao_produto_pos_backtest_2025.md`.
- **SICONFI** (`gasto_por_habitante_educacao`, ~9 mil requisições a API
  pública) não foi buscado — o teste barato (população + meta) já mostrou
  que o problema é o modelo tentar ser um baseline municipal, não falta de
  mais uma feature municipal.
- **Reprodutibilidade de versão**: scikit-learn 1.8→1.9 mudou o Recall do
  baseline em ~1,6pp com o mesmo seed e dado — `requirements.txt` pinado
  mitiga, mas não elimina esse tipo de variação entre ambientes.

- **O enriquecimento com infraestrutura escolar cobre um único ano (2023).**
  A escolha é de validade temporal, não de conveniência (ver §8), mas
  significa que o efeito medido é estrutural, não dinâmico: não se testou se
  *mudança* de infraestrutura acompanha *mudança* de alfabetização. E a
  conclusão vale para o ciclo 2023→2024 — promover isso ao backtest 2025
  exigiria refazer a escolha do ano **para aquele ciclo**, não herdar esta.
- **Três enriquecimentos externos foram testados e nenhum entrou em produção**
  — IDHM (misto), FUNDEB (adiado por fricção de acesso), infraestrutura
  escolar (misto, AUC agregado negativo). As features existem no código como
  capacidade testada e desligada, não como promessa não cumprida:
  `montar_dataset(com_idhm=True)` e `montar_dataset(com_infra=True)`.

## 10. Aplicação prática para políticas públicas

**Duas recomendações, ambas sustentadas por evidência estatística com
intervalo de confiança:**

1. **Para busca ativa de alunos**, usar a **meta do PDE do município** como
   critério de priorização, não um modelo aluno-nível. Mais simples de
   explicar, mais barata de manter (nenhum pipeline de ML em produção), e
   estatisticamente mais eficaz com os dados disponíveis.
2. **Para priorização entre municípios**, comparar **dentro do estado**, nunca
   entre estados, e liberar o ranking somente onde o teste temporal o
   sustenta: o modelo venceu em 14 UFs; no CE, a regra simples é superior; e
   em 8 UFs a recomendação responsável é não ranquear. Uma regra nacional
   única continua inválida.

### O painel de priorização

A recomendação 2 não fica apenas em prosa: `reports/painel_intra_uf.html` é
uma demonstração autocontida, regenerada a partir do backtest prospectivo de
2025 (`reports/ranking_prospectivo_2025.json`). Ele já aplica o contrato de uso
condicional — ranking do modelo nas 14 UFs vencedoras, regra simples no CE,
abstenção diagnóstica nas 8 inconclusivas — e mostra fonte oficial, SHA-256 da
planilha e data de corte do treino. A decisão completa está em
`reports/decisao_produto_pos_backtest_2025.md`.

Três decisões de produto que valem registro:

- **Não existe visão nacional, de propósito.** Se a interface permitisse
  ordenar municípios de estados diferentes, ela convidaria exatamente o erro
  descrito em §9. A restrição vive na ferramenta, não no rodapé.
- **Cada estado declara se o modelo ajuda ali, no ciclo futuro.** O
  backtest 2025 registra `modelo_vence` em 14 UFs, `modelo_perde` no CE e
  `inconclusivo` em 8. O painel já aplica isso: recomenda a regra simples no
  CE, exibe só diagnóstico nas 8 inconclusivas (cabeçalho da tabela muda para
  "score do modelo (diagnóstico)" e o texto não sugere ordem de ação) e libera
  o ranking do modelo só nas 14. Um número médio não pode esconder essas
  diferenças.
- **Cada estado declara qual direção vale ali.** Onde o painel usa a regra
  simples (CE) ou se abstém, ele diz se a regra que funciona naquele estado é
  "priorize quem estava melhor" ou "quem estava pior" — a direção usada é a que
  já funcionava na própria UF em 2024, nunca escolhida olhando o resultado de
  2025.
- **O score vem do backtest, fora do ciclo de treino.** O número que o gestor
  vê é o que o modelo — congelado em 2023→2024 — atribuiu ao município para o
  ciclo de 2025 antes de o resultado sair.

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
  resíduo de 6,7% de influência fica sem explicação causal.
- **Re-executar a cada resultado anual** para verificar se o ganho de 2025
  persiste, antes de alterar a regra de qualquer UF.
- **Reportar toda contagem de veredito contra a distribuição nula** — já
  medida (§8): permutação entrega 1–6 mudanças por acaso. Qualquer
  enriquecimento futuro precisa vir com esse `p`, nunca com a contagem
  sozinha. O placebo custa 20 execuções e é reaproveitável como está.
- **Rodar o placebo com mais replicações** — 20 dão resolução mínima de
  p ≈ 0,048, insuficiente para o teste por UF depois da correção de múltiplas
  comparações. A conclusão global não depende disso (o observado cai no meio
  da distribuição nula), mas o teste UF a UF fica subdimensionado por
  construção.

---

## Estrutura do repositório

```
tech-challenge-fase3-alfabetizacao/
├── data/                    Snapshots processados (território local, etc.)
├── docs/
│   └── adr/                 Decisões arquiteturais registradas (0001–0011)
├── images/                  Gráficos SHAP e diagnósticos
├── notebooks/
│   └── 01_analise_completa.ipynb   Narrativa analítica, gerada e executada por script
├── reports/                 EDA, dicionário, métricas, proveniência,
│                            ranking intra-UF e o painel HTML
├── src/
│   ├── preprocessing/       Extração, guarda de leakage, pipeline, território,
│   │                        agregação e EDA do Censo Escolar
│   ├── modeling/            Baseline, tournament, ranking intra-UF, regressão,
│   │                        experimentos de enriquecimento e placebo
│   ├── evaluation/          SHAP, falsificação, resíduo, backtest 2025,
│   │                        nível vs. furo da meta
│   └── visualization/       Geração do painel e do notebook
├── requirements.txt
└── README.md                Este arquivo
```

## Reprodutibilidade

### Pré-requisitos

**Este projeto depende da pasta da Fase 2, que precisa estar ao lado dele:**

```
PROJETOS/01_PRIORITY/
├── tech-challenge-fase2-alfabetizacao/
│   └── dados/
│       ├── br_inep_avaliacao_alfabetizacao_meta_alfabetizacao_municipio.csv.gz
│       └── Alunos.csv
└── tech-challenge-fase3-alfabetizacao/     <- este projeto
```

A Fase 3 consome o dado tratado pela Fase 2 (é o que o enunciado pede, pág. 2:
"os dados tratados na camada Gold serão utilizados"). Os scripts resolvem o
caminho por `BASE.parent / "tech-challenge-fase2-alfabetizacao"` — sem a pasta
irmã, falham na leitura.

**Dados que NÃO estão no repositório e são baixados ou gerados na hora:**

| Arquivo | Como obter | Tamanho |
|---|---|---|
| `dados_externos/resultados_e_metas_municipios_2025_3.xlsx` | Baixado automaticamente pelo backtest, com verificação de SHA-256 | 519 KB |
| `dados_externos/_cache_censo_escolar_2023.zip` | Baixado automaticamente pela agregação do Censo | 32 MB |
| `data/*.parquet` | Gerados pelos scripts de pré-processamento | — |

### Verificação de reprodução (executada em 2026-08-31)

O backtest foi rodado **do zero**, com a planilha do Inep baixada novamente da
fonte oficial, e os dois artefatos canônicos saíram **idênticos bit a bit** aos
versionados:

```
IDENTICO  reports/backtest_prospectivo_2025.json
IDENTICO  reports/ranking_prospectivo_2025.json
```

O SHA-256 da planilha baixada confere com o registrado em
[`proveniencia_ica_2025.md`](reports/proveniencia_ica_2025.md) e dentro do
próprio JSON. A imutabilidade do backtest não é uma afirmação do README: é uma
propriedade verificada, e há teste que falha se a constante do código divergir
da proveniência publicada.

**Entregável 1 — modelo aluno-nível** (resultado negativo, §7):

```bash
pip install -r requirements.txt
python src/preprocessing/05_montar_territorio.py             # IBGE + metas, 1 requisição
python src/preprocessing/02_extrair_snapshot.py --full --silver data/territorio_local.parquet
python src/preprocessing/03_guarda_leakage.py                # gate: falha se houver vazamento
python src/preprocessing/01_eda_alunos.py --dataset snapshot
python src/modeling/02_tournament_modelos.py --temporal
python src/modeling/05_comparar_encodings.py                 # OneHot, Target e Frequency
python src/evaluation/01_shap_interpretabilidade.py --temporal
python src/evaluation/02_teste_falsificacao.py               # o teste que decide o projeto
python src/evaluation/03_teste_residuo.py                    # sobra sinal individual?
python src/evaluation/04_robustez_algoritmo.py               # veredito independe do algoritmo?
```

**Entregável 2 — priorização municipal intra-UF** (§8 e §10):

```bash
python src/modeling/03_experimento_municipio_meta.py    # 5 etapas, a 4ª é a que decide
python src/modeling/04_ranking_intra_uf.py              # modelo produtizado (retrato histórico)
python src/evaluation/05_backtest_prospectivo_2025.py   # backtest 2024→2025 + ranking_prospectivo_2025.json
python src/visualization/01_gerar_painel_intra_uf.py    # gera reports/painel_intra_uf.html (contrato 2025)
```

O painel depende de `reports/ranking_prospectivo_2025.json` — rode o backtest
antes do gerador.

**Enriquecimento externo — testado e não promovido** (§8, ADR-0009 e ADR-0011):

```bash
python src/preprocessing/06_agregar_censo_escolar.py    # baixa o Censo 2023 e agrega por município
python src/preprocessing/07_eda_censo_escolar.py        # EDA dos 9 itens do gate CRISP-DM
python src/modeling/06_experimento_idhm.py              # IDHM: misto, não promovido
python src/modeling/08_experimento_infra_escolar.py     # infraestrutura: misto, não promovido
python src/evaluation/06_infra_nivel_vs_meta.py         # nível vs. furo da meta (efeito ecológico)
python src/modeling/09_placebo_permutacao.py 20         # distribuição nula por permutação
```

O primeiro script baixa ~32 MB do Inep e guarda em
`dados_externos/_cache_censo_escolar_2023.zip` (fora do git); as execuções
seguintes reusam o cache. O agregado municipal versionado é
`dados_externos/censo_escolar_municipio_2023.csv`.

**Notebook da narrativa analítica:**

```bash
python src/visualization/02_gerar_notebook.py   # constrói E executa o notebook
```

O notebook é **gerado por script, não escrito à mão** — assim as saídas
gravadas são sempre as do código atual. Notebook escrito à mão apodrece:
alguém roda uma célula fora de ordem, salva, e o arquivo versionado passa a
mostrar um número que o código não produz mais.

Decisões técnicas completas, incluindo a sequência de correções (vazamentos
achados, escala corrigida, régua de teste recalibrada), no diário de
bordo interno (não publicado) e nos ADRs em
[`docs/adr/`](docs/adr/) (migrados de `docs/wayfinder/tech_challenge_fase3/adr/`
em 2026-08-20).

</details>
