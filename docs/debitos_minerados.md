# Débitos minerados — tech-challenge-fase3-alfabetizacao (pos_tech)

> Rodada 1: 2026-08-22, via skill `/minerar-debitos`. Fonte: `docs/HANDOFF_RENAN.md` (13 capítulos) — projeto sem `AGENTS.md` com "Débitos técnicos conhecidos" numerado; o HANDOFF cumpre a mesma função (diagnóstico de falha, causa raiz, correção). Já é a origem de 6 gates existentes em `.claude/rules/dados.md` (threshold vs balanceamento, ADR sem código, cobertura de teste, guarda de leakage com teste próprio, nulidade prediz alvo — item 9 do gate CRISP-DM, baseline mesma população). Esses não foram reminerados — são o material de origem.

| Capítulo | Achado | Classificação | Destino |
|---|---|---|---|
| 1.2/1.3 | 5 críticas da Fase 2; padrão "peça construída ≠ entregue" | Fonte do gate existente | Origem do gate "ADR sem código" (`dados.md`) |
| 1.3 (2ª regra) | "Não confie na memória do enunciado, cruze linha por linha" | Já coberto | Fluxo `spec-governance` (diff review contra spec) já cobre compliance de requisito |
| 4.2/9.3 | Vazamento por `peso_aluno` (nulidade prediz alvo) | Fonte do gate existente | Origem do item 9 do gate CRISP-DM |
| 6.1/6.2 | Padrão de Fase 2 se repetindo (peça construída, ligação faltando) | Já coberto | Mesma classe do 1.3 — Lei da Travessia, já nomeada |
| 8.1-8.5 | Tournament de 3 modelos, gap treino-validação, reprodutibilidade | Fonte do gate existente | Origem do gate "threshold vs balanceamento" e adjacentes |
| **10.1** | Regra "AI Jail" da Fase 2 (motivo: cota GCP/travar máquina) herdada literalmente pra Fase 3 e aplicada a CSV local de 7MB — modelagem rodou 8,7% dos dados por meses sem necessidade | **Estrutural (gate novo)** | `AGENTS.md` § Regras de engenharia — "Regra herdada sem revalidar o motivo" |
| 10.8 | 3 gates do próprio projeto violados ao decidir próximo passo (EDA desatualizada, dicionário incompleto) | Já coberto | Confirma que os gates de `dados.md` existentes funcionam quando checados — não é achado novo, é o próprio sistema funcionando |
| 10.9 | "Peça existia, ligação não" 3x seguidas no mesmo projeto | Já coberto | É a Lei da Travessia relatada em palavras — não gera gate adicional |
| 11-13 | Teste de falsificação, ensaio `--full`, validação contra número oficial | Fonte do gate existente | Origem indireta do gate "critério de ADR precisa aparecer em código" (o critério de falsificação em si) |

## Achado da rodada

**1 débito estrutural genuinamente novo** (Cap. 10.1) — diferente dos outros dois projetos minerados, o pos_tech não tinha lista de débito numerada; o HANDOFF (documento de handoff, não backlog) já tinha sido fonte de 6 gates diretamente, então a maior parte do que sobrou pra minerar já é conhecida. O achado novo é de uma classe diferente dos anteriores: não é "declaração sem código" (Lei da Travessia clássica) — é o **inverso**: código seguindo declaração cegamente, sem revalidar se o motivo dela ainda vale no novo contexto. Custo medido: meses de modelagem em 8,7% dos dados disponíveis.

**3 rodadas completas** (stable-treasury 0 novo, payflow 2 novos, pos_tech 1 novo) — total 4 gates manuais escritos nesta sub-frente, todos sem sinal automático testado ainda.

## Teste de aplicação (2026-08-24) — diferente de mineração

Não é mineração de débito novo: é rodar os 4 gates manuais já escritos direto contra `src/` (14 arquivos, fora `.venv/`), pra ver se pegam algo no código atual. Contraste com o mesmo teste rodado contra `shadow_fx_terminal` em 2026-08-22 (0 achados, 0 falso positivo) — este projeto é a origem de um dos 4 gates, então era esperado achar algo aqui e não lá.

