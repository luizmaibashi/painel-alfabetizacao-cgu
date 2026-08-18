# Feedback oficial da Fase 2 e o que ele muda na Fase 3

> **Pra que serve este documento:** o avaliador da Fase 2 devolveu um feedback
> detalhado. Ele não é só "nota do passado" — três das críticas descrevem
> padrões de falha que a Fase 3 pode repetir se a gente não corrigir de
> propósito. Este arquivo registra o feedback na íntegra e traduz cada ponto
> em ação concreta pra esta fase.
>
> **Renan:** se você só tem 5 minutos, leia a Seção 3 (o padrão que se repete)
> e a Seção 4 (o que mudei por causa disso). O resto é contexto.

**Data do feedback:** recebido antes de 2026-08-18 (data exata não registrada).
**Repo avaliado:** https://github.com/alfabetizacao-datateam/tech-challenge-fase2-alfabetizacao

---

## 1. Pontos fortes reconhecidos pelo avaliador

Vale registrar porque **define o padrão de qualidade que a Fase 3 precisa manter** —
não são elogios decorativos, são o piso a partir do qual seremos avaliados de novo:

- O tratamento da **imputação de metas** (KNN, ADR-004).
- **Quinze ADRs** documentando decisões.
- **Nulos estruturais preservados** com o racional explícito.
- **Validação cruzada contra o dado publicado pelo INEP.**
- Terraform modularizado.
- **114 testes** cobrindo o caminho inteiro.
- `safe_build` isolando cada mart.
- O dashboard tem **arco narrativo**.

## 2. Feedback construtivo (íntegra, agrupado por tema)

### 2.1 O streaming não alimenta nada

> "O consumer grava em `datalake/bronze/streaming_eventos`, e nenhum script do
> projeto lê esse caminho. Nem `02_silver_transform.py`, nem
> `dataproc_02_silver.py`, nem a Gold.
>
> A implementação em si está boa: schema explícito, `checkpointLocation`,
> `trigger(processingTime="10 seconds")` e `cleanSource=archive` com
> `sourceArchiveDir`, que é um detalhe que quase ninguém configura e que evita
> reprocessamento e acúmulo na landing zone. O ADR-006 justifica bem a escolha
> de File Stream sobre Kafka para esta fase.
>
> **O problema é que o evento chega, é validado, é persistido, e para ali.**
> Como a arquitetura híbrida é o eixo do desafio, o ponto onde batch e streaming
> convergem é justamente o que precisa existir. Vocês já têm a OBT da Silver com
> chave de junção padronizada; bastaria a Silver ler também o caminho de
> streaming, unir com marcação de origem e deduplicar por município, ano e rede."

### 2.2 Inconsistências entre páginas do dashboard

> "**Página 1 contra página 5.** A página 1 informa taxa média nacional de 59,86%
> e 4.679 municípios abaixo de 80%. A página 5 traz o scatter 'taxa × déficit'
> com eixo x indo de 78 a 100 e mediana em torno de 85. Se a maioria dos
> municípios está abaixo de 80%, a nuvem deveria estar concentrada à esquerda de
> 80, não entre 78 e 100. Ou o gráfico está filtrado para um subconjunto, ou usa
> métrica diferente. Em qualquer dos casos, precisa estar rotulado.
>
> **Página 6.** O `custo_estimado` dos primeiros municípios fica entre R$ 969 e
> R$ 1.190, e o `beneficio_alunos_ate_80` é 1 para todos eles. Com orçamento de
> R$ 500 milhões cobrindo 2.334 municípios, a ordem de grandeza não fecha: se o
> custo médio fosse mil reais, 2.334 municípios custariam cerca de R$ 2,3
> milhões. Provavelmente o valor está em milhares, ou o greedy pega municípios
> muito mais caros adiante. De todo modo, **a unidade precisa aparecer no
> cabeçalho da coluna**, porque hoje um leitor conclui que se alfabetiza um
> município por mil reais."

### 2.3 Falta a estimativa de custo da própria arquitetura

> "A seção de FinOps é boa em mecanismo: cluster efêmero com TTL,
> dimensionamento, região barata, disco padrão, particionamento, cache de API, e
> até a declaração honesta do gap de lifecycle no GCS. **Mas o enunciado pede
> especificamente estimativa de custo da arquitetura, e ela não existe.**"

### 2.4 Monitoramento tem isolamento de falha, mas não observabilidade

> "O `safe_build` garante que uma falha não derruba o job e que o traceback fica
> no log do Dataproc. Isso é resiliência, e é bem feito. **Mas o enunciado pede
> quatro coisas: falhas de ingestão, latência, volume processado e alertas.**"

### 2.5 Não há agendamento

> "O pipeline roda por invocação manual dos scripts ou por `terraform apply`
> mais submissão de job. Não há Cloud Scheduler, Cloud Composer ou workflow do
> Dataproc encadeando as etapas com dependência declarada."

---

## 3. O padrão que se repete (a parte que importa pra Fase 3)

Lendo as 5 críticas juntas, **três delas são o mesmo erro em roupas diferentes**:

| Crítica | O que foi construído | O que faltou |
|---|---|---|
| Streaming | Consumer bem implementado, com detalhes que "quase ninguém configura" | **Ninguém lê o que ele grava** |
| FinOps | Mecanismos de economia bem pensados | **A estimativa de custo pedida não existe** |
| Monitoramento | `safe_build` resiliente e bem feito | **3 dos 4 itens pedidos não existem** |

O padrão: **a peça foi construída com qualidade técnica alta, mas não foi
conectada ao consumo — ou não foi cruzada contra o que o enunciado literalmente
pediu.** O avaliador elogiou a execução e cobrou a ligação.

Traduzindo pro nosso vocabulário: *não basta a peça funcionar isolada; ela
precisa estar plugada e precisa existir porque alguém pediu, item por item.*

### 3.1 Onde esse mesmo padrão JÁ estava acontecendo na Fase 3

Ao revisar o `src/preprocessing/02_extrair_snapshot.py` em 2026-08-18, achei o
caso idêntico:

- A Fase 2 construiu a **imputação KNN de metas** — foi o **primeiro ponto forte
  listado** pelo avaliador. Cobertura 43,6% → 100%, holdout validado
  (MAE 5,12pp / RMSE 7,26pp), em produção desde 2026-07-08, gravando em
  `silver/alfabetizacao_municipios_obt_com_metas_imputadas`.
- O enunciado da **Fase 3** pede explicitamente "metas estaduais e municipais"
  entre as variáveis da base analítica.
- **O script de extração da Fase 3 não lia essa tabela.** Lia a OBT base
  (`alfabetizacao_municipios_obt`, 6 colunas), sem nenhuma meta.

Ou seja: construído, validado, elogiado — **e não conectado**. Exatamente a
crítica do streaming, repetida numa fase nova. Corrigido nesta sessão (ver
Seção 4.1).

---

## 4. O que mudou na Fase 3 por causa deste feedback

### 4.1 Extração passa a incluir a meta imputada — CORRIGIDO

`02_extrair_snapshot.py` agora aponta pra
`silver/alfabetizacao_municipios_obt_com_metas_imputadas` e traz
`meta_alfabetizacao_2024_imputada` como feature.

**Por que isso NÃO é leakage** (importante, Renan — checar se você concorda):
a meta é definida **externamente** pelo PDE (política pública), não deriva do
desempenho do aluno sendo predito. É estrutural, mesmo raciocínio que já
validou `populacao_total` e `gasto_por_habitante_educacao` como seguros no
ADR-0001. **Diferente** de `gap_meta` e `taxa_alfabetizacao`, que continuam
excluídos — esses são calculados *a partir* do desempenho do próprio ano e são
circulares.

⚠️ **Ressalva honesta:** parte das metas é imputada por KNN (não é dado
oficial pra todas as redes). O flag de imputação precisa acompanhar a feature,
mesma disciplina que a Fase 2 aplicou com `is_imputado`. Ver Seção 4.3.

### 4.2 Auditoria linha a linha do enunciado — obrigatória antes de fechar

Duas das cinco críticas foram "o enunciado pede X e X não existe". A defesa
contra isso não é lembrar melhor — é **cruzar cada linha do PDF contra o
implementado, por escrito**. Ver `docs/AUDITORIA_ENUNCIADO_FASE3.md`.

### 4.3 Rotular unidade e origem de todo número exibido

A crítica do dashboard (R$ 969 lidos como "alfabetiza um município por mil
reais") é sobre **rótulo ausente**, não sobre cálculo errado. Vale pro nosso
relatório e vídeo executivo da Fase 3:
- Toda métrica exibida diz a unidade e a base (`n`).
- Toda feature imputada é marcada como imputada onde aparece.
- Todo gráfico filtrado diz que está filtrado, e por quê.

*(Isso conversa direto com a regra da nossa base: "nunca reportar proporção sem
`n` e sem intervalo".)*

### 4.4 Não replicar as críticas que não se aplicam

Honestidade sobre escopo: **agendamento** (2.5) e **observabilidade de
pipeline** (2.4) eram exigências da Fase 2 (engenharia de dados em produção).
O enunciado da Fase 3 **não pede** nenhum dos dois — pede pipeline sklearn
reprodutível, interpretabilidade e resposta a perguntas de negócio. Não vamos
construir Cloud Composer aqui por trauma da fase anterior; isso seria
overengineering.

**Mas** a lição transferível é: se o enunciado da Fase 3 pedir algo análogo
(ex.: "validação garantindo replicabilidade e generalização"), isso precisa
existir de forma verificável, não presumida. É o que a auditoria da Seção 4.2
checa.

---

## 5. Perguntas pro Renan sobre este feedback

1. **Concorda que `meta_alfabetizacao_2024_imputada` não é leakage?** É a
   decisão mais consequente desta sessão e quero seu contraponto antes de
   virar definitivo.
2. **Vale mencionar as correções da Fase 2 no README da Fase 3?** (Ex.: "o
   scatter da página 5 estava filtrado, agora rotulado"). Minha inclinação é
   que sim, demonstra maturidade — mas é decisão de dupla.
3. **Você tem o registro da nota numérica?** Só o texto do feedback foi
   preservado aqui; se a nota tiver detalhamento por critério, ajuda a calibrar
   onde investir esforço nesta fase.
