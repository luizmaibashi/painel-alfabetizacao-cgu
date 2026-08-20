# Model Card — Tech Challenge Fase 3

**Projeto:** Predição de Alfabetização Infantil no Brasil  
**Versão:** 1.0 (2026-08-20)  
**Entrega:** Dois modelos com vereditos diferentes — um reprovado, um aprovado

---

## 1. Model Details

### 1.1 Modelo A — Previsão aluno-nível (não recomendado)

| Atributo | Valor |
|---|---|
| **Nome** | `modelo_aluno_nivel_xgboost` |
| **Tipo** | Classificação binária supervisionada |
| **Framework** | scikit-learn + XGBoost 2.1.3 |
| **Alvo** | `alfabetizado` (Sim=1 / Não=0) |
| **Grão** | Aluno individual |
| **Features de entrada** | 12 (após remoção de vazamento): histórico municipal (absenteísmo t-1, contador, flag), rede, caderno, histórico de escola (4 features contextuais) |
| **Hyperparâmetros finais** | `n_estimators=200, max_depth=6, learning_rate=0.1, subsample=0.8` (tuning via GridSearchCV em StratifiedKFold(5)) |
| **Outputs** | Probabilidade de estar alfabetizado (0–1) |
| **Versão do scikit-learn** | 1.5.2 (versão pinada; 1.8→1.9 muda Recall do baseline em ~1,6pp com mesmo seed) |

**Pipeline de pré-processamento:**
- `SimpleImputer(strategy='median')` para numéricas
- `RobustScaler()` (robusto a outliers)
- `OneHotEncoder()` para categóricas
- Adaptativo: descobre colunas disponíveis em vez de listar à mão (evita ignorar features novas)

---

### 1.2 Modelo B — Previsão municipal intra-UF (recomendado com ressalvas)

| Atributo | Valor |
|---|---|
| **Nome** | `modelo_municipio_intra_uf_random_forest` |
| **Tipo** | Classificação binária supervisionada, um modelo por estado |
| **Framework** | scikit-learn RandomForest |
| **Alto** | `taxa_municipio_2024 < meta_2024` (sim/não) |
| **Grão** | Município dentro de cada UF (não comparável entre estados) |
| **Features de entrada** | 4: taxa de alfabetização 2023, meta do PDE 2024, população total, UF (intra-modelo) |
| **Hyperparâmetros** | `n_estimators=200, max_depth=6` (pequeno; n por estado varia de 102 a 801) |
| **Outputs** | Probabilidade de falhar a meta (0–1); predições out-of-fold (cada município pontuado por modelo que não o viu) |
| **Quantidade de modelos** | 23 modelos (um por UF do Brasil) |

**Validação:**
- Leave-One-UF-Out (LOUO): modelo treinado em 22 UFs, testado na 23ª
- Garantia: nenhum município do estado de teste apareceu no treino (elimina data leakage intra-estado)

---

## 2. Intended Use

⚠️ **Leia com cuidado.** Este card descreve dois modelos com usos diferentes e limitações severas.

### 2.1 Modelo A — Aluno-nível (NÃO RECOMENDADO)

**Caso de uso original (enunciado):**  
Apoiar busca ativa escolar: identificar alunos em risco de não-alfabetização para intervenção pedagógica. Decisão micro (indivíduo), não macro.

**Veredito:**  
❌ **Não use este modelo.** Falhou no teste de falsificação — não supera o baseline municipal.

**Por quê:**
- ROC-AUC 0,6013 (modelo) vs 0,6331 (meta do PDE aplicada uniformemente)
- Diferença: −0,0318, IC95% [−0,0374, −0,0261] — inteiramente negativo
- Interprets: em 5 de 5 orçamentos de busca ativa testados (5%, 10%, 20%, 30%, 50% dos alunos), o modelo perde do baseline trivial

**Achado técnico:**
Teste de resíduo mostrou que adicionar features de aluno ao baseline municipal **piora** o desempenho (AUC: 0,6331 → 0,6013, IC95% [−0,0374, −0,0261] com significância). Não há sinal individual a extrair com os dados disponíveis.

---

### 2.2 Modelo B — Municipal intra-UF (RECOMENDADO COM RESSALVAS)

