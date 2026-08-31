# Architecture Decision Records — Tech Challenge Fase 3

Migrado em 2026-08-20 de `docs/wayfinder/tech_challenge_fase3/adr/` (local
provisório) para cá. Repositório GitHub próprio da Fase 3 segue não criado
(ticket 0004 em `docs/wayfinder/tech_challenge_fase3/`) — se for criado,
esta pasta migra de novo.

## Index

| ADR | Título | Status | Data |
|-----|--------|--------|------|
| [0001](0001-pipeline-sklearn-snapshot-e-politica-leakage.md) | Pipeline sklearn sobre snapshot único do Gold + política de data leakage e validação temporal | Proposed | 2026-08-10 |
| [0002](0002-modelo-final-validacao-temporal-e-tratamento-caderno.md) | Modelo final, validação temporal e tratamento do campo `caderno` | Proposed | 2026-08-18 |
| [0003](0003-gold-vs-silver-fonte-de-dados.md) | Gold vs Silver como fonte de dados | Accepted | 2026-08-19 |
| [0004](0004-validacao-adaptativa-ranking-intra-uf.md) | Validação adaptativa e piso de amostra no ranking intra-UF | Accepted (manchete superseded pelo 0005) | 2026-08-20 |
| [0005](0005-correcao-da-regua-do-baseline-intra-uf.md) | Correção da régua do baseline intra-UF e a inversão de direção entre estados | Accepted | 2026-08-20 |
| [0006](0006-ceiling-analysis-como-gate-pre-treino.md) | Ceiling analysis como gate pré-treino | Accepted com correção (§7 método, §7.1 número) | 2026-08-22 |
| [0007](0007-determinismo-de-execucao-como-requisito-de-entrega.md) | Determinismo de execução como requisito de entrega | Accepted | 2026-08-25 |
| [0008](0008-skew-treino-servico-nas-features-de-historico.md) | Features de histórico t-1 são não-funcionais no split temporal (skew treino-serviço) | Aceito | 2026-08-29 |
| [0009](0009-enriquecimento-municipal-fundeb-idhm.md) | Enriquecimento municipal FUNDEB/IDHM (resultado misto, não promovido) | Aceito | 2026-08-29 |
| [0010](0010-painel-derivado-do-backtest-com-contrato-de-uso-condicional.md) | Painel derivado do backtest prospectivo, com contrato de uso condicional no artefato | Aceito | 2026-08-30 |
| [0011](0011-enriquecimento-infraestrutura-censo-escolar.md) | Enriquecimento com infraestrutura escolar do Censo Escolar (resultado misto, não promovido) | Aceito | 2026-08-31 |

> **Nota de 2026-08-25:** o ADR-0006 existia desde 22/08 mas **nunca tinha sido
> adicionado a este índice** — mais uma ocorrência do padrão que o próprio 0007
> documenta (artefato criado, registro não atualizado). Incluído junto com o 0007.
>
> **Nota de 2026-08-30:** os ADR-0008 e 0009 também não tinham sido indexados —
> mesmo padrão de novo. Incluídos junto com o 0010.
>
> **Nota de 2026-08-31:** o ADR-0011 foi indexado **na mesma sessão em que foi
> criado** — primeira vez que o padrão documentado acima (artefato criado,
> registro não atualizado) não se repetiu.
