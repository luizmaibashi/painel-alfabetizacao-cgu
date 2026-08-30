"""
O veredito da falsificacao sobrevive a troca de algoritmo?

A PERGUNTA
----------
`02_teste_falsificacao.py` mede UM modelo (XGBoost 800/8) contra o melhor
baseline municipal e conclui que o aluno-nivel perde. Dai vem uma objecao
obvia, que ate 2026-08-29 o projeto nao tinha resposta medida para:

    "Voces perderam porque escolheram o algoritmo errado."

Este script responde. Roda os TRES candidatos do torneio
(`02_tournament_modelos.py`) no MESMO split temporal, com as MESMAS features e
o MESMO baseline do teste canonico, e pergunta se algum deles limpa a barra.

POR QUE ISTO NAO E "TENTAR DE NOVO ATE PASSAR"
----------------------------------------------
A diferenca entre replicar um teste e caca-niquel estatistico esta em declarar
o criterio ANTES e corrigir para o numero de tentativas. As duas coisas estao
feitas aqui:

  - Criterio, escrito antes de rodar: o modelo passa se a diferenca de AUC
    contra o melhor baseline for POSITIVA com intervalo inteiramente acima de
    zero. Identico ao ADR-0001 secao 5, sem afrouxar nada.
  - Correcao de comparacoes multiplas: sao 3 comparacoes informando UMA
    decisao ("existe algoritmo que salva o aluno-nivel?"). Sem correcao, a
    chance de um vencer por ruido cresce com o numero de tentativas -- o
    winner's curse. Reporta-se o IC95 por comparacao E o IC corrigido por
    Bonferroni (alpha 0,05/3 = 0,0167 -> IC de 98,33%), e o veredito usa o
    CORRIGIDO. Gate "correcao de comparacoes multiplas" do .claude/rules/dados.md.

O QUE E REUSADO, E POR QUE
---------------------------
`carregar`, `baselines_municipais` e o desenho do split vem por import do
proprio `02_teste_falsificacao.py`, nao reescritos aqui. Isso e deliberado: o
bug do ADR-0005 foi exatamente uma regua de baseline calculada em separado que
divergiu da canonica e inflou o ganho de +0,027 para +0,245. Comparacao contra
baseline reimplementado nao vale nada; entao o baseline vem de la, ponto.

A unica coisa reimplementada e o bootstrap, porque a versao canonica fixa o
intervalo em 95% e aqui e preciso o corrigido tambem. Para que essa copia nao
divirja em silencio, `tests/test_robustez_algoritmo.py` exige que ela reproduza
a saida de `ic_diferenca_auc` no nivel de 95%.

LEITURA DO RESULTADO
--------------------
Se os tres perderem, o veredito do projeto deixa de ser "o XGBoost perdeu" e
passa a ser "o problema nao tem solucao por algoritmo" -- consistente com o
argumento estrutural (chave de join unica => toda feature e constante dentro
do municipio), e muito mais dificil de refutar.

Se algum vencer, isso e achado grande e obriga a revisar o ADR-0006.
"""
import importlib.util
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.pipeline import Pipeline
from xgboost import XGBClassifier

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BASE = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(BASE / "src" / "preprocessing"))
from pipeline_preprocessamento import (  # noqa: E402
    colunas_feature, construir_preprocessador,
)


def _carregar_modulo_falsificacao():
    """
    Importa 02_teste_falsificacao.py, cujo nome comeca com digito e por isso
    nao e importavel por `import`. Mesmo padrao usado pelos testes do projeto.
    """
    caminho = BASE / "src" / "evaluation" / "02_teste_falsificacao.py"
    spec = importlib.util.spec_from_file_location("teste_falsificacao", caminho)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


FALSIF = _carregar_modulo_falsificacao()
RANDOM_STATE = FALSIF.RANDOM_STATE
ANO_TREINO, ANO_TESTE = FALSIF.ANO_TREINO, FALSIF.ANO_TESTE

N_COMPARACOES = 3
ALPHA = 0.05
ALPHA_CORRIGIDO = ALPHA / N_COMPARACOES

# Cada algoritmo na sua configuracao FORTE, nao na do grid modesto do torneio.
# O objetivo aqui nao e comparar algoritmos entre si (o torneio ja faz isso) --
# e dar a cada um a melhor chance de limpar a barra do baseline. Amarrar a
# mao de um candidato tornaria o "todos perdem" um artefato de configuracao.
CANDIDATOS = {
    "xgboost": dict(
        estimador=XGBClassifier(**FALSIF.PARAMS_XGB),
        nota="configuracao canonica do 02_teste_falsificacao.py (800 arvores, depth 8)",
    ),
    "random_forest": dict(
        # n_jobs=-1 e aceitavel aqui: a media das arvores em predict_proba e
        # uma reducao paralela e NAO e bit-identica (medido 2026-08-30:
        # |diff| ~ 3,3e-16), mas as metricas deste script sao arredondadas em
        # 4 casas e o efeito some. So amplifica onde ha bootstrap/percentil a
        # jusante -- ver a docstring de tests/test_determinismo_execucao.py. O
        # problema de ordem de soma em ponto flutuante e MUITO maior no
        # tree_method="hist" do XGBoost.
        estimador=RandomForestClassifier(
            n_estimators=800, max_depth=12, min_samples_leaf=10,
            class_weight="balanced", random_state=RANDOM_STATE, n_jobs=-1,
        ),
        nota="extremo forte do grid do torneio (800 arvores, depth 12)",
    ),
    "regressao_logistica": dict(
        estimador=LogisticRegression(
            C=1.0, class_weight="balanced", random_state=RANDOM_STATE,
            max_iter=2000,
        ),
        nota="C=1.0, o centro do grid do torneio",
    ),
}


