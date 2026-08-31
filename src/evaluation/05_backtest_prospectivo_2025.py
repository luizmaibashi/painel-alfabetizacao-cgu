"""Backtest prospectivo do ranking municipal intra-UF.

Congela a decisão tomada antes de ler o alvo de 2025: treina somente na
transição 2023->2024 e pontua 2025 com taxa de 2024 e metas já publicadas.
Não atualiza o produto nem o painel; produz evidência para decidir isso.
"""
import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.metrics import roc_auc_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import RobustScaler

BASE = Path(__file__).resolve().parents[2]
ICA_2025 = BASE / "dados_externos" / "resultados_e_metas_municipios_2025_3.xlsx"
# A planilha e a FONTE do backtest, mas nao entra no git (`*.xlsx` no
# .gitignore da base). Sem o download automatico abaixo, este script — que
# produz o numero canonico do projeto — falhava num clone limpo, e o
# "pipeline reproduzivel" exigido pelo enunciado (pag. 7) nao se sustentava.
URL_ICA_2025 = ("https://download.inep.gov.br/avaliacao_da_alfabetizacao/"
                "resultados/resultados_e_metas_municipios_2025_3.xlsx")
SHA256_ICA_2025 = "709c7eeba34d9c91e7f193e6c2b25e453ec7b535a6d8ac7e39c095bd0c24eb60"
TERRITORIO = BASE / "data" / "territorio_local.parquet"
SAIDA = BASE / "reports" / "backtest_prospectivo_2025.json"
SAIDA_RANKING = BASE / "reports" / "ranking_prospectivo_2025.json"
DATA_PUBLICACAO_INEP = "2026-04-01"
ANO_CICLO = 2025

RANDOM_STATE = 42
N_BOOT = 1000
MIN_MUNICIPIOS = 40
FEATURES = ["taxa_base", "meta_alvo", "meta_seguinte", "populacao_total"]

COLUNAS_ICA = {
    "CO_MUNICIPIO": "id_municipio",
    "SG_UF": "sigla_uf",
    "NO_MUNICIPIO": "nome_municipio",
    "PC_ALUNO_ALFABETIZADO_2023": "taxa23",
    "PC_ALUNO_ALFABETIZADO_2024": "taxa24",
    "PC_ALUNO_ALFABETIZADO_2025": "taxa25",
    "META_FINAL_2024": "meta24",
    "META_FINAL_2025": "meta25",
    "META_FINAL_2026": "meta26",
    "PC_AVALIADOS_LP": "participacao_2025",
}


def hash_arquivo(caminho: Path) -> str:
    return hashlib.sha256(caminho.read_bytes()).hexdigest()


def sha256_de(caminho: Path) -> str:
    h = hashlib.sha256()
    with open(caminho, "rb") as f:
        for bloco in iter(lambda: f.read(1 << 20), b""):
            h.update(bloco)
    return h.hexdigest()


