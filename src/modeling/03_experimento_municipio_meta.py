"""
EXPERIMENTO OPÇÃO B — reformular o alvo: MUNICÍPIO vai atingir a meta do PDE?

CONTEXTO
--------
O modelo aluno-nível falhou no teste de falsificação (Cap. 14 do
o diário de bordo interno (não publicado)): perdeu para a meta do PDE aplicada uniformemente, e o
teste de resíduo (03_teste_residuo.py) mostrou que não sobra sinal individual.

A pergunta desta rodada é outra: no grão em que o dado NASCE (município), dá
para prever quem não atinge a meta do ciclo seguinte? É a pergunta de negócio
nº 4 do enunciado ("Como prever municípios que podem não atingir metas
futuras?"), a única das cinco sem resposta.

DESENHO
-------
Features (todas conhecidas ANTES do resultado de 2024):
    taxa_alfabetizacao_2023, meta_2024, meta_2025, populacao_total [, sigla_uf]
Alvo:
    y = 1 se taxa_2024 < meta_2024  (município não atingiu a meta)
N = 5.232 municípios com taxa medida em 2023 E 2024.

O QUE ESTE SCRIPT MEDE (5 etapas, nesta ordem — a ordem é o argumento)
----------------------------------------------------------------------
1. Tournament binário vs contínuo, k-fold aleatório  -> qual formulação usar
2. Ablação                                           -> de onde vem o sinal
3. Falsificação contra lookup de UF                  -> o modelo vence?
4. **Leave-One-UF-Out**                              -> generaliza para UF nova?
5. Modelo DENTRO de cada UF                          -> onde o sinal é legítimo

A etapa 4 é a que decide. As etapas 1-3 produzem um resultado que PARECE
vitória (AUC 0,77); a 4 mostra que essa vitória depende de o modelo ter visto
outros municípios da MESMA UF no MESMO ano — informação contemporânea que uma
previsão real não teria. É o mesmo padrão que derrubou o modelo aluno-nível,
um nível de agregação acima.
"""
import json
import sys
import warnings
from pathlib import Path

# Console do Windows abre em cp1252 e quebra em '->' unicode, 'R2' e emoji.
# Sem isto o script morre no meio do relatorio, depois de ja ter treinado tudo.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression, Ridge
from sklearn.metrics import r2_score, roc_auc_score
from sklearn.model_selection import KFold, LeaveOneGroupOut, StratifiedKFold
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, RobustScaler
from xgboost import XGBClassifier, XGBRegressor

warnings.filterwarnings("ignore")

BASE = Path(__file__).resolve().parents[2]
FASE2 = BASE.parent / "tech-challenge-fase2-alfabetizacao"
METAS = FASE2 / "dados" / "br_inep_avaliacao_alfabetizacao_meta_alfabetizacao_municipio.csv.gz"
TERRITORIO = BASE / "data" / "territorio_local.parquet"

RANDOM_STATE = 42
N_FOLDS = 5
NUM = ["taxa23", "meta_alfabetizacao_2024", "meta_alfabetizacao_2025", "populacao_total"]
CAT = ["sigla_uf"]


def montar_dataset() -> pd.DataFrame:
    df = pd.read_csv(METAS)
    df["id_municipio"] = df["id_municipio"].astype(str).str.zfill(7)
    d23 = df[df.ano == 2023][["id_municipio", "taxa_alfabetizacao",
                               "meta_alfabetizacao_2024", "meta_alfabetizacao_2025"]] \
        .rename(columns={"taxa_alfabetizacao": "taxa23"})
    d24 = df[df.ano == 2024][["id_municipio", "taxa_alfabetizacao"]] \
        .rename(columns={"taxa_alfabetizacao": "taxa24"})
    m = d23.merge(d24, on="id_municipio").dropna(
        subset=["taxa23", "taxa24", "meta_alfabetizacao_2024"])

    terr = pd.read_parquet(TERRITORIO)
    t23 = terr[terr.ano == 2023][["id_municipio", "populacao_total", "sigla_uf"]] \
        .drop_duplicates("id_municipio")
    m = m.merge(t23, on="id_municipio", how="left").reset_index(drop=True)

    m["uf"] = m.id_municipio.str[:2]
    m["y"] = (m.taxa24 < m.meta_alfabetizacao_2024).astype(int)
    m["gap"] = m.meta_alfabetizacao_2024 - m.taxa24
    m["delta"] = m.taxa24 - m.taxa23
    return m


