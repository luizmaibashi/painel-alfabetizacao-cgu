# ADR-0008 — As features de histórico t-1 são não-funcionais no split temporal

**Data:** 2026-08-29
**Status:** Aceito
**Contexto:** descoberto ao responder "o veredito depende do algoritmo escolhido?"
**Supersede parcialmente:** leitura de mecanismo do ADR-0006 §4 (não o veredito)

---

## 1. O que motivou

Até 2026-08-29 o projeto tinha uma objeção sem resposta medida:

> "Vocês concluíram que o aluno-nível não funciona, mas só testaram XGBoost.
> Perderam porque escolheram o algoritmo errado."

`src/evaluation/04_robustez_algoritmo.py` foi escrito para responder isso. O
resultado respondeu — e, de quebra, expôs um defeito estrutural que nenhum
gate do projeto pegava.

## 2. O experimento

Os três candidatos do torneio, no **mesmo split temporal** (treina 2023,
testa 2024), com as mesmas features e o mesmo baseline do teste canônico
(reusado por import de `02_teste_falsificacao.py`, não reimplementado — o
ADR-0005 documenta o que custa recalcular a régua em separado).

Correção de Bonferroni para 3 comparações informando uma decisão
(α 0,05/3 = 0,0167 → IC de 98,33%), conforme o gate de comparações múltiplas
de `.claude/rules/dados.md`. O veredito usa o intervalo **corrigido**.

| candidato | ROC-AUC | diferença vs baseline (0,6331) | IC 98,33% | veredito |
|---|---|---|---|---|
| XGBoost (800/8, canônico) | 0,6047 | **−0,0284** | [−0,0354, −0,0217] | perde com significância |
| Random Forest (800/12) | **0,6322** | −0,0009 | [−0,0042, +0,0024] | empata |
| Regressão Logística (C=1,0) | **0,6325** | −0,0006 | [−0,0034, +0,0021] | empata |

**Nenhum supera o baseline.** O veredito de negócio do ADR-0006 se mantém
intacto: a meta do PDE é gratuita e nenhum modelo a bate, então a recomendação
continua sendo usá-la.

**Mas a magnitude da derrota era artefato do algoritmo.** O −0,0284 do
XGBoost é ~30× maior que o −0,0009 do Random Forest. Dizer "o modelo perde
por 0,028" era verdade sobre *um* modelo, não sobre a classe.

## 3. O achado que explica o resultado

Um `UserWarning` do sklearn na saída (`Skipping features without any observed
values`) levou à inspeção do dado **por ano de split** — algo que nenhuma EDA
do projeto tinha feito, porque todas rodaram sobre o dataset inteiro.

Estado das 6 features de histórico t-1 **no ano de treino (2023)**:

| feature | 2023 (treino) | 2024 (scoring) |
|---|---|---|
| `n_alunos_hist_escola_t1` | **100% nula** → sklearn descarta a coluna em silêncio | 78,2% nula |
| `n_alunos_hist_municipio_t1` | **100% nula** → descartada em silêncio | 28,5% nula |
| `possui_hist_escola_t1` | **constante 0** (variância zero) | 0/1 |
| `possui_hist_municipio_t1` | **constante 0** (variância zero) | 0/1 |
| `absenteismo_hist_escola_t1` | **1 valor único por UF** | 3 a 21 valores por UF |
| `absenteismo_hist_municipio_t1` | **1 valor único por UF** | até 50 valores por UF |

Verificado nas 23 UFs: em 2023, `groupby("sigla_uf")[col].nunique()` devolve
**exatamente 1 para todas**, nos dois níveis.

### Por que, mecanicamente

A base tem 2 anos. O t-1 de 2023 seria 2022, que não existe. Então:

1. `calcular_historico_t1` produz histórico só para 2024
   (`02_extrair_snapshot.py:162`, `agg["ano"] = agg["ano"] + 1`).
2. `juntar_historico` deriva `possui_hist_*` de `.notna()` **antes** da
   imputação (linha 176) — correto, mas em 2023 dá 0 para todo mundo.
3. `imputar_historico` (linha 193) preenche **só** as duas colunas de
   absenteísmo, pela mediana da UF. Em 2023 tudo é nulo, então todo aluno
   recebe a mediana da própria UF — a coluna vira **função determinística de
   `sigla_uf`**, que já está no modelo como categórica.
4. Os contadores `n_alunos_*` **não entram nessa imputação** e continuam
   100% nulos. O `SimpleImputer(strategy="median")` não consegue mediana de
   coluna toda nula e **descarta a coluna**, emitindo apenas um `UserWarning`.

**O modelo declara 12 features e treina com 10.** Duas somem sem log, duas são
constantes, e duas são cópias de `sigla_uf`.

### Consequência

É **training-serving skew** — proibido explicitamente em
`.claude/rules/dados.md`: *"o modelo passa a receber um dado diferente do que
viu no treino. Nada quebra — a métrica offline continua boa."*

E explica o experimento da §2 sem hipótese adicional:

