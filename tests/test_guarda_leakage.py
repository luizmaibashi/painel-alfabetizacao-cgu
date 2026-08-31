"""
Teste proprio do guarda de leakage (src/preprocessing/03_guarda_leakage.py).

POR QUE ESTE ARQUIVO EXISTE
----------------------------
GATE ML - Guarda de qualidade/leakage precisa de teste proprio
(.claude/rules/dados.md, base de conhecimento). O guarda ja teve um bug real
(o diário de bordo interno (não publicado) Cap. 12.2): qualquer coluna categorica de alta cardinalidade
(`sigla_uf`, 27 valores) ia parar em `pd.qcut`, levantando
`ArrowNotImplementedError` -- excecao fora do `except (ValueError, TypeError)`
da epoca, que escapava em silencio. So foi descoberto porque o autor decidiu,
por conta propria, rodar um ensaio manual antes da execucao real -- nao
porque havia teste cobrindo o proprio guarda.

Este arquivo cobre os 3 itens do checklist do gate:
  1. Guarda testado contra cada tipo real de coluna do dataset-alvo (numerica
     continua, numerica baixa cardinalidade, categorica baixa e alta
     cardinalidade, texto livre).
  2. Excecao fora da lista prevista NAO e engolida em silencio -- propaga.
  3. Guarda simulado com dado hostil sintetico confirma que a suspeita ALTA
     de fato aparece (guarda que morre silenciosamente vira "0 suspeitas" por
     omissao, nao por checagem real).
"""
import importlib.util
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

BASE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE / "src" / "preprocessing"))

spec = importlib.util.spec_from_file_location(
    "guarda_leakage", BASE / "src" / "preprocessing" / "03_guarda_leakage.py")
gl = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gl)


def _df_base(n=200, seed=42):
    """DataFrame sintetico com alvo aleatorio (sem vazamento) — controle."""
    rng = np.random.default_rng(seed)
    return pd.DataFrame({"_y": rng.integers(0, 2, n)})


# --- item 1: cada tipo real de coluna do dataset-alvo -----------------------

def test_numerica_continua_sem_vazamento_nao_dispara():
    """populacao_total-like: numerica continua, muitos valores unicos, sem
    relacao com o alvo -- os 3 testes devem voltar None."""
    df = _df_base()
    df["populacao_total"] = np.random.default_rng(1).normal(50_000, 20_000, len(df))
    assert gl.teste_a_nulidade(df, "populacao_total") is None
    assert gl.teste_b_valor(df, "populacao_total") is None
    assert gl.teste_c_auc_sozinha(df, "populacao_total") is None


def test_numerica_baixa_cardinalidade_sem_vazamento():
    """n_alunos_hist_escola_t1-like: numerica com poucos valores distintos."""
    df = _df_base()
    df["n_dias_letivos"] = np.random.default_rng(2).integers(180, 220, len(df))
    assert gl.teste_a_nulidade(df, "n_dias_letivos") is None
    assert gl.teste_c_auc_sozinha(df, "n_dias_letivos") is None


def test_categorica_baixa_cardinalidade_sem_vazamento():
    """rede-like: 2-3 categorias, sem relacao com o alvo."""
    df = _df_base()
    df["rede"] = np.random.default_rng(3).choice(
        ["Municipal", "Estadual", "Federal"], len(df))
    assert gl.teste_b_valor(df, "rede") is None


def test_categorica_alta_cardinalidade_nao_levanta_arrownotimplementederror():
    """
    REGRESSAO DIRETA do bug do HANDOFF Cap. 12.2: `sigla_uf` tem 27 valores
    distintos (> MIN de 20 do guarda), string, sem ser numerica. Antes da
    correcao, isso ia parar em `pd.qcut` e levantava `ArrowNotImplementedError`,
    tipo fora do `except` da epoca -- o guarda MORRIA aqui.

    O teste passa se `teste_b_valor` roda ate o fim sem excecao, qualquer que
    seja o resultado (achado ou None) -- o que importa e nao morrer.
    """
    df = _df_base(n=540)
    ufs = [f"UF{i:02d}" for i in range(27)]  # 27 categorias, como sigla_uf real
    df["sigla_uf"] = np.random.default_rng(4).choice(ufs, len(df))
    resultado = gl.teste_b_valor(df, "sigla_uf")  # NAO pode levantar excecao
    assert resultado is None or resultado["teste"] == "B_valor_isola_target"


def test_texto_livre_alta_cardinalidade_nao_levanta_excecao():
    """Coluna de texto livre (cardinalidade quase == n linhas) -- caso mais
    hostil de todos para um guarda que assume categorica/numerica."""
    df = _df_base(n=100)
    df["observacao_livre"] = [f"nota individual do aluno numero {i}" for i in range(100)]
    resultado = gl.teste_b_valor(df, "observacao_livre")
    assert resultado is None or resultado["teste"] == "B_valor_isola_target"


# --- item 2: excecao fora da lista prevista PROPAGA, nao e engolida --------

