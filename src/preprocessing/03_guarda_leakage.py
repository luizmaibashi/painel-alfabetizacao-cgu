"""
Guarda de leakage: testa TODA feature candidata contra padrões de vazamento.

POR QUE ESTE SCRIPT EXISTE
--------------------------
Este projeto já encontrou o MESMO vazamento entrando por quatro colunas
diferentes:

  1. `proficiencia`      -> define o target (achado no desenho)
  2. `presenca`          -> 100% dos "Ausente" têm alfabetizado="Não" (EDA)
  3. `preenchimento_caderno` -> 834/835 coincidem com `presenca` (EDA)
  4. `peso_aluno` (NULO) -> 835/835 dos nulos têm alfabetizado="Não" (2026-08-18)

As três primeiras foram achadas por inspeção manual. A quarta passou por
EDA, dicionário, ADR, baseline, tournament e SHAP sem ser vista — porque o
vazamento não estava no VALOR da coluna, estava no padrão de AUSÊNCIA dela.
Nenhum dos artefatos anteriores olhava para isso.

Inspeção manual não escala e não se repete. Este script transforma a busca
num teste que roda sempre, sobre qualquer snapshot, e falha alto.

O QUE ELE TESTA
---------------
  A. Vazamento por nulidade: `coluna.isna()` prevê o target?
  B. Vazamento por valor: alguma categoria/faixa isola o target quase puro?
  C. Poder suspeito isolado: uma única feature sozinha entrega AUC alto?

Um teste que só olha o valor da coluna (A ausente) teria deixado passar o
`peso_aluno`, que é o motivo de o teste A existir.

USO: rodar depois de gerar o snapshot e antes de treinar qualquer modelo.
Saída: código 1 se houver suspeita ALTA, para poder virar gate de CI.
"""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score

BASE = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(BASE / "src" / "preprocessing"))
from pipeline_preprocessamento import (  # noqa: E402
    COLUNA_TARGET, TODAS_CANDIDATAS,
)

# Limiares. Deliberadamente severos: o custo de um falso alarme é uma
# conferência manual; o custo de um falso negativo é o projeto inteiro medir a
# coisa errada — que foi o que aconteceu até 2026-08-18.
PUREZA_ALTA = 0.95      # grupo com >=95% de uma classe
PUREZA_MEDIA = 0.85
AUC_SOZINHA_ALTA = 0.75
MIN_LINHAS = 30         # grupos menores que isso não são conclusivos


def carregar(caminho: Path) -> pd.DataFrame:
    df = pd.read_parquet(caminho)
    df["_y"] = (df[COLUNA_TARGET] == "Não").astype(int)
    return df


def teste_a_nulidade(df: pd.DataFrame, col: str) -> dict | None:
    """A nulidade da coluna prevê o target? (o caso `peso_aluno`)"""
    nulos = df[col].isna()
    n_nulos = int(nulos.sum())
    if n_nulos < MIN_LINHAS or n_nulos == len(df):
        return None
    taxa_nulo = float(df.loc[nulos, "_y"].mean())
    taxa_resto = float(df.loc[~nulos, "_y"].mean())
    pureza = max(taxa_nulo, 1 - taxa_nulo)
    if pureza < PUREZA_MEDIA:
        return None
    return {
        "coluna": col,
        "teste": "A_nulidade_prediz_target",
        "gravidade": "ALTA" if pureza >= PUREZA_ALTA else "MEDIA",
        "detalhe": (f"{n_nulos} linhas com valor nulo ({n_nulos / len(df):.1%}); "
                    f"nelas o alvo é 'risco' em {taxa_nulo:.1%} dos casos, contra "
                    f"{taxa_resto:.1%} no restante. Pureza {pureza:.1%}."),
    }