def garantir_fonte_ica(caminho: Path = ICA_2025, url: str = URL_ICA_2025,
                        sha_esperado: str = SHA256_ICA_2025) -> Path:
    """
    Garante que a planilha oficial do Inep esteja no disco e seja A MESMA que
    produziu o resultado canonico.

    Falha ALTO em divergencia de hash, nunca segue em silencio: um arquivo
    diferente com o mesmo nome produziria um backtest diferente sem que nada
    quebrasse — o modo de falha mais caro possivel para um numero que o
    projeto trata como imutavel (ADR-0010).
    """
    if not caminho.exists():
        import time
        import urllib.error
        import urllib.request
        print(f"  fonte ausente; baixando de {url}")
        caminho.parent.mkdir(parents=True, exist_ok=True)
        # O servidor do Inep derruba a conexao de forma intermitente
        # (WinError 10054 observado em 2026-08-31); 3 tentativas com espera
        # resolvem. Sem o retry, o script falharia por instabilidade de rede
        # e nao por problema do projeto — erro caro de diagnosticar.
        req = urllib.request.Request(url, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            "Accept": "*/*"})
        ultimo_erro = None
        for tentativa in range(1, 4):
            try:
                with urllib.request.urlopen(req, timeout=600) as r:
                    dados = r.read()
                caminho.write_bytes(dados)
                break
            except (urllib.error.URLError, OSError) as e:
                ultimo_erro = e
                print(f"    tentativa {tentativa}/3 falhou ({e}); repetindo...")
                time.sleep(3)
        else:
            raise RuntimeError(
                f"Nao foi possivel baixar a fonte ICA apos 3 tentativas: "
                f"{ultimo_erro}. Baixe manualmente de {url} e salve em "
                f"{caminho}.")

    sha = sha256_de(caminho)
    if sha != sha_esperado:
        raise ValueError(
            "SHA-256 da fonte ICA nao confere.\n"
            f"  esperado: {sha_esperado}\n"
            f"  obtido:   {sha}\n"
            f"  arquivo:  {caminho}\n"
            "O Inep pode ter republicado a planilha. NAO prossiga sem decidir "
            "explicitamente: um dado diferente muda o resultado canonico do "
            "projeto (ADR-0010).")
    print(f"  fonte verificada (SHA-256 confere): {caminho.name}")
    return caminho


def carregar_ica(caminho: Path = ICA_2025) -> pd.DataFrame:
    """Lê a planilha oficial e rejeita linhas que não são municípios."""
    bruto = pd.read_excel(caminho, sheet_name=0, header=1,
                          dtype={"CO_MUNICIPIO": "string"})
    faltantes = set(COLUNAS_ICA) - set(bruto.columns)
    if faltantes:
        raise ValueError(f"Planilha ICA sem colunas esperadas: {sorted(faltantes)}")
    df = bruto.dropna(subset=["CO_MUNICIPIO"]).rename(columns=COLUNAS_ICA).copy()
    df["id_municipio"] = df["id_municipio"].astype(str).str.zfill(7)
    if df.id_municipio.duplicated().any():
        raise ValueError("A fonte ICA contém código municipal duplicado")
    for coluna in [c for c in COLUNAS_ICA.values() if c.startswith(("taxa", "meta", "participacao"))]:
        df[coluna] = pd.to_numeric(df[coluna], errors="coerce")
    return df[list(COLUNAS_ICA.values())]


