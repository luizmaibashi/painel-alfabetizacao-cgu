"""
Teste de unidade para src/modeling/04_ranking_intra_uf.py.

POR QUE ESTE ARQUIVO EXISTE
----------------------------
`04_ranking_intra_uf.py` e o UNICO entregavel positivo do projeto (README:
"o produto que sobreviveu a todos os testes do projeto") e tinha ZERO
cobertura de teste de unidade ate 2026-08-29 — achado ao editar o script
para o enriquecimento com IDHM (ADR-0009). O GATE ML de cobertura minima
(.claude/rules/dados.md) ja previa esse tipo de lacuna ("3+ funcoes sem
test_*.py"), mas nunca tinha disparado/sido enderecado para este arquivo
especifico.

Cobre as funcoes que o enriquecimento de features vai tocar
(`prever_direcao_loo`, `comparar_pareado`) e a montagem do dataset
(`montar_dataset`, indiretamente via teste de integracao do join), para que
a mudanca de FEATURES tenha rede de seguranca antes de entrar em producao.
"""
import importlib.util
from pathlib import Path

import numpy as np
import pandas as pd

BASE = Path(__file__).resolve().parents[1]

spec = importlib.util.spec_from_file_location(
    "ranking_intra_uf", BASE / "src" / "modeling" / "04_ranking_intra_uf.py")
riu = importlib.util.module_from_spec(spec)
spec.loader.exec_module(riu)


# --- bootstrap_ic_auc: IC nao pode ser um ponto so ------------------------

def test_bootstrap_ic_auc_retorna_intervalo_nao_degenerado():
    rng = np.random.default_rng(0)
    y = rng.integers(0, 2, 200)
    score = y + rng.normal(0, 0.5, 200)  # score correlacionado com y
    lo, hi = riu.bootstrap_ic_auc(y, score, n_boot=200, seed=0)
    assert lo < hi
    assert 0 <= lo <= 1
    assert 0 <= hi <= 1


def test_bootstrap_ic_auc_e_deterministico_com_mesma_seed():
    rng = np.random.default_rng(1)
    y = rng.integers(0, 2, 100)
    score = rng.random(100)
    r1 = riu.bootstrap_ic_auc(y, score, n_boot=100, seed=42)
    r2 = riu.bootstrap_ic_auc(y, score, n_boot=100, seed=42)
    assert r1 == r2


# --- prever_direcao_loo: preditor de direcao por leave-one-UF-out --------