def _prep(num, cat):
    blocos = [("n", Pipeline([("i", SimpleImputer(strategy="median")),
                               ("s", RobustScaler())]), num)]
    if cat:
        blocos.append(("c", OneHotEncoder(handle_unknown="ignore"), cat))
    return ColumnTransformer(blocos)


def _oof_classificador(m, modelo, num, cat, cv) -> np.ndarray:
    X, y = m[num + cat], m.y.values
    oof = np.zeros(len(m))
    for tr, te in cv:
        pipe = Pipeline([("p", _prep(num, cat)), ("m", modelo)])
        pipe.fit(X.iloc[tr], y[tr])
        oof[te] = pipe.predict_proba(X.iloc[te])[:, 1]
    return oof


def ic_bootstrap(y, score_a, score_b, n_boot=2000) -> dict:
    """IC95% da diferença de AUC, bootstrap pareado (mesmo método do Cap. 14)."""
    rng = np.random.default_rng(RANDOM_STATE)
    difs = []
    for _ in range(n_boot):
        i = rng.integers(0, len(y), len(y))
        if y[i].min() == y[i].max():
            continue
        difs.append(roc_auc_score(y[i], score_a[i]) - roc_auc_score(y[i], score_b[i]))
    lo, hi = np.percentile(difs, [2.5, 97.5])
    return {"diferenca": float(roc_auc_score(y, score_a) - roc_auc_score(y, score_b)),
            "ic95_inferior": float(lo), "ic95_superior": float(hi),
            "significativo": bool(lo > 0)}


# ---------------------------------------------------------------- etapa 1
def etapa1_tournament(m) -> dict:
    print("\n" + "=" * 74)
    print("1) TOURNAMENT — formulação binária vs contínua (k-fold aleatório)")
    print("=" * 74)
    X, y, gap = m[NUM + CAT], m.y.values, m.gap.values
    skf = list(StratifiedKFold(N_FOLDS, shuffle=True, random_state=RANDOM_STATE).split(X, y))
    kf = list(KFold(N_FOLDS, shuffle=True, random_state=RANDOM_STATE).split(X))

    res = {"binaria": {}, "continua": {}}
    print("  BINÁRIA (atingiu a meta? sim/não)")
    for nome, mod in {
        "logistica": LogisticRegression(max_iter=2000, random_state=RANDOM_STATE),
        "random_forest": RandomForestClassifier(n_estimators=300, max_depth=8,
                                                 random_state=RANDOM_STATE, n_jobs=-1),
        "xgboost": XGBClassifier(n_estimators=300, max_depth=4, learning_rate=0.1,
                                  random_state=RANDOM_STATE, eval_metric="logloss",
                                  # n_jobs=1: hist + threads = AUC nao reproduz
                                  # entre maquinas (ver 0009 no wayfinder).
                                  tree_method="hist", n_jobs=1),
    }.items():
        auc = roc_auc_score(y, _oof_classificador(m, mod, NUM, CAT, skf))
        res["binaria"][nome] = float(auc)
        print(f"    {nome:<20} AUC {auc:.4f}")

    print("  CONTÍNUA (gap até a meta, em pontos percentuais)")
    for nome, mod in {
        "ridge": Ridge(alpha=1.0, random_state=RANDOM_STATE),
        "random_forest": RandomForestRegressor(n_estimators=300, max_depth=8,
                                                random_state=RANDOM_STATE, n_jobs=-1),
        "xgboost": XGBRegressor(n_estimators=300, max_depth=4, learning_rate=0.1,
                                 # n_jobs=1: hist + threads = resultado nao
                                 # reproduz entre maquinas (ver 0009).
                                 random_state=RANDOM_STATE, tree_method="hist", n_jobs=1),
    }.items():
        oof = np.zeros(len(m))
        for tr, te in kf:
            pipe = Pipeline([("p", _prep(NUM, CAT)), ("m", mod)])
            pipe.fit(X.iloc[tr], gap[tr])
            oof[te] = pipe.predict(X.iloc[te])
        r2, auc = r2_score(gap, oof), roc_auc_score(y, oof)
        res["continua"][nome] = {"r2": float(r2), "auc_equivalente": float(auc)}
        print(f"    {nome:<20} R² {r2:+.4f} | AUC-equiv {auc:.4f}")

    melhor_b = max(res["binaria"].values())
    melhor_c = max(v["auc_equivalente"] for v in res["continua"].values())
    print(f"\n  Melhor binária {melhor_b:.4f} vs melhor contínua {melhor_c:.4f} "
          f"→ {'BINÁRIA' if melhor_b >= melhor_c else 'CONTÍNUA'} (empate técnico)")
    return res


