# Painel de Priorização Municipal de Alfabetização

> **[Abrir o painel ao vivo](https://luizmaibashi.github.io/painel-alfabetizacao-cgu/)**
>
> Ferramenta gratuita e de código aberto que cruza dados públicos federais
> (INEP e IBGE) para dizer a um gestor de educação, estado por estado, se um
> modelo estatístico consegue apontar quais municípios correm risco de furar
> a meta de alfabetização infantil no próximo ciclo. E, onde os dados não
> sustentam essa afirmação, dizer isso abertamente em vez de arriscar um
> palpite.

## Resumo em 30 segundos

- **O problema:** o Indicador Criança Alfabetizada (INEP) é público e sai
  todo ano por município, mas chega ao gestor como uma tabela crua de
  milhares de linhas. Ele não diz onde o histórico permite antecipar risco e
  onde não permite.
- **A ferramenta:** o painel transforma essa tabela em uma lista de
  prioridade por estado, com uma regra explícita de quando confiar no modelo
  e quando não confiar.
- **O teste:** o modelo foi congelado com dados até 2024 e usado para prever
  2025 de verdade, sem ver o resultado antes. Só depois comparamos com o que
  aconteceu, em 5.285 municípios de 23 estados.
- **O resultado:** o modelo aponta risco melhor que um método simples e
  gratuito em 14 estados. Em 1 (Ceará) o método simples ganha. Em 8 os dados
  não bastam, e o painel avisa isso na tela.

## Por que é reúso de dados abertos

Três fontes públicas federais, nenhuma com credencial paga ou acesso
restrito:

| Fonte pública | O que traz |
|---|---|
| [INEP, Resultados da Avaliação da Alfabetização](https://www.gov.br/inep/pt-br/areas-de-atuacao/avaliacao-e-exames-educacionais/avaliacao-da-alfabetizacao/resultados/2025) | Taxas municipais e metas do PDE, 2023 a 2026 |
| [IBGE, SIDRA (API pública)](https://sidra.ibge.gov.br/) | População municipal |
| [INEP, Censo Escolar 2023](https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/microdados/censo-escolar) | Infraestrutura escolar por município (testada como enriquecimento) |

O download da planilha de resultados é verificado por hash SHA-256,
registrado em [`reports/proveniencia_ica_2025.md`](reports/proveniencia_ica_2025.md).
Qualquer pessoa refaz o mesmo download e confirma que os dados que alimentam
o painel são os publicados pelo INEP.

**Relevância.** O painel serve à decisão concreta de uma secretaria de
educação: em qual município investir busca ativa e acompanhamento pedagógico
primeiro, com orçamento limitado. Ele evita dois erros comuns de uso de dado
público: comparar municípios de estados diferentes numa régua nacional
única, quando cada estado aplica sua própria prova; e apresentar um "score de
IA" onde o histórico não sustenta a afirmação.

**Benefício para a sociedade.** Apoio a uma política de primeira infância
(alfabetização até o 2º ano é meta nacional do PDE), sem custo de licença,
sem coleta de dado pessoal identificável, com o código de geração público sob
licença [MIT](LICENSE). Qualquer secretaria adapta o mesmo pipeline para o
próprio estado.

## O que este projeto entrega

| # | Entregável | Resultado |
|---|---|---|
| 1 | Painel de priorização municipal ([ao vivo](https://luizmaibashi.github.io/painel-alfabetizacao-cgu/)) | Testado contra o resultado real de 2025 em 5.285 municípios de 23 estados. O modelo acerta 65,3% das vezes contra 45,2% de um método simples de comparação (sortear ao acaso daria 50%). A decisão é por estado: modelo em 14, método simples em 1 (Ceará), abstenção em 8 |
| 2 | A descoberta de que não existe regra nacional única | "Quem estava melhor em 2023 falha mais a meta no ano seguinte" vale em 16 estados, e o oposto vale em 7. Por isso o painel é sempre por estado |
| 3 | Advertência de validade sobre comparação entre estados | Um ranking nacional compararia réguas de avaliação distintas. O painel é dividido por estado de propósito |
| 4 | Modelo por aluno (exigência da fase acadêmica de origem, mantido por transparência) | Testado com o mesmo rigor e reprovado no critério definido antes de testar: 60,5% de acerto contra 63,3% de aplicar a meta oficial a todos os alunos do município. Resultado negativo, medido e mantido no relatório |

Caso de reúso cadastrado no Portal Brasileiro de Dados Abertos:
`[link a preencher após homologação]`.

## Origem e licença

Este repositório é um recorte, com narrativa reorientada, do projeto
[Tech Challenge Fase 3](https://github.com/luizmaibashi/tech-challenge-fase3-alfabetizacao)
(Pós-Tech em Data Analytics, FIAP). O trabalho técnico é o mesmo. O que muda
aqui é o produto em destaque (o painel, não o modelo por aluno) e o público
(gestor público, não avaliador acadêmico). Enviado ao 2º Concurso de Reúso de
Dados Abertos da CGU.

---

## Como funciona, em linguagem simples

### Primeiro tentamos prever aluno por aluno, e não funcionou

O pedido original era prever, para cada aluno, se ele seria alfabetizado,
usando dados disponíveis antes da prova. Construímos esse modelo com cuidado,
removendo qualquer coluna que entregasse a resposta de graça (por exemplo,
uma coluna que só existe quando o aluno faltou à prova, o que já revela o
resultado). Testamos contra a régua mais simples possível: aplicar a meta
oficial daquele município a todos os alunos dele, igual, sem olhar nada
individual.

O modelo perdeu dessa régua. Não por pouco e não por azar: perdeu de forma
consistente, com três algoritmos diferentes, com folga estatística. A causa,
uma vez investigada, é simples: os dados disponíveis não descrevem o aluno,
descrevem o município dele. Depois de tirar tudo que era cola, o que sobra
sobre cada aluno é uma cópia do dado do município. Um número que já existe de
graça (a meta oficial) prevê isso tão bem quanto um modelo caro de treinar e
manter.

Para o gestor, isso é uma boa notícia: não é preciso pagar por
infraestrutura de IA para saber quais alunos priorizar. A meta oficial já
cumpre esse papel.

### O que funciona: priorizar município dentro do próprio estado

Com o aluno descartado, testamos a mesma pergunta um nível acima: dá para
prever quais municípios vão ficar abaixo da meta no próximo ano? Aqui havia
sinal real, mas só ao comparar municípios do mesmo estado. Cada estado aplica
sua própria prova, com sua própria dificuldade a cada ano. Comparar
municípios de estados diferentes na mesma régua seria como comparar notas de
provas diferentes como se fossem a mesma.

Para provar que o modelo funciona de verdade, nós o congelamos com dados até
2024 e o usamos para prever 2025 sem deixá-lo ver esse resultado. Só depois
comparamos com o que aconteceu. É o teste mais rigoroso disponível: prever o
futuro, não reencontrar um padrão já visto.

### Os números, traduzidos

| Pergunta | Resposta |
|---|---|
| Em quantos municípios o modelo foi testado de verdade? | 5.285, em 23 estados |
| Em quantos estados o modelo apontou risco melhor que o método simples? | 14 de 23 |
| Em quantos o método simples continua sendo a melhor escolha? | 1 (Ceará) |
| Em quantos os dados não bastam para afirmar nada com segurança? | 8, e o painel avisa isso na tela |
| Sorteando dois municípios (um que furou a meta, outro que não), qual a chance de o modelo apontar corretamente qual estava em mais risco? | 65,3%, contra 45,2% do método simples |
| E o modelo por aluno, que a fase acadêmica pedia? | Perdeu do método simples (60,5% contra 63,3%), mantido no relatório |

### Limitações, sem rodeio

- Não compara municípios de estados diferentes, de propósito. A variação de
  um ano para outro dentro do mesmo estado já chega a 20 pontos. Uma lista
  nacional seria enganosa.
- Não serve para decisão sobre um aluno específico. É priorização municipal,
  para orientar onde alocar apoio pedagógico e orçamento, nunca para rotular
  ou negar direito a uma criança.
- Só existe um teste no mundo real completo até agora (previsão de 2025
  conferida contra o resultado real). Cada novo ciclo aumenta a confiança ou
  revela se algo precisa mudar.
- Nos 8 estados sem sinal suficiente, o painel prefere dizer "não sabemos" a
  inventar resposta. É decisão de desenho: uma ferramenta pública que finge
  certeza é mais perigosa que uma que admite o limite.

### O que fazer com isso

1. Para priorizar alunos dentro de uma escola, use a meta oficial do PDE do
   município, aplicada a todos os alunos dele. É mais simples, mais barata e,
   pelos nossos testes, tão ou mais eficaz que um modelo de IA.
2. Para priorizar municípios dentro do seu estado, use o painel, mas só onde
   ele mostra "ranking do modelo" (14 estados). Onde mostra "método simples"
   (Ceará) ou "sem recomendação" (8 estados), siga o que o painel indica.

---

## Detalhamento técnico

A metodologia completa (tratamento de data leakage, teste de falsificação,
SHAP, backtest prospectivo, testes de placebo por permutação) e as decisões
registradas em ADR estão no repositório de origem:
**[tech-challenge-fase3-alfabetizacao](https://github.com/luizmaibashi/tech-challenge-fase3-alfabetizacao)**.

Em uma página:

- **Por que o modelo de aluno perde.** Os dados são amostrais e as chaves de
  aluno e escola são sintéticas, sem correspondência com fontes externas.
  Todo enriquecimento possível (IBGE, Censo Escolar, FUNDEB, IDHM) é
  constante dentro do município e não distingue dois alunos do mesmo
  município. SHAP: features de município somam 81,3% da influência.
- **Por que o modelo municipal só vale dentro do estado.** As avaliações são
  aplicadas pelos estados. Um Leave-One-UF-Out, com a UF de teste nunca vista
  no treino, derruba o AUC para 0,48 (abaixo do acaso). A variação estadual
  entre anos chega a 20 pontos, e isso é mudança de régua, não aprendizado.
- **De onde vem a vantagem do modelo.** Contra o baseline honesto (regra
  trivial com a direção prevista a partir das outras UFs), o modelo ganha
  +0,027 de AUC, IC95% [+0,007, +0,048]. A vantagem inteira vem das 7 UFs
  onde a direção não é previsível de fora. É um seguro contra errar a
  direção, não um ranqueador superior.
- **Enriquecimentos externos.** IDHM, FUNDEB e infraestrutura do Censo
  Escolar foram testados e nenhum entrou em produção. Um teste de placebo por
  permutação mostrou que os "flips de veredito" antes usados como critério de
  sucesso são reproduzidos por ruído puro. A nota retroativa está no ADR
  correspondente, não corrigida em silêncio.

## Reprodutibilidade

```bash
pip install -r requirements.txt
python src/evaluation/05_backtest_prospectivo_2025.py   # baixa a planilha do INEP, verifica SHA-256, gera o ranking de 2025
python src/visualization/01_gerar_painel_intra_uf.py    # gera reports/painel_intra_uf.html
```

O painel publicado em GitHub Pages é a saída de `01_gerar_painel_intra_uf.py`.
O backtest foi rodado do zero em 2026-08-31 e os artefatos canônicos saíram
idênticos bit a bit aos versionados.
