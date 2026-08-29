"""
Comparacao de tecnicas de feature encoding (exigencia literal do enunciado).

O QUE O ENUNCIADO PEDE
----------------------
p.5, descricao da Modelagem Supervisionada: "aplicacao de tecnicas de
**feature encoding**" -- plural. Ate 2026-08-29 o projeto usava so OneHot.
Este e o unico dos 10 gaps do roadmap com respaldo literal do enunciado
(ticket 0008); os outros 9 sao objetivo pedagogico, nao requisito.

O QUE ISTO NAO E
-----------------
**Encoding nao cria informacao.** Transformar `X` nao muda o conteudo
informacional de `X` -- e a mesma variavel escrita de outro jeito. Este script
cumpre requisito de entrega e demonstra dominio de tecnica; nao e busca de
sinal, e nao deve ser lido como tentativa de salvar o modelo aluno-nivel, que
o ADR-0006 e o ADR-0008 ja fecharam por outro caminho.

**Criterio declarado ANTES de rodar:** a expectativa e diferenca desprezivel
entre encodings sobre `caderno`/`rede`/`sigla_uf`. Se algum encoding
"melhorar" de forma relevante, a primeira hipotese e VAZAMENTO, nao
descoberta -- Target encoding sem fold interno vaza o alvo, e esse e o modo
de falha classico da tecnica.

AS DUAS BATERIAS
----------------
**Bateria A -- as categoricas atuais** (`caderno` 12 valores, `rede` 2,
`sigla_uf` 27). Compara OneHot (atual), Target e Frequency. Cardinalidade
media, onde os tres sao aplicaveis e a comparacao e justa.

**Bateria B -- `id_municipio` (4.478 valores).** O caso de livro-texto: OneHot
com 4.478 colunas e inviavel, e Target/Frequency existem exatamente para isso.
Aqui a previsao e mais especifica e mais interessante -- ver secao seguinte.

A PREVISAO SOBRE A BATERIA B (escrita antes de rodar)
------------------------------------------------------
Target encoding de `id_municipio` calcula, por municipio, a media do alvo no
TREINO. O alvo e "nao alfabetizado". Ou seja: a feature resultante e a **taxa
de nao-alfabetizacao municipal de 2023** -- que e literalmente o baseline
`taxa_nao_alfab_t1` do 02_teste_falsificacao.py, com outro nome.

Entao a previsao nao e "vai melhorar" nem "nao vai mudar": e que o modelo com
`id_municipio` target-encoded deve convergir para perto de **0,5816** (o AUC
daquele baseline), nao para 0,6331 (a meta do PDE, que e informacao externa de
politica publica e nao deriva do alvo).

Se isso se confirmar, e demonstracao limpa da tese do projeto: dar ao modelo a
identidade do municipio nao adiciona nada alem do que a taxa municipal ja
dizia. E confirma, por um terceiro caminho independente, que o teto e municipal.

VAZAMENTO: COMO ESTA CONTIDO
-----------------------------
`TargetEncoder` do sklearn faz cross-fitting interno (`cv=5`): a codificacao de
cada linha de treino vem de folds que nao a contem. Sem isso, cada linha
carregaria seu proprio alvo e o AUC de treino iria a ~1,0 com generalizacao
nula. O `fit` acontece so no treino (gate "transformador fitado fora do treino"
de .claude/rules/dados.md); o teste e apenas transformado.

Alem disso o split e TEMPORAL (treina 2023, testa 2024), o mesmo do veredito --
entao um vazamento de alvo apareceria como salto grande e implausivel no teste,
nao como melhora sutil.
"""
import argparse
import importlib.util
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.metrics import roc_auc_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import (
    OneHotEncoder, RobustScaler, TargetEncoder,
)
from xgboost import XGBClassifier

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BASE = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(BASE / "src" / "preprocessing"))
from pipeline_preprocessamento import (  # noqa: E402
    colunas_por_tipo,
)


def _carregar(nome: str, rel: str):
    spec = importlib.util.spec_from_file_location(nome, BASE / rel)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


FALSIF = _carregar("teste_falsificacao", "src/evaluation/02_teste_falsificacao.py")
ROBUST = _carregar("robustez_algoritmo", "src/evaluation/04_robustez_algoritmo.py")