# ---------------------------------------------------------------- etapa 2
def etapa2_ablacao(m) -> dict:
    print("\n" + "=" * 74)
    print("2) ABLAÇÃO — de onde vem o poder preditivo?")
    print("=" * 74)
    y = m.y.values
    skf = list(StratifiedKFold(N_FOLDS, shuffle=True, random_state=RANDOM_STATE).split(m, y))
    rf = lambda: RandomForestClassifier(n_estimators=300, max_depth=8,
                                         random_state=RANDOM_STATE, n_jobs=-1)
    combos = {
        "só taxa23": (["taxa23"], []),
        "só meta2024": (["meta_alfabetizacao_2024"], []),
        "taxa23 + meta2024": (["taxa23", "meta_alfabetizacao_2024"], []),
        "taxa23 + meta2024 + UF": (["taxa23", "meta_alfabetizacao_2024"], ["sigla_uf"]),
        "só contexto (pop + UF)": (["populacao_total"], ["sigla_uf"]),
        "TUDO": (NUM, CAT),
    }
    res = {}
    for label, (num, cat) in combos.items():
        auc = float(roc_auc_score(y, _oof_classificador(m, rf(), num, cat, skf)))
        res[label] = auc
        print(f"    {label:<26} AUC {auc:.4f}")
    print("\n  → adicionar UF salta ~0,21 de AUC. O sinal é de ESTADO, não de município.")
    return res


# ---------------------------------------------------------------- etapa 3
def etapa3_falsificacao(m) -> dict:
    print("\n" + "=" * 74)
    print("3) FALSIFICAÇÃO — o modelo vence o lookup de UF (24 números)?")
    print("=" * 74)
    X, y = m[NUM + CAT], m.y.values
    skf = list(StratifiedKFold(N_FOLDS, shuffle=True, random_state=RANDOM_STATE).split(X, y))
    oof = _oof_classificador(m, RandomForestClassifier(
        n_estimators=300, max_depth=8, random_state=RANDOM_STATE, n_jobs=-1), NUM, CAT, skf)

    # lookup de UF calculado SÓ no treino de cada fold (senão é vazamento)
    oof_uf = np.zeros(len(m))
    for tr, te in skf:
        taxas = m.iloc[tr].groupby("uf").y.mean()
        oof_uf[te] = m.iloc[te].uf.map(taxas).fillna(y[tr].mean()).values

    ic = ic_bootstrap(y, oof, oof_uf)
    print(f"    modelo completo        AUC {roc_auc_score(y, oof):.4f}")
    print(f"    lookup de UF           AUC {roc_auc_score(y, oof_uf):.4f}")
    print(f"    diferença {ic['diferenca']:+.4f}  IC95% "
          f"[{ic['ic95_inferior']:+.4f}, {ic['ic95_superior']:+.4f}]")
    print(f"\n  → {'PASSOU' if ic['significativo'] else 'não passou'} — "
          "mas ver etapa 4 antes de concluir.")
    return {"auc_modelo": float(roc_auc_score(y, oof)),
            "auc_lookup_uf": float(roc_auc_score(y, oof_uf)), "ic": ic}


# ---------------------------------------------------------------- etapa 4
def etapa4_leave_one_uf_out(m) -> dict:
    print("\n" + "=" * 74)
    print("4) LEAVE-ONE-UF-OUT — a UF de teste NUNCA foi vista no treino")
    print("=" * 74)
    print("  Por que importa: no k-fold aleatório, municípios da mesma UF ficam")
    print("  no treino E no teste. O modelo aprende a taxa de falha do estado a")
    print("  partir de vizinhos do MESMO ano — informação que uma previsão real")
    print("  não teria. Aqui isso é impossível por construção.\n")
    X, y, g = m[NUM], m.y.values, m.uf.values   # sem sigla_uf: UF de teste é nova
    oof = np.zeros(len(m))
    for tr, te in LeaveOneGroupOut().split(X, y, g):
        if len(np.unique(y[te])) < 2:
            continue
        pipe = Pipeline([("p", _prep(NUM, [])), ("m", RandomForestClassifier(
            n_estimators=300, max_depth=8, random_state=RANDOM_STATE, n_jobs=-1))])
        pipe.fit(X.iloc[tr], y[tr])
        oof[te] = pipe.predict_proba(X.iloc[te])[:, 1]
    auc = float(roc_auc_score(y, oof))
    print(f"    AUC global (UF nunca vista):  {auc:.4f}   (acaso = 0,500)")
    print("\n  🔴 COLAPSO. A vitória da etapa 3 era informação contemporânea de UF.")
    return {"auc_leave_one_uf_out": auc}


