"""
Guarda de determinismo de execucao — ADR-0007.

POR QUE ESTE ARQUIVO EXISTE
----------------------------
Medido em 2026-08-25: `02_teste_falsificacao.py` produzia AUCs diferentes a
cada execucao, com a MESMA seed (`random_state=42`), o MESMO snapshot e o
MESMO codigo. A unica variavel era quantas threads o processo tinha:

    OMP_NUM_THREADS=1 -> 0,6047     OMP_NUM_THREADS=6 -> 0,6025
    OMP_NUM_THREADS=2 -> 0,6061     OMP_NUM_THREADS=8 -> 0,6048

Amplitude de 0,0036 — cerca de 13% do efeito medido (a diferenca para o
baseline e -0,028). Foi assim que o numero 0,6026 entrou no ADR-0006 e no
README sem ser reproduzivel.

CAUSA: `tree_method="hist"` paraleliza a reducao do histograma. Soma em ponto
flutuante nao e associativa — (a+b)+c != a+(b+c) por arredondamento — entao a
ordem em que as threads combinam os parciais entra no resultado. A seed
controla QUAIS numeros entram na conta; nao controla EM QUE ORDEM o
processador vai soma-los.

O QUE ESTE TESTE PROTEGE
-------------------------
O risco real nao e o bug voltar sozinho: e alguem (inclusive um agente de IA)
ver `n_jobs=1` num script de ML, achar que e desperdicio de CPU e "otimizar"
para `n_jobs=-1`. O comentario no codigo explica o porque, mas comentario nao
falha build. Este teste falha.

O QUE ELE DELIBERADAMENTE NAO PROIBE
-------------------------------------
`n_jobs=-1` em `RandomForest`, `GridSearchCV` e `cross_val_predict` continua
permitido. Eles paralelizam UNIDADES INDEPENDENTES (uma arvore, uma combinacao
de hiperparametro, uma dobra), entao o efeito de ordem e ordens de grandeza
menor que no `tree_method="hist"` — mas NAO e zero, e a versao anterior desta
docstring afirmava que era.

CORRECAO MEDIDA EM 2026-08-30. A afirmacao anterior ("nao ha soma compartilhada,
entao nao ha dependencia de ordem") esta errada para `RandomForest`:
`predict_proba` MEDIA as arvores, e essa media e uma reducao paralelizada em
blocos por thread. Medido diretamente:

    RandomForestClassifier(n_estimators=200, max_depth=6, random_state=42)
    n_jobs=-1 vs n_jobs=-1 : bit-identico? False
    n_jobs=-1 vs n_jobs=1  : bit-identico? False
    max |diff| = 3.3e-16  (epsilon de float64)

Por que a verificacao original passou mesmo assim: ela foi feita em
`04_ranking_intra_uf.py`, que grava metricas arredondadas em 4 casas — e 3,3e-16
some no arredondamento. Continua verdade que aquele script e bit a bit identico
a 1, 2 e 6 threads (reconfirmado em 2026-08-30). O que mudou foi o
`05_backtest_prospectivo_2025.py`: ele passa os scores por um bootstrap de 1.000
reamostragens, e o percentil 97,5 AMPLIFICA o epsilon — basta uma reamostragem
cruzar o corte para o limite do IC mudar na 4a casa. Efeito observado:

    RS, ganho_ic95 superior:  0,2717 (1 thread)  vs  0,2716 (6 threads)

Escopo do efeito, medido: 1 valor em 23 UFs; `auc_modelo`, `auc_baseline`,
`ganho_sobre_baseline`, o bloco `resumo` e os 23 vereditos ficam identicos. A
menor margem entre um IC e o zero (PE, 0,0035) e 35x maior que a variacao
observada (0,0001), entao nenhum veredito pode virar por este ruido. E divida
de reproducibilidade bit-a-bit, nao erro de resultado — registrada como debito
aberto no ADR-0007 em vez de corrigida as pressas, porque forcar `n_jobs=1` no
backtest muda o custo de execucao e merece decisao explicita, nao um patch
lateral no meio de uma auditoria.

A regra, entao, nao e "paralelismo e ruim" nem "sobre unidades independentes e
seguro" — e "toda reducao em ponto flutuante paralelizada introduz ruido de
ordem; o que muda e a MAGNITUDE, e se o pipeline a jusante amplifica ou
arredonda esse ruido".
"""
import ast
from pathlib import Path

