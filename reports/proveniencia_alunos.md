# Proveniência — dataset `alunos` (snapshot_modelagem)

**Gate:** `.claude/rules/dados.md` — GATE CRISP-DM Verificação de Origem (manual)
**Data do preenchimento:** 2026-08-17

## Fonte

INEP — microdados. Origem confirmada, mas **exportação manual e o próprio Luiz tem incerteza residual** ("se não me engano") sobre os detalhes exatos do processo. Sistema: **atualizado em 2026-08-18** — não é Censo Escolar (hipótese inicial, descartada); é o **Indicador Criança Alfabetizada / Pesquisa Alfabetiza Brasil (2023)**, identificado via basedosdados.org (https://basedosdados.org/dataset/073a39d4-89cf-4068-b1e8-34ed0d9c0b72?table=bb27c746-18df-4ba8-8f98-5110232e2162) — coerente com o corte de 743 pts na escala Saeb e a coluna `alfabetizado`.

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

Ao investigar `caderno=12` (ver seção abaixo), o o diário de bordo interno (não publicado) (linha 36) registra: *"`Alunos.csv` (microdados SAEB, **já tínhamos na Fase 2**)"*. Isso contradiz a leitura inicial de "exportei manualmente agora" — o arquivo já existia desde a Fase 2 do curso, o que é coerente com a incerteza que Luiz sinalizou ("se não me engano"): ele pode não ter sido quem baixou originalmente, ou baixou na Fase 2 e não lembra os detalhes hoje.

**Pendência real, não resolvida:** confirmar quem/quando baixou o `Alunos.csv` originalmente (Fase 2) e se o pacote de microdados original do INEP (com a pasta "Dicionário") ainda está acessível. Luiz confirmou em 2026-08-17 que **não lembra** se tem esse pacote — verificar em casa.

## Investigação `caderno=12` — ✅ RESOLVIDA em 2026-08-18 (não era acessibilidade)

> **RESPOSTA:** `caderno=12` é **proxy de ausência à prova**, não caderno
> adaptado. 79,7% dos seus alunos faltaram (contra 12-16% dos outros cadernos),
> e entre os que compareceram o desempenho é **melhor** que a média (37,3% de
> "Não" contra ~41%). Os 87,3% que motivaram esta investigação eram inteiramente
> artefato de ausência.
>
> **Como foi resolvido:** um `crosstab` de `caderno` contra `presenca` na base
> completa. As 3 tentativas registradas abaixo — portal do INEP, basedosdados.org
> e o PDF do relatório técnico — buscavam a resposta na documentação externa, e
> ela estava no próprio dado. Fica o registro do contraste de método.
>
> Detalhe completo no Cap. 11.3 do diário de bordo interno (não publicado).

### Histórico da investigação (mantido: mostra o caminho até a resposta)

**Hipótese:** `caderno=12` (236 alunos, 86,9% "Não" vs. ~50% dos demais cadernos) é uma versão adaptada/acessibilidade da prova, não uma variação neutra de conteúdo (anti-cola).

**Suporte encontrado (pesquisa web, 2026-08-17):** SAEB regular usa desenho BIB com 21-26 cadernos por combinação de blocos de conteúdo — nosso dataset só tem 4 valores distintos (1, 10, 11, 12), o que já destoa do padrão de cadernos "de conteúdo". SAEB também documenta cadernos de acessibilidade separados (Braille, macrotipo, adaptado) para necessidades especiais. Fontes: [SAEB — Microdados INEP](https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/microdados/saeb), [Diretrizes SAEB 2025](https://download.inep.gov.br/publicacoes/institucionais/avaliacoes_e_exames_da_educacao_basica/cartilha_saeb_2025_diretrizes_da_edicao.pdf).

### Correção de premissa (2026-08-18)

Luiz trouxe uma definição genérica de `caderno` ("código do caderno atribuído ao aluno na prova de língua portuguesa") e o link da tabela no basedosdados.org
(https://basedosdados.org/dataset/073a39d4-89cf-4068-b1e8-34ed0d9c0b72?table=bb27c746-18df-4ba8-8f98-5110232e2162).
Isso identificou a base de origem com precisão: **não é o SAEB clássico/Prova Brasil** — é o **Indicador Criança Alfabetizada / Pesquisa Alfabetiza Brasil (2023)**, avaliação mais nova (divulgada desde 2024) com prova bem menor — **16 itens de múltipla escolha + 3 de resposta construída**, contra os 169 itens do SAEB tradicional que geram os 21-26 cadernos.

**Isso enfraquece a analogia usada em 2026-08-17**: o raciocínio "SAEB tem 21-26 cadernos de conteúdo + cadernos de acessibilidade separados" foi construído em cima do SAEB clássico, uma prova de estrutura bem diferente desta. Não invalida a hipótese de acessibilidade (é plausível que qualquer prova em larga escala do INEP tenha versão adaptada), mas a base de comparação estava errada — o suporte anterior é mais fraco do que registrado.

**Ainda não confirmado:** a página do basedosdados.org é uma aplicação client-side (React) — o fetch automatizado não consegue ler o dicionário de valores da coluna (só a casca da página). A página oficial do INEP sobre esses microdados está com acesso restrito (login gov.br exigido). **Checagem real pendente**: abrir o link do basedosdados.org num navegador e inspecionar a coluna `caderno` diretamente — só um humano com a página renderizada consegue ver isso agora.

**Próximo passo real:** Luiz abrir https://basedosdados.org/dataset/073a39d4-89cf-4068-b1e8-34ed0d9c0b72?table=bb27c746-18df-4ba8-8f98-5110232e2162 no navegador e checar se a coluna `caderno` tem dicionário de valores (1, 10, 11, 12 → significado). Alternativa: localizar o pacote de microdados original do INEP (pasta "Dicionário") do Indicador Criança Alfabetizada. Até lá, a decisão de incluir `caderno` como feature (`reports/dicionario_alunos.md`, já marcada "com ressalva") permanece condicional a essa confirmação.

### Beco sem saída, por ora (2026-08-18)

Luiz checou o basedosdados.org no navegador: **não há dicionário de valores pra `caderno` nessa página** (confirma o limite que o fetch automatizado já tinha sinalizado). As duas rotas tentadas hoje (INEP direto — acesso restrito; basedosdados.org — sem dicionário de coluna) **não resolveram**. A hipótese de acessibilidade permanece "plausível por analogia geral com avaliações do INEP em larga escala", sem confirmação — status inalterado desde 2026-08-17, agora com duas tentativas documentadas de fechar a lacuna e nenhuma bem-sucedida.

**Rotas tentadas e esgotadas nesta sessão:** (1) INEP direto — acesso restrito (login gov.br); (2) basedosdados.org — sem dicionário de valores pra coluna; (3) relatório técnico da Pesquisa Alfabetiza Brasil em PDF (https://download.inep.gov.br/publicacoes/institucionais/avaliacoes_e_exames_da_educacao_basica/relatorio_da_pesquisa_alfabetiza_brasil.pdf) — fetch falhou por erro de certificado/conexão do servidor do INEP, não é limite de conteúdo, é técnico. Pode valer tentar abrir esse PDF direto no navegador (fora do Claude) numa sessão futura.

**Rotas ainda não tentadas:** contato direto com suporte do INEP; localizar pacote de microdados original (se existir, fora do portal restrito).

**Decisão prática pra seguir o projeto:** tratar `caderno=12` como risco documentado e não resolvido (já está assim no `dicionario_alunos.md`), sem bloquear a Seção 2 do plano de refinamento por causa disso.