def ic_bootstrap_pareado(y, score_a, score_b, n_boot: int = 2000,
                         alphas: tuple[float, ...] = (0.05,)) -> dict:
    """
    Distribuicao bootstrap da diferenca de AUC, com IC em varios niveis.

    Replica o esquema de `ic_diferenca_auc` do 02_teste_falsificacao.py --
    mesma seed, mesmo pareamento, mesmo descarte de reamostra degenerada -- e
    so acrescenta a possibilidade de pedir mais de um nivel de confianca, que
    e o que a correcao de Bonferroni exige.

    `tests/test_robustez_algoritmo.py` prova que, em alpha=0,05, esta funcao
    devolve exatamente o mesmo intervalo da canonica. Sem esse teste, a copia
    poderia divergir em silencio -- que e o modo de falha que este projeto ja
    pagou uma vez (ADR-0005).
    """
    rng = np.random.default_rng(RANDOM_STATE)
    n = len(y)
    difs = []
    for _ in range(n_boot):
        idx = rng.integers(0, n, n)
        yb = y[idx]
        if yb.min() == yb.max():   # reamostra sem as duas classes
            continue
        difs.append(roc_auc_score(yb, score_a[idx]) - roc_auc_score(yb, score_b[idx]))
    difs = np.array(difs)

    intervalos = {}
    for alpha in alphas:
        lo, hi = np.percentile(difs, [100 * alpha / 2, 100 * (1 - alpha / 2)])
        intervalos[f"ic{100 * (1 - alpha):.6g}"] = {
            "alpha": float(alpha),
            "inferior": float(lo),
            "superior": float(hi),
            "vence": bool(lo > 0),      # supera o baseline com significancia
            "perde": bool(hi < 0),      # PERDE com significancia (nao e empate)
        }

    return {
        "diferenca_observada": float(
            roc_auc_score(y, score_a) - roc_auc_score(y, score_b)),
        "n_teste": int(n),
        "n_bootstrap": int(len(difs)),
        "intervalos": intervalos,
    }


def avaliar_candidato(nome: str, config: dict, treino: pd.DataFrame,
                      teste: pd.DataFrame, feats: list[str],
                      score_baseline: np.ndarray, y: np.ndarray) -> dict:
    pipe = Pipeline([
        ("preprocessador", construir_preprocessador(treino[feats])),
        ("modelo", config["estimador"]),
    ])
    pipe.fit(treino[feats], treino["_y"])
    score = pipe.predict_proba(teste[feats])[:, 1]

    ic = ic_bootstrap_pareado(y, score, score_baseline,
                              alphas=(ALPHA, ALPHA_CORRIGIDO))
    return {
        "nota_configuracao": config["nota"],
        "roc_auc": float(roc_auc_score(y, score)),
        **ic,
    }