RANDOM_STATE = FALSIF.RANDOM_STATE
ANO_TREINO, ANO_TESTE = FALSIF.ANO_TREINO, FALSIF.ANO_TESTE


class FrequencyEncoder(BaseEstimator, TransformerMixin):
    """
    Substitui cada categoria pela frequencia relativa dela NO TREINO.

    Por que existe: e a alternativa de alta cardinalidade que NAO toca no
    alvo -- entao nao tem como vazar, ao contrario do Target encoding. Serve
    de controle: se Target ganhar muito de Frequency, a diferenca vem de
    informacao do alvo, e vale checar se e sinal ou vazamento.

    Categoria nunca vista no treino recebe 0.0 (frequencia observada nula), que
    e a leitura honesta -- e nao a media, que fingiria conhecimento.
    """

    def fit(self, X, y=None):
        X = self._para_frame(X)
        self.colunas_ = list(X.columns)
        self.mapas_ = {
            c: X[c].astype("object").value_counts(normalize=True).to_dict()
            for c in self.colunas_
        }
        return self

    def transform(self, X):
        X = self._para_frame(X)
        saida = np.column_stack([
            X[c].astype("object").map(self.mapas_[c]).fillna(0.0).to_numpy(dtype=float)
            for c in self.colunas_
        ])
        return saida

    def get_feature_names_out(self, input_features=None):
        return np.array([f"freq__{c}" for c in self.colunas_], dtype=object)

    @staticmethod
    def _para_frame(X):
        if isinstance(X, pd.DataFrame):
            return X
        return pd.DataFrame(X)


def bloco_categorico(estrategia: str):
    """Devolve o transformador do bloco categorico para cada estrategia."""
    imputer = SimpleImputer(strategy="most_frequent")
    if estrategia == "onehot":
        return Pipeline([("imputer", imputer),
                         ("enc", OneHotEncoder(handle_unknown="ignore"))])
    if estrategia == "target":
        # cv=5: cross-fitting INTERNO. Sem isso cada linha carrega o proprio
        # alvo -- o modo de falha classico desta tecnica.
        return Pipeline([("imputer", imputer),
                         ("enc", TargetEncoder(cv=5, random_state=RANDOM_STATE))])
    if estrategia == "frequency":
        return Pipeline([("imputer", imputer), ("enc", FrequencyEncoder())])
    raise ValueError(f"estrategia desconhecida: {estrategia}")


def montar_preprocessador(df: pd.DataFrame, estrategia: str,
                          categoricas: list[str]) -> ColumnTransformer:
    tipos = colunas_por_tipo(df)
    blocos = []
    if tipos["numericas"]:
        blocos.append(("num", Pipeline([
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", RobustScaler()),
        ]), tipos["numericas"]))
    if categoricas:
        blocos.append(("cat", bloco_categorico(estrategia), categoricas))
    if tipos["passthrough"]:
        blocos.append(("bin", SimpleImputer(strategy="most_frequent"),
                       tipos["passthrough"]))
    return ColumnTransformer(blocos, remainder="drop")


def rodar(df, treino, teste, y, categoricas, estrategias, rotulo,
          score_baseline, auc_baseline, extras: list[str] = ()):
    print("\n" + "=" * 74)
    print(rotulo)
    print("=" * 74)
    print(f"Categoricas: {categoricas}")

    feats = (colunas_por_tipo(df)["numericas"] + list(categoricas)
             + colunas_por_tipo(df)["passthrough"])
    resultados = {}
    for est in estrategias:
        pipe = Pipeline([
            ("preprocessador", montar_preprocessador(df, est, list(categoricas))),
            ("modelo", XGBClassifier(**FALSIF.PARAMS_XGB)),
        ])
        pipe.fit(treino[feats], treino["_y"])
        score = pipe.predict_proba(teste[feats])[:, 1]
        auc = float(roc_auc_score(y, score))
        n_col = pipe.named_steps["preprocessador"].transform(treino[feats].head(5)).shape[1]
        ic = ROBUST.ic_bootstrap_pareado(y, score, score_baseline, alphas=(0.05,))
        resultados[est] = {
            "roc_auc": auc,
            "n_colunas_apos_encoding": int(n_col),
            "vs_baseline": ic,
        }
        d = ic["intervalos"]["ic95"]
        print(f"  {est:<10} AUC {auc:.4f}  ({n_col:>4} colunas)  "
              f"vs baseline {ic['diferenca_observada']:+.4f} "
              f"[{d['inferior']:+.4f}, {d['superior']:+.4f}]")
    return resultados


