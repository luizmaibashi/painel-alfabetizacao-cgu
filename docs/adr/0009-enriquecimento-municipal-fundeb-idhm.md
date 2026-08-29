# ADR-0009: Enriquecimento municipal com FUNDEB e IDHM-M no ranking intra-UF

**Data**: 2026-08-29
**Status**: Accepted com resultado MISTO — **IDHM não promovido a
produção**. FUNDEB adiado (Seção 7). Resultado final do experimento na
Seção 8.
**Proposto por**: Luiz Maibashi
**Contexto**: Ticket 0010, próximo item aberto da frente `pos_tech`
(`brain/sessions/frentes/pos_tech.md`). Sabatina rodada via `/grill-with-docs`.

---

## 🤔 1. CONTEXTO (O QUÊ?)

O ranking intra-UF (`src/modeling/04_ranking_intra_uf.py`) é o único
entregável do projeto com resultado positivo: AUC 0,6478 contra 0,6209 do
baseline honesto, +0,027 IC95% [+0,007, +0,048] (ADR-0005). Usa 4 features
municipais: `taxa23`, `meta_alfabetizacao_2024`, `meta_alfabetizacao_2025`,
`populacao_total`.

**17 das 23 UFs no produto têm veredito `inconclusivo`** (IC bootstrap
pareado cruza zero) — nem vitória nem derrota do modelo contra o baseline,
ausência de evidência, não equivalência (distinção que o próprio README já
faz explícita, ver bridge 2026-08-29). Essas 17 UFs, junto com as 4
hipóteses candidatas já levantadas (poder estatístico, `taxa_falha_observada`,
`folga_media`, instabilidade ano a ano — citadas no bridge sob "ticket 0016"),
formam o pano de fundo deste ADR: **será que falta variável, não é falta de
poder estatístico?**

**Restrição de fonte, achada no Blind Spot Pass desta sessão:** IDHM-M
(PNUD/Atlas Brasil) não tem série municipal anual — o último ano com
cobertura municipal completa é **2010**. FUNDEB (SICONFI/Tesouro Nacional) é
anual, mas por sistema de nomenclatura/granularidade própria do Tesouro, não
IBGE — o join por `id_municipio` (7 dígitos, zfill) pode ter buracos de
cobertura que só a EDA real vai revelar.

---

## ⚙️ 2. DECISÃO (POR QUÊ?)

**O que escolhemos:** enriquecer com as duas fontes, tratadas de forma
diferente conforme a natureza temporal de cada uma:

1. **FUNDEB (anual)** entra como covariável temporal, mesmo tratamento de
   `taxa23`/`meta_alfabetizacao_2024` — varia por ano.
2. **IDHM-M (2010, sem série anual)** entra como covariável **estrutural
   constante** — mesmo valor em 2023/2024, papel análogo ao de
   `populacao_total` hoje (já é efetivamente constante no dataset atual).
   Não testa "IDHM mudou e explica a mudança de risco"; testa "desigualdade
   estrutural de base explica por que a direção do efeito (ADR-0005, MG vs.
   CE) é diferente entre UFs".
3. **Sem piso de cobertura mínima.** Ao contrário do piso de 40
   municípios/UF (ADR-0004, decisão diferente, sobre outra dimensão), aqui a
   cobertura real do join é documentada no dicionário/EDA e o
   `SimpleImputer` + IC bootstrap absorvem a incerteza — consistente com o
   resto do pipeline, que já reporta incerteza em vez de excluir por
   decreto.
4. **Critério de sucesso reportado em duas métricas, nunca uma só** —
   decisão explícita para não repetir o erro que o ADR-0005 já corrigiu
   uma vez neste projeto (ganho médio escondendo que vem de poucos casos):
   - IC95% bootstrap pareado do AUC ponderado, modelo com enriquecimento
     vs. modelo atual (mesma metodologia de `comparar_pareado()`).
   - Contagem de UFs que mudam de veredito `inconclusivo` → `modelo_vence`
     (não o inverso — perder cobertura seria regressão, reportar também se
     acontecer).

