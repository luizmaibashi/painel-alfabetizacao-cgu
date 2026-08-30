# ADR-0007: Determinismo de execução como requisito de entrega

**Data**: 2026-08-25
**Status**: Accepted — com **correção medida em 2026-08-30** na §2.2 (a
premissa "`RandomForest` com `n_jobs=-1` não tem dependência de ordem" é
falsa; efeito é real mas 35× menor que a margem de qualquer veredito, e
nenhum número publicado muda). Débito de reprodutibilidade aberto, com 3
opções de correção listadas na própria §2.2.
**Proposto por**: Luiz Maibashi
**Contexto**: Verificação da exigência de "replicabilidade" do enunciado (p.3)
durante o planejamento do recomeço pedagógico. O que começou como um item
menor de checklist revelou que **um número publicado no ADR-0006 e no README
não era reproduzível** — e que os relatórios versionados em `reports/` estavam
dessincronizados do código.

---

## 🤔 1. CONTEXTO (O QUÊ?)

O enunciado exige, entre os itens obrigatórios da pipeline (p.3): *"Validação
do modelo garantindo **replicabilidade** e generalização"*. O projeto tratava
isso como atendido por `random_state=42` — a suposição usual de que semente
fixa basta.

**Não basta.** Medição controlada em 2026-08-25: mesma `.venv` pinada, mesmo
`snapshot_modelagem.parquet` (intocado desde 2026-08-18), mesmo código, mesma
seed. A **única** variável foi `OMP_NUM_THREADS`:

| Threads | AUC | | Threads | AUC |
|---|---|---|---|---|
| 1 | 0,6047 | | **6** | **0,6025** |
| 2 | **0,6061** | | 8 (`nproc` da máquina) | 0,6048 |
| 3 | 0,6034 | | 12 e 16 | 0,6048 |

**Amplitude 0,0036 — cerca de 13% do efeito medido** (a diferença para o
baseline é −0,028). Acima de 8 satura, porque a máquina tem 8 núcleos.

### Mecanismo

Soma em ponto flutuante **não é associativa**: `(a+b)+c ≠ a+(b+c)` por
arredondamento em precisão finita. `tree_method="hist"` paraleliza a redução do
histograma — cada thread soma um pedaço e os parciais são combinados. **Quantas
threads existem determina a ordem das somas.**

> A seed controla **quais** números entram na conta.
> Não controla **em que ordem o processador vai somá-los**.

### A consequência que já tinha acontecido

O número **0,6026**, publicado no ADR-0006 §7 e no README §5.1 como resultado
canônico do modelo aluno-nível, corresponde a uma execução com ~6 threads
disponíveis — provavelmente com outra carga competindo pela CPU. **Não era
reproduzível, e ninguém tinha como saber**, porque o mesmo comando na mesma
máquina em condições parecidas devolvia o mesmo valor.

Isto é a **terceira instância no projeto** do mesmo padrão — número aceito sem
verificar a régua que o produziu:

| Onde | Régua não verificada | Custo |
|---|---|---|
| ADR-0005 | direção da AUC (antissimétrica) | ganho caiu de +0,245 para +0,027 |
| ADR-0006 §7 | teto por tupla discreta + k-fold com vazamento temporal | teto de 0,6017 invalidado |
| **Aqui** | **ambiente de execução (contagem de threads)** | **0,6026 publicado, na verdade 0,6047** |

### Registro honesto do caminho

A primeira investigação deste fenômeno, no mesmo dia, **concluiu erradamente
que `n_jobs` não era a causa** — porque testou 5 vezes na mesma máquina sem
carga, ou seja, sempre com 8 threads, e viu 0,6048 nas 5. Depois atribuiu a
diferença a versões de biblioteca, com base numa coincidência numérica.

Manter uma variável constante sem perceber que ela é variável não é
determinismo. O erro fica registrado porque é o mesmo gênero que a ADR combate.

---

## ⚙️ 2. DECISÃO (POR QUÊ?)

