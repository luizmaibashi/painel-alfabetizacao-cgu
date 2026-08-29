# Proveniência — dataset `idhm` (Atlas do Desenvolvimento Humano)

**Gate:** `.claude/rules/dados.md` — GATE CRISP-DM Verificação de Origem (manual)
**Data do preenchimento:** 2026-08-29
**Confirmado por:** Luiz Maibashi (sabatina rodada nesta sessão)

## Fonte

**Base dos Dados** (basedosdados.org), dataset "Atlas do Desenvolvimento
Humano (ADH)", organização **ONU/PNUD** (Programa das Nações Unidas para o
Desenvolvimento) — mesma organização que publica o Atlas Brasil
(atlasbrasil.org.br), origem primária dos dados. Tabela consumida:
`municipio` (ID BigQuery `basedosdados.mundo_onu_adh.municipio`), 35,27 MB.

**Rota tentada primeiro e descartada:** atlasbrasil.org.br (fonte primária
direta) ficou inacessível durante toda a sessão — timeout de conexão
confirmado tanto por fetch automatizado quanto por browser real (Playwright),
em múltiplas tentativas ao longo de ~1h. Não é bloqueio a bot: o site não
respondeu para nenhum tipo de acesso testado. Base dos Dados foi usada como
espelho confiável do mesmo dataset — mesma organização de origem (ONU/PNUD),
mesmas colunas (`idhm`, `idhm_e`, `idhm_l`, `idhm_r`), mesma cobertura
temporal (1991-2010).

## Timestamp da fonte

- **Última atualização na Base dos Dados:** 2021-07-18.
- **Última atualização na fonte original:** não informada pela Base dos
  Dados ("Não informado" no painel "Frequência de atualização dos dados").
- **Cobertura temporal do dataset:** 1991, 2000, 2010 (censos demográficos).
  **2010 é o ano mais recente com série municipal completa** — não existe
  atualização anual do IDHM-M oficial; a limitação já estava prevista no
  ADR-0009 antes do download.
- Download feito **2026-08-29**, uma única vez nesta sessão.

## Rastro de extração

1. Navegado via browser real (Playwright) até
   `https://basedosdados.org/dataset/cbfc7253-089b-44e2-8825-755e1419efc8`.
2. Selecionada tabela **"Município"** na lista lateral ("Tabelas tratadas").
3. Aba **"Download"** (alternativa a "BigQuery e Pacotes" — não exige conta
   GCP/billing project, consistente com o padrão "zero credencial" do
   projeto, README §3.2).
4. Colunas confirmadas via busca por "idhm" no campo de busca da tabela:
   `idhm`, `indice_escolaridade`, `indice_frequencia_escolar`, `idhm_e`,
   `idhm_l`, `idhm_r`, entre 180+ variáveis totais.
5. Clique em **"Download da tabela (35.27 MB)"** — baixa
   `mundo_onu_adh_municipio.csv.gz` diretamente, sem autenticação.

**Reprodutibilidade:** total — mesmo link, mesmo botão, sem filtro manual
a lembrar (diferente do `Alunos.csv`, cujo passo a passo de download não
foi documentado à época). Qualquer pessoa com o link chega ao mesmo
arquivo.

## Arquivos gerados

| Arquivo | Descrição |
|---|---|
| `dados_externos/idhm_municipio_1991_2010.csv.gz` | Download original, íntegro, 3 anos |
| `dados_externos/idhm_municipio_1991_2010.csv` | Descompactado, 16.696 linhas (5.565 municípios × 3 anos, cabeçalho incluso) |
| `dados_externos/idhm_municipio_2010.csv` | **Filtrado para ano 2010** (5.565 municípios + cabeçalho) — é o que o ADR-0009 usa |

## Itens em aberto (não bloqueantes, registrados)

- Data exata de atualização na fonte original (PNUD/IPEA/FJP) não
  confirmada — só se sabe que os dados são do Censo 2010, não quando o
  Atlas Brasil os publicou pela primeira vez.
- `atlasbrasil.org.br` ficou fora do ar durante toda a sessão — vale
  checar em sessão futura se os números batem 1:1 com a fonte primária
  (não foi possível comparar lado a lado nesta sessão).
