"""
EDA genérica sobre um dataset do projeto (base bruta de Alunos ou snapshot).

Cobre o checklist obrigatório de 8 itens do `.claude/rules/dados.md` — mais um
**item 9 que não existia no checklist** e cuja ausência custou caro:

    9. A NULIDADE de cada coluna prediz o alvo?

O item 6 do checklist original conta nulos por coluna, mas nunca os cruza com o
target. Foi exatamente por aí que `peso_aluno` passou: 835 nulos que eram os
alunos ausentes, com alfabetizado="Não" em 100% dos casos. A coluna atravessou
EDA, dicionário, ADR, baseline, tournament e SHAP sem ninguém ver, porque todo
mundo olhava o valor e ninguém olhava a ausência dele.
(Ver Cap. 9 do diário de bordo interno (não publicado) e src/preprocessing/03_guarda_leakage.py.)

REESCRITO EM 2026-08-18: antes era um script linear que fixava
`data/Alunos_amostra.csv` (5.000 linhas) no código. A base completa tem 57.781
alunos e estava disponível o tempo todo — ver Cap. 10 do diário de bordo interno (não publicado).

USO
    python src/preprocessing/01_eda_alunos.py                 # base completa
    python src/preprocessing/01_eda_alunos.py --dataset snapshot
    python src/preprocessing/01_eda_alunos.py --input <caminho> --nome <slug>
"""
import argparse
from pathlib import Path

import numpy as np
import pandas as pd

BASE = Path(__file__).resolve().parents[2]
ALUNOS_COMPLETO = (BASE.parent / "tech-challenge-fase2-alfabetizacao" /
                    "dados" / "Alunos.csv")
SNAPSHOT = BASE / "data" / "snapshot_modelagem.parquet"

ALVO = "alfabetizado"
CLASSE_RISCO = "Não"
SENTINELAS = {-1, 0, 9999, -9999, 999999, 365243, 99, -99}
CODIGOS_AUSENCIA = {"XNA", "XAP", "UNKNOWN", "DESCONHECIDO", "N/A", "NA",
                    "NAO INFORMADO", "NÃO INFORMADO", "SEM INFORMACAO", "-1", "9999"}


def carregar(caminho: Path) -> pd.DataFrame:
    if caminho.suffix == ".parquet":
        return pd.read_parquet(caminho)
    return pd.read_csv(caminho)


def secao(titulo: str) -> str:
    return f"\n### {titulo}\n\n"


def perfil_alvo(df: pd.DataFrame) -> pd.Series | None:
    if ALVO not in df.columns:
        return None
    return (df[ALVO] == CLASSE_RISCO).astype(int)


