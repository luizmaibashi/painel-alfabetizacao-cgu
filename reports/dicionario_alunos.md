# Dicionário de Dados — Alunos e snapshot_modelagem (Tech Challenge Fase 3)

**Datasets cobertos por este dicionário:**

| Dataset | Arquivo | O que é |
|---|---|---|
| `alunos` | `../tech-challenge-fase2-alfabetizacao/dados/Alunos.csv` | Base completa, 57.781 alunos. **É a base de trabalho desde 2026-08-18** |
| `alunos_amostra` | `data/Alunos_amostra.csv` | Amostra aleatória de 5.000 (8,7%), cópia byte a byte de `dados_sample/Alunos.csv` da Fase 2. Foi a base de trabalho até 2026-08-18; mantida como referência histórica dos relatórios daquele período |
| `snapshot_modelagem` | `data/snapshot_modelagem.parquet` | Saída de `02_extrair_snapshot.py`: alunos + histórico t-1 (dois níveis) + território/meta quando em `--full`. **É o que o modelo consome** |
| `territorio_local` | `data/territorio_local.parquet` | Saída de `05_montar_territorio.py`: substituto local e reduzido da Silver da Fase 2, montado sem GCP (IBGE SIDRA + metas do disco + UF por prefixo). 10.704 linhas (município × ano × rede) |

EDA de cada um em `reports/eda_<dataset>.md`.

## Colunas (pós-limpeza) — `territorio_local`

| Coluna | Tipo | Significado | Interpretação de negócio | Decisão de uso |
|---|---|---|---|---|
| `ano` | int | 2023 ou 2024 | Chave temporal do join | Chave, não feature |
| `id_municipio` | str (zfill 7) | Código IBGE do município | Chave de join com os microdados | Chave — cast obrigatório para STRING (ADR-005 da Fase 2) |
| `rede` | str | Rede de ensino | Só "Municipal" nesta fonte de metas | Chave do join; sem variância aqui |
| `meta_alfabetizacao_2024` | float | Meta oficial do PDE para 2024 | Alvo de política pública definido externamente | Feature (via versão imputada) e **baseline do teste de falsificação** — sozinha vence o modelo aluno-nível (Cap. 14) |
| `meta_alfabetizacao_2024_imputada` | float | Meta com nulos preenchidos por mediana de UF | Cobre as redes sem meta do PDE | Feature. ⚠️ **Não é o KNN da Fase 2** (ADR-004) — é substituto simplificado, declarado na coluna `_origem` |
| `populacao_total` | float | População do município (IBGE SIDRA 2021) | Porte do município, contexto estrutural | Feature — não deriva de desempenho educacional |
| `sigla_uf` | str | UF derivada do prefixo do código IBGE | Contexto territorial | Feature. 🔴 **Domina o alvo município-nível** (+0,21 de AUC) porque cada estado aplica sua própria prova — ver Cap. 16.4 do HANDOFF |
| `_origem` | str | Declaração de procedência e do que falta | Auditoria de proveniência | ⚠️ Prefixo `_` = **nunca feature** |

**Deixado de fora de propósito** (o arquivo de metas traz, mas não entram):
`taxa_alfabetizacao` (desempenho do mesmo ano, circular) e
`percentual_participacao` (ausência em nível municipal — o vazamento que custou
cinco capítulos). Ver docstring de `05_montar_territorio.py`.

## Conexão com objetivo de negócio — `territorio_local`

Existe para responder à terceira dependência falsa do projeto (Cap. 14.1 do
HANDOFF): o `--full` nunca precisou de credencial GCP, porque IBGE e metas do
PDE são dado público. Ancorado no mesmo objetivo do dataset `alunos` (prever
risco de não-alfabetização usando contexto, não desempenho próprio) e na
hipótese de que contexto territorial/socioeconômico carregaria o sinal que as
features de aluno não tinham.

**Resultado da hipótese:** território de fato moveu o modelo de 0,507 para
0,6013 — mas a meta do PDE aplicada sozinha chega a 0,6331 e vence o modelo
(Cap. 14.5). E no grão município, `sigla_uf` domina por artefato de régua
estadual, não por sinal municipal (Cap. 16).

Este documento cobre os microdados do Indicador Criança Alfabetizada / Alfabetiza
Brasil (INEP) e as features derivadas do snapshot de modelagem. Ancorado em
`docs/wayfinder/tech_challenge_fase3/SPEC_FINAL.md` e
`docs/wayfinder/tech_challenge_fase3/adr/0001-pipeline-sklearn-snapshot-e-politica-leakage.md`.