**Caso de uso:**  
Priorizar municípios em risco de falhar a meta do Indicador Criança Alfabetizada no ciclo seguinte, **dentro de um estado específico**. Decisão macro, planejamento de políticas.

**Veredito:**  
✅ **Funciona, mas com condições.**
- ROC-AUC 0,6478 (modelo) vs 0,6209 (baseline honesto previsto por Leave-One-UF-Out)
- Diferença: +0,027, IC95% [+0,007, +0,048] — ganho pequeno, mas significativo
- Veredito por UF (IC95% pareado): vence em 3 (PR, RJ, RS), perde em 3 (MG, RN, TO), empata em 17

**Achado técnico:**
O modelo é um **seguro contra errar a direção**, não um ranqueador superior. Funciona bem nas 7 UFs onde a direção (priorize quem estava melhor vs quem estava pior) não é previsível de fora. Nas 16 UFs previsíveis, o modelo e a regra simples empatam.

---

## 3. Model Performance

### 3.1 Modelo A — Aluno-nível

#### Teste de falsificação (critério de sucesso definido *antes* de qualquer treino)

| Modelo / Baseline | ROC-AUC | Confiança |
|---|---|---|
| Taxa municipal 2023 (baseline fraco) | 0,5816 | — |
| **Meta PDE 2024** (baseline forte) | **0,6331** | — |
| **Modelo XGBoost aluno-nível** | **0,6013** | — |
| **Diferença** | **−0,0318** | IC95% [−0,0374, −0,0261] |

**Interpretação:** o modelo perde do baseline com significância estatística. A meta municipal aplicada igualmente a todos os alunos supera o modelo completo de 12 features.

#### Performance por métrica

| Métrica | Treino (val 5-fold) | Teste |
|---|---|---|
| ROC-AUC | 0,6054 | 0,6013 |
| Recall (classe "Não") | 0,729 | 0,702 |
| Precision (classe "Não") | 0,431 | 0,428 |
| F1 | 0,542 | 0,534 |
| Gap treino-validação | +0,013 | — |

*(Recall da classe "Não" é a métrica principal — falso negativo (aluno em risco não identificado) é o erro caro para busca ativa.)*

#### Recall @ K (orçamento de busca ativa)

Se você pudesse visitar K% dos alunos em ordem do modelo, quantos em risco você encontraria?

| Orçamento | Modelo | Baseline meta PDE | Diferença |
|---|---|---|---|
| 5% | 23,4% | 24,8% | −1,4pp |
| 10% | 37,2% | 39,1% | −1,9pp |
| 20% | 56,1% | 58,7% | −2,6pp |
| 30% | 69,4% | 71,2% | −1,8pp |
| 50% | 85,9% | 86,8% | −0,9pp |

---

### 3.2 Modelo B — Municipal intra-UF

#### Teste de falsificação (Leave-One-UF-Out)

| Abordagem | ROC-AUC | Confiança |
|---|---|---|
| Regra trivial "pior em 2023" | 0,4032 | — |
| Regra trivial "melhor em 2023" (invertida) | 0,5968 | — |
| **Baseline honesto** (direção por LOO) | **0,6209** | — |
| **Modelo intra-UF** | **0,6478** | — |
| **Ganho sobre baseline** | **+0,0270** | IC95% [+0,0073, +0,0476] |

**Interpretação:** o modelo vence o baseline com significância. Funciona como seguro contra escolher a direção errada.

#### Performance por UF (IC95% pareado)

| UF | N | AUC Baseline | AUC Modelo | Veredito | Direção |
|---|---|---|---|---|---|
| PR | 399 | 0,5981 | 0,6378 | Vence | Melhor em 23 → falha mais |
| RJ | 92 | 0,5715 | 0,6289 | Vence | Melhor em 23 → falha mais |
| RS | 497 | 0,6186 | 0,6582 | Vence | Melhor em 23 → falha mais |
| **17 outros** | ... | ... | ... | **Empata** | Variado |
| MG | 853 | 0,6241 | 0,6089 | Perde | Pior em 23 → falha mais |
| RN | 167 | 0,6302 | 0,6141 | Perde | Pior em 23 → falha mais |
| TO | 139 | 0,6176 | 0,5987 | Perde | Pior em 23 → falha mais |

