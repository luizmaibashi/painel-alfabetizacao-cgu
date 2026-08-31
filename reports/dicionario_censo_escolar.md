# Dicionário — Censo Escolar 2023 agregado por município

> Gate CRISP-DM (`.claude/rules/dados.md`): dicionário obrigatório antes de
> feature engineering. Fonte do dado e diagnóstico numérico em
> [`eda_censo_escolar.md`](eda_censo_escolar.md). Decisão em
> [`ADR-0011`](../docs/adr/0011-enriquecimento-infraestrutura-censo-escolar.md).

## Proveniência

| Item | Valor |
|---|---|
| Fonte | `https://download.inep.gov.br/dados_abertos/microdados_censo_escolar_2023.zip` |
| SHA-256 do zip | `8ed0db8c557137593727b0574d5c99d0abb52491cd7c5769f8cefa98e1fa9e66` |
| Publicação (datas internas do zip) | 2024-02-19 |
| Data de referência do Censo | maio/2023 |
| Rastro de extração | `src/preprocessing/06_agregar_censo_escolar.py` (baixa, filtra, agrega) |
| Credencial necessária | nenhuma — download público direto |

**Por que 2023 e não 2024.** O Censo Escolar 2024 existe (verificado
2026-08-31, HTTP 200) mas o servidor do Inep reporta `Last-Modified:
2026-07-08`. O alvo do modelo é o desfecho do ciclo **2024**; usar um dado
publicado depois do desfecho daria ao modelo informação indisponível no
momento da decisão — o data leakage que o enunciado da Fase 3 (pág. 3) manda
tratar e o skew treino-serviço do [ADR-0008](../docs/adr/0008-skew-treino-servico-nas-features-de-historico.md).

**Limitação declarada:** se este enriquecimento for promovido ao backtest
prospectivo 2025, a escolha do ano precisa ser refeita **para aquele ciclo**.
2023 não serve automaticamente para todo ciclo.

## Conexão com objetivo de negócio

**Hipótese que este dataset deve confirmar ou refutar:** as 8 UFs com veredito
`inconclusivo` no backtest 2025 (ADR-0010) ficam assim por **falta de
variável** — especificamente, por o modelo não enxergar condição material da
escola — e não por falta de poder estatístico.

É a terceira tentativa de responder essa mesma pergunta neste projeto:

| Tentativa | Fonte | Desfecho |
|---|---|---|
| 1ª (ADR-0009) | IDHM-M 2010 | **Misto** — melhora PE/MG/RN, regride BA. Não promovido |
| 2ª (ADR-0009 §7) | FUNDEB | **Adiado** — 4 rotas de acesso, todas com fricção alta |
| 3ª (ADR-0011) | Censo Escolar 2023 | esta |

**Por que esta fonte e não outra:** é a única das três sem barreira de acesso
(download direto, sem credencial, sem Power BI, sem BigQuery) e a única
autorizada nominalmente pelo enunciado que ainda não tinha sido tentada em
grão municipal. A tentativa anterior de usar Censo Escolar **em nível de
escola** falhou por motivo estrutural (README linha 586): o `id_escola` do
dataset de alunos é sintético, sem correspondência com o `CO_ENTIDADE`
oficial. O grão municipal contorna isso — `CO_MUNICIPIO` é código IBGE real.

**Ligação com a pergunta de negócio do enunciado:** "Quais fatores mais
impactam a alfabetização?" (pág. 5). Infraestrutura escolar é candidato
óbvio a fator, e responder "medimos e não impacta o ranking intra-UF" é
resposta tão válida quanto o contrário.

## Recorte da população (o que entra e o que fica de fora)

O Indicador Criança Alfabetizada mede alunos do **2º ano do fundamental da
rede pública**. Agregar todas as escolas do município (creche, médio,
privada) descreveria população diferente da que o alvo mede.

| Filtro | Coluna | Escolas restantes |
|---|---|---:|
| (bruto) | — | 217.625 |
| Em atividade | `TP_SITUACAO_FUNCIONAMENTO == 1` | 180.230 |
| Rede pública (federal/estadual/municipal) | `TP_DEPENDENCIA in (1,2,3)` | 137.914 |
| Com matrícula no 2º ano | `QT_MAT_FUND_AI_2 > 0` | **73.660** |

Matrículas de 2º ano cobertas: **2.357.055** — compatível com a coorte anual
brasileira, serve de sanity check do recorte.

## Colunas (pós-limpeza)

