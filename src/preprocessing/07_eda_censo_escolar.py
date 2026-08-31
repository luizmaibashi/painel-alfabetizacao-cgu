"""
EDA do agregado municipal do Censo Escolar 2023 (gate CRISP-DM, ADR-0011).

POR QUE ESTE SCRIPT EXISTE
--------------------------
`.claude/rules/dados.md` proibe construir feature antes de existir artefato de
EDA versionado, e enumera 9 itens obrigatorios. O item 9 (a NULIDADE prediz o
alvo?) nasceu NESTE projeto: `peso_aluno` tinha 16,9% de nulos que eram
exatamente os alunos ausentes do exame, com o alvo em "Nao" para 100% deles —
vazamento entrando pela AUSENCIA do valor, invisivel para todo artefato que
olhava so o valor.

Gera `reports/eda_censo_escolar.md` com numero real, nao prosa.

USO
    python src/preprocessing/07_eda_censo_escolar.py
"""
import importlib.util
import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score

warnings.filterwarnings("ignore")
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BASE = Path(__file__).resolve().parents[2]
AGREGADO = BASE / "dados_externos" / "censo_escolar_municipio_2023.csv"
SAIDA = BASE / "reports" / "eda_censo_escolar.md"

_spec = importlib.util.spec_from_file_location(
    "ranking_intra_uf", BASE / "src" / "modeling" / "04_ranking_intra_uf.py")
riu = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(riu)

_spec2 = importlib.util.spec_from_file_location(
    "agregar_censo_escolar",
    BASE / "src" / "preprocessing" / "06_agregar_censo_escolar.py")
ace = importlib.util.module_from_spec(_spec2)
_spec2.loader.exec_module(ace)

SENTINELAS = [-1, 9999, 99999, 999999, 88888, 77777]
NUM_COLS = ace.TODOS_INDICADORES + [f"infra_{g}" for g in ace.INDICADORES] + \
    ["mat_2ano_total", "n_escolas_2ano"]


def ic_wilson(k: int, n: int, z: float = 1.96) -> tuple[float, float]:
    """IC95% de proporcao (Wilson). AGENTS.md: proporcao nunca sem n e IC."""
    if n == 0:
        return (float("nan"), float("nan"))
    p = k / n
    d = 1 + z**2 / n
    c = (p + z**2 / (2 * n)) / d
    m = z * np.sqrt(p * (1 - p) / n + z**2 / (4 * n**2)) / d
    return (round(max(0.0, c - m), 4), round(min(1.0, c + m), 4))


