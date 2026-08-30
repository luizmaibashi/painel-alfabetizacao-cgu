"""
Gera e executa `notebooks/01_analise_completa.ipynb`.

POR QUE O NOTEBOOK E GERADO, E NAO ESCRITO A MAO
-------------------------------------------------
Notebook escrito a mao apodrece: alguem roda uma celula fora de ordem, salva, e
o arquivo versionado passa a mostrar um numero que o codigo nao produz mais.
Este script constroi o notebook e o EXECUTA do zero, entao as saidas gravadas
sao sempre as do codigo atual. Regerar e um comando.

O QUE O NOTEBOOK E (E O QUE NAO E)
-----------------------------------
E a NARRATIVA analitica: percorre os achados que decidiram o projeto, com o
codigo que os produz visivel. NAO e a pipeline -- essa vive em `src/`, e o
notebook a referencia em vez de duplicar. Duplicar a logica de modelagem aqui
criaria duas versoes que divergem em silencio (.claude/rules/dados.md).

Por isso o notebook carrega os JSONs de `reports/` para os resultados caros
(modelos ja treinados, backtest prospectivo) e calcula ao vivo so o que e
barato e diagnostico (crosstabs, correlacoes, os dois graficos).

ESTADO: alinhado ao contrato operacional de 2025 (ADR-0010)
---------------------------------------------------------
As secoes 6 e 7 consomem `backtest_prospectivo_2025.json` e
`ranking_prospectivo_2025.json` -- a mesma fonte do painel
(`01_gerar_painel_intra_uf.py`). Notebook e painel contam a mesma historia:
validacao prospectiva 2024->2025, uso condicional por UF (modelo em 14, regra
simples no CE, abstencao em 8). A secao 5 ilustra o mecanismo da regua
estadual com o ciclo 2023->2024 (dado ja no CSV da Fase 2); o parser do XLSX
de 2025 nao e duplicado aqui -- vive so em `src/evaluation/05_*`.

PALETA
------
Reusa o sistema de cor do painel (`01_gerar_painel_intra_uf.py`), ajustado
para marca de dado: o petrol #0F5C58 do painel tem croma 0,07 e leria como
cinza num grafico, entao vira #0F9086. Par categorico e par divergente
validados nos 5 checks em modo claro (as figuras sao PNG sobre fundo claro --
tema unico deliberado).
"""
import sys
from pathlib import Path

import nbformat
from nbclient import NotebookClient

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BASE = Path(__file__).resolve().parents[2]
SAIDA = BASE / "notebooks" / "01_analise_completa.ipynb"

MD = "markdown"
CODE = "code"