**Razão principal (ROI statement):**
"Se não fizéssemos: as 17 UFs inconclusivas ficam como lacuna aberta
indefinidamente, sem saber se é falta de sinal (nenhuma feature resolve) ou
falta desta feature específica (contexto socioeconômico ausente do
snapshot atual)."
"Se fizéssemos sem separar as duas métricas: um ganho médio positivo
pequeno poderia esconder que na prática só 2-3 UFs mudaram — mesma ilusão
que o baseline 0,4032 escondia antes do ADR-0005."

---

## 📊 3. CONSEQUÊNCIAS

**Positivas (esperadas):**
- Resposta empírica (não especulativa) para a pergunta "falta variável ou
  falta poder estatístico" nas 17 UFs inconclusivas.
- Reutiliza 100% da metodologia já validada (dobras adaptativas, IC
  bootstrap pareado, ADR-0004/0005) — sem gate metodológico novo a inventar.
- Gates de proveniência + EDA + dicionário do `.claude/rules/dados.md`,
  acionados por dataset novo, produzem `reports/proveniencia_fundeb.md`,
  `reports/proveniencia_idhm.md`, `reports/eda_<dataset>.md` e seção nova
  em `reports/dicionario_alunos.md` — documentação formal que hoje falta
  para qualquer dado municipal além de território/metas.

**Negativas (risco/custo):**
- IDHM 2010 pode estar desatualizado para municípios que mudaram muito na
  década — limitação a documentar explicitamente no dicionário, não
  esconder (mesmo padrão do Grupo 2 do ADR-0004: limite de fonte declarado,
  não escondido).
- Cobertura de FUNDEB por `id_municipio` desconhecida até a EDA rodar —
  pode ser baixa o suficiente para a feature virar maioria de imputação
  (a decidir com número real na mão, não a priori).
- Resultado pode ser negativo (nenhuma UF muda de veredito) — é resultado
  válido e documentável, não motivo para não tentar.

---

## 🎯 4. ALTERNATIVAS DESCARTADAS

| Opção | Vantagem | Por quê rejeitada |
|-------|----------|------------------|
| Só FUNDEB (mantém tudo anual/temporal) | Mais simples, sem covariável constante | Testa só "mais gasto → melhor resultado", hipótese mais fraca e já parcialmente coberta por `populacao_total`/`meta` como proxy indireto de recurso |
| Só IDHM primeiro, isolado | Testa hipótese de desigualdade estrutural sem ruído de FUNDEB | Custo de gate (proveniência/EDA/dicionário) é o mesmo para 1 ou 2 fontes — rodar as duas de uma vez é mais eficiente e o join por `id_municipio` é compartilhado |
| Exigir piso de cobertura mínima (ex.: 80%) antes de usar a feature | Protege contra feature majoritariamente imputada | Decisão prematura sem o número real — o piso de 40 do ADR-0004 resolve outro problema (amostra por UF pequena demais para treinar), não cobertura de coluna; aplicar o mesmo raciocínio aqui sem medir seria regra copiada sem revalidar motivo (AGENTS.md, regra de débito herdado) |

---

## 💰 5. IMPACTO ROI & VALIDAÇÃO

- **Métrica de sucesso:** `ganho_ic95` do AUC ponderado (bootstrap pareado,
  mesma função `comparar_pareado()` de `04_ranking_intra_uf.py`) positivo
  com significância, **e/ou** contagem de UFs que saem de `inconclusivo`
  registrada em `reports/ranking_intra_uf.json` (`veredito` por UF).
- **Timeline:** gate de proveniência (manual, sabatina humana) → EDA →
  dicionário → feature engineering → re-treino intra-UF com IC pareado.
- **Risco de regressão:** se a cobertura de FUNDEB ou IDHM vier muito baixa
  (a checar na EDA), a feature pode não ser usável — critério de decisão
  fica para quando o número real existir, não antes.
- **Cenário de falha (falsificação):** se o IC bootstrap pareado não for
  positivo com significância **e** nenhuma UF sair de `inconclusivo`, o
  achado é negativo — registrado como tal, mesmo tratamento dado ao modelo
  aluno-nível (resultado negativo é entregável válido neste projeto).