**Municípios avaliados:** 5.216 (predições out-of-fold)

---

## 4. Limitations

⚠️ **Limitação mais consequente: comparação entre estados não é válida.**

Cada estado aplica sua própria avaliação do Compromisso Nacional Criança Alfabetizada. Variações entre anos chegam a ±20 pontos percentuais:
- **RS 2023→2024:** 73,1% → 53,1% (queda de 20pp; 90,5% dos municípios falharam a meta)
- **MG 2023→2024:** 62,8% → 75,1% (alta de 12,3pp; 20,5% falharam)

Correlação entre variação do estado e taxa de falha: **−0,651** (mais forte que correlação com nível de 2023: −0,431). Isso significa: **não é aprendizado real, é mudança de régua na aplicação da prova.**

Ordenar municípios de UFs diferentes na mesma escala compara réguas distintas. Um gestor lendo um ranking nacional diracionaria recursos para municípios gaúchos ("90% falharam") quando parte substancial do efeito é a régua do estado, não a política municipal.

**Consequência:** os marts `agg_municipio_ranking` e `agg_priorizacao` da nossa própria Fase 2 (em produção) sofrem do mesmo problema. A engenharia daqueles marts é sólida; a *leitura nacional* que se faz em cima deles é que é inválida.

---

### Limitações específicas

| # | Limitação | Severidade | Mitigação |
|---|---|---|---|
| **1** | Modelo aluno-nível não supera baseline municipal | Alto | Use a meta do PDE em vez do modelo para busca ativa |
| **2** | Comparação entre estados invalida | Alto | Sempre compare **dentro do estado**; nunca entre estados |
| **3** | Direção não previsível em 7 UFs | Médio | Modelo protege contra errar a direção nessas UFs; nas outras, regra simples já resolve |
| **4** | Sem validação em 2025 (ano real de uso) | Médio | Modelo treinado em 2023–2024; performance em novo ciclo desconhecida |
| **5** | `peso_aluno` excluído por vazamento de nulidade | Técnico | Nenhum impacto no uso; foi detecção correta de vazamento |
| **6** | `caderno=12` (11,6% SHAP) sem causa confirmada | Técnico | Resolvido por análise de dados (crosstab), não documentação externa; categoria representa alta ausência |
| **7** | SICONFI não buscado | Técnico | Decisão documentada (ADR-0002): teste barato já mostrou limitação é o modelo tentar ser baseline municipal, não falta de features |
| **8** | Variação de versão do scikit-learn (~1,6pp em Recall) | Técnico | `requirements.txt` pinado mitiga (não elimina); usar ambiente reproduzível |

---

## 5. Training Data

### 5.1 Fonte e proveniência

| Item | Detalhe |
|---|---|
| **Dataset principal** | `Alunos.csv` (57.782 alunos, 2023–2024) |
| **Origem** | Indicador Criança Alfabetizada / Pesquisa Alfabetiza Brasil (INEP), não SAEB clássico (prova menor: 16 itens MC + 3 construídas vs 169 do SAEB) |
| **Herança** | Processado no nível Bronze→Silver da Fase 2; original nunca processado além disso |
| **Metadados** | Identificador: sequencial (60000002–60042811), sem mapeamento oficial para `CO_ENTIDADE` do Censo; território via IBGE + arquivo de metas local |
| **Timestamp da última atualização** | 2024 (ano do dado); baseado em 2023 como preditores |

### 5.2 Tamanho e composição

| Grupo | N | Nota |
|---|---|---|
| Alunos totais | 57.782 | |
| Alunos avaliados (rótulo = medição real) | 48.055 | Exclui ausentes (foram rotulados "Não" por convenção, não medição) |
| Treino (5-fold CV) | ~38.444 | Validação cruzada estratificada mantida dentro do treino |
| Teste (holdout final) | ~9.611 | Tocado uma única vez após tuning |
| **Modelo A teste final** | 24.505 | Subconjunto com rótulo de medição real (filtra pre-processamento) |

### 5.3 Distribuição do alvo

