"""
Interpretabilidade via SHAP — e execução dos gates do ADR-0001 §5.

POR QUE ESTE SCRIPT EXISTE
--------------------------
Fecha a última lacuna 🔴 da auditoria do enunciado (Cap. 7.3 do
docs/HANDOFF_RENAN.md) e faz três coisas que nenhum outro script fazia:

  1. Responde 2 das 5 perguntas de negócio do enunciado:
     "Quais fatores mais impactam a alfabetização?" e
     "Quais variáveis possuem maior influência nos modelos?"

  2. VERIFICA os riscos 2 e 7 do Risk Register (Cap. 9.1). Até aqui eles eram
     riscos declarados sem instrumento de verificação:
       - risco 2: `caderno=12` pode ser proxy de necessidade especial
       - risco 7: meta imputada pode virar artefato de "quem teve imputação"

  3. Torna EXECUTÁVEL o checklist de monitoramento do ADR-0001 §5. Ele estava
     escrito como plano e nada o rodava — exatamente o padrão que o avaliador
     da Fase 2 criticou ("o evento chega, é validado, e para ali"). Aqui cada
     item vira um gate que imprime PASSOU / FALHOU.

COMO O SHAP É CALCULADO AQUI
----------------------------
O modelo vive dentro de uma Pipeline (pré-processador + estimador). O SHAP
precisa das features JÁ transformadas, então:
  1. `preprocessador.transform(X)` gera a matriz numérica
  2. `get_feature_names_out()` dá os nomes pós-One-Hot (ex.: `cat__caderno_12`)
  3. TreeExplainer roda sobre o estimador com essa matriz

Manter o nome pós-One-Hot é o que permite olhar `caderno=12` isoladamente, em
vez de só um `caderno` agregado — sem isso o risco 2 seria inverificável.

ATENÇÃO: roda sobre o snapshot disponível. No `--local-only` não existem
território/socioeconômico/meta, então os gates que dependem dessas features
são reportados como NÃO APLICÁVEL, nunca como aprovados.
"""
import json
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import matplotlib
matplotlib.use("Agg")  # sem display: salva em arquivo
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import shap
from sklearn.metrics import (
    f1_score, precision_score, recall_score, roc_auc_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from xgboost import XGBClassifier

BASE = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(BASE / "src" / "preprocessing"))
from pipeline_preprocessamento import (  # noqa: E402
    COLUNA_TARGET, colunas_feature, construir_preprocessador, descrever_features,
    validar_cobertura_colunas,
)

RANDOM_STATE = 42
TEST_SIZE = 0.2
TOP_N = 5  # o "top-5" citado no checklist do ADR-0001 §5

# Modelo forte validado em 00c_teste_residuo_modelo_forte.py, canônico pra
# fase 3 do recomeço pedagógico (2026-08-22). Split temporal 2023/2024,
# sem sinal incremental de features de aluno vs baseline municipal.
# Se o tournament for re-rodado, este SHAP roda sobre o modelo forte de
# referência, não o vencedor do tournament — mantém metodologia consistente.
PARAMS_XGB = dict(
    n_estimators=800, max_depth=8, learning_rate=0.03,
    subsample=0.8, colsample_bytree=0.8, min_child_weight=3,
    reg_lambda=1.0, random_state=RANDOM_STATE, eval_metric="logloss",
    tree_method="hist", n_jobs=-1,
)

# Prefixos usados para classificar features nos gates do ADR-0001 §5.
FEATURES_TERRITORIO = ("populacao_total", "gasto_por_habitante_educacao", "sigla_uf")
FEATURES_ARTEFATO = ("possui_hist_escola_t1", "possui_hist_municipio_t1",
                     "meta_is_imputada")


def carregar_snapshot() -> pd.DataFrame:
    df = pd.read_parquet(BASE / "data" / "snapshot_modelagem.parquet")
    # Coluna nova no snapshot para aqui, em vez de sair do modelo em silêncio.
    validar_cobertura_colunas(df)
    df[COLUNA_TARGET] = (df[COLUNA_TARGET] == "Não").astype(int)  # 1 = risco
    return df


def nome_original(nome_transformado: str) -> str:
    """`cat__caderno_12` -> `caderno`. Usado para agregar One-Hot por feature."""
    sem_prefixo = nome_transformado.split("__", 1)[-1]
    for candidata in sorted(
        ["absenteismo_hist_escola_t1", "absenteismo_hist_municipio_t1",
         "n_alunos_hist_escola_t1", "n_alunos_hist_municipio_t1", "populacao_total",
         "gasto_por_habitante_educacao", "meta_alfabetizacao_2024_imputada",
         "caderno", "rede", "sigla_uf", "possui_hist_escola_t1",
         "possui_hist_municipio_t1", "meta_is_imputada"],
        key=len, reverse=True,
    ):
        if sem_prefixo.startswith(candidata):
            return candidata
    return sem_prefixo


