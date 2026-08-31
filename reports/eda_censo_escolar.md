# EDA — Censo Escolar 2023 agregado por municipio

> Gerado por `src/preprocessing/07_eda_censo_escolar.py`. Gate CRISP-DM dos 9 itens (`.claude/rules/dados.md`), ADR-0011.

- **Fonte:** https://download.inep.gov.br/dados_abertos/microdados_censo_escolar_2023.zip
- **SHA-256 do zip:** `8ed0db8c557137593727b0574d5c99d0abb52491cd7c5769f8cefa98e1fa9e66`
- **Agregado:** 5.569 municipios x 18 colunas
- **Cobertura do join** contra o dataset canonico do ranking: **5231/5232** (100.0%, IC95% Wilson [99.9%, 100.0%])

## 1. Duplicatas (chave e linha inteira)

- Chave `id_municipio` duplicada: **0**
- Linha inteira duplicada: **0**

A agregacao usa `groupby(CO_MUNICIPIO)`, entao duplicata de chave seria bug da propria funcao, nao caracteristica da fonte. Zero e o esperado — o teste serve de guarda contra regressao silenciosa.

## 2. Colunas constantes / quase constantes

| Coluna | Valores distintos | % no valor modal | Veredito |
|---|---:|---:|---|
| `IN_AGUA_POTAVEL` | 727 | 86.2% | ok |
| `IN_ESGOTO_REDE_PUBLICA` | 2531 | 30.7% | ok |
| `IN_ENERGIA_REDE_PUBLICA` | 329 | 93.8% | ok |
| `IN_LIXO_SERVICO_COLETA` | 2082 | 55.0% | ok |
| `IN_INTERNET` | 1251 | 74.1% | ok |
| `IN_INTERNET_ALUNOS` | 2931 | 21.8% | ok |
| `IN_COMPUTADOR` | 1732 | 63.5% | ok |
| `IN_DESKTOP_ALUNO` | 3127 | 23.8% | ok |
| `IN_BIBLIOTECA` | 2844 | 24.7% | ok |
| `IN_BIBLIOTECA_SALA_LEITURA` | 3164 | 26.6% | ok |
| `IN_SALA_LEITURA` | 2797 | 34.6% | ok |
| `IN_LABORATORIO_INFORMATICA` | 2703 | 29.4% | ok |
| `infra_saneamento` | 2358 | 17.4% | ok |
| `infra_conectividade` | 2974 | 14.7% | ok |
| `infra_pedagogico` | 3226 | 10.0% | ok |
| `mat_2ano_total` | 1151 | 0.8% | ok |
| `n_escolas_2ano` | 143 | 13.5% | ok |

Coluna quase constante nao separa municipio nenhum — entra no modelo gastando dimensao sem informar. Sinalizada aqui, decidida na secao de features do dicionario.

## 3. Valores sentinela em numericas

Nenhum dos sentinelas [-1, 9999, 99999, 999999, 88888, 77777] encontrado.

Os indicadores `IN_*` sao proporcoes em [0,1] por construcao da agregacao, entao sentinela do Censo (se existisse no dado bruto) teria sido absorvida na media — a checagem util contra isso e a secao 5 (faixa fora de [0,1]), nao a busca por valor magico.

## 4. Codigos de ausencia mascarados

- Proporcoes fora da faixa [0,1]: **0** ocorrencias

A funcao `agregar_por_municipio` trata nulo do Censo excluindo a escola do peso daquele indicador (nao convertendo para zero) — decisao testada em `test_indicador_nulo_nao_vira_zero`. Por isso nao ha categoria de ausencia disfarcada de valor valido: ausencia vira NaN explicito, contado na secao 6.

## 5. Outliers implausiveis por criterio RELACIONAL

| Criterio relacional | n | Leitura |
|---|---:|---|
| Municipio com 1 unica escola de 2o ano | 752 | % de infra assume so 2 valores (0 ou 1) — nao e erro, e granularidade |
| Media de matricula/escola > 200 | 1 | plausivel em capital, checar se ha valor absurdo |
| Media de matricula/escola < 3 | 0 | escola rural minuscula, plausivel no Brasil |
| `mat_2ano_total` == 0 | 0 | filtrado na origem (`QT_MAT_FUND_AI_2 > 0`) |