def teste_b_valor(df: pd.DataFrame, col: str) -> dict | None:
    """Alguma categoria (ou faixa, para numéricas) isola o alvo quase puro?"""
    serie = df[col].dropna()
    if serie.empty:
        return None

    # Numérica de alta cardinalidade -> fatiar em decis. Categórica -> agrupar
    # pelos próprios valores, qualquer que seja a cardinalidade.
    #
    # CORREÇÃO (2026-08-18, achada pelo ensaio do --full): a versão anterior
    # mandava qualquer coluna com mais de 20 valores distintos para o `qcut`,
    # inclusive texto. Com `sigla_uf` (27 UFs) isso levanta
    # ArrowNotImplementedError, que não é ValueError nem TypeError e portanto
    # escapava do `except` — o guarda MORRIA no snapshot `--full`, deixando a
    # execução mais importante do projeto sem checagem de vazamento nenhuma.
    if pd.api.types.is_numeric_dtype(serie) and serie.nunique() > 20:
        try:
            faixas = pd.qcut(serie, 10, duplicates="drop")
        except Exception:
            return None
        grupos = df.loc[serie.index].groupby(faixas, observed=True)["_y"]
    else:
        grupos = df.groupby(col, dropna=True, observed=True)["_y"]

    piores = []
    for valor, g in grupos:
        if len(g) < MIN_LINHAS:
            continue
        taxa = float(g.mean())
        pureza = max(taxa, 1 - taxa)
        if pureza >= PUREZA_MEDIA:
            piores.append((str(valor), len(g), taxa, pureza))
    if not piores:
        return None
    piores.sort(key=lambda t: -t[3])
    valor, n, taxa, pureza = piores[0]
    return {
        "coluna": col,
        "teste": "B_valor_isola_target",
        "gravidade": "ALTA" if pureza >= PUREZA_ALTA else "MEDIA",
        "detalhe": (f"grupo `{valor}` tem {n} linhas com alvo 'risco' em "
                    f"{taxa:.1%} (pureza {pureza:.1%}). "
                    f"{len(piores)} grupo(s) acima do limiar."),
    }


def teste_c_auc_sozinha(df: pd.DataFrame, col: str) -> dict | None:
    """Uma feature sozinha entrega poder alto demais para ser plausível?"""
    serie = df[col]
    if serie.dropna().nunique() < 2:
        return None
    if pd.api.types.is_numeric_dtype(serie):
        x = serie.fillna(serie.median())
    else:
        # codifica categoria pela taxa de risco do grupo (target encoding
        # simples): serve só para medir separabilidade, não vira feature
        x = serie.map(df.groupby(serie, observed=True)["_y"].mean()).fillna(df["_y"].mean())
    try:
        auc = float(roc_auc_score(df["_y"], x))
    except ValueError:
        return None
    auc = max(auc, 1 - auc)  # direção não importa
    if auc < AUC_SOZINHA_ALTA:
        return None
    return {
        "coluna": col,
        "teste": "C_auc_sozinha_alta",
        "gravidade": "ALTA" if auc >= 0.90 else "MEDIA",
        "detalhe": f"sozinha, esta coluna separa o alvo com AUC {auc:.3f}.",
    }


def main():
    caminho = Path(sys.argv[1]) if len(sys.argv) > 1 else BASE / "data" / "snapshot_modelagem.parquet"
    df = carregar(caminho)
    candidatas = [c for c in TODAS_CANDIDATAS if c in df.columns]

    print("=" * 74)
    print("GUARDA DE LEAKAGE")
    print("=" * 74)
    print(f"Snapshot: {caminho.name} | {len(df)} linhas | "
          f"alvo 'risco' = {df['_y'].mean():.1%}")
    print(f"Features candidatas testadas: {candidatas}\n")

    achados = []
    for col in candidatas:
        for teste in (teste_a_nulidade, teste_b_valor, teste_c_auc_sozinha):
            r = teste(df, col)
            if r:
                achados.append(r)

    if not achados:
        print("Nenhuma suspeita de vazamento nas features candidatas.")
    else:
        for a in sorted(achados, key=lambda r: 0 if r["gravidade"] == "ALTA" else 1):
            marca = "[ALTA] " if a["gravidade"] == "ALTA" else "[MEDIA]"
            print(f"{marca} {a['coluna']}  ({a['teste']})")
            print(f"         {a['detalhe']}")

    altas = [a for a in achados if a["gravidade"] == "ALTA"]
    print("\n" + "-" * 74)
    print(f"Resumo: {len(altas)} suspeita(s) ALTA, "
          f"{len(achados) - len(altas)} MEDIA.")
    if altas:
        print("Suspeita ALTA significa: conferir antes de treinar. Uma coluna que")
        print("isola o alvo quase puro raramente e sinal real -- em geral e o")
        print("proprio evento do alvo entrando por outro nome.")

    out = BASE / "reports" / "guarda_leakage.json"
    out.write_text(json.dumps({
        "snapshot": caminho.name,
        "n_linhas": int(len(df)),
        "candidatas_testadas": candidatas,
        "achados": achados,
    }, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Relatorio salvo em {out}")

    sys.exit(1 if altas else 0)


if __name__ == "__main__":
    main()