def montar_janelas(ica: pd.DataFrame, territorio: Path = TERRITORIO) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Monta treino 2023->2024 e teste prospectivo 2024->2025."""
    pop = pd.read_parquet(territorio)
    pop = pop[pop.ano == 2023][["id_municipio", "populacao_total"]].drop_duplicates("id_municipio")
    dados = ica.merge(pop, on="id_municipio", how="left")

    treino = dados.rename(columns={
        "taxa23": "taxa_base", "meta24": "meta_alvo", "meta25": "meta_seguinte"
    }).copy()
    treino["y"] = (treino.taxa24 < treino.meta_alvo).astype("int8")
    treino = treino.dropna(subset=["taxa_base", "meta_alvo", "meta_seguinte"])

    teste = dados.rename(columns={
        "taxa24": "taxa_base", "meta25": "meta_alvo", "meta26": "meta_seguinte"
    }).copy()
    teste["y"] = (teste.taxa25 < teste.meta_alvo).astype("int8")
    teste = teste.dropna(subset=["taxa_base", "meta_alvo", "meta_seguinte", "taxa25"])
    return treino.reset_index(drop=True), teste.reset_index(drop=True)


def pipeline() -> Pipeline:
    pre = ColumnTransformer([("num", Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", RobustScaler()),
    ]), FEATURES)])
    return Pipeline([("prep", pre), ("modelo", RandomForestClassifier(
        n_estimators=200, max_depth=6, random_state=RANDOM_STATE, n_jobs=-1
    ))])


def direcoes_persistentes(treino: pd.DataFrame) -> dict[str, str]:
    """Usa em 2025 a direção observada no próprio estado em 2024.

    É mais forte que prever a direção por outras UFs e ainda é legítimo: o
    resultado 2024 já estava disponível antes do alvo 2025. Se o modelo não o
    superar, não há razão para manter uma alternativa mais complexa.
    """
    direcoes = {}
    for uf, grupo in treino.groupby("sigla_uf"):
        if len(grupo) < MIN_MUNICIPIOS or grupo.y.nunique() < 2:
            continue
        auc_melhor = roc_auc_score(grupo.y, grupo.taxa_base)
        direcoes[uf] = "melhor_primeiro" if auc_melhor > 0.5 else "pior_primeiro"
    return direcoes


def _auc_por_pesos(y: np.ndarray, scores: np.ndarray, pesos: np.ndarray) -> np.ndarray:
    """AUC por reamostragem representada pelas contagens de cada linha.

    As contagens multinomiais são equivalentes a sortear ``n`` linhas com
    reposição. A forma vetorizada conserva o pareamento modelo/baseline e
    permite calcular 1.000 reamostragens para todas as UFs rapidamente.
    """
    ordem = np.argsort(scores, kind="stable")
    y_ord = y[ordem]
    score_ord = scores[ordem]
    pesos_ord = pesos[:, ordem]
    inicio = np.flatnonzero(np.r_[True, score_ord[1:] != score_ord[:-1]])
    fim = np.r_[inicio[1:], len(score_ord)]

    positivos = np.zeros(len(pesos), dtype=float)
    negativos = np.zeros(len(pesos), dtype=float)
    concordancias = np.zeros(len(pesos), dtype=float)
    for primeiro, ultimo in zip(inicio, fim):
        grupo = pesos_ord[:, primeiro:ultimo]
        pos = grupo[:, y_ord[primeiro:ultimo] == 1].sum(axis=1)
        neg = grupo[:, y_ord[primeiro:ultimo] == 0].sum(axis=1)
        concordancias += pos * (negativos + 0.5 * neg)
        positivos += pos
        negativos += neg

    denominador = positivos * negativos
    aucs = np.full(len(pesos), np.nan)
    validos = denominador > 0
    aucs[validos] = concordancias[validos] / denominador[validos]
    return aucs


def bootstrap_ganho(y: np.ndarray, modelo: np.ndarray, baseline: np.ndarray,
                    n_boot: int = N_BOOT, seed: int = RANDOM_STATE) -> list[float]:
    """IC bootstrap pareado para AUC(modelo) - AUC(baseline)."""
    y = np.asarray(y)
    rng = np.random.default_rng(seed)
    tamanho = len(y)
    pesos = rng.multinomial(tamanho, np.full(tamanho, 1 / tamanho), size=n_boot)
    ganhos = _auc_por_pesos(y, np.asarray(modelo), pesos) - _auc_por_pesos(y, np.asarray(baseline), pesos)
    ganhos = ganhos[~np.isnan(ganhos)]
    lo, hi = np.percentile(ganhos, [2.5, 97.5])
    return [round(float(lo), 4), round(float(hi), 4)]


def executar_backtest(treino: pd.DataFrame, teste: pd.DataFrame,
                      n_boot: int = N_BOOT) -> tuple[pd.DataFrame, list[dict]]:
    direcoes = direcoes_persistentes(treino)
    rankings, metricas = [], []
    for uf, tr in treino.groupby("sigla_uf"):
        te = teste[teste.sigla_uf == uf].copy()
        if len(tr) < MIN_MUNICIPIOS or len(te) < MIN_MUNICIPIOS:
            continue
        if tr.y.nunique() < 2 or te.y.nunique() < 2:
            continue
        modelo = pipeline().fit(tr[FEATURES], tr.y)
        te["score_modelo"] = modelo.predict_proba(te[FEATURES])[:, 1]
        direcao = direcoes[uf]
        te["score_baseline"] = te.taxa_base if direcao == "melhor_primeiro" else -te.taxa_base
        auc_modelo = roc_auc_score(te.y, te.score_modelo)
        auc_baseline = roc_auc_score(te.y, te.score_baseline)
        ic = bootstrap_ganho(te.y.to_numpy(), te.score_modelo.to_numpy(),
                              te.score_baseline.to_numpy(), n_boot=n_boot)
        veredito = "modelo_vence" if ic[0] > 0 else "modelo_perde" if ic[1] < 0 else "inconclusivo"
        te["rank_modelo"] = te.score_modelo.rank(ascending=False, method="first").astype(int)
        rankings.append(te)
        metricas.append({
            "uf": uf, "n_municipios": int(len(te)), "direcao_prevista": direcao,
            "taxa_falha_2025": round(float(te.y.mean()), 4),
            "auc_modelo": round(float(auc_modelo), 4),
            "auc_baseline": round(float(auc_baseline), 4),
            "ganho_sobre_baseline": round(float(auc_modelo - auc_baseline), 4),
            "ganho_ic95": ic, "veredito": veredito,
        })
    return pd.concat(rankings, ignore_index=True), metricas


NOME_UF = {
    "AC": "Acre", "AL": "Alagoas", "AM": "Amazonas", "AP": "Amapá",
    "BA": "Bahia", "CE": "Ceará", "DF": "Distrito Federal", "ES": "Espírito Santo",
    "GO": "Goiás", "MA": "Maranhão", "MG": "Minas Gerais", "MS": "Mato Grosso do Sul",
    "MT": "Mato Grosso", "PA": "Pará", "PB": "Paraíba", "PE": "Pernambuco",
    "PI": "Piauí", "PR": "Paraná", "RJ": "Rio de Janeiro", "RN": "Rio Grande do Norte",
    "RO": "Rondônia", "RR": "Roraima", "RS": "Rio Grande do Sul", "SC": "Santa Catarina",
    "SE": "Sergipe", "SP": "São Paulo", "TO": "Tocantins",
}

# Como o painel deve tratar cada UF, derivado do veredito prospectivo de 2025.
CONTRATO_POR_VEREDITO = {
    "modelo_vence": "ranking_modelo",
    "modelo_perde": "regra_simples",
    "inconclusivo": "abster",
}


def montar_ranking_operacional(ranking: pd.DataFrame, metricas: list[dict],
                               fonte: dict) -> dict:
    """Monta o JSON que o painel de 2025 consome, já com o contrato de uso.

    Cada UF recebe ``uso`` (``ranking_modelo`` | ``regra_simples`` | ``abster``)
    a partir do veredito do backtest prospectivo. A ordenação municipal exposta
    segue o ``uso``: pelo score do modelo onde ele venceu, pela taxa de 2024 na
    direção que funcionou naquela UF onde perdeu, e pelo score do modelo
    (apenas como diagnóstico, sem recomendar ação) onde é inconclusivo.
    A comparação entre UFs continua impossível: não há eixo nacional no payload.
    """
    met = {m["uf"]: m for m in metricas}
    ufs = {}
    for uf, grupo in ranking.groupby("sigla_uf"):
        m = met[uf]
        uso = CONTRATO_POR_VEREDITO[m["veredito"]]
        direcao = m["direcao_prevista"]
        g = grupo.copy()
        if uso == "regra_simples":
            # ordena pela regra simples da direção prevista: "melhor_primeiro"
            # prioriza a MAIOR taxa de 2024 (topo falha mais por regressão à
            # média); "pior_primeiro" prioriza a MENOR taxa.
            asc = direcao == "pior_primeiro"
            g = g.sort_values("taxa_base", ascending=asc)
        else:
            g = g.sort_values("score_modelo", ascending=False)
        g = g.reset_index(drop=True)
        g["rank_uf"] = np.arange(1, len(g) + 1)
        linhas = [
            # [rank, nome, score_modelo, taxa24, meta25, taxa25, y_2025]
            [int(r.rank_uf), r.nome_municipio, round(float(r.score_modelo), 4),
             _num(r.taxa_base), _num(r.meta_alvo), _num(r.taxa25), int(r.y)]
            for r in g.itertuples()
        ]
        ufs[uf] = {
            "nome": NOME_UF.get(uf, uf),
            "n": int(m["n_municipios"]),
            "uso": uso,
            "veredito": m["veredito"],
            "direcao": direcao,
            "taxa_falha_2025": m["taxa_falha_2025"],
            "auc_modelo": m["auc_modelo"],
            "auc_baseline": m["auc_baseline"],
            "ganho": m["ganho_sobre_baseline"],
            "ganho_ic": m["ganho_ic95"],
            "amostra_pequena": bool(m["n_municipios"] < 100),
            "m": linhas,
        }
    resumo = {
        "ufs": len(ufs),
        "municipios": int(len(ranking)),
        "ufs_ranking_modelo": sum(u["uso"] == "ranking_modelo" for u in ufs.values()),
        "ufs_regra_simples": sum(u["uso"] == "regra_simples" for u in ufs.values()),
        "ufs_abster": sum(u["uso"] == "abster" for u in ufs.values()),
    }
    return {
        "fonte": fonte,
        "ciclo": ANO_CICLO,
        "data_publicacao_inep": DATA_PUBLICACAO_INEP,
        "desenho": (
            "Ranking municipal intra-UF congelado no backtest prospectivo 2024->2025. "
            "Uso condicional por UF: modelo onde venceu a regra simples com "
            "significância, regra simples onde perdeu, abstenção onde é inconclusivo. "
            "Comparação entre UFs bloqueada por construção."
        ),
        "aviso_validade": (
            "Retrato do ciclo 2025 do Compromisso Nacional Criança Alfabetizada. "
            "Reavaliar a cada publicação anual do Inep antes de mudar a regra de "
            "qualquer UF."
        ),
        "resumo": resumo,
        "ufs": ufs,
    }


def _num(valor) -> float | None:
    if valor is None or (isinstance(valor, float) and np.isnan(valor)):
        return None
    return round(float(valor), 1)


def main() -> None:
    garantir_fonte_ica()
    ica = carregar_ica()
    treino, teste = montar_janelas(ica)
    n_boot = N_BOOT
    ranking, metricas = executar_backtest(treino, teste, n_boot=n_boot)
    dfm = pd.DataFrame(metricas)
    pesos = dfm.n_municipios
    fonte = {
        "arquivo": str(ICA_2025.relative_to(BASE)), "sha256": hash_arquivo(ICA_2025),
        "url": "https://download.inep.gov.br/avaliacao_da_alfabetizacao/resultados/resultados_e_metas_municipios_2025_3.xlsx",
    }
    resultado = {
        "fonte": fonte,
        "desenho": "Treina 2023->2024 e testa prospectivamente 2024->2025; sem tuning ou alvo de 2025 no treino.",
        "resumo": {
            "ufs": int(len(dfm)), "municipios": int(len(ranking)),
            "auc_modelo_ponderado": round(float(np.average(dfm.auc_modelo, weights=pesos)), 4),
            "auc_baseline_ponderado": round(float(np.average(dfm.auc_baseline, weights=pesos)), 4),
            "ganho_ponderado": round(float(np.average(dfm.ganho_sobre_baseline, weights=pesos)), 4),
            "ufs_modelo_vence": int((dfm.veredito == "modelo_vence").sum()),
            "ufs_inconclusivo": int((dfm.veredito == "inconclusivo").sum()),
            "ufs_modelo_perde": int((dfm.veredito == "modelo_perde").sum()),
            "reamostragens_bootstrap": n_boot,
        },
        "metricas_por_uf": metricas,
    }
    SAIDA.write_text(json.dumps(resultado, ensure_ascii=False, indent=2), encoding="utf-8")

    operacional = montar_ranking_operacional(ranking, metricas, fonte)
    SAIDA_RANKING.write_text(
        json.dumps(operacional, ensure_ascii=False, indent=2), encoding="utf-8")

    print(json.dumps(resultado["resumo"], ensure_ascii=False, indent=2))
    print(json.dumps(operacional["resumo"], ensure_ascii=False, indent=2))
    print(f"Relatório: {SAIDA.relative_to(BASE)}")
    print(f"Ranking operacional: {SAIDA_RANKING.relative_to(BASE)}")


if __name__ == "__main__":
    main()