# ---------------------------------------------------------------- etapa 5
def etapa5_dentro_da_uf(m) -> dict:
    print("\n" + "=" * 74)
    print("5) DENTRO DE CADA UF — onde o sinal é legítimo")
    print("=" * 74)
    linhas = []
    for uf, g in m.groupby("uf"):
        if len(g) < 100 or g.y.nunique() < 2:
            continue
        X, y = g[NUM], g.y.values
        oof = np.zeros(len(g))
        for tr, te in StratifiedKFold(N_FOLDS, shuffle=True,
                                       random_state=RANDOM_STATE).split(X, y):
            if len(np.unique(y[tr])) < 2:
                continue
            pipe = Pipeline([("p", _prep(NUM, [])), ("m", RandomForestClassifier(
                n_estimators=200, max_depth=6, random_state=RANDOM_STATE, n_jobs=-1))])
            pipe.fit(X.iloc[tr], y[tr])
            oof[te] = pipe.predict_proba(X.iloc[te])[:, 1]
        linhas.append({"uf": uf, "n": len(g), "taxa_falha": float(g.y.mean()),
                        "auc_modelo": float(roc_auc_score(y, oof)),
                        # baseline ingênuo: "quem estava pior em 2023 falha mais"
                        "auc_baseline": float(roc_auc_score(y, -g.taxa23.values))})
    r = pd.DataFrame(linhas)
    am = float(np.average(r.auc_modelo, weights=r.n))
    ab = float(np.average(r.auc_baseline, weights=r.n))
    print(f"    UFs avaliadas (n>=100): {len(r)}")
    print(f"    AUC modelo (média ponderada):   {am:.4f}")
    print(f"    AUC baseline ingênuo:           {ab:.4f}  (direção FIXA — ver aviso)")
    print(f"    UFs em que o modelo vence:      {int((r.auc_modelo > r.auc_baseline).sum())} de {len(r)}")
    print("\n  → dentro do estado HÁ sinal real.")
    print("\n  " + "!" * 68)
    print("  !! AVISO (ADR-0005): o baseline acima NÃO é a comparação válida.")
    print("  !! Ele fixa a direção ('quem estava pior falha mais'). AUC é")
    print(f"  !! antissimétrica: AUC(-s) = 1 - AUC(s), então {ab:.4f} lido ao")
    print(f"  !! contrário vale {1 - ab:.4f} — não é 'abaixo do acaso', é a mesma")
    print("  !! regra na direção oposta. Comparar contra a direção mais fraca")
    print("  !! INFLA o ganho do modelo (foi assim que virou '+0,245').")
    print("  !!")
    print("  !! O baseline HONESTO escolhe a direção por leave-one-out e vale")
    print("  !! 0,6209, contra 0,6478 do modelo -> ganho real de +0,027.")
    print("  !! Fonte canônica: src/modeling/04_ranking_intra_uf.py")
    print("  !! Este script é o EXPERIMENTO que descobriu o fenômeno; os")
    print("  !! números dele são históricos e não devem ser citados como")
    print("  !! resultado do projeto.")
    print("  " + "!" * 68)
    return {"auc_modelo_ponderado": am, "auc_baseline_ponderado": ab,
            "ufs_avaliadas": int(len(r)),
            "ufs_modelo_vence": int((r.auc_modelo > r.auc_baseline).sum()),
            "por_uf": r.to_dict(orient="records")}


