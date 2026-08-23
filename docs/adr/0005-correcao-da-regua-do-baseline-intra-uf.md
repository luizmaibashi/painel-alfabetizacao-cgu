# ADR-0005: Correção da régua do baseline intra-UF e a inversão de direção entre estados

**Data**: 2026-08-20
**Status**: Accepted (correção de erro medido; números reproduzidos por duas
implementações independentes e estáveis em 5 sementes)
**Proposto por**: Luiz Maibashi
**Contexto**: Auditoria do entregável nº 2 (ranking intra-UF), na mesma sessão
que produziu o ADR-0004. **Supersede a manchete do ADR-0004**, não a decisão
dele: piso de 40 municípios/UF e dobras adaptativas seguem válidos; o que cai
é o número "vence em 18 de 23 UFs" que aquele ADR reportou.

---

## 🤔 1. CONTEXTO (O QUÊ?)

Desde o commit `c7c89bc`, `04_ranking_intra_uf.py` comparava o modelo contra
um único baseline:

```python
score_intuicao = -g.taxa23.values   # "priorize quem estava pior"
```

AUC ponderado **0,4032**. O README, o HANDOFF (Cap. 16.6), o painel, o
notebook, o dossiê e o próprio ADR-0004 leram esse número como *"a intuição
corrente é ativamente errada, abaixo do acaso"* e reportaram que o modelo
(0,6478) vencia por **+0,245**, em **18 de 23 UFs**.

**O sinal não é um bug** — ele codifica corretamente a intuição declarada. O
erro é de método: **AUC é antissimétrica**, `AUC(-s) = 1 - AUC(s)`. Reportar
que uma regra vale 0,4032 é reportar que a **mesma regra, lida ao contrário,
vale 0,5968** — de graça. Um baseline "abaixo do acaso" não é fraco; é forte
e está apontado para trás.