Maior media matricula/escola: **203** (municipio `2706448`). Menor: **4.0**.

**Criterio relacional, nao absoluto** (regra do `dados.md`): 'municipio com 300 matriculas' e legitimo; 'municipio com 300 matriculas numa unica escola de 2o ano' e o que mereceria checagem.

## 6. Perfil de nulos por coluna

| Coluna | Nulos no agregado | % | Nulos apos join canonico | % |
|---|---:|---:|---:|---:|
| `IN_AGUA_POTAVEL` | 0 | 0.00% | 1 | 0.02% |
| `IN_ESGOTO_REDE_PUBLICA` | 0 | 0.00% | 1 | 0.02% |
| `IN_ENERGIA_REDE_PUBLICA` | 0 | 0.00% | 1 | 0.02% |
| `IN_LIXO_SERVICO_COLETA` | 0 | 0.00% | 1 | 0.02% |
| `IN_INTERNET` | 0 | 0.00% | 1 | 0.02% |
| `IN_INTERNET_ALUNOS` | 0 | 0.00% | 1 | 0.02% |
| `IN_COMPUTADOR` | 0 | 0.00% | 1 | 0.02% |
| `IN_DESKTOP_ALUNO` | 0 | 0.00% | 1 | 0.02% |
| `IN_BIBLIOTECA` | 0 | 0.00% | 1 | 0.02% |
| `IN_BIBLIOTECA_SALA_LEITURA` | 0 | 0.00% | 1 | 0.02% |
| `IN_SALA_LEITURA` | 0 | 0.00% | 1 | 0.02% |
| `IN_LABORATORIO_INFORMATICA` | 0 | 0.00% | 1 | 0.02% |
| `infra_saneamento` | 0 | 0.00% | 1 | 0.02% |
| `infra_conectividade` | 0 | 0.00% | 1 | 0.02% |
| `infra_pedagogico` | 0 | 0.00% | 1 | 0.02% |
| `mat_2ano_total` | 0 | 0.00% | 1 | 0.02% |
| `n_escolas_2ano` | 0 | 0.00% | 1 | 0.02% |

O nulo apos o join tem duas origens distintas: municipio ausente do Censo agregado (nenhuma escola publica com 2o ano) e indicador nulo em todas as escolas do municipio. A primeira e a que domina — 1 municipios do dataset canonico sem linha no agregado.

## 7. Redundancia entre colunas

Nenhum par com |r| > 0,7.

## 8. Relacao de cada coluna com o alvo

Alvo: `y = (taxa24 < meta_alfabetizacao_2024)`, taxa de falha global 46.7% (n=5232).

AUC isolada de cada coluna (0,5 = sem sinal). **Intra-UF**, porque o produto decide dentro da UF e AUC nacional confundiria regua estadual com sinal real (ADR-0004/0005).

| Coluna | AUC nacional | AUC intra-UF (media pond.) |
|---|---:|---:|
| `IN_AGUA_POTAVEL` | 0.4721 | 0.4955 |
| `IN_ESGOTO_REDE_PUBLICA` | 0.4563 | 0.4979 |
| `IN_ENERGIA_REDE_PUBLICA` | 0.4814 | 0.4986 |
| `IN_LIXO_SERVICO_COLETA` | 0.4829 | 0.4823 |
| `IN_INTERNET` | 0.4665 | 0.4864 |
| `IN_INTERNET_ALUNOS` | 0.5121 | 0.4964 |
| `IN_COMPUTADOR` | 0.4692 | 0.4921 |
| `IN_DESKTOP_ALUNO` | 0.4916 | 0.4978 |
| `IN_BIBLIOTECA` | 0.4897 | 0.5114 |
| `IN_BIBLIOTECA_SALA_LEITURA` | 0.4631 | 0.4868 |
| `IN_SALA_LEITURA` | 0.4855 | 0.4925 |
| `IN_LABORATORIO_INFORMATICA` | 0.4913 | 0.4933 |
| `infra_saneamento` | 0.4537 | 0.4945 |
| `infra_conectividade` | 0.4961 | 0.4981 |
| `infra_pedagogico` | 0.4681 | 0.4885 |
| `mat_2ano_total` | 0.5480 | 0.5610 |
| `n_escolas_2ano` | 0.5686 | 0.5527 |

