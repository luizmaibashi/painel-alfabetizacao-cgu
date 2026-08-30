"""Testes das garantias estatísticas do backtest prospectivo."""
import importlib.util
from pathlib import Path

import numpy as np
from sklearn.metrics import roc_auc_score


ARQUIVO = Path(__file__).resolve().parents[1] / "src" / "evaluation" / "05_backtest_prospectivo_2025.py"
ESPEC = importlib.util.spec_from_file_location("backtest_2025", ARQUIVO)
MODULO = importlib.util.module_from_spec(ESPEC)
ESPEC.loader.exec_module(MODULO)


def test_auc_por_pesos_respeita_empates_e_equivale_a_amostra_expandida():
    y = np.array([0, 1, 0, 1, 1])
    scores = np.array([0.2, 0.2, 0.8, 0.9, 0.9])
    pesos = np.array([[2, 1, 3, 2, 1], [1, 2, 1, 1, 3]])

    esperado = []
    for linha in pesos:
        indices = np.repeat(np.arange(len(y)), linha)
        esperado.append(roc_auc_score(y[indices], scores[indices]))

    obtido = MODULO._auc_por_pesos(y, scores, pesos)
    np.testing.assert_allclose(obtido, esperado)


def test_bootstrap_ganho_e_deterministico_e_pareado():
    y = np.array([0, 1, 0, 1, 0, 1, 0, 1])
    modelo = np.array([0.1, 0.9, 0.3, 0.8, 0.2, 0.7, 0.4, 0.6])
    baseline = np.array([0.4, 0.6, 0.3, 0.7, 0.5, 0.5, 0.2, 0.8])

    primeiro = MODULO.bootstrap_ganho(y, modelo, baseline, n_boot=250, seed=7)
    segundo = MODULO.bootstrap_ganho(y, modelo, baseline, n_boot=250, seed=7)

    assert primeiro == segundo
    assert primeiro[0] <= primeiro[1]
