"""
Teste de unidade para src/evaluation/02_teste_falsificacao.py.

POR QUE ESTE ARQUIVO EXISTE
----------------------------
`02_teste_falsificacao.py` decide se o modelo aluno-nível é aprovado ou
reprovado (o veredito mais citado do projeto: ROC-AUC 0,6047 modelo vs
0,6331 baseline, reprovado) e tinha ZERO cobertura de teste de unidade
(achado no mapeamento de 2026-08-30, docs/wayfinder/tech_challenge_fase3/,
item "cobertura de teste desigual"). GATE ML de cobertura mínima
(.claude/rules/dados.md) cobre justamente isso: "3+ funções sem test_*.py".

Cobre as duas funções puras que sustentam o veredito: `recall_no_orcamento`
(métrica operacional real do caso de uso — busca ativa por orçamento) e
`ic_diferenca_auc` (intervalo de confiança que decide se a diferença é
distinguível de ruído amostral — a `AGENTS.md` proíbe proporção sem `n` e
sem intervalo, esta função é o que produz o intervalo).
"""
import importlib.util
from pathlib import Path

import numpy as np

BASE = Path(__file__).resolve().parents[1]

spec = importlib.util.spec_from_file_location(
    "teste_falsificacao", BASE / "src" / "evaluation" / "02_teste_falsificacao.py")
tf = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tf)


def test_recall_no_orcamento_pega_os_k_maiores_scores():
    y = np.array([1, 0, 1, 0, 1, 0, 1, 0])
    score = np.array([0.9, 0.1, 0.2, 0.8, 0.7, 0.6, 0.05, 0.95])
    # ordenado desc: idx 7(0.95,y=0) 0(0.9,y=1) 3(0.8,y=0) 4(0.7,y=1) 5(0.6,y=0)...

    resultado = tf.recall_no_orcamento(y, score, fracao=0.25)  # k=2

    assert resultado["k"] == 2
    # top-2 por score: indices 7 (y=0) e 0 (y=1) -> 1 achado
    assert resultado["achados"] == 1
    assert resultado["precision"] == 0.5


def test_recall_no_orcamento_fracao_maior_aumenta_ou_mantem_recall():
    """Parametro `fracao` variando -> recall so pode subir ou manter (nunca
    cai, e um conjunto crescente de visitados) -- GATE cobertura item 1."""
    rng = np.random.default_rng(1)
    y = rng.integers(0, 2, 200)
    score = rng.uniform(0, 1, 200)

    r_10 = tf.recall_no_orcamento(y, score, fracao=0.10)
    r_50 = tf.recall_no_orcamento(y, score, fracao=0.50)

    assert r_50["recall"] >= r_10["recall"]
    assert r_50["k"] > r_10["k"]


def test_recall_no_orcamento_k_minimo_e_1():
    y = np.array([1, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    score = np.arange(10, dtype=float)

    resultado = tf.recall_no_orcamento(y, score, fracao=0.001)

    assert resultado["k"] == 1  # max(1, round(10 * 0.001)) = max(1, 0)


def test_ic_diferenca_auc_scores_identicos_da_diferenca_zero():
    rng = np.random.default_rng(0)
    y = rng.integers(0, 2, 100)
    score = rng.uniform(0, 1, 100)

    resultado = tf.ic_diferenca_auc(y, score, score, n_boot=200)

    assert resultado["diferenca_observada"] == 0.0
    assert resultado["significativo"] is False  # IC nao pode excluir zero


def test_ic_diferenca_auc_modelo_claramente_melhor_e_significativo():
    """score_a = y perfeito (+ruido minimo), score_b = aleatorio -> diferenca
    de AUC grande e positiva, IC nao deve cruzar zero."""
    rng = np.random.default_rng(2)
    n = 300
    y = rng.integers(0, 2, n)
    score_a = y.astype(float) + rng.normal(0, 0.05, n)  # quase perfeito
    score_b = rng.uniform(0, 1, n)  # aleatorio, sem sinal

    resultado = tf.ic_diferenca_auc(y, score_a, score_b, n_boot=500)

    assert resultado["diferenca_observada"] > 0.3
    assert resultado["ic95_inferior"] > 0
    assert resultado["significativo"] is True


def test_ic_diferenca_auc_e_deterministico_com_mesmo_random_state():
    """RANDOM_STATE fixo no modulo -- duas chamadas com os mesmos dados
    devem reproduzir o mesmo IC (GATE cobertura item 3: fallback/calculo
    nao pode variar em silencio entre execucoes)."""
    rng = np.random.default_rng(3)
    y = rng.integers(0, 2, 150)
    score_a = rng.uniform(0, 1, 150)
    score_b = rng.uniform(0, 1, 150)

    r1 = tf.ic_diferenca_auc(y, score_a, score_b, n_boot=300)
    r2 = tf.ic_diferenca_auc(y, score_a, score_b, n_boot=300)

    assert r1 == r2