Leitura: AUC intra-UF perto de 0,5 significa que a coluna nao separa municipios que falham dos que cumprem a meta DENTRO do estado — que e a decisao que o produto toma. Distancia de 0,5 em qualquer direcao e sinal (AUC 0,42 informa tanto quanto 0,58, invertida).

## 9. A NULIDADE de cada coluna prediz o alvo?

O item que nasceu deste projeto (`peso_aluno`, 16,9% de nulos = alunos ausentes do exame, alvo 'Nao' em 100% deles). Aqui: a taxa de falha entre municipios COM dado difere da taxa entre municipios SEM dado?

| Coluna | n sem dado | falha (sem dado) | falha (com dado) | Diferenca | IC95% Wilson (grupo sem dado) |
|---|---:|---:|---:|---:|---|
| `IN_AGUA_POTAVEL` | 1 | 100.0% | 46.7% | +53.3% | [20.6%, 100.0%] |
| `IN_ESGOTO_REDE_PUBLICA` | 1 | 100.0% | 46.7% | +53.3% | [20.6%, 100.0%] |
| `IN_ENERGIA_REDE_PUBLICA` | 1 | 100.0% | 46.7% | +53.3% | [20.6%, 100.0%] |
| `IN_LIXO_SERVICO_COLETA` | 1 | 100.0% | 46.7% | +53.3% | [20.6%, 100.0%] |
| `IN_INTERNET` | 1 | 100.0% | 46.7% | +53.3% | [20.6%, 100.0%] |
| `IN_INTERNET_ALUNOS` | 1 | 100.0% | 46.7% | +53.3% | [20.6%, 100.0%] |
| `IN_COMPUTADOR` | 1 | 100.0% | 46.7% | +53.3% | [20.6%, 100.0%] |
| `IN_DESKTOP_ALUNO` | 1 | 100.0% | 46.7% | +53.3% | [20.6%, 100.0%] |
| `IN_BIBLIOTECA` | 1 | 100.0% | 46.7% | +53.3% | [20.6%, 100.0%] |
| `IN_BIBLIOTECA_SALA_LEITURA` | 1 | 100.0% | 46.7% | +53.3% | [20.6%, 100.0%] |
| `IN_SALA_LEITURA` | 1 | 100.0% | 46.7% | +53.3% | [20.6%, 100.0%] |
| `IN_LABORATORIO_INFORMATICA` | 1 | 100.0% | 46.7% | +53.3% | [20.6%, 100.0%] |
| `infra_saneamento` | 1 | 100.0% | 46.7% | +53.3% | [20.6%, 100.0%] |
| `infra_conectividade` | 1 | 100.0% | 46.7% | +53.3% | [20.6%, 100.0%] |
| `infra_pedagogico` | 1 | 100.0% | 46.7% | +53.3% | [20.6%, 100.0%] |
| `mat_2ano_total` | 1 | 100.0% | 46.7% | +53.3% | [20.6%, 100.0%] |
| `n_escolas_2ano` | 1 | 100.0% | 46.7% | +53.3% | [20.6%, 100.0%] |

**Nenhuma coluna suspeita.** Em todas, o IC95% da taxa de falha no grupo sem dado contem a taxa do grupo com dado — ou seja, a diferenca observada e compativel com acaso. **Sem indicio de vazamento pela ausencia neste agregado.**

---

## Conclusao operacional

- Cobertura do join: 100.0% (IC95% [99.9%, 100.0%]) — sem piso minimo, `SimpleImputer` absorve o resto, mesma decisao do ADR-0009.
- Item 9 e o gate que decide se estas features podem entrar: **limpo**, nenhuma coluna vaza pela ausencia.