def treinar(X_train, y_train) -> Pipeline:
    pipe = Pipeline([
        ("preprocessador", construir_preprocessador(X_train)),
        ("modelo", XGBClassifier(**PARAMS_XGB)),
    ])
    pipe.fit(X_train, y_train)
    return pipe


def calcular_shap(pipe: Pipeline, X_test: pd.DataFrame):
    pre = pipe.named_steps["preprocessador"]
    Xt = pre.transform(X_test)
    if hasattr(Xt, "toarray"):
        Xt = Xt.toarray()
    nomes = list(pre.get_feature_names_out())

    explainer = shap.TreeExplainer(pipe.named_steps["modelo"])
    valores = explainer.shap_values(Xt)
    valores = np.asarray(valores)
    if valores.ndim == 3:  # algumas versões devolvem (n, features, classes)
        valores = valores[..., -1]
    return valores, Xt, nomes


def salvar_graficos(valores, Xt, nomes, destino: Path):
    destino.mkdir(parents=True, exist_ok=True)

    shap.summary_plot(valores, Xt, feature_names=nomes, plot_type="bar", show=False)
    plt.title("Influência média de cada variável (|SHAP| médio)")
    plt.tight_layout()
    plt.savefig(destino / "shap_importancia_global.png", dpi=130)
    plt.close()

    shap.summary_plot(valores, Xt, feature_names=nomes, show=False)
    plt.title("Direção do efeito por aluno (vermelho = valor alto da variável)")
    plt.tight_layout()
    plt.savefig(destino / "shap_beeswarm.png", dpi=130)
    plt.close()

    return ["shap_importancia_global.png", "shap_beeswarm.png"]


def metricas(pipe, X_test, y_test) -> dict:
    y_pred = pipe.predict(X_test)
    y_proba = pipe.predict_proba(X_test)[:, 1]
    return {
        "recall": float(recall_score(y_test, y_pred)),
        "precision": float(precision_score(y_test, y_pred, zero_division=0)),
        "f1": float(f1_score(y_test, y_pred)),
        "roc_auc": float(roc_auc_score(y_test, y_proba)),
    }


def teste_ablacao(feature, X_train, y_train, X_test, y_test, base_metricas) -> dict:
    """
    Retreina o mesmo modelo SEM a feature dominante e compara.

    Por que isto importa: descobrir que uma feature concentra 70% da influência
    não diz, sozinho, o que fazer. A ablação responde a pergunta prática — o
    modelo depende dela porque ela carrega sinal real, ou porque não há mais
    nada? Se o desempenho quase não cair, a feature é dispensável e tirá-la
    torna o modelo mais defensável. Se despencar, o modelo não tem substância
    própria, e isso é um achado ainda mais importante de reportar.
    """
    Xtr = X_train.drop(columns=[feature])
    Xte = X_test.drop(columns=[feature])
    pipe = Pipeline([
        ("preprocessador", construir_preprocessador(Xtr)),
        ("modelo", XGBClassifier(**PARAMS_XGB)),
    ])
    pipe.fit(Xtr, y_train)
    sem = metricas(pipe, Xte, y_test)
    return {
        "feature_removida": feature,
        "com_a_feature": base_metricas,
        "sem_a_feature": sem,
        "delta": {k: round(sem[k] - base_metricas[k], 4) for k in sem},
    }