CELULAS: list[tuple[str, str]] = [

(MD, """# Tech Challenge Fase 3 — a análise que decidiu o projeto

Este notebook percorre os achados que mudaram o rumo do projeto, na ordem em
que aconteceram. Ele **não é a pipeline** — essa vive em `src/` e é executada
pelos scripts. Aqui o objetivo é mostrar *como sabemos o que sabemos*.

O projeto entrega duas coisas, e a segunda só existe por causa da primeira:

1. **Modelo aluno-nível** — executado com rigor e **reprovado** no próprio
   critério de falsificação.
2. **Priorização municipal intra-UF** — o que sobrou de pé depois de testar
   tudo, **validado prospectivamente** no ciclo 2024 → 2025 do Inep, mais uma
   advertência de validade que atinge a Fase 2.

> **Alinhamento (2026-08-30):** as seções 6 e 7 refletem o backtest
> prospectivo 2024 → 2025 (ticket 0018) e o contrato de uso condicional por UF
> do `ADR-0010` — a mesma fonte de `reports/painel_intra_uf.html`. Nada de
> número histórico solto: o painel e este notebook contam a mesma história.

> Para regenerar este notebook do zero:
> `python src/visualization/02_gerar_notebook.py`"""),

(CODE, """import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

BASE = Path.cwd().parent if Path.cwd().name == "notebooks" else Path.cwd()
FASE2 = BASE.parent / "tech-challenge-fase2-alfabetizacao"
REPORTS = BASE / "reports"
IMAGES = BASE / "images"
IMAGES.mkdir(exist_ok=True)

# Sistema de cor do projeto, ajustado para marca de dado (ver docstring do gerador)
TEAL, AMBAR, TERRACOTA = "#0F9086", "#A9661F", "#B4553C"
INK, MUTED, GRID = "#16211F", "#67746F", "#D8DEDB"

plt.rcParams.update({
    "figure.dpi": 130, "savefig.dpi": 130,
    "font.size": 9, "axes.titlesize": 11, "axes.labelsize": 9,
    "axes.edgecolor": GRID, "axes.labelcolor": INK, "text.color": INK,
    "xtick.color": MUTED, "ytick.color": MUTED,
    "axes.spines.top": False, "axes.spines.right": False,
    "figure.facecolor": "white", "axes.facecolor": "white",
})

def carregar(nome):
    return json.loads((REPORTS / nome).read_text(encoding="utf-8"))

print("Relatórios disponíveis:")
for p in sorted(REPORTS.glob("*.json")):
    print(" ", p.name)"""),

(MD, """## 1. O vazamento que sustentava o resultado

O projeto encontrou **cinco colunas** que codificavam o mesmo evento — *o aluno
faltou à prova* —, e quem falta recebe rótulo "não alfabetizado" por convenção
do indicador, não por medição.

Três vazavam pelo **valor** (`proficiencia`, `presenca`,
`preenchimento_caderno`). A quarta (`peso_aluno`) vazava pela **nulidade**. A
quinta é a mais instrutiva: `caderno=12` parecia uma categoria de altíssimo
risco (87,3% de "Não"), e três buscas na documentação oficial do INEP não
explicaram por quê.

Um `crosstab` de duas colunas resolveu em segundos o que a documentação não
resolveu."""),

(CODE, """alunos = pd.read_csv(FASE2 / "dados" / "Alunos.csv",
                     usecols=["caderno", "presenca", "alfabetizado"])

tab = alunos.groupby("caderno").apply(lambda g: pd.Series({
    "n": len(g),
    "% ausente": (g.presenca == "Ausente").mean() * 100,
    '% "Não" (todos)': (g.alfabetizado == "Não").mean() * 100,
    '% "Não" (só presentes)': (g.loc[g.presenca != "Ausente", "alfabetizado"] == "Não").mean() * 100,
}), include_groups=False).round(1)

print(tab.to_string())
print()
print('O caderno 12 tem 79,7% de ausentes contra 12-16% dos outros.')
print('Entre quem FEZ a prova, esses alunos vão MELHOR que a média (37,3% vs ~41%).')
print('Os 87,3% eram artefato de ausência — não característica do aluno.')"""),

(MD, """## 2. O teste de falsificação — o critério que o projeto escreveu para si

O `ADR-0001 §5` definiu, antes de qualquer treino, o que reprovaria o projeto:
o modelo aluno-nível precisa **superar** o baseline trivial de aplicar um
número do município igualmente a todos os seus alunos.

Esse critério ficou escrito e **nunca executado** até uma auditoria interna
notar. Quando rodou, passou — e aí descobrimos que a régua estava baixa: o
baseline usado (taxa bruta t-1) era mais fraco que o disponível (a meta do
PDE). Corrigido o baseline, o veredito inverteu."""),

(CODE, """f = carregar("teste_falsificacao.json")
pres = f["so_presentes"]

print("População que importa: só quem fez a prova (rótulo = medição real)")
print(f"  n de teste: {pres['n_teste']:,}".replace(",", "."))
print()
for nome, auc in pres["roc_auc"].items():
    print(f"  {nome:<28} ROC-AUC {auc:.4f}")

ic = pres["ic_diferenca"]
print()
print(f"  Diferença modelo − baseline: {ic['diferenca_observada']:+.4f}")
print(f"  IC95% bootstrap pareado:     [{ic['ic95_inferior']:+.4f}, {ic['ic95_superior']:+.4f}]")
print()
print(f"  VEREDITO: {f['veredito']}")"""),

(MD, """## 3. O teste de resíduo — sobra sinal individual?

A comparação acima trata modelo e baseline como alternativas concorrentes. Mas
o modelo **já tinha** a meta municipal entre as features — então ela não isola
a pergunta certa: *dado que vou usar o baseline municipal de qualquer forma,
adicionar informação de aluno melhora alguma coisa?*

O método correto é dar o baseline ao modelo **como feature** e medir o
incremento."""),

(CODE, """r = carregar("teste_residuo.json")

print(f"  Modelo A (só o baseline municipal):        AUC {r['roc_auc']['modelo_a_so_baseline']:.4f}")
print(f"  Modelo B (baseline + features de aluno):   AUC {r['roc_auc']['modelo_b_baseline_mais_features']:.4f}")
ic = r["ic_diferenca_b_menos_a"]
print()
print(f"  Diferença (B − A): {ic['diferenca_observada']:+.4f}   "
      f"IC95% [{ic['ic95_inferior']:+.4f}, {ic['ic95_superior']:+.4f}]")
print()
print(f"  {r['veredito']}")
print()
print("  Adicionar features de aluno ao baseline PIORA o resultado,")
print("  com significância estatística. O resíduo é vazio.")"""),

(MD, """## 4. A reformulação — e se o problema for o alvo, não o algoritmo?

Com o resíduo vazio, a pergunta mudou: no grão em que o dado **nasce**
(município), dá para prever quem não atinge a meta do PDE?

O experimento tem 5 etapas e **a ordem é o argumento**: as três primeiras
produzem um resultado que parece vitória; a quarta mostra que ela dependia de
informação contemporânea do estado."""),

(CODE, """e = carregar("experimento_opcaoB_municipio.json")

print(f"N = {e['n_municipios']:,} municípios | taxa base de risco: {e['taxa_risco_base']:.1%}"
      .replace(",", "."))
print()
print("ABLAÇÃO — de onde vem o poder preditivo?")
for k, v in e["etapa2_ablacao"].items():
    marca = "  <<< salto de +0,21" if "UF" in k and "contexto" not in k else ""
    print(f"  {k:<26} AUC {v:.4f}{marca}")

print()
print("O SALTO É A UF. E o k-fold aleatório deixa municípios do mesmo estado")
print("no treino E no teste — o modelo aprende a taxa do estado olhando")
print("vizinhos do MESMO ano, informação que uma previsão real não teria.")
print()
print("=" * 62)
print(f"  k-fold aleatório (parece vitória):  AUC {e['etapa3_falsificacao']['auc_modelo']:.4f}")
print(f"  lookup de UF (baseline):            AUC {e['etapa3_falsificacao']['auc_lookup_uf']:.4f}")
print(f"  LEAVE-ONE-UF-OUT (teste honesto):   AUC {e['etapa4_leave_one_uf_out']['auc_leave_one_uf_out']:.4f}")
print("=" * 62)
print("  Colapso: abaixo do acaso (0,500). O 'sinal' era a régua estadual.")"""),

(MD, """## 5. Por que a UF domina: cada estado aplica sua própria prova

As avaliações do Compromisso Nacional Criança Alfabetizada são aplicadas
**pelos estados**. Isso significa que a comparação entre UFs não mede só
política educacional — mede também diferença de régua.

O gráfico abaixo ilustra o **mecanismo** com o ciclo 2023 → 2024 (o dado que
já mora no CSV da Fase 2). Uma queda de 20 pontos percentuais em um ano não é
perda de aprendizado real — é a régua estadual mudando. Isto é **estrutural,
não do ano**: a aplicação continua descentralizada por estado no ciclo 2025, e
é por isso que o backtest prospectivo (seção 6) trava a comparação **dentro**
de cada UF em vez de comparar UFs entre si."""),

(CODE, """metas = pd.read_csv(FASE2 / "dados" / "br_inep_avaliacao_alfabetizacao_meta_alfabetizacao_municipio.csv.gz")
metas["id_municipio"] = metas["id_municipio"].astype(str).str.zfill(7)

d23 = metas[metas.ano == 2023][["id_municipio", "taxa_alfabetizacao", "meta_alfabetizacao_2024"]] \\
    .rename(columns={"taxa_alfabetizacao": "t23"})
d24 = metas[metas.ano == 2024][["id_municipio", "taxa_alfabetizacao"]] \\
    .rename(columns={"taxa_alfabetizacao": "t24"})
m = d23.merge(d24, on="id_municipio").dropna(subset=["t23", "t24", "meta_alfabetizacao_2024"])
m["uf_pref"] = m.id_municipio.str[:2]
m["falhou"] = (m.t24 < m.meta_alfabetizacao_2024).astype(int)
m["delta"] = m.t24 - m.t23

UF = {"11":"RO","12":"AC","13":"AM","14":"RR","15":"PA","16":"AP","17":"TO","21":"MA",
      "22":"PI","23":"CE","24":"RN","25":"PB","26":"PE","27":"AL","28":"SE","29":"BA",
      "31":"MG","32":"ES","33":"RJ","35":"SP","41":"PR","42":"SC","43":"RS","50":"MS",
      "51":"MT","52":"GO","53":"DF"}
g = m.groupby("uf_pref").agg(n=("falhou","size"), delta=("delta","mean"),
                              falha=("falhou","mean")).reset_index()
g["uf"] = g.uf_pref.map(UF)
g = g.sort_values("delta")

fig, ax = plt.subplots(figsize=(7.2, 5.4))
cores = [TERRACOTA if d < 0 else TEAL for d in g.delta]
ax.barh(g.uf, g.delta, color=cores, height=0.68, zorder=3)
ax.axvline(0, color=MUTED, lw=1, zorder=4)
ax.grid(axis="x", color=GRID, lw=0.7, zorder=0)
ax.set_axisbelow(True)
ax.set_xlabel("variação da taxa de alfabetização, 2023 → 2024 (pontos percentuais)")
ax.set_title("Cada estado aplica sua própria prova — ciclo 2023 → 2024\\n"
             "Variações de ±20pp em um ano não são aprendizado real",
             loc="left", fontweight="bold", color=INK)

# folga nos dois lados para os rótulos diretos caberem sem colidir
span = g.delta.max() - g.delta.min()
ax.set_xlim(g.delta.min() - span * 0.16, g.delta.max() + span * 0.16)

# rótulo direto só nos extremos — nunca um número em cada barra
for uf, d in [(g.iloc[0].uf, g.iloc[0].delta), (g.iloc[-1].uf, g.iloc[-1].delta)]:
    ax.text(d + (-0.7 if d < 0 else 0.7), uf, f"{d:+.1f}".replace(".", ","),
            va="center", ha="right" if d < 0 else "left",
            fontsize=8.5, fontweight="bold", color=TERRACOTA if d < 0 else TEAL)

ax.tick_params(length=0)
fig.tight_layout()
fig.savefig(IMAGES / "efeito_regua_estadual.png", bbox_inches="tight", facecolor="white")
plt.show()

print(f"corr(variação da UF, taxa de falha) = {g.delta.corr(g.falha):+.3f}")
print(f"corr(nível de 2023,  taxa de falha) = {g.set_index('uf').join(m.groupby('uf_pref').t23.mean().rename(index=UF)).t23.corr(g.set_index('uf').falha):+.3f}")
print()
print("A correlação com a VARIAÇÃO é mais forte que com o NÍVEL —")
print("não é artefato mecânico da fórmula da meta, é o choque do ano.")"""),

(MD, """### A consequência: nosso próprio ranking nacional é inválido

Os marts `agg_municipio_ranking` e `agg_priorizacao` — da **nossa Fase 2, em
produção** — ordenam municípios **nacionalmente** por taxa de alfabetização e
gap até a meta.

Se cada estado aplica sua própria prova e a variação estadual chega a ±20pp em
um ano, comparar um município do RS com um de MG nessa escala **não é
comparação válida**. Um gestor lendo esse ranking direcionaria recursos para
municípios gaúchos ("90% falharam a meta") quando parte substancial do efeito
é a régua do estado, não a política municipal.

Isso não invalida a engenharia daqueles marts — invalida a *leitura nacional*
que se faz em cima deles."""),

(MD, """## 6. O que funciona: priorização dentro do estado, testada no futuro

Controlada a régua estadual, características municipais **preveem** quem fica
para trás. E o baseline intuitivo — *"priorize quem estava pior no ciclo
anterior"* — é frágil: em vários estados a direção certa é a inversa (regressão
à média somada à meta progressiva do PDE — quem estava baixo tende a subir
mais e bater a meta).

A prova aqui **não é out-of-fold no mesmo período**. É um **backtest
prospectivo**: treina a decisão na transição 2023 → 2024 e pontua o ciclo 2025
do Inep sem nunca ter visto o alvo de 2025 (`src/evaluation/05_*`, ticket
0018). Cada UF é comparada contra a regra simples com IC95% bootstrap pareado.
O veredito por UF vira o **contrato de uso** do painel (`ADR-0010`): ranking do
modelo onde venceu, regra simples onde perdeu, abstenção onde é
inconclusivo."""),

(CODE, """bt = carregar("backtest_prospectivo_2025.json")
rk_full = carregar("ranking_prospectivo_2025.json")

# Os dois JSONs saem do mesmo main() do 05_backtest_prospectivo_2025.py.
# Se um foi regenerado e o outro nao (execucao parcial), o notebook estaria
# misturando o backtest de um ciclo com o contrato de outro -- trava aqui.
assert bt["resumo"]["municipios"] == rk_full["resumo"]["municipios"], (
    "backtest e ranking prospectivo divergem em n de municipios -- regenere os dois")
assert bt["resumo"]["ufs"] == rk_full["resumo"]["ufs"], (
    "backtest e ranking prospectivo divergem em n de UFs -- regenere os dois")

met = pd.DataFrame(bt["metricas_por_uf"]).sort_values("auc_modelo")

# .get com fallback: se um ciclo futuro introduzir um veredito novo
# (ex.: "baseline_vence"), o ponto sai cinza em vez de quebrar o notebook.
COR_VEREDITO = {"modelo_vence": TEAL, "modelo_perde": TERRACOTA, "inconclusivo": MUTED}

fig, ax = plt.subplots(figsize=(7.2, 5.8))
y = np.arange(len(met))

# haste ligando baseline e modelo — o que importa é a DISTÂNCIA entre eles
for yi, (a, b) in enumerate(zip(met.auc_baseline, met.auc_modelo)):
    ax.plot([a, b], [yi, yi], color=GRID, lw=1.6, zorder=1, solid_capstyle="round")

ax.scatter(met.auc_baseline, y, s=52, color=AMBAR, zorder=3,
           label="regra simples (direção do próprio estado em 2024)",
           edgecolor="white", linewidth=1.4)
ax.scatter(met.auc_modelo, y, s=52,
           color=[COR_VEREDITO.get(v, MUTED) for v in met.veredito], zorder=3,
           label="modelo intra-UF — verde vence, terracota perde, cinza inconclusivo",
           edgecolor="white", linewidth=1.4)

ax.axvline(0.5, color=MUTED, lw=1, ls=(0, (4, 3)), zorder=2)
ax.set_ylim(-0.8, len(met) - 0.2)
ax.text(0.5, len(met) - 0.45, " acaso", fontsize=8, color=MUTED, va="top")

ax.set_yticks(y, met.uf)
ax.set_xlabel("ROC-AUC prospectivo (predições para o ciclo 2025, alvo nunca visto)")
ax.set_title("Backtest prospectivo 2024 → 2025: modelo contra regra simples\\n"
             "Modelo vence em 14 UFs; onde não vence, o painel usa a regra ou se abstém",
             loc="left", fontweight="bold", color=INK)
ax.grid(axis="x", color=GRID, lw=0.7, zorder=0)
ax.set_axisbelow(True)
ax.tick_params(length=0)
ax.legend(frameon=False, loc="lower right", fontsize=8.5)
fig.tight_layout()
fig.savefig(IMAGES / "modelo_vs_intuicao_por_uf.png", bbox_inches="tight", facecolor="white")
plt.show()

res = bt["resumo"]
print("  MÉDIA PONDERADA POR MUNICÍPIO (backtest prospectivo):")
print(f"    regra simples  AUC {res['auc_baseline_ponderado']:.4f}")
print(f"    MODELO         AUC {res['auc_modelo_ponderado']:.4f}  ({res['ganho_ponderado']:+.4f})")
print()
print(f"  Municípios pontuados: {res['municipios']:,}".replace(",", "."))
print(f"  n de UFs: {res['ufs']}")
print(f"  Veredito por UF (IC95% bootstrap pareado, {res['reamostragens_bootstrap']} reamostragens):")
print(f"    modelo vence   {res['ufs_modelo_vence']}")
print(f"    inconclusivo   {res['ufs_inconclusivo']}")
print(f"    modelo perde   {res['ufs_modelo_perde']}")
print()
rk = rk_full["resumo"]
print("  CONTRATO DE USO DO PAINEL (ADR-0010), derivado do veredito acima:")
print(f"    ranking do modelo  {rk['ufs_ranking_modelo']} UFs")
print(f"    regra simples      {rk['ufs_regra_simples']} UF (CE)")
print(f"    abstenção          {rk['ufs_abster']} UFs — o painel diz que não há recomendação")"""),

(MD, """## 7. O que sai disso

**Duas recomendações de política pública, ambas com intervalo de confiança:**

1. **Busca ativa de alunos** → usar a **meta do PDE do município**, não um
   modelo aluno-nível. Mais simples, mais barata, e estatisticamente mais
   eficaz com os dados disponíveis.
2. **Priorização entre municípios** → comparar **dentro do estado**, nunca
   entre estados. O backtest prospectivo 2024 → 2025 diz onde confiar em quê:
   o modelo intra-UF vence a regra simples em **14 das 23 UFs** (ganho
   ponderado +0,16 de AUC, IC95% bootstrap pareado por UF); no CE a regra
   simples fica; nas **8 restantes o veredito é inconclusivo** e a resposta
   honesta é não priorizar por esse critério.

A recomendação 2 não fica em prosa: `reports/painel_intra_uf.html` é a
ferramenta, com **5.285 municípios**, **3 modos por UF** (ranking do modelo /
regra simples / abstenção diagnóstica) travados pelo contrato do `ADR-0010`, e
a advertência de validade embutida na interface — o painel **não tem visão
nacional, de propósito**. Notebook e painel leem os mesmos JSONs de `reports/`.

---

### O que este projeto demonstra

Definir um critério de falsificação antes de medir, executá-lo, **desconfiar da
própria vitória quando ela aparece**, corrigir a régua e reportar o resultado
desfavorável com significância — duas vezes, em dois grãos diferentes — e então
**testar o que sobrou num backtest prospectivo**, com o alvo do ciclo seguinte
nunca visto no treino.

O resultado negativo do modelo aluno-nível não é o fracasso do projeto. É o
que dá credibilidade ao resultado positivo do modelo intra-UF — que passou no
teste mais duro que havia para dar: prever o futuro."""),
]


def main():
    nb = nbformat.v4.new_notebook()
    nb.cells = [nbformat.v4.new_markdown_cell(txt) if tipo == MD
                else nbformat.v4.new_code_cell(txt)
                for tipo, txt in CELULAS]
    nb.metadata = {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python"},
    }

    SAIDA.parent.mkdir(exist_ok=True)
    print(f"Executando {len(nb.cells)} celulas...")
    NotebookClient(nb, timeout=900, kernel_name="python3",
                   resources={"metadata": {"path": str(SAIDA.parent)}}).execute()

    nbformat.write(nb, SAIDA)
    kb = SAIDA.stat().st_size / 1024
    print(f"Notebook gerado e executado: {SAIDA}  ({kb:.0f} KB)")
    print("Figuras salvas em images/")


if __name__ == "__main__":
    main()
