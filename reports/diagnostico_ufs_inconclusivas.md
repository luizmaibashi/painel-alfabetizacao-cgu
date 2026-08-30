# Diagnóstico das 17 UFs inconclusivas

**Data:** 2026-08-29  
**Decisão:** o produto continua em `src/modeling/04_ranking_intra_uf.py` com Random Forest. Nenhuma alternativa foi promovida.

## Pergunta

As 17 UFs com intervalo de confiança que cruza zero são apenas falta de poder estatístico? Uma alternativa de algoritmo fecha alguma delas sem esconder regressões em outras UFs?

## Método

- Fonte e regra de comparação: `reports/ranking_intra_uf.json` canônico.
- Mesmas quatro features, dobras estratificadas adaptativas e predições OOF do produto.
- A direção do baseline permaneceu a prevista por LOO no artefato canônico; ela não foi escolhida olhando o resultado de cada alternativa.
- Triagem pré-fixada de três alternativas: Regressão Logística, Extra Trees regularizado e HistGradientBoosting regularizado. XGBoost não foi incluído: a dependência não está instalada neste ambiente.
- Qualquer promoção após essa triagem exigiria IC bootstrap pareado corrigido por Bonferroni para três alternativas (98,33%), além de não criar novas derrotas relevantes por UF.

## Achados

### Poder explica uma parte, não o todo

Nas 17 UFs, `n_municipios` e largura do IC têm correlação de Spearman **−0,6438** (p=**0,0053**): amostras menores realmente deixam o IC mais largo. Mas apenas 5/17 têm menos de 100 municípios e 9/17 têm 180 ou mais. BA (394), CE (184) e SP (621) continuam inconclusivas no modelo canônico; não é honesto atribuir toda a incerteza a `n` pequeno.

### Algoritmos alternativos não geram melhora promovível

| Modelo | AUC ponderada | Ganho ponderado vs. baseline | Diferença vs. RF canônico |
|---|---:|---:|---:|
| RF canônico | 0,6478 | +0,0269 | — |
| Regressão Logística | 0,6772 | +0,0563 | +0,0294 |
| Extra Trees regularizado | 0,6543 | +0,0335 | +0,0066 |
| HistGradientBoosting | 0,6420 | +0,0211 | −0,0058 |

A média da Regressão Logística é melhor, mas a decisão do produto é por UF, não pela média. Entre as 17 UFs originalmente inconclusivas, a triagem transformou CE, MT e RO em derrotas; GO e PE pareciam vitórias em uma reamostragem curta.

O reteste bootstrap pareado com 5.000 reamostragens eliminou a aparente vitória de GO já no IC95% (+0,1563; IC [−0,0081, +0,3170]). PE mantém IC95% nominal positivo (+0,1527; IC [+0,0040, +0,2969]), mas falha no IC de 98,33% exigido pela correção de três alternativas ([−0,0312, +0,3262]). Logo, nenhuma nova UF pode ser declarada `modelo_vence` sem selecionar algoritmo pós-hoc.

### Instabilidade temporal continua hipótese, não explicação

Só existem 2023 e 2024; há uma única variação anual por município, portanto não existe série suficiente para estimar estabilidade ano a ano. A dispersão municipal de `taxa24 - taxa23` nas inconclusivas vai de 5,50 pp (CE) a 23,74 pp (PB), dado descritivo insuficiente para atribuir causalidade. Um terceiro ano é pré-condição para testar essa hipótese.

## Atualização de fonte — 2026-08-29

Depois desta análise, o Inep confirmou e disponibilizou a planilha municipal
oficial de 2025. Ela cobre 5.208/5.232 municípios deste recorte (99,54%) e
permite o backtest prospectivo formalizado no ticket 0018. Portanto, a frase
"obter um terceiro ano" não é mais uma evolução futura: é a próxima
validação obrigatória antes de qualquer decisão de produto.

## Conclusão provisória

O resultado melhor de média da Logística é exploratório e não sobrevive ao controle de seleção nem à regra de não trocar incerteza por regressões. O RF canônico e os 17 vereditos `inconclusivo` permanecem vigentes **até** o backtest 2025; ele decidirá se o produto pode ser promovido, restringido ou deve se abster.
