"""
Gera o PAINEL DE PRIORIZAÇÃO INTRA-UF — ciclo 2025, com contrato de uso condicional.

POR QUE ESTE SCRIPT EXISTE
--------------------------
A auditoria CRISP-DM deste projeto deu nota 1 em Deployment: a recomendação de
negócio existia só como prosa em Markdown. Este script fecha esse buraco — lê o
ranking prospectivo de 2025 e gera uma página HTML autocontida onde o gestor
escolhe o estado dele e vê os municípios ordenados por risco.

O QUE MUDOU EM 2025
-------------------
O painel antigo era um retrato histórico de 2024. O Inep publicou a planilha
municipal de 2025 em 01/04/2026, e `src/evaluation/05_backtest_prospectivo_2025.py`
testou o modelo fora do ciclo de treino: congelado em 2023->2024, avaliado em
2024->2025 sem tuning nem alvo de 2025. Resultado por UF, não nacional:

  - 14 UFs: o modelo vence a regra simples com IC95% inteiramente positivo
    -> painel mostra o RANKING DO MODELO;
  - CE: o modelo perde para a regra simples (IC95% inteiramente negativo)
    -> painel mostra a REGRA SIMPLES, sem score do modelo como recomendação;
  - 8 UFs: inconclusivo (IC95% cruza zero)
    -> painel SE ABSTÉM: só diagnóstico, sem sugerir ordem de ação.

A DECISÃO DE DESIGN QUE IMPORTA
-------------------------------
O painel é particionado por UF, SEM visão nacional — deliberado, não limitação.
Comparar municípios de estados diferentes compara réguas de avaliação distintas
(as provas são aplicadas pelos próprios estados). O payload não tem eixo
nacional; a restrição está na ferramenta, não só no rodapé.

FONTE E RASTREABILIDADE
-----------------------
Entrada: reports/ranking_prospectivo_2025.json (gerado pelo backtest, carrega
fonte oficial, SHA-256 da planilha, data de publicação e data de corte).

SAÍDA
-----
    reports/painel_intra_uf.html — autocontido, sem dependência externa
"""
import json
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BASE = Path(__file__).resolve().parents[2]
ENTRADA = BASE / "reports" / "ranking_prospectivo_2025.json"
SAIDA = BASE / "reports" / "painel_intra_uf.html"


def main():
    dados = json.loads(ENTRADA.read_text(encoding="utf-8"))
    payload = json.dumps({
        "ufs": dados["ufs"],
        "resumo": dados["resumo"],
        "fonte": dados["fonte"],
        "ciclo": dados["ciclo"],
        "data_publicacao_inep": dados["data_publicacao_inep"],
        "aviso_validade": dados["aviso_validade"],
    }, ensure_ascii=False, separators=(",", ":"))

    html = TEMPLATE.replace("__PAYLOAD__", payload)
    SAIDA.write_text(html, encoding="utf-8")

    r = dados["resumo"]
    kb = len(html.encode("utf-8")) / 1024
    print(f"Painel gerado: {SAIDA}")
    print(f"  {r['ufs']} UFs | {r['municipios']} municipios | {kb:.0f} KB")
    print(f"  contrato 2025: ranking do modelo em {r['ufs_ranking_modelo']}, "
          f"regra simples em {r['ufs_regra_simples']}, "
          f"abstencao em {r['ufs_abster']}")


