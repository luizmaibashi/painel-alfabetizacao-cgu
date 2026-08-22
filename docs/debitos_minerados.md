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
