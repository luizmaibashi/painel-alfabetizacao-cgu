# Dicionário de Dados — `idhm` (Atlas do Desenvolvimento Humano)

**Dataset coberto:** `idhm` — `dados_externos/idhm_municipio_2010.csv`
(filtrado do bruto `dados_externos/idhm_municipio_1991_2010.csv.gz`, ano
2010, único com série municipal completa).

Proveniência: `reports/proveniencia_idhm.md`. EDA: `reports/eda_idhm.md`.

## Conexão com objetivo de negócio

**Objetivo do dataset**: testar se desigualdade estrutural municipal
(IDHM-M e componentes) explica parte da variância que o ranking intra-UF
(`src/modeling/04_ranking_intra_uf.py`) não captura — hoje 17 das 23 UFs
têm veredito `inconclusivo` (IC bootstrap pareado cruza zero).

**Hipótese a confirmar/refutar**: municípios com IDHM mais baixo podem ter
mecanismo de risco diferente dos municípios com IDHM alto (análogo aos
mecanismos já medidos em MG — regressão à média — e CE — teto de meta,
ADR-0005) — e essa diferença estrutural pode ser o que falta para separar
sinal de ruído nas UFs hoje inconclusivas.

**Sabatina de conexão**: rodada via `/grill-with-docs` na sessão de
2026-08-29, resultado formalizado em `ADR-0009`. Decisão-chave: IDHM entra
como covariável **constante** (não temporal) — mesmo valor 2023/2024 do
ranking intra-UF, porque a fonte não tem série anual (2010 é o ano mais
recente com cobertura municipal completa).

Ancorado em `docs/adr/0009-enriquecimento-municipal-fundeb-idhm.md` e
`docs/wayfinder/tech_challenge_fase3/0019-enriquecimento-municipal-fundeb-idhm.md`
(raiz da base — renomeado de 0010 em 2026-08-30, colidia com ticket homônimo
já existente naquela árvore).

## Colunas (pós-limpeza)

O dataset bruto tem 180+ variáveis (ver `reports/eda_idhm.md`, seção
"Colunas e tipos"). Só as colunas abaixo são candidatas a entrar no
`FEATURES` de `04_ranking_intra_uf.py` — as demais ficam no arquivo, não
descartadas fisicamente, mas fora do escopo desta rodada (ADR-0009 não
testa 180 variáveis, testa o índice-síntese e seus 3 componentes).

| Coluna | Tipo | Significado | Interpretação de negócio | Decisão de uso |
|---|---|---|---|---|
| `id_municipio` | int (7 dígitos, sem zfill no CSV — **cast obrigatório** antes do join) | Código IBGE do município | Chave de join com `ranking_intra_uf` | Chave — `astype(str).str.zfill(7)` antes de qualquer merge (mesma regra ADR-005 da Fase 2, já aplicada no restante do projeto) |
| `ano` | int | Sempre 2010 nesta versão filtrada | Não é temporal aqui — é o ano-base do censo que gerou o índice | **Não é feature** — descartar na hora do merge (é constante, entraria como "coluna 100% igual" no gate 2 do EDA se deixada) |
| `idhm` | float [0,1] | Índice de Desenvolvimento Humano Municipal — média geométrica de `idhm_e`, `idhm_l`, `idhm_r` | Síntese de desigualdade estrutural do município (educação + longevidade + renda) | **Feature principal** — candidata direta a testar no ranking intra-UF |
| `idhm_e` | float [0,1] | Sub-índice Educação (escolaridade adulta + frequência escolar jovem) | Mede acesso/permanência escolar histórica do município, distinto do desempenho anual do PDE | Feature — mais próxima conceitualmente do domínio do problema (educação) que os outros dois sub-índices |
| `idhm_l` | float [0,1] | Sub-índice Longevidade | Proxy de saúde/expectativa de vida — **redundante com `expectativa_vida` por definição do índice** (corr 1.000, EDA item 7) | Feature candidata, mas correlação com `expectativa_vida` não é achado — é como o IDHM-L é calculado. Não usar as duas juntas se `expectativa_vida` também entrar (não é o caso aqui, ela não está no `FEATURES` de nenhum script do projeto) |
| `idhm_r` | float [0,1] | Sub-índice Renda | Renda per capita municipal normalizada | Feature candidata — mede poder aquisitivo, dimensão que `populacao_total` (já usada no modelo) não cobre |

**Todas as demais 180+ colunas do dataset bruto** (população por faixa
etária, taxas de trabalho, indicadores de moradia, etc.) **ficam fora do
`FEATURES`** desta rodada — não avaliadas individualmente, por estarem fora
do escopo do ADR-0009 (testar IDHM-M como hipótese de desigualdade
estrutural, não fazer feature engineering extensivo sobre 180 variáveis
socioeconômicas).

## Features criadas

Nenhuma feature derivada nesta etapa — as 4 colunas candidatas (`idhm`,
`idhm_e`, `idhm_l`, `idhm_r`) entram no `FEATURES` de
`04_ranking_intra_uf.py` **como estão**, sem transformação, além do cast de
`id_municipio` para join. Qualquer feature derivada (ex.: quintil de IDHM,
interação IDHM × população) fica para uma rodada futura, condicionada ao
resultado desta primeira (ADR-0009, critério de falsificação).

## Qualidade e cobertura (resumo da EDA)

- **0 duplicatas, 0 nulos** em qualquer coluna (`reports/eda_idhm.md`).
- **Cobertura do join**: 5.212 de 5.216 municípios do `ranking_intra_uf.json`
  têm match em `id_municipio` — **99,92%**. Sem piso de cobertura mínima
  necessário (decisão do ADR-0009 §2 item 3 se confirma na prática: a
  cobertura veio alta o suficiente para não precisar de exceção).
- Os 4 municípios sem match não identificados individualmente nesta rodada
  — se relevante, investigar depois (não bloqueia o teste principal, cai em
  `SimpleImputer` como o resto do pipeline já faz).