TEMPLATE = r"""<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Priorização da Alfabetização</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;500;600;700&family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,600;1,8..60,400&family=IBM+Plex+Mono:wght@400;500;600&display=swap" rel="stylesheet">
<style>
:root{
  --bg:#EFF2F1; --surface:#FFFFFF; --surface-2:#F7F9F8;
  --ink:#16211F; --ink-2:#3A4744; --muted:#67746F; --line:#D3DAD7; --line-2:#E4E9E7;
  --primary:#0F5C58; --primary-soft:#DCEAE7;
  --r1:#E9D9A8; --r2:#DFBB72; --r3:#CE8F49; --r4:#B4553C;
  --ok:#2E6B4F; --ok-soft:#DEEBE2; --warn:#8A5A1E; --warn-soft:#F3E7D2;
  --shadow:0 1px 2px rgba(22,33,31,.05),0 10px 28px -14px rgba(22,33,31,.22);
  --ui:"Archivo",-apple-system,"Segoe UI",sans-serif;
  --prose:"Source Serif 4",Georgia,serif;
  --mono:"IBM Plex Mono","Consolas",monospace;
}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){
  --bg:#101614; --surface:#18211F; --surface-2:#1E2825;
  --ink:#E7EBE9; --ink-2:#C3CCC8; --muted:#8B9793; --line:#2C3835; --line-2:#232C2A;
  --primary:#5CC2B5; --primary-soft:#16302D;
  --r1:#5E5433; --r2:#7E6435; --r3:#A2703C; --r4:#C96A4E;
  --ok:#6DBE95; --ok-soft:#15291F; --warn:#D2A75E; --warn-soft:#2B2314;
  --shadow:0 1px 2px rgba(0,0,0,.4),0 10px 28px -14px rgba(0,0,0,.7);
}}
:root[data-theme="dark"]{
  --bg:#101614; --surface:#18211F; --surface-2:#1E2825;
  --ink:#E7EBE9; --ink-2:#C3CCC8; --muted:#8B9793; --line:#2C3835; --line-2:#232C2A;
  --primary:#5CC2B5; --primary-soft:#16302D;
  --r1:#5E5433; --r2:#7E6435; --r3:#A2703C; --r4:#C96A4E;
  --ok:#6DBE95; --ok-soft:#15291F; --warn:#D2A75E; --warn-soft:#2B2314;
  --shadow:0 1px 2px rgba(0,0,0,.4),0 10px 28px -14px rgba(0,0,0,.7);
}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font-family:var(--ui);font-size:16px;line-height:1.5;-webkit-font-smoothing:antialiased}
@media (prefers-reduced-motion:reduce){*{transition:none!important;animation:none!important}}
::selection{background:var(--primary-soft);color:var(--ink)}
button,select,input{font:inherit;color:inherit}
:focus-visible{outline:2px solid var(--primary);outline-offset:2px;border-radius:3px}

.wrap{max-width:1120px;margin:0 auto;padding:clamp(1.5rem,4vw,2.75rem) clamp(1rem,3vw,2rem) 4rem}

header.top{margin-bottom:1.5rem}
.kicker{font-family:var(--mono);font-size:.7rem;letter-spacing:.13em;text-transform:uppercase;color:var(--primary);margin-bottom:.6rem}
h1{font-size:clamp(1.6rem,3.4vw,2.2rem);font-weight:700;letter-spacing:-.02em;line-height:1.1;margin:0 0 .5rem;text-wrap:balance}
.sub{color:var(--ink-2);max-width:62ch;margin:0;font-size:1rem}

.warn{display:grid;grid-template-columns:auto 1fr;gap:.9rem;align-items:start;
  background:var(--warn-soft);border-left:3px solid var(--warn);border-radius:0 10px 10px 0;
  padding:.95rem 1.2rem;margin:1.4rem 0 1.8rem}
.warn .ic{font-family:var(--mono);font-weight:600;color:var(--warn);font-size:.95rem;line-height:1.4}
.warn p{margin:0;font-family:var(--prose);font-size:.94rem;color:var(--ink-2);max-width:74ch}
.warn strong{color:var(--ink)}

.picker{margin-bottom:1.2rem}
.picker-label{font-family:var(--mono);font-size:.68rem;letter-spacing:.1em;text-transform:uppercase;color:var(--muted);margin-bottom:.55rem}
.chips{display:flex;flex-wrap:wrap;gap:.4rem}
.chip{background:var(--surface);border:1px solid var(--line);border-radius:7px;padding:.42rem .7rem;
  cursor:pointer;font-size:.86rem;font-weight:500;transition:background .12s,border-color .12s;font-family:var(--mono);
  display:flex;align-items:center;gap:.4rem}
.chip:hover{border-color:var(--primary)}
.chip[aria-pressed="true"]{background:var(--primary);border-color:var(--primary);color:var(--surface)}
.chip .mk{width:6px;height:6px;border-radius:50%;flex:none}
.chip .mk.ranking_modelo{background:var(--ok)}
.chip .mk.regra_simples{background:var(--warn)}
.chip .mk.abster{background:var(--muted)}
.chip[aria-pressed="true"] .mk{outline:1px solid var(--surface)}
:root[data-theme="dark"] .chip[aria-pressed="true"],
:root:not([data-theme="light"]) .chip[aria-pressed="true"]{color:#0F1614}
@media (prefers-color-scheme:light){:root:not([data-theme="dark"]) .chip[aria-pressed="true"]{color:#fff}}

.legend-uf{display:flex;flex-wrap:wrap;gap:.3rem 1.1rem;font-size:.76rem;color:var(--muted);margin-top:.55rem;font-family:var(--mono)}
.legend-uf i{display:inline-block;width:6px;height:6px;border-radius:50%;margin-right:.35rem}
.legend-uf i.ranking_modelo{background:var(--ok)}
.legend-uf i.regra_simples{background:var(--warn)}
.legend-uf i.abster{background:var(--muted)}

.state-head{display:flex;flex-wrap:wrap;gap:1rem;justify-content:space-between;align-items:flex-end;margin:1.6rem 0 .9rem}
.state-name{font-size:1.5rem;font-weight:700;letter-spacing:-.01em;margin:0}
.state-name small{display:block;font-family:var(--mono);font-size:.7rem;font-weight:500;color:var(--muted);letter-spacing:.08em;text-transform:uppercase;margin-top:.2rem}

.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:.7rem;margin-bottom:1.1rem}
.stat{background:var(--surface);border:1px solid var(--line);border-radius:10px;padding:.8rem .95rem}
.stat .k{font-size:.72rem;color:var(--muted);margin-bottom:.3rem}
.stat .v{font-family:var(--mono);font-variant-numeric:tabular-nums;font-size:1.25rem;font-weight:600;line-height:1}
.stat .d{font-size:.74rem;color:var(--muted);margin-top:.3rem}

.trust{display:flex;align-items:flex-start;gap:.5rem;padding:.7rem .95rem;border-radius:8px;font-size:.9rem;margin-bottom:1.1rem;line-height:1.45}
.trust.good{background:var(--ok-soft);color:var(--ok)}
.trust.bad{background:var(--warn-soft);color:var(--warn)}
.trust.warn{background:var(--surface-2);color:var(--ink-2);border:1px solid var(--line)}
.trust b{font-family:var(--mono);font-variant-numeric:tabular-nums}

.auc-compare{background:var(--surface);border:1px solid var(--line);border-radius:10px;padding:.95rem 1.1rem 1.1rem;margin-bottom:.7rem}
.auc-note{font-family:var(--prose);font-size:.86rem;color:var(--ink-2);margin:0;max-width:68ch}
.auc-track{position:relative;height:6px;background:var(--line-2);border-radius:99px;margin:1.7rem .4rem 1.9rem}
.auc-tick{position:absolute;top:-5px;left:50%;transform:translateX(-50%);width:1px;height:16px;background:var(--muted);opacity:.55}
.auc-tick label{position:absolute;top:18px;left:50%;transform:translateX(-50%);font-family:var(--mono);font-size:.64rem;color:var(--muted);white-space:nowrap}
.auc-end{position:absolute;top:14px;font-family:var(--mono);font-size:.64rem;color:var(--muted)}
.auc-end.left{left:0}
.auc-end.right{right:0}
.auc-mark{position:absolute;top:50%;width:13px;height:13px;border-radius:50%;transform:translate(-50%,-50%);border:2px solid var(--surface)}
.auc-mark.intuicao{background:var(--warn)}
.auc-mark.modelo{background:var(--primary)}
.auc-legend{display:flex;flex-wrap:wrap;gap:.4rem 1.3rem;font-size:.82rem;color:var(--ink-2)}
.auc-legend .dot{display:inline-block;width:8px;height:8px;border-radius:50%;margin-right:.4rem}
.auc-legend .dot.intuicao{background:var(--warn)}
.auc-legend .dot.modelo{background:var(--primary)}
.auc-legend b{font-family:var(--mono);color:var(--ink)}
.auc-legend .ic{font-family:var(--mono);color:var(--muted);font-size:.9em}
.auc-small{font-family:var(--mono);font-size:.72rem;color:var(--warn);margin:.7rem 0 0}

.toolbar{display:flex;flex-wrap:wrap;gap:.6rem;align-items:center;margin-bottom:.8rem}
.search{flex:1;min-width:180px;background:var(--surface);border:1px solid var(--line);border-radius:8px;padding:.5rem .75rem;font-size:.9rem}
.search::placeholder{color:var(--muted)}
.count{font-family:var(--mono);font-size:.78rem;color:var(--muted)}

.tbl-wrap{overflow-x:auto;background:var(--surface);border:1px solid var(--line);border-radius:12px;box-shadow:var(--shadow)}
table{border-collapse:collapse;width:100%;min-width:660px;font-size:.88rem}
thead th{position:sticky;top:0;background:var(--surface-2);font-family:var(--mono);font-size:.66rem;letter-spacing:.07em;
  text-transform:uppercase;color:var(--muted);font-weight:500;text-align:left;padding:.6rem .8rem;border-bottom:1px solid var(--line);white-space:nowrap}
tbody td{padding:.52rem .8rem;border-bottom:1px solid var(--line-2);vertical-align:middle;white-space:nowrap}
tbody tr:last-child td{border-bottom:none}
tbody tr:hover{background:var(--surface-2)}
td.rk{font-family:var(--mono);color:var(--muted);font-variant-numeric:tabular-nums;width:44px}
td.nm{font-weight:500;white-space:normal;min-width:150px}
td.num{font-family:var(--mono);font-variant-numeric:tabular-nums;text-align:right;color:var(--ink-2)}
.riskcell{display:flex;align-items:center;gap:.55rem;min-width:132px}
.riskbar{flex:1;height:7px;border-radius:99px;background:var(--line-2);overflow:hidden;min-width:52px}
.riskfill{height:100%;border-radius:99px}
.riskval{font-family:var(--mono);font-size:.8rem;font-variant-numeric:tabular-nums;width:34px;text-align:right}
.badge{display:inline-block;font-family:var(--mono);font-size:.68rem;padding:.14rem .42rem;border-radius:5px;font-weight:500}
.badge.miss{background:var(--warn-soft);color:var(--warn)}
.badge.hit{background:var(--ok-soft);color:var(--ok)}

footer.note{margin-top:2rem;padding-top:1.2rem;border-top:1px solid var(--line);font-size:.83rem;color:var(--muted);max-width:82ch}
footer.note p{margin:0 0 .5rem}
footer.note code{font-family:var(--mono);font-size:.9em}

.lead{font-family:var(--prose);font-size:1.05rem;line-height:1.55;color:var(--ink-2);max-width:68ch;margin:1.3rem 0 1rem}
.lead strong{color:var(--ink)}

.gterms{display:flex;flex-wrap:wrap;align-items:flex-start;gap:.5rem;margin-bottom:1.5rem}
.gterms details{background:var(--surface);border:1px solid var(--line);border-radius:8px;padding:.4rem .7rem;max-width:260px}
.gterms summary{cursor:pointer;font-family:var(--mono);font-size:.78rem;color:var(--primary);list-style:none;display:flex;align-items:center;gap:.4rem}
.gterms summary::-webkit-details-marker,.gterms summary::marker{display:none}
.gterms summary::after{content:"o que é?";font-family:var(--ui);font-size:.72rem;color:var(--muted)}
.gterms details[open] summary::after{content:"fechar"}
.gterms p{font-family:var(--prose);font-size:.86rem;color:var(--ink-2);margin:.5rem 0 .1rem}

.method{background:var(--surface);border:1px solid var(--line);border-radius:10px;padding:.9rem 1.1rem;margin-bottom:1.2rem}
.method summary{cursor:pointer;font-weight:500;font-size:.9rem;list-style:none;display:flex;align-items:center;justify-content:space-between;gap:.6rem}
.method summary::-webkit-details-marker,.method summary::marker{display:none}
.method summary .mchev{font-family:var(--mono);color:var(--muted);font-size:.75rem;transition:transform .15s}
.method[open] summary .mchev{transform:rotate(180deg)}
.method ol{font-family:var(--prose);font-size:.9rem;color:var(--ink-2);margin:.9rem 0 0;padding-left:1.2rem}
.method li{margin-bottom:.55rem}
.method li:last-child{margin-bottom:0}
.method code{font-family:var(--mono);font-size:.85em}

.provenance{font-family:var(--mono);font-size:.74rem;color:var(--muted);background:var(--surface-2);border:1px solid var(--line-2);border-radius:8px;padding:.7rem .9rem;margin-bottom:1.4rem;line-height:1.7;word-break:break-all}
.provenance b{color:var(--ink-2)}
</style>

<div class="wrap">
  <header class="top">
    <div class="kicker" id="kicker">Compromisso Nacional Criança Alfabetizada</div>
    <h1>Quais municípios do meu estado não vão atingir a meta?</h1>
    <p class="sub">Risco previsto de o município ficar abaixo da meta do PDE no próximo ciclo, ordenado dentro de cada estado — com uso condicional por UF, definido por um teste fora do ciclo de treino.</p>
  </header>

  <p class="lead">Este painel estima, <strong>antes do resultado sair</strong>, quais municípios têm mais chance de não bater a meta de alfabetização — para ajudar a decidir onde priorizar apoio primeiro. O modelo foi <strong>congelado com dados até 2024 e testado no ciclo de 2025</strong> sem ver o resultado de 2025. Onde ele provou vencer uma regra simples, o painel mostra o ranking do modelo. Onde perdeu, mostra a regra simples. Onde o teste foi inconclusivo, <strong>o painel se abstém</strong> — mostra só o diagnóstico.</p>

  <div class="provenance" id="provenance"></div>

  <div class="gterms">
    <details><summary>Risco previsto</summary><p>Probabilidade estimada (0 a 1) de o município ficar abaixo da meta no próximo ciclo, calculada só com dado do ciclo anterior — sem espiar o resultado real.</p></details>
    <details><summary>Meta do PDE</summary><p>Meta de alfabetização de cada município, definida pelo Plano de Metas do Compromisso Nacional Criança Alfabetizada. Ela sobe a cada ano, então comparar direto com a taxa do ano anterior engana.</p></details>
    <details><summary>Regra simples</summary><p>Ordenar os municípios só pela taxa do ano anterior, numa direção fixa. Em alguns estados "quem estava melhor falha mais" (regressão à média); em outros é o contrário (a meta satura e protege quem já está no topo). O modelo só se justifica se superar essa regra.</p></details>
    <details><summary>Backtest prospectivo</summary><p>Testar o modelo num ciclo que ele nunca viu: treina com 2023→2024, prevê 2024→2025 e só então compara com o que de fato aconteceu em 2025. É a evidência mais forte de que a previsão funciona fora do laboratório.</p></details>
    <details><summary>IC95%</summary><p>Faixa onde o ganho verdadeiro sobre a regra simples provavelmente está, por bootstrap pareado. Se a faixa cruza o zero, não dá para afirmar que o modelo é melhor — é o caso das 8 UFs em que o painel se abstém.</p></details>
  </div>

  <div class="warn">
    <span class="ic">!</span>
    <p><strong>Este painel não permite comparação entre estados — de propósito.</strong> As avaliações são aplicadas pelos próprios estados, e a variação estadual entre anos chega a 20 pontos percentuais. Ordenar municípios de UFs diferentes na mesma escala compara réguas de prova distintas, não desempenho educacional. Também <strong>não serve para decisão sobre um aluno</strong>: é priorização municipal para orientar busca ativa e alocação de apoio, nunca para negar direito ou rotular uma criança.</p>
  </div>

  <div class="picker">
    <div class="picker-label">Selecione o estado</div>
    <div class="chips" id="chips"></div>
    <div class="legend-uf">
      <span><i class="ranking_modelo"></i>ranking do modelo (venceu o backtest)</span>
      <span><i class="regra_simples"></i>regra simples (modelo perdeu)</span>
      <span><i class="abster"></i>abstenção (inconclusivo)</span>
    </div>
  </div>

  <div class="state-head">
    <h2 class="state-name" id="stateName">—<small id="stateSub"></small></h2>
  </div>

  <div class="stats" id="stats"></div>
  <div id="trust"></div>

  <details class="method">
    <summary>Como este modelo foi construído e testado <span class="mchev">&#9662;</span></summary>
    <ol>
      <li><strong>Dado:</strong> taxa de alfabetização por município (2023, 2024 e 2025), meta do PDE por município e porte populacional — planilha oficial de resultados e metas do Inep, publicada em <span id="mData">01/04/2026</span>.</li>
      <li><strong>Um modelo por estado, não um modelo nacional.</strong> Um modelo único para o Brasil, testado fora da amostra (Leave-One-UF-Out), caiu para AUC 0,48 — pior que sortear. Cada estado aplica sua própria prova e sua própria meta.</li>
      <li><strong>Backtest prospectivo:</strong> o modelo foi congelado na transição 2023→2024 — mesmos hiperparâmetros, sem retuning — e usado para prever o ciclo de 2025. O alvo de 2025 nunca entrou no treino. A comparação é contra a regra simples cuja direção já funcionava naquele estado em 2024.</li>
      <li><strong>Veredito por UF, com IC95% bootstrap pareado (1.000 reamostragens):</strong> em <span id="mVence">14</span> estados o ganho do modelo sobre a regra simples tem intervalo inteiramente positivo → o painel usa o ranking do modelo. No <span id="mPerde">Ceará</span> o intervalo é inteiramente negativo → o painel usa a regra simples. Em <span id="mAbster">8</span> estados o intervalo cruza zero → o painel se abstém, mostrando só o diagnóstico.</li>
      <li><strong>Abstenção é uma resposta, não uma falha.</strong> Onde não há evidência de que o modelo supere a regra simples, recomendar qualquer um dos dois seria vender certeza inexistente. O painel mostra os números e não sugere ordem de ação.</li>
      <li><strong>Reavaliação anual.</strong> A cada publicação de um novo ciclo pelo Inep, o mesmo backtest roda de novo antes de mudar a regra de qualquer UF.</li>
    </ol>
    <p>Decisões completas em <code>docs/adr/0002-modelo-final-validacao-temporal-e-tratamento-caderno.md</code>, <code>reports/decisao_produto_pos_backtest_2025.md</code> e <code>reports/diagnostico_ufs_inconclusivas.md</code>.</p>
  </details>

  <div class="toolbar">
    <input class="search" id="search" type="search" placeholder="Buscar município…" aria-label="Buscar município">
    <span class="count" id="count"></span>
  </div>

  <div class="tbl-wrap">
    <table>
      <thead><tr>
        <th>#</th><th>Município</th><th id="thOrd">Risco previsto</th>
        <th style="text-align:right">Taxa 2024</th>
        <th style="text-align:right">Meta 2025</th>
        <th style="text-align:right">Taxa 2025</th>
        <th>Resultado real</th>
      </tr></thead>
      <tbody id="rows"></tbody>
    </table>
  </div>

  <footer class="note">
    <p><strong>Como ler a tabela.</strong> “Taxa 2024” e “Meta 2025” são o que já se sabia antes do resultado de 2025 — é o que o modelo usa para prever. “Taxa 2025” e “Resultado real” são o que de fato aconteceu, mostrados só para conferência do backtest.</p>
    <p id="footProv"></p>
    <p>Gerado por <code>src/visualization/01_gerar_painel_intra_uf.py</code> a partir de <code>reports/ranking_prospectivo_2025.json</code> (saída de <code>src/evaluation/05_backtest_prospectivo_2025.py</code>).</p>
  </footer>
</div>

<script>
const DATA = __PAYLOAD__;
const ufs = Object.keys(DATA.ufs).sort();
let atual = ufs.includes("MG") ? "MG" : ufs[0];
let filtro = "";

const el = id => document.getElementById(id);
const pct = v => (v*100).toFixed(1).replace(".", ",") + "%";
const num = v => v === null || v === undefined ? "—" : Number(v).toFixed(1).replace(".", ",");
const n3 = v => v.toFixed(3).replace(".", ",");

function corRisco(s){
  if (s >= 0.75) return "var(--r4)";
  if (s >= 0.55) return "var(--r3)";
  if (s >= 0.35) return "var(--r2)";
  return "var(--r1)";
}

function montarProvenance(){
  const f = DATA.fonte;
  el("provenance").innerHTML =
    `<b>Fonte:</b> Inep — Indicador Criança Alfabetizada, planilha municipal de resultados e metas.<br>` +
    `<b>Arquivo:</b> ${f.arquivo}<br>` +
    `<b>SHA-256:</b> ${f.sha256}<br>` +
    `<b>Publicação Inep:</b> ${DATA.data_publicacao_inep} &nbsp;·&nbsp; <b>Ciclo avaliado:</b> ${DATA.ciclo} &nbsp;·&nbsp; <b>Data de corte do treino:</b> 2024`;
  el("footProv").innerHTML =
    `${DATA.aviso_validade} Fonte oficial: <code>${f.url}</code>.`;
  el("mData").textContent = DATA.data_publicacao_inep.split("-").reverse().join("/");
}

function montarChips(){
  el("chips").innerHTML = ufs.map(uf =>
    `<button class="chip" data-uf="${uf}" aria-pressed="${uf===atual}"><span class="mk ${DATA.ufs[uf].uso}"></span>${uf}</button>`).join("");
  el("chips").querySelectorAll(".chip").forEach(b =>
    b.addEventListener("click", () => { atual = b.dataset.uf; filtro=""; el("search").value=""; render(); }));
}

function montarResumoMetodologia(){
  const r = DATA.resumo;
  el("mVence").textContent = r.ufs_ranking_modelo;
  el("mAbster").textContent = r.ufs_abster;
}

function renderTrust(d){
  const clamp = v => Math.max(1, Math.min(99, v * 100));
  const avisoAmostra = d.amostra_pequena
    ? `<p class="auc-small">Amostra pequena (${d.n} municípios) — intervalo de confiança mais largo. Trate como referência mais fraca do que nos estados maiores.</p>`
    : "";
  const regraTxt = d.direcao === "melhor_primeiro"
    ? "priorizar quem tinha a <b>maior</b> taxa em 2024"
    : "priorizar quem tinha a <b>menor</b> taxa em 2024";

  const cls = {ranking_modelo:"good", regra_simples:"bad", abster:"warn"}[d.uso];
  const txt = {
    ranking_modelo: "✓ No backtest de 2025, o modelo <b>superou</b> a regra simples neste estado, com o intervalo de confiança inteiramente positivo (ganho <b>" + (d.ganho>=0?"+":"") + n3(d.ganho) + "</b>, IC95% " + n3(d.ganho_ic[0]) + " a " + n3(d.ganho_ic[1]) + "). <b>Use o ranking abaixo.</b>",
    regra_simples: "⚠ No backtest de 2025, o modelo <b>ficou atrás</b> da regra simples neste estado, com o intervalo inteiramente negativo (ganho <b>" + n3(d.ganho) + "</b>, IC95% " + n3(d.ganho_ic[0]) + " a " + n3(d.ganho_ic[1]) + "). A tabela abaixo está ordenada pela <b>regra simples</b> (" + regraTxt + "); o score do modelo é mostrado só para referência.",
    abster: "≈ No backtest de 2025, a diferença entre modelo e regra simples <b>não é estatisticamente distinguível</b> neste estado (ganho <b>" + (d.ganho>=0?"+":"") + n3(d.ganho) + "</b>, IC95% " + n3(d.ganho_ic[0]) + " a " + n3(d.ganho_ic[1]) + ", cruzando zero). <b>O painel não recomenda ordem de ação aqui</b> — a tabela é só diagnóstico. Olhe a lista inteira e complemente com conhecimento local."
  }[d.uso];

  return `
    <div class="auc-compare">
      <p class="auc-note">Comparação medida no ciclo de 2025, que o modelo nunca viu no treino. A régua da esquerda é o sorteio aleatório (0,5); mais à direita é melhor.</p>
      <div class="auc-track">
        <span class="auc-tick"><label>sorteio aleatório</label></span>
        <span class="auc-end left">0,0</span>
        <span class="auc-end right">1,0</span>
        <span class="auc-mark intuicao" style="left:${clamp(d.auc_baseline)}%"></span>
        <span class="auc-mark modelo" style="left:${clamp(d.auc_modelo)}%"></span>
      </div>
      <div class="auc-legend">
        <span><i class="dot intuicao"></i>regra simples — <b>${n3(d.auc_baseline)}</b></span>
        <span><i class="dot modelo"></i>modelo — <b>${n3(d.auc_modelo)}</b></span>
        <span>diferença <b>${d.ganho >= 0 ? "+" : ""}${n3(d.ganho)}</b> <span class="ic">IC95% ${n3(d.ganho_ic[0])} a ${n3(d.ganho_ic[1])}</span></span>
      </div>
      ${avisoAmostra}
    </div>
    <div class="trust ${cls}">${txt}</div>`;
}

function render(){
  const d = DATA.ufs[atual];
  el("chips").querySelectorAll(".chip").forEach(b =>
    b.setAttribute("aria-pressed", String(b.dataset.uf === atual)));

  el("stateName").innerHTML = `${d.nome}<small>${atual} &middot; ${d.n} municípios avaliados no backtest 2025</small>`;

  const rotuloOrd = d.uso === "regra_simples"
    ? "ordenado pela regra simples"
    : d.uso === "abster" ? "score do modelo (diagnóstico)" : "ranking do modelo";
  el("thOrd").textContent = d.uso === "regra_simples" ? "Score do modelo (ref.)" : "Risco previsto";

  el("stats").innerHTML = `
    <div class="stat"><div class="k">Municípios</div><div class="v">${d.n}</div></div>
    <div class="stat"><div class="k">Ficaram abaixo da meta</div>
      <div class="v" style="color:${d.taxa_falha_2025>=.5?'var(--r4)':'var(--ink)'}">${pct(d.taxa_falha_2025)}</div>
      <div class="d">observado em 2025</div></div>
    <div class="stat"><div class="k">AUC do modelo (2025)</div><div class="v">${n3(d.auc_modelo)}</div>
      <div class="d">fora do ciclo de treino</div></div>
    <div class="stat"><div class="k">AUC da regra simples</div><div class="v">${n3(d.auc_baseline)}</div>
      <div class="d">${d.direcao === "melhor_primeiro" ? "“priorize quem estava melhor”" : "“priorize quem estava pior”"}</div></div>`;

  el("trust").innerHTML = renderTrust(d);

  const termo = filtro.trim().toLowerCase();
  const linhas = d.m.filter(r => !termo || r[1].toLowerCase().includes(termo));
  el("count").textContent = termo
    ? `${linhas.length} de ${d.m.length} municípios`
    : `${d.m.length} municípios — ${rotuloOrd}`;

  el("rows").innerHTML = linhas.map(r => {
    const [rank, nome, score, t24, meta, t25, real] = r;
    return `<tr>
      <td class="rk">${rank}</td>
      <td class="nm">${nome}</td>
      <td><div class="riskcell">
        <span class="riskbar"><span class="riskfill" style="width:${(score*100).toFixed(0)}%;background:${corRisco(score)}"></span></span>
        <span class="riskval">${score.toFixed(2).replace(".",",")}</span>
      </div></td>
      <td class="num">${num(t24)}</td>
      <td class="num">${num(meta)}</td>
      <td class="num">${num(t25)}</td>
      <td>${real === 1
        ? '<span class="badge miss">abaixo da meta</span>'
        : '<span class="badge hit">atingiu</span>'}</td>
    </tr>`;
  }).join("");
}

el("search").addEventListener("input", e => { filtro = e.target.value; render(); });
montarProvenance();
montarChips();
montarResumoMetodologia();
render();
</script>
"""


if __name__ == "__main__":
    main()
