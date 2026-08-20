# ADR-0004: Validação adaptativa e piso de amostra no ranking intra-UF

**Data**: 2026-08-20
**Status**: Accepted (decisão técnica com resultado verificado — script rodado, números conferidos, painel republicado)
**Proposto por**: Luiz Maibashi
**Contexto**: Sessão de continuação da frente `pos_tech`, após a pergunta do
usuário "não existe a possibilidade de adicionarmos os estados faltantes?"
sobre o painel de priorização (`reports/painel_intra_uf.html`).

---

## 🤔 1. CONTEXTO (O QUÊ?)

O ranking intra-UF (`src/modeling/04_ranking_intra_uf.py`, produtizado no
commit `c7c89bc`) cobria só **17 dos 27 UFs**. O script usava um piso fixo
`MIN_MUNICIPIOS_POR_UF = 100` e `StratifiedKFold(5)` fixo para todo estado —
abaixo de 100 municípios, o k-fold de 5 dobras não era confiável (dobra
pequena demais, risco de sobrar uma classe só no treino).

Ao ser perguntado se dava para incluir os 10 UFs de fora, a investigação
achou **dois grupos com causas diferentes**, que este ADR trata de forma
diferente:

**Grupo 1 — dado completo, só abaixo do piso (7 UFs):**
AP (16 municípios), AM (48), RO (52), SE (75), ES (78), MS (79), RJ (90).
Todos com `taxa23`, `taxa24` e `meta_alfabetizacao_2024` presentes e válidos.

**Grupo 2 — dado ausente na fonte, não é limite de modelo (3 UFs):**
AC, DF e RR. Confirmado até o nível estadual no arquivo fonte
(`br_inep_avaliacao_alfabetizacao_meta_alfabetizacao_uf.csv.gz`, Base dos
Dados/INEP):
- **AC**: `taxa_alfabetizacao` nula em 2023 (nos dois níveis, UF e
  município) e `meta_alfabetizacao_2024` nula nos dois anos. Só existe taxa
  2024.
- **DF**: mesmo padrão do AC — nulo em 2023, meta nula nos dois anos. Some
  ainda tem uma causa estrutural adicional: DF não é dividido em municípios
  (Brasília/GDF administra como unidade única), então a rede "Municipal" do
  indicador — que é o recorte usado neste projeto — não se aplica a ele por
  definição, independente de qualquer dado faltando.
- **RR**: `taxa_alfabetizacao` nula em **ambos** os anos, em qualquer rede.
  Nenhum registro de nível município para RR em nenhum dos dois arquivos
  fonte checados.

Não é bug de mapeamento de UF (o prefixo IBGE de cada uma das 3 está
corretamente cadastrado em `UF_POR_PREFIXO`, só não existe linha nenhuma —
ou só existe com o dado em branco — para esses códigos no arquivo fonte).

**Restrições técnicas:**
- `StratifiedKFold` exige `n_splits <= min(contagem de cada classe)`.
- AUC calculado em amostra pequena tem variância alta e vinha sendo
  reportado como ponto único, sem intervalo — escondendo essa incerteza.

**Métricas atuais (baseline, piso=100, 5-fold fixo):**
- 17 UFs, 4.794 municípios, AUC ponderado 0,6496 vs intuição 0,4015,
  modelo vence em 14/17 UFs.

---

## ⚙️ 2. DECISÃO (POR QUÊ?)

**O que escolhemos:**

1. **Piso absoluto abaixado de 100 para 40 municípios por UF.** Exclui só o
   AP (16 municípios no estado inteiro). Abaixo de ~40, nem dobra reduzida
   nem intervalo de confiança tornam o AUC informativo — e com tão poucos
   municípios o gestor não precisa de um modelo, consegue olhar a lista
   inteira.
2. **Dobras adaptativas** em vez de 5-fold fixo:
   `n_folds = max(2, min(5, len(g) // 20, classe_minoritaria))`. Estado
   grande mantém 5 dobras (piso antigo, inalterado); estado pequeno reduz
   proporcionalmente, sem deixar dobra sem as duas classes.
3. **IC95% por bootstrap (1.000 reamostragens) reportado para TODO estado**,
   não só os pequenos — ao lado do AUC pontual, tanto do modelo quanto da
   intuição. O painel (`01_gerar_painel_intra_uf.py`) passou a desenhar esse
   intervalo como uma barra visual (whisker) na régua de comparação, e a
   avisar explicitamente quando o estado é "amostra pequena" (n < 100).
4. **Grupo 2 (AC, DF, RR) documentado como limite de fonte, não atacado.**
   Nenhuma engenharia resolve dado que não existe no INEP. Registrado no
   painel (bloco "Como este modelo foi construído") e neste ADR.

**Razão principal (ROI statement):**
"Se NÃO fizéssemos: o painel continuaria calado sobre por que 10 estados
não aparecem — um gestor do RJ ou do ES abriria o painel e não entenderia
a ausência, sem custo de implementação nenhum evitado (a informação já
existia, só não estava exposta nem calculada)."
"Se fizéssemos sem o IC: incluiríamos 7 estados novos escondendo que 2
deles (AM, ES) têm resultado estatisticamente inconclusivo — pareceria mais
cobertura sem ser mais rigor, o oposto do que este projeto vem fazendo
desde a Fase 3."

