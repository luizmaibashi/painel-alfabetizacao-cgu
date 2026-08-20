# ADR-0001: Pipeline sklearn sobre snapshot único do Gold + política de data leakage e validação temporal

**Data**: 2026-08-10
**Status**: Proposed (decisão unilateral do Luiz — pendente revisão do Renan
se a dupla se confirmar, ver ticket 0004; vira Accepted só depois do PR
cruzado, mesmo contrato do AGENTS.md da Fase 2, regra 1)
**Proposto por**: Luiz Maibashi
**Contexto**: Tech Challenge Fase 3 (Pós-Tech FIAP) — modelo supervisionado de
alfabetização por aluno. Migrado em 2026-08-20 de `docs/wayfinder/
tech_challenge_fase3/adr/` (local provisório, ver ticket 0004) para este
`docs/adr/` do projeto; repositório GitHub próprio da Fase 3 (org
`alfabetizacao-datateam`) segue não criado (ticket 0004, ação pendente que
afeta espaço compartilhado da org).

---

## 🤔 1. CONTEXTO (O QUÊ?)

O enunciado da Fase 3 pede um modelo supervisionado que preveja se um
**aluno** (não município) será alfabetizado, usando "dados da camada Gold"
da Fase 2, com pipeline scikit-learn completa (imputação, encoding,
tratamento de data leakage, integração pré-processamento→modelo, validação
com generalização).

A Fase 2 é um pipeline PySpark em produção (Bronze/Silver/Gold, Dataproc/
BigQuery), majoritariamente nível-**município**. A única fonte nível-aluno é
`Alunos.csv` (microdados SAEB individuais).

**Restrições técnicas:**
- Volume real: 57.781 alunos (`dados/Alunos.csv`, 7,3MB) — pequeno o
  suficiente para pandas/sklearn puro, sem necessidade de processamento
  distribuído.
- Cobertura temporal: só 2 anos de dado (2023, 2024) — limita qualquer
  estratégia de feature histórica ou validação temporal a uma única janela.
- AGENTS.md da Fase 2 restringe IA a atuar só em `dados_sample`/camada Gold
  ("AI Jail") — qualquer extração deve respeitar esse limite.

**Dependências afetadas:**
- Infraestrutura BigQuery/Gold da Fase 2 (ponto único de extração).
- `agg_priorizacao`/`agg_municipio_ranking` (Fase 2) — vira baseline de
  comparação obrigatório para o modelo novo (ver Seção 5).

**Baseline (o que já existe, não muda):**
- `src/ml/03_modelo_preditivo_risco.py` (RandomForest, nível-município,
  protótipo validado mas nunca rodado em produção completa — ADR-015 da
  Fase 2) — referência de estilo de código (split estratificado, métricas
  completas, regularização), não ponto de partida direto: problema diferente
  (aluno vs. município).

---

## ⚙️ 2. DECISÃO (POR QUÊ?)

**O que escolhemos** (quatro decisões amarradas, tratadas como uma unidade
porque uma depende da outra):

### 2.1 Arquitetura: Opção A — snapshot único, sklearn puro

**Correção de premissa (2026-08-10, achado ao preparar o script de extração)**:
a versão original desta seção assumia "SQL no BigQuery" como ponto único de
extração. Isso estava errado — checado no código real da Fase 2:
- `Alunos.csv` **nunca entrou no pipeline cloud** (não aparece em nenhum
  `dataproc_0X_*.py`) — só existe localmente (`dados/Alunos.csv`, processado
  por `src/batch/06_alunos_bronze_to_silver.py`, script local).
- Território/socioeconômico (`populacao_total`, `gasto_por_habitante_educacao`,
  `sigla_uf`) vive na **Silver** (`alfabetizacao_municipios_obt`) — Parquet no
  GCS, **nunca carregada no BigQuery** (só a Gold, agregados por município,
  vai para lá — README: "BigQuery serve a camada Gold para BI").

**Arquitetura real de extração**: dois pontos de contato, não um:
1. `Alunos` — já disponível localmente, sem dependência de nuvem.
2. Território/socioeconômico — requer acesso ao **GCS** (ler o Parquet da
   Silver), não ao BigQuery. Join em pandas por `id_municipio` (cast para
   STRING — ADR-005 da Fase 2, zeros à esquerda) + `ano` + `rede`.

O restante da decisão (Opção A: tudo em pandas/sklearn depois da extração,
sem Spark/GCP na Fase 3) continua válido — só o mecanismo de extração mudou.

### 2.2 Política de data leakage
**Fora do modelo, sempre:**
- `proficiencia` — define o target (`alfabetizado`) por corte de 743 pontos.
- `presenca` do próprio aluno no próprio exame — achado empírico desta sessão:
  100% dos alunos "Ausente" (amostra n=5.000) têm `alfabetizado=Não`
  (convenção do dado, não medição), tornando `presenca` quase-determinística.
