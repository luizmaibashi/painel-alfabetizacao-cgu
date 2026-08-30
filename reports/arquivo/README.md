# Arquivo — artefatos obsoletos

Artefatos versionados que ficaram desatualizados e foram movidos pra cá em
vez de deletados, por honestidade de histórico. Nenhum é referenciado por
README/HANDOFF/código — se algo aqui voltar a ser citado, mova de volta pra
`reports/` e remova o sufixo `_OBSOLETO_*`.

## `dossie_fase3_OBSOLETO_2026-08-29.html`

Versionado manualmente (não gerado por script, ao contrário de
`painel_intra_uf.html`) em 22-29/08. Zero referências em qualquer `.md`/`.py`
do projeto — órfão desde a criação, nunca foi a fonte de verdade oficial
(essa é o `README.md`).

Congelado antes de 3 decisões que mudaram números centrais do projeto:

- ADR-0008 (skew treino-serviço, histórico t-1)
- ADR-0009 (enriquecimento municipal FUNDEB/IDHM)
- ADR-0010 (painel derivado do backtest, contrato de uso condicional)

Números que aparecem nele (AUC, régua do baseline intra-UF) **não devem ser
citados** sem conferir contra `README.md` e `reports/backtest_prospectivo_2025.json`
primeiro — provavelmente divergem do estado atual.

## `MODEL_CARD_OBSOLETO_2026-08-29.md`

Mesmo padrão do dossiê acima: "versão 1.0" datada 29/08, zero referências em
qualquer `.md`/`.py` do projeto, órfão desde a criação. Cita AUC 0,6478 pro
ranking intra-UF — número **pré-ADR-0005** (régua do baseline corrigida,
ganho caiu de +0,245 pra +0,027) e **pré-backtest prospectivo 2025**
(número atual e canônico: AUC modelo 0,6167 vs baseline 0,4523, ver README).
Não usar nenhum número deste arquivo sem conferir a fonte atual primeiro.

Se o projeto precisar de um model card pra entrega, **recriar do zero** a
partir do estado atual (README + `docs/adr/0010-*.md`), não editar este.
