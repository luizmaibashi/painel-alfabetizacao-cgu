# Risk Register — Tech Challenge Fase 3

**Origem:** `PLANO_REFINAMENTO_CONCEITOS.md`, Seção 2, Atividade 3.
**Atualizado em:** 2026-08-18 (riscos 6 e 7 adicionados após reler o feedback
oficial da Fase 2 — ver `docs/FEEDBACK_FASE2_E_LICOES.md`).
**Uso:** insumo pra call com o Renan (aprovar/reajustar) e pra seção
"Limitações do projeto" do README final.

| # | Risco | Origem/evidência | Mitigação atual | Dono da decisão |
|---|---|---|---|---|
| 1 | Recall baixo (0,34–0,42) sem território/socioeconômico pode não justificar o esforço técnico frente ao baseline municipal já existente da Fase 2 | Baseline rodado `--local-only`, ADR-0001 Seção 5 (critério de falsificação: superar `agg_priorizacao`) | Critério de falsificação já definido; decisão final só com `--full` (dado com território, credencial GCP do Renan) | Renan (call) |
| 2 | `caderno=12` (236 alunos, 86,9% "Não") pode ser proxy de necessidade especial/acessibilidade, não metadado neutro — incluir como feature sem confirmar pode ensinar o modelo a penalizar deficiência, não desempenho real | EDA (`reports/eda_alunos.md`) + investigação sem sucesso (`reports/proveniencia_alunos.md`, 3 tentativas de validação externa) | Feature mantida "com ressalva"; checagem obrigatória no SHAP (Seção 3 do plano); decisão final condicionada, ver ADR-0002 | Renan (call) |
| 3 | Sem dado de 2025 — modelo treinado 2023-2024 nunca foi validado contra o ano em que hipoteticamente seria usado | ADR-0002, Seção 2.2 | Documentado como limitação no README (`Limitações do projeto` + `Possíveis evoluções futuras`), sem construir monitoramento (enunciado não exige) | Fechado — decisão tomada, não pendente |
| 4 | Proveniência do `Alunos.csv` é herdada da Fase 2, não confirmada por quem/quando foi baixado do INEP originalmente — sem o pacote oficial (pasta "Dicionário"), nenhuma validação de código de coluna é possível | `docs/HANDOFF_RENAN.md` linha 36 + `reports/proveniencia_alunos.md` | Nenhuma — pendência real, sem rota de resolução conhecida hoje | A confirmar (talvez o Renan tenha acesso ao pacote original) |
| 5 | `--full` (dado com território) depende de credencial GCP que só o Renan tem — se a call atrasar ou a extração falhar, o projeto fica preso no `--local-only` até o prazo de entrega | `docs/HANDOFF_RENAN.md`, `02_extrair_snapshot.py` | Nenhuma — dependência externa direta | Renan (execução), Luiz (prazo) |
| 6 | **Repetir o erro central da Fase 2**: entregar peça bem construída mas não conectada/não citada. Concretamente: os marts da Fase 2 respondem 2 das 5 perguntas de negócio, mas se o README não os citar explicitamente, o avaliador lê como "não respondido" | Feedback oficial da Fase 2 (`docs/FEEDBACK_FASE2_E_LICOES.md` §3): "o evento chega, é validado, é persistido, e para ali" | Auditoria linha a linha do enunciado criada (`docs/AUDITORIA_ENUNCIADO_FASE3.md`); README final deve citar cada mart reaproveitado pelo nome | Luiz (execução), Renan (revisão) |
| 7 | **Meta imputada pode virar artefato**: a feature `meta_alfabetizacao_2024_imputada` é majoritariamente imputada por KNN em algumas redes (só Municipal tem meta oficial do PDE) — o modelo pode aprender "quem teve meta imputada" em vez do sinal da meta | ADR-004 da Fase 2 (cobertura original 43,6%); mesmo padrão do risco já conhecido de `possui_historico_t1` (ADR-0001) | Flag `meta_is_imputada` derivado e incluído; extrator já alerta se >50% imputada; **checagem obrigatória no SHAP** | Renan (confirmar que não é leakage), Luiz (checar no SHAP) |

## Como usar

Antes da call: revisar linha por linha com o Renan, marcar cada uma como
**Aceito** (segue como está), **Mitigar** (ação definida) ou **Escalar**
(sem solução dentro do prazo — vira limitação documentada no README).
