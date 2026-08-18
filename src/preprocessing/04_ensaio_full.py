"""
ENSAIO DO MODO `--full` — testa o caminho que nunca foi executado.

POR QUE ESTE SCRIPT EXISTE
--------------------------
O modo `--full` (que traz território, socioeconômico e meta da Silver no GCS)
nunca rodou: depende de credencial que só o Renan tem. E o padrão dominante
deste projeto, encontrado cinco vezes, é **"nada quebra, mas o resultado está
errado"**. A chance de o `--full` rodar na call, dar um número ruim e ninguém
saber por quê é alta demais para aceitar.

Este ensaio constrói uma Silver **sintética** com o schema esperado e roda o
caminho `--full` inteiro contra ela, localmente. Não valida o conteúdo do dado
real — valida a **mecânica do join e do pipeline**, que é onde os cinco erros
anteriores moraram.

AS ARMADILHAS REPRODUZIDAS DE PROPÓSITO
---------------------------------------
A Silver sintética é construída hostil, imitando problemas que a Fase 2 já
documentou ou que são clássicos deste tipo de join:

  1. `id_municipio` como INTEIRO — perde o zero à esquerda (ADR-005 da Fase 2).
     Se o `zfill(7)` do extrator falhar, ~9% dos municípios não casam.
  2. Linhas DUPLICADAS em (municipio, ano, rede) — se o `drop_duplicates` não
     rodar, o join multiplica alunos e o modelo treina com peso dobrado.
  3. `meta_alfabetizacao_2024` NULA fora da rede Municipal — é o cenário real
     do ADR-004 (só Municipal tem meta oficial do PDE). Testa a derivação do
     flag `meta_is_imputada`.
  4. Municípios FALTANDO na Silver — testa se o left join preserva as linhas e
     se a cobertura é reportada em vez de passar batido.
  5. `sigla_uf` presente — é a única condição em que a imputação por mediana de
     UF (ADR-0001 §2.3) consegue executar. Nunca foi exercitada.

USO
    python src/preprocessing/04_ensaio_full.py
"""
import subprocess
import sys
from pathlib import Path

import numpy as np
import pandas as pd

BASE = Path(__file__).resolve().parents[2]
ALUNOS = BASE.parent / "tech-challenge-fase2-alfabetizacao" / "dados" / "Alunos.csv"
SILVER_FAKE = BASE / "data" / "_silver_sintetica_ensaio.parquet"

RANDOM_STATE = 42
FRACAO_MUNICIPIOS_AUSENTES = 0.08   # armadilha 4
N_DUPLICATAS = 50                    # armadilha 2

# Prefixo do código IBGE -> UF (só o necessário para gerar sigla_uf plausível)
UF_POR_PREFIXO = {
    11: "RO", 12: "AC", 13: "AM", 14: "RR", 15: "PA", 16: "AP", 17: "TO",
    21: "MA", 22: "PI", 23: "CE", 24: "RN", 25: "PB", 26: "PE", 27: "AL",
    28: "SE", 29: "BA", 31: "MG", 32: "ES", 33: "RJ", 35: "SP", 41: "PR",
    42: "SC", 43: "RS", 50: "MS", 51: "MT", 52: "GO", 53: "DF",
}