### 2.1 `n_jobs=1` onde o paralelismo é sobre uma redução compartilhada

Aplicado a **6 pontos em 5 arquivos**, com o motivo comentado no código:

| Arquivo | Estimador | Ação |
|---|---|---|
| `evaluation/01_shap_interpretabilidade.py` | XGB `hist` | `n_jobs=1` |
| `evaluation/02_teste_falsificacao.py` | XGB `hist` | `n_jobs=1` |
| `evaluation/03_teste_residuo.py` | XGB `hist` | `n_jobs=1` |
| `modeling/02_tournament_modelos.py` | XGB `hist` | `n_jobs=1` |
| `modeling/03_experimento_municipio_meta.py` (2×) | XGB `hist` | `n_jobs=1` |

### 2.2 `n_jobs=-1` **permanece** onde o paralelismo é sobre unidades independentes

`RandomForest`, `GridSearchCV` e `cross_val_predict` mantêm `n_jobs=-1`
deliberadamente. Eles distribuem **unidades calculadas em isolamento** — uma
árvore, uma combinação de hiperparâmetro, uma dobra — coletadas só ao final.
Não há redução compartilhada, logo não há dependência de ordem.

**Verificado empiricamente**: `04_ranking_intra_uf.py` (RandomForest,
`n_jobs=-1`) produz resultado **bit a bit idêntico** a 1, 2 e 6 threads —
incluindo a lista nominal de UFs em cada veredito, e o `ranking_intra_uf.json`
não muda entre execuções.

**A regra generalizável não é "paralelismo é ruim":**

> Paralelismo sobre uma **redução compartilhada** quebra reprodutibilidade.
> Paralelismo sobre **unidades independentes**, não.

O tournament tem os dois tipos lado a lado e a distinção está comentada lá.

---

> #### ⚠️ Correção medida em 2026-08-30 — a frase acima é forte demais
>
> Auditoria de ponta a ponta rodou `05_backtest_prospectivo_2025.py` duas
> vezes e o output **não** foi bit a bit idêntico. Investigado até a causa:
>
> ```
> RandomForestClassifier(n_estimators=200, max_depth=6, random_state=42)
> n_jobs=-1 vs n_jobs=-1 : bit-idêntico? False
> n_jobs=-1 vs n_jobs=1  : bit-idêntico? False
> max |diff| = 3,3e-16   (épsilon de float64)
> ```
>
> **`RandomForest` com `n_jobs=-1` não é bit-a-bit determinístico** — nem
> contra si mesmo. `predict_proba` **calcula a média** das árvores, e essa
> média é uma redução paralelizada em blocos por thread. Ou seja: a redução
> compartilhada que a §2.2 dizia não existir, existe. O que a distingue do
> `tree_method="hist"` é **magnitude**, não natureza.
>
> **Por que a verificação original passou e continua válida no que afirmou.**
> Ela foi feita em `04_ranking_intra_uf.py`, que grava métricas arredondadas
> em 4 casas — 3,3e-16 desaparece no arredondamento. Reconfirmado em
> 2026-08-30: aquele script segue bit a bit idêntico a 1, 2 e 6 threads. O
> erro não foi a medição; foi **generalizar de um script para uma classe de
> algoritmos**.
>
> **O que mudou desde então.** O `05_backtest_prospectivo_2025.py` passa os
> scores por um bootstrap de 1.000 reamostragens. O percentil 97,5
> **amplifica** o épsilon: basta uma reamostragem cruzar o corte para o
> limite do IC mudar na 4ª casa.
>
> ```
> RS, ganho_ic95 superior:  0,2717 (1 thread)  vs  0,2716 (6 threads)
> ```
>
> **Escopo medido, sem inflar:** 1 valor em 23 UFs. `auc_modelo`,
> `auc_baseline`, `ganho_sobre_baseline`, o bloco `resumo` e os **23
> vereditos** ficam idênticos. A menor margem entre um IC e o zero (PE,
> 0,0035) é **35× maior** que a variação observada (0,0001) — nenhum veredito
> pode virar por este ruído. É **dívida de reprodutibilidade bit-a-bit, não
> erro de resultado**: nenhum número publicado no README, painel ou notebook
> muda.
>
> **Débito aberto (não corrigido aqui, deliberadamente).** Forçar `n_jobs=1`
> no backtest resolveria, mas muda o custo de execução de um script que treina
> 23 modelos — decisão que merece ser explícita, não um patch lateral no meio
> de uma auditoria. Opções, para decidir antes da próxima rodada Inep:
> (a) `n_jobs=1` só no `05_backtest`, aceitando o tempo maior; (b) manter
> `n_jobs=-1` e declarar a tolerância de ±0,0001 no IC como parte do contrato
> do artefato; (c) gravar o IC com 3 casas, onde o ruído não aparece.
>
> **A regra corrigida, que substitui a formulação acima:**
>
> > Toda redução em ponto flutuante paralelizada introduz ruído de ordem.
> > O que muda entre `tree_method="hist"` e `RandomForest` é a **magnitude**
> > — e se o pipeline a jusante **amplifica** (bootstrap, percentil) ou
> > **arredonda** esse ruído.
>
> Registrado também em `tests/test_determinismo_execucao.py` (docstring),
> `02_tournament_modelos.py` e `04_robustez_algoritmo.py`, que repetiam a
> premissa antiga como fato verificado.

