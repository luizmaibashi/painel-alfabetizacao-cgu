# ADR-0003: Não usar a camada Gold como fonte de dados — Silver + microdados no lugar

**Data**: 2026-08-19
**Status**: Accepted (decisão técnica com evidência de código auditável; não
depende de call com o Renan como o ADR-0002, mas ele deve ser informado)
**Proposto por**: Luiz Maibashi
**Contexto**: Auditoria pedida pelo Luiz ("verificação profunda do projeto...
atende o enunciado?") revelou que o enunciado exige, em duas passagens
literais (PDF p.2 e p.3), que "os dados utilizados deverão ser provenientes
da camada Gold desenvolvida na Fase 2" — e o projeto usa Silver + microdados
locais. Esta ADR formaliza e evidencia por que essa divergência é
metodologicamente necessária, não uma escolha de conveniência.

---

## 🤔 1. CONTEXTO (O QUÊ?)

O enunciado da Fase 3 pede um modelo supervisionado no **grão aluno**
("prever se um aluno será considerado alfabetizado"), e especifica que os
dados devem vir da camada Gold da Fase 2. O projeto, desde o ADR-0001, usa
`Alunos.csv` (microdados locais) + Silver territorial/socioeconômica — nunca
a Gold. Isso apareceu na auditoria de 2026-08-19 como risco de nota: um
requisito explícito, repetido duas vezes no PDF, não cumprido literalmente.

A questão levantada pelo Luiz: **"você tem certeza que as Golds geradas no
GCP não possuem os dados de aluno?"** — a resposta não podia ficar em
inferência sobre a documentação da Fase 2; precisava vir do código-fonte
real, incluindo o script que roda no GCP de verdade (não só o script local
usado pra desenvolvimento).

---

## ⚙️ 2. DECISÃO (POR QUÊ?)

**Não usar a camada Gold como fonte de dados para o modelo aluno-nível.**
Usar Silver (`alfabetizacao_municipios_obt*`, território/socioeconômico) +
microdados locais (`Alunos.csv`, nunca processado pela Fase 2 além do
Bronze→Silver) — arquitetura já registrada no ADR-0001 §2.1, agora com
evidência de código anexada.

### 2.1 Verificação feita — dois scripts, não um

Inspecionei os dois geradores de Gold que existem no repositório da Fase 2
(`tech-challenge-fase2-alfabetizacao`, HEAD local sincronizado com
`github.com/alfabetizacao-datateam/tech-challenge-fase2-alfabetizacao`,
commit de `01_gerar_marts_gold.py` em 2026-07-26):

| Script | Onde roda | Marts gerados |
|---|---|---|
| `src/gold/01_gerar_marts_gold.py` | Local, contra `datalake_sample` | 9 (uso em dev) |
| `src/cloud/dataproc_03_gold.py` | **Dataproc/GCS real** — o que o Renan rodaria com a credencial dele | 15 (produção) |

O segundo é o que importa: é o script que gera a Gold **de verdade**, a que
vai pro BigQuery. Não bastava auditar o script de desenvolvimento.

### 2.2 O achado — grão, não conteúdo

Os 15 marts do script cloud (`agg_uf_indicadores`, `agg_evolucao_temporal`,
`agg_municipio_ranking`, `agg_rede_indicadores`, `agg_priorizacao`,
`agg_top10_uf`, `agg_vulnerabilidade_ml`, `agg_qualidade_resumo`,
`agg_eficiencia_financeira`, `agg_custo_ineficiencia`,
`agg_projecao_investimento`, `agg_correlacoes_uf`, `agg_roi_executivo`,
`agg_alocacao_otima`, `agg_alocacao_otima_estrategias`) são **todos**
`groupBy` em `id_municipio` / `sigla_uf` / `rede` / `ano`. Inclusive o único
que usa Machine Learning (`agg_vulnerabilidade_ml`, K-Means) primeiro agrega
pra município (`taxa_media`, `deficit_per_capita`, `log_populacao` por
`id_municipio`) e só então clusteriza — nunca vê uma linha de aluno.

`load_silver()` (linha 89-123 do script cloud) só lê as três variantes da
Silver municipal (`alfabetizacao_municipios_obt*`). Nenhum caminho do script
cloud toca `Alunos.csv` ou qualquer fonte de microdado.

**Conclusão verificada, não inferida:** a Gold real, gerada com credencial
GCP de verdade, **não tem nenhuma linha de aluno** — em nenhuma das duas
versões do gerador. Não é uma lacuna de extração da Fase 3; é uma
característica do desenho da Gold na Fase 2. Rodar o `--full` do Renan não
resolveria isso — a Gold que sai do outro lado do pipeline continua no grão
errado.

### 2.3 Por que isso é mais forte que "leakage parcial"

A primeira formulação do ADR-0001 §2.2 dizia que métricas município-nível do
mesmo ano (`taxa_alfabetizacao`, `gap_meta`, `deficit_absoluto_proxy`) seriam
circulares se usadas como feature — argumento correto, mas formulado como
"parte da Gold vaza". A verificação mostra o argumento mais forte: **não há
"parte não-circular" suficiente para modelar aluno**, porque não há aluno na
Gold pra começar. Mesmo se toda métrica de desempenho fosse removida, restaria
`populacao_total`, `sigla_uf` e as colunas cruas do SICONFI — todas no grão
município, exigindo a mesma junção (aluno → município) que a Silver já faz, e
sem nenhuma vantagem sobre usar a Silver diretamente.

O que a Fase 3 de fato usa (via `05_montar_territorio.py`) já exclui, por
comentário explícito no próprio código, exatamente as duas colunas que
seriam circulares se estivessem disponíveis (`taxa_alfabetizacao`,
`percentual_participacao`) — coerente com o motivo agora comprovado por que
a Gold nunca foi a fonte certa.

---

## 📊 3. CONSEQUÊNCIAS

**Positivas (Wins):**
- Defesa da divergência do enunciado deixa de ser argumento de projeto e
  vira fato verificável em código, citável linha a linha se o avaliador
  questionar.
- Reforça, com evidência independente, uma escolha de arquitetura que já
  estava certa desde o ADR-0001 — não foi preciso mudar nada no pipeline.
- Fecha a lacuna 🟡 nº 2 da auditoria do enunciado (Cap. 7.2 do
  `o diário de bordo interno (não publicado)`): a divergência agora tem parágrafo formal, pronto pra
  entrar no README ("Descrição da base utilizada").

**Negativas (Custo/Risco):**
- O enunciado continua, na letra, pedindo Gold — nenhuma quantidade de
  evidência técnica muda o texto do PDF. O risco de avaliação subjetiva
  (avaliador que não lê a justificativa) permanece; a mitigação é garantir
  que o README cite este ADR explicitamente, não deixe a divergência
  implícita.
- Esta ADR não resolve a estrutura de pastas nem o git flow — riscos
  separados, já registrados na auditoria.

**Timeline:**
- Verificação de código: ✅ feita em 2026-08-19, sessão de auditoria.
- Pendente: citar este ADR na seção "Descrição da base utilizada" do README
  (bloco seguinte do projeto).

---

## 🎯 4. ALTERNATIVAS DESCARTADAS

| Opção | Vantagem | Por quê rejeitada |
|-------|----------|--------------------|
| Usar a Gold e aceitar o leakage circular como "limitação documentada" | Cumpre o enunciado ao pé da letra | ❌ Pioraria o projeto de propósito — o Cap. 14 do HANDOFF já mostrou que uma única feature correlacionada 0,979 com o alvo (a meta do PDE) já contamina o teste de falsificação; usar `taxa_alfabetizacao` do mesmo ano seria vazamento direto, não sutil |
| Juntar Gold (`agg_municipio_ranking`) aos alunos só pelas colunas "seguras" (`populacao_total`, `sigla_uf`) | Cumpriria a letra "dados vêm da Gold" | ❌ Essas colunas já estão na Silver, sem a junção extra por município nem a dependência do BigQuery — usar a Gold aqui seria caminho mais longo pro mesmo dado, sem ganho |
| Aceitar a afirmação da Fase 2 sobre a Gold sem checar o script cloud | Mais rápido | ❌ Era exatamente o tipo de erro que este projeto já cometeu 3 vezes (Cap. 10.1, 14.1 do HANDOFF): aceitar dependência/limitação sem checar a origem. Checar os dois scripts (local e cloud) evitou repetir o padrão pela 4ª vez |

---

## 💰 5. IMPACTO ROI & VALIDAÇÃO

**Métrica de sucesso:** README cita este ADR na seção "Descrição da base
utilizada", com a tabela de marts e a conclusão de grão — não deixa a
divergência do enunciado implícita.

**Cenários de regressão (quando falha silenciosamente):**
1. Nova versão da Gold é gerada na Fase 2 e passa a incluir microdado —
   revalidar antes de assumir que a decisão continua válida indefinidamente.
2. README cita "usamos Silver por causa de leakage" sem citar que a Gold
   simplesmente não tem grão de aluno — argumento mais fraco que o disponível.

**Monitoramento (a checar no README/entrega):**
```
- checar: seção "Descrição da base utilizada" cita este ADR-0003
- checar: tabela de marts Gold (grão município) aparece pra evidenciar visualmente
- checar: menção explícita de que dataproc_03_gold.py (script cloud real) foi auditado, não só o script local
```

---

## 🔗 6. REFERÊNCIAS & LINKS

**Relacionados:**
- `ADR-0001` (§2.1, §2.2) — arquitetura original e política de leakage; esta
  ADR não muda nenhuma decisão dele, só formaliza e evidencia por que a
  Gold nunca foi a fonte certa.
- `PROJETOS/01_PRIORITY/tech-challenge-fase2-alfabetizacao/src/gold/01_gerar_marts_gold.py`
  — gerador local (dev), 9 marts, todos município/UF/rede.
- `PROJETOS/01_PRIORITY/tech-challenge-fase2-alfabetizacao/src/cloud/dataproc_03_gold.py`
  — gerador cloud real (Dataproc/GCS), 15 marts, todos município/UF/rede;
  fonte principal desta verificação.
- `PROJETOS/01_PRIORITY/tech-challenge-fase3-alfabetizacao/src/preprocessing/05_montar_territorio.py`
  — exclui `taxa_alfabetizacao` e `percentual_participacao` por comentário
  explícito no código, coerente com o achado desta ADR.
- diário de bordo interno (não publicado)
  — Cap. 7.2 (auditoria do enunciado, divergência nº 2) referencia esta ADR
  como resolução.
- `[IAST] - Tech Challenge - Fase 3.pdf` (p.2, p.3 — as duas menções
  literais à camada Gold como fonte obrigatória).

**Pendência formal resolvida em 2026-08-20:** mesma dos ADR-0001/0002 —
arquivo já migrado para este `docs/adr/`.

---

## ✅ CRITÉRIA DE ACEITAÇÃO

- [x] Trade-offs documentados com justificativa (grão de dado, não só
      leakage).
- [x] Alternativas rejeitadas com motivo técnico (Seção 4).
- [x] Impacto quantificado onde possível (15 marts cloud auditados, 0 com
      grão de aluno).
- [x] Métricas de sucesso definidas e testáveis (Seção 5).
- [x] Plano de checagem descrito (checklist Seção 5).
- [x] Riscos/edge cases identificados (2 cenários de falha silenciosa).
- [x] Evidência em código citável linha a linha (Seção 2.1-2.2), não só
      documentação de outro projeto.