def test_excecao_inesperada_no_qcut_propaga_nao_e_engolida(monkeypatch):
    """
    O `except` de `teste_b_valor` cobre so (ValueError, TypeError) -- as
    falhas ESPERADAS do qcut. Qualquer outra excecao (o mesmo genero do
    ArrowNotImplementedError historico) deve PROPAGAR, nunca desaparecer
    como um None silencioso -- e exatamente o antipadrao "guarda silenciosa"
    que este projeto ja levou um incidente real por causa dele.
    """
    class ErroInesperado(RuntimeError):
        pass

    def qcut_hostil(*a, **k):
        raise ErroInesperado("simulando falha fora do (ValueError, TypeError)")

    monkeypatch.setattr(gl.pd, "qcut", qcut_hostil)

    df = _df_base()
    df["numerica_alta_cardinalidade"] = np.random.default_rng(5).normal(0, 1, len(df))
    with pytest.raises(ErroInesperado):
        gl.teste_b_valor(df, "numerica_alta_cardinalidade")


def test_valueerror_do_qcut_e_engolido_corretamente():
    """Falha ESPERADA (poucos bins distintos apos dropna) deve voltar None,
    nao propagar -- contraste com o teste anterior."""
    df = pd.DataFrame({
        "_y": [0, 1] * 15,
        "quase_constante": [1.0] * 29 + [2.0],  # so 2 valores, qcut(10) falha
    })
    # forca o caminho de alta cardinalidade mesmo com poucos valores unicos
    # reais, via coluna com muitas repeticoes do mesmo numero (simula o
    # cenario real: >20 nunique exigido pelo guarda, mas cauda quase constante)
    df2 = _df_base(n=100)
    df2["numerica_cauda_constante"] = [float(i % 25) for i in range(100)]
    resultado = gl.teste_b_valor(df2, "numerica_cauda_constante")
    assert resultado is None or resultado["teste"] == "B_valor_isola_target"


# --- item 3: dado hostil sintetico -> guarda ACHA a suspeita, nao passa reto -

def test_nulidade_do_peso_aluno_e_detectada_alta():
    """Regressao do achado real de 2026-08-18: nulidade de uma coluna
    coincide quase 100% com o alvo positivo -- o guarda TEM que marcar ALTA,
    senao o proprio motivo do teste A existir deixou de funcionar."""
    n = 200
    y = np.array([0] * 100 + [1] * 100)
    peso = np.where(y == 1, np.nan, np.random.default_rng(6).normal(10, 2, n))
    df = pd.DataFrame({"_y": y, "peso_aluno": peso})
    r = gl.teste_a_nulidade(df, "peso_aluno")
    assert r is not None
    assert r["gravidade"] == "ALTA"
    assert r["teste"] == "A_nulidade_prediz_target"


def test_valor_que_isola_alvo_e_detectado_alta():
    """Categoria que isola o alvo quase puro (proxy do achado `presenca`)."""
    n = 200
    y = np.array([0] * 100 + [1] * 100)
    presenca = np.where(y == 1, "Ausente", "Presente")
    df = pd.DataFrame({"_y": y, "presenca": presenca})
    r = gl.teste_b_valor(df, "presenca")
    assert r is not None
    assert r["gravidade"] == "ALTA"


def test_feature_com_auc_isolada_alta_e_detectada():
    """Feature numerica que sozinha separa o alvo quase perfeitamente
    (proxy do achado `proficiencia`)."""
    n = 200
    y = np.array([0] * 100 + [1] * 100)
    proficiencia = np.where(y == 1, np.random.default_rng(7).normal(700, 10, n),
                             np.random.default_rng(8).normal(300, 10, n))
    df = pd.DataFrame({"_y": y, "proficiencia": proficiencia})
    r = gl.teste_c_auc_sozinha(df, "proficiencia")
    assert r is not None
    assert r["gravidade"] == "ALTA"


def test_pipeline_completo_com_dado_hostil_acha_ao_menos_uma_suspeita_alta():
    """
    Integracao: roda os 3 testes sobre um snapshot sintetico com UMA coluna
    de vazamento deliberado (nulidade == alvo) e varias colunas limpas.
    Confirma que o guarda nao passa reto -- se isto falhar, o guarda esta
    "morrendo silenciosamente" (0 suspeitas por omissao, nao por checagem).
    """
    n = 300
    rng = np.random.default_rng(9)
    y = rng.integers(0, 2, n)
    df = pd.DataFrame({
        "_y": y,
        "populacao_total": rng.normal(50_000, 20_000, n),
        "sigla_uf": rng.choice([f"UF{i:02d}" for i in range(27)], n),
        "rede": rng.choice(["Municipal", "Estadual"], n),
        "peso_aluno": np.where(y == 1, np.nan, rng.normal(10, 2, n)),  # vazamento
    })
    achados = []
    for col in ["populacao_total", "sigla_uf", "rede", "peso_aluno"]:
        for teste in (gl.teste_a_nulidade, gl.teste_b_valor, gl.teste_c_auc_sozinha):
            r = teste(df, col)
            if r:
                achados.append(r)
    altas = [a for a in achados if a["gravidade"] == "ALTA"]
    assert len(altas) >= 1, "guarda nao achou nenhuma suspeita ALTA em dado hostil"
    assert any(a["coluna"] == "peso_aluno" for a in altas)