def main():
    parser = argparse.ArgumentParser(description="Comparacao de encodings (ticket 0008)")
    parser.add_argument("--so-bateria-a", action="store_true",
                        help="Roda so as categoricas atuais, sem id_municipio.")
    args = parser.parse_args()

    df = FALSIF.carregar()
    treino = df[df["ano"] == ANO_TREINO]
    teste = df[df["ano"] == ANO_TESTE].copy()
    y = teste["_y"].to_numpy()

    baselines = FALSIF.baselines_municipais(df)
    aucs_b = {n: float(roc_auc_score(y, s.loc[teste.index].to_numpy()))
              for n, s in baselines.items()}
    melhor = max(aucs_b, key=lambda k: aucs_b[k])
    score_baseline = baselines[melhor].loc[teste.index].to_numpy()

    print("=" * 74)
    print("COMPARACAO DE TECNICAS DE FEATURE ENCODING (ticket 0008)")
    print("=" * 74)
    print(f"Split temporal: treino {ANO_TREINO} (n={len(treino):,}) -> "
          f"teste {ANO_TESTE} (n={len(teste):,})".replace(",", "."))
    print(f"Baselines: " + ", ".join(f"{k}={v:.4f}" for k, v in aucs_b.items()))
    print(f"Comparacao contra o melhor: {melhor} ({aucs_b[melhor]:.4f})")
    print("\nLembrete de metodo: encoding NAO cria informacao. Melhora relevante")
    print("aqui e suspeita de vazamento antes de ser descoberta.")

    cat_atuais = colunas_por_tipo(df)["categoricas"]
    saida = {
        "aviso": ("Encoding nao cria informacao. Este relatorio cumpre a "
                  "exigencia literal do enunciado (p.5, 'tecnicas de feature "
                  "encoding', plural) e demonstra dominio de tecnica. Nao e "
                  "tentativa de salvar o modelo aluno-nivel."),
        "desenho": {
            "split": f"temporal, treina {ANO_TREINO}, testa {ANO_TESTE}",
            "n_treino": int(len(treino)), "n_teste": int(len(teste)),
            "baseline_comparado": melhor,
            "auc_baseline": aucs_b[melhor],
            "aucs_baselines": aucs_b,
            "contencao_de_vazamento": ("TargetEncoder com cv=5 (cross-fitting "
                                       "interno); fit so no treino; split temporal"),
        },
        "bateria_a_categoricas_atuais": rodar(
            df, treino, teste, y, cat_atuais,
            ["onehot", "target", "frequency"],
            "BATERIA A -- categoricas atuais (cardinalidade baixa/media)",
            score_baseline, aucs_b[melhor]),
    }

    if not args.so_bateria_a:
        # id_municipio nao e feature declarada (esta em COLUNAS_ID). Entra aqui
        # SO como demonstracao de alta cardinalidade, e o resultado nao volta
        # para o modelo de producao.
        cat_b = cat_atuais + ["id_municipio"]
        print(f"\nCardinalidade de id_municipio: {df['id_municipio'].nunique()} valores")
        print("OneHot fica de fora da bateria B: 4.478 colunas e o problema que")
        print("Target/Frequency existem para resolver.")
        saida["bateria_b_alta_cardinalidade"] = rodar(
            df, treino, teste, y, cat_b, ["target", "frequency"],
            "BATERIA B -- id_municipio (alta cardinalidade)",
            score_baseline, aucs_b[melhor])
        saida["bateria_b_previsao_registrada"] = (
            "Escrita antes de rodar: target encoding de id_municipio calcula a "
            "media do alvo por municipio no treino, que E a taxa de "
            "nao-alfabetizacao municipal de 2023 -- o baseline "
            f"taxa_nao_alfab_t1 ({aucs_b.get('taxa_nao_alfab_t1', float('nan')):.4f}). "
            "Previsao: converge para perto desse valor, nao para o da meta do PDE."
        )

    destino = BASE / "reports" / "comparacao_encodings.json"
    destino.write_text(json.dumps(saida, indent=2, ensure_ascii=False),
                       encoding="utf-8")
    print(f"\nGravado: {destino.relative_to(BASE)}")


if __name__ == "__main__":
    main()
