"""Testes das garantias estatísticas do backtest prospectivo."""
import importlib.util
from pathlib import Path

import numpy as np
import pandas as pd
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


# --- Contrato de uso condicional no ranking operacional de 2025 --------------

def _ranking_ficticio(uf, direcao, scores, taxa_base, y):
    return pd.DataFrame({
        "sigla_uf": uf,
        "nome_municipio": [f"{uf}-{i}" for i in range(len(scores))],
        "score_modelo": scores,
        "taxa_base": taxa_base,
        "meta_alvo": [80.0] * len(scores),
        "taxa25": [70.0] * len(scores),
        "y": y,
    })


def _metrica(uf, direcao, veredito, n, ganho=0.1):
    return {
        "uf": uf, "n_municipios": n, "direcao_prevista": direcao,
        "taxa_falha_2025": 0.3, "auc_modelo": 0.62, "auc_baseline": 0.52,
        "ganho_sobre_baseline": ganho, "ganho_ic95": [0.02, 0.18],
        "veredito": veredito,
    }


FONTE = {"arquivo": "x.xlsx", "sha256": "abc", "url": "http://inep"}


def test_veredito_mapeia_para_uso_do_painel():
    ranking = pd.concat([
        _ranking_ficticio("SP", "melhor_primeiro", [.9, .5, .1], [30, 60, 90], [1, 1, 0]),
        _ranking_ficticio("CE", "pior_primeiro", [.8, .4, .2], [40, 70, 95], [1, 0, 0]),
        _ranking_ficticio("PR", "pior_primeiro", [.7, .6, .3], [50, 65, 88], [0, 1, 0]),
    ], ignore_index=True)
    metricas = [
        _metrica("SP", "melhor_primeiro", "modelo_vence", 3),
        _metrica("CE", "pior_primeiro", "modelo_perde", 3),
        _metrica("PR", "pior_primeiro", "inconclusivo", 3),
    ]
    op = MODULO.montar_ranking_operacional(ranking, metricas, FONTE)

    assert op["ufs"]["SP"]["uso"] == "ranking_modelo"
    assert op["ufs"]["CE"]["uso"] == "regra_simples"
    assert op["ufs"]["PR"]["uso"] == "abster"
    assert op["resumo"] == {
        "ufs": 3, "municipios": 9,
        "ufs_ranking_modelo": 1, "ufs_regra_simples": 1, "ufs_abster": 1,
    }
    # sem eixo nacional no payload
    assert "ranking_nacional" not in op and "nacional" not in op["resumo"]


def test_uf_modelo_ordena_por_score_decrescente():
    ranking = _ranking_ficticio("SP", "melhor_primeiro", [.2, .9, .5], [90, 30, 60], [0, 1, 1])
    op = MODULO.montar_ranking_operacional(
        ranking, [_metrica("SP", "melhor_primeiro", "modelo_vence", 3)], FONTE)
    linhas = op["ufs"]["SP"]["m"]
    assert [l[0] for l in linhas] == [1, 2, 3]
    assert [l[2] for l in linhas] == sorted([l[2] for l in linhas], reverse=True)


def test_uf_regra_simples_ordena_pela_direcao_prevista():
    # pior_primeiro -> menor taxa_base primeiro (ascendente)
    ranking = _ranking_ficticio("CE", "pior_primeiro", [.5, .5, .5], [95, 40, 70], [0, 1, 0])
    op = MODULO.montar_ranking_operacional(
        ranking, [_metrica("CE", "pior_primeiro", "modelo_perde", 3)], FONTE)
    taxas = [l[3] for l in op["ufs"]["CE"]["m"]]
    assert taxas == [40.0, 70.0, 95.0]

    # melhor_primeiro -> maior taxa_base primeiro (descendente)
    ranking2 = _ranking_ficticio("BA", "melhor_primeiro", [.5, .5, .5], [40, 95, 70], [1, 0, 0])
    op2 = MODULO.montar_ranking_operacional(
        ranking2, [_metrica("BA", "melhor_primeiro", "modelo_perde", 3)], FONTE)
    assert [l[3] for l in op2["ufs"]["BA"]["m"]] == [95.0, 70.0, 40.0]