- **XGBoost** (800 árvores, depth 8) tem capacidade para ajustar o mapeamento
  degenerado de 2023 — inclusive a redundância entre `absenteismo_hist_*` e
  `sigla_uf`. Esse mapeamento não vale em 2024, e o AUC cai para 0,6047. Era
  o candidato com maior gap treino-validação do torneio (+0,0303 contra
  +0,0064 do RF e +0,0010 da Logística); o gap já apontava para isso.
- **Random Forest e Logística** não se agarram ao ruído e pousam no sinal que
  sobra — meta do PDE, população, UF. Ou seja, **re-derivam o baseline**, e
  por isso empatam com ele em 0,632.

## 4. O que isto muda na tese do projeto

A tese fica **mais forte e mais precisa**.

- **Antes:** "o sinal que o modelo captura é municipal; usá-lo direto funciona
  melhor que passá-lo por um modelo de aluno."
- **Agora:** "as features de aluno e escola são **estruturalmente
  inutilizáveis** num split temporal de 2 anos, porque o ano de treino não tem
  histórico. O que resta é o sinal municipal, e o melhor modelo possível sobre
  ele **é** o baseline. Os modelos que não overfitam provam isso ao empatar
  com ele em 0,632 contra 0,6331."

Um modelo que empata com uma regra gratuita não justifica existir — a
conclusão de negócio não muda. Mas o **motivo** deixa de ser "aluno não tem
sinal" e passa a ser "com 2 anos de dado, não dá para *testar* se aluno tem
sinal": o desenho temporal consome o único ano de histórico disponível.

Isso converte o pedido de dado novo ao INEP de opinião em consequência medida:
**um terceiro ano não é melhoria incremental, é pré-condição** para a pergunta
do enunciado ser respondível com validação temporal.

## 5. Decisão

1. **Manter o veredito e a recomendação de negócio.** Nenhum candidato supera
   o baseline; a meta do PDE continua sendo a resposta.
2. **Parar de reportar o −0,0284 como "a" distância do modelo ao baseline.**
   Reportar a faixa dos três candidatos e dizer que o pior caso é o XGBoost.
3. **Registrar o skew como limitação de primeira ordem** no README §9, não
   como nota de rodapé.
4. **Não "consertar" imputando os contadores.** Imputar `n_alunos_*` em 2023
   inventaria um histórico que não existe — trocaria uma falha visível por
   uma invisível. A ausência é a informação correta.
5. **Alinhar SHAP e falsificação.** `01_shap_interpretabilidade.py` ganhou
   `--temporal`: ele usava `train_test_split` aleatório, que mistura 2024 no
   treino e devolve as 12 features ao modelo — então §7.1 e §7.2 do README
   descreviam **modelos diferentes**. Artefatos separados
   (`shap_interpretabilidade_temporal.json`), sem sobrescrever o canônico.

## 6. Alternativas descartadas

| Alternativa | Por que não |
|---|---|
| Imputar `n_alunos_*` com 0 ou mediana em 2023 | Inventa histórico inexistente. Trocaria descarte silencioso por valor falso — pior, porque some do radar |
| Remover as 6 features de histórico do modelo | Elas funcionam no split aleatório e no ranking intra-UF. Removê-las globalmente resolveria o sintoma num desenho e destruiria valor noutro |
| Usar só split aleatório, abandonando o temporal | O split aleatório vaza informação temporal (linhas de 2024 no treino prevendo 2024). Seria trocar rigor por número bonito |
| Trocar o modelo final para Random Forest | Empatar com o baseline não é vencer. E escolher o algoritmo *depois* de ver qual dá o número melhor é exatamente o que a correção de Bonferroni existe para punir |

## 7. Critério de aceitação

- `reports/robustez_algoritmo.json` existe e traz os três candidatos com IC
  corrigido — gerado por `src/evaluation/04_robustez_algoritmo.py`.
- `tests/test_robustez_algoritmo.py` prova que o bootstrap desse script
  reproduz `ic_diferenca_auc` do `02_teste_falsificacao.py` em α=0,05, e que
  a correção de Bonferroni **alarga** o intervalo.
- `tests/test_pipeline_preprocessamento.py` prova que `descrever_snapshot`
  varia com o dataframe (uma constante literal reprova).

## 8. Achado colateral corrigido junto

`02_tournament_modelos.py` gravava em `reports/metrics_tournament.json` a
string fixa `"snapshot": "local-only (sem territorio/socioeconomico/meta)"`,
enquanto o mesmo JSON listava `populacao_total`,
`meta_alfabetizacao_2024_imputada` e `sigla_uf` em `features_usadas`. O
rótulo citava ainda um flag `--local-only` que o script nunca teve.

Quem lesse o relatório concluiria que o ROC-AUC ~0,68 vinha de sinal
puramente local. Substituído por `descrever_snapshot(df)`, que deriva o
rótulo das colunas presentes e distingue três estados
(`local-only` / `parcial` / `full`).

Mesma classe da "guarda silenciosa" do `AGENTS.md`: o rótulo errado não
quebra nada, não derruba teste — só convence.