- `preenchimento_caderno` — **achado da EDA real (2026-08-10)**: correlaciona
  quase 1:1 com `presenca` (834 dos 835 "Prova não preenchida" são exatamente
  os alunos "Ausente") — mesmo evento em coluna diferente, excluída pelo
  mesmo motivo (mantê-la reintroduziria o leakage de `presenca` por outro
  nome).
- Métricas de desempenho agregadas no nível município **do mesmo ano** do
  aluno (`taxa_alfabetizacao`, `gap_meta`, `deficit_per_capita`) — incluem o
  próprio aluno sendo predito, são circulares (mesmo princípio do ADR-015 da
  Fase 2, aplicado na direção aluno→município).
- **`peso_aluno` — adicionado em 2026-08-18.** Não vaza pelo valor, vaza pela
  **nulidade**: os 835 nulos da amostra são os alunos ausentes, e neles o alvo
  é "Não" em 100% dos casos (contra 41% no restante). É o mesmo evento que já
  motivou excluir `presenca` e `preenchimento_caderno`, entrando por uma
  terceira porta. Após `SimpleImputer(median)` o valor imputado identifica os
  ausentes com 94,7% de pureza, e uma regra única "nulo ⇒ risco" atinge
  Precision 1,000.

  **Lição de método registrada aqui porque a política acima não bastou:** esta
  lista era de colunas cujo *valor* vaza. Faltava vigiar o *padrão de ausência*
  de valor. A verificação virou código — `src/preprocessing/03_guarda_leakage.py`
  testa toda feature candidata contra vazamento por nulidade, por valor e por
  poder isolado, e falha com código 1 em suspeita alta.

**Dentro do modelo:** metadado de exame (`caderno` — cardinalidade baixa
confirmada na EDA, 4 valores, seguro para one-hot; `serie` e `peso_aluno`
saíram depois — ver acima e §2.2),
território/socioeconômico estrutural do mesmo ano (população, gasto per
capita, região — nunca métricas derivadas de desempenho), e histórico
agregado t-1 (absenteísmo, possivelmente
taxa de alfabetização do ano anterior).

### 2.3 Tratamento do histórico t-1 ausente (cohort 2023)
Como só existem 2 anos de dado, o cohort 2023 não tem ano anterior — a
feature de histórico t-1 fica ausente para ~metade da base. Decisão: **não
descartar o cohort** (cortaria a base pela metade e destruiria a única
janela de validação temporal). Tratar como dado faltante genuíno — o próprio
enunciado já exige imputação de numéricas: imputar (mediana da UF) + adicionar
flag binária `possui_historico_t1` (não é leakage, só informa disponibilidade
de dado).

### 2.4 Estratégia de validação dupla
Split aleatório estratificado por município como validação principal + split
temporal 2023(treino)→2024(teste) como checagem secundária, documentado como
limitado pela janela de só 2 anos (treino com histórico majoritariamente
imputado, teste com histórico real — viés conhecido, relatado no README, não
escondido).

**Razão principal:**
"Se NÃO fizermos isso: o pipeline reconstrói Spark/GCP para um volume que não
precisa (57k linhas), o enunciado explícito de leakage fica sem tratamento
documentado (risco de nota/avaliação), e a metade da base sem histórico t-1
vira descarte silencioso ou erro de imputação não documentado — os dois
minam a credibilidade técnica da entrega."

"Se fizermos: pipeline mais simples de auditar e rodar (sklearn puro), leakage
tratado com o mesmo rigor que a Fase 2 já aplicou (ADR-015), e o dataset
inteiro (2 anos) aproveitado sem sacrificar volume nem validação temporal."

---

## 📊 3. CONSEQUÊNCIAS

**Positivas (Wins):**
- Sem dependência de Spark/GCP na Fase 3 — reduz superfície de erro e tempo
  de iteração (treina em segundos, não em cluster).
- Política de leakage auditável e testável (lista fechada de colunas
  incluídas/excluídas, com justificativa por item).
- Volume de dado preservado (57.781 linhas, não ~29k) mesmo com a limitação
  de histórico ausente.
- Consistência de rigor com a Fase 2 (mesmo princípio anti-leakage do
  ADR-015, mesma disciplina de reportar limitação em vez de escondê-la —
  ex.: `is_imputado` no KNN de metas).

**Negativas (Custo/Risco):**
- `possui_historico_t1` pode virar, ele mesmo, uma feature de alto peso no
  SHAP por artefato de dado (indica "é cohort 2023"), não sinal real —
  precisa checagem explícita no relatório de interpretabilidade.
- Split temporal secundário tem viés conhecido (treino majoritariamente
  imputado vs. teste real) — resultado dessa checagem deve ser lido com
  cautela, não como validação forte isolada.
- Território/socioeconômico é proxy municipal, não individual — risco real
  de o modelo aprender "de qual município vem" em vez de sinal do aluno (ver
  Seção 5, critério de falsificação).