---

## 📊 3. CONSEQUÊNCIAS

**Positivas (Wins):**
- Cobertura de 17 → 23 UFs, 4.794 → 5.216 municípios (+422).
- Toda UF agora reporta incerteza (IC95%), não só um ponto — o painel deixa
  de sugerir uma confiança que o dado não sustenta.
- Achado honesto preservado: 2 dos 6 estados recém-incluídos (AM, ES) o
  modelo **não** supera a intuição — é reportado como tal, não escondido.
- Grupo 2 (AC/DF/RR) sai de "silêncio" para "limite documentado e
  investigado", reduzindo a chance de alguém tentar "consertar" isso depois
  sem saber que já foi investigado.

**Negativas (Custo/Risco):**
- AUC ponderado geral caiu ligeiramente (0,6496 → 0,6478) e a taxa de vitória
  caiu proporcionalmente (14/17=82% → 18/23=78%) — é o preço esperado de
  incluir estados mais ruidosos, não uma regressão do modelo em si.
- Estados com 2 dobras (RO, AM) têm out-of-fold menos robusto que os de 5
  dobras — mitigado pelo IC exposto, não eliminado.
- `bootstrap_ic_auc` com 1.000 reamostragens × 23 UFs aumenta o tempo de
  execução do script (segundos, não minutos — não é bloqueio).

**Timeline:**
- Implementação: ~1h nesta sessão (código + regeneração + republicação do
  artifact).
- Validação: imediata — números conferidos rodando o script antes e depois.

---

## 🎯 4. ALTERNATIVAS DESCARTADAS

| Opção | Vantagem | Por quê rejeitada |
|-------|----------|------------------|
| Manter piso 100 fixo | Simplicidade, nenhum código novo | ❌ Deixa 7 estados com dado bom de fora sem necessidade — cobertura menor que o dado permite |
| Baixar piso pra incluir também o AP (16) | Cobertura total dos 24 UFs com dado | ❌ Com 16 municípios o AUC não é informativo em nenhum esquema de validação razoável (variância domina o sinal); e o caso de uso (gestor olha a lista) não precisa de modelo nesse tamanho |
| Forçar modelo em AC/DF/RR com imputação de meta/taxa | "Resolve" os 27 UFs | ❌ Inventaria o alvo (`y`) a partir de dado que não existe — pior que não ter ranking nenhum, porque pareceria real |
| Pool de estados pequenos numa "região" para ganhar N | Mais dado por modelo | ❌ Reintroduz exatamente o erro que o pivô pro grão município corrigiu: misturar réguas de avaliação diferentes |

---

## 💰 5. IMPACTO ROI & VALIDAÇÃO

**Métrica de sucesso (como sabemos que funcionou):**
- UFs cobertas: 17 → 23 (confirmado, saída do script).
- Todo UF com IC95% no JSON e visível no painel: confirmado
  (`auc_ic`, `auc_intuicao_ic` em `reports/ranking_intra_uf.json`).
- Painel republicado e conferido: bloco de metodologia lista o piso de 40 e
  os 3 UFs de fonte ausente.

**Cenários de regressão (quando falha):**
- Se a fonte (`br_inep_avaliacao_alfabetizacao_meta_alfabetizacao_municipio.csv.gz`)
  for atualizada e passar a ter AC/DF/RR, este ADR fica desatualizado —
  revisar o Grupo 2 nessa hipótese.
- Se o Renan discordar do piso de 40 ou da fórmula de dobras adaptativas na
  call de alinhamento, ambos são um parâmetro (`MIN_MUNICIPIOS_POR_UF`,
  fórmula em `treinar_por_uf`), não uma decisão espalhada pelo código.

---

## 🔗 6. REFERÊNCIAS & LINKS

**Relacionados:**
- `ADR-0001` (pipeline sklearn, política de leakage) — não alterado.
- `ADR-0002` (modelo aluno-nível, superseded pelo pivô município) e
  `ADR-0003` (Gold vs Silver) — nenhum cobria o ranking intra-UF; este ADR
  preenche essa lacuna.
- `docs/HANDOFF_RENAN.md`, Cap. 16.6 — números da tabela atualizados junto
  com este ADR.
- `src/modeling/04_ranking_intra_uf.py` — `MIN_MUNICIPIOS_POR_UF`,
  `bootstrap_ic_auc`, `treinar_por_uf`.
- `src/visualization/01_gerar_painel_intra_uf.py` — item "Piso de 40
  municípios" e "3 estados de fora" no bloco de metodologia do painel.

**Commits relevantes:**
- `c7c89bc` — produtização original do ranking intra-UF (piso 100, 5-fold
  fixo), que este ADR revisa.

---

## ✅ CRITÉRIA DE ACEITAÇÃO

- [x] Trade-offs documentados com justificativa (Seção 3).
- [x] Alternativas rejeitadas com motivo técnico (Seção 4).
- [x] Impacto quantificado (17→23 UFs, 4.794→5.216 municípios, AUC
      0,6496→0,6478, 14/17→18/23).
- [x] Métricas de sucesso definidas e testáveis (Seção 5).
- [x] Plano de checagem descrito (rodar o script, conferir JSON e painel).
- [x] Riscos/edge cases identificados (fonte atualizada, piso questionado
      pelo Renan).