### 2.3 Relatórios de `reports/` ficam versionados — exceção consciente ao `AGENTS.md`

O `AGENTS.md` da base diz: *"nunca commitar saídas geradas por scripts
(relatórios regeneráveis ficam fora do git)"*. Mantemos os 8 JSONs versionados,
com dois motivos:

1. **Antes deste ADR eles não eram regeneráveis.** Rodar de novo produzia
   números diferentes. O gate *"saída não-determinística usada como ground
   truth não é regenerável"* (`.claude/rules/dados.md`) já mandava versioná-los.
2. **Depois deste ADR, eles viram a prova da própria alegação.** "É
   reprodutível" é afirmação não verificável sem uma referência contra a qual
   reproduzir. Com os JSONs no repositório, o teste é trivial: o Renan clona,
   roda o pipeline, dá `git diff reports/`. **Zero diferenças = alegação
   comprovada na máquina dele. Diferenças = o conserto está incompleto.**

### 2.4 O guarda é um teste, não uma checagem em runtime

`tests/test_determinismo_execucao.py` faz parsing AST de todo `src/**/*.py` e
reprova qualquer chamada com `tree_method` paralelizável (`hist`, `gpu_hist`,
`approx`) que não declare `n_jobs=1`. **Omitir o parâmetro também reprova** — o
default do XGBoost usa todos os núcleos, que é exatamente o comportamento não
reprodutível; omitir não é neutro, é escolher o default errado em silêncio.

Custo de execução: **zero** (roda no pytest, 0,9s). Verificado que **falha** ao
reintroduzir `n_jobs=-1`, com a linha exata no erro — um guarda que nunca
reprovou não é guarda.

Inclui teste anti-vacuidade: se nenhuma chamada com `tree_method` existir mais,
o arquivo falha em vez de passar por omissão — o antipadrão "lista de cobertura
falha aberta" do `AGENTS.md`.

---

## 3. CONSEQUÊNCIAS

**Positivas:**
- Número canônico do modelo aluno-nível passa a ser **0,6047** (IC95%
  [−0,0342, −0,0228]), estável em qualquer contagem de threads. Confirmado por
  dois scripts independentes (`02_teste_falsificacao` e `03_teste_residuo`).
- O veredito do projeto **não muda em nenhum ponto da faixa** (0,6025–0,6061):
  o modelo perde do baseline 0,6331 com folga em todos.
- A alegação de replicabilidade do enunciado passa a ser **verificável por
  terceiro**, não afirmada.