def construir_silver_sintetica() -> pd.DataFrame:
    rng = np.random.default_rng(RANDOM_STATE)
    alunos = pd.read_csv(ALUNOS, usecols=["id_municipio", "ano", "rede"])

    combos = alunos.drop_duplicates(subset=["id_municipio", "ano", "rede"]).copy()

    # armadilha 4: alguns municipios simplesmente nao existem na Silver
    municipios = combos["id_municipio"].unique()
    fora = rng.choice(municipios,
                      size=int(len(municipios) * FRACAO_MUNICIPIOS_AUSENTES),
                      replace=False)
    combos = combos[~combos["id_municipio"].isin(fora)].copy()

    # armadilha 1: id_municipio como INTEIRO (o CSV ja vem assim; garantir)
    combos["id_municipio"] = combos["id_municipio"].astype("int64")

    prefixo = (combos["id_municipio"] // 100000).astype(int)
    combos["sigla_uf"] = prefixo.map(UF_POR_PREFIXO).fillna("XX")

    n = len(combos)
    combos["populacao_total"] = rng.lognormal(9.5, 1.3, n).round(0)
    combos["gasto_por_habitante_educacao"] = rng.normal(950, 280, n).clip(120).round(2)

    # armadilha 3: meta oficial so existe na rede Municipal (ADR-004)
    meta_base = rng.normal(72, 9, n).clip(30, 100).round(2)
    combos["meta_alfabetizacao_2024"] = np.where(
        combos["rede"].eq("Municipal"), meta_base, np.nan)
    # a imputada (KNN) preenche todas
    combos["meta_alfabetizacao_2024_imputada"] = meta_base

    # armadilha 2: duplicatas na chave do join
    dups = combos.sample(N_DUPLICATAS, random_state=RANDOM_STATE)
    return pd.concat([combos, dups], ignore_index=True)


def checar(nome: str, ok: bool, detalhe: str = "") -> bool:
    print(f"  {'[OK]  ' if ok else '[FALHA]'} {nome}")
    if detalhe:
        print(f"          {detalhe}")
    return ok


def main():
    print("=" * 74)
    print("ENSAIO DO MODO --full (o caminho que nunca foi executado)")
    print("=" * 74)

    silver = construir_silver_sintetica()
    SILVER_FAKE.parent.mkdir(exist_ok=True)
    silver.to_parquet(SILVER_FAKE, index=False)
    print(f"\nSilver sintetica: {len(silver)} linhas, "
          f"{silver['id_municipio'].nunique()} municipios, "
          f"dtype de id_municipio = {silver['id_municipio'].dtype} (armadilha 1)")
    print(f"  {N_DUPLICATAS} duplicatas plantadas (armadilha 2)")
    print(f"  meta oficial nula fora da rede Municipal (armadilha 3): "
          f"{silver['meta_alfabetizacao_2024'].isna().mean():.1%} das linhas")
    print(f"  ~{FRACAO_MUNICIPIOS_AUSENTES:.0%} dos municipios fora da Silver "
          f"(armadilha 4)")

    print("\n" + "-" * 74)
    print("Rodando: 02_extrair_snapshot.py --full --silver <sintetica>")
    print("-" * 74)
    r = subprocess.run(
        [sys.executable, str(BASE / "src" / "preprocessing" / "02_extrair_snapshot.py"),
         "--full", "--silver", str(SILVER_FAKE)],
        capture_output=True, text=True,
    )
    print(r.stdout.strip())
    if r.returncode != 0:
        print("\n[FALHA] a extracao --full quebrou:\n")
        print(r.stderr[-2500:])
        sys.exit(1)

    snap = pd.read_parquet(BASE / "data" / "snapshot_modelagem.parquet")

    # Esperado = população de modelagem (só avaliados), não o CSV bruto.
    # A extração filtra os ausentes por metodologia oficial (ver docstring de
    # `carregar_alunos`), então comparar contra o total do arquivo daria falso
    # negativo. O que este teste precisa garantir é que o JOIN com a Silver não
    # multiplicou nem perdeu linhas — não que nada foi filtrado antes dele.
    bruto = pd.read_csv(ALUNOS, usecols=["presenca"])
    alunos_n = int((bruto["presenca"] != "Ausente").sum())

    print("\n" + "-" * 74)
    print("VERIFICACOES")
    print("-" * 74)
    ok = []

    ok.append(checar("join preservou as linhas da populacao de modelagem",
                     len(snap) == alunos_n,
                     f"avaliados no CSV={alunos_n} snapshot={len(snap)}"))

    esperadas = ["populacao_total", "gasto_por_habitante_educacao", "sigla_uf",
                 "meta_alfabetizacao_2024_imputada", "meta_is_imputada"]
    faltando = [c for c in esperadas if c not in snap.columns]
    ok.append(checar("as 5 colunas do --full chegaram no snapshot",
                     not faltando, f"faltando: {faltando}" if faltando else ""))

    if "populacao_total" in snap.columns:
        casou = snap["populacao_total"].notna().mean()
        ok.append(checar("join casou acima de 85% (zeros a esquerda OK)",
                         casou > 0.85, f"casou em {casou:.1%} das linhas"))

    if "meta_is_imputada" in snap.columns:
        # rede != Municipal deve ter meta imputada (flag=1)
        nao_mun = snap[snap["rede"].ne("Municipal") & snap["meta_is_imputada"].notna()]
        taxa = nao_mun["meta_is_imputada"].mean() if len(nao_mun) else float("nan")
        ok.append(checar("flag meta_is_imputada derivado corretamente",
                         len(nao_mun) > 0 and taxa > 0.99,
                         f"{taxa:.1%} das linhas fora da rede Municipal marcadas "
                         f"como imputadas (esperado ~100%)"))

    if "absenteismo_hist_municipio_t1" in snap.columns:
        semnulo = snap["absenteismo_hist_municipio_t1"].notna().all()
        ok.append(checar("imputacao do historico rodou (sem nulos restantes)",
                         semnulo))

    # o pre-processador enxerga as colunas novas?
    sys.path.insert(0, str(BASE / "src" / "preprocessing"))
    from pipeline_preprocessamento import colunas_feature, colunas_ignoradas
    feats = colunas_feature(snap)
    novas = [c for c in esperadas if c in feats]
    ok.append(checar("pre-processador adotou as features novas",
                     len(novas) >= 4, f"features do --full em uso: {novas}"))

    ignoradas = colunas_ignoradas(snap)
    ok.append(checar("nenhuma coluna do snapshot sendo descartada em silencio",
                     not ignoradas, f"ignoradas: {ignoradas}" if ignoradas else ""))

    # guarda de leakage sobre o snapshot --full
    print("\n" + "-" * 74)
    print("Guarda de leakage sobre o snapshot --full")
    print("-" * 74)
    g = subprocess.run(
        [sys.executable, str(BASE / "src" / "preprocessing" / "03_guarda_leakage.py")],
        capture_output=True, text=True,
    )
    linhas_guarda = [l for l in g.stdout.splitlines()
                     if l.startswith(("[", "Resumo"))]
    for linha in linhas_guarda:
        print("  " + linha)
    if not linhas_guarda and g.stderr:
        print("  o guarda QUEBROU (nao chegou a avaliar):")
        print("  " + g.stderr.strip().splitlines()[-1][:200])
    ok.append(checar("guarda de leakage roda e nao acha suspeita ALTA no --full",
                     g.returncode == 0 and bool(linhas_guarda)))

    print("\n" + "=" * 74)
    if all(ok):
        print(f"ENSAIO PASSOU ({sum(ok)}/{len(ok)}). O caminho --full esta mecanicamente")
        print("correto. Quando o Renan rodar com a Silver real, o que pode diferir e")
        print("o CONTEUDO do dado, nao a mecanica do pipeline.")
    else:
        print(f"ENSAIO FALHOU ({sum(ok)}/{len(ok)} verificacoes). Corrigir antes da call.")
    print("=" * 74)

    print(f"\nRestaurando o snapshot --local-only (o ensaio sobrescreveu)...")
    subprocess.run(
        [sys.executable, str(BASE / "src" / "preprocessing" / "02_extrair_snapshot.py")],
        capture_output=True, text=True,
    )
    SILVER_FAKE.unlink(missing_ok=True)
    print("Snapshot restaurado e Silver sintetica removida.")
    sys.exit(0 if all(ok) else 1)


if __name__ == "__main__":
    main()