def rodar_gates(ranking_detalhado, ranking_agregado, df) -> list[dict]:
    """
    Executa o checklist do ADR-0001 §5 que dependia de SHAP.

    Cada gate devolve status PASSOU / FALHOU / NAO_APLICAVEL. NAO_APLICAVEL
    nunca deve ser lido como aprovado — é lacuna, não sucesso.
    """
    gates = []
    top_n_agregado = [nome for nome, _ in ranking_agregado[:TOP_N]]

    # Gate 1 (ADR-0001 §5, cenário 1): território/socioeconômico não pode
    # dominar sozinho, senão o modelo é o baseline municipal disfarçado.
    territorio_presente = [c for c in FEATURES_TERRITORIO if c in df.columns]
    if not territorio_presente:
        gates.append({
            "gate": "territorio_nao_domina_o_top5",
            "status": "NAO_APLICAVEL",
            "detalhe": ("Snapshot --local-only não tem território/socioeconômico. "
                        "Este gate só pode ser avaliado depois do --full."),
        })
    else:
        n_territorio = sum(1 for f in top_n_agregado if f in FEATURES_TERRITORIO)
        gates.append({
            "gate": "territorio_nao_domina_o_top5",
            "status": "FALHOU" if n_territorio >= TOP_N - 1 else "PASSOU",
            "detalhe": (f"{n_territorio} de {TOP_N} do top-5 são território/"
                        f"socioeconômico. Top-5: {top_n_agregado}"),
        })

    # Gate 2 (ADR-0001 §5, cenário 3): features que marcam DISPONIBILIDADE de
    # dado não podem carregar influência relevante — se carregam, o modelo lê o
    # artefato de imputação, não sinal do aluno. Cobre o risco 7.
    #
    # CORREÇÃO DE CRITÉRIO (2026-08-18): o ADR-0001 escreveu este gate como
    # "possui_historico_t1 fora do top-5 SHAP". Com o snapshot --local-only o
    # modelo tem só 5 features — top-5 é TODO o modelo, então o critério por
    # posição reprova sempre, sem informar nada. Trocado por participação na
    # influência (limiar 10%), que funciona com qualquer número de features. A
    # posição vira contexto, não veredito.
    total_infl = sum(v for _, v in ranking_agregado) or 1.0
    flags = {f: dict(ranking_agregado).get(f, 0.0) / total_infl
             for f in FEATURES_ARTEFATO if f in dict(ranking_agregado)}
    acima = {f: p for f, p in flags.items() if p >= 0.10}
    if not flags:
        gates.append({"gate": "flags_de_imputacao_sem_influencia_relevante",
                      "status": "NAO_APLICAVEL",
                      "detalhe": "Nenhuma flag de disponibilidade de dado no modelo."})
    else:
        detalhe = ", ".join(f"{f}={p:.1%}" for f, p in flags.items())
        gates.append({
            "gate": "flags_de_imputacao_sem_influencia_relevante",
            "status": "FALHOU" if acima else "PASSOU",
            "detalhe": (f"Participação na influência: {detalhe}. Limiar: 10%. "
                        f"(Critério por posição do ADR-0001 não discrimina aqui: "
                        f"o modelo tem {len(ranking_agregado)} features, "
                        f"então top-{TOP_N} seria o modelo inteiro.)"),
        })

    # Gate 4 (novo, 2026-08-18): nenhuma feature isolada deveria concentrar a
    # maior parte da influência — e menos ainda uma que não seja característica
    # acionável do aluno. Não estava no ADR-0001 porque o problema só apareceu
    # quando o SHAP foi calculado.
    if ranking_agregado:
        lider, v_lider = ranking_agregado[0]
        share = v_lider / total_infl
        gates.append({
            "gate": "nenhuma_feature_isolada_domina",
            "status": "FALHOU" if share >= 0.50 else "PASSOU",
            "detalhe": (f"`{lider}` concentra {share:.1%} da influência. "
                        f"Limiar: 50%."),
        })

    # Gate 3 (risco 2 do Risk Register): caderno=12 não pode dominar sobre as
    # outras categorias do mesmo caderno. Se dominar, a suspeita de proxy de
    # necessidade especial ganha peso e a feature precisa de decisão explícita.
    cadernos = {n: v for n, v in ranking_detalhado.items() if nome_original(n) == "caderno"}
    if not cadernos:
        gates.append({
            "gate": "caderno_12_nao_domina",
            "status": "NAO_APLICAVEL",
            "detalhe": "Feature `caderno` não está no modelo.",
        })
    else:
        c12 = next((v for n, v in cadernos.items() if n.endswith("_12")), None)
        outros = [v for n, v in cadernos.items() if not n.endswith("_12")]
        if c12 is None:
            gates.append({"gate": "caderno_12_nao_domina", "status": "NAO_APLICAVEL",
                          "detalhe": "Categoria 12 ausente neste split."})
        else:
            media_outros = float(np.mean(outros)) if outros else 0.0
            razao = c12 / media_outros if media_outros > 0 else float("inf")
            gates.append({
                "gate": "caderno_12_nao_domina",
                "status": "FALHOU" if razao >= 2.0 else "PASSOU",
                "detalhe": (f"|SHAP| de caderno=12 é {razao:.2f}x a média das outras "
                            f"categorias de caderno ({c12:.4f} vs {media_outros:.4f}). "
                            f"Limiar de alerta: 2.0x"),
            })
    return gates


