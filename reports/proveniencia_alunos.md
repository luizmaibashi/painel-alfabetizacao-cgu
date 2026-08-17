# Proveniência — dataset `alunos` (snapshot_modelagem)

**Gate:** `.claude/rules/dados.md` — GATE CRISP-DM Verificação de Origem (manual)
**Data do preenchimento:** 2026-08-17

## Fonte

INEP — microdados. Origem confirmada, mas **exportação manual e o próprio Luiz tem incerteza residual** ("se não me engano") sobre os detalhes exatos do processo. Sistema: microdados do INEP (Censo Escolar — não confirmado com 100% de certeza, mas é a hipótese mais provável dado o contexto do projeto).

## Timestamp da fonte

Dados referentes aos **ciclos 2023 e 2024**. A data exata de atualização na origem (INEP) não foi confirmada — o que se sabe é o ciclo/ano de referência dos microdados, não o timestamp de publicação no portal. Download foi feito **uma única vez** (sem histórico de re-download/atualização).

**Lacuna documentada, não inventada:** não há confirmação de que os ciclos 2023/2024 são efetivamente os mais recentes disponíveis no INEP no momento da modelagem — vale conferir antes da call com Renan.

## Rastro de extração

Download **direto do portal de microdados do INEP** (sem filtro/query intermediário relatado). Luiz confirma que **consegue reproduzir o download hoje** seguindo os mesmos passos — reprodutibilidade OK, mas o passo a passo exato (URL, filtros aplicados na tela) não foi documentado neste momento.

## Itens em aberto (não bloqueantes, mas registrados)

- Confirmar qual base exata do INEP (Censo Escolar vs. outro microdado) — sinalizado como incerto pelo próprio Luiz.
- Confirmar se 2023/2024 são os ciclos mais atuais disponíveis, ou se há dado mais recente não capturado.
- Documentar o passo a passo de reprodução do download (URL + filtros), já que Luiz confirma que consegue refazer.

## Atualização — contradição encontrada (2026-08-17, sessão de refinamento)

Ao investigar `caderno=12` (ver seção abaixo), o `docs/HANDOFF_RENAN.md` (linha 36) registra: *"`Alunos.csv` (microdados SAEB, **já tínhamos na Fase 2**)"*. Isso contradiz a leitura inicial de "exportei manualmente agora" — o arquivo já existia desde a Fase 2 do curso, o que é coerente com a incerteza que Luiz sinalizou ("se não me engano"): ele pode não ter sido quem baixou originalmente, ou baixou na Fase 2 e não lembra os detalhes hoje.

**Pendência real, não resolvida:** confirmar quem/quando baixou o `Alunos.csv` originalmente (Fase 2) e se o pacote de microdados original do INEP (com a pasta "Dicionário") ainda está acessível. Luiz confirmou em 2026-08-17 que **não lembra** se tem esse pacote — verificar em casa.

## Investigação `caderno=12` — status: hipótese reforçada, NÃO confirmada

**Hipótese:** `caderno=12` (236 alunos, 86,9% "Não" vs. ~50% dos demais cadernos) é uma versão adaptada/acessibilidade da prova SAEB (Braille, macrotipo, instrumento adaptado), não uma variação neutra de conteúdo (anti-cola).

**Suporte encontrado (pesquisa web, 2026-08-17):** SAEB regular usa desenho BIB com 21-26 cadernos por combinação de blocos de conteúdo — nosso dataset só tem 4 valores distintos (1, 10, 11, 12), o que já destoa do padrão de cadernos "de conteúdo". SAEB também documenta cadernos de acessibilidade separados (Braille, macrotipo, adaptado) para necessidades especiais. Fontes: [SAEB — Microdados INEP](https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/microdados/saeb), [Diretrizes SAEB 2025](https://download.inep.gov.br/publicacoes/institucionais/avaliacoes_e_exames_da_educacao_basica/cartilha_saeb_2025_diretrizes_da_edicao.pdf).

**Não confirmado:** o código oficial `12` não foi cruzado com o Dicionário de Variáveis do pacote de microdados do INEP (não está disponível localmente nem indexado em busca web). Sem esse cruzamento, a hipótese fica em "reforçada por analogia", não "validada".

**Próximo passo real (retomar em casa):** localizar o pacote de microdados original do INEP (pasta "Dicionário") ou baixar novamente do portal oficial, e conferir o código de `caderno=12` no dicionário de variáveis. Até lá, a decisão de incluir `caderno` como feature (`reports/dicionario_alunos.md`, já marcada "com ressalva") permanece condicional a essa confirmação.