**Timeline:**
- Extração do snapshot: 1 sessão.
- EDA + pipeline sklearn + validação: several sessões subsequentes (fora do
  escopo desta ADR).

---

## 🎯 4. ALTERNATIVAS DESCARTADAS

| Opção | Vantagem | Por quê rejeitada |
|-------|----------|--------------------|
| B: Pipeline híbrida (join pesado em Spark, modelagem em sklearn) | Mais fiel à arquitetura de produção da Fase 2 | ❌ Duplica complexidade de infra que a entrega não pede; volume real (57k linhas) não justifica Spark |
| Modelo D0 (só dado de matrícula, sem histórico t-1) | Mais simples, evita o problema de dado ausente no cohort 2023 | ❌ Depende de features que não existem no projeto (infraestrutura de escola, histórico de reprovação individual) — promessa que o dado não sustenta |
| Descartar cohort 2023 (usar só 2024, que tem t-1 completo) | Evita imputação, elimina o viés do split temporal | ❌ Reduz a base pela metade e destrói a única janela de validação temporal disponível (treinar no passado, testar no futuro vira impossível com 1 ano só) |
| Accuracy como métrica principal | Simples de calcular e explicar | ❌ Caso de uso (busca ativa) pune falso negativo mais que falso positivo — Recall da classe "Não" é a métrica que reflete o custo real do erro |

---

## 💰 5. IMPACTO ROI & VALIDAÇÃO

**Métrica de sucesso:**
- Recall da classe "Não" (principal) + Precision (contrapeso) + ROC-AUC
  (suporte).
- **Critério de falsificação real**: o modelo aluno-nível precisa **superar**
  o baseline trivial de aplicar `agg_priorizacao` (risco município-nível já
  existente na Fase 2) igualmente a todos os alunos do mesmo município. Sem
  superar esse baseline, o esforço técnico desta ADR (leakage, validação
  dupla, SHAP) não se justifica — a tese de negócio (ADR depende da Sabatina
  registrada em `SPEC_FINAL.md`, Seção 5.5) cai.

**Cenários de regressão (quando falha silenciosamente):**
1. SHAP mostra território/socioeconômico dominando sobre features
   individuais (caderno, histórico de absenteísmo) → modelo é o baseline
   municipal disfarçado, sem valor aluno-nível real.
2. Métrica boa no split aleatório, ruim no split temporal (2023→2024) →
   modelo memorizou o cohort, não aprendeu padrão generalizável.
3. `possui_historico_t1` aparece como feature de alto peso no SHAP → modelo
   está detectando o artefato de imputação, não um sinal real do aluno.

**Monitoramento (a implementar no relatório de EDA/avaliação):**
```
- checar: recall_classe_nao >= baseline_municipio (agg_priorizacao aplicado por aluno)
- checar: shap_top_features não dominadas só por território/socioeconômico
- checar: metric(split_temporal) não muito abaixo de metric(split_aleatorio)
- checar: possui_historico_t1 fora do top-5 SHAP
```

---

## 🔗 6. REFERÊNCIAS & LINKS

**Relacionados:**
- `docs/wayfinder/tech_challenge_fase3/SPEC_FINAL.md` (spec completa desta
  decisão, seções 2-5.6)
- `docs/wayfinder/tech_challenge_fase3/0002-politica-data-leakage.md`,
  `0003-volume-balanceamento-alunos.md`, `0005-reaproveitamento-vs-pipeline-nova.md`
  (tickets de origem)
- `PROJETOS/01_PRIORITY/tech-challenge-fase2-alfabetizacao/docs/adr/ADR-015-auditoria-deficit-per-capita-e-status-ml.md`
  (precedente de política de leakage e de "manter protótipo sem forçar
  produção" reaplicado aqui)
- `PROJETOS/01_PRIORITY/tech-challenge-fase2-alfabetizacao/src/ml/03_modelo_preditivo_risco.py`
  (referência de estilo, não de arquitetura)

**Pendência formal resolvida em 2026-08-20:** arquivo migrado para este
`docs/adr/`. Segue pendente só a revisão técnica do Renan (mesma condição
de Status acima) e a eventual migração de repositório se o ticket 0004
(GitHub próprio) avançar.

---

## ✅ CRITÉRIA DE ACEITAÇÃO

- [x] Trade-offs documentados com justificativa (efeito na credibilidade
      técnica da entrega, não $ — projeto acadêmico).
- [x] Alternativas rejeitadas com motivo técnico (Seção 4).
- [x] Impacto quantificado onde possível (volume, cobertura temporal,
      métrica de sucesso).
- [x] Métricas de sucesso definidas e testáveis (Seção 5).
- [x] Plano de monitoramento descrito (checklist Seção 5).
- [x] Riscos/edge cases identificados (3 cenários de falha silenciosa).