def eda(df: pd.DataFrame, nome: str, origem: str) -> str:
    y = perfil_alvo(df)
    L = [f"# EDA — {nome} (n={len(df):,})\n".replace(",", ".")]
    L.append(f"**Origem:** `{origem}`\n")
    L.append(f"**Gerado por:** `src/preprocessing/01_eda_alunos.py`\n")
    if y is not None:
        L.append(f"**Alvo:** `{ALVO}` · classe de risco `\"{CLASSE_RISCO}\"` = "
                 f"{y.mean():.1%} das linhas\n")

    L.append("\n## Colunas e tipos\n\n")
    L.append(df.dtypes.to_frame("tipo").to_markdown() + "\n")

    L.append("\n## Checklist CRISP-DM (`.claude/rules/dados.md`)\n")

    # 1 -------------------------------------------------------------------
    L.append(secao("1. Duplicatas"))
    L.append(f"- Linha inteira: **{df.duplicated().sum()}**\n")
    if {"id_aluno", "ano"} <= set(df.columns):
        d_aluno = int(df["id_aluno"].duplicated().sum())
        d_chave = int(df.duplicated(subset=["id_aluno", "ano"]).sum())
        L.append(f"- `id_aluno` sozinho: **{d_aluno}** — mas `id_aluno`+`ano`: "
                 f"**{d_chave}**. O aluno reaparece em ano diferente; a chave "
                 f"real inclui `ano`.\n")

    # 2 -------------------------------------------------------------------
    L.append(secao("2. Colunas constantes / quase-constantes"))
    achou = False
    for c in df.columns:
        vc = df[c].value_counts(normalize=True, dropna=False)
        if len(vc) and vc.iloc[0] > 0.95:
            achou = True
            L.append(f"- `{c}`: **{vc.iloc[0]:.1%}** concentrado em "
                     f"`{vc.index[0]!r}` — sem variância útil.\n")
    if not achou:
        L.append("- Nenhuma coluna acima de 95% de concentração.\n")

    # 3 -------------------------------------------------------------------
    L.append(secao("3. Valores sentinela em numéricas"))
    num = df.select_dtypes(include=[np.number]).columns
    achou = False
    for c in num:
        presentes = SENTINELAS & set(df[c].dropna().unique().tolist())
        # 0 e -1 só interessam se forem frequentes demais para ser real
        suspeitos = {v for v in presentes
                     if (df[c] == v).mean() > 0.02 and v not in (0, 1)}
        if suspeitos:
            achou = True
            L.append(f"- `{c}`: valores suspeitos {sorted(suspeitos)}\n")
    if not achou:
        L.append("- Nenhum valor sentinela clássico com frequência relevante.\n")
    if len(num):
        L.append("\nFaixas das numéricas:\n\n")
        L.append(df[num].describe().T[["min", "50%", "max"]].round(4).to_markdown() + "\n")

    # 4 -------------------------------------------------------------------
    L.append(secao("4. Códigos de ausência mascarados em categóricas"))
    cat = df.select_dtypes(include=["object", "str", "category"]).columns
    achou = False
    for c in cat:
        vals = {str(v).strip().upper() for v in df[c].dropna().unique()}
        inter = vals & CODIGOS_AUSENCIA
        if inter:
            achou = True
            L.append(f"- `{c}`: {sorted(inter)}\n")
    if not achou:
        L.append("- Nenhum código de ausência mascarado encontrado.\n")

    # 5 -------------------------------------------------------------------
    L.append(secao("5. Outliers implausíveis (critério relacional)"))
    if len(num):
        linhas = []
        for c in num:
            s = df[c].dropna()
            if s.empty or s.nunique() < 3:
                continue
            p99, mx = s.quantile(0.99), s.max()
            razao = mx / p99 if p99 > 0 else np.nan
            linhas.append((c, s.median(), p99, mx, razao))
        if linhas:
            t = pd.DataFrame(linhas, columns=["coluna", "mediana", "p99", "max",
                                              "max/p99"]).round(4)
            L.append(t.to_markdown(index=False) + "\n")
            L.append("\nRazão `max/p99` alta indica cauda desproporcional — não é "
                     "prova de erro, é candidato a checar contra a metodologia da "
                     "fonte antes de usar sem tratamento.\n")

    # 6 -------------------------------------------------------------------
    L.append(secao("6. Perfil de nulos por coluna"))
    nulos = df.isna().sum()
    nulos = nulos[nulos > 0].sort_values(ascending=False)
    if len(nulos):
        t = pd.DataFrame({"nulos": nulos, "%": (nulos / len(df) * 100).round(2)})
        L.append(t.to_markdown() + "\n")
    else:
        L.append("- Nenhuma coluna com nulos.\n")

    # 7 -------------------------------------------------------------------
    L.append(secao("7. Redundância entre colunas"))
    pares = []
    if len(num) > 1:
        corr = df[num].corr().abs()
        for i, a in enumerate(corr.columns):
            for b in corr.columns[i + 1:]:
                if pd.notna(corr.loc[a, b]) and corr.loc[a, b] > 0.9:
                    pares.append(f"- `{a}` ↔ `{b}`: correlação {corr.loc[a, b]:.3f}\n")
    for i, a in enumerate(cat):
        for b in list(cat)[i + 1:]:
            if df[a].nunique() == df[b].nunique() and df[a].nunique() > 1:
                tab = pd.crosstab(df[a], df[b])
                if (tab > 0).sum().max() == 1 and (tab > 0).sum(axis=1).max() == 1:
                    pares.append(f"- `{a}` ↔ `{b}`: mapeamento 1:1\n")
    L.extend(pares or ["- Nenhuma redundância forte (|corr| > 0,9 ou 1:1).\n"])

    # 8 -------------------------------------------------------------------
    L.append(secao("8. Relação de cada coluna com o alvo"))
    if y is None:
        L.append(f"- Coluna `{ALVO}` ausente neste dataset.\n")
    else:
        for c in df.columns:
            if c == ALVO:
                continue
            s = df[c]
            if s.nunique(dropna=True) <= 12 and not pd.api.types.is_float_dtype(s):
                g = y.groupby(s.astype(str)).agg(["size", "mean"])
                g.columns = ["n", "% risco"]
                g["% risco"] = (g["% risco"] * 100).round(1)
                L.append(f"\n**`{c}`**\n\n" + g.to_markdown() + "\n")
            elif pd.api.types.is_numeric_dtype(s) and s.nunique() > 12:
                m = s.groupby(y).median()
                if len(m) == 2:
                    L.append(f"\n**`{c}`** — mediana: risco={m.get(1, np.nan):.4f} · "
                             f"não-risco={m.get(0, np.nan):.4f}\n")

    # 9 -------------------------------------------------------------------
    L.append(secao("9. A NULIDADE de cada coluna prediz o alvo? "
                   "(item novo — não estava no checklist)"))
    L.append("Item acrescentado em 2026-08-18. O item 6 conta nulos mas nunca os "
             "cruza com o alvo — e foi por essa fresta que `peso_aluno` passou: "
             "835 nulos que eram os alunos ausentes, todos com alvo \"Não\". "
             "Ver Cap. 9 do diário de bordo interno (não publicado).\n\n")
    if y is None:
        L.append("- Sem alvo neste dataset, item não aplicável.\n")
    else:
        achou = False
        for c in df.columns:
            if c == ALVO:
                continue
            nul = df[c].isna()
            if nul.sum() < 30 or nul.all():
                continue
            achou = True
            t_nulo, t_resto = y[nul].mean(), y[~nul].mean()
            pureza = max(t_nulo, 1 - t_nulo)
            marca = " 🔴 **VAZAMENTO**" if pureza >= 0.95 else (
                    " 🟡 suspeito" if pureza >= 0.85 else "")
            L.append(f"- `{c}`: {int(nul.sum())} nulos ({nul.mean():.1%}) — "
                     f"risco entre nulos **{t_nulo:.1%}** vs **{t_resto:.1%}** "
                     f"no resto{marca}\n")
        if not achou:
            L.append("- Nenhuma coluna com nulos suficientes para o teste (mín. 30).\n")

    # contexto ------------------------------------------------------------
    L.append("\n## Contexto estrutural (não é gate, mas decide o que é possível)\n\n")
    for chave, rotulo in (("id_escola", "escolas"), ("id_municipio", "municípios")):
        if chave in df.columns:
            n = df[chave].nunique()
            g = df.groupby(chave).size()
            L.append(f"- **{rotulo}**: {n:,} · {len(df) / n:.2f} alunos por "
                     f"{rotulo[:-1]} · {(g == 1).mean():.1%} com 1 aluno só\n"
                     .replace(",", "."))
    if "ano" in df.columns:
        L.append(f"- **anos**: {sorted(df['ano'].unique().tolist())}\n")
        if "id_escola" in df.columns and df["ano"].nunique() > 1:
            anos = sorted(df["ano"].unique())
            a, b = anos[0], anos[-1]
            e_a = set(df.loc[df.ano == a, "id_escola"])
            e_b = set(df.loc[df.ano == b, "id_escola"])
            L.append(f"- **escolas em {a} e {b}**: {len(e_a & e_b):,} "
                     f"({len(e_a & e_b) / len(e_b):.1%} das de {b}) — limita "
                     f"qualquer feature histórica por escola\n".replace(",", "."))
    return "".join(L)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dataset", choices=["alunos", "snapshot"], default="alunos")
    ap.add_argument("--input")
    ap.add_argument("--nome")
    args = ap.parse_args()

    if args.input:
        caminho, nome = Path(args.input), args.nome or Path(args.input).stem
    elif args.dataset == "snapshot":
        caminho, nome = SNAPSHOT, "snapshot_modelagem"
    else:
        caminho, nome = ALUNOS_COMPLETO, "alunos"

    df = carregar(caminho)
    texto = eda(df, nome, str(caminho).replace("\\", "/"))
    out = BASE / "reports" / f"eda_{nome}.md"
    out.parent.mkdir(exist_ok=True)
    out.write_text(texto, encoding="utf-8")
    print(f"EDA de `{nome}` ({len(df)} linhas) salva em {out}")


if __name__ == "__main__":
    main()