def main():
    df = carregar_snapshot()
    X, y = df[colunas_feature(df)], df[COLUNA_TARGET]
    print(f"Snapshot: {len(df)} linhas | classe de risco ('Não') = {y.mean():.1%}")
    print(descrever_features(df))

    # Mesmo split do tournament (mesmo random_state) — o SHAP precisa explicar
    # o modelo nas mesmas condições em que ele foi escolhido.
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=TEST_SIZE, stratify=y, random_state=RANDOM_STATE,
    )
    pipe = treinar(X_train, y_train)
    valores, Xt, nomes = calcular_shap(pipe, X_test)

    media_abs = np.abs(valores).mean(axis=0)
    ranking_detalhado = dict(sorted(zip(nomes, media_abs.round(5)),
                                    key=lambda kv: -kv[1]))

    agregado: dict[str, float] = {}
    for nome, v in zip(nomes, media_abs):
        agregado[nome_original(nome)] = agregado.get(nome_original(nome), 0.0) + float(v)
    ranking_agregado = sorted(agregado.items(), key=lambda kv: -kv[1])

    print("\n" + "=" * 72)
    print("INFLUENCIA POR VARIAVEL (|SHAP| medio, One-Hot somado por variavel)")
    print("=" * 72)
    print("Responde: 'Quais variaveis possuem maior influencia nos modelos?'\n")
    total = sum(v for _, v in ranking_agregado) or 1.0
    for i, (nome, v) in enumerate(ranking_agregado, 1):
        print(f"{i:>2}. {nome:<34}{v:>9.4f}   ({v / total:>5.1%} da influencia)")

    print("\n" + "=" * 72)
    print("DETALHE POR CATEGORIA (pos One-Hot)")
    print("=" * 72)
    for nome, v in ranking_detalhado.items():
        print(f"    {nome:<38}{v:>9.4f}")

    print("\n" + "=" * 72)
    print("GATES DO ADR-0001 SECAO 5 (o checklist que ninguem executava)")
    print("=" * 72)
    gates = rodar_gates(ranking_detalhado, ranking_agregado, df)
    simbolo = {"PASSOU": "[OK]  ", "FALHOU": "[FALHA]", "NAO_APLICAVEL": "[N/A] "}
    for g in gates:
        print(f"{simbolo[g['status']]} {g['gate']}")
        print(f"        {g['detalhe']}")

    # Ablação: só faz sentido se alguma feature domina de fato.
    ablacao = None
    lider, v_lider = ranking_agregado[0]
    if v_lider / (sum(v for _, v in ranking_agregado) or 1.0) >= 0.50:
        print(chr(10) + "=" * 72)
        print(f"TESTE DE ABLACAO: o modelo sem `{lider}`")
        print("=" * 72)
        base = metricas(pipe, X_test, y_test)
        ablacao = teste_ablacao(lider, X_train, y_train, X_test, y_test, base)
        print(f"{'metrica':<12}{'com':>10}{'sem':>10}{'delta':>10}")
        print("-" * 42)
        for k in ("recall", "precision", "f1", "roc_auc"):
            print(f"{k:<12}{ablacao['com_a_feature'][k]:>10.3f}"
                  f"{ablacao['sem_a_feature'][k]:>10.3f}"
                  f"{ablacao['delta'][k]:>+10.3f}")

    graficos = salvar_graficos(valores, Xt, nomes, BASE / "images")
    print(f"\nGraficos salvos em images/: {', '.join(graficos)}")

    saida = {
        "contexto": {
            "modelo_explicado": "XGBoost (vencedor do tournament)",
            "hiperparametros": {k: str(v) for k, v in PARAMS_XGB.items()},
            "snapshot": "local-only" if "populacao_total" not in df.columns else "full",
            "n_explicado": int(len(X_test)),
            "aviso": ("Metrica de influencia = |SHAP| medio. Mede o quanto a "
                      "variavel move a predicao, NAO se o efeito e bom ou ruim."),
        },
        "influencia_por_variavel": {k: float(v) for k, v in ranking_agregado},
        "influencia_por_categoria": {k: float(v) for k, v in ranking_detalhado.items()},
        "gates_adr0001_seccao5": gates,
        "teste_ablacao": ablacao,
        "graficos": graficos,
    }
    out = BASE / "reports" / "shap_interpretabilidade.json"
    out.write_text(json.dumps(saida, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Relatorio salvo em {out}")


if __name__ == "__main__":
    main()