## Conexão com objetivo de negócio

**Objetivo**: prever se um aluno será alfabetizado, usando apenas
contexto (não o próprio desempenho), para alimentar ação de busca
ativa/priorização na ponta escolar (Diretor/Coordenador Pedagógico) — Fase 2
já resolve a leitura macro (Secretário/Prefeito), Fase 3 ataca o indivíduo
que a média município-nível esconde.

**Hipótese a confirmar/refutar**: absenteísmo histórico (t-1) + contexto
territorial/socioeconômico estrutural explicam risco de não-alfabetização
sem depender do resultado do próprio aluno no exame que gera o rótulo.

**Critério de falsificação** (ver ADR-0001, Seção 5): o modelo precisa
superar o baseline trivial de aplicar o risco município-nível já calculado
na Fase 2 (`agg_priorizacao`) igualmente a todos os alunos do município —
senão o esforço de leakage/validação temporal desta fase não se justifica.

Confirmado com o usuário em 2026-08-10 que este objetivo, fechado na Sabatina
Socrática do Grill with Docs, ainda vale.

## Colunas (pós-limpeza)

| Coluna | Tipo | Significado | Interpretação de negócio | Decisão de uso |
|---|---|---|---|---|
| `ano` | int | Ano da aplicação da prova (2023/2024) | Define o cohort do aluno | Usado para join de histórico t-1 e para split temporal |
| `id_municipio` | int (no CSV bruto) | Código IBGE do município | Chave de join com território/socioeconômico | **Cast obrigatório para STRING antes de qualquer join** (ADR-005 da Fase 2 — zeros à esquerda) |
| `id_municipio_nome` | string | Nome do município | Leitura humana | Não entra como feature (redundante com `id_municipio`, alta cardinalidade textual) |
| `id_escola` | int | Código INEP da escola | Granularidade abaixo de município | Chave para agregação de histórico t-1 por escola (mais fino que por município) |
| `id_aluno` | int | Identificador do aluno | Chave única (aluno pode repetir entre anos, não duplicata de erro) | Não é feature, é identificador |
| `caderno` | int (categórico) | Versão do caderno de prova | Metadado administrativo do exame | 🔴 **PROXY DE AUSÊNCIA (descoberto 2026-08-18)** — `caderno=12` tem **79,7% de ausentes** contra 12-16% dos demais. Os 87,3% de "Não" investigados por 3 capítulos eram artefato de ausência: entre quem fez a prova, esses alunos vão **melhor** que a média (37,3% vs ~41%). A hipótese de caderno de acessibilidade está **descartada**. Quinta porta do mesmo vazamento. Ver Cap. 11.3 do HANDOFF_RENAN.md |
| `serie` | string | Série escolar | Constante na amostra (100% "2° ano do Ensino Fundamental") | **Fora do modelo** — sem variância, não separa nada (achado do item 2 do checklist EDA) |
| `rede` | string | Rede de ensino (Municipal/Estadual/...) | Contexto administrativo | Feature — mas achatado por não ter Federal/Privada na amostra (checar cobertura na base completa) |
| `presenca` | string | Se o aluno compareceu à prova | Determina se há nota | **Fora do modelo, sempre** — leakage direto (ADR-0001) |
| `preenchimento_caderno` | string | Se a prova foi respondida | Redundante com `presenca` (834/835 casos coincidem) | **Fora do modelo, sempre** — leakage por redundância (ADR-0001) |
| `alfabetizado` | string (Sim/Não) | Target — aluno atingiu 743 pts na escala Saeb | É o que o modelo prevê | Target |
| `proficiencia` | float | Score contínuo da prova (escala Saeb) | Define `alfabetizado` por corte determinístico (743 pts, confirmado sem sobreposição na EDA) | **Fora do modelo, sempre** — define o target |
| `peso_aluno` | float | Peso amostral (pós-estratificação) | Ajuste estatístico de representatividade, não desempenho | ❌ **FORA DO MODELO, SEMPRE (desde 2026-08-18) — leakage.** Os 835 nulos desta coluna são os alunos ausentes, e neles o alvo é "Não" em 100% dos casos. É o mesmo vazamento de `presenca`/`preenchimento_caderno` (ADR-0001 §2.2), entrando pela **nulidade**. Após imputação pela mediana, o valor imputado identifica os ausentes com 94,7% de pureza. Ver Cap. 9.3 do HANDOFF_RENAN.md |

