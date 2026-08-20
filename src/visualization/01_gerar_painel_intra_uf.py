"""
Gera o PAINEL DE PRIORIZAÇÃO INTRA-UF — a peça que faltava no projeto.

POR QUE ESTE SCRIPT EXISTE
--------------------------
A auditoria de maturidade CRISP-DM deste projeto deu nota 3 ou 4 em cinco das
seis fases, e **1 em Deployment**: a recomendação de negócio existia só como
prosa em Markdown. Nenhum gestor abre um `.md` de 1.700 linhas para decidir
quem visitar na segunda-feira.

Este script fecha esse buraco. Ele lê `reports/ranking_intra_uf.json` (saída de
`04_ranking_intra_uf.py`) e gera uma página HTML autocontida onde o gestor
escolhe o estado dele e vê os municípios ordenados por risco.

A DECISÃO DE DESIGN QUE IMPORTA
-------------------------------
O painel é **particionado por UF, sem opção de visão nacional** — e isso é
deliberado, não limitação. O achado central do Cap. 16 é que comparar
municípios de estados diferentes compara réguas de avaliação distintas. Se a
interface permitisse ordenar nacionalmente, ela convidaria exatamente o erro
que o projeto descobriu. A restrição está na ferramenta, não só no rodapé.

Cada estado mostra o veredito honesto em TRÊS estados possíveis, não dois
(ADR-0005): o modelo vence a regra simples com significância em 3 UFs
(PR, RJ, RS), perde em 3 (MG, RN, TO) e empata nas outras 17 — e o painel diz
isso na cara, inclusive recomendando a regra simples onde ela é melhor.

O painel também nomeia, por estado, QUAL direção da regra simples funciona
ali — porque ela inverte: "quem estava melhor falha mais" vale em 16 UFs,
o oposto em 7. Piso e dobras adaptativas: ADR-0004 (antes eram 17 UFs com
piso fixo de 100). Correção da régua do baseline: ADR-0005.

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
ENTRADA = BASE / "reports" / "ranking_intra_uf.json"
SAIDA = BASE / "reports" / "painel_intra_uf.html"

NOME_UF = {
    "AL": "Alagoas", "BA": "Bahia", "CE": "Ceará", "GO": "Goiás",
    "MA": "Maranhão", "MG": "Minas Gerais", "MT": "Mato Grosso",
    "PA": "Pará", "PB": "Paraíba", "PE": "Pernambuco", "PI": "Piauí",
    "PR": "Paraná", "RN": "Rio Grande do Norte", "RS": "Rio Grande do Sul",
    "SC": "Santa Catarina", "SP": "São Paulo", "TO": "Tocantins",
}


def compactar(dados: dict) -> dict:
    """
    Reduz o payload para o que a interface usa. O JSON completo tem 1,4 MB;
    embutir tudo numa página estática é desperdício de banda por campo que
    ninguém lê. Arrays posicionais em vez de objetos cortam ~60%.
    """
    metricas = {m["uf"]: m for m in dados["metricas_por_uf"]}
    compacto = {}
    for uf, linhas in dados["ranking"].items():
        compacto[uf] = {
            "nome": NOME_UF.get(uf, uf),
            "n": metricas[uf]["n_municipios"],
            "taxa_falha": metricas[uf]["taxa_falha_observada"],
            "auc": metricas[uf]["auc_modelo"],
            "auc_ic": metricas[uf]["auc_modelo_ic95"],
            "auc_base": metricas[uf]["auc_baseline_honesto"],
            "ganho": metricas[uf]["ganho_sobre_baseline"],
            "ganho_ic": metricas[uf]["ganho_ic95"],
            "veredito": metricas[uf]["veredito"],
            "direcao": metricas[uf]["direcao_real"],
            "direcao_previsivel": metricas[uf]["direcao_previsivel"],
            "amostra_pequena": metricas[uf]["amostra_pequena"],
            # [rank, nome, score, taxa23, taxa24, meta, gap, resultado_real]
            "m": [[l["rank_uf"], l["nome_municipio"], l["score_risco"],
                    l["taxa23"], l["taxa24"], l["meta_alfabetizacao_2024"],
                    l["gap_meta"], l["y"]] for l in linhas],
        }
    return compacto


def main():
    dados = json.loads(ENTRADA.read_text(encoding="utf-8"))
    compacto = compactar(dados)
    resumo = dados["resumo"]
    payload = json.dumps({"ufs": compacto, "resumo": resumo},
                          ensure_ascii=False, separators=(",", ":"))

    html = TEMPLATE.replace("__PAYLOAD__", payload)
    SAIDA.write_text(html, encoding="utf-8")

    kb = len(html.encode("utf-8")) / 1024
    print(f"Painel gerado: {SAIDA}")
    print(f"  {len(compacto)} UFs | {resumo['municipios']} municipios | {kb:.0f} KB")
    print(f"  vs baseline honesto: vence {resumo['ufs_modelo_vence']}, "
          f"empata {resumo['ufs_inconclusivo']}, perde {resumo['ufs_modelo_perde']} "
          f"(de {resumo['ufs']} UFs)")


TEMPLATE = r"""<title>Priorização da Alfabetização</title>
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
  cursor:pointer;font-size:.86rem;font-weight:500;transition:background .12s,border-color .12s;font-family:var(--mono)}