| Classe | N | Proporção |
|---|---|---|
| Alfabetizado (Sim) | 28.308 | 58,9% |
| Não-alfabetizado (Não) | 19.747 | 41,1% |

**Corte utilizado:** `proficiencia >= 743` pontos (Indicador Criança Alfabetizada, sem sobreposição: máx(Não)=742,97, mín(Sim)=743,02).

### 5.4 Features — origem e decisão

#### Features de histórico municipal (60,9% SHAP)

| Feature | Origem | Decisão | Razão |
|---|---|---|---|
| `taxa_nao_alfabetizacao_t1` | Alunos avaliados em 2023, agregado por município | Mantida | Sinal forte; coeficiente de correlação 0,65 com alvo 2024 |
| `contador_falhas_municipio` | Contagem cumulativa de ciclos com falha | Mantida | Padrão persistente |
| `flag_regiao_prioritaria` | Derivado de meta vs performance histórica | Mantida | Contexto administrativo |

#### Features categóricas (13,3% + 11,6% SHAP)

| Feature | Valores | Decisão | Razão |
|---|---|---|---|
| `rede` | Estadual / Municipal / Federal / Privada | OneHot | Proxy de capacidade administrativa |
| `caderno` | 1, 10, 11, 12 | OneHot | Categoria 12 = 79,7% ausência; análise cruzada resolveu causa |

#### Features de contexto escolar (14,2% SHAP)

| Feature | Detalhe | Decisão |
|---|---|---|
| `indice_socioeconmico_escola` | KNN-imputado na Fase 2 | Mantida |
| `taxa_repeticao_escola` | Agregado por escola | Mantida |
| `taxa_distorcao_idade_escola` | Agregado por escola | Mantida |
| `tamanho_escola` | Categorizado em faixas | Mantida |

### 5.5 Tratamento de vazamento

**Cinco colunas foram identificadas como vazamento do mesmo evento** — *aluno faltou à prova* — e removidas:

| Coluna | Tipo | Ocorrência | Motivo da exclusão |
|---|---|---|---|
| `proficiencia` | Valor | 100% colinear com alvo | Medida que define o corte (743 pontos) |
| `presenca` | Valor | 100% colinear com alvo | "Ausente" → "Não alfabetizado" por convenção |
| `preenchimento_caderno` | Valor | 78,4% colinear | Faltosos não preenchem; faltosos = Não |
| `peso_aluno` | Nulidade | 16,9% nulo = 100% "Não" | Peso amostral vazava apenas pela ausência |
| `caderno=12` | Categoria | 79,7% ausência; 87,3% "Não" | Artefato de ausência, não característica |

**Gate automatizado:** script `src/preprocessing/03_guarda_leakage.py` testa todo candidato por (A) nulidade prediz alvo, (B) valor isola alvo, (C) AUC isolada alta — roda como gate de CI antes de qualquer treino.

### 5.6 Imputação

| Coluna | Estratégia | Justificativa |
|---|---|---|
| Numéricas | `SimpleImputer(strategy='median')` | Robusta a outliers; não assume distribuição |
| Categóricas | `SimpleImputer(strategy='most_frequent')` | Última categoria antes do One-Hot Encoding |
| **Nulos que restam** | Preservados como categoria separada no One-Hot | Nulo é sinal: "este campo não é confiável aqui" |

---

## 6. Evaluation Methodology

### 6.1 Protocolo de validação

#### Modelo A (aluno-nível)

1. **StratifiedKFold(5)** — validação cruzada estratificada mantida 100% dentro do treino
2. **Tuning de hiperparâmetro:** GridSearchCV sobre 5 folds, testando 18 combinações (3 valores para cada de `max_depth`, `learning_rate`, `subsample`)
3. **Teste tocado uma única vez** — *após* escolher melhor hyperparâmetro, nunca antes (elimina snooping)
4. **Split temporal** — treina 2023, testa 2024 (checagem separada, mais próxima do uso real)

#### Modelo B (municipal intra-UF)

