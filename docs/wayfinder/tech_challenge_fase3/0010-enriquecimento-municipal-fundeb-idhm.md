# Ticket 0010 — Enriquecimento municipal (FUNDEB/IDHM-M)

**Status**: **fechado com resultado MISTO, não promovido a produção**
(2026-08-29). FUNDEB segue adiado (ADR-0009 §7). · **Aberto em**:
2026-08-29 · **ADR**: [0009](../../adr/0009-enriquecimento-municipal-fundeb-idhm.md)

## Resultado (ver ADR-0009 §8 para detalhe completo)

IDHM-M testado no ranking intra-UF: AUC ponderado sobe +0,0101 (0,6478 →
0,6579), mas o efeito por UF é misto — PE fecha (`inconclusivo` →
`modelo_vence`), MG e RN melhoram parcialmente, **BA regride**
(`inconclusivo` → `modelo_perde`). Não promovido a `04_ranking_intra_uf.py`
por decisão explícita: redistribuir incerteza entre UFs não é o mesmo que
reduzi-la. Capacidade fica pronta no código (`com_idhm=True`,
`FEATURES_IDHM`), desligada por padrão. Reproduzível via
`src/modeling/06_experimento_idhm.py`.

## O quê

Adicionar IDHM-M (PNUD/Atlas Brasil, 2010, constante) como feature nova do
ranking intra-UF (`src/modeling/04_ranking_intra_uf.py`), testando se fecha
parte das 17 UFs hoje com veredito `inconclusivo` em
`reports/ranking_intra_uf.json`. FUNDEB (SICONFI/Tesouro, anual) adiado
para rodada futura — 4 fontes tentadas sem sucesso sem fricção alta nesta
sessão (detalhe em ADR-0009 §7); retomar com navegação manual do Power BI
do FNDE quando houver tempo.

## Por quê

Único item de entrega ainda aberto do projeto (bridge 2026-08-29). Testa se
a lacuna das 17 UFs inconclusivas é falta de variável (contexto
socioeconômico ausente) ou falta de poder estatístico — pergunta em aberto
desde 2026-08-25.

## Passos (gates do `.claude/rules/dados.md`, nesta ordem)

1. **Gate de proveniência (MANUAL)** — sabatina humana antes de gerar EDA:
   fonte exata, timestamp real de atualização, rastro de extração. Registrar
   em `reports/proveniencia_fundeb.md` e `reports/proveniencia_idhm.md`.
2. **EDA** de cada dataset novo (`reports/eda_fundeb.md`,
   `reports/eda_idhm.md`) — os 9 itens do gate CRISP-DM, incluindo item 9
   (nulidade prediz alvo).
3. **Dicionário** — seções `## Colunas`, `## Conexão com objetivo de
   negócio`, `## Features criadas` em `reports/dicionario_alunos.md` (ou
   arquivo próprio, desde que coberto em algum dicionário do projeto).
4. **Join por `id_municipio`** (zfill 7) — medir e documentar cobertura
   real de cada fonte antes de decidir uso.
5. **Feature engineering** — FUNDEB entra temporal (por ano); IDHM entra
   constante (mesmo valor 2023/2024), com a limitação documentada.
6. **Re-treino** do ranking intra-UF com `comparar_pareado()` — IC95%
   bootstrap pareado do AUC ponderado + contagem de UFs que mudam de
   veredito, reportados juntos (nunca um sem o outro — ver ADR-0009 §2).

## Critério de sucesso / falsificação

- **Sucesso**: IC bootstrap pareado positivo com significância, e/ou UFs
  saindo de `inconclusivo` para `modelo_vence`.
- **Falha**: nem IC positivo nem UF muda de veredito — achado negativo,
  registrado como tal (mesmo tratamento do modelo aluno-nível).

## Referências

- ADR-0009 (este ticket)
- ADR-0004/0005/0006 (metodologia herdada: dobras adaptativas, baseline
  honesto, IC bootstrap pareado, ceiling analysis)
- `src/modeling/04_ranking_intra_uf.py`