def main():
    df = FALSIF.carregar()
    treino = df[df["ano"] == ANO_TREINO]
    teste = df[df["ano"] == ANO_TESTE].copy()
    feats = colunas_feature(df)
    y = teste["_y"].to_numpy()

    # Baseline vem do modulo canonico, nao recalculado aqui (ver docstring).
    baselines = FALSIF.baselines_municipais(df)
    aucs_baseline = {
        nome: float(roc_auc_score(y, serie.loc[teste.index].to_numpy()))
        for nome, serie in baselines.items()
    }
    melhor_nome = max(aucs_baseline, key=lambda k: aucs_baseline[k])
    score_baseline = baselines[melhor_nome].loc[teste.index].to_numpy()
    auc_baseline = aucs_baseline[melhor_nome]

    print("=" * 74)
    print("ROBUSTEZ DO VEREDITO A ESCOLHA DE ALGORITMO")
    print("=" * 74)
    print(f"Split temporal: treino {ANO_TREINO} (n={len(treino):,}) -> "
          f"teste {ANO_TESTE} (n={len(teste):,})".replace(",", "."))
    print(f"Features: {len(feats)}")
    print(f"Melhor baseline municipal: {melhor_nome} (AUC {auc_baseline:.4f})")
    print(f"\nCriterio (ADR-0001 secao 5, declarado antes de rodar): o modelo passa")
    print(f"se a diferenca contra o baseline for positiva com IC inteiramente")
    print(f"acima de zero. Correcao de Bonferroni para {N_COMPARACOES} comparacoes:")
    print(f"alpha {ALPHA} / {N_COMPARACOES} = {ALPHA_CORRIGIDO:.4f} "
          f"(IC de {100 * (1 - ALPHA_CORRIGIDO):.2f}%).")

    resultados = {}
    for nome, config in CANDIDATOS.items():
        print(f"\n--- {nome} ---")
        print(f"    {config['nota']}")
        r = avaliar_candidato(nome, config, treino, teste, feats,
                              score_baseline, y)
        resultados[nome] = r
        ic95 = r["intervalos"][f"ic{100 * (1 - ALPHA):.6g}"]
        icc = r["intervalos"][f"ic{100 * (1 - ALPHA_CORRIGIDO):.6g}"]
        print(f"    AUC {r['roc_auc']:.4f} vs baseline {auc_baseline:.4f}")
        print(f"    Diferenca {r['diferenca_observada']:+.4f}")
        print(f"      IC95%          [{ic95['inferior']:+.4f}, {ic95['superior']:+.4f}]")
        print(f"      IC{100 * (1 - ALPHA_CORRIGIDO):.2f}% (Bonferroni) "
              f"[{icc['inferior']:+.4f}, {icc['superior']:+.4f}]")
        if icc["vence"]:
            print("      >> SUPERA o baseline mesmo apos correcao.")
        elif icc["perde"]:
            print("      >> PERDE do baseline com significancia (nao e empate).")
        else:
            print("      >> Inconclusivo apos correcao: o intervalo cruza o zero.")

    venceram = [n for n, r in resultados.items()
                if r["intervalos"][f"ic{100 * (1 - ALPHA_CORRIGIDO):.6g}"]["vence"]]
    perderam = [n for n, r in resultados.items()
                if r["intervalos"][f"ic{100 * (1 - ALPHA_CORRIGIDO):.6g}"]["perde"]]

    print("\n" + "=" * 74)
    if not venceram and len(perderam) == len(CANDIDATOS):
        veredito = "ROBUSTO — nenhum algoritmo supera o baseline"
        leitura = (
            "Os tres candidatos perdem do melhor baseline municipal com "
            "significancia, apos correcao para comparacoes multiplas. O "
            "veredito do projeto nao depende da escolha de algoritmo: e "
            "limitacao do DADO, nao do metodo. Isso e o que o argumento "
            "estrutural ja previa -- toda feature disponivel e constante "
            "dentro do municipio, entao nenhum modelo consegue separar dois "
            "alunos do mesmo municipio, seja ele linear ou ensemble."
        )
    elif venceram:
        veredito = f"REVISAR — {', '.join(venceram)} supera o baseline"
        leitura = (
            "Pelo menos um algoritmo limpa a barra do ADR-0001 secao 5. Isso "
            "contradiz a conclusao do ADR-0006 e exige revisao antes de "
            "qualquer entrega."
        )
    else:
        veredito = "PARCIAL — nenhum vence, mas nem todos perdem com significancia"
        leitura = (
            "Nenhum candidato supera o baseline, mas algum ficou inconclusivo "
            "apos a correcao. O veredito de derrota se sustenta para os que "
            "perderam; para os demais o dado nao permite afirmar nem negar."
        )
    print(f">> {veredito}")
    print(leitura)

    saida = {
        "pergunta": ("O veredito da falsificacao depende do algoritmo "
                     "escolhido, ou e limitacao do dado?"),
        "desenho": {
            "treino": f"alunos de {ANO_TREINO}",
            "n_treino": int(len(treino)),
            "teste": f"alunos de {ANO_TESTE}",
            "n_teste": int(len(teste)),
            "features": feats,
            "baseline": melhor_nome,
            "auc_baseline": auc_baseline,
            "aucs_todos_baselines": aucs_baseline,
            "baseline_reusado_de": ("src/evaluation/02_teste_falsificacao.py "
                                    "(baselines_municipais) — nao reimplementado"),
        },
        "correcao_comparacoes_multiplas": {
            "metodo": "Bonferroni",
            "n_comparacoes": N_COMPARACOES,
            "alpha_original": ALPHA,
            "alpha_corrigido": ALPHA_CORRIGIDO,
            "por_que": ("3 comparacoes informam UMA decisao (existe algoritmo "
                        "que salva o aluno-nivel?). Sem correcao, a chance de "
                        "um vencer por ruido cresce com o numero de tentativas."),
            "veredito_usa": "o intervalo corrigido",
        },
        "resultados": resultados,
        "veredito": veredito,
        "leitura": leitura,
    }
    destino = BASE / "reports" / "robustez_algoritmo.json"
    destino.write_text(json.dumps(saida, indent=2, ensure_ascii=False),
                       encoding="utf-8")
    print(f"\nGravado: {destino.relative_to(BASE)}")


if __name__ == "__main__":
    main()
