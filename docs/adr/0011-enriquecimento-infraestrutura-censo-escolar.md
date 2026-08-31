# ADR-0011: Enriquecimento com infraestrutura escolar (Censo Escolar INEP)

**Data**: 2026-08-31
**Status**: Accepted com resultado MISTO — **infraestrutura não promovida a
produção**. Resultado do experimento na Seção 7; achado que ele abriu na
Seção 8; placebo que o testa na Seção 9.
**Proposto por**: Luiz Maibashi
**Contexto**: Investigação para o 2º Concurso de Reúso de Dados Abertos da
CGU (`PROJETOS/01_PRIORITY/Concurso-CGU/`), mas o enriquecimento é autorizado
pelo próprio enunciado da Pós-Tech (pág. 3-4: "IBGE; Censo Escolar; FUNDEB;
Atlas do Desenvolvimento Humano; PNAD; Cadastro Único") — entra como melhoria
legítima do entregável acadêmico, não como escopo à parte.

---

## 🤔 1. CONTEXTO (O QUÊ?)

O backtest prospectivo 2025 (ADR-0010, imutável) classifica as 23 UFs em três
grupos: 14 onde o modelo vence, 1 (CE) onde a regra simples vence, e **8 onde
o resultado é inconclusivo** — o IC bootstrap pareado cruza zero e o produto
abstém de recomendação.

Essas 8 UFs inconclusivas hoje ficam sem explicação: sabe-se *que* o modelo
não decide ali, não se sabe *por quê*. O ADR-0009 já tentou responder pergunta
parecida com IDHM-M (estrutural, 2010) e FUNDEB (adiado por fricção de
acesso) — resultado misto, capacidade testada mas não promovida.

**Achado desta investigação:** o Censo Escolar (INEP) publica microdados por
escola com `CO_MUNICIPIO` (código IBGE de 7 dígitos, mesmo padrão de
`id_municipio` já usado no projeto). Testado e confirmado nesta sessão:

- Download direto, sem autenticação (`download.inep.gov.br`), zero fricção
  — diferente do FUNDEB (Power BI manual, SICONFI sem anexo localizável,
  BigQuery com credencial, CNM bloqueado por 403).
- 217.625 escolas no arquivo 2023; 180.230 em atividade.
- **Cobertura de município: 5.570/5.570 (100%)** — universo nacional
  completo, sem buracos.
- Indicadores binários (`IN_*`) de infraestrutura por escola: água potável,
  energia, esgoto, internet (inclusive `IN_INTERNET_ALUNOS`, distinto de
  internet só administrativa), biblioteca, laboratórios, acessibilidade.

**Restrição já conhecida (README, linha 586):** enriquecimento por **escola**
já foi tentado e falhou — `id_escola` do dataset de alunos é sintético
(60000002–60042811), sem correspondência com `CO_ENTIDADE` oficial do INEP
(prefixo de UF, 11-53). **Este ADR propõe join só em nível de município**
(`CO_MUNICIPIO` agregado → `id_municipio`), granularidade onde essa restrição
não se aplica — é a mesma chave que já sustenta IDHM/FUNDEB no ADR-0009.

---

## ⚙️ 2. DECISÃO (POR QUÊ?)

**Proposta:** agregar o Censo Escolar 2023 por município (% de escolas ativas
com cada indicador de infraestrutura) e testar, com a **mesma metodologia já
validada no ADR-0009**, se essas features mudam o veredito das UFs
inconclusivas — sem tocar no backtest 2025 imutável.

1. **Feature estrutural, não temporal** — Censo Escolar entra como
   `com_infra=True` em `montar_dataset()` (mesmo padrão de `com_idhm=True`),
   ano fixo (2023), mesma limitação declarada explicitamente (não escondida).
2. **Sem piso de cobertura mínimo a priori** — coerente com a decisão já
   tomada no ADR-0009 item 3 (evitar regra copiada sem revalidar motivo); com
   100% de cobertura confirmada, essa cautela nem se aplica aqui.
3. **Duas métricas de sucesso, nunca uma só** — mesma lição do ADR-0005/0009:
   IC bootstrap pareado do AUC ponderado **e** contagem de UFs que mudam de
   veredito (incluindo regressões, não só melhoras).
4. **Escopo do experimento fica em script novo** (`08_experimento_infra_escolar.py`,
   mesmo padrão do `06_experimento_idhm.py`) — não altera
   `05_backtest_prospectivo_2025.py` nem `reports/backtest_prospectivo_2025.json`.
   Só é promovido a produto se o resultado justificar, com decisão explícita
   registrada (mesmo tratamento dado ao IDHM: "testado, resultado documentado,
   promovido ou não").

**Razão principal (ROI statement):**
"Se não fizéssemos: as 8 UFs inconclusivas continuam sem hipótese testada de
causa — depois do IDHM (estrutural, adiado por não ter série anual) e do
FUNDEB (adiado por fricção de acesso), infraestrutura escolar é a terceira
candidata óbvia da lista do próprio enunciado, e a única sem barreira de
acesso conhecida."
"Se prometêssemos resultado positivo antes de medir: repetiríamos o erro que
o ADR-0005 já corrigiu — o IDHM pareceu promissor (+0,01 agregado) e o exame
UF a UF revelou regressão real em BA. Este ADR não assume que vai funcionar."

---

## 📊 3. CONSEQUÊNCIAS

**Positivas (esperadas):**
- Terceira tentativa de explicar as UFs inconclusivas, com a fonte de menor
  fricção de acesso das três (IDHM, FUNDEB, Censo Escolar).
- Reaproveita 100% da infraestrutura de teste pareado já construída
  (`comparar_pareado()`, bootstrap, `tests/test_ranking_intra_uf.py`).
- Achado nacional já observável mesmo sem o teste de UF: só 44,7% das
  escolas ativas têm internet disponível pro aluno (vs. 87,2% com
  computador) — gap de conectividade documentável independente do resultado
  do modelo.

**Negativas (risco/custo):**
- Pode repetir o padrão MISTO do IDHM (melhora em algumas UFs, regride em
  outras) — resultado válido e documentável, não motivo para não tentar,
  mas não pode ser vendido como vitória se vier misto ou negativo.
- Ano único (2023) — se o Censo Escolar 2024/2025 já estiver disponível e
  divergir muito, a escolha do ano fica como limitação declarada.
- Indicadores binários por escola agregados em % têm janela de agregação a
  decidir (média simples vs. ponderada por matrícula) — decisão de EDA, não
  deste ADR.

---

## 🎯 4. ALTERNATIVAS DESCARTADAS

| Opção | Vantagem | Por quê rejeitada |
|-------|----------|------------------|
| Join em nível de escola (não de município) | Granularidade mais fina, sinal potencialmente mais forte | Já comprovadamente inviável — `id_escola` sintético sem correspondência com `CO_ENTIDADE` (README linha 586) |
| Retomar FUNDEB em vez de Censo Escolar | Resposta a hipótese de recurso financeiro, não só infraestrutura física | Fricção de acesso não resolvida (Power BI manual); Censo Escolar testa hipótese adjacente (infraestrutura) com zero fricção — não mutuamente exclusivo, mas prioridade pela viabilidade |
| Adicionar direto ao backtest 2025 canônico, sem experimento isolado | Menos arquivos, decisão mais rápida | Violaria o princípio já estabelecido de manter o backtest imutável (ticket 0018) e pularia a etapa de medir antes de prometer (ADR-0005) |

---

## 💰 5. IMPACTO ROI & VALIDAÇÃO

- **Métrica de sucesso:** IC bootstrap pareado do AUC ponderado (mesma função
  `comparar_pareado()`) **e** contagem de UFs que mudam de veredito nas duas
  direções — mesmo padrão do ADR-0009.
- **Timeline:** EDA de agregação (`reports/eda_censo_escolar.md`) →
  dicionário → feature engineering → experimento isolado → decisão de
  promoção ou não.
- **Cenário de falha (falsificação):** se nenhuma UF sair de `inconclusivo`
  **e** o IC não for positivo com significância, resultado negativo,
  registrado como tal — mesmo padrão do modelo aluno-nível e do IDHM.

---

## 🔗 6. REFERÊNCIAS & LINKS

- `ADR-0009` — padrão de enriquecimento municipal, motivo das duas métricas
  de sucesso, motivo de não impor piso de cobertura a priori.
- `ADR-0010` — backtest 2025 imutável; este ADR não o altera.
- `README.md` linha 586 — restrição de join por escola (`id_escola`
  sintético), motivo do enriquecimento ser só em nível de município.
- `reports/eda_censo_escolar.md` — EDA dos 9 itens do gate CRISP-DM.
- `reports/dicionario_censo_escolar.md` — proveniência, recorte da população,
  colunas, features criadas e a predição registrada antes da medição.
- `dados_externos/censo_escolar_municipio_2023.csv` — agregado municipal,
  regenerável por `src/preprocessing/06_agregar_censo_escolar.py`.
- Enunciado Tech Challenge Fase 3, pág. 3-4 — autorização explícita de
  enriquecimento com Censo Escolar.

---

## ✅ CRITÉRIOS DE ACEITAÇÃO

- [ ] EDA formal do agregado (`reports/eda_censo_escolar.md`), cobrindo os 9
      itens do gate CRISP-DM.
- [ ] Dicionário atualizado com as colunas de infraestrutura usadas.
- [ ] Cobertura do join contra os municípios do backtest 2025 documentada
      (não só contra o universo nacional de 5.570).
- [ ] `06_experimento_infra_escolar.py` reproduz o experimento de forma
      determinística (mesma seed, dois runs idênticos).
- [ ] IC bootstrap pareado do AUC ponderado reportado ao lado da contagem de
      UFs que mudam de veredito — nunca uma métrica sem a outra.
- [ ] Limitação do ano único (2023) documentada explicitamente.
- [ ] Decisão de promoção ou não promoção registrada com número real, não a
      priori.

---

## 7. RESULTADO DO EXPERIMENTO (2026-08-31) — MISTO, não promovido

**Executado:** `src/modeling/08_experimento_infra_escolar.py` — treina o
ranking intra-UF duas vezes (com e sem os 3 índices de infraestrutura),
compara pareado por UF via bootstrap (1000 reamostragens), reporta as duas
métricas definidas na Seção 2.

**Cobertura do join confirmada:** 5.231/5.232 municípios (100,0%, IC95%
Wilson [99,9%, 100,0%]) — sem piso necessário, decisão da Seção 2 item 2 se
confirma na prática. Um único município do dataset canônico não tem escola
pública com 2º ano no Censo 2023.

**Predição registrada ANTES da medição** (`reports/dicionario_censo_escolar.md`):
Luiz previu **positivo** — ao menos 1 UF sairia de `inconclusivo` para
`modelo_vence` sem nenhuma regredir. **Errou.**

**Números:**

| Métrica | Valor |
|---|---|
| AUC ponderado sem infra | 0,6478 |
| AUC ponderado com infra | 0,6456 |
| Diferença | **−0,0022** |
| UFs onde infra ajuda (IC pareado positivo) | **0** |
| UFs onde infra atrapalha (IC pareado negativo) | **2** — PR, RJ |
| UFs sem diferença detectável | 21 |

As duas UFs em que o IC pareado é conclusivo apontam na direção contrária:

| UF | AUC sem | AUC com | IC95% da diferença |
|---|---|---|---|
| PR | 0,6902 | 0,6591 | [−0,0583, −0,0046] |
| RJ | 0,7474 | 0,6548 | [−0,1745, −0,0174] |

**Mudanças de veredito** (ordem de força `modelo_perde < inconclusivo <
modelo_vence`, contando as duas direções):

| UF | Antes | Depois | Direção |
|---|---|---|---|
| GO | inconclusivo | **modelo_vence** | 🟢 fecha |
| PE | inconclusivo | **modelo_vence** | 🟢 fecha |
| TO | modelo_perde | inconclusivo | 🟢 melhora parcial |
| BA | inconclusivo | **modelo_perde** | 🔴 regride |

**Classificação: MISTO** — melhora real (GO, PE, TO) e regressão real (BA),
com AUC agregado levemente negativo. Mesmo padrão do IDHM (ADR-0009 §8).

**Decisão: não promover a `04_ranking_intra_uf.py`.** Três razões, em ordem
de peso:

1. O IC pareado não identifica **nenhuma** UF em que a infra ajude, e
   identifica duas em que atrapalha. Uma mudança de veredito sem IC pareado
   que a sustente é movimento de fronteira, não ganho medido.
2. O AUC ponderado cai (−0,0022). Trocar "2 UFs inconclusivas viram vitória"
   por "1 vira derrota" com o agregado piorando é redistribuição de
   incerteza, não redução líquida — mesma leitura que barrou o IDHM.
3. A EDA já previa: AUC intra-UF isolada dos 3 índices entre 0,4885 e
   0,4981. A hipótese de que o Random Forest resgataria interação
   multivariada invisível na análise univariada **foi testada e falhou**.

`FEATURES` em produção continua `FEATURES_BASE` (4 colunas).
`FEATURES_INFRA` existe no código como capacidade testada, não ativada —
mesmo tratamento dado a `FEATURES_IDHM`.

**O que fica pronto para reativar, se investigação futura justificar:**
- `montar_dataset(com_infra=True)` e `treinar_por_uf(features=...)` — mudança
  estrutural feita e testada (15 testes novos em
  `tests/test_agregar_censo_escolar.py`), só não ligada por padrão.
- `src/preprocessing/06_agregar_censo_escolar.py` regenera o agregado
  municipal de forma determinística a partir do zip oficial.
- `src/modeling/08_experimento_infra_escolar.py` reproduz o experimento.

## 8. O ACHADO QUE O EXPERIMENTO ABRIU (2026-08-31)

Comparando com o experimento do IDHM (ADR-0009 §8), dois conjuntos de
variáveis **sem relação entre si** (r ≈ 0,02–0,08 entre IDHM e os índices de
infra) produzem a mesma mudança nas mesmas UFs:

| UF | IDHM (socioeconômico, 2010) | INFRA (escolar, 2023) |
|---|---|---|
| **BA** | inconclusivo → modelo_perde | inconclusivo → modelo_perde |
| **PE** | inconclusivo → modelo_vence | inconclusivo → modelo_vence |

Ambos classificados MISTO. Se a mudança viesse da **informação** de cada
fonte, dois conjuntos de variáveis não correlacionadas não deveriam mover as
mesmas UFs na mesma direção.

**Hipótese alternativa:** a mudança vem do ato de **adicionar dimensão**. UFs
cujo IC bootstrap pareado já estava encostado no zero atravessam a fronteira
com qualquer perturbação do espaço de features — e a classificação
`inconclusivo`/`vence`/`perde` é justamente uma discretização de onde o IC
cai em relação ao zero.

Se a hipótese se confirmar, o "PE fechou" de **ambos** os experimentos é
artefato, e a métrica "contagem de UFs que mudam de veredito" — usada como
critério de sucesso desde o ADR-0009 — mede instabilidade de fronteira, não
ganho de informação.

Teste registrado em `src/modeling/09_placebo_permutacao.py`. **Resultado na
Seção 9: a hipótese se confirma.**

## 9. PLACEBO — a hipótese da Seção 8 se confirma (2026-08-31)

**Executado:** `src/modeling/09_placebo_permutacao.py`, 20 replicações.

**Desenho do nulo.** Permutação dos 3 índices **dentro de cada UF**, com a
mesma permutação aplicada às 3 colunas. Isso preserva exatamente a
distribuição marginal de cada índice, a correlação entre eles e a estrutura
entre estados — e destrói só o vínculo município → `y`. Ruído gaussiano
testaria um nulo mais fraco (features com distribuição diferente das reais);
a permutação testa a pergunta certa: **a informação importa, ou só a
dimensão?** O `random_state` do RandomForest fica fixo, para que a
estocasticidade do modelo não se confunda com o efeito medido.

**Resultado principal — o observado é indistinguível de ruído:**

| Métrica | Nulo (20 permutações) | Infra real | p |
|---|---|---|---|
| Mudanças de veredito | mediana 3, faixa 1–6 | **4** | **0,400** |
| AUC ponderado | média 0,6445, faixa [0,6359; 0,6511] | **0,6456** | **0,350** |

**As quatro mudanças de veredito são todas reproduzidas por ruído, na mesma
direção:**

| UF | Mudança com dado real | Ruído reproduz a mesma mudança |
|---|---|---|
| BA | inconclusivo → modelo_perde | **10/20 (50%)** — e em 10 de 10 flips, sempre nessa direção |
| PE | inconclusivo → modelo_vence | **7/20 (35%)** — sempre nessa direção |
| GO | inconclusivo → modelo_vence | 3/20 (15%) — sempre nessa direção |
| TO | modelo_perde → inconclusivo | 3/20 (15%) — sempre nessa direção |

Nenhuma UF sobrevive à correção de Benjamini-Hochberg (todos os `p_BH` ≥
0,309).

**O mecanismo.** Uma UF cujo IC bootstrap pareado já está encostado no zero
atravessa a fronteira com qualquer perturbação do espaço de features — e
sempre para o mesmo lado, porque o IC está mais perto de uma das bordas. BA
não "regride por causa do IDHM" nem "por causa da infraestrutura": BA regride
porque seu IC está a um passo do zero pelo lado negativo, e **qualquer** coluna
a mais o empurra. O mesmo vale, invertido, para PE.

**Consequência metodológica — e ela alcança o ADR-0009.** A métrica "contagem
de UFs que mudam de veredito", adotada como critério de sucesso desde o
ADR-0009 §2, **mede instabilidade de fronteira, não ganho de informação**.
Isso invalida a leitura otimista que se poderia fazer do experimento do IDHM:
o "PE fechou" registrado no ADR-0009 §8 é o mesmo flip que o ruído produz em
35% das permutações. A decisão de não promover o IDHM continua correta; o que
muda é o motivo — não era "ganho real que não compensa a regressão em BA", era
**movimento de fronteira em ambas as pontas**.

**O que a métrica deveria ser.** Contagem de vereditos só é interpretável
contra uma distribuição nula. Sem o placebo, qualquer enriquecimento futuro
produziria 1–6 mudanças e pareceria ter efeito. A forma correta de reportar é
a deste ADR: `n` observado, distribuição nula, e p — nunca a contagem sozinha.

**Limitação honesta do próprio placebo.** 20 replicações dão resolução mínima
de p = 1/21 ≈ 0,048; com correção BH sobre 13 UFs, **nenhuma UF poderia
atingir significância** mesmo que nunca virasse sob ruído. A coluna `p_BH` é
portanto pouco informativa por construção. O que sustenta a conclusão não é o
p por UF — é (a) o p global de 0,400 e 0,350, com o observado no meio da
distribuição nula, e (b) a **consistência direcional**: 10 de 10 flips de BA
na mesma direção, 7 de 7 de PE. Isso é padrão determinístico de fronteira,
não coincidência amostral.

**Decisão final do ADR-0011: infraestrutura escolar não é promovida**, e a
justificativa é mais forte do que a da Seção 7 — não é "o ganho não compensa",
é "não há ganho distinguível de ruído".