Isso é literalmente o mesmo erro que o projeto já pegou e corrigiu uma vez, no
modelo aluno-nível (Cap. 4.6 do dossiê, "A vitória boa demais para ser
verdade"): comparar contra um baseline mais fraco que o melhor disponível. O
princípio está escrito no `ADR-0001 §5`. Não foi aplicado ao entregável que
sobreviveu.

**Restrição de método:** um baseline precisa ser especificável **sem** ver o
resultado. As duas direções fixas são; escolher a direção por UF olhando 2024
não é — isso é oráculo.

---

## ⚙️ 2. DECISÃO (POR QUÊ?)

**O que escolhemos:** substituir o baseline único por três níveis, todos
gravados em `reports/ranking_intra_uf.json`:

1. **As duas direções fixas** (`auc_dir_pior`, `auc_dir_melhor`) — nenhuma é
   escondida, porque uma é o complemento da outra.
2. **Baseline honesto** (`auc_baseline_honesto`): a regra trivial sobre
   `taxa23` com a **direção prevista para cada UF a partir das outras**
   (leave-one-UF-out sobre `folga_media` = média de `taxa23 - meta2024`,
   calculável só com dado pré-2024). É o melhor baseline que um gestor
   consegue montar sem conhecer o resultado do próprio estado.
3. **IC95% bootstrap pareado** da diferença modelo − baseline honesto, por UF
   (`ganho_ic95`), com veredito de **três** estados (`veredito`):
   `modelo_vence` / `inconclusivo` / `modelo_perde`.

**Razão principal (ROI statement):**
"Se não corrigíssemos: o entregável principal do projeto seguiria vendendo
uma vantagem de +0,245 que some para +0,027 sob qualquer conferência — e a
conferência custa cinco minutos a quem conhece AUC. Numa entrega cujo valor
declarado é rigor metodológico, ser pego nisso custa mais que o próprio
resultado negativo."

---

## 📊 3. CONSEQUÊNCIAS

### O que muda nos números

| | antes (régua inválida) | depois (régua honesta) |
|---|---|---|
| Baseline | 0,4032 | **0,6209** |
| Modelo | 0,6478 | 0,6478 |
| Diferença | +0,245 | **+0,027** — IC95% [+0,007, +0,048] |
| UFs em que vence | 18 / 23 | **3 / 23** (PR, RJ, RS) |
| UFs em que perde | 5 / 23 | **3 / 23** (MG, RN, TO) |
| UFs empatadas | — | **17 / 23** |

### O achado que cresce (e vale mais que o modelo)

**A direção da relação inverte entre estados.** "Quem estava melhor em 2023
falha mais a meta de 2024" vale em **16 UFs**; o oposto vale em **7**
(AL, AM, CE, ES, PE, PR, RJ). A média nacional de 0,4032 era esses dois grupos
se cancelando — não um erro sistemático único. Dois mecanismos medidos:

- **MG** (meta acompanha o município) — regressão à média: o pior quartil
  subiu **+23,9pp** e passou; o melhor caiu **−2,4pp** e perdeu a meta que
  superava por só 3,6pp. ⇒ "melhor primeiro" funciona.
- **CE** (meta satura em 80,0 para **82%** dos municípios) — os melhores já
  estavam **+19,1pp acima** da meta e não têm como falhar; só quem está na
  linha (−0,2pp) corre risco. ⇒ "pior primeiro" funciona.

É a **terceira manifestação do efeito de régua estadual**, depois do colapso
Leave-One-UF-Out (Cap. 16.3) e da advertência sobre os marts da Fase 2 — e a
primeira que dá o *mecanismo*, não só o sintoma.

### O valor real do modelo, redefinido

Não é ranquear melhor. É **não precisar saber a direção de antemão**:

| | regra trivial | modelo | diferença |
|---|---|---|---|
| 16 UFs com direção previsível | 0,6736 | 0,6638 | −0,010 (**IC cruza zero: empate**) |
| 7 UFs com direção imprevisível | 0,4378 | 0,5922 | **+0,155** — IC95% [+0,082, +0,226] |

Toda a vantagem está, com significância, nas 7 UFs em que a direção não é
previsível de fora. O modelo funciona como **seguro contra errar a direção**.
Essa é a única afirmação de valor que sobrevive aos testes.

**Negativas (custo/risco):**
- A manchete do entregável nº 2 encolhe de "+0,245, vence em 18/23" para
  "+0,027, vence em 3/23" — e precisa ser reescrita em 6 artefatos.
- O modelo perde com significância em 3 UFs; o painel agora **recomenda a
  regra simples** nesses estados, o que é o comportamento correto mas reduz o
  escopo de uso da ferramenta.

---

## 🎯 4. ALTERNATIVAS DESCARTADAS

| Opção | Vantagem | Por quê rejeitada |
|-------|----------|------------------|
| Manter a régua e sinalizar como limitação | Zero retrabalho; preserva a manchete | ❌ É exatamente o que o projeto critica nos outros. Um leitor que conheça AUC derruba em 5 minutos |
| Trocar só pela direção invertida fixa (`+taxa23`, 0,5968) | Simples, um número só | ❌ Injusto ao contrário: em CE "melhor primeiro" vale 0,0718, e comparar contra isso infla o modelo |
| Usar a melhor das duas direções por UF (oráculo, 0,6487) | A barra mais dura possível | ❌ Usa o resultado de 2024 para escolher a direção — informação que ninguém tem ao decidir. Serve como referência (o modelo empata: −0,0008), não como baseline |
| Escolher a regra por LOO numa família maior (`±taxa23`, `±meta`, `±gap`) | Baseline mais expressivo | ❌ Testado: cai sempre em `+meta` e dá 0,6064, **pior** que o preditor de direção (0,6209). Mantido o mais forte |

---

## 💰 5. IMPACTO ROI & VALIDAÇÃO

**Seis checagens executadas antes de aceitar a conclusão:**

| Checagem | Resultado |
|---|---|
| Outras regras triviais óbvias (gap até a meta, meta sozinha, população) | modelo bate todas (melhor delas: `meta` 0,6064) |
| Baseline com direito de escolher a regra por LOO | 0,6064 — pior que o preditor de direção |
| **LOO aninhado** (seleção de feature dentro do fold, elimina vazamento de seleção) | **idêntico: +0,0270** — e escolhe, nesta rodada específica de análise exploratória (não uma feature persistida no pipeline), a taxa de 2023 (14×) e a folga até o teto (8×), não a feature que eu havia escolhido a olho |
| Integridade do out-of-fold | **zero folds pulados**; os 102 scores 0,0 do CE são predições confiantes corretas, não bug |
| Estabilidade (5 sementes) | +0,0267 a +0,0278; todos os IC inteiramente positivos |
| Significância por grupo | 7 UFs: +0,155 [+0,082, +0,226] · 16 UFs: −0,010, **inconclusivo** |

**Cenários de regressão (quando falha):**
- `folga_media` prevê a direção em 16/23. Se a fonte mudar a fórmula da meta
  (ex.: tirar o teto de 80,0), o preditor de direção precisa ser refeito — o
  mecanismo do CE deixa de existir.
- Com n=23 estados, o preditor de direção é uma regressão sobre 22 pontos.
  Qualquer UF nova entra como teste real, não como confirmação.

---

## 🔗 6. REFERÊNCIAS & LINKS

- `ADR-0004` — piso de 40 e dobras adaptativas **seguem válidos**; só a
  manchete de desempenho daquele ADR é superseded por este.
- `ADR-0001 §5` — o princípio de comparar contra o melhor baseline trivial,
  que este ADR restaura.
- Dossiê §4.6 ("A vitória boa demais para ser verdade") — o precedente do
  mesmo erro, pego e corrigido no modelo aluno-nível.
- `src/modeling/04_ranking_intra_uf.py` — `prever_direcao_loo()`,
  `comparar_pareado()`.

---

## ✅ CRITÉRIA DE ACEITAÇÃO

- [x] Trade-offs documentados com justificativa (Seção 3).
- [x] Alternativas rejeitadas com motivo técnico e **medido** (Seção 4).
- [x] Impacto quantificado (+0,245 → +0,027; 18/23 → 3/23).
- [x] Métricas de sucesso definidas e testáveis (Seção 5).
- [x] Plano de checagem descrito e **executado** — 6 validações independentes.
- [x] Riscos/edge cases identificados (mudança da fórmula da meta; n=23).