## Features criadas

**Atualizado em 2026-08-18** — reescrito após três achados: a base completa
(57.781 alunos) passou a ser usada, o histórico por escola se mostrou inviável
por desenho amostral, e `peso_aluno` foi para a lista de leakage.

### Já existentes no snapshot `--local-only`

| Feature | Origem | Cálculo | Justificativa | Cobertura real (não imputada) |
|---|---|---|---|---|
| `absenteismo_hist_municipio_t1` | `Alunos.csv`, agregado | Taxa de ausência do **município** no ano anterior; imputada por mediana da UF (ou global se `sigla_uf` ausente) | Substitui `presenca` do próprio aluno (leakage) por sinal histórico legítimo — ADR-0001 §2.1/2.3. **Nível município escolhido por evidência**: SHAP dá 45,1% da influência ao bloco município contra 9,9% ao de escola | **36,9%** |
| `n_alunos_hist_municipio_t1` | idem | Quantos alunos sustentam a taxa acima | Uma taxa vinda de 1 aluno só pode valer 0% ou 100% — não é taxa. O contador deixa o modelo distinguir taxa confiável de taxa frágil. Sozinho pesa 16,8% no SHAP | 36,9% |
| `possui_hist_municipio_t1` | Derivada | Binária: 1 se o município tem dado do ano anterior | Sinaliza imputação sem ser leakage (indica disponibilidade de dado, não resultado) — ADR-0001 §2.3. Vigiado pelo gate de artefato (limiar 10%; hoje 8,7%) | — |
| `absenteismo_hist_escola_t1` | `Alunos.csv`, agregado | Mesma lógica, no nível **escola** | ⚠️ **Estruturalmente frágil**: 49,9% dos grupos escola-ano têm 1 aluno só, e apenas 22,4% das escolas de 2024 aparecem em 2023. Mantida para documentar o achado e permitir comparação — SHAP dá só 2,4% a ela | **11,3%** |
| `n_alunos_hist_escola_t1` | idem | Contador do nível escola | Mesma justificativa do contador municipal | 11,3% |
| `possui_hist_escola_t1` | Derivada | Binária, nível escola | idem | — |
| `_ausente_no_exame` | Derivada de `presenca` | Binária: 1 se `presenca == "Ausente"` | ⚠️ **AUDITORIA, NUNCA FEATURE** (prefixo `_`). Existe porque 16,8% da base tem rótulo por convenção ("não fez prova ⇒ não alfabetizado"), e decidir se essas linhas ficam na população exige saber quem são mesmo depois de `presenca` sair por leakage. Ver Cap. 11.2 do HANDOFF_RENAN.md | — |
### Planejadas — só existem no snapshot `--full` (dependem de credencial GCP)

| Feature | Origem | Cálculo | Justificativa |
|---|---|---|---|
| `populacao_total` | Silver Fase 2 (IBGE) | Direto, join por `id_municipio`+`ano` | Estrutural, não deriva de desempenho educacional |
| `gasto_por_habitante_educacao` | Silver Fase 2 (SICONFI) | Direto, join por `id_municipio`+`ano` | Estrutural/fiscal, não deriva de desempenho educacional |
| `sigla_uf` / região | Silver Fase 2 | Direto ou derivado do prefixo de `id_municipio` | Contexto territorial, mesmo princípio do `03_modelo_preditivo_risco.py` da Fase 2. Também habilita a imputação por mediana de UF do ADR-0001 §2.3, que hoje cai no fallback global |
| `meta_alfabetizacao_2024_imputada` | Silver Fase 2, OBT **com metas imputadas** (KNN, ADR-004) | Direto, join por `id_municipio`+`ano`+`rede` | Meta do PDE: definida externamente por política pública, não deriva do desempenho do aluno predito. Enunciado pede "metas estaduais e municipais" explicitamente. Ver Cap. 6.3 do HANDOFF_RENAN.md |
| `meta_is_imputada` | Derivada | Binária: 1 se a meta original era nula (veio do KNN) | A tabela do KNN não grava essa marcação. Meta imputada sem rótulo repete o erro apontado no dashboard da Fase 2 |

**Fora do modelo, sempre** (leakage, ADR-0001 + adição de 2026-08-18):
`proficiencia`, `presenca`, `preenchimento_caderno`, **`peso_aluno`**, qualquer métrica de desempenho município-nível do
mesmo ano (`taxa_alfabetizacao`, `gap_meta`, `deficit_per_capita`).