- Regra transferível para qualquer projeto futuro com gradient boosting.

**Negativas:**
- Perda de paralelismo no treino dos modelos XGBoost. Medição limpa disponível
  só para `02_teste_falsificacao.py`: **33s contra 40s** — mais rápido, porque
  com 48k linhas × 12 features o custo de coordenar threads supera o ganho. ⚠️
  Os tempos do tournament (`16,7s → 24,1s`) estão **confundidos** com a troca
  simultânea do modelo fraco pelo forte e **não medem** o efeito do `n_jobs`.
  Em dataset maior o custo pode ser real e a decisão merece nova medição.
- Os JSONs versionados criam ruído de diff a cada re-execução legítima.
  Aceito: é o preço de ter evidência auditável.

**Achado colateral, corrigido junto:** ao regenerar os relatórios descobriu-se
que estavam **dessincronizados do código**. `shap_interpretabilidade.json`
documentava o modelo **fraco** (400 árvores, depth 3) enquanto o código usava o
forte (800/8) desde 22/08; `metrics_tournament.json` não continha os blocos de
calibração e threshold, apesar de a frente registrar "5 gates ML fechados". Um
avaliador lendo `reports/` veria o modelo fraco e nenhuma evidência de
calibração. Mesma família: **declaração e artefato fora de sincronia**.

---

## 4. ALTERNATIVAS DESCARTADAS

| Opção | Por quê foi rejeitada |
|-------|----------------------|
| Manter `n_jobs=-1` e reportar o intervalo (`0,604 ± 0,002`) | Honesto, mas não atende o enunciado: replicabilidade significa o avaliador reproduzir o número, não receber uma faixa. E não resolve o SHAP, lido como evidência de negócio |
| Fixar `OMP_NUM_THREADS=1` por variável de ambiente | Frágil — depende de quem executa lembrar de exportar. Não sobrevive a clone e `python script.py` |
| Guarda em runtime que aborta se `n_jobs != 1` | Custo em toda execução para pegar um erro que só entra em tempo de edição. Teste pega mais cedo e mais barato |
| Serializar **todo** `n_jobs=-1`, inclusive RandomForest/GridSearchCV | Custo de tempo sem ganho: medido que não afetam o resultado. Seria cargo cult — aplicar a regra sem o mecanismo que a justifica |
| Tirar os JSONs do git conforme o `AGENTS.md` | Elimina a única forma de terceiro verificar a alegação de reprodutibilidade |

---

## 5. IMPACTO ROI

- **Métrica de sucesso**: `pytest tests/test_determinismo_execucao.py` verde, e
  `git diff reports/` vazio após re-executar o pipeline numa máquina limpa.
- **Resultado medido nesta sessão**: 16 testes do guarda passando; suíte total
  em **48 testes**; `02_teste_falsificacao.py` em 0,6047 a 2 e a 6 threads
  (antes: 0,6061 e 0,6025).
- **Timeline**: aplicado em uma sessão; nenhum retrabalho de modelagem.
- **Risco de regressão**: coberto pelo teste. O risco real não é o bug voltar
  sozinho — é alguém (inclusive um agente de IA) ver `n_jobs=1` num script de
  ML, julgar desperdício de CPU e "otimizar". Comentário explica; comentário não
  falha build. O teste falha.

---

## 6. LINKS RELACIONADOS

- `docs/wayfinder/tech_challenge_fase3/0009-replicabilidade.md` — investigação
  completa, incluindo as duas conclusões erradas antes da correta.
- [[docs/adr/0005-correcao-da-regua-do-baseline-intra-uf.md]] e
  [[docs/adr/0006-ceiling-analysis-como-gate-pre-treino.md]] §7.1 — as outras
  duas instâncias de "número aceito sem verificar a régua".
- `tests/test_determinismo_execucao.py` — o guarda executável.
- `.claude/rules/dados.md` — gate "saída não-determinística não é regenerável",
  que sustenta a decisão 2.3.