---

## 🔗 6. REFERÊNCIAS & LINKS

- `ADR-0004` — piso de 40 municípios/UF e dobras adaptativas (dimensão
  diferente: tamanho de amostra por UF, não cobertura de coluna).
- `ADR-0005` — correção da régua do baseline; motivo direto da decisão de
  reportar sucesso em duas métricas separadas.
- `ADR-0006` — ceiling analysis; lembrete de que "espaço de features
  insuficiente" é modo de falha distinto de "algoritmo fraco", relevante se
  o resultado vier negativo.
- `.claude/rules/dados.md` — gates de proveniência (MANUAL), EDA e
  dicionário, acionados por dataset novo.
- `src/modeling/04_ranking_intra_uf.py` — `treinar_por_uf()`,
  `comparar_pareado()`, `FEATURES` (lista a estender).
- Bridge `brain/sessions/frentes/pos_tech.md` — ticket 0010 e as 17 UFs
  inconclusivas (ticket 0016, referenciado em prosa, sem arquivo formal —
  achado do Blind Spot Pass desta sessão).

---

## 7. ADIAMENTO DO FUNDEB (2026-08-29, mesma sessão)

**FUNDEB fica fora desta rodada.** Quatro fontes tentadas, nenhuma
concluída sem fricção alta:

| Fonte | Resultado |
|---|---|
| Power BI (FNDE, "Painel FUNDEB", aba "Intraestadual") | Painel identificado, mas dado agregado nacional na tela inicial; export exige navegação manual interativa (fetch automatizado não renderiza Power BI) |
| SICONFI API (Tesouro Nacional) | Endpoint RREO confirmado (`apidatalake.tesouro.gov.br/ords/siconfi/tt/rreo`), mas anexo específico de FUNDEB/MDE não identificado em 3 buscas |
| Base dos Dados (`br-me-siconfi`) | Tabela existe (`municipio_receitas_orcamentarias`), mas download real exige BigQuery com conta GCP — decisão anterior desta sessão já descartou essa rota por quebrar o padrão "zero credencial" do projeto (README §3.2) |
| CNM (Confederação Nacional de Municípios) | Bloqueia acesso automatizado (HTTP 403); teria que ser navegação manual |

**Decisão:** seguir com **só IDHM-M** nesta rodada — fonte confirmada
(Atlas Brasil, export direto, zero credencial, zero fricção). FUNDEB vira
item adiado, não cancelado: retomar quando houver tempo para navegação
manual do Power BI (única rota sem custo de credencial que ainda não foi
esgotada — só falta um humano clicar em "Exportar dados" dentro do visual
"Intraestadual", filtrado por ano 2023).

**Impacto na Seção 2 (decisão original):** o item 1 ("FUNDEB entra como
covariável temporal") fica pendente. Os itens 2-4 (IDHM constante, sem piso
de cobertura, duas métricas de sucesso separadas) valem integralmente para
a rodada só-IDHM.

**Critério de sucesso desta rodada reduzida:** o mesmo do ADR original,
medindo só a contribuição do IDHM (sem FUNDEB somado) — se o resultado for
negativo com IDHM sozinho, ainda vale testar de novo quando FUNDEB entrar,
porque a combinação pode ter efeito que a feature isolada não tem.

---

## 8. RESULTADO DO EXPERIMENTO (2026-08-29) — MISTO, não promovido

**Executado:** `src/modeling/06_experimento_idhm.py` — treina o ranking
intra-UF duas vezes (com e sem as 4 features de IDHM), compara pareado por
UF via bootstrap (1000 reamostragens), reporta as duas métricas definidas
na Seção 2: IC bootstrap do AUC ponderado + contagem de UFs que mudam de
veredito.

**Cobertura do join confirmada:** 5.228/5.232 municípios (99,9%) — sem
piso necessário, decisão da Seção 2 item 3 se confirma na prática.

**Números:**