| Gate | Resultado |
|---|---|
| Guarda silenciosa | **Achado real**: `src/preprocessing/05_montar_territorio.py:127-132` — imputação em cascata (mediana UF → mediana global) de `meta_alfabetizacao_2024_imputada` sem logar `n` afetado por fallback. O mesmo projeto já corrigiu esse exato padrão em `02_extrair_snapshot.py:198-210` (loga `n_imp`/total/origem) — a correção existe, não foi replicada aqui. ✅ **Corrigido em 2026-08-24** (ver abaixo). |
| Lista de cobertura fail-open | **Achado real**: `src/preprocessing/pipeline_preprocessamento.py:121-136` — `colunas_ignoradas()` existe no comentário pra evitar "coluna nova descartada em silêncio", mas só reporta em log (`descrever_features`), nunca bloqueia; zero teste chama a função. Coluna nova fora de `TODAS_CANDIDATAS` é excluída do modelo sem forçar ninguém a notar. ✅ **Corrigido em 2026-08-24** (ver abaixo). |
| Saída não-determinística como ground truth | Não se aplica — projeto não usa saída de LLM como rótulo. |
| Regra herdada sem revalidar motivo | Sem achado novo — já corrigido corretamente. `02_extrair_snapshot.py:35-37` documenta o motivo original (custo GCP) e por que não se aplica a CSV local de 7,3MB. Exemplo do padrão bem aplicado. |

**Decisão do Luiz**: registrar os 2 achados e corrigir na próxima sessão de trabalho no pos_tech, não nesta sessão (que era sobre `base_conhecimento`).

## Correção dos 2 achados (2026-08-24)

### 1. Guarda silenciosa — `05_montar_territorio.py`

Cascata extraída para `imputar_meta(df)`, função testável, que agora loga o `n`
de **cada degrau separadamente**. O total sozinho não serviria: os dois degraus
não têm o mesmo risco — cair na mediana da própria UF é razoável, cair na
mediana **global** significa que a UF inteira estava sem meta.

Números reais que estavam invisíveis: **240 de 10.704** imputadas (2,2%), sendo
**196 pela mediana da UF** e **44 pela mediana global**.

Acrescentado também um `raise` para o caso de a coluna vir 100% nula — aí a
mediana global também é `NaN` e a cascata entregaria uma feature inteiramente
nula ao modelo sem quebrar nada. É dado ausente, não dado imputado.

**A imputação não mudou de valor.** Verificado contra a lógica antiga e contra
o Parquet já em disco: `equals() == True`, diferença máxima absoluta `0.0`. A
mudança é observabilidade pura — o modelo canônico já validado continua
treinando sobre exatamente os mesmos números.

### 2. Lista fail-open — `pipeline_preprocessamento.py`

`colunas_ignoradas()` continua sendo a consulta pura (não quebra
`descrever_features` nem `04_ensaio_full.py`). O bloqueio veio numa função
nova, `validar_cobertura_colunas(df, permitidas=())`, que levanta
`ColunaNaoDeclaradaError` — default **restritivo**, invertendo o fail-open.

Ligada no carregamento do snapshot dos 5 scripts que o consomem
(`01_treinar_baseline`, `02_tournament_modelos`, `01_shap_interpretabilidade`,
`02_teste_falsificacao`, `03_teste_residuo`).

**Por que no carregamento e não em `construir_preprocessador`**: aquele ponto
recebe o frame já fatiado, e `03_teste_residuo.py:95` passa
`colunas_feature(df) + ["_score_baseline"]` — coluna de apoio criada dentro do
próprio script, que não é "coluna nova que apareceu no snapshot". Validar ali
quebraria o script e o gate viraria falso positivo, removido na primeira vez
que atrapalhasse.

### Verificação

- **32 testes passando** (17 antes, +15 novos em `tests/test_montar_territorio.py`
  e `tests/test_pipeline_preprocessamento.py`).
- Gate tem dentes: coluna fictícia injetada no snapshot real é **bloqueada**;
  antes o treino seguia com 12 features, descartando-a em silêncio.
- Snapshot real de hoje passa sem levantar — nenhum pipeline existente quebrou.
- `scripts/check_gates_ml.py --project tech-challenge-fase3-alfabetizacao`:
  nenhum achado.