def test_amostra_pequena_e_rastreabilidade_no_payload():
    ranking = _ranking_ficticio("RO", "melhor_primeiro", [.6, .4], [50, 70], [1, 0])
    op = MODULO.montar_ranking_operacional(
        ranking, [_metrica("RO", "melhor_primeiro", "modelo_vence", 52)], FONTE)
    assert op["ufs"]["RO"]["amostra_pequena"] is True
    assert op["fonte"]["sha256"] == "abc"
    assert op["data_publicacao_inep"] == MODULO.DATA_PUBLICACAO_INEP
    assert op["ciclo"] == MODULO.ANO_CICLO
    assert "entre UFs" in op["desenho"] or "Comparação entre UFs" in op["desenho"]


def test_num_trata_nulo_e_arredonda():
    assert MODULO._num(None) is None
    assert MODULO._num(float("nan")) is None
    assert MODULO._num(72.348) == 72.3


# --- Garantia da fonte (ADR-0010 + reprodutibilidade do enunciado) ---------
#
# POR QUE ESTES TESTES EXISTEM
# A planilha do Inep nao entra no git (`*.xlsx` ignorado) e, em 2026-08-31, a
# revisao do projeto achou que ela tambem nao estava no disco: o script que
# produz o numero canonico do projeto NAO rodava num clone limpo, contra o
# "pipeline reproduzivel" exigido pelo enunciado (pag. 7).
#
# A correcao (baixar sob demanda) cria um risco novo e pior: baixar um arquivo
# DIFERENTE com o mesmo nome produziria um backtest diferente sem nada
# quebrar. Por isso a verificacao de SHA-256 tem que falhar ALTO, e por isso
# ela tem teste proprio.

import hashlib

import pytest


def test_sha256_de_confere_com_hashlib(tmp_path):
    arq = tmp_path / "x.bin"
    conteudo = b"conteudo de teste do backtest"
    arq.write_bytes(conteudo)
    assert MODULO.sha256_de(arq) == hashlib.sha256(conteudo).hexdigest()


def test_sha256_de_muda_quando_o_conteudo_muda(tmp_path):
    a, b = tmp_path / "a.bin", tmp_path / "b.bin"
    a.write_bytes(b"conteudo A")
    b.write_bytes(b"conteudo B")
    assert MODULO.sha256_de(a) != MODULO.sha256_de(b)


def test_garantir_fonte_aceita_arquivo_com_sha_esperado(tmp_path):
    arq = tmp_path / "ica.xlsx"
    arq.write_bytes(b"planilha oficial")
    sha = hashlib.sha256(b"planilha oficial").hexdigest()
    assert MODULO.garantir_fonte_ica(arq, url="http://nao-usar", sha_esperado=sha) == arq


def test_garantir_fonte_FALHA_ALTO_com_sha_divergente(tmp_path):
    """
    O teste mais importante deste arquivo: arquivo trocado NAO pode passar em
    silencio. Sem isso, o Inep republicar a planilha mudaria o resultado
    canonico do projeto sem aviso nenhum.
    """
    arq = tmp_path / "ica.xlsx"
    arq.write_bytes(b"planilha ADULTERADA")
    with pytest.raises(ValueError, match="SHA-256"):
        MODULO.garantir_fonte_ica(arq, url="http://nao-usar", sha_esperado="0" * 64)


def test_garantir_fonte_nao_baixa_quando_arquivo_ja_existe(tmp_path):
    """URL invalida de proposito: se tentasse baixar, o teste quebraria."""
    arq = tmp_path / "ica.xlsx"
    arq.write_bytes(b"ja esta aqui")
    sha = hashlib.sha256(b"ja esta aqui").hexdigest()
    MODULO.garantir_fonte_ica(arq, url="http://host.invalido.invalido/x.xlsx",
                               sha_esperado=sha)


def test_sha_esperado_do_projeto_bate_com_o_registrado_no_relatorio():
    """
    Guarda contra deriva entre a constante do codigo e a proveniencia
    publicada: os dois tem que contar a mesma historia sobre qual arquivo
    gerou o numero canonico.
    """
    import json
    rel = Path(__file__).resolve().parents[1] / "reports" / "backtest_prospectivo_2025.json"
    registrado = json.loads(rel.read_text(encoding="utf-8"))["fonte"]["sha256"]
    assert MODULO.SHA256_ICA_2025 == registrado
