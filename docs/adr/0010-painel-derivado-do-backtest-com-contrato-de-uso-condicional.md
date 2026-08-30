# ADR-0010 — O painel operacional é derivado do backtest prospectivo, com contrato de uso condicional embutido no artefato

**Data:** 2026-08-30
**Status:** Aceito
**Contexto:** próxima etapa após o backtest prospectivo de 2025 (ticket 0018) —
converter a evidência prospectiva em um artefato utilizável.
**Relaciona-se com:** ADR-0002 §2.2 (superada), ADR-0004 (validação adaptativa),
ADR-0005 (régua do baseline), `reports/decisao_produto_pos_backtest_2025.md`.

---

## 1. O que motivou

O painel (`reports/painel_intra_uf.html`) era gerado de
`reports/ranking_intra_uf.json` — um retrato **histórico de 2024** com predições
out-of-fold. Após o backtest prospectivo (ticket 0018), esse painel passou a
mentir por omissão: mostrava um ranking do modelo em todas as 23 UFs, quando a
evidência prospectiva diz que o modelo só vence a regra simples em 14, perde no
CE e é inconclusivo em 8. Apresentá-lo como ferramenta operacional convidava
exatamente o erro que o projeto passou meses medindo.

`reports/decisao_produto_pos_backtest_2025.md` já fixava a decisão de negócio
(uso condicional por UF). Faltava o **onde**: em prosa de Markdown, num JSON, ou
na própria interface.

## 2. Decisão

**O contrato de uso condicional vive no artefato de dados, não na prosa nem na
interface.**

1. `src/evaluation/05_backtest_prospectivo_2025.py` passa a gravar uma segunda
   saída, `reports/ranking_prospectivo_2025.json`, com as listas municipais de
   2025 (rank, nome, taxa 2024, meta 2025, taxa 2025, resultado real), o campo
   `uso` por UF (`ranking_modelo` | `regra_simples` | `abster`) derivado
   **mecanicamente** do veredito do backtest, e a rastreabilidade da fonte
   (arquivo, SHA-256, URL, data de publicação do Inep, data de corte do treino).
2. A ordenação exposta segue o `uso`: pelo score do modelo onde ele venceu;
   pela taxa de 2024 na direção que já funcionava naquela UF em 2024 onde ele
   perdeu; pelo score do modelo apenas como diagnóstico (sem recomendar ação)
   onde é inconclusivo.
3. `src/visualization/01_gerar_painel_intra_uf.py` passa a consumir **só** esse
   JSON. Onde o `uso` é `abster`, o cabeçalho da tabela e o texto de veredito
   dizem explicitamente que não há recomendação de ordem.
4. O payload não tem eixo nacional — comparação entre UFs continua impossível
   por construção, não por aviso no rodapé (mantém ADR-0004).

## 3. Alternativas rejeitadas

| Opção | Por quê rejeitada |
|---|---|
| Manter o painel lendo `ranking_intra_uf.json` e escrever o contrato só no rodapé | O rodapé não impede o gestor de tratar o ranking do CE como recomendação. A restrição precisa estar na ordenação e no texto de cada UF, não num parágrafo que ninguém lê. |
| Colar as listas históricas de 2024 (do `ranking_intra_uf.json`) com os vereditos de 2025 (do backtest) | Junta dado de dois ciclos: as listas seriam de 2024 e o veredito de 2025. O backtest já pontua 2025 município a município — usar essa saída é o dado coerente. |
| Derivar o `uso` na camada do painel (JS) a partir do JSON de métricas | O mapeamento veredito→uso é decisão de produto e precisa ser testável em Python, versionada no JSON, não escondida em template string. |
| Recriar o score prospectivo num script novo de visualização | Duplicaria a lógica de modelagem fora de `src/evaluation/` — training-serving skew auto-infligido (o erro do ADR-0008). O backtest é a fonte única do score. |

## 4. Consequências

**Positivas:**
- O painel deixa de ser "demonstração histórica que precisa ser regenerada" e
  passa a ser o retrato operacional do ciclo 2025, auditável até o SHA-256 da
  planilha.
- Abstenção vira comportamento visível: 8 UFs mostram só diagnóstico.
- `montar_ranking_operacional` e `_num` têm teste de unidade
  (`tests/test_backtest_prospectivo_2025.py`) — o mapa veredito→uso e a direção
  da regra simples são verificados, não presumidos. Um bug de direção
  (`pior_primeiro` ordenando descendente) foi pego pelo teste antes do commit.

**Custos e limites:**
- O painel agora depende de `reports/ranking_prospectivo_2025.json`; o backtest
  tem que rodar antes do gerador (documentado no README).
- Há apenas **uma** transição temporal validada (2024→2025). O contrato exige
  reavaliação a cada publicação anual do Inep antes de mudar a regra de qualquer
  UF — está no `aviso_validade` do JSON e no rodapé do painel.
- O campo `auc_ic` do JSON histórico não é mais lido pelo painel; o IC exposto
  agora é o do ganho sobre o baseline (`ganho_ic`), que é o que decide o
  veredito. Nota adicionada ao ADR-0004 §5.

## 5. Reprodução

```powershell
cd PROJETOS/01_PRIORITY/tech-challenge-fase3-alfabetizacao
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe src/evaluation/05_backtest_prospectivo_2025.py
.\.venv\Scripts\python.exe src/visualization/01_gerar_painel_intra_uf.py
```