import pytest

BASE = Path(__file__).resolve().parents[1]
SRC = BASE / "src"

# Parametros que ligam a construcao paralela de histograma no XGBoost/LightGBM.
TREE_METHODS_PARALELOS = {"hist", "gpu_hist", "approx"}


def _chamadas_com_tree_method(caminho: Path):
    """Toda chamada no arquivo que passa `tree_method`, com seus kwargs."""
    arvore = ast.parse(caminho.read_text(encoding="utf-8"), filename=str(caminho))
    for no in ast.walk(arvore):
        if not isinstance(no, ast.Call):
            continue
        kwargs = {kw.arg: kw.value for kw in no.keywords if kw.arg}
        if "tree_method" not in kwargs:
            continue
        valor = kwargs["tree_method"]
        if isinstance(valor, ast.Constant) and valor.value in TREE_METHODS_PARALELOS:
            yield no, kwargs


def _arquivos_fonte():
    return sorted(p for p in SRC.rglob("*.py") if "__pycache__" not in p.parts)


def test_existe_pelo_menos_um_alvo_para_este_guarda():
    """
    Se ninguem mais usa `tree_method` parametrizado, este teste virou decoracao
    e passa por vacuidade — o modo de falha silenciosa que o AGENTS.md chama de
    "lista de cobertura falha aberta". Melhor falhar e forcar a revisao.
    """
    alvos = [(p, no) for p in _arquivos_fonte() for no, _ in _chamadas_com_tree_method(p)]
    assert alvos, (
        "Nenhuma chamada com tree_method parelelizavel encontrada em src/. "
        "Ou o projeto parou de usar XGBoost, ou o parser deste teste quebrou. "
        "Nos dois casos, revisar o ADR-0007 antes de apagar este arquivo."
    )


@pytest.mark.parametrize("caminho", _arquivos_fonte(), ids=lambda p: p.name)
def test_xgboost_com_hist_usa_n_jobs_1(caminho):
    """
    `tree_method` paralelizavel exige `n_jobs=1` explicito.

    Ausencia do parametro tambem reprova: o default do XGBoost e usar todos os
    nucleos, que e exatamente o comportamento nao reprodutivel. Omitir nao e
    neutro — e optar pelo default errado em silencio.
    """
    problemas = []
    for no, kwargs in _chamadas_com_tree_method(caminho):
        n_jobs = kwargs.get("n_jobs")
        if n_jobs is None:
            problemas.append(
                f"linha {no.lineno}: usa tree_method paralelizavel e NAO declara "
                f"n_jobs — o default usa todos os nucleos e nao reproduz."
            )
        elif not (isinstance(n_jobs, ast.Constant) and n_jobs.value == 1):
            achado = ast.unparse(n_jobs)
            problemas.append(
                f"linha {no.lineno}: tree_method paralelizavel com n_jobs={achado}. "
                f"So n_jobs=1 reproduz entre maquinas."
            )

    assert not problemas, (
        f"\n{caminho.relative_to(BASE)} quebra o determinismo de execucao "
        f"(ADR-0007):\n  " + "\n  ".join(problemas) + "\n\n"
        "Medido: o AUC oscila 0,6025-0,6061 so por contagem de threads, com a "
        "mesma seed. Se voce precisa mesmo de paralelismo aqui, o caminho e "
        "revisar o ADR-0007 -- nao relaxar este teste."
    )