Uma linha por município. Todo indicador `IN_*` é **proporção ponderada pela
matrícula do 2º ano**, não média simples entre escolas (ver "Features
criadas").

| Coluna | Tipo | Significado | Interpretação de negócio |
|---|---|---|---|
| `id_municipio` | str (7) | Código IBGE, zero-padded | Chave de join com o dataset canônico |
| `IN_AGUA_POTAVEL` | float [0,1] | % de matrículas em escola com água potável | Condição sanitária básica |
| `IN_ESGOTO_REDE_PUBLICA` | float [0,1] | % com esgoto em rede pública | Saneamento formal (vs. fossa) |
| `IN_ENERGIA_REDE_PUBLICA` | float [0,1] | % com energia da rede | Viabiliza qualquer recurso elétrico |
| `IN_LIXO_SERVICO_COLETA` | float [0,1] | % com coleta de lixo | Serviço urbano presente |
| `IN_INTERNET` | float [0,1] | % com internet (qualquer uso) | Conectividade da escola |
| `IN_INTERNET_ALUNOS` | float [0,1] | % com internet **para alunos** | Distingue uso pedagógico de administrativo |
| `IN_COMPUTADOR` | float [0,1] | % com computador | Equipamento presente |
| `IN_DESKTOP_ALUNO` | float [0,1] | % com desktop para aluno | Equipamento de uso discente |
| `IN_BIBLIOTECA` | float [0,1] | % com biblioteca | Espaço de leitura formal |
| `IN_BIBLIOTECA_SALA_LEITURA` | float [0,1] | % com biblioteca ou sala de leitura | Versão ampla do anterior |
| `IN_SALA_LEITURA` | float [0,1] | % com sala de leitura | Alternativa de menor porte |
| `IN_LABORATORIO_INFORMATICA` | float [0,1] | % com laboratório de informática | Infra digital dedicada |
| `mat_2ano_total` | int | Matrículas de 2º ano no município | Porte da coorte avaliada |
| `n_escolas_2ano` | int | Escolas públicas com 2º ano | Capilaridade da rede |

## Features criadas

| Feature | Fórmula | Interpretação | Decisão |
|---|---|---|---|
| `infra_saneamento` | média de `IN_AGUA_POTAVEL`, `IN_ESGOTO_REDE_PUBLICA`, `IN_ENERGIA_REDE_PUBLICA`, `IN_LIXO_SERVICO_COLETA` | Índice de condição material básica | **Candidata a feature** |
| `infra_conectividade` | média de `IN_INTERNET`, `IN_INTERNET_ALUNOS`, `IN_COMPUTADOR`, `IN_DESKTOP_ALUNO` | Índice de infra digital | **Candidata a feature** |
| `infra_pedagogico` | média de `IN_BIBLIOTECA`, `IN_BIBLIOTECA_SALA_LEITURA`, `IN_SALA_LEITURA`, `IN_LABORATORIO_INFORMATICA` | Índice de espaço pedagógico | **Candidata a feature** |

**Por que índices e não as 12 colunas individuais.** `FEATURES_BASE` tem 4
colunas e várias UFs treinam com 40–100 municípios (piso do ADR-0004). Somar
12 features nesse regime é convite a overfitting. Três índices mantêm a
dimensionalidade na ordem de grandeza do enriquecimento anterior
(`FEATURES_IDHM`, 4 colunas). A EDA §7 confirma redundância alta entre os
indicadores individuais, o que sustenta a agregação.

**Por que `mat_2ano_total` e `n_escolas_2ano` NÃO viram feature.** Medido na
EDA: são as únicas colunas com sinal isolado real (AUC intra-UF 0,561 e
0,553), **mas** correlacionam r = +0,985 e r = +0,838 com `populacao_total`,
que já está em `FEATURES_BASE`. Incluí-las adicionaria colinearidade sem
informação nova — o sinal que carregam o modelo já captura. Ficam na saída
como contexto de leitura (quantas escolas sustentam o percentual de cada
município), não como entrada do modelo.

## Predição registrada antes da medição

Regra do `AGENTS.md` ("predição antes da medição"). Registrado em
2026-08-31, **antes** de rodar `08_experimento_infra_escolar.py`:

- **Evidência na mesa:** AUC intra-UF isolada de todos os índices entre
  0,4885 e 0,4981 (colada em 0,5); informação genuinamente nova (r ≈ 0,02–0,08
  com `populacao_total`), mas sem poder discriminante univariado.
- **Predição do Luiz:** **positivo** — o modelo multivariado acha interação
  que a análise univariada não vê, e ao menos 1 UF sai de `inconclusivo`
  para `modelo_vence` sem nenhuma regredir.
- **Leitura contrária (a favor de negativo):** o pouco sinal disponível já
  está capturado por `populacao_total`.

O erro de predição — em qualquer direção — é o registro que interessa.