1. **Leave-One-UF-Out (LOUO)** — modelo treinado em 22 UFs, testado na 23ª (nenhum município do estado de teste aparece no treino)
2. **Out-of-fold predictions** — cada município pontuado por modelo que não o viu durante treino (elimina overfitting de ranking)
3. **Ablação de features** — mede quanto cada bloco (taxa, meta, UF, contexto) contribui para o ganho
4. **IC95% pareado (bootstrap)** — toda comparação modelo vs baseline reporta intervalo de confiança

### 6.2 Baselines (critério de referência)

#### Para Modelo A
- Taxa de não-alfabetização municipal 2023 (baseline fraco): AUC 0,5816
- Meta do PDE 2024, aplicada igualmente a todos os alunos (baseline forte): AUC **0,6331** ← o que vence
- Modelo: AUC 0,6013 (perde)

#### Para Modelo B
- Regra trivial "priorize quem estava pior em 2023": AUC 0,4032 (inválida — é simétrica)
- Regra trivial "melhor em 2023" (a mesma, invertida): AUC 0,5968
- Baseline honesto (direção prevista por Leave-One-UF-Out): AUC **0,6209** ← o que se compara
- Modelo: AUC 0,6478 (vence)

---

## 7. Ethical Considerations

### 7.1 Viés por estado (regra estadual)

**Problema:** cada estado aplica sua própria avaliação. Variações de ±20pp entre anos refletem mudanças de régua, não aprendizado.

**Risco:** um modelo treinado com dados de múltiplos estados aprendia a diferenciar estados, não municípios. Deixava municípios gaúchos sempre "em risco" (porque RS teve queda de 20pp) mesmo que a política municipal fosse excelente.

**Mitigação:** Modelo B traz um modelo **por UF**. Baseline municipal é normalizado dentro do estado. O painel (`reports/painel_intra_uf.html`) não oferece visão nacional *de propósito* — a interface força comparação intra-UF.

---

### 7.2 Confiabilidade do rótulo

**Problema:** alunos ausentes são rotulados "Não" por *convenção*, não porque foram medidos.

**Risco:** modelo poderia aprender a detectar ausência em vez de não-alfabetização real.

**Mitigação:** 
- Remover alunos ausentes da população de modelagem (48.782 → 48.055)
- Teste de resíduo confirmou: adicionar features de aluno ao baseline municipal **piora** resultado (−0,0318, IC95% [−0,0374, −0,0261])
- Cinco colunas de vazamento foram identificadas e removidas

---

### 7.3 Inequidade territorial

**Problema:** dados concentrados em certas regiões (amostragem desigual da Pesquisa Alfabetiza Brasil).

**Detalhe:** este modelo não foi desenvolvido com foco em equidade territorial — é herdado da Fase 2.

**Status:** lacuna documentada, fora do escopo desta fase, mas registrada em Limitações.

---

### 7.4 Falta de dados de 2025

**Problema:** modelo treinado em 2023–2024, nunca validado no ano de uso real.

**Risco:** performance pode degradar (concept drift, mudança de distribuição).

**Mitigação:** ADR-0002 documentou essa lacuna e a aceitamos como trade-off — o enunciado não exige monitoramento.

---

## 8. Caveats and Recommendations

### 8.1 Usar Modelo B, não Modelo A

Para **busca ativa de alunos:**
- ❌ Não use o modelo aluno-nível
- ✅ Use a **meta do PDE do município** (aplicada igualmente a todos os alunos)
- Razão: mais simples, mais barata de manter (zero pipeline ML em produção), e estatisticamente mais eficaz com os dados disponíveis

Para **priorização de municípios:**
- ✅ Use o **modelo intra-UF** (Modelo B)
- Sempre compare **dentro de um estado**, nunca entre estados
- **Verifique a direção antes de ordenar:** em 16 UFs quem estava melhor em 2023 falha mais em 2024; em 7 UFs é o oposto

---

### 8.2 Interpretação de resultados por UF

| Cenário | Recomendação |
|---|---|
| Estado onde o modelo **vence** (PR, RJ, RS) | Use o modelo; ele protege contra errar a direção |
| Estado onde o modelo **empata** (17 UFs) | Use o modelo ou a regra simples — ganho é técnico, não visível |
| Estado onde o modelo **perde** (MG, RN, TO) | Use a regra simples em vez do modelo |