# ---------------------------------------------------------------- diagnóstico
def diagnostico_uf(m) -> dict:
    print("\n" + "=" * 74)
    print("DIAGNÓSTICO — por que a UF domina? (choque estadual no ano da prova)")
    print("=" * 74)
    g = m.groupby("uf").agg(n=("y", "size"), falha=("y", "mean"),
                             taxa23=("taxa23", "mean"), taxa24=("taxa24", "mean"),
                             delta=("delta", "mean"))
    c_nivel = float(g.taxa23.corr(g.falha))
    c_delta = float(g.delta.corr(g.falha))
    print(f"    corr(nível 2023 da UF, taxa de falha):  {c_nivel:+.3f}")
    print(f"    corr(variação 23→24 da UF, falha):     {c_delta:+.3f}  ← mais forte")
    piores = g.nsmallest(3, "delta")[["taxa23", "taxa24", "delta", "falha"]]
    melhores = g.nlargest(3, "delta")[["taxa23", "taxa24", "delta", "falha"]]
    print("\n    UFs que mais CAÍRAM entre 2023 e 2024:")
    print(piores.round(2).to_string())
    print("\n    UFs que mais SUBIRAM:")
    print(melhores.round(2).to_string())
    print("\n  → variações de ±20pp em UM ano não são aprendizado real: são mudança")
    print("    na aplicação/correção da prova pelo estado. As avaliações do CNCA")
    print("    são aplicadas PELOS ESTADOS, então cada UF tem sua própria régua.")
    return {"corr_nivel_falha": c_nivel, "corr_delta_falha": c_delta,
            "por_uf": g.round(3).reset_index().to_dict(orient="records")}


def main():
    m = montar_dataset()
    print("=" * 74)
    print("EXPERIMENTO OPÇÃO B — município, alvo = não atingir a meta do PDE")
    print("=" * 74)
    print(f"N municípios (rede Municipal, taxa em 2023 e 2024): {len(m):,}".replace(",", "."))
    print(f"Taxa base de risco (não atingiu a meta 2024): {m.y.mean():.1%}")

    saida = {
        "n_municipios": int(len(m)),
        "taxa_risco_base": float(m.y.mean()),
        "etapa1_tournament": etapa1_tournament(m),
        "etapa2_ablacao": etapa2_ablacao(m),
        "etapa3_falsificacao": etapa3_falsificacao(m),
        "etapa4_leave_one_uf_out": etapa4_leave_one_uf_out(m),
        "etapa5_dentro_da_uf": etapa5_dentro_da_uf(m),
        "diagnostico_uf": diagnostico_uf(m),
    }

    print("\n" + "=" * 74)
    print("VEREDITO")
    print("=" * 74)
    a3 = saida["etapa3_falsificacao"]["auc_modelo"]
    a4 = saida["etapa4_leave_one_uf_out"]["auc_leave_one_uf_out"]
    a5 = saida["etapa5_dentro_da_uf"]["auc_modelo_ponderado"]
    b5 = saida["etapa5_dentro_da_uf"]["auc_baseline_ponderado"]
    print(f"  k-fold aleatório (parece vitória):  AUC {a3:.4f}")
    print(f"  leave-one-UF-out (teste honesto):   AUC {a4:.4f}  ← não generaliza")
    print(f"  dentro da UF (uso legítimo):        AUC {a5:.4f} vs baseline {b5:.4f}")
    print(f"     ^^ baseline {b5:.4f} = direção FIXA, REFUTADO pelo ADR-0005.")
    print("     O baseline honesto é 0,6209 e o ganho real é +0,027, não o que")
    print("     esta linha sugere. Número canônico: 04_ranking_intra_uf.py")
    print("\n  >> Ranking NACIONAL de municípios é inválido: cada estado aplica sua")
    print("     própria prova, e o efeito de estado (choque de até 20pp em um ano)")
    print("     domina qualquer característica municipal.")
    print("  >> Ranking DENTRO do estado é válido, mas o ganho é +0,027 — e por UF")
    print("     são 3 vitórias, 3 derrotas e 17 inconclusivos (ver ticket 0016).")
    saida["veredito"] = {
        "ranking_nacional": "INVALIDO — efeito de estado domina e nao generaliza",
        "ranking_intra_uf": (
            "VALIDO com ressalva — ganho de +0,027 sobre o baseline HONESTO "
            "(0,6209), nao sobre o baseline de direcao fixa reportado neste "
            "script. Por UF: 3 vencem, 3 perdem, 17 inconclusivos. "
            "Fonte canonica: 04_ranking_intra_uf.py; ver ADR-0004 e ADR-0005."
        ),
        "_aviso": (
            "Os numeros deste script sao HISTORICOS (o experimento que "
            "descobriu o fenomeno). Nao citar como resultado do projeto."
        ),
    }

    out = BASE / "reports" / "experimento_opcaoB_municipio.json"
    out.write_text(json.dumps(saida, ensure_ascii=False, indent=2, default=float),
                   encoding="utf-8")
    print(f"\nRelatório salvo em {out}")


if __name__ == "__main__":
    main()
