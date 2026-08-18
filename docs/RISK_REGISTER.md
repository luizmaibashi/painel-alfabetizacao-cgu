# Risk Register — Tech Challenge Fase 3

**Origem:** `PLANO_REFINAMENTO_CONCEITOS.md`, Seção 2, Atividade 3.
**Atualizado em:** 2026-08-18.
**Uso:** insumo pra call com o Renan (aprovar/reajustar) e pra seção
"Limitações do projeto" do README final.

| # | Risco | Origem/evidência | Mitigação atual | Dono da decisão |
|---|---|---|---|---|
| 1 | Recall baixo (0,34–0,42) sem território/socioeconômico pode não justificar o esforço técnico frente ao baseline municipal já existente da Fase 2 | Baseline rodado `--local-only`, ADR-0001 Seção 5 (critério de falsificação: superar `agg_priorizacao`) | Critério de falsificação já definido; decisão final só com `--full` (dado com território, credencial GCP do Renan) | Renan (call) |
| 2 | `caderno=12` (236 alunos, 86,9% "Não") pode ser proxy de necessidade especial/acessibilidade, não metadado neutro — incluir como feature sem confirmar pode ensinar o modelo a penalizar deficiência, não desempenho real | EDA (`reports/eda_alunos.md`) + investigação sem sucesso (`reports/proveniencia_alunos.md`, 3 tentativas de validação externa) | Feature mantida "com ressalva"; checagem obrigatória no SHAP (Seção 3 do plano); decisão final condicionada, ver ADR-0002 | Renan (call) |
| 3 | Sem dado de 2025 — modelo treinado 2023-2024 nunca foi validado contra o ano em que hipoteticamente seria usado | ADR-0002, Seção 2.2 | Documentado como limitação no README (`Limitações do projeto` + `Possíveis evoluções futuras`), sem construir monitoramento (enunciado não exige) | Fechado — decisão tomada, não pendente |
| 4 | Proveniência do `Alunos.csv` é herdada da Fase 2, não confirmada por quem/quando foi baixado do INEP originalmente — sem o pacote oficial (pasta "Dicionário"), nenhuma validação de código de coluna é possível | `docs/HANDOFF_RENAN.md` linha 36 + `reports/proveniencia_alunos.md` | Nenhuma — pendência real, sem rota de resolução conhecida hoje | A confirmar (talvez o Renan tenha acesso ao pacote original) |
| 5 | `--full` (dado com território) depende de credencial GCP que só o Renan tem — se a call atrasar ou a extração falhar, o projeto fica preso no `--local-only` até o prazo de entrega | `docs/HANDOFF_RENAN.md`, `02_extrair_snapshot.py` | Nenhuma — dependência externa direta | Renan (execução), Luiz (prazo) |

## Como usar

Antes da call: revisar linha por linha com o Renan, marcar cada uma como
**Aceito** (segue como está), **Mitigar** (ação definida) ou **Escalar**
(sem solução dentro do prazo — vira limitação documentada no README).
