# Tech Challenge Fase 3 — Predição de Alfabetização por Aluno

> **Em planejamento/estruturação.** O README completo (11 seções exigidas
> pelo enunciado: contexto, objetivo, base, modelagem, métricas,
> interpretação, insights, limitações, aplicação prática, evoluções
> futuras) só será escrito quando houver resultado de modelo pra reportar.

## Comece por aqui

- [`docs/HANDOFF_RENAN.md`](docs/HANDOFF_RENAN.md) — **documento vivo do
  projeto**: de onde viemos (feedback da Fase 2), decisões técnicas e por quê,
  auditoria contra o enunciado, riscos abertos e o que falta. É o único
  documento necessário pra entender o projeto inteiro.
- [`docs/CONTEUDO_AULAS_RELEVANTE.md`](docs/CONTEUDO_AULAS_RELEVANTE.md) —
  conteúdo das aulas do curso conectado às decisões técnicas do projeto.
- `reports/eda_alunos.md` — EDA real sobre a amostra de `Alunos.csv`.
- `reports/dicionario_alunos.md` — dicionário de dados + conexão com
  objetivo de negócio.
- `src/preprocessing/02_extrair_snapshot.py` — script de extração do
  snapshot de modelagem (modo `--local-only` funciona; `--full` precisa de
  credencial GCP).

## Planejamento completo (spec + ADR + histórico de decisões)

Vive na base de conhecimento, fora deste repo por enquanto:
`docs/wayfinder/tech_challenge_fase3/` — `SPEC_FINAL.md`, `adr/0001-*.md` e
os 6 tickets do wayfinder. Migra pra cá quando o repo for publicado no
GitHub.
