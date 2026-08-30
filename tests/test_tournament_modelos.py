"""
Teste de unidade para src/modeling/02_tournament_modelos.py.

POR QUE ESTE ARQUIVO EXISTE
----------------------------
`02_tournament_modelos.py` decide qual algoritmo vence o torneio e tinha
ZERO cobertura de teste de unidade (achado no mapeamento de 2026-08-30,
docs/wayfinder/tech_challenge_fase3/, item "cobertura de teste desigual").
GATE ML de cobertura mínima (.claude/rules/dados.md) cobre justamente isso:
"3+ funções sem test_*.py".

Cobre as duas funções puras (sem I/O, sem fit de modelo) que decidem o
resultado reportado: `avaliar` (métricas no threshold escolhido) e
`limiar_por_custo` (escolha do threshold via F-beta sobre OOF).
"""
import importlib.util
from pathlib import Path

import numpy as np

BASE = Path(__file__).resolve().parents[1]

spec = importlib.util.spec_from_file_location(
    "tournament_modelos", BASE / "src" / "modeling" / "02_tournament_modelos.py")
tm = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tm)


class _PipelineFake:
    """Substitui um sklearn Pipeline treinado: devolve probabilidades fixas
    passadas no construtor, para testar `avaliar()` isolado de qualquer fit
    real."""
    def __init__(self, proba_classe_1):
        self._proba = np.asarray(proba_classe_1, dtype=float)

    def predict_proba(self, X_test):
        return np.column_stack([1 - self._proba, self._proba])


def test_avaliar_threshold_default_bate_com_predict_proba_05():
    y_test = np.array([1, 0, 1, 0, 1])
    proba = np.array([0.9, 0.1, 0.6, 0.4, 0.51])
    pipeline = _PipelineFake(proba)

    resultado = tm.avaliar(pipeline, X_test=None, y_test=y_test)

    assert resultado["threshold"] == 0.5
    # y_pred = [1, 0, 1, 0, 1] -- todos corretos
    assert resultado["recall"] == 1.0
    assert resultado["precision"] == 1.0
    assert resultado["matriz_confusao"] == [[2, 0], [0, 3]]


def test_avaliar_threshold_diferente_muda_matriz_confusao():
    """Parametro `threshold` variando -> saida varia (GATE cobertura, item 1
    do checklist dados.md)."""
    y_test = np.array([1, 0, 1, 0, 1])
    proba = np.array([0.9, 0.1, 0.6, 0.4, 0.45])
    pipeline = _PipelineFake(proba)

    resultado_05 = tm.avaliar(pipeline, X_test=None, y_test=y_test, threshold=0.5)
    resultado_04 = tm.avaliar(pipeline, X_test=None, y_test=y_test, threshold=0.40)

    # Com threshold 0,40 o quinto caso (proba=0,45) vira positivo -- recall sobe
    assert resultado_04["recall"] > resultado_05["recall"]


def test_limiar_por_custo_prefere_threshold_baixo_quando_recall_domina():
    """beta=2 pondera Recall 4x mais que Precision -- threshold otimo deve
    cair abaixo de 0,5 quando marcar mais gente como risco aumenta recall
    sem destruir precision."""
    rng = np.random.default_rng(42)
    y_train = np.array([1] * 30 + [0] * 70)
    # proba_oof correlacionada com y mas com ruido -- classe 1 tende a ter
    # proba mais alta, mas nao perfeitamente separavel
    proba_oof = np.concatenate([
        rng.uniform(0.3, 0.9, 30),   # classe 1
        rng.uniform(0.0, 0.6, 70),   # classe 0
    ])

    resultado = tm.limiar_por_custo(proba_oof, y_train, beta=2.0)

    assert 0.0 < resultado["threshold_escolhido"] < 1.0
    assert resultado["threshold_default_sklearn"] == 0.5
    assert "F2" in resultado["criterio"]


def test_limiar_por_custo_beta_maior_pondera_mais_recall():
    """beta maior -> Recall pesa mais -> threshold escolhido nao deve subir
    (mesma direcao ou mais baixo, nunca mais alto que um beta menor)."""
    rng = np.random.default_rng(7)
    y_train = np.array([1] * 30 + [0] * 70)
    proba_oof = np.concatenate([
        rng.uniform(0.3, 0.9, 30),
        rng.uniform(0.0, 0.6, 70),
    ])

    r_beta1 = tm.limiar_por_custo(proba_oof, y_train, beta=1.0)
    r_beta4 = tm.limiar_por_custo(proba_oof, y_train, beta=4.0)

    assert r_beta4["threshold_escolhido"] <= r_beta1["threshold_escolhido"] + 1e-9