def main():
    linhas: list[str] = []
    A = linhas.append

    agg = pd.read_csv(AGREGADO, dtype={"id_municipio": str})
    print(f"Agregado: {len(agg)} municipios, {agg.shape[1]} colunas")

    print("Montando dataset canonico (para os itens 8 e 9)...")
    m = riu.montar_dataset()[["id_municipio", "sigla_uf", "y"]]
    j = m.merge(agg, on="id_municipio", how="left")
    cobertura = int(j["infra_saneamento"].notna().sum())
    lo, hi = ic_wilson(cobertura, len(j))

    A("# EDA — Censo Escolar 2023 agregado por municipio")
    A("")
    A("> Gerado por `src/preprocessing/07_eda_censo_escolar.py`. "
      "Gate CRISP-DM dos 9 itens (`.claude/rules/dados.md`), ADR-0011.")
    A("")
    A(f"- **Fonte:** {ace.URL_CENSO}")
    A(f"- **SHA-256 do zip:** `{ace.SHA256_ESPERADO}`")
    A(f"- **Agregado:** {len(agg):,} municipios x {agg.shape[1]} colunas"
      .replace(",", "."))
    A(f"- **Cobertura do join** contra o dataset canonico do ranking: "
      f"**{cobertura}/{len(j)}** ({cobertura/len(j):.1%}, "
      f"IC95% Wilson [{lo:.1%}, {hi:.1%}])")
    A("")

    # --- 1. duplicatas -----------------------------------------------------
    dup_chave = int(agg["id_municipio"].duplicated().sum())
    dup_linha = int(agg.duplicated().sum())
    A("## 1. Duplicatas (chave e linha inteira)")
    A("")
    A(f"- Chave `id_municipio` duplicada: **{dup_chave}**")
    A(f"- Linha inteira duplicada: **{dup_linha}**")
    A("")
    A("A agregacao usa `groupby(CO_MUNICIPIO)`, entao duplicata de chave seria "
      "bug da propria funcao, nao caracteristica da fonte. Zero e o esperado — "
      "o teste serve de guarda contra regressao silenciosa.")
    A("")

    # --- 2. constantes -----------------------------------------------------
    A("## 2. Colunas constantes / quase constantes")
    A("")
    A("| Coluna | Valores distintos | % no valor modal | Veredito |")
    A("|---|---:|---:|---|")
    for c in NUM_COLS:
        nun = int(agg[c].nunique(dropna=True))
        modal = float(agg[c].value_counts(normalize=True, dropna=True).iloc[0]) \
            if nun else float("nan")
        v = ("CONSTANTE" if nun <= 1 else
             "quase constante" if modal > 0.95 else "ok")
        A(f"| `{c}` | {nun} | {modal:.1%} | {v} |")
    A("")
    A("Coluna quase constante nao separa municipio nenhum — entra no modelo "
      "gastando dimensao sem informar. Sinalizada aqui, decidida na secao de "
      "features do dicionario.")
    A("")

    # --- 3. sentinelas -----------------------------------------------------
    A("## 3. Valores sentinela em numericas")
    A("")
    achou_sent = []
    for c in NUM_COLS:
        for s in SENTINELAS:
            n = int((agg[c] == s).sum())
            if n:
                achou_sent.append((c, s, n))
    if achou_sent:
        A("| Coluna | Sentinela | Ocorrencias |")
        A("|---|---:|---:|")
        for c, s, n in achou_sent:
            A(f"| `{c}` | {s} | {n} |")
    else:
        A(f"Nenhum dos sentinelas {SENTINELAS} encontrado.")
    A("")
    A("Os indicadores `IN_*` sao proporcoes em [0,1] por construcao da "
      "agregacao, entao sentinela do Censo (se existisse no dado bruto) teria "
      "sido absorvida na media — a checagem util contra isso e a secao 5 "
      "(faixa fora de [0,1]), nao a busca por valor magico.")
    A("")

    # --- 4. ausencia mascarada --------------------------------------------
    A("## 4. Codigos de ausencia mascarados")
    A("")
    fora_faixa = {c: int(((agg[c] < 0) | (agg[c] > 1)).sum())
                  for c in ace.TODOS_INDICADORES + [f"infra_{g}" for g in ace.INDICADORES]}
    total_fora = sum(fora_faixa.values())
    A(f"- Proporcoes fora da faixa [0,1]: **{total_fora}** ocorrencias")
    A("")
    A("A funcao `agregar_por_municipio` trata nulo do Censo excluindo a escola "
      "do peso daquele indicador (nao convertendo para zero) — decisao "
      "testada em `test_indicador_nulo_nao_vira_zero`. Por isso nao ha "
      "categoria de ausencia disfarcada de valor valido: ausencia vira NaN "
      "explicito, contado na secao 6.")
    A("")

    # --- 5. outliers relacionais ------------------------------------------
    A("## 5. Outliers implausiveis por criterio RELACIONAL")
    A("")
    mat_por_escola = agg["mat_2ano_total"] / agg["n_escolas_2ano"].replace(0, np.nan)
    A("| Criterio relacional | n | Leitura |")
    A("|---|---:|---|")
    A(f"| Municipio com 1 unica escola de 2o ano | "
      f"{int((agg.n_escolas_2ano == 1).sum())} | % de infra assume so 2 valores "
      f"(0 ou 1) — nao e erro, e granularidade |")
    A(f"| Media de matricula/escola > 200 | {int((mat_por_escola > 200).sum())} | "
      f"plausivel em capital, checar se ha valor absurdo |")
    A(f"| Media de matricula/escola < 3 | {int((mat_por_escola < 3).sum())} | "
      f"escola rural minuscula, plausivel no Brasil |")
    A(f"| `mat_2ano_total` == 0 | {int((agg.mat_2ano_total == 0).sum())} | "
      f"filtrado na origem (`QT_MAT_FUND_AI_2 > 0`) |")
    A("")
    A(f"Maior media matricula/escola: **{mat_por_escola.max():.0f}** "
      f"(municipio `{agg.loc[mat_por_escola.idxmax(), 'id_municipio']}`). "
      f"Menor: **{mat_por_escola.min():.1f}**.")
    A("")
    A("**Criterio relacional, nao absoluto** (regra do `dados.md`): "
      "'municipio com 300 matriculas' e legitimo; 'municipio com 300 "
      "matriculas numa unica escola de 2o ano' e o que mereceria checagem.")
    A("")

    # --- 6. perfil de nulos -----------------------------------------------
    A("## 6. Perfil de nulos por coluna")
    A("")
    A("| Coluna | Nulos no agregado | % | Nulos apos join canonico | % |")
    A("|---|---:|---:|---:|---:|")
    for c in NUM_COLS:
        na_a = int(agg[c].isna().sum())
        na_j = int(j[c].isna().sum())
        A(f"| `{c}` | {na_a} | {na_a/len(agg):.2%} | {na_j} | {na_j/len(j):.2%} |")
    A("")
    A(f"O nulo apos o join tem duas origens distintas: municipio ausente do "
      f"Censo agregado (nenhuma escola publica com 2o ano) e indicador nulo "
      f"em todas as escolas do municipio. A primeira e a que domina — "
      f"{len(j) - cobertura} municipios do dataset canonico sem linha no "
      f"agregado.")
    A("")

    # --- 7. redundancia ----------------------------------------------------
    A("## 7. Redundancia entre colunas")
    A("")
    corr = agg[ace.TODOS_INDICADORES].corr()
    pares = []
    for i, a in enumerate(ace.TODOS_INDICADORES):
        for b in ace.TODOS_INDICADORES[i+1:]:
            r = corr.loc[a, b]
            if abs(r) > 0.7:
                pares.append((a, b, r))
    if pares:
        A("| Coluna A | Coluna B | Pearson |")
        A("|---|---|---:|")
        for a, b, r in sorted(pares, key=lambda t: -abs(t[2])):
            A(f"| `{a}` | `{b}` | {r:+.3f} |")
        A("")
        A("Par com |r| > 0,7 carrega quase a mesma informacao. E o argumento "
          "a favor dos indices compostos (`infra_*`) em vez das 12 colunas "
          "individuais no modelo — ver ADR-0011.")
    else:
        A("Nenhum par com |r| > 0,7.")
    A("")

    # --- 8. relacao com o alvo --------------------------------------------
    A("## 8. Relacao de cada coluna com o alvo")
    A("")
    A(f"Alvo: `y = (taxa24 < meta_alfabetizacao_2024)`, "
      f"taxa de falha global {j.y.mean():.1%} (n={len(j)}).")
    A("")
    A("AUC isolada de cada coluna (0,5 = sem sinal). **Intra-UF**, porque o "
      "produto decide dentro da UF e AUC nacional confundiria regua estadual "
      "com sinal real (ADR-0004/0005).")
    A("")
    A("| Coluna | AUC nacional | AUC intra-UF (media pond.) |")
    A("|---|---:|---:|")
    for c in NUM_COLS:
        sub = j[[c, "y", "sigla_uf"]].dropna()
        auc_nac = roc_auc_score(sub.y, sub[c]) if sub.y.nunique() > 1 else np.nan
        aucs, pesos = [], []
        for uf, g in sub.groupby("sigla_uf"):
            if g.y.nunique() < 2 or len(g) < riu.MIN_MUNICIPIOS_POR_UF:
                continue
            aucs.append(roc_auc_score(g.y, g[c]))
            pesos.append(len(g))
        auc_uf = float(np.average(aucs, weights=pesos)) if aucs else np.nan
        A(f"| `{c}` | {auc_nac:.4f} | {auc_uf:.4f} |")
    A("")
    A("Leitura: AUC intra-UF perto de 0,5 significa que a coluna nao separa "
      "municipios que falham dos que cumprem a meta DENTRO do estado — que e "
      "a decisao que o produto toma. Distancia de 0,5 em qualquer direcao e "
      "sinal (AUC 0,42 informa tanto quanto 0,58, invertida).")
    A("")

    # --- 9. a NULIDADE prediz o alvo? -------------------------------------
    A("## 9. A NULIDADE de cada coluna prediz o alvo?")
    A("")
    A("O item que nasceu deste projeto (`peso_aluno`, 16,9% de nulos = alunos "
      "ausentes do exame, alvo 'Nao' em 100% deles). Aqui: a taxa de falha "
      "entre municipios COM dado difere da taxa entre municipios SEM dado?")
    A("")
    A("| Coluna | n sem dado | falha (sem dado) | falha (com dado) | Diferenca | "
      "IC95% Wilson (grupo sem dado) |")
    A("|---|---:|---:|---:|---:|---|")
    alerta9 = []
    for c in NUM_COLS:
        nulo = j[c].isna()
        n_nulo = int(nulo.sum())
        if n_nulo == 0:
            A(f"| `{c}` | 0 | — | {j.y.mean():.1%} | sem nulo | — |")
            continue
        f_nulo = float(j.loc[nulo, "y"].mean())
        f_ok = float(j.loc[~nulo, "y"].mean())
        dif = f_nulo - f_ok
        lo9, hi9 = ic_wilson(int(j.loc[nulo, "y"].sum()), n_nulo)
        # CRITERIO: diferenca bruta NAO basta. Com n=1, "100% vs 46,7%" tem
        # IC95% [20,6%, 100%] — intervalo que nao exclui nada. So e sinal se o
        # IC do grupo nulo EXCLUI a taxa do grupo com dado (AGENTS.md: nunca
        # reportar proporcao sem n e sem intervalo; a versao anterior deste
        # script disparava 17 alertas, todos do mesmo unico municipio).
        suspeito = not (lo9 <= f_ok <= hi9)
        if suspeito:
            alerta9.append((c, n_nulo, dif, lo9, hi9))
        marca = " ⚠️" if suspeito else ""
        A(f"| `{c}` | {n_nulo} | {f_nulo:.1%} | {f_ok:.1%} | {dif:+.1%} | "
          f"[{lo9:.1%}, {hi9:.1%}]{marca} |")
    A("")
    if alerta9:
        A("**ATENCAO** — colunas em que o IC95% do grupo sem dado EXCLUI a "
          "taxa do grupo com dado:")
        for c, n, d, lo9, hi9 in alerta9:
            A(f"- `{c}`: n={n}, diferenca {d:+.1%}, "
              f"IC95% Wilson [{lo9:.1%}, {hi9:.1%}]")
    else:
        A("**Nenhuma coluna suspeita.** Em todas, o IC95% da taxa de falha no "
          "grupo sem dado contem a taxa do grupo com dado — ou seja, a "
          "diferenca observada e compativel com acaso. **Sem indicio de "
          "vazamento pela ausencia neste agregado.**")
    A("")

    A("---")
    A("")
    A("## Conclusao operacional")
    A("")
    A(f"- Cobertura do join: {cobertura/len(j):.1%} "
      f"(IC95% [{lo:.1%}, {hi:.1%}]) — sem piso minimo, `SimpleImputer` "
      f"absorve o resto, mesma decisao do ADR-0009.")
    A("- Item 9 e o gate que decide se estas features podem entrar: "
      + ("**ATENCAO, ver alertas acima**." if alerta9 else
         "**limpo**, nenhuma coluna vaza pela ausencia."))
    A("")

    SAIDA.parent.mkdir(parents=True, exist_ok=True)
    SAIDA.write_text("\n".join(linhas), encoding="utf-8")
    print(f"\n  {SAIDA}")
    print(f"  cobertura do join: {cobertura}/{len(j)} ({cobertura/len(j):.1%})")
    print(f"  alertas do item 9: {len(alerta9)}")


if __name__ == "__main__":
    main()
