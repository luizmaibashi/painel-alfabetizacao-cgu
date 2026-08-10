# Dicionário de Dados — Alunos (Tech Challenge Fase 3)

Cobre `Alunos.csv` (microdados SAEB individuais, amostra de
`dados_sample/Alunos.csv` da Fase 2) e as features derivadas planejadas para
o snapshot de modelagem. Ancorado em
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
| `caderno` | int (categórico) | Versão do caderno de prova (controle anti-cola) | Metadado administrativo do exame | **Feature — com ressalva**: `caderno=12` teve taxa de "Não" anormal na EDA (86,9% vs ~50%), possível proxy de caderno adaptado/acessibilidade. Entra como feature, mas o achado deve constar no relatório final e no SHAP checar se domina de forma suspeita |
| `serie` | string | Série escolar | Constante na amostra (100% "2° ano do Ensino Fundamental") | **Fora do modelo** — sem variância, não separa nada (achado do item 2 do checklist EDA) |
| `rede` | string | Rede de ensino (Municipal/Estadual/...) | Contexto administrativo | Feature — mas achatado por não ter Federal/Privada na amostra (checar cobertura na base completa) |
| `presenca` | string | Se o aluno compareceu à prova | Determina se há nota | **Fora do modelo, sempre** — leakage direto (ADR-0001) |
| `preenchimento_caderno` | string | Se a prova foi respondida | Redundante com `presenca` (834/835 casos coincidem) | **Fora do modelo, sempre** — leakage por redundância (ADR-0001) |
| `alfabetizado` | string (Sim/Não) | Target — aluno atingiu 743 pts na escala Saeb | É o que o modelo prevê | Target |
| `proficiencia` | float | Score contínuo da prova (escala Saeb) | Define `alfabetizado` por corte determinístico (743 pts, confirmado sem sobreposição na EDA) | **Fora do modelo, sempre** — define o target |
| `peso_aluno` | float | Peso amostral (pós-estratificação) | Ajuste estatístico de representatividade, não desempenho | Sem diferença relevante entre classes (EDA item 8) — uso opcional, baixo valor preditivo esperado |

## Features criadas (planejadas — dependem do snapshot com BigQuery, ainda não extraído)

| Feature | Origem | Cálculo | Justificativa |
|---|---|---|---|
| `possui_historico_t1` | Derivada | Binária: 1 se o município/escola do aluno tem dado do ano anterior, 0 caso contrário (sempre 0 para cohort 2023) | Sinaliza imputação sem ser leakage (só indica disponibilidade de dado, não resultado) — ADR-0001 Seção 2.3 |
| `absenteismo_historico_t1` | Silver/Gold Fase 2, agregado | Taxa de ausência da escola/município no ano anterior (imputada por mediana da UF quando ausente) | Substitui `presenca` do próprio aluno (leakage) por sinal histórico legítimo — ADR-0001 Seção 2.1/2.3 |
| `populacao_total` | Silver Fase 2 (`populacao_total`, IBGE) | Direto, join por `id_municipio`+`ano` | Estrutural, não deriva de desempenho educacional |
| `gasto_por_habitante_educacao` | Silver Fase 2 (SICONFI) | Direto, join por `id_municipio`+`ano` | Estrutural/fiscal, não deriva de desempenho educacional |
| `sigla_uf` / região | Silver Fase 2 (`sigla_uf`, mapeamento por UF) | Direto ou derivado do prefixo de `id_municipio` | Contexto territorial, mesmo princípio do `03_modelo_preditivo_risco.py` da Fase 2 |

**Fora do modelo, sempre** (leakage, ADR-0001): `proficiencia`, `presenca`,
`preenchimento_caderno`, qualquer métrica de desempenho município-nível do
mesmo ano (`taxa_alfabetizacao`, `gap_meta`, `deficit_per_capita`).