def _metricas_sinteticas(n_ufs: int = 5) -> list[dict]:
    """UFs onde folga_media prediz auc_dir_melhor de forma quase perfeita
    (relacao linear), para o teste checar que o LOO recupera essa relacao."""
    metricas = []
    for i in range(n_ufs):
        folga = float(i - n_ufs // 2)  # ..., -2, -1, 0, 1, 2, ...
        auc_melhor = 0.5 + 0.1 * folga  # cresce com folga
        metricas.append({
            "uf": f"UF{i}",
            "folga_media": folga,
            "auc_dir_melhor": auc_melhor,
            "auc_dir_pior": 1 - auc_melhor,
            "direcao_real": "melhor_primeiro" if auc_melhor > 0.5 else "pior_primeiro",
            "auc_modelo": auc_melhor,  # modelo hipotetico == auc_dir_melhor p/ simplificar
        })
    return metricas


def test_prever_direcao_loo_preenche_campos_novos_em_cada_uf():
    metricas = _metricas_sinteticas()
    riu.prever_direcao_loo(metricas)
    for m in metricas:
        assert "direcao_prevista" in m
        assert "direcao_previsivel" in m
        assert "auc_baseline_honesto" in m
        assert "ganho_sobre_baseline" in m
        assert m["direcao_prevista"] in ("melhor_primeiro", "pior_primeiro")


def test_prever_direcao_loo_usa_apenas_as_outras_ufs():
    """Uma UF com folga extrema (fora do padrao das demais) nao pode
    "prever a si mesma" -- o LOO tem que ignorar seu proprio ponto."""
    metricas = _metricas_sinteticas(n_ufs=6)
    # antes do LOO, cada UF tem folga/auc coerentes entre si (ver fixture)
    riu.prever_direcao_loo(metricas)
    # A folga da própria UF é entrada legítima da previsão. O que LOO exclui é
    # seu resultado de 2024: alterá-lo não pode mudar a direção prevista.
    direcao_uf0_antes = metricas[0]["direcao_prevista"]

    metricas2 = _metricas_sinteticas(n_ufs=6)
    metricas2[0]["auc_dir_melhor"] = 0.0  # resultado observado de UF0 hostil
    riu.prever_direcao_loo(metricas2)
    direcao_uf0_depois = metricas2[0]["direcao_prevista"]

    assert direcao_uf0_depois == direcao_uf0_antes


# --- comparar_pareado: veredito por UF a partir do IC ---------------------

def _ranked_sintetico() -> tuple[pd.DataFrame, list[dict]]:
    rng = np.random.default_rng(7)
    linhas = []
    for uf, deslocamento in [("VENCE", 0.3), ("PERDE", -0.3), ("EMPATA", 0.0)]:
        n = 60
        taxa23 = rng.random(n)
        y = (taxa23 + rng.normal(0, 0.05, n) > 0.5).astype(int)
        score_risco = taxa23 + deslocamento * (1 - taxa23) + rng.normal(0, 0.05, n)
        linhas.append(pd.DataFrame({
            "sigla_uf": uf, "taxa23": taxa23, "y": y, "score_risco": score_risco,
        }))
    ranked = pd.concat(linhas, ignore_index=True)
    metricas = [{"uf": uf, "direcao_prevista": "melhor_primeiro"}
                for uf in ["VENCE", "PERDE", "EMPATA"]]
    return ranked, metricas


def test_comparar_pareado_preenche_veredito_valido_em_toda_uf():
    ranked, metricas = _ranked_sintetico()
    riu.comparar_pareado(ranked, metricas, n_boot=200, seed=7)
    for m in metricas:
        assert m["veredito"] in ("modelo_vence", "modelo_perde", "inconclusivo")
        lo, hi = m["ganho_ic95"]
        assert lo <= hi


def test_comparar_pareado_e_deterministico_com_mesma_seed():
    ranked, metricas1 = _ranked_sintetico()
    _, metricas2 = _ranked_sintetico()
    riu.comparar_pareado(ranked, metricas1, n_boot=200, seed=7)
    riu.comparar_pareado(ranked, metricas2, n_boot=200, seed=7)
    for m1, m2 in zip(metricas1, metricas2):
        assert m1["ganho_ic95"] == m2["ganho_ic95"]
        assert m1["veredito"] == m2["veredito"]


# --- FEATURES: guarda contra mudanca silenciosa da lista de colunas -------

def test_features_e_uma_lista_nao_vazia_de_strings():
    """Guarda simples: se alguem zerar ou corromper FEATURES sem querer,
    isso deve quebrar aqui, nao silenciosamente no pipeline de producao."""
    assert isinstance(riu.FEATURES, list)
    assert len(riu.FEATURES) > 0
    assert all(isinstance(f, str) for f in riu.FEATURES)


def test_montar_dataset_com_idhm_preserva_municipios_e_adiciona_features(
        tmp_path, monkeypatch):
    """O enriquecimento deve ser um left join: não pode multiplicar nem
    descartar municípios quando a feature externa entra no ranking."""
    metas = pd.DataFrame({
        "id_municipio": [1100015, 1100023, 1100015, 1100023],
        "ano": [2023, 2023, 2024, 2024],
        "taxa_alfabetizacao": [80.0, 70.0, 85.0, 65.0],
        "meta_alfabetizacao_2024": [82.0, 72.0, 82.0, 72.0],
        "meta_alfabetizacao_2025": [84.0, 74.0, 84.0, 74.0],
    })
    territorio = pd.DataFrame({
        "id_municipio": ["1100015", "1100023"],
        "ano": [2023, 2023],
        "populacao_total": [1000, 2000],
    })
    idhm = pd.DataFrame({
        "id_municipio": [1100015, 1100023],
        "idhm": [0.70, 0.60],
        "idhm_e": [0.65, 0.55],
        "idhm_l": [0.75, 0.70],
        "idhm_r": [0.72, 0.58],
    })
    caminho_metas = tmp_path / "metas.csv"
    caminho_territorio = tmp_path / "territorio.parquet"
    caminho_idhm = tmp_path / "idhm_2010.csv"
    metas.to_csv(caminho_metas, index=False)
    territorio.to_parquet(caminho_territorio, index=False)
    idhm.to_csv(caminho_idhm, index=False)

    monkeypatch.setattr(riu, "METAS", caminho_metas)
    monkeypatch.setattr(riu, "TERRITORIO", caminho_territorio)
    monkeypatch.setattr(riu, "IDHM", caminho_idhm)
    monkeypatch.setattr(riu, "buscar_nomes_ibge", lambda: pd.DataFrame({
        "id_municipio": ["1100015", "1100023"],
        "nome_municipio": ["A", "B"],
    }))

    resultado = riu.montar_dataset(com_idhm=True)

    assert len(resultado) == 2
    assert resultado["id_municipio"].is_unique
    assert set(riu.FEATURES_IDHM).issubset(resultado.columns)
    assert resultado[riu.FEATURES_IDHM].notna().all().all()
