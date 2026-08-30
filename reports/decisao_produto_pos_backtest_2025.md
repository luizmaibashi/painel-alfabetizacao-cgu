# Decisão de produto após o backtest prospectivo de 2025

**Decisão:** posicionar a entrega como **inteligência pública de priorização
municipal intra-UF, com uso condicional**, e não como ranking nacional nem
como previsão individual de alunos.

## Evidência que muda a decisão

O modelo foi congelado com dados de 2023->2024 e avaliado no ciclo de 2025
sem acessar o alvo de 2025 no treino. Em 5.285 municípios de 23 UFs, alcançou
AUC ponderada de **0,6167**, ante **0,4523** da regra simples cuja direção já
era conhecida em 2024: ganho de **+0,1644**. O IC bootstrap pareado de 1.000
reamostragens declara vitória em 14 UFs, incerteza em 8 e derrota no CE.
Fonte e números reproduzíveis: `reports/backtest_prospectivo_2025.json`.

Isso demonstra valor preditivo fora do ciclo em que o modelo foi ajustado.
Também impede uma promessa excessiva: a evidência é local ao estado, e não
autoriza comparar municípios entre UFs nem automatizar decisão sobre alunos.

## Produto que faz sentido agora

| Situação medida no backtest | Comportamento do produto |
|---|---|
| UF em que o modelo vence | Exibir ranking municipal de prioridade e seus drivers; apoiar triagem humana de busca ativa e alocação de apoio. |
| CE, onde o baseline vence | Exibir a regra simples, sem score do modelo como recomendação. |
| UF inconclusiva | Exibir somente diagnóstico/monitoramento; não sugerir ordem de ação. |
| Comparação entre estados ou decisão por aluno | Bloquear: as escalas e os sinais disponíveis não sustentam esses usos. |

O painel existente é uma demonstração histórica de 2024. Ele não deve ser
apresentado como ferramenta operacional até ser regenerado com os vereditos
temporais acima e com os bloqueios de uso condicional.

## Próxima etapa de maior valor

1. Regenerar o painel com o contrato de uso condicional de 2025 (14 UFs,
   baseline no CE e abstenção nas 8 restantes), preservando rastreabilidade
   da fonte e data de corte.
2. Instituir atualização anual: ao publicar o resultado do ano, executar o
   mesmo backtest antes de mudar a regra de qualquer UF.
3. Para atacar a dor antes da avaliação, integrar somente dados legítimos e
   disponíveis no início do ano — frequência, trajetória escolar e contexto
   socioeconômico/escolar agregados — com chave adequada e governança LGPD.
4. Avaliar ganho incremental e equidade por subgrupos antes de qualquer
   piloto. O ranking deve orientar revisão humana e oferta de apoio, nunca
   negar direito ou rotular uma criança.

Assim, a entrega acadêmica permanece auditável e ganha uma trajetória real:
um sistema de decisão limitado pela evidência, que aprende a cada ciclo em
vez de vender certeza onde ela não existe.
