"""
Guarda contra divergencia silenciosa entre o bootstrap do
04_robustez_algoritmo.py e o canonico do 02_teste_falsificacao.py.

POR QUE ESTE ARQUIVO EXISTE
----------------------------
`04_robustez_algoritmo.py` precisa de intervalo de confianca em mais de um
nivel (95% e o corrigido por Bonferroni), e a funcao canonica
`ic_diferenca_auc` fixa 95%. Para nao mexer no script que produz o veredito
oficial do projeto, o bootstrap foi copiado com o parametro a mais.

Copia e o comeco de divergencia. E este projeto ja pagou uma vez por isso: o
ADR-0005 documenta um baseline calculado em separado que divergiu da regua
canonica e inflou o ganho reportado de +0,027 para +0,245 — numero que passou
por revisao, README e ADR antes de alguem notar.

Entao a copia so e aceitavel com um teste que prove, contra dado real, que ela
reproduz a original onde as duas se sobrepoem (alpha = 0,05). Se alguem mudar
o esquema de reamostragem, a seed ou o tratamento de reamostra degenerada em
um dos dois arquivos, este teste reprova.
"""
import importlib.util
from pathlib import Path

import numpy as np
import pytest

BASE = Path(__file__).resolve().parents[1]


def _carregar(nome_modulo: str, caminho_relativo: str):
    spec = importlib.util.spec_from_file_location(
        nome_modulo, BASE / caminho_relativo)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


@pytest.fixture(scope="module")
def falsif():
    return _carregar("teste_falsificacao",
                     "src/evaluation/02_teste_falsificacao.py")


@pytest.fixture(scope="module")
def robustez():
    return _carregar("robustez_algoritmo",
                     "src/evaluation/04_robustez_algoritmo.py")


@pytest.fixture(scope="module")
def dado_sintetico():
    """
    Dois scores com separacao diferente sobre o mesmo y, para a diferenca de
    AUC nao ser zero — um teste onde a diferenca e nula passaria mesmo com os
    dois bootstraps errados do mesmo jeito.
    """
    rng = np.random.default_rng(7)
    n = 600
    y = rng.integers(0, 2, n)
    score_a = y * 0.6 + rng.normal(0, 1.0, n)   # separa melhor
    score_b = y * 0.2 + rng.normal(0, 1.0, n)   # separa pior
    return y, score_a, score_b


def test_bootstrap_reproduz_a_canonica_em_95(falsif, robustez, dado_sintetico):
    """O mesmo input tem que dar o mesmo intervalo nos dois arquivos."""
    y, a, b = dado_sintetico
    canonico = falsif.ic_diferenca_auc(y, a, b, n_boot=300)
    copia = robustez.ic_bootstrap_pareado(y, a, b, n_boot=300, alphas=(0.05,))

    ic95 = copia["intervalos"]["ic95"]
    assert copia["diferenca_observada"] == pytest.approx(
        canonico["diferenca_observada"])
    assert copia["n_bootstrap"] == canonico["n_bootstrap"]
    assert ic95["inferior"] == pytest.approx(canonico["ic95_inferior"])
    assert ic95["superior"] == pytest.approx(canonico["ic95_superior"])


def test_significancia_bate_com_a_canonica(falsif, robustez, dado_sintetico):
    """`vence` da copia tem que significar o mesmo que `significativo` da original."""
    y, a, b = dado_sintetico
    canonico = falsif.ic_diferenca_auc(y, a, b, n_boot=300)
    copia = robustez.ic_bootstrap_pareado(y, a, b, n_boot=300, alphas=(0.05,))
    assert copia["intervalos"]["ic95"]["vence"] == canonico["significativo"]


def test_bonferroni_alarga_o_intervalo(robustez, dado_sintetico):
    """
    Correcao para comparacoes multiplas so faz sentido se for MAIS
    conservadora. Intervalo corrigido mais estreito seria erro de sinal no
    calculo do percentil — e passaria despercebido, porque o numero continua
    saindo bonito.
    """
    y, a, b = dado_sintetico
    r = robustez.ic_bootstrap_pareado(y, a, b, n_boot=300,
                                      alphas=(0.05, 0.05 / 3))
    largo = r["intervalos"]["ic98.3333"]
    estreito = r["intervalos"]["ic95"]
    assert largo["inferior"] <= estreito["inferior"]
    assert largo["superior"] >= estreito["superior"]


def test_vence_e_perde_sao_mutuamente_exclusivos(robustez, dado_sintetico):
    """
    Um intervalo nao pode estar acima e abaixo de zero ao mesmo tempo. Se os
    dois viessem True, o veredito do script leria a primeira condicao e
    ignoraria a contradicao em silencio.
    """
    y, a, b = dado_sintetico
    r = robustez.ic_bootstrap_pareado(y, a, b, n_boot=300,
                                      alphas=(0.05, 0.05 / 3))
    for ic in r["intervalos"].values():
        assert not (ic["vence"] and ic["perde"])


def test_perde_detecta_intervalo_inteiramente_negativo(robustez, dado_sintetico):
    """
    O caso que o projeto de fato tem: modelo pior que o baseline. A versao
    antiga do console imprimia "cruza o zero" (empate) mesmo com o intervalo
    inteiramente negativo — perda significativa lida como empate.
    """
    y, a, b = dado_sintetico
    # Ordem invertida: `b` separa pior, entao b - a e negativo.
    r = robustez.ic_bootstrap_pareado(y, b, a, n_boot=300, alphas=(0.05,))
    ic = r["intervalos"]["ic95"]
    assert r["diferenca_observada"] < 0
    assert ic["superior"] < 0
    assert ic["perde"] is True
    assert ic["vence"] is False