**O painel (`reports/painel_intra_uf.html`) já faz isso automaticamente** — cada estado declara qual abordagem funciona ali.

---

### 8.3 Predições out-of-fold, sempre

Se usar o modelo em produção:
- Nunca rank um município com o mesmo modelo que o treinou (vazamento de ranking)
- Sempre use predições out-of-fold geradas durante validação cruzada
- No arquivo `reports/ranking_intra_uf.json` as predições já estão out-of-fold — pronto para usar

---

### 8.4 O que NÃO fazer

| Ação | Por quê |
|---|---|
| Comparar um município do RS com um de MG no mesmo ranking | Réguas diferentes; iria gerar ranking inválido |
| Usar apenas a métrica AUC sem IC95% | Uma comparação pontual mascara a incerteza |
| Treinar um modelo nacional único | Colapsa em Leave-One-UF-Out (AUC 0,48) |
| Usar o modelo aluno-nível para decisão individual | Não supera o baseline; você estaria adicionando complexidade sem ganho |
| Ignorar a direção (priorize pior vs melhor) por UF | 7 UFs têm direção imprevisível; a regra nacional fixa erra |

---

## 9. Data and Model Provenance

| Item | Localização | Versão |
|---|---|---|
| README completo | `README.md` (11 seções) | Final |
| Notebook analítico | `notebooks/01_analise_completa.ipynb` (gerado por script, não à mão) | Reexecutável |
| Documento vivo | `docs/HANDOFF_RENAN.md` (16 capítulos, com sequência de erros e correções) | Até 2026-08-20 |
| Arquivos de Arquitetura | `docs/adr/` (5 ADRs, incluindo trade-offs de vazamento e régua) | Approved |
| EDA | `reports/eda_alunos.md` | Com 9 itens verificados |
| Dicionário | `reports/dicionario_alunos.md` | Pós-limpeza + conexão com objetivo |
| Dados de teste | `reports/ranking_intra_uf.{json,csv}` (5.216 municípios, out-of-fold) | Pronto para usar |
| Painel interativo | `reports/painel_intra_uf.html` (autocontido, particionado por UF) | Publicado |
| Código reproducível | `requirements.txt` (versões pinadas) + 4 scripts de CLI | Replicável |

---

## 10. Contact and Questions

- **Desenvolvedor:** Luiz Maibashi (AI Engineer, Pós-Tech FIAP)
- **Revisor de Arquitetura:** Renan Braga (Tech Lead, FIAP)
- **Repositório:** GitHub (em preparação — ticket #0004)
- **Última atualização:** 2026-08-20

Para dúvidas sobre uso do modelo em produção, consulte:
- `docs/HANDOFF_RENAN.md` Cap. 15 (decisões pendentes)
- `docs/adr/0005-modelo-intra-uf-e-invalidade-nacional.md` (justificativa da mudança)

---

## Appendix: Sequência de Decisões e Correções

Este Model Card descreve o resultado final. O caminho até aqui envolveu:

1. **Cap. 5–8 do HANDOFF:** vazamento identificado (5 colunas) → AUC caiu de 0,669 (falso) para 0,53
2. **Cap. 9:** descoberta que a base completa (57.782) estava em disco enquanto tudo rodava sobre amostra (5.000) → AUC subiu de 0,53 para 0,577
3. **Cap. 14:** integração de território público (população IBGE + meta do PDE) sem depender de GCP → AUC subiu de 0,507 para 0,6013, mas baseline (meta simples) saltou para 0,6331 e venceu
4. **Cap. 14.5:** detecção de que a própria régua do teste estava fraca → refeita contra baseline mais forte → veredito: FALHOU (−0,0318, IC95% [−0,0374, −0,0261])
5. **Cap. 8 (reformulação):** com modelo aluno reprovado, testado grão município → Leave-One-UF-Out colapsou em 0,48 (régua estadual)
6. **Cap. 8 (final):** modelo intra-UF funcionou (0,6478 vs 0,6209, +0,027) — seguro contra errar direção nas UFs imprevisíveis

**Não omitimos os erros — registramos a sequência.** O resultado negativo do aluno-nível é o que dá credibilidade ao positivo do municipal intra-UF.