| Métrica | Valor |
|---|---|
| AUC ponderado sem IDHM | 0,6478 (idêntico ao produtizado, ADR-0005) |
| AUC ponderado com IDHM | 0,6579 |
| Diferença | +0,0101 |

**Mudanças de veredito** (usando a ordem de força
`modelo_perde < inconclusivo < modelo_vence` — corrigido depois de um bug no
critério inicial que só contava "inconclusivo→vence" e deixava passar
"inconclusivo→perde" sem contar como regressão, o mesmo gênero de erro que
o ADR-0005 já corrigiu uma vez: métrica agregada escondendo o que acontece
UF a UF):

| UF | Antes | Depois | Direção |
|---|---|---|---|
| PE | inconclusivo | **modelo_vence** | 🟢 fecha de vez |
| MG | modelo_perde | inconclusivo | 🟢 melhora parcial |
| RN | modelo_perde | inconclusivo | 🟢 melhora parcial |
| BA | inconclusivo | **modelo_perde** | 🔴 regride |

RJ (já `modelo_vence` antes) manteve o veredito, mas o AUC caiu com
significância (diferença pareada IC95% [−0,1816, −0,0222]) — sinal de
instabilidade que a contagem de veredito sozinha não capturaria.

**Classificação: MISTO.** Nem positivo puro (há regressão real em BA) nem
negativo puro (há melhora real em PE/MG/RN). O critério de falsificação
original (Seção 2) previa só positivo/negativo — "misto" é uma terceira
categoria que a formulação binária não cobria, e que só apareceu porque o
critério foi corrigido para contar TODAS as mudanças, não só as favoráveis.

**Decisão: não promover a `04_ranking_intra_uf.py`.** Um ganho agregado de
+0,01 que troca "1 UF inconclusiva vira vitória" por "1 UF inconclusiva
vira derrota" é redistribuição de incerteza entre estados, não redução
líquida dela — não é claramente melhor para o produto entregue. `FEATURES`
em produção continua `FEATURES_BASE` (4 colunas antigas); `FEATURES_IDHM`
existe no código como capacidade testada, não ativada.

**O que fica pronto para reativar, se uma investigação futura justificar:**
- `04_ranking_intra_uf.py` aceita `com_idhm=True` em `montar_dataset()` e
  `features=` em `treinar_por_uf()` — a mudança estrutural está feita e
  testada (7 testes de unidade novos, `tests/test_ranking_intra_uf.py`),
  só não está *ligada* por padrão.
- `src/modeling/06_experimento_idhm.py` reproduz o experimento completo a
  qualquer momento — determinístico, mesma seed, números idênticos em duas
  execuções independentes nesta sessão.
- Próximo passo natural, se retomado: investigar por que BA piora
  especificamente (outlier de IDHM? interação com `populacao_total`?) antes
  de tentar de novo — não tentado nesta sessão por decisão explícita de
  não abrir mais uma frente de investigação no mesmo dia.

## ✅ CRITÉRIA DE ACEITAÇÃO

- [ ] Gate de proveniência rodado (sabatina humana) para FUNDEB e IDHM,
      registrado em `reports/proveniencia_fundeb.md` /
      `reports/proveniencia_idhm.md`.
- [ ] EDA de cada dataset novo (`reports/eda_fundeb.md`,
      `reports/eda_idhm.md`), cobrindo os 9 itens do gate CRISP-DM.
- [ ] Dicionário atualizado (`reports/dicionario_alunos.md` ou arquivo
      próprio) com seções `## Colunas`, `## Conexão com objetivo de
      negócio`, `## Features criadas`.
- [ ] Cobertura real do join por `id_municipio` documentada (% de
      municípios com valor não-nulo em cada fonte).
- [ ] Re-treino do ranking intra-UF com as features novas, IC bootstrap
      pareado reportado.
- [ ] Contagem de UFs que mudam de veredito reportada ao lado do AUC
      ponderado — nunca uma métrica sem a outra.
- [ ] Limitação do IDHM 2010 (sem atualização anual) documentada
      explicitamente, não escondida.