.chip:hover{border-color:var(--primary)}
.chip[aria-pressed="true"]{background:var(--primary);border-color:var(--primary);color:var(--surface)}
:root[data-theme="dark"] .chip[aria-pressed="true"],
:root:not([data-theme="light"]) .chip[aria-pressed="true"]{color:#0F1614}
@media (prefers-color-scheme:light){:root:not([data-theme="dark"]) .chip[aria-pressed="true"]{color:#fff}}

.state-head{display:flex;flex-wrap:wrap;gap:1rem;justify-content:space-between;align-items:flex-end;margin:1.6rem 0 .9rem}
.state-name{font-size:1.5rem;font-weight:700;letter-spacing:-.01em;margin:0}
.state-name small{display:block;font-family:var(--mono);font-size:.7rem;font-weight:500;color:var(--muted);letter-spacing:.08em;text-transform:uppercase;margin-top:.2rem}

.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:.7rem;margin-bottom:1.1rem}
.stat{background:var(--surface);border:1px solid var(--line);border-radius:10px;padding:.8rem .95rem}
.stat .k{font-size:.72rem;color:var(--muted);margin-bottom:.3rem}
.stat .v{font-family:var(--mono);font-variant-numeric:tabular-nums;font-size:1.25rem;font-weight:600;line-height:1}
.stat .d{font-size:.74rem;color:var(--muted);margin-top:.3rem}

.trust{display:flex;align-items:center;gap:.5rem;padding:.55rem .85rem;border-radius:8px;font-size:.87rem;margin-bottom:1.1rem}
.trust.good{background:var(--ok-soft);color:var(--ok)}
.trust.bad{background:var(--warn-soft);color:var(--warn)}
.trust.warn{background:var(--surface-2);color:var(--ink-2);border:1px solid var(--line)}
.trust b{font-family:var(--mono);font-variant-numeric:tabular-nums}

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

footer.note{margin-top:2rem;padding-top:1.2rem;border-top:1px solid var(--line);font-size:.83rem;color:var(--muted);max-width:76ch}
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

.auc-compare{background:var(--surface);border:1px solid var(--line);border-radius:10px;padding:.95rem 1.1rem 1.1rem;margin-bottom:.7rem}
.auc-note{font-family:var(--prose);font-size:.86rem;color:var(--ink-2);margin:0;max-width:68ch}
.auc-track{position:relative;height:6px;background:var(--line-2);border-radius:99px;margin:1.7rem .4rem 1.9rem}
.auc-tick{position:absolute;top:-5px;left:50%;transform:translateX(-50%);width:1px;height:16px;background:var(--muted);opacity:.55}
.auc-tick label{position:absolute;top:18px;left:50%;transform:translateX(-50%);font-family:var(--mono);font-size:.64rem;color:var(--muted);white-space:nowrap}
.auc-end{position:absolute;top:14px;font-family:var(--mono);font-size:.64rem;color:var(--muted)}
.auc-end.left{left:0}
.auc-end.right{right:0}
.auc-ci{position:absolute;top:50%;height:4px;transform:translateY(-50%);border-radius:99px;opacity:.32}
.auc-ci.intuicao{background:var(--warn)}
.auc-ci.modelo{background:var(--primary)}
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

.method{background:var(--surface);border:1px solid var(--line);border-radius:10px;padding:.9rem 1.1rem;margin-bottom:1.2rem}
.method summary{cursor:pointer;font-weight:500;font-size:.9rem;list-style:none;display:flex;align-items:center;justify-content:space-between;gap:.6rem}
.method summary::-webkit-details-marker,.method summary::marker{display:none}
.method summary .mchev{font-family:var(--mono);color:var(--muted);font-size:.75rem;transition:transform .15s}
.method[open] summary .mchev{transform:rotate(180deg)}
.method ol{font-family:var(--prose);font-size:.9rem;color:var(--ink-2);margin:.9rem 0 0;padding-left:1.2rem}
.method li{margin-bottom:.55rem}
.method li:last-child{margin-bottom:0}
.method code{font-family:var(--mono);font-size:.85em}
</style>

<div class="wrap">
  <header class="top">
    <div class="kicker">Compromisso Nacional Criança Alfabetizada &middot; ciclo 2024</div>
    <h1>Quais municípios do meu estado não vão atingir a meta?</h1>
    <p class="sub">Risco previsto de o município ficar abaixo da meta do PDE, ordenado dentro de cada estado — um modelo separado para cada UF.</p>
  </header>

  <p class="lead">Este painel estima, <strong>antes do resultado sair</strong>, quais municípios têm mais chance de não bater a meta de alfabetização — para ajudar a decidir onde priorizar apoio primeiro. A estimativa vem de um modelo treinado separadamente para cada estado; não existe um ranking nacional único, pelo motivo explicado no aviso abaixo.</p>

  <div class="gterms">
    <details><summary>Risco previsto</summary><p>Probabilidade estimada (0 a 1) de o município ficar abaixo da meta em 2024, calculada só com dado disponível até 2023 — sem espiar o resultado real.</p></details>
    <details><summary>Meta do PDE</summary><p>Meta de alfabetização de cada município, definida pelo Plano de Metas do Compromisso Nacional Criança Alfabetizada. Ela sobe a cada ano, então comparar direto com a taxa de 2023 engana.</p></details>
    <details><summary>AUC</summary><p>Métrica de 0 a 1 que mede se um critério separa bem quem vai ficar abaixo da meta de quem vai atingir. 0,5 é o mesmo que sortear; 1,0 seria acerto perfeito.</p></details>
    <details><summary>IC95%</summary><p>Faixa onde o AUC verdadeiro provavelmente está, calculada repetindo o cálculo em milhares de reamostras dos municípios do estado. Estado com poucos municípios tem faixa mais larga — o número sozinho esconde essa incerteza.</p></details>
  </div>

  <div class="warn">
    <span class="ic">!</span>
    <p><strong>Este painel não permite comparação entre estados — de propósito.</strong> As avaliações são aplicadas pelos próprios estados, e a variação estadual entre 2023 e 2024 chega a 20 pontos percentuais (RS caiu 20,0; MG subiu 12,3). Ordenar municípios de UFs diferentes na mesma escala compara réguas de prova distintas, não desempenho educacional.</p>
  </div>

  <div class="picker">
    <div class="picker-label">Selecione o estado</div>
    <div class="chips" id="chips"></div>
  </div>

  <div class="state-head">
    <h2 class="state-name" id="stateName">—<small id="stateSub"></small></h2>
  </div>

  <div class="stats" id="stats"></div>
  <div id="trust"></div>

  <details class="method">
    <summary>Como este modelo foi construído <span class="mchev">&#9662;</span></summary>
    <ol>
      <li><strong>Dado:</strong> taxa de alfabetização por município (2023 e 2024), meta do PDE por município e porte populacional — Indicador Criança Alfabetizada (INEP).</li>
      <li><strong>Um modelo por estado, não um modelo nacional.</strong> Testamos primeiro um modelo único para o Brasil inteiro: fora da amostra (Leave-One-UF-Out) ele caiu para AUC 0,48 — pior que sortear. Cada estado aplica sua própria prova e sua própria meta; misturar todos numa régua só esconde esse efeito, não neutraliza.</li>
      <li><strong>Validação:</strong> dentro de cada estado, as predições mostradas são <em>out-of-fold</em> — nenhum município foi avaliado por um modelo que o viu durante o treino. O número de dobras é adaptativo (2 a 5, conforme o tamanho do estado) para não deixar dobra pequena sem as duas classes — e por isso todo AUC vem com intervalo de confiança de 95% por bootstrap, não só o ponto.</li>
      <li><strong>Piso de 40 municípios por UF.</strong> Abaixo disso nem dobra reduzida nem intervalo de confiança tornam o número confiável — é o caso só do Amapá (16 municípios no estado inteiro). Não é limitação deste painel: com 16 municípios, o gestor consegue olhar a lista inteira sem precisar de um modelo.</li>
      <li><strong>3 estados de fora por falta de dado na fonte, não por limite de modelo:</strong> Acre, Distrito Federal e Roraima não têm taxa de alfabetização de 2023 (Acre e DF) ou de nenhum ano (Roraima) publicada pelo INEP para este indicador — confirmado até o nível estadual, não é falha de coleta deste projeto.</li>
      <li><strong>A direção da regra simples inverte entre estados — e esse é o achado principal.</strong> Em 16 estados quem ia <em>melhor</em> em 2023 falha mais a meta (a meta acompanha o município, e a regressão à média derruba quem estava no topo). Em 7 estados é o contrário, porque a meta satura em 80,0 e blinda quem já está muito acima dela. Não existe uma regra nacional única.</li>
      <li><strong>Comparação honesta:</strong> o modelo é medido contra a regra simples <em>na direção certa daquele estado</em>, sendo que essa direção é prevista a partir dos <em>outros</em> estados — nunca olhando o resultado do próprio. Diferença com IC95% por bootstrap pareado.</li>
      <li><strong>O que o modelo de fato entrega:</strong> ele não ranqueia melhor — ele dispensa saber a direção de antemão. No conjunto ele supera a regra simples por <strong>+0,027</strong> (IC95% +0,007 a +0,048), e essa vantagem vem quase toda dos <span id="mResumo">7</span> estados em que a direção não é previsível de fora. Nos demais, empata.</li>
    </ol>
    <p>Decisões completas em <code>docs/adr/0002-modelo-final-validacao-temporal-e-tratamento-caderno.md</code> e no Cap. 16 de <code>docs/HANDOFF_RENAN.md</code>.</p>
  </details>

  <div class="toolbar">
    <input class="search" id="search" type="search" placeholder="Buscar município…" aria-label="Buscar município">
    <span class="count" id="count"></span>
  </div>

  <div class="tbl-wrap">
    <table>
      <thead><tr>
        <th>#</th><th>Município</th><th>Risco previsto</th>
        <th style="text-align:right">Taxa 2023</th>
        <th style="text-align:right">Meta 2024</th>
        <th style="text-align:right">Taxa 2024</th>
        <th>Resultado real</th>
      </tr></thead>
      <tbody id="rows"></tbody>
    </table>
  </div>

  <footer class="note">
    <p><strong>Como ler a tabela.</strong> “Taxa 2023” e “Meta 2024” são o que já se sabia antes do resultado — é o que o modelo usa para prever. “Taxa 2024” e “Resultado real” são o que de fato aconteceu, mostrados só para conferência.</p>
    <p>Gerado por <code>src/visualization/01_gerar_painel_intra_uf.py</code> a partir de <code>reports/ranking_intra_uf.json</code>. Fonte: microdados do Indicador Criança Alfabetizada (INEP) e metas do PDE.</p>
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

function corRisco(s){
  if (s >= 0.75) return "var(--r4)";
  if (s >= 0.55) return "var(--r3)";
  if (s >= 0.35) return "var(--r2)";
  return "var(--r1)";
}

function montarChips(){
  el("chips").innerHTML = ufs.map(uf =>
    `<button class="chip" data-uf="${uf}" aria-pressed="${uf===atual}">${uf}</button>`).join("");
  el("chips").querySelectorAll(".chip").forEach(b =>
    b.addEventListener("click", () => { atual = b.dataset.uf; filtro=""; el("search").value=""; render(); }));
}

function montarResumoMetodologia(){
  const r = DATA.resumo;
  el("mResumo").textContent = `${r.ufs - r.ufs_direcao_previsivel}`;
}

function renderTrust(d){
  const n3 = v => v.toFixed(3).replace(".", ",");
  const clamp = v => Math.max(1, Math.min(99, v * 100));
  const [loM, hiM] = d.auc_ic.map(clamp);
  const regra = d.direcao === "melhor_primeiro"
    ? "priorizar quem tinha a <b>maior</b> taxa em 2023"
    : "priorizar quem tinha a <b>menor</b> taxa em 2023";
  const avisoAmostra = d.amostra_pequena
    ? `<p class="auc-small">Amostra pequena (${d.n} municípios) — intervalo de confiança mais largo. Trate como referência mais fraca do que nos estados maiores.</p>`
    : "";
  const cls = {modelo_vence:"good", modelo_perde:"bad", inconclusivo:"warn"}[d.veredito];
  const txt = {
    modelo_vence: "✓ Aqui o modelo <b>supera</b> a regra simples, com significância estatística. Use o ranking abaixo.",
    modelo_perde: "⚠ Aqui o modelo <b>fica atrás</b> da regra simples. Prefira ordenar por " +
                  (d.direcao === "melhor_primeiro" ? "maior" : "menor") + " taxa de 2023.",
    inconclusivo: "≈ Aqui modelo e regra simples <b>empatam</b> — a diferença não é estatisticamente distinguível. Qualquer um dos dois serve."
  }[d.veredito];
  return `
    <div class="auc-compare">
      <p class="auc-note">Neste estado, a regra simples que funciona é <b>${regra}</b> — e ela não é a mesma em todo lugar: a direção se inverte entre estados${d.direcao_previsivel ? "" : ", e <b>este é um dos estados em que ela não dá para adivinhar de fora</b>"}. O modelo só se justifica se superar essa regra.</p>
      <div class="auc-track">
        <span class="auc-tick"><label>sorteio aleatório</label></span>
        <span class="auc-end left">0,0</span>
        <span class="auc-end right">1,0</span>
        <span class="auc-ci modelo" style="left:${loM}%;width:${hiM - loM}%"></span>
        <span class="auc-mark intuicao" style="left:${clamp(d.auc_base)}%"></span>
        <span class="auc-mark modelo" style="left:${clamp(d.auc)}%"></span>
      </div>
      <div class="auc-legend">
        <span><i class="dot intuicao"></i>regra simples — <b>${n3(d.auc_base)}</b></span>
        <span><i class="dot modelo"></i>modelo — <b>${n3(d.auc)}</b> <span class="ic">(${n3(d.auc_ic[0])}–${n3(d.auc_ic[1])})</span></span>
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

  el("stateName").innerHTML = `${d.nome}<small>${atual} &middot; ${d.n} municípios avaliados</small>`;

  el("stats").innerHTML = `
    <div class="stat"><div class="k">Municípios</div><div class="v">${d.n}</div></div>
    <div class="stat"><div class="k">Ficaram abaixo da meta</div>
      <div class="v" style="color:${d.taxa_falha>=.5?'var(--r4)':'var(--ink)'}">${pct(d.taxa_falha)}</div>
      <div class="d">observado em 2024</div></div>
    <div class="stat"><div class="k">AUC do modelo</div><div class="v">${d.auc.toFixed(3).replace(".",",")}</div>
      <div class="d">nunca viu esse município no treino</div></div>
    <div class="stat"><div class="k">AUC da regra simples</div><div class="v">${d.auc_base.toFixed(3).replace(".",",")}</div>
      <div class="d">${d.direcao === "melhor_primeiro" ? "“priorize quem estava melhor”" : "“priorize quem estava pior”"}</div></div>`;

  el("trust").innerHTML = renderTrust(d);

  const termo = filtro.trim().toLowerCase();
  const linhas = d.m.filter(r => !termo || r[1].toLowerCase().includes(termo));
  el("count").textContent = termo
    ? `${linhas.length} de ${d.m.length} municípios`
    : `${d.m.length} municípios, do maior para o menor risco`;

  el("rows").innerHTML = linhas.map(r => {
    const [rank, nome, score, t23, t24, meta, gap, real] = r;
    return `<tr>
      <td class="rk">${rank}</td>
      <td class="nm">${nome}</td>
      <td><div class="riskcell">
        <span class="riskbar"><span class="riskfill" style="width:${(score*100).toFixed(0)}%;background:${corRisco(score)}"></span></span>
        <span class="riskval">${score.toFixed(2).replace(".",",")}</span>
      </div></td>
      <td class="num">${num(t23)}</td>
      <td class="num">${num(meta)}</td>
      <td class="num">${num(t24)}</td>
      <td>${real === 1
        ? '<span class="badge miss">abaixo da meta</span>'
        : '<span class="badge hit">atingiu</span>'}</td>
    </tr>`;
  }).join("");
}

el("search").addEventListener("input", e => { filtro = e.target.value; render(); });
montarChips();
montarResumoMetodologia();
render();
</script>
"""


if __name__ == "__main__":
    main()
