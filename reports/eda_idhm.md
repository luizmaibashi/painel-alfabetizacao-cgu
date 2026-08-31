# EDA — idhm (n=5.565)
**Origem:** `dados_externos/idhm_municipio_2010.csv`
**Gerado por:** `src/preprocessing/01_eda_alunos.py`

## Colunas e tipos

|                                 | tipo    |
|:--------------------------------|:--------|
| ano                             | int64   |
| id_municipio                    | int64   |
| expectativa_vida                | float64 |
| fecundidade_total               | float64 |
| mortalidade_1                   | float64 |
| mortalidade_5                   | float64 |
| razao_dependencia               | float64 |
| prob_sobrevivencia_40           | float64 |
| prob_sobrevivencia_60           | float64 |
| taxa_envelhecimento             | float64 |
| expectativa_anos_estudo         | float64 |
| taxa_analfabetismo_11_a_14      | float64 |
| taxa_analfabetismo_15_a_17      | float64 |
| taxa_analfabetismo_15_mais      | float64 |
| taxa_analfabetismo_18_a_24      | float64 |
| taxa_analfabetismo_18_mais      | float64 |
| taxa_analfabetismo_25_a_29      | float64 |
| taxa_analfabetismo_25_mais      | float64 |
| taxa_atraso_0_basico            | float64 |
| taxa_atraso_0_fundamental       | float64 |
| taxa_atraso_0_medio             | float64 |
| taxa_atraso_1_basico            | float64 |
| taxa_atraso_1_fundamental       | float64 |
| taxa_atraso_1_medio             | float64 |
| taxa_atraso_2_basico            | float64 |
| taxa_atraso_2_fundamental       | float64 |
| taxa_atraso_2_medio             | float64 |
| taxa_freq_bruta_basico          | float64 |
| taxa_freq_bruta_fundamental     | float64 |
| taxa_freq_bruta_medio           | float64 |
| taxa_freq_bruta_pre             | float64 |
| taxa_freq_bruta_superior        | float64 |
| taxa_freq_liquida_basico        | float64 |
| taxa_freq_liquida_fundamental   | float64 |
| taxa_freq_liquida_medio         | float64 |
| taxa_freq_liquida_pre           | float64 |
| taxa_freq_liquida_superior      | float64 |
| taxa_freq_0_3                   | float64 |
| taxa_freq_11_14                 | float64 |
| taxa_freq_15_17                 | float64 |
| taxa_freq_18_24                 | float64 |
| taxa_freq_25_29                 | float64 |
| taxa_freq_4_5                   | float64 |
| taxa_freq_4_6                   | float64 |
| taxa_freq_5_6                   | float64 |
| taxa_freq_6                     | float64 |
| taxa_freq_6_14                  | float64 |
| taxa_freq_6_17                  | float64 |
| taxa_freq_fundamental_15_17     | float64 |
| taxa_freq_fundamental_18_24     | float64 |
| taxa_freq_fundamental_4_5       | float64 |
| taxa_freq_medio_18_24           | float64 |
| taxa_freq_medio_6_14            | float64 |
| taxa_freq_superior_15_17        | float64 |
| taxa_fundamental_11_13          | float64 |
| taxa_fundamental_12_14          | float64 |
| taxa_fundamental_15_17          | float64 |
| taxa_fundamental_16_18          | float64 |
| taxa_fundamental_18_24          | float64 |
| taxa_fundamental_18_mais        | float64 |
| taxa_fundamental_25_mais        | float64 |
| taxa_medio_18_20                | float64 |
| taxa_medio_18_24                | float64 |
| taxa_medio_18_mais              | float64 |
| taxa_medio_19_21                | float64 |
| taxa_medio_25_mais              | float64 |
| taxa_superior_25_mais           | float64 |
| renda_pc_max_quintil_1          | float64 |
| renda_pc_max_quintil_2          | float64 |
| renda_pc_max_quintil_3          | float64 |
| renda_pc_max_quintil_4          | float64 |
| renda_pc_max_decil_9            | float64 |
| indice_gini                     | float64 |
| prop_pobreza_extrema            | float64 |
| prop_pobreza_extrema_criancas   | float64 |
| prop_pobreza                    | float64 |
| prop_pobreza_criancas           | float64 |
| prop_vulner_pobreza             | float64 |
| prop_vulner_pobreza_criancas    | float64 |
| prop_renda_10_ricos             | float64 |
| prop_renda_20_pobres            | float64 |
| prop_renda_20_ricos             | float64 |
| prop_renda_40_pobres            | float64 |
| prop_renda_60_pobres            | float64 |
| prop_renda_80_pobres            | float64 |
| prop_renda_trabalho             | float64 |
| razao_10_ricos_40_pobres        | float64 |
| razao_20_ricos_40_pobres        | float64 |
| renda_pc                        | float64 |
| renda_pc_quintil_1              | float64 |
| renda_pc_decil_10               | float64 |
| renda_pc_quintil_2              | float64 |
| renda_pc_quintil_3              | float64 |
| renda_pc_quintil_4              | float64 |
| renda_pc_quintil_5              | float64 |
| renda_pc_exc_renda_nula         | float64 |
| renda_pc_pobreza_extrema        | float64 |
| renda_pc_pobreza                | float64 |
| renda_pc_vulner_pobreza         | float64 |
| indice_theil                    | float64 |
| prop_trabalhadores_conta_proria | float64 |
| prop_empregadores               | float64 |
| prop_ocupados_agropecuaria      | float64 |
| prop_ocupados_comercio          | float64 |
| prop_ocupados_construcao        | float64 |
| prop_ocupados_extracao          | float64 |
| prop_ocupados_formalizacao      | float64 |
| prop_ocupados_fundamental       | float64 |
| prop_ocupados_medio             | float64 |
| prop_ocupados_servicos          | float64 |
| prop_ocupados_siup              | float64 |
| prop_ocupados_superior          | float64 |
| prop_ocupados_transformacao     | float64 |
| prop_ocupados_renda_0           | float64 |
| prop_ocupados_renda_1_sm        | float64 |
| prop_ocupados_renda_2_sm        | float64 |
| prop_ocupados_renda_3_sm        | float64 |
| prop_ocupados_renda_5_sm        | float64 |
| renda_media_ocupados            | float64 |
| taxa_atividade                  | float64 |
| taxa_atividade_10_14            | float64 |
| taxa_atividade_15_17            | float64 |
| taxa_atividade_18_24            | float64 |
| taxa_atividade_18_mais          | float64 |
| taxa_atividade_25_29            | float64 |
| taxa_desocupacao                | float64 |
| taxa_desocupacao_10_14          | float64 |
| taxa_desocupacao_15_17          | float64 |
| taxa_desocupacao_18_24          | float64 |
| taxa_desocupacao_18_mais        | float64 |
| taxa_desocupacao_25_29          | float64 |
| indice_treil_trabalho           | float64 |
| taxa_ocupados_carteira          | float64 |
| taxa_ocupados_setor_publico     | float64 |
| taxa_ocupados_sem_carteira      | float64 |
| taxa_agua_encanada              | float64 |
| taxa_banheiro_agua_encanada     | float64 |
| taxa_densidade_2_mais           | float64 |
| taxa_coleta_lixo                | float64 |
| taxa_energia_eletrica           | float64 |
| taxa_agua_esgoto_inadequados    | float64 |
| taxa_paredes_inadequados        | float64 |
| taxa_criancas_dom_sem_fund      | float64 |
| taxa_criancas_fora_escola_4_5   | float64 |
| taxa_criancas_fora_escola_6_14  | float64 |
| taxa_dom_sem_fund               | float64 |
| taxa_dom_vulner_sem_fund        | float64 |
| taxa_sem_fund_informal          | float64 |
| taxa_mulheres_com_filho_10_14   | float64 |
| taxa_mulheres_com_filho_15_17   | float64 |
| taxa_mulheres_chefe_filho_15m   | float64 |
| taxa_nest_ntrab_vulner_15_24    | float64 |
| taxa_vulner_desloc_1_hora       | float64 |
| taxa_dom_vulner_dep_idoso       | float64 |
| taxa_sem_energia_eletrica       | float64 |
| populacao_homens_0_4            | int64   |
| populacao_homens_10_14          | int64   |
| populacao_homens_15_19          | int64   |
| populacao_homens_20_24          | int64   |
| populacao_homens_25_29          | int64   |
| populacao_homens_30_34          | int64   |
| populacao_homens_35_39          | int64   |
| populacao_homens_40_44          | int64   |
| populacao_homens_45_49          | int64   |
| populacao_homens_50_54          | int64   |
| populacao_homens_55_59          | int64   |
| populacao_homens_5_9            | int64   |
| populacao_homens_60_64          | int64   |
| populacao_homens_65_69          | int64   |
| populacao_homens_70_74          | int64   |
| populacao_homens_75_79          | int64   |
| populacao_homens                | int64   |
| populacao_homens_80_mais        | int64   |
| populacao_mulheres_0_4          | int64   |
| populacao_mulheres_10_14        | int64   |
| populacao_mulheres_15_19        | int64   |
| populacao_mulheres_20_24        | int64   |
| populacao_mulheres_25_29        | int64   |
| populacao_mulheres_30_34        | int64   |
| populacao_mulheres_35_39        | int64   |
| populacao_mulheres_40_44        | int64   |
| populacao_mulheres_45_49        | int64   |
| populacao_mulheres_50_54        | int64   |
| populacao_mulheres_55_59        | int64   |
| populacao_mulheres_5_9          | int64   |
| populacao_mulheres_60_64        | int64   |
| populacao_mulheres_65_69        | int64   |
| populacao_mulheres_70_74        | int64   |
| populacao_mulheres_75_79        | int64   |
| populacao_mulheres_80_mais      | int64   |
| populacao_mulheres              | int64   |
| populacao_1_menos               | int64   |
| populacao_11_14                 | int64   |
| populacao_11_13                 | int64   |
| populacao_12_14                 | int64   |
| populacao_1_3                   | int64   |
| populacao_15_mais               | int64   |
| populacao_15_17                 | int64   |
| populacao_15_24                 | int64   |
| populacao_16_18                 | int64   |
| populacao_18_mais               | int64   |
| populacao_18_20                 | int64   |
| populacao_18_24                 | int64   |
| populacao_19_21                 | int64   |
| populacao_25_mais               | int64   |
| populacao_4                     | int64   |
| populacao_5                     | int64   |
| populacao_6                     | int64   |
| populacao_6_10                  | int64   |
| populacao_6_17                  | int64   |
| populacao_65_mais               | int64   |
| populacao                       | int64   |
| populacao_urbana                | int64   |
| populacao_rural                 | int64   |
| populacao_dom_pp                | int64   |
| populacao_dom_pp_exc_renda_nula | int64   |
| pea                             | int64   |
| pea_10_14                       | int64   |
| pea_15_17                       | int64   |
| pea_18_mais                     | int64   |
| pia                             | int64   |
| pia_10_14                       | int64   |
| pia_15_17                       | int64   |
| pia_18_mais                     | int64   |
| indice_escolaridade             | float64 |
| indice_frequencia_escolar       | float64 |
| idhm                            | float64 |
| idhm_e                          | float64 |
| idhm_l                          | float64 |
| idhm_r                          | float64 |

## Checklist CRISP-DM (`.claude/rules/dados.md`)

### 1. Duplicatas

- Linha inteira: **0**

### 2. Colunas constantes / quase-constantes

- `ano`: **100.0%** concentrado em `np.int64(2010)` — sem variância útil.

### 3. Valores sentinela em numéricas

- Nenhum valor sentinela clássico com frequência relevante.

Faixas das numéricas:

|                                 |            min |             50% |              max |
|:--------------------------------|---------------:|----------------:|-----------------:|
| ano                             | 2010           |  2010           |   2010           |
| id_municipio                    |    1.10002e+06 |     3.14621e+06 |      5.30011e+06 |
| expectativa_vida                |   65.3         |    73.47        |     78.64        |
| fecundidade_total               |    1.21        |     2.13        |      4.89        |
| mortalidade_1                   |    8.49        |    16.9         |     46.8         |
| mortalidade_5                   |    9.98        |    19.42        |     50.94        |
| razao_dependencia               |   29.17        |    49.59        |    118.04        |
| prob_sobrevivencia_40           |   88.83        |    93.89        |     97.09        |
| prob_sobrevivencia_60           |   71.98        |    82.92        |     90.81        |
| taxa_envelhecimento             |    1.46        |     8.38        |     20.42        |
| expectativa_anos_estudo         |    4.34        |     9.47        |     12.83        |
| taxa_analfabetismo_11_a_14      |    0           |     2.02        |     38.98        |
| taxa_analfabetismo_15_a_17      |    0           |     1.71        |     33.53        |
| taxa_analfabetismo_15_mais      |    0.95        |    13.12        |     44.4         |
| taxa_analfabetismo_18_a_24      |    0           |     2.26        |     36.37        |
| taxa_analfabetismo_18_mais      |    0.97        |    14.11        |     47.64        |
| taxa_analfabetismo_25_a_29      |    0           |     3.87        |     36.13        |
| taxa_analfabetismo_25_mais      |    1.1         |    16.46        |     57.18        |
| taxa_atraso_0_basico            |   23.84        |    60.98        |     92.48        |
| taxa_atraso_0_fundamental       |   25.92        |    64.82        |     95.41        |
| taxa_atraso_0_medio             |    0           |    72.27        |    100           |
| taxa_atraso_1_basico            |    4.33        |    18.8         |     32.31        |
| taxa_atraso_1_fundamental       |    3.01        |    18.88        |     35.58        |
| taxa_atraso_1_medio             |    0           |    20.32        |     63.08        |
| taxa_atraso_2_basico            |    0.75        |    19.64        |     58.62        |
| taxa_atraso_2_fundamental       |    0           |    16.07        |     51.74        |
| taxa_atraso_2_medio             |    0           |     6.56        |     55.31        |
| taxa_freq_bruta_basico          |   58.71        |    99.03        |    168.88        |
| taxa_freq_bruta_fundamental     |   64.71        |   110.42        |    195.59        |
| taxa_freq_bruta_medio           |    0           |    66.06        |    168.64        |
| taxa_freq_bruta_pre             |    3.91        |    64.62        |    165.74        |
| taxa_freq_bruta_superior        |    0.96        |    17.18        |     76.78        |
| taxa_freq_liquida_basico        |   47.26        |    88.94        |     98.75        |
| taxa_freq_liquida_fundamental   |   47.92        |    93.37        |    100           |
| taxa_freq_liquida_medio         |    0           |    41.04        |     91.3         |
| taxa_freq_liquida_pre           |    3.91        |    55.56        |    100           |
| taxa_freq_liquida_superior      |    0           |     8.43        |     43.89        |
| taxa_freq_0_3                   |    0           |    17.52        |     70.22        |
| taxa_freq_11_14                 |   54.46        |    96.98        |    100           |
| taxa_freq_15_17                 |   50.11        |    82.33        |    100           |
| taxa_freq_18_24                 |    4.52        |    25.78        |     58.77        |
| taxa_freq_25_29                 |    0           |    10.05        |     46.29        |
| taxa_freq_4_5                   |   13.03        |    82.14        |    100           |
| taxa_freq_4_6                   |   32           |    87.05        |    100           |
| taxa_freq_5_6                   |   41.51        |    94.13        |    100           |
| taxa_freq_6                     |   48.12        |    97.38        |    100           |
| taxa_freq_6_14                  |   51.77        |    97.62        |    100           |
| taxa_freq_6_17                  |   52.55        |    93.47        |    100           |
| taxa_freq_fundamental_15_17     |    0           |    27.32        |     68.95        |
| taxa_freq_fundamental_18_24     |    0           |     2.72        |     35.31        |
| taxa_freq_fundamental_4_5       |    0           |    14.85        |     70.13        |
| taxa_freq_medio_18_24           |    0           |     6.48        |     25.51        |
| taxa_freq_medio_6_14            |    0           |     1.83        |      9.66        |
| taxa_freq_superior_15_17        |    0           |     0.72        |     12.17        |
| taxa_fundamental_11_13          |   34.62        |    86.58        |    100           |
| taxa_fundamental_12_14          |   36.67        |    87.6         |    100           |
| taxa_fundamental_15_17          |    6.89        |    55.42        |     96.81        |
| taxa_fundamental_16_18          |   11.4         |    64.6         |     98.4         |
| taxa_fundamental_18_24          |   17.48        |    68.78        |     97.85        |
| taxa_fundamental_18_mais        |   12.03        |    38.44        |     80.03        |
| taxa_fundamental_25_mais        |    9.41        |    32.33        |     78.04        |
| taxa_medio_18_20                |    1.91        |    35.14        |     88.03        |
| taxa_medio_18_24                |    1.81        |    39.45        |     90.62        |
| taxa_medio_18_mais              |    3.04        |    23.48        |     66.23        |
| taxa_medio_19_21                |    1.6         |    40.31        |     94.67        |
| taxa_medio_25_mais              |    3.46        |    20.13        |     65.86        |
| taxa_superior_25_mais           |    0.28        |     4.81        |     33.68        |
| renda_pc_max_quintil_1          |    0           |   150           |    585           |
| renda_pc_max_quintil_2          |    0           |   253.67        |    945           |
| renda_pc_max_quintil_3          |   31.25        |   382           |   1496.67        |
| renda_pc_max_quintil_4          |  150           |   575           |   2900           |
| renda_pc_max_decil_9            |  250           |   866.67        |   5000           |
| indice_gini                     |    0.28        |     0.49        |      0.8         |
| prop_pobreza_extrema            |    0           |     6.24        |     69.67        |
| prop_pobreza_extrema_criancas   |    0           |     9.95        |     72.43        |
| prop_pobreza                    |    0           |    18.14        |     78.59        |
| prop_pobreza_criancas           |    0           |    30.03        |     84.66        |
| prop_vulner_pobreza             |    1.97        |    42.23        |     91.57        |
| prop_vulner_pobreza_criancas    |    2.45        |    61.04        |     95.44        |
| prop_renda_10_ricos             |   22.26        |    37.62        |     75.34        |
| prop_renda_20_pobres            |    0           |     3.72        |      9.26        |
| prop_renda_20_ricos             |    0           |    53.56        |     81.54        |
| prop_renda_40_pobres            |    0           |    12.17        |     22.5         |
| prop_renda_60_pobres            |    0           |    25.53        |     40.12        |
| prop_renda_80_pobres            |    0           |    46.43        |     63.11        |
| prop_renda_trabalho             |   27.43        |    70.58        |     95.24        |
| razao_10_ricos_40_pobres        |    0           |    12.55        |    221.1         |
| razao_20_ricos_40_pobres        |    0           |     8.85        |    146.11        |
| renda_pc                        |   96.25        |   467.65        |   2043.74        |
| renda_pc_quintil_1              |    0           |    89.67        |    437.76        |
| renda_pc_decil_10               |  396.56        |  1698.26        |  10610.9         |
| renda_pc_quintil_2              |    0           |   199.8         |    731.02        |
| renda_pc_quintil_3              |   21.7         |   311.85        |   1175.12        |
| renda_pc_quintil_4              |   78.99        |   479.33        |   2057.78        |
| renda_pc_quintil_5              |  302.47        |  1208.88        |   6735.07        |
| renda_pc_exc_renda_nula         |  112.2         |   473.72        |   2043.74        |
| renda_pc_pobreza_extrema        |    0           |    32.51        |     70           |
| renda_pc_pobreza                |    0           |    80.62        |    132.25        |
| renda_pc_vulner_pobreza         |   41.53        |   149.78        |    217.08        |
| indice_theil                    |    0.14        |     0.44        |      1.36        |
| prop_trabalhadores_conta_proria |    1.36        |    22.66        |     76.68        |
| prop_empregadores               |    0           |     1.06        |      8.92        |
| prop_ocupados_agropecuaria      |    0.06        |    36.45        |     85.12        |
| prop_ocupados_comercio          |    0.74        |    10.05        |     36.57        |
| prop_ocupados_construcao        |    0.14        |     6.06        |     26.3         |
| prop_ocupados_extracao          |    0           |     0.12        |     28.19        |
| prop_ocupados_formalizacao      |    2.97        |    42.85        |     89.11        |
| prop_ocupados_fundamental       |   13.08        |    45.18        |     86.47        |
| prop_ocupados_medio             |    4.16        |    29.12        |     73.65        |
| prop_ocupados_servicos          |    8.5         |    31.89        |     78.23        |
| prop_ocupados_siup              |    0           |     0.65        |     12.95        |
| prop_ocupados_superior          |    0.32        |     6.4         |     37.53        |
| prop_ocupados_transformacao     |    0           |     6.53        |     65.11        |
| prop_ocupados_renda_0           |    0           |     9.41        |     73.93        |
| prop_ocupados_renda_1_sm        |    4.53        |    35.81        |     89.33        |
| prop_ocupados_renda_2_sm        |   36.49        |    83.86        |     99.14        |
| prop_ocupados_renda_3_sm        |   51.45        |    91.94        |    100           |
| prop_ocupados_renda_5_sm        |   68.28        |    96.82        |    100           |
| renda_media_ocupados            |  136.42        |   761.72        |   3177.26        |
| taxa_atividade                  |   17.29        |    55.64        |     91.27        |
| taxa_atividade_10_14            |    0           |     8.71        |     72.55        |
| taxa_atividade_15_17            |    0.83        |    32.51        |     87.59        |
| taxa_atividade_18_24            |   16.39        |    66.94        |     99.09        |
| taxa_atividade_18_mais          |   21.18        |    64.01        |     95.6         |
| taxa_atividade_25_29            |   17.72        |    75.64        |    100           |
| taxa_desocupacao                |    0           |     6.26        |     41.93        |
| taxa_desocupacao_10_14          |    0           |    10.17        |    100           |
| taxa_desocupacao_15_17          |    0           |    16.11        |    100           |
| taxa_desocupacao_18_24          |    0           |    12.01        |     56.85        |
| taxa_desocupacao_18_mais        |    0           |     5.66        |     38.45        |
| taxa_desocupacao_25_29          |    0           |     7           |     44.35        |
| indice_treil_trabalho           |    0.12        |     0.38        |      1.4         |
| taxa_ocupados_carteira          |    0.9         |    26.76        |     83.21        |
| taxa_ocupados_setor_publico     |    0           |     5.83        |     42.08        |
| taxa_ocupados_sem_carteira      |    3.03        |    24.75        |     62.23        |
| taxa_agua_encanada              |    0.15        |    90.28        |    100           |
| taxa_banheiro_agua_encanada     |    3.26        |    91.25        |    100           |
| taxa_densidade_2_mais           |    0.65        |    23.07        |     88.64        |
| taxa_coleta_lixo                |    0           |    98.03        |    100           |
| taxa_energia_eletrica           |   27.41        |    99.39        |    100           |
| taxa_agua_esgoto_inadequados    |    0           |     3.26        |     85.36        |
| taxa_paredes_inadequados        |    0           |     1.64        |     82.74        |
| taxa_criancas_dom_sem_fund      |    6.35        |    38.4         |     80.91        |
| taxa_criancas_fora_escola_4_5   |    0           |    17.86        |     86.97        |
| taxa_criancas_fora_escola_6_14  |    0           |     2.38        |     48.23        |
| taxa_dom_sem_fund               |    7.59        |    35.56        |     77.89        |
| taxa_dom_vulner_sem_fund        |    0.21        |    18.75        |     74.45        |
| taxa_sem_fund_informal          |   12.5         |    50.35        |     84.96        |
| taxa_mulheres_com_filho_10_14   |    0           |     0           |      8.38        |
| taxa_mulheres_com_filho_15_17   |    0           |     6.79        |     40.6         |
| taxa_mulheres_chefe_filho_15m   |    0           |    18.09        |     77.59        |
| taxa_nest_ntrab_vulner_15_24    |    0           |    13.67        |     55.25        |
| taxa_vulner_desloc_1_hora       |    0           |     0.9         |     16.4         |
| taxa_dom_vulner_dep_idoso       |    0           |     2.85        |     18.17        |
| taxa_sem_energia_eletrica       |    0           |     0.61        |     72.59        |
| populacao_homens_0_4            |   19           |   425           | 361709           |
| populacao_homens_10_14          |   31           |   553           | 438356           |
| populacao_homens_15_19          |   33           |   537           | 420552           |
| populacao_homens_20_24          |   30           |   491           | 489432           |
| populacao_homens_25_29          |   30           |   455           | 519694           |
| populacao_homens_30_34          |   25           |   415           | 481258           |
| populacao_homens_35_39          |   30           |   372           | 423024           |
| populacao_homens_40_44          |   26           |   356           | 385172           |
| populacao_homens_45_49          |   22           |   324           | 342042           |
| populacao_homens_50_54          |   18           |   270           | 301852           |
| populacao_homens_55_59          |   15           |   229           | 243863           |
| populacao_homens_5_9            |   25           |   473           | 385672           |
| populacao_homens_60_64          |   13           |   192           | 183012           |
| populacao_homens_65_69          |    9           |   150           | 127020           |
| populacao_homens_70_74          |    8           |   115           |  95214           |
| populacao_homens_75_79          |    3           |    76           |  64324           |
| populacao_homens                |  422           |  5548           |      5.32863e+06 |
| populacao_homens_80_mais        |    1           |    83           |  66436           |
| populacao_mulheres_0_4          |   22           |   410           | 349218           |
| populacao_mulheres_10_14        |   33           |   521           | 429074           |
| populacao_mulheres_15_19        |   26           |   513           | 421705           |
| populacao_mulheres_20_24        |   21           |   464           | 502227           |
| populacao_mulheres_25_29        |   30           |   435           | 554888           |
| populacao_mulheres_30_34        |   20           |   401           | 528818           |
| populacao_mulheres_35_39        |   25           |   363           | 465661           |
| populacao_mulheres_40_44        |   23           |   342           | 427807           |
| populacao_mulheres_45_49        |   19           |   308           | 400678           |
| populacao_mulheres_50_54        |   22           |   266           | 365806           |
| populacao_mulheres_55_59        |   15           |   230           | 304250           |
| populacao_mulheres_5_9          |   19           |   456           | 372607           |
| populacao_mulheres_60_64        |   11           |   190           | 240043           |
| populacao_mulheres_65_69        |    6           |   152           | 175318           |
| populacao_mulheres_70_74        |    4           |   119           | 142087           |
| populacao_mulheres_75_79        |    3           |    83           | 106645           |
| populacao_mulheres_80_mais      |    3           |    97           | 138039           |
| populacao_mulheres              |  383           |  5419           |      5.92487e+06 |
| populacao_1_menos               |    7           |   160           | 142819           |
| populacao_11_14                 |   48           |   855           | 688360           |
| populacao_11_13                 |   36           |   635           | 515828           |
| populacao_12_14                 |   30           |   646           | 515281           |
| populacao_1_3                   |   23           |   491           | 421276           |
| populacao_15_mais               |  639           |  8082           |      8.9129e+06  |
| populacao_15_17                 |   39           |   651           | 505693           |
| populacao_15_24                 |  122           |  1994           |      1.8331e+06  |
| populacao_16_18                 |   37           |   627           | 498886           |
| populacao_18_mais               |  597           |  7423           |      8.4072e+06  |
| populacao_18_20                 |   35           |   586           | 523852           |
| populacao_18_24                 |   83           |  1342           |      1.3274e+06  |
| populacao_19_21                 |   32           |   572           | 550248           |
| populacao_25_mais               |  503           |  6072           |      7.0798e+06  |
| populacao_4                     |    6           |   177           | 146688           |
| populacao_5                     |    9           |   180           | 149757           |
| populacao_6                     |    7           |   180           | 146923           |
| populacao_6_10                  |   46           |   964           | 787281           |
| populacao_6_17                  |  128           |  2264           |      1.81517e+06 |
| populacao_65_mais               |   58           |   879           | 914646           |
| populacao                       |  805           | 10934           |      1.12535e+07 |
| populacao_urbana                |  174           |  6263           |      1.11523e+07 |
| populacao_rural                 |    0           |  3233           | 125336           |
| populacao_dom_pp                |  805           | 10871           |      1.11726e+07 |
| populacao_dom_pp_exc_renda_nula |  805           | 10704           |      1.11665e+07 |
| pea                             |  307           |  4933           |      6.02621e+06 |
| pea_10_14                       |    0           |   102           |  45447           |
| pea_15_17                       |    1           |   210           | 144412           |
| pea_18_mais                     |  294           |  4594           |      5.83635e+06 |
| pia                             |  710           |  9185           |      9.78387e+06 |
| pia_10_14                       |   64           |  1072           | 867351           |
| pia_15_17                       |   42           |   649           | 506046           |
| pia_18_mais                     |  597           |  7462           |      8.41047e+06 |
| indice_escolaridade             |    0.12        |     0.384       |      0.8         |
| indice_frequencia_escolar       |    0.268       |     0.67        |      0.962       |
| idhm                            |    0.418       |     0.665       |      0.862       |
| idhm_e                          |    0.207       |     0.56        |      0.825       |
| idhm_l                          |    0.672       |     0.808       |      0.894       |
| idhm_r                          |    0.4         |     0.654       |      0.891       |

### 4. Códigos de ausência mascarados em categóricas

- Nenhum código de ausência mascarado encontrado.

### 5. Outliers implausíveis (critério relacional)

| coluna                          |         mediana |              p99 |              max |   max/p99 |
|:--------------------------------|----------------:|-----------------:|-----------------:|----------:|
| id_municipio                    |     3.14621e+06 |      5.21817e+06 |      5.30011e+06 |    1.0157 |
| expectativa_vida                |    73.47        |     78.06        |     78.64        |    1.0074 |
| fecundidade_total               |     2.13        |      3.79        |      4.89        |    1.2902 |
| mortalidade_1                   |    16.9         |     39.9         |     46.8         |    1.1729 |
| mortalidade_5                   |    19.42        |     43.318       |     50.94        |    1.176  |
| razao_dependencia               |    49.59        |     80.3296      |    118.04        |    1.4694 |
| prob_sobrevivencia_40           |    93.89        |     96.3236      |     97.09        |    1.008  |
| prob_sobrevivencia_60           |    82.92        |     88.5436      |     90.81        |    1.0256 |
| taxa_envelhecimento             |     8.38        |     14.51        |     20.42        |    1.4073 |
| expectativa_anos_estudo         |     9.47        |     11.91        |     12.83        |    1.0772 |
| taxa_analfabetismo_11_a_14      |     2.02        |     16.2944      |     38.98        |    2.3922 |
| taxa_analfabetismo_15_a_17      |     1.71        |     11.0804      |     33.53        |    3.0261 |
| taxa_analfabetismo_15_mais      |    13.12        |     38.84        |     44.4         |    1.1432 |
| taxa_analfabetismo_18_a_24      |     2.26        |     15.288       |     36.37        |    2.379  |
| taxa_analfabetismo_18_mais      |    14.11        |     42.12        |     47.64        |    1.1311 |
| taxa_analfabetismo_25_a_29      |     3.87        |     26.5676      |     36.13        |    1.3599 |
| taxa_analfabetismo_25_mais      |    16.46        |     49.6552      |     57.18        |    1.1515 |
| taxa_atraso_0_basico            |    60.98        |     85.5624      |     92.48        |    1.0808 |
| taxa_atraso_0_fundamental       |    64.82        |     87.9172      |     95.41        |    1.0852 |
| taxa_atraso_0_medio             |    72.27        |     94.808       |    100           |    1.0548 |
| taxa_atraso_1_basico            |    18.8         |     26.7836      |     32.31        |    1.2063 |
| taxa_atraso_1_fundamental       |    18.88        |     27.9944      |     35.58        |    1.271  |
| taxa_atraso_1_medio             |    20.32        |     44.0308      |     63.08        |    1.4326 |
| taxa_atraso_2_basico            |    19.64        |     44.5144      |     58.62        |    1.3169 |
| taxa_atraso_2_fundamental       |    16.07        |     38.4468      |     51.74        |    1.3458 |
| taxa_atraso_2_medio             |     6.56        |     24.9408      |     55.31        |    2.2177 |
| taxa_freq_bruta_basico          |    99.03        |    121.413       |    168.88        |    1.391  |
| taxa_freq_bruta_fundamental     |   110.42        |    138.171       |    195.59        |    1.4156 |
| taxa_freq_bruta_medio           |    66.06        |    102.265       |    168.64        |    1.649  |
| taxa_freq_bruta_pre             |    64.62        |    118.439       |    165.74        |    1.3994 |
| taxa_freq_bruta_superior        |    17.18        |     49.9496      |     76.78        |    1.5371 |
| taxa_freq_liquida_basico        |    88.94        |     95.82        |     98.75        |    1.0306 |
| taxa_freq_liquida_fundamental   |    93.37        |     98.12        |    100           |    1.0192 |
| taxa_freq_liquida_medio         |    41.04        |     73.67        |     91.3         |    1.2393 |
| taxa_freq_liquida_pre           |    55.56        |     87.5352      |    100           |    1.1424 |
| taxa_freq_liquida_superior      |     8.43        |     28.568       |     43.89        |    1.5363 |
| taxa_freq_0_3                   |    17.52        |     52.0664      |     70.22        |    1.3487 |
| taxa_freq_11_14                 |    96.98        |    100           |    100           |    1      |
| taxa_freq_15_17                 |    82.33        |     94.636       |    100           |    1.0567 |
| taxa_freq_18_24                 |    25.78        |     42.9116      |     58.77        |    1.3696 |
| taxa_freq_25_29                 |    10.05        |     23.5936      |     46.29        |    1.962  |
| taxa_freq_4_5                   |    82.14        |    100           |    100           |    1      |
| taxa_freq_4_6                   |    87.05        |    100           |    100           |    1      |
| taxa_freq_5_6                   |    94.13        |    100           |    100           |    1      |
| taxa_freq_6                     |    97.38        |    100           |    100           |    1      |
| taxa_freq_6_14                  |    97.62        |    100           |    100           |    1      |
| taxa_freq_6_17                  |    93.47        |     97.8736      |    100           |    1.0217 |
| taxa_freq_fundamental_15_17     |    27.32        |     58.4388      |     68.95        |    1.1799 |
| taxa_freq_fundamental_18_24     |     2.72        |     14.7996      |     35.31        |    2.3859 |
| taxa_freq_fundamental_4_5       |    14.85        |     43.736       |     70.13        |    1.6035 |
| taxa_freq_medio_18_24           |     6.48        |     17.9344      |     25.51        |    1.4224 |
| taxa_freq_medio_6_14            |     1.83        |      6.5636      |      9.66        |    1.4718 |
| taxa_freq_superior_15_17        |     0.72        |      6.14        |     12.17        |    1.9821 |
| taxa_fundamental_11_13          |    86.58        |     98.968       |    100           |    1.0104 |
| taxa_fundamental_12_14          |    87.6         |    100           |    100           |    1      |
| taxa_fundamental_15_17          |    55.42        |     86.3032      |     96.81        |    1.1217 |
| taxa_fundamental_16_18          |    64.6         |     90.8296      |     98.4         |    1.0833 |
| taxa_fundamental_18_24          |    68.78        |     92.0544      |     97.85        |    1.063  |
| taxa_fundamental_18_mais        |    38.44        |     67.1908      |     80.03        |    1.1911 |
| taxa_fundamental_25_mais        |    32.33        |     63.7088      |     78.04        |    1.2249 |
| taxa_medio_18_20                |    35.14        |     72.2656      |     88.03        |    1.2181 |
| taxa_medio_18_24                |    39.45        |     71.5696      |     90.62        |    1.2662 |
| taxa_medio_18_mais              |    23.48        |     49.7136      |     66.23        |    1.3322 |
| taxa_medio_19_21                |    40.31        |     75.3016      |     94.67        |    1.2572 |
| taxa_medio_25_mais              |    20.13        |     47.7844      |     65.86        |    1.3783 |
| taxa_superior_25_mais           |     4.81        |     16.5896      |     33.68        |    2.0302 |
| renda_pc_max_quintil_1          |   150           |    442.059       |    585           |    1.3234 |
| renda_pc_max_quintil_2          |   253.67        |    628.045       |    945           |    1.5047 |
| renda_pc_max_quintil_3          |   382           |    874.75        |   1496.67        |    1.711  |
| renda_pc_max_quintil_4          |   575           |   1379.87        |   2900           |    2.1016 |
| renda_pc_max_decil_9            |   866.67        |   2176.8         |   5000           |    2.2969 |
| indice_gini                     |     0.49        |      0.67        |      0.8         |    1.194  |
| prop_pobreza_extrema            |     6.24        |     45.1952      |     69.67        |    1.5415 |
| prop_pobreza_extrema_criancas   |     9.95        |     55.9812      |     72.43        |    1.2938 |
| prop_pobreza                    |    18.14        |     63.878       |     78.59        |    1.2303 |
| prop_pobreza_criancas           |    30.03        |     76.4936      |     84.66        |    1.1068 |
| prop_vulner_pobreza             |    42.23        |     83.1716      |     91.57        |    1.101  |
| prop_vulner_pobreza_criancas    |    61.04        |     91.8644      |     95.44        |    1.0389 |
| prop_renda_10_ricos             |    37.62        |     55.9736      |     75.34        |    1.346  |
| prop_renda_20_pobres            |     3.72        |      7.19        |      9.26        |    1.2879 |
| prop_renda_20_ricos             |    53.56        |     69.0556      |     81.54        |    1.1808 |
| prop_renda_40_pobres            |    12.17        |     19.2372      |     22.5         |    1.1696 |
| prop_renda_60_pobres            |    25.53        |     35.6572      |     40.12        |    1.1252 |
| prop_renda_80_pobres            |    46.43        |     57.7536      |     63.11        |    1.0927 |
| prop_renda_trabalho             |    70.58        |     87.3408      |     95.24        |    1.0904 |
| razao_10_ricos_40_pobres        |    12.55        |     43.4124      |    221.1         |    5.093  |
| razao_20_ricos_40_pobres        |     8.85        |     28.3624      |    146.11        |    5.1515 |
| renda_pc                        |   467.65        |   1158.64        |   2043.74        |    1.7639 |
| renda_pc_quintil_1              |    89.67        |    304.174       |    437.76        |    1.4392 |
| renda_pc_decil_10               |  1698.26        |   5255.42        |  10610.9         |    2.019  |
| renda_pc_quintil_2              |   199.8         |    530.677       |    731.02        |    1.3775 |
| renda_pc_quintil_3              |   311.85        |    745.28        |   1175.12        |    1.5767 |
| renda_pc_quintil_4              |   479.33        |   1084.25        |   2057.78        |    1.8979 |
| renda_pc_quintil_5              |  1208.88        |   3401.05        |   6735.07        |    1.9803 |
| renda_pc_exc_renda_nula         |   473.72        |   1158.64        |   2043.74        |    1.7639 |
| renda_pc_pobreza_extrema        |    32.51        |     59.9936      |     70           |    1.1668 |
| renda_pc_pobreza                |    80.62        |    114.648       |    132.25        |    1.1535 |
| renda_pc_vulner_pobreza         |   149.78        |    198.108       |    217.08        |    1.0958 |
| indice_theil                    |     0.44        |      0.83        |      1.36        |    1.6386 |
| prop_trabalhadores_conta_proria |    22.66        |     57.8848      |     76.68        |    1.3247 |
| prop_empregadores               |     1.06        |      4.73        |      8.92        |    1.8858 |
| prop_ocupados_agropecuaria      |    36.45        |     73.6136      |     85.12        |    1.1563 |
| prop_ocupados_comercio          |    10.05        |     21.8988      |     36.57        |    1.67   |
| prop_ocupados_construcao        |     6.06        |     16.16        |     26.3         |    1.6275 |
| prop_ocupados_extracao          |     0.12        |      7.8972      |     28.19        |    3.5696 |
| prop_ocupados_formalizacao      |    42.85        |     79.5336      |     89.11        |    1.1204 |
| prop_ocupados_fundamental       |    45.18        |     74.7524      |     86.47        |    1.1568 |
| prop_ocupados_medio             |    29.12        |     57.6836      |     73.65        |    1.2768 |
| prop_ocupados_servicos          |    31.89        |     55.3608      |     78.23        |    1.4131 |
| prop_ocupados_siup              |     0.65        |      2.8208      |     12.95        |    4.5909 |
| prop_ocupados_superior          |     6.4         |     19.0824      |     37.53        |    1.9667 |
| prop_ocupados_transformacao     |     6.53        |     40.6508      |     65.11        |    1.6017 |
| prop_ocupados_renda_0           |     9.41        |     48.7944      |     73.93        |    1.5151 |
| prop_ocupados_renda_1_sm        |    35.81        |     80.748       |     89.33        |    1.1063 |
| prop_ocupados_renda_2_sm        |    83.86        |     96.9372      |     99.14        |    1.0227 |
| prop_ocupados_renda_3_sm        |    91.94        |     98.8936      |    100           |    1.0112 |
| prop_ocupados_renda_5_sm        |    96.82        |     99.77        |    100           |    1.0023 |
| renda_media_ocupados            |   761.72        |   1670.13        |   3177.26        |    1.9024 |
| taxa_atividade                  |    55.64        |     78.2516      |     91.27        |    1.1664 |
| taxa_atividade_10_14            |     8.71        |     40.036       |     72.55        |    1.8121 |
| taxa_atividade_15_17            |    32.51        |     72.1836      |     87.59        |    1.2134 |
| taxa_atividade_18_24            |    66.94        |     92.7972      |     99.09        |    1.0678 |
| taxa_atividade_18_mais          |    64.01        |     83.9172      |     95.6         |    1.1392 |
| taxa_atividade_25_29            |    75.64        |     95.696       |    100           |    1.045  |
| taxa_desocupacao                |     6.26        |     18.7276      |     41.93        |    2.2389 |
| taxa_desocupacao_10_14          |    10.17        |     65.3568      |    100           |    1.5301 |
| taxa_desocupacao_15_17          |    16.11        |     50.6412      |    100           |    1.9747 |
| taxa_desocupacao_18_24          |    12.01        |     33.82        |     56.85        |    1.681  |
| taxa_desocupacao_18_mais        |     5.66        |     17.6716      |     38.45        |    2.1758 |
| taxa_desocupacao_25_29          |     7           |     23.6932      |     44.35        |    1.8718 |
| indice_treil_trabalho           |     0.38        |      0.76        |      1.4         |    1.8421 |
| taxa_ocupados_carteira          |    26.76        |     69.2008      |     83.21        |    1.2024 |
| taxa_ocupados_setor_publico     |     5.83        |     20.5252      |     42.08        |    2.0502 |
| taxa_ocupados_sem_carteira      |    24.75        |     49.4972      |     62.23        |    1.2572 |
| taxa_agua_encanada              |    90.28        |     99.72        |    100           |    1.0028 |
| taxa_banheiro_agua_encanada     |    91.25        |    100           |    100           |    1      |
| taxa_densidade_2_mais           |    23.07        |     68.0908      |     88.64        |    1.3018 |
| taxa_coleta_lixo                |    98.03        |    100           |    100           |    1      |
| taxa_energia_eletrica           |    99.39        |    100           |    100           |    1      |
| taxa_agua_esgoto_inadequados    |     3.26        |     55.7424      |     85.36        |    1.5313 |
| taxa_paredes_inadequados        |     1.64        |     47.3916      |     82.74        |    1.7459 |
| taxa_criancas_dom_sem_fund      |    38.4         |     68.0936      |     80.91        |    1.1882 |
| taxa_criancas_fora_escola_4_5   |    17.86        |     68.272       |     86.97        |    1.2739 |
| taxa_criancas_fora_escola_6_14  |     2.38        |     13.278       |     48.23        |    3.6323 |
| taxa_dom_sem_fund               |    35.56        |     60.8676      |     77.89        |    1.2797 |
| taxa_dom_vulner_sem_fund        |    18.75        |     51.7456      |     74.45        |    1.4388 |
| taxa_sem_fund_informal          |    50.35        |     75.898       |     84.96        |    1.1194 |
| taxa_mulheres_com_filho_10_14   |     0           |      3.0672      |      8.38        |    2.7321 |
| taxa_mulheres_com_filho_15_17   |     6.79        |     21.6972      |     40.6         |    1.8712 |
| taxa_mulheres_chefe_filho_15m   |    18.09        |     51.1816      |     77.59        |    1.516  |
| taxa_nest_ntrab_vulner_15_24    |    13.67        |     35.2836      |     55.25        |    1.5659 |
| taxa_vulner_desloc_1_hora       |     0.9         |      7.3544      |     16.4         |    2.23   |
| taxa_dom_vulner_dep_idoso       |     2.85        |      9.96        |     18.17        |    1.8243 |
| taxa_sem_energia_eletrica       |     0.61        |     30.6532      |     72.59        |    2.3681 |
| populacao_homens_0_4            |   425           |  13624           | 361709           |   26.5494 |
| populacao_homens_10_14          |   553           |  16413           | 438356           |   26.7079 |
| populacao_homens_15_19          |   537           |  16269           | 420552           |   25.85   |
| populacao_homens_20_24          |   491           |  17571.8         | 489432           |   27.8532 |
| populacao_homens_25_29          |   455           |  17243.9         | 519694           |   30.1379 |
| populacao_homens_30_34          |   415           |  15911.8         | 481258           |   30.2454 |
| populacao_homens_35_39          |   372           |  14173           | 423024           |   29.8473 |
| populacao_homens_40_44          |   356           |  13029.5         | 385172           |   29.5616 |
| populacao_homens_45_49          |   324           |  11638           | 342042           |   29.39   |
| populacao_homens_50_54          |   270           |   9820.48        | 301852           |   30.737  |
| populacao_homens_55_59          |   229           |   7767.44        | 243863           |   31.3955 |
| populacao_homens_5_9            |   473           |  14350           | 385672           |   26.876  |
| populacao_homens_60_64          |   192           |   5809.84        | 183012           |   31.5004 |
| populacao_homens_65_69          |   150           |   3845.04        | 127020           |   33.0348 |
| populacao_homens_70_74          |   115           |   2990.92        |  95214           |   31.8344 |
| populacao_homens_75_79          |    76           |   1921.24        |  64324           |   33.4805 |
| populacao_homens                |  5548           | 183698           |      5.32863e+06 |   29.0076 |
| populacao_homens_80_mais        |    83           |   1885.4         |  66436           |   35.2371 |
| populacao_mulheres_0_4          |   410           |  13083.6         | 349218           |   26.6913 |
| populacao_mulheres_10_14        |   521           |  16202.6         | 429074           |   26.4818 |
| populacao_mulheres_15_19        |   513           |  16352.2         | 421705           |   25.7889 |
| populacao_mulheres_20_24        |   464           |  17770           | 502227           |   28.2627 |
| populacao_mulheres_25_29        |   435           |  18397.2         | 554888           |   30.1615 |
| populacao_mulheres_30_34        |   401           |  17152.5         | 528818           |   30.8303 |
| populacao_mulheres_35_39        |   363           |  15146.9         | 465661           |   30.7429 |
| populacao_mulheres_40_44        |   342           |  14252.4         | 427807           |   30.0166 |
| populacao_mulheres_45_49        |   308           |  13017.1         | 400678           |   30.7809 |
| populacao_mulheres_50_54        |   266           |  11436.8         | 365806           |   31.985  |
| populacao_mulheres_55_59        |   230           |   9204.08        | 304250           |   33.056  |
| populacao_mulheres_5_9          |   456           |  13886           | 372607           |   26.8332 |
| populacao_mulheres_60_64        |   190           |   7125.72        | 240043           |   33.6868 |
| populacao_mulheres_65_69        |   152           |   5118.08        | 175318           |   34.2546 |
| populacao_mulheres_70_74        |   119           |   4025.88        | 142087           |   35.2934 |
| populacao_mulheres_75_79        |    83           |   2891.56        | 106645           |   36.8815 |
| populacao_mulheres_80_mais      |    97           |   3347.48        | 138039           |   41.2367 |
| populacao_mulheres              |  5419           | 199053           |      5.92487e+06 |   29.7653 |
| populacao_1_menos               |   160           |   5390.52        | 142819           |   26.4945 |
| populacao_11_14                 |   855           |  25985.8         | 688360           |   26.4899 |
| populacao_11_13                 |   635           |  19400.3         | 515828           |   26.5887 |
| populacao_12_14                 |   646           |  19449.9         | 515281           |   26.4928 |
| populacao_1_3                   |   491           |  15941.4         | 421276           |   26.4265 |
| populacao_15_mais               |  8082           | 293865           |      8.9129e+06  |   30.3299 |
| populacao_15_17                 |   651           |  19633           | 505693           |   25.7572 |
| populacao_15_24                 |  1994           |  67320.4         |      1.8331e+06  |   27.2294 |
| populacao_16_18                 |   627           |  19414           | 498886           |   25.6972 |
| populacao_18_mais               |  7423           | 273744           |      8.4072e+06  |   30.7119 |
| populacao_18_20                 |   586           |  19751.4         | 523852           |   26.5223 |
| populacao_18_24                 |  1342           |  47627.1         |      1.3274e+06  |   27.8708 |
| populacao_19_21                 |   572           |  20319.9         | 550248           |   27.0792 |
| populacao_25_mais               |  6072           | 225558           |      7.0798e+06  |   31.388  |
| populacao_4                     |   177           |   5311.12        | 146688           |   27.619  |
| populacao_5                     |   180           |   5555.72        | 149757           |   26.9555 |
| populacao_6                     |   180           |   5555.68        | 146923           |   26.4455 |
| populacao_6_10                  |   964           |  29311           | 787281           |   26.8596 |
| populacao_6_17                  |  2264           |  68430.1         |      1.81517e+06 |   26.5259 |
| populacao_65_mais               |   879           |  26570.4         | 914646           |   34.4235 |
| populacao                       | 10934           | 380654           |      1.12535e+07 |   29.5636 |
| populacao_urbana                |  6263           | 369853           |      1.11523e+07 |   30.1534 |
| populacao_rural                 |  3233           |  30462.2         | 125336           |    4.1145 |
| populacao_dom_pp                | 10871           | 378802           |      1.11726e+07 |   29.4946 |
| populacao_dom_pp_exc_renda_nula | 10704           | 378568           |      1.11665e+07 |   29.4968 |
| pea                             |  4933           | 196942           |      6.02621e+06 |   30.5989 |
| pea_10_14                       |   102           |   1762           |  45447           |   25.7928 |
| pea_15_17                       |   210           |   5609.92        | 144412           |   25.7423 |
| pea_18_mais                     |  4594           | 189226           |      5.83635e+06 |   30.8433 |
| pia                             |  9185           | 325261           |      9.78387e+06 |   30.08   |
| pia_10_14                       |  1072           |  32615.6         | 867351           |   26.5932 |
| pia_15_17                       |   649           |  19550.7         | 506046           |   25.8838 |
| pia_18_mais                     |  7462           | 274376           |      8.41047e+06 |   30.6531 |
| indice_escolaridade             |     0.384       |      0.672       |      0.8         |    1.1905 |
| indice_frequencia_escolar       |     0.67        |      0.8694      |      0.962       |    1.1066 |
| idhm                            |     0.665       |      0.795       |      0.862       |    1.0843 |
| idhm_e                          |     0.56        |      0.749       |      0.825       |    1.1015 |
| idhm_l                          |     0.808       |      0.884       |      0.894       |    1.0113 |
| idhm_r                          |     0.654       |      0.7994      |      0.891       |    1.1146 |

Razão `max/p99` alta indica cauda desproporcional — não é prova de erro, é candidato a checar contra a metodologia da fonte antes de usar sem tratamento.

### 6. Perfil de nulos por coluna

- Nenhuma coluna com nulos.

### 7. Redundância entre colunas

- `expectativa_vida` ↔ `mortalidade_1`: correlação 0.967
- `expectativa_vida` ↔ `mortalidade_5`: correlação 0.964
- `expectativa_vida` ↔ `idhm_l`: correlação 1.000
- `mortalidade_1` ↔ `mortalidade_5`: correlação 0.996
- `mortalidade_1` ↔ `idhm_l`: correlação 0.967
- `mortalidade_5` ↔ `idhm_l`: correlação 0.964
- `prob_sobrevivencia_40` ↔ `prob_sobrevivencia_60`: correlação 0.956
- `taxa_analfabetismo_11_a_14` ↔ `taxa_analfabetismo_15_a_17`: correlação 0.919
- `taxa_analfabetismo_11_a_14` ↔ `taxa_analfabetismo_18_a_24`: correlação 0.908
- `taxa_analfabetismo_15_a_17` ↔ `taxa_analfabetismo_18_a_24`: correlação 0.921
- `taxa_analfabetismo_15_mais` ↔ `taxa_analfabetismo_18_mais`: correlação 1.000
- `taxa_analfabetismo_15_mais` ↔ `taxa_analfabetismo_25_a_29`: correlação 0.922
- `taxa_analfabetismo_15_mais` ↔ `taxa_analfabetismo_25_mais`: correlação 0.998
- `taxa_analfabetismo_18_a_24` ↔ `taxa_analfabetismo_25_a_29`: correlação 0.942
- `taxa_analfabetismo_18_mais` ↔ `taxa_analfabetismo_25_a_29`: correlação 0.922
- `taxa_analfabetismo_18_mais` ↔ `taxa_analfabetismo_25_mais`: correlação 0.999
- `taxa_analfabetismo_25_a_29` ↔ `taxa_analfabetismo_25_mais`: correlação 0.920
- `taxa_atraso_0_basico` ↔ `taxa_atraso_0_fundamental`: correlação 0.982
- `taxa_atraso_0_basico` ↔ `taxa_atraso_2_basico`: correlação 0.961
- `taxa_atraso_0_basico` ↔ `taxa_atraso_2_fundamental`: correlação 0.926
- `taxa_atraso_0_fundamental` ↔ `taxa_atraso_2_basico`: correlação 0.940
- `taxa_atraso_0_fundamental` ↔ `taxa_atraso_2_fundamental`: correlação 0.944
- `taxa_atraso_1_basico` ↔ `taxa_atraso_1_fundamental`: correlação 0.955
- `taxa_atraso_2_basico` ↔ `taxa_atraso_2_fundamental`: correlação 0.969
- `taxa_freq_bruta_pre` ↔ `taxa_freq_liquida_pre`: correlação 0.923
- `taxa_freq_bruta_superior` ↔ `taxa_freq_liquida_superior`: correlação 0.923
- `taxa_freq_liquida_medio` ↔ `taxa_fundamental_15_17`: correlação 0.905
- `taxa_freq_11_14` ↔ `taxa_freq_6_14`: correlação 0.916
- `taxa_freq_11_14` ↔ `taxa_criancas_fora_escola_6_14`: correlação 0.916
- `taxa_freq_4_5` ↔ `taxa_freq_4_6`: correlação 0.984
- `taxa_freq_4_5` ↔ `taxa_criancas_fora_escola_4_5`: correlação 1.000
- `taxa_freq_4_6` ↔ `taxa_criancas_fora_escola_4_5`: correlação 0.984
- `taxa_freq_6_14` ↔ `taxa_criancas_fora_escola_6_14`: correlação 1.000
- `taxa_freq_fundamental_15_17` ↔ `taxa_fundamental_15_17`: correlação 0.906
- `taxa_fundamental_11_13` ↔ `taxa_fundamental_12_14`: correlação 0.904
- `taxa_fundamental_15_17` ↔ `taxa_fundamental_16_18`: correlação 0.959
- `taxa_fundamental_15_17` ↔ `indice_frequencia_escolar`: correlação 0.927
- `taxa_fundamental_16_18` ↔ `indice_frequencia_escolar`: correlação 0.920
- `taxa_fundamental_18_24` ↔ `taxa_medio_18_24`: correlação 0.930
- `taxa_fundamental_18_24` ↔ `idhm_e`: correlação 0.920
- `taxa_fundamental_18_mais` ↔ `taxa_fundamental_25_mais`: correlação 0.993
- `taxa_fundamental_18_mais` ↔ `taxa_medio_18_mais`: correlação 0.964
- `taxa_fundamental_18_mais` ↔ `taxa_medio_25_mais`: correlação 0.958
- `taxa_fundamental_18_mais` ↔ `prop_ocupados_fundamental`: correlação 0.973
- `taxa_fundamental_18_mais` ↔ `prop_ocupados_medio`: correlação 0.929
- `taxa_fundamental_18_mais` ↔ `taxa_dom_sem_fund`: correlação 0.947
- `taxa_fundamental_18_mais` ↔ `taxa_sem_fund_informal`: correlação 0.918
- `taxa_fundamental_18_mais` ↔ `indice_escolaridade`: correlação 1.000
- `taxa_fundamental_25_mais` ↔ `taxa_medio_18_mais`: correlação 0.959
- `taxa_fundamental_25_mais` ↔ `taxa_medio_25_mais`: correlação 0.967
- `taxa_fundamental_25_mais` ↔ `prop_ocupados_fundamental`: correlação 0.967
- `taxa_fundamental_25_mais` ↔ `prop_ocupados_medio`: correlação 0.926
- `taxa_fundamental_25_mais` ↔ `taxa_dom_sem_fund`: correlação 0.918
- `taxa_fundamental_25_mais` ↔ `taxa_sem_fund_informal`: correlação 0.907
- `taxa_fundamental_25_mais` ↔ `indice_escolaridade`: correlação 0.993
- `taxa_medio_18_20` ↔ `taxa_medio_18_24`: correlação 0.956
- `taxa_medio_18_20` ↔ `taxa_medio_19_21`: correlação 0.957
- `taxa_medio_18_20` ↔ `indice_frequencia_escolar`: correlação 0.917
- `taxa_medio_18_24` ↔ `taxa_medio_19_21`: correlação 0.964
- `taxa_medio_18_24` ↔ `indice_frequencia_escolar`: correlação 0.901
- `taxa_medio_18_24` ↔ `idhm_e`: correlação 0.907
- `taxa_medio_18_mais` ↔ `taxa_medio_25_mais`: correlação 0.987
- `taxa_medio_18_mais` ↔ `prop_ocupados_fundamental`: correlação 0.948
- `taxa_medio_18_mais` ↔ `prop_ocupados_medio`: correlação 0.972
- `taxa_medio_18_mais` ↔ `taxa_dom_sem_fund`: correlação 0.907
- `taxa_medio_18_mais` ↔ `indice_escolaridade`: correlação 0.964
- `taxa_medio_25_mais` ↔ `prop_ocupados_fundamental`: correlação 0.938
- `taxa_medio_25_mais` ↔ `prop_ocupados_medio`: correlação 0.963
- `taxa_medio_25_mais` ↔ `indice_escolaridade`: correlação 0.958
- `taxa_superior_25_mais` ↔ `prop_ocupados_superior`: correlação 0.967
- `renda_pc_max_quintil_1` ↔ `renda_pc_max_quintil_2`: correlação 0.988
- `renda_pc_max_quintil_1` ↔ `renda_pc_max_quintil_3`: correlação 0.969
- `renda_pc_max_quintil_1` ↔ `renda_pc_max_quintil_4`: correlação 0.918
- `renda_pc_max_quintil_1` ↔ `prop_pobreza`: correlação 0.909
- `renda_pc_max_quintil_1` ↔ `prop_pobreza_criancas`: correlação 0.932
- `renda_pc_max_quintil_1` ↔ `prop_vulner_pobreza`: correlação 0.960
- `renda_pc_max_quintil_1` ↔ `prop_vulner_pobreza_criancas`: correlação 0.972
- `renda_pc_max_quintil_1` ↔ `renda_pc`: correlação 0.915
- `renda_pc_max_quintil_1` ↔ `renda_pc_quintil_1`: correlação 0.991
- `renda_pc_max_quintil_1` ↔ `renda_pc_quintil_2`: correlação 0.995
- `renda_pc_max_quintil_1` ↔ `renda_pc_quintil_3`: correlação 0.981
- `renda_pc_max_quintil_1` ↔ `renda_pc_quintil_4`: correlação 0.950
- `renda_pc_max_quintil_1` ↔ `renda_pc_exc_renda_nula`: correlação 0.910
- `renda_pc_max_quintil_1` ↔ `renda_pc_vulner_pobreza`: correlação 0.901
- `renda_pc_max_quintil_1` ↔ `idhm_r`: correlação 0.917
- `renda_pc_max_quintil_2` ↔ `renda_pc_max_quintil_3`: correlação 0.988
- `renda_pc_max_quintil_2` ↔ `renda_pc_max_quintil_4`: correlação 0.949
- `renda_pc_max_quintil_2` ↔ `prop_pobreza`: correlação 0.911
- `renda_pc_max_quintil_2` ↔ `prop_pobreza_criancas`: correlação 0.931
- `renda_pc_max_quintil_2` ↔ `prop_vulner_pobreza`: correlação 0.968
- `renda_pc_max_quintil_2` ↔ `prop_vulner_pobreza_criancas`: correlação 0.976
- `renda_pc_max_quintil_2` ↔ `renda_pc`: correlação 0.940
- `renda_pc_max_quintil_2` ↔ `renda_pc_quintil_1`: correlação 0.974
- `renda_pc_max_quintil_2` ↔ `renda_pc_quintil_2`: correlação 0.997
- `renda_pc_max_quintil_2` ↔ `renda_pc_quintil_3`: correlação 0.996
- `renda_pc_max_quintil_2` ↔ `renda_pc_quintil_4`: correlação 0.975
- `renda_pc_max_quintil_2` ↔ `renda_pc_exc_renda_nula`: correlação 0.936
- `renda_pc_max_quintil_2` ↔ `idhm`: correlação 0.912
- `renda_pc_max_quintil_2` ↔ `idhm_r`: correlação 0.938
- `renda_pc_max_quintil_3` ↔ `renda_pc_max_quintil_4`: correlação 0.974
- `renda_pc_max_quintil_3` ↔ `renda_pc_max_decil_9`: correlação 0.932
- `renda_pc_max_quintil_3` ↔ `prop_pobreza`: correlação 0.902
- `renda_pc_max_quintil_3` ↔ `prop_pobreza_criancas`: correlação 0.919
- `renda_pc_max_quintil_3` ↔ `prop_vulner_pobreza`: correlação 0.960
- `renda_pc_max_quintil_3` ↔ `prop_vulner_pobreza_criancas`: correlação 0.963
- `renda_pc_max_quintil_3` ↔ `renda_pc`: correlação 0.960
- `renda_pc_max_quintil_3` ↔ `renda_pc_quintil_1`: correlação 0.951
- `renda_pc_max_quintil_3` ↔ `renda_pc_quintil_2`: correlação 0.982
- `renda_pc_max_quintil_3` ↔ `renda_pc_quintil_3`: correlação 0.996
- `renda_pc_max_quintil_3` ↔ `renda_pc_quintil_4`: correlação 0.992
- `renda_pc_max_quintil_3` ↔ `renda_pc_exc_renda_nula`: correlação 0.958
- `renda_pc_max_quintil_3` ↔ `idhm`: correlação 0.917
- `renda_pc_max_quintil_3` ↔ `idhm_r`: correlação 0.950
- `renda_pc_max_quintil_4` ↔ `renda_pc_max_decil_9`: correlação 0.979
- `renda_pc_max_quintil_4` ↔ `prop_vulner_pobreza`: correlação 0.910
- `renda_pc_max_quintil_4` ↔ `prop_vulner_pobreza_criancas`: correlação 0.918
- `renda_pc_max_quintil_4` ↔ `renda_pc`: correlação 0.976
- `renda_pc_max_quintil_4` ↔ `renda_pc_quintil_2`: correlação 0.937
- `renda_pc_max_quintil_4` ↔ `renda_pc_quintil_3`: correlação 0.964
- `renda_pc_max_quintil_4` ↔ `renda_pc_quintil_4`: correlação 0.992
- `renda_pc_max_quintil_4` ↔ `renda_pc_quintil_5`: correlação 0.917
- `renda_pc_max_quintil_4` ↔ `renda_pc_exc_renda_nula`: correlação 0.975
- `renda_pc_max_quintil_4` ↔ `prop_ocupados_renda_2_sm`: correlação 0.907
- `renda_pc_max_quintil_4` ↔ `prop_ocupados_renda_3_sm`: correlação 0.910
- `renda_pc_max_quintil_4` ↔ `idhm_r`: correlação 0.938
- `renda_pc_max_decil_9` ↔ `renda_pc`: correlação 0.970
- `renda_pc_max_decil_9` ↔ `renda_pc_decil_10`: correlação 0.901
- `renda_pc_max_decil_9` ↔ `renda_pc_quintil_3`: correlação 0.916
- `renda_pc_max_decil_9` ↔ `renda_pc_quintil_4`: correlação 0.960
- `renda_pc_max_decil_9` ↔ `renda_pc_quintil_5`: correlação 0.944
- `renda_pc_max_decil_9` ↔ `renda_pc_exc_renda_nula`: correlação 0.970
- `renda_pc_max_decil_9` ↔ `prop_ocupados_renda_3_sm`: correlação 0.924
- `renda_pc_max_decil_9` ↔ `prop_ocupados_renda_5_sm`: correlação 0.907
- `renda_pc_max_decil_9` ↔ `renda_media_ocupados`: correlação 0.906
- `renda_pc_max_decil_9` ↔ `idhm_r`: correlação 0.916
- `indice_gini` ↔ `prop_renda_20_ricos`: correlação 0.959
- `indice_gini` ↔ `prop_renda_40_pobres`: correlação 0.925
- `indice_gini` ↔ `prop_renda_60_pobres`: correlação 0.983
- `indice_gini` ↔ `prop_renda_80_pobres`: correlação 0.974
- `indice_gini` ↔ `indice_theil`: correlação 0.974
- `prop_pobreza_extrema` ↔ `prop_pobreza_extrema_criancas`: correlação 0.991
- `prop_pobreza_extrema` ↔ `prop_pobreza`: correlação 0.964
- `prop_pobreza_extrema` ↔ `prop_pobreza_criancas`: correlação 0.931
- `prop_pobreza_extrema` ↔ `renda_pc_vulner_pobreza`: correlação 0.945
- `prop_pobreza_extrema_criancas` ↔ `prop_pobreza`: correlação 0.966
- `prop_pobreza_extrema_criancas` ↔ `prop_pobreza_criancas`: correlação 0.949
- `prop_pobreza_extrema_criancas` ↔ `prop_vulner_pobreza`: correlação 0.904
- `prop_pobreza_extrema_criancas` ↔ `renda_pc_vulner_pobreza`: correlação 0.951
- `prop_pobreza` ↔ `prop_pobreza_criancas`: correlação 0.987
- `prop_pobreza` ↔ `prop_vulner_pobreza`: correlação 0.970
- `prop_pobreza` ↔ `prop_vulner_pobreza_criancas`: correlação 0.927
- `prop_pobreza` ↔ `renda_pc_quintil_2`: correlação 0.912
- `prop_pobreza` ↔ `renda_pc_quintil_3`: correlação 0.910
- `prop_pobreza` ↔ `renda_pc_vulner_pobreza`: correlação 0.962
- `prop_pobreza` ↔ `taxa_dom_vulner_sem_fund`: correlação 0.929
- `prop_pobreza` ↔ `idhm`: correlação 0.922
- `prop_pobreza` ↔ `idhm_r`: correlação 0.942
- `prop_pobreza_criancas` ↔ `prop_vulner_pobreza`: correlação 0.977
- `prop_pobreza_criancas` ↔ `prop_vulner_pobreza_criancas`: correlação 0.957
- `prop_pobreza_criancas` ↔ `renda_pc_quintil_1`: correlação 0.917
- `prop_pobreza_criancas` ↔ `renda_pc_quintil_2`: correlação 0.934
- `prop_pobreza_criancas` ↔ `renda_pc_quintil_3`: correlação 0.929
- `prop_pobreza_criancas` ↔ `renda_pc_vulner_pobreza`: correlação 0.956
- `prop_pobreza_criancas` ↔ `prop_ocupados_renda_1_sm`: correlação 0.901
- `prop_pobreza_criancas` ↔ `taxa_dom_vulner_sem_fund`: correlação 0.930
- `prop_pobreza_criancas` ↔ `idhm`: correlação 0.925
- `prop_pobreza_criancas` ↔ `idhm_r`: correlação 0.943
- `prop_vulner_pobreza` ↔ `prop_vulner_pobreza_criancas`: correlação 0.983
- `prop_vulner_pobreza` ↔ `renda_pc`: correlação 0.909
- `prop_vulner_pobreza` ↔ `renda_pc_quintil_1`: correlação 0.946
- `prop_vulner_pobreza` ↔ `renda_pc_quintil_2`: correlação 0.967
- `prop_vulner_pobreza` ↔ `renda_pc_quintil_3`: correlação 0.968
- `prop_vulner_pobreza` ↔ `renda_pc_quintil_4`: correlação 0.940
- `prop_vulner_pobreza` ↔ `renda_pc_exc_renda_nula`: correlação 0.905
- `prop_vulner_pobreza` ↔ `renda_pc_vulner_pobreza`: correlação 0.922
- `prop_vulner_pobreza` ↔ `taxa_dom_vulner_sem_fund`: correlação 0.933
- `prop_vulner_pobreza` ↔ `taxa_nest_ntrab_vulner_15_24`: correlação 0.915
- `prop_vulner_pobreza` ↔ `idhm`: correlação 0.936
- `prop_vulner_pobreza` ↔ `idhm_r`: correlação 0.960
- `prop_vulner_pobreza_criancas` ↔ `renda_pc`: correlação 0.916
- `prop_vulner_pobreza_criancas` ↔ `renda_pc_quintil_1`: correlação 0.961
- `prop_vulner_pobreza_criancas` ↔ `renda_pc_quintil_2`: correlação 0.977
- `prop_vulner_pobreza_criancas` ↔ `renda_pc_quintil_3`: correlação 0.973
- `prop_vulner_pobreza_criancas` ↔ `renda_pc_quintil_4`: correlação 0.946
- `prop_vulner_pobreza_criancas` ↔ `renda_pc_exc_renda_nula`: correlação 0.914
- `prop_vulner_pobreza_criancas` ↔ `taxa_dom_vulner_sem_fund`: correlação 0.911
- `prop_vulner_pobreza_criancas` ↔ `idhm`: correlação 0.918
- `prop_vulner_pobreza_criancas` ↔ `idhm_r`: correlação 0.940
- `prop_renda_10_ricos` ↔ `prop_renda_20_ricos`: correlação 0.935
- `prop_renda_10_ricos` ↔ `prop_renda_80_pobres`: correlação 0.947
- `prop_renda_20_pobres` ↔ `prop_renda_40_pobres`: correlação 0.966
- `prop_renda_20_pobres` ↔ `renda_pc_vulner_pobreza`: correlação 0.905
- `prop_renda_20_ricos` ↔ `prop_renda_60_pobres`: correlação 0.915
- `prop_renda_20_ricos` ↔ `prop_renda_80_pobres`: correlação 0.971
- `prop_renda_20_ricos` ↔ `indice_theil`: correlação 0.931
- `prop_renda_40_pobres` ↔ `prop_renda_60_pobres`: correlação 0.970
- `prop_renda_40_pobres` ↔ `indice_theil`: correlação 0.918
- `prop_renda_60_pobres` ↔ `prop_renda_80_pobres`: correlação 0.935
- `prop_renda_60_pobres` ↔ `indice_theil`: correlação 0.961
- `prop_renda_80_pobres` ↔ `indice_theil`: correlação 0.938
- `razao_10_ricos_40_pobres` ↔ `razao_20_ricos_40_pobres`: correlação 0.992
- `renda_pc` ↔ `renda_pc_decil_10`: correlação 0.940
- `renda_pc` ↔ `renda_pc_quintil_2`: correlação 0.930
- `renda_pc` ↔ `renda_pc_quintil_3`: correlação 0.952
- `renda_pc` ↔ `renda_pc_quintil_4`: correlação 0.973
- `renda_pc` ↔ `renda_pc_quintil_5`: correlação 0.970
- `renda_pc` ↔ `renda_pc_exc_renda_nula`: correlação 0.999
- `renda_pc` ↔ `prop_ocupados_renda_2_sm`: correlação 0.906
- `renda_pc` ↔ `prop_ocupados_renda_3_sm`: correlação 0.907
- `renda_pc` ↔ `renda_media_ocupados`: correlação 0.929
- `renda_pc` ↔ `idhm`: correlação 0.908
- `renda_pc` ↔ `idhm_r`: correlação 0.962
- `renda_pc_quintil_1` ↔ `renda_pc_quintil_2`: correlação 0.983
- `renda_pc_quintil_1` ↔ `renda_pc_quintil_3`: correlação 0.965
- `renda_pc_quintil_1` ↔ `renda_pc_quintil_4`: correlação 0.929
- `renda_pc_quintil_1` ↔ `renda_pc_vulner_pobreza`: correlação 0.905
- `renda_pc_decil_10` ↔ `renda_pc_quintil_5`: correlação 0.993
- `renda_pc_decil_10` ↔ `renda_pc_exc_renda_nula`: correlação 0.943
- `renda_pc_decil_10` ↔ `renda_media_ocupados`: correlação 0.906
- `renda_pc_quintil_2` ↔ `renda_pc_quintil_3`: correlação 0.992
- `renda_pc_quintil_2` ↔ `renda_pc_quintil_4`: correlação 0.966
- `renda_pc_quintil_2` ↔ `renda_pc_exc_renda_nula`: correlação 0.926
- `renda_pc_quintil_2` ↔ `idhm`: correlação 0.907
- `renda_pc_quintil_2` ↔ `idhm_r`: correlação 0.931
- `renda_pc_quintil_3` ↔ `renda_pc_quintil_4`: correlação 0.986
- `renda_pc_quintil_3` ↔ `renda_pc_exc_renda_nula`: correlação 0.949
- `renda_pc_quintil_3` ↔ `idhm`: correlação 0.917
- `renda_pc_quintil_3` ↔ `idhm_r`: correlação 0.947
- `renda_pc_quintil_4` ↔ `renda_pc_exc_renda_nula`: correlação 0.971
- `renda_pc_quintil_4` ↔ `prop_ocupados_renda_2_sm`: correlação 0.905
- `renda_pc_quintil_4` ↔ `idhm`: correlação 0.912
- `renda_pc_quintil_4` ↔ `idhm_r`: correlação 0.949
- `renda_pc_quintil_5` ↔ `renda_pc_exc_renda_nula`: correlação 0.972
- `renda_pc_quintil_5` ↔ `renda_media_ocupados`: correlação 0.926
- `renda_pc_quintil_5` ↔ `idhm_r`: correlação 0.911
- `renda_pc_exc_renda_nula` ↔ `prop_ocupados_renda_2_sm`: correlação 0.907
- `renda_pc_exc_renda_nula` ↔ `prop_ocupados_renda_3_sm`: correlação 0.910
- `renda_pc_exc_renda_nula` ↔ `renda_media_ocupados`: correlação 0.931
- `renda_pc_exc_renda_nula` ↔ `idhm`: correlação 0.904
- `renda_pc_exc_renda_nula` ↔ `idhm_r`: correlação 0.960
- `prop_ocupados_formalizacao` ↔ `prop_ocupados_renda_1_sm`: correlação 0.913
- `prop_ocupados_formalizacao` ↔ `taxa_ocupados_carteira`: correlação 0.924
- `prop_ocupados_formalizacao` ↔ `taxa_sem_fund_informal`: correlação 0.926
- `prop_ocupados_fundamental` ↔ `prop_ocupados_medio`: correlação 0.961
- `prop_ocupados_fundamental` ↔ `taxa_dom_sem_fund`: correlação 0.928
- `prop_ocupados_fundamental` ↔ `indice_escolaridade`: correlação 0.973
- `prop_ocupados_medio` ↔ `indice_escolaridade`: correlação 0.929
- `prop_ocupados_renda_2_sm` ↔ `prop_ocupados_renda_3_sm`: correlação 0.966
- `prop_ocupados_renda_2_sm` ↔ `renda_media_ocupados`: correlação 0.946
- `prop_ocupados_renda_3_sm` ↔ `prop_ocupados_renda_5_sm`: correlação 0.951
- `prop_ocupados_renda_3_sm` ↔ `renda_media_ocupados`: correlação 0.947
- `prop_ocupados_renda_5_sm` ↔ `renda_media_ocupados`: correlação 0.911
- `renda_media_ocupados` ↔ `idhm_r`: correlação 0.915
- `taxa_atividade` ↔ `taxa_atividade_18_24`: correlação 0.915
- `taxa_atividade` ↔ `taxa_atividade_18_mais`: correlação 0.982
- `taxa_atividade` ↔ `taxa_atividade_25_29`: correlação 0.901
- `taxa_desocupacao` ↔ `taxa_desocupacao_18_24`: correlação 0.907
- `taxa_desocupacao` ↔ `taxa_desocupacao_18_mais`: correlação 0.991
- `taxa_desocupacao_18_24` ↔ `taxa_desocupacao_18_mais`: correlação 0.917
- `taxa_energia_eletrica` ↔ `taxa_sem_energia_eletrica`: correlação 1.000
- `taxa_criancas_dom_sem_fund` ↔ `taxa_dom_sem_fund`: correlação 0.966
- `taxa_criancas_dom_sem_fund` ↔ `taxa_dom_vulner_sem_fund`: correlação 0.915
- `taxa_criancas_dom_sem_fund` ↔ `idhm_e`: correlação 0.936
- `taxa_dom_sem_fund` ↔ `indice_escolaridade`: correlação 0.947
- `taxa_dom_sem_fund` ↔ `idhm_e`: correlação 0.939
- `taxa_dom_vulner_sem_fund` ↔ `idhm`: correlação 0.961
- `taxa_dom_vulner_sem_fund` ↔ `idhm_e`: correlação 0.921
- `taxa_dom_vulner_sem_fund` ↔ `idhm_r`: correlação 0.906
- `taxa_sem_fund_informal` ↔ `indice_escolaridade`: correlação 0.918
- `taxa_sem_fund_informal` ↔ `idhm`: correlação 0.910
- `populacao_homens_0_4` ↔ `populacao_homens_10_14`: correlação 0.999
- `populacao_homens_0_4` ↔ `populacao_homens_15_19`: correlação 0.998
- `populacao_homens_0_4` ↔ `populacao_homens_20_24`: correlação 0.998
- `populacao_homens_0_4` ↔ `populacao_homens_25_29`: correlação 0.996
- `populacao_homens_0_4` ↔ `populacao_homens_30_34`: correlação 0.996
- `populacao_homens_0_4` ↔ `populacao_homens_35_39`: correlação 0.995
- `populacao_homens_0_4` ↔ `populacao_homens_40_44`: correlação 0.994
- `populacao_homens_0_4` ↔ `populacao_homens_45_49`: correlação 0.989
- `populacao_homens_0_4` ↔ `populacao_homens_50_54`: correlação 0.984
- `populacao_homens_0_4` ↔ `populacao_homens_55_59`: correlação 0.980
- `populacao_homens_0_4` ↔ `populacao_homens_5_9`: correlação 1.000
- `populacao_homens_0_4` ↔ `populacao_homens_60_64`: correlação 0.977
- `populacao_homens_0_4` ↔ `populacao_homens_65_69`: correlação 0.974
- `populacao_homens_0_4` ↔ `populacao_homens_70_74`: correlação 0.968
- `populacao_homens_0_4` ↔ `populacao_homens_75_79`: correlação 0.958
- `populacao_homens_0_4` ↔ `populacao_homens`: correlação 0.996
- `populacao_homens_0_4` ↔ `populacao_homens_80_mais`: correlação 0.958
- `populacao_homens_0_4` ↔ `populacao_mulheres_0_4`: correlação 1.000
- `populacao_homens_0_4` ↔ `populacao_mulheres_10_14`: correlação 0.999
- `populacao_homens_0_4` ↔ `populacao_mulheres_15_19`: correlação 0.998
- `populacao_homens_0_4` ↔ `populacao_mulheres_20_24`: correlação 0.997
- `populacao_homens_0_4` ↔ `populacao_mulheres_25_29`: correlação 0.996
- `populacao_homens_0_4` ↔ `populacao_mulheres_30_34`: correlação 0.995
- `populacao_homens_0_4` ↔ `populacao_mulheres_35_39`: correlação 0.995
- `populacao_homens_0_4` ↔ `populacao_mulheres_40_44`: correlação 0.993
- `populacao_homens_0_4` ↔ `populacao_mulheres_45_49`: correlação 0.988
- `populacao_homens_0_4` ↔ `populacao_mulheres_50_54`: correlação 0.982
- `populacao_homens_0_4` ↔ `populacao_mulheres_55_59`: correlação 0.977
- `populacao_homens_0_4` ↔ `populacao_mulheres_5_9`: correlação 1.000
- `populacao_homens_0_4` ↔ `populacao_mulheres_60_64`: correlação 0.972
- `populacao_homens_0_4` ↔ `populacao_mulheres_65_69`: correlação 0.968
- `populacao_homens_0_4` ↔ `populacao_mulheres_70_74`: correlação 0.961
- `populacao_homens_0_4` ↔ `populacao_mulheres_75_79`: correlação 0.950
- `populacao_homens_0_4` ↔ `populacao_mulheres_80_mais`: correlação 0.945
- `populacao_homens_0_4` ↔ `populacao_mulheres`: correlação 0.994
- `populacao_homens_0_4` ↔ `populacao_1_menos`: correlação 1.000
- `populacao_homens_0_4` ↔ `populacao_11_14`: correlação 0.999
- `populacao_homens_0_4` ↔ `populacao_11_13`: correlação 0.999
- `populacao_homens_0_4` ↔ `populacao_12_14`: correlação 0.999
- `populacao_homens_0_4` ↔ `populacao_1_3`: correlação 1.000
- `populacao_homens_0_4` ↔ `populacao_15_mais`: correlação 0.993
- `populacao_homens_0_4` ↔ `populacao_15_17`: correlação 0.999
- `populacao_homens_0_4` ↔ `populacao_15_24`: correlação 0.998
- `populacao_homens_0_4` ↔ `populacao_16_18`: correlação 0.998
- `populacao_homens_0_4` ↔ `populacao_18_mais`: correlação 0.992
- `populacao_homens_0_4` ↔ `populacao_18_20`: correlação 0.998
- `populacao_homens_0_4` ↔ `populacao_18_24`: correlação 0.998
- `populacao_homens_0_4` ↔ `populacao_19_21`: correlação 0.998
- `populacao_homens_0_4` ↔ `populacao_25_mais`: correlação 0.990
- `populacao_homens_0_4` ↔ `populacao_4`: correlação 1.000
- `populacao_homens_0_4` ↔ `populacao_5`: correlação 1.000
- `populacao_homens_0_4` ↔ `populacao_6`: correlação 1.000
- `populacao_homens_0_4` ↔ `populacao_6_10`: correlação 1.000
- `populacao_homens_0_4` ↔ `populacao_6_17`: correlação 0.999
- `populacao_homens_0_4` ↔ `populacao_65_mais`: correlação 0.962
- `populacao_homens_0_4` ↔ `populacao`: correlação 0.995
- `populacao_homens_0_4` ↔ `populacao_urbana`: correlação 0.993
- `populacao_homens_0_4` ↔ `populacao_dom_pp`: correlação 0.995
- `populacao_homens_0_4` ↔ `populacao_dom_pp_exc_renda_nula`: correlação 0.995
- `populacao_homens_0_4` ↔ `pea`: correlação 0.993
- `populacao_homens_0_4` ↔ `pea_10_14`: correlação 0.975
- `populacao_homens_0_4` ↔ `pea_15_17`: correlação 0.981
- `populacao_homens_0_4` ↔ `pea_18_mais`: correlação 0.992
- `populacao_homens_0_4` ↔ `pia`: correlação 0.994
- `populacao_homens_0_4` ↔ `pia_10_14`: correlação 0.999
- `populacao_homens_0_4` ↔ `pia_15_17`: correlação 0.999
- `populacao_homens_0_4` ↔ `pia_18_mais`: correlação 0.992
- `populacao_homens_10_14` ↔ `populacao_homens_15_19`: correlação 0.999
- `populacao_homens_10_14` ↔ `populacao_homens_20_24`: correlação 0.998
- `populacao_homens_10_14` ↔ `populacao_homens_25_29`: correlação 0.997
- `populacao_homens_10_14` ↔ `populacao_homens_30_34`: correlação 0.997
- `populacao_homens_10_14` ↔ `populacao_homens_35_39`: correlação 0.997
- `populacao_homens_10_14` ↔ `populacao_homens_40_44`: correlação 0.996
- `populacao_homens_10_14` ↔ `populacao_homens_45_49`: correlação 0.993
- `populacao_homens_10_14` ↔ `populacao_homens_50_54`: correlação 0.989
- `populacao_homens_10_14` ↔ `populacao_homens_55_59`: correlação 0.985
- `populacao_homens_10_14` ↔ `populacao_homens_5_9`: correlação 1.000
- `populacao_homens_10_14` ↔ `populacao_homens_60_64`: correlação 0.982
- `populacao_homens_10_14` ↔ `populacao_homens_65_69`: correlação 0.979
- `populacao_homens_10_14` ↔ `populacao_homens_70_74`: correlação 0.974
- `populacao_homens_10_14` ↔ `populacao_homens_75_79`: correlação 0.965
- `populacao_homens_10_14` ↔ `populacao_homens`: correlação 0.998
- `populacao_homens_10_14` ↔ `populacao_homens_80_mais`: correlação 0.965
- `populacao_homens_10_14` ↔ `populacao_mulheres_0_4`: correlação 0.999
- `populacao_homens_10_14` ↔ `populacao_mulheres_10_14`: correlação 1.000
- `populacao_homens_10_14` ↔ `populacao_mulheres_15_19`: correlação 0.999
- `populacao_homens_10_14` ↔ `populacao_mulheres_20_24`: correlação 0.997
- `populacao_homens_10_14` ↔ `populacao_mulheres_25_29`: correlação 0.997
- `populacao_homens_10_14` ↔ `populacao_mulheres_30_34`: correlação 0.996
- `populacao_homens_10_14` ↔ `populacao_mulheres_35_39`: correlação 0.996
- `populacao_homens_10_14` ↔ `populacao_mulheres_40_44`: correlação 0.995
- `populacao_homens_10_14` ↔ `populacao_mulheres_45_49`: correlação 0.992
- `populacao_homens_10_14` ↔ `populacao_mulheres_50_54`: correlação 0.987
- `populacao_homens_10_14` ↔ `populacao_mulheres_55_59`: correlação 0.982
- `populacao_homens_10_14` ↔ `populacao_mulheres_5_9`: correlação 1.000
- `populacao_homens_10_14` ↔ `populacao_mulheres_60_64`: correlação 0.978
- `populacao_homens_10_14` ↔ `populacao_mulheres_65_69`: correlação 0.975
- `populacao_homens_10_14` ↔ `populacao_mulheres_70_74`: correlação 0.968
- `populacao_homens_10_14` ↔ `populacao_mulheres_75_79`: correlação 0.958
- `populacao_homens_10_14` ↔ `populacao_mulheres_80_mais`: correlação 0.953
- `populacao_homens_10_14` ↔ `populacao_mulheres`: correlação 0.997
- `populacao_homens_10_14` ↔ `populacao_1_menos`: correlação 0.999
- `populacao_homens_10_14` ↔ `populacao_11_14`: correlação 1.000
- `populacao_homens_10_14` ↔ `populacao_11_13`: correlação 1.000
- `populacao_homens_10_14` ↔ `populacao_12_14`: correlação 1.000
- `populacao_homens_10_14` ↔ `populacao_1_3`: correlação 0.999
- `populacao_homens_10_14` ↔ `populacao_15_mais`: correlação 0.995
- `populacao_homens_10_14` ↔ `populacao_15_17`: correlação 0.999
- `populacao_homens_10_14` ↔ `populacao_15_24`: correlação 0.999
- `populacao_homens_10_14` ↔ `populacao_16_18`: correlação 0.999
- `populacao_homens_10_14` ↔ `populacao_18_mais`: correlação 0.995
- `populacao_homens_10_14` ↔ `populacao_18_20`: correlação 0.999
- `populacao_homens_10_14` ↔ `populacao_18_24`: correlação 0.998
- `populacao_homens_10_14` ↔ `populacao_19_21`: correlação 0.998
- `populacao_homens_10_14` ↔ `populacao_25_mais`: correlação 0.993
- `populacao_homens_10_14` ↔ `populacao_4`: correlação 0.999
- `populacao_homens_10_14` ↔ `populacao_5`: correlação 0.999
- `populacao_homens_10_14` ↔ `populacao_6`: correlação 0.999
- `populacao_homens_10_14` ↔ `populacao_6_10`: correlação 1.000
- `populacao_homens_10_14` ↔ `populacao_6_17`: correlação 1.000
- `populacao_homens_10_14` ↔ `populacao_65_mais`: correlação 0.969
- `populacao_homens_10_14` ↔ `populacao`: correlação 0.997
- `populacao_homens_10_14` ↔ `populacao_urbana`: correlação 0.996
- `populacao_homens_10_14` ↔ `populacao_dom_pp`: correlação 0.997
- `populacao_homens_10_14` ↔ `populacao_dom_pp_exc_renda_nula`: correlação 0.997
- `populacao_homens_10_14` ↔ `pea`: correlação 0.995
- `populacao_homens_10_14` ↔ `pea_10_14`: correlação 0.971
- `populacao_homens_10_14` ↔ `pea_15_17`: correlação 0.978
- `populacao_homens_10_14` ↔ `pea_18_mais`: correlação 0.994
- `populacao_homens_10_14` ↔ `pia`: correlação 0.996
- `populacao_homens_10_14` ↔ `pia_10_14`: correlação 1.000
- `populacao_homens_10_14` ↔ `pia_15_17`: correlação 0.999
- `populacao_homens_10_14` ↔ `pia_18_mais`: correlação 0.995
- `populacao_homens_15_19` ↔ `populacao_homens_20_24`: correlação 0.999
- `populacao_homens_15_19` ↔ `populacao_homens_25_29`: correlação 0.997
- `populacao_homens_15_19` ↔ `populacao_homens_30_34`: correlação 0.997
- `populacao_homens_15_19` ↔ `populacao_homens_35_39`: correlação 0.996
- `populacao_homens_15_19` ↔ `populacao_homens_40_44`: correlação 0.996
- `populacao_homens_15_19` ↔ `populacao_homens_45_49`: correlação 0.993
- `populacao_homens_15_19` ↔ `populacao_homens_50_54`: correlação 0.989
- `populacao_homens_15_19` ↔ `populacao_homens_55_59`: correlação 0.985
- `populacao_homens_15_19` ↔ `populacao_homens_5_9`: correlação 0.999
- `populacao_homens_15_19` ↔ `populacao_homens_60_64`: correlação 0.983
- `populacao_homens_15_19` ↔ `populacao_homens_65_69`: correlação 0.980
- `populacao_homens_15_19` ↔ `populacao_homens_70_74`: correlação 0.975
- `populacao_homens_15_19` ↔ `populacao_homens_75_79`: correlação 0.965
- `populacao_homens_15_19` ↔ `populacao_homens`: correlação 0.998
- `populacao_homens_15_19` ↔ `populacao_homens_80_mais`: correlação 0.965
- `populacao_homens_15_19` ↔ `populacao_mulheres_0_4`: correlação 0.998
- `populacao_homens_15_19` ↔ `populacao_mulheres_10_14`: correlação 0.999
- `populacao_homens_15_19` ↔ `populacao_mulheres_15_19`: correlação 1.000
- `populacao_homens_15_19` ↔ `populacao_mulheres_20_24`: correlação 0.998
- `populacao_homens_15_19` ↔ `populacao_mulheres_25_29`: correlação 0.997
- `populacao_homens_15_19` ↔ `populacao_mulheres_30_34`: correlação 0.996
- `populacao_homens_15_19` ↔ `populacao_mulheres_35_39`: correlação 0.996
- `populacao_homens_15_19` ↔ `populacao_mulheres_40_44`: correlação 0.996
- `populacao_homens_15_19` ↔ `populacao_mulheres_45_49`: correlação 0.992
- `populacao_homens_15_19` ↔ `populacao_mulheres_50_54`: correlação 0.987
- `populacao_homens_15_19` ↔ `populacao_mulheres_55_59`: correlação 0.982
- `populacao_homens_15_19` ↔ `populacao_mulheres_5_9`: correlação 0.999
- `populacao_homens_15_19` ↔ `populacao_mulheres_60_64`: correlação 0.979
- `populacao_homens_15_19` ↔ `populacao_mulheres_65_69`: correlação 0.975
- `populacao_homens_15_19` ↔ `populacao_mulheres_70_74`: correlação 0.968
- `populacao_homens_15_19` ↔ `populacao_mulheres_75_79`: correlação 0.958
- `populacao_homens_15_19` ↔ `populacao_mulheres_80_mais`: correlação 0.953
- `populacao_homens_15_19` ↔ `populacao_mulheres`: correlação 0.997
- `populacao_homens_15_19` ↔ `populacao_1_menos`: correlação 0.998
- `populacao_homens_15_19` ↔ `populacao_11_14`: correlação 0.999
- `populacao_homens_15_19` ↔ `populacao_11_13`: correlação 0.999
- `populacao_homens_15_19` ↔ `populacao_12_14`: correlação 0.999
- `populacao_homens_15_19` ↔ `populacao_1_3`: correlação 0.998
- `populacao_homens_15_19` ↔ `populacao_15_mais`: correlação 0.996
- `populacao_homens_15_19` ↔ `populacao_15_17`: correlação 1.000
- `populacao_homens_15_19` ↔ `populacao_15_24`: correlação 1.000
- `populacao_homens_15_19` ↔ `populacao_16_18`: correlação 1.000
- `populacao_homens_15_19` ↔ `populacao_18_mais`: correlação 0.995
- `populacao_homens_15_19` ↔ `populacao_18_20`: correlação 1.000
- `populacao_homens_15_19` ↔ `populacao_18_24`: correlação 0.999
- `populacao_homens_15_19` ↔ `populacao_19_21`: correlação 0.999
- `populacao_homens_15_19` ↔ `populacao_25_mais`: correlação 0.993
- `populacao_homens_15_19` ↔ `populacao_4`: correlação 0.998
- `populacao_homens_15_19` ↔ `populacao_5`: correlação 0.998
- `populacao_homens_15_19` ↔ `populacao_6`: correlação 0.999
- `populacao_homens_15_19` ↔ `populacao_6_10`: correlação 0.999
- `populacao_homens_15_19` ↔ `populacao_6_17`: correlação 0.999
- `populacao_homens_15_19` ↔ `populacao_65_mais`: correlação 0.969
- `populacao_homens_15_19` ↔ `populacao`: correlação 0.997
- `populacao_homens_15_19` ↔ `populacao_urbana`: correlação 0.996
- `populacao_homens_15_19` ↔ `populacao_dom_pp`: correlação 0.997
- `populacao_homens_15_19` ↔ `populacao_dom_pp_exc_renda_nula`: correlação 0.997
- `populacao_homens_15_19` ↔ `pea`: correlação 0.995
- `populacao_homens_15_19` ↔ `pea_10_14`: correlação 0.969
- `populacao_homens_15_19` ↔ `pea_15_17`: correlação 0.978
- `populacao_homens_15_19` ↔ `pea_18_mais`: correlação 0.995
- `populacao_homens_15_19` ↔ `pia`: correlação 0.996
- `populacao_homens_15_19` ↔ `pia_10_14`: correlação 0.999
- `populacao_homens_15_19` ↔ `pia_15_17`: correlação 1.000
- `populacao_homens_15_19` ↔ `pia_18_mais`: correlação 0.995
- `populacao_homens_20_24` ↔ `populacao_homens_25_29`: correlação 0.999
- `populacao_homens_20_24` ↔ `populacao_homens_30_34`: correlação 0.999
- `populacao_homens_20_24` ↔ `populacao_homens_35_39`: correlação 0.998
- `populacao_homens_20_24` ↔ `populacao_homens_40_44`: correlação 0.998
- `populacao_homens_20_24` ↔ `populacao_homens_45_49`: correlação 0.995
- `populacao_homens_20_24` ↔ `populacao_homens_50_54`: correlação 0.991
- `populacao_homens_20_24` ↔ `populacao_homens_55_59`: correlação 0.987
- `populacao_homens_20_24` ↔ `populacao_homens_5_9`: correlação 0.998
- `populacao_homens_20_24` ↔ `populacao_homens_60_64`: correlação 0.984
- `populacao_homens_20_24` ↔ `populacao_homens_65_69`: correlação 0.981
- `populacao_homens_20_24` ↔ `populacao_homens_70_74`: correlação 0.976
- `populacao_homens_20_24` ↔ `populacao_homens_75_79`: correlação 0.967
- `populacao_homens_20_24` ↔ `populacao_homens`: correlação 0.998
- `populacao_homens_20_24` ↔ `populacao_homens_80_mais`: correlação 0.967
- `populacao_homens_20_24` ↔ `populacao_mulheres_0_4`: correlação 0.997
- `populacao_homens_20_24` ↔ `populacao_mulheres_10_14`: correlação 0.998
- `populacao_homens_20_24` ↔ `populacao_mulheres_15_19`: correlação 0.999
- `populacao_homens_20_24` ↔ `populacao_mulheres_20_24`: correlação 1.000
- `populacao_homens_20_24` ↔ `populacao_mulheres_25_29`: correlação 0.999
- `populacao_homens_20_24` ↔ `populacao_mulheres_30_34`: correlação 0.998
- `populacao_homens_20_24` ↔ `populacao_mulheres_35_39`: correlação 0.998
- `populacao_homens_20_24` ↔ `populacao_mulheres_40_44`: correlação 0.998
- `populacao_homens_20_24` ↔ `populacao_mulheres_45_49`: correlação 0.994
- `populacao_homens_20_24` ↔ `populacao_mulheres_50_54`: correlação 0.989
- `populacao_homens_20_24` ↔ `populacao_mulheres_55_59`: correlação 0.984
- `populacao_homens_20_24` ↔ `populacao_mulheres_5_9`: correlação 0.998
- `populacao_homens_20_24` ↔ `populacao_mulheres_60_64`: correlação 0.981
- `populacao_homens_20_24` ↔ `populacao_mulheres_65_69`: correlação 0.977
- `populacao_homens_20_24` ↔ `populacao_mulheres_70_74`: correlação 0.970
- `populacao_homens_20_24` ↔ `populacao_mulheres_75_79`: correlação 0.960
- `populacao_homens_20_24` ↔ `populacao_mulheres_80_mais`: correlação 0.956
- `populacao_homens_20_24` ↔ `populacao_mulheres`: correlação 0.998
- `populacao_homens_20_24` ↔ `populacao_1_menos`: correlação 0.998
- `populacao_homens_20_24` ↔ `populacao_11_14`: correlação 0.998
- `populacao_homens_20_24` ↔ `populacao_11_13`: correlação 0.998
- `populacao_homens_20_24` ↔ `populacao_12_14`: correlação 0.998
- `populacao_homens_20_24` ↔ `populacao_1_3`: correlação 0.997
- `populacao_homens_20_24` ↔ `populacao_15_mais`: correlação 0.997
- `populacao_homens_20_24` ↔ `populacao_15_17`: correlação 0.998
- `populacao_homens_20_24` ↔ `populacao_15_24`: correlação 1.000
- `populacao_homens_20_24` ↔ `populacao_16_18`: correlação 0.998
- `populacao_homens_20_24` ↔ `populacao_18_mais`: correlação 0.997
- `populacao_homens_20_24` ↔ `populacao_18_20`: correlação 0.999
- `populacao_homens_20_24` ↔ `populacao_18_24`: correlação 1.000
- `populacao_homens_20_24` ↔ `populacao_19_21`: correlação 1.000
- `populacao_homens_20_24` ↔ `populacao_25_mais`: correlação 0.995
- `populacao_homens_20_24` ↔ `populacao_4`: correlação 0.997
- `populacao_homens_20_24` ↔ `populacao_5`: correlação 0.997
- `populacao_homens_20_24` ↔ `populacao_6`: correlação 0.997
- `populacao_homens_20_24` ↔ `populacao_6_10`: correlação 0.998
- `populacao_homens_20_24` ↔ `populacao_6_17`: correlação 0.998
- `populacao_homens_20_24` ↔ `populacao_65_mais`: correlação 0.971
- `populacao_homens_20_24` ↔ `populacao`: correlação 0.998
- `populacao_homens_20_24` ↔ `populacao_urbana`: correlação 0.997
- `populacao_homens_20_24` ↔ `populacao_dom_pp`: correlação 0.998
- `populacao_homens_20_24` ↔ `populacao_dom_pp_exc_renda_nula`: correlação 0.998
- `populacao_homens_20_24` ↔ `pea`: correlação 0.998
- `populacao_homens_20_24` ↔ `pea_10_14`: correlação 0.968
- `populacao_homens_20_24` ↔ `pea_15_17`: correlação 0.982
- `populacao_homens_20_24` ↔ `pea_18_mais`: correlação 0.997
- `populacao_homens_20_24` ↔ `pia`: correlação 0.998
- `populacao_homens_20_24` ↔ `pia_10_14`: correlação 0.998
- `populacao_homens_20_24` ↔ `pia_15_17`: correlação 0.998
- `populacao_homens_20_24` ↔ `pia_18_mais`: correlação 0.997
- `populacao_homens_25_29` ↔ `populacao_homens_30_34`: correlação 1.000
- `populacao_homens_25_29` ↔ `populacao_homens_35_39`: correlação 0.999
- `populacao_homens_25_29` ↔ `populacao_homens_40_44`: correlação 0.999
- `populacao_homens_25_29` ↔ `populacao_homens_45_49`: correlação 0.996
- `populacao_homens_25_29` ↔ `populacao_homens_50_54`: correlação 0.993
- `populacao_homens_25_29` ↔ `populacao_homens_55_59`: correlação 0.990
- `populacao_homens_25_29` ↔ `populacao_homens_5_9`: correlação 0.997
- `populacao_homens_25_29` ↔ `populacao_homens_60_64`: correlação 0.987
- `populacao_homens_25_29` ↔ `populacao_homens_65_69`: correlação 0.983
- `populacao_homens_25_29` ↔ `populacao_homens_70_74`: correlação 0.978
- `populacao_homens_25_29` ↔ `populacao_homens_75_79`: correlação 0.970
- `populacao_homens_25_29` ↔ `populacao_homens`: correlação 0.999
- `populacao_homens_25_29` ↔ `populacao_homens_80_mais`: correlação 0.970
- `populacao_homens_25_29` ↔ `populacao_mulheres_0_4`: correlação 0.996
- `populacao_homens_25_29` ↔ `populacao_mulheres_10_14`: correlação 0.997
- `populacao_homens_25_29` ↔ `populacao_mulheres_15_19`: correlação 0.997
- `populacao_homens_25_29` ↔ `populacao_mulheres_20_24`: correlação 0.999
- `populacao_homens_25_29` ↔ `populacao_mulheres_25_29`: correlação 1.000
- `populacao_homens_25_29` ↔ `populacao_mulheres_30_34`: correlação 1.000
- `populacao_homens_25_29` ↔ `populacao_mulheres_35_39`: correlação 0.999
- `populacao_homens_25_29` ↔ `populacao_mulheres_40_44`: correlação 0.998
- `populacao_homens_25_29` ↔ `populacao_mulheres_45_49`: correlação 0.996
- `populacao_homens_25_29` ↔ `populacao_mulheres_50_54`: correlação 0.992
- `populacao_homens_25_29` ↔ `populacao_mulheres_55_59`: correlação 0.987
- `populacao_homens_25_29` ↔ `populacao_mulheres_5_9`: correlação 0.997
- `populacao_homens_25_29` ↔ `populacao_mulheres_60_64`: correlação 0.983
- `populacao_homens_25_29` ↔ `populacao_mulheres_65_69`: correlação 0.980
- `populacao_homens_25_29` ↔ `populacao_mulheres_70_74`: correlação 0.973
- `populacao_homens_25_29` ↔ `populacao_mulheres_75_79`: correlação 0.964
- `populacao_homens_25_29` ↔ `populacao_mulheres_80_mais`: correlação 0.959
- `populacao_homens_25_29` ↔ `populacao_mulheres`: correlação 0.999
- `populacao_homens_25_29` ↔ `populacao_1_menos`: correlação 0.996
- `populacao_homens_25_29` ↔ `populacao_11_14`: correlação 0.997
- `populacao_homens_25_29` ↔ `populacao_11_13`: correlação 0.997
- `populacao_homens_25_29` ↔ `populacao_12_14`: correlação 0.997
- `populacao_homens_25_29` ↔ `populacao_1_3`: correlação 0.996
- `populacao_homens_25_29` ↔ `populacao_15_mais`: correlação 0.998
- `populacao_homens_25_29` ↔ `populacao_15_17`: correlação 0.997
- `populacao_homens_25_29` ↔ `populacao_15_24`: correlação 0.999
- `populacao_homens_25_29` ↔ `populacao_16_18`: correlação 0.997
- `populacao_homens_25_29` ↔ `populacao_18_mais`: correlação 0.998
- `populacao_homens_25_29` ↔ `populacao_18_20`: correlação 0.998
- `populacao_homens_25_29` ↔ `populacao_18_24`: correlação 0.999
- `populacao_homens_25_29` ↔ `populacao_19_21`: correlação 0.999
- `populacao_homens_25_29` ↔ `populacao_25_mais`: correlação 0.997
- `populacao_homens_25_29` ↔ `populacao_4`: correlação 0.996
- `populacao_homens_25_29` ↔ `populacao_5`: correlação 0.996
- `populacao_homens_25_29` ↔ `populacao_6`: correlação 0.996
- `populacao_homens_25_29` ↔ `populacao_6_10`: correlação 0.997
- `populacao_homens_25_29` ↔ `populacao_6_17`: correlação 0.997
- `populacao_homens_25_29` ↔ `populacao_65_mais`: correlação 0.974
- `populacao_homens_25_29` ↔ `populacao`: correlação 0.999
- `populacao_homens_25_29` ↔ `populacao_urbana`: correlação 0.998
- `populacao_homens_25_29` ↔ `populacao_dom_pp`: correlação 0.999
- `populacao_homens_25_29` ↔ `populacao_dom_pp_exc_renda_nula`: correlação 0.999
- `populacao_homens_25_29` ↔ `pea`: correlação 0.999
- `populacao_homens_25_29` ↔ `pea_10_14`: correlação 0.966
- `populacao_homens_25_29` ↔ `pea_15_17`: correlação 0.981
- `populacao_homens_25_29` ↔ `pea_18_mais`: correlação 0.999
- `populacao_homens_25_29` ↔ `pia`: correlação 0.998
- `populacao_homens_25_29` ↔ `pia_10_14`: correlação 0.997
- `populacao_homens_25_29` ↔ `pia_15_17`: correlação 0.997
- `populacao_homens_25_29` ↔ `pia_18_mais`: correlação 0.998
- `populacao_homens_30_34` ↔ `populacao_homens_35_39`: correlação 1.000
- `populacao_homens_30_34` ↔ `populacao_homens_40_44`: correlação 0.999
- `populacao_homens_30_34` ↔ `populacao_homens_45_49`: correlação 0.997
- `populacao_homens_30_34` ↔ `populacao_homens_50_54`: correlação 0.994
- `populacao_homens_30_34` ↔ `populacao_homens_55_59`: correlação 0.991
- `populacao_homens_30_34` ↔ `populacao_homens_5_9`: correlação 0.996
- `populacao_homens_30_34` ↔ `populacao_homens_60_64`: correlação 0.988
- `populacao_homens_30_34` ↔ `populacao_homens_65_69`: correlação 0.985
- `populacao_homens_30_34` ↔ `populacao_homens_70_74`: correlação 0.980
- `populacao_homens_30_34` ↔ `populacao_homens_75_79`: correlação 0.972
- `populacao_homens_30_34` ↔ `populacao_homens`: correlação 0.999
- `populacao_homens_30_34` ↔ `populacao_homens_80_mais`: correlação 0.971
- `populacao_homens_30_34` ↔ `populacao_mulheres_0_4`: correlação 0.996
- `populacao_homens_30_34` ↔ `populacao_mulheres_10_14`: correlação 0.997
- `populacao_homens_30_34` ↔ `populacao_mulheres_15_19`: correlação 0.996
- `populacao_homens_30_34` ↔ `populacao_mulheres_20_24`: correlação 0.998
- `populacao_homens_30_34` ↔ `populacao_mulheres_25_29`: correlação 0.999
- `populacao_homens_30_34` ↔ `populacao_mulheres_30_34`: correlação 1.000
- `populacao_homens_30_34` ↔ `populacao_mulheres_35_39`: correlação 0.999
- `populacao_homens_30_34` ↔ `populacao_mulheres_40_44`: correlação 0.999
- `populacao_homens_30_34` ↔ `populacao_mulheres_45_49`: correlação 0.996
- `populacao_homens_30_34` ↔ `populacao_mulheres_50_54`: correlação 0.993
- `populacao_homens_30_34` ↔ `populacao_mulheres_55_59`: correlação 0.989
- `populacao_homens_30_34` ↔ `populacao_mulheres_5_9`: correlação 0.996
- `populacao_homens_30_34` ↔ `populacao_mulheres_60_64`: correlação 0.985
- `populacao_homens_30_34` ↔ `populacao_mulheres_65_69`: correlação 0.981
- `populacao_homens_30_34` ↔ `populacao_mulheres_70_74`: correlação 0.975
- `populacao_homens_30_34` ↔ `populacao_mulheres_75_79`: correlação 0.966
- `populacao_homens_30_34` ↔ `populacao_mulheres_80_mais`: correlação 0.961
- `populacao_homens_30_34` ↔ `populacao_mulheres`: correlação 0.999
- `populacao_homens_30_34` ↔ `populacao_1_menos`: correlação 0.996
- `populacao_homens_30_34` ↔ `populacao_11_14`: correlação 0.997
- `populacao_homens_30_34` ↔ `populacao_11_13`: correlação 0.997
- `populacao_homens_30_34` ↔ `populacao_12_14`: correlação 0.997
- `populacao_homens_30_34` ↔ `populacao_1_3`: correlação 0.996
- `populacao_homens_30_34` ↔ `populacao_15_mais`: correlação 0.999
- `populacao_homens_30_34` ↔ `populacao_15_17`: correlação 0.996
- `populacao_homens_30_34` ↔ `populacao_15_24`: correlação 0.998
- `populacao_homens_30_34` ↔ `populacao_16_18`: correlação 0.996
- `populacao_homens_30_34` ↔ `populacao_18_mais`: correlação 0.998
- `populacao_homens_30_34` ↔ `populacao_18_20`: correlação 0.997
- `populacao_homens_30_34` ↔ `populacao_18_24`: correlação 0.998
- `populacao_homens_30_34` ↔ `populacao_19_21`: correlação 0.998
- `populacao_homens_30_34` ↔ `populacao_25_mais`: correlação 0.997
- `populacao_homens_30_34` ↔ `populacao_4`: correlação 0.996
- `populacao_homens_30_34` ↔ `populacao_5`: correlação 0.996
- `populacao_homens_30_34` ↔ `populacao_6`: correlação 0.996
- `populacao_homens_30_34` ↔ `populacao_6_10`: correlação 0.996
- `populacao_homens_30_34` ↔ `populacao_6_17`: correlação 0.997
- `populacao_homens_30_34` ↔ `populacao_65_mais`: correlação 0.976
- `populacao_homens_30_34` ↔ `populacao`: correlação 0.999
- `populacao_homens_30_34` ↔ `populacao_urbana`: correlação 0.999
- `populacao_homens_30_34` ↔ `populacao_dom_pp`: correlação 0.999
- `populacao_homens_30_34` ↔ `populacao_dom_pp_exc_renda_nula`: correlação 0.999
- `populacao_homens_30_34` ↔ `pea`: correlação 0.999
- `populacao_homens_30_34` ↔ `pea_10_14`: correlação 0.965
- `populacao_homens_30_34` ↔ `pea_15_17`: correlação 0.980
- `populacao_homens_30_34` ↔ `pea_18_mais`: correlação 0.999
- `populacao_homens_30_34` ↔ `pia`: correlação 0.999
- `populacao_homens_30_34` ↔ `pia_10_14`: correlação 0.997
- `populacao_homens_30_34` ↔ `pia_15_17`: correlação 0.996
- `populacao_homens_30_34` ↔ `pia_18_mais`: correlação 0.998
- `populacao_homens_35_39` ↔ `populacao_homens_40_44`: correlação 1.000
- `populacao_homens_35_39` ↔ `populacao_homens_45_49`: correlação 0.998
- `populacao_homens_35_39` ↔ `populacao_homens_50_54`: correlação 0.995
- `populacao_homens_35_39` ↔ `populacao_homens_55_59`: correlação 0.993
- `populacao_homens_35_39` ↔ `populacao_homens_5_9`: correlação 0.996
- `populacao_homens_35_39` ↔ `populacao_homens_60_64`: correlação 0.990
- `populacao_homens_35_39` ↔ `populacao_homens_65_69`: correlação 0.987
- `populacao_homens_35_39` ↔ `populacao_homens_70_74`: correlação 0.982
- `populacao_homens_35_39` ↔ `populacao_homens_75_79`: correlação 0.974
- `populacao_homens_35_39` ↔ `populacao_homens`: correlação 0.999
- `populacao_homens_35_39` ↔ `populacao_homens_80_mais`: correlação 0.973
- `populacao_homens_35_39` ↔ `populacao_mulheres_0_4`: correlação 0.995
- `populacao_homens_35_39` ↔ `populacao_mulheres_10_14`: correlação 0.996
- `populacao_homens_35_39` ↔ `populacao_mulheres_15_19`: correlação 0.995
- `populacao_homens_35_39` ↔ `populacao_mulheres_20_24`: correlação 0.997
- `populacao_homens_35_39` ↔ `populacao_mulheres_25_29`: correlação 0.999
- `populacao_homens_35_39` ↔ `populacao_mulheres_30_34`: correlação 0.999
- `populacao_homens_35_39` ↔ `populacao_mulheres_35_39`: correlação 1.000
- `populacao_homens_35_39` ↔ `populacao_mulheres_40_44`: correlação 0.999
- `populacao_homens_35_39` ↔ `populacao_mulheres_45_49`: correlação 0.997
- `populacao_homens_35_39` ↔ `populacao_mulheres_50_54`: correlação 0.994
- `populacao_homens_35_39` ↔ `populacao_mulheres_55_59`: correlação 0.990
- `populacao_homens_35_39` ↔ `populacao_mulheres_5_9`: correlação 0.996
- `populacao_homens_35_39` ↔ `populacao_mulheres_60_64`: correlação 0.987
- `populacao_homens_35_39` ↔ `populacao_mulheres_65_69`: correlação 0.983
- `populacao_homens_35_39` ↔ `populacao_mulheres_70_74`: correlação 0.977
- `populacao_homens_35_39` ↔ `populacao_mulheres_75_79`: correlação 0.968
- `populacao_homens_35_39` ↔ `populacao_mulheres_80_mais`: correlação 0.963
- `populacao_homens_35_39` ↔ `populacao_mulheres`: correlação 0.999
- `populacao_homens_35_39` ↔ `populacao_1_menos`: correlação 0.995
- `populacao_homens_35_39` ↔ `populacao_11_14`: correlação 0.997
- `populacao_homens_35_39` ↔ `populacao_11_13`: correlação 0.997
- `populacao_homens_35_39` ↔ `populacao_12_14`: correlação 0.996
- `populacao_homens_35_39` ↔ `populacao_1_3`: correlação 0.995
- `populacao_homens_35_39` ↔ `populacao_15_mais`: correlação 0.999
- `populacao_homens_35_39` ↔ `populacao_15_17`: correlação 0.995
- `populacao_homens_35_39` ↔ `populacao_15_24`: correlação 0.997
- `populacao_homens_35_39` ↔ `populacao_16_18`: correlação 0.995
- `populacao_homens_35_39` ↔ `populacao_18_mais`: correlação 0.999
- `populacao_homens_35_39` ↔ `populacao_18_20`: correlação 0.997
- `populacao_homens_35_39` ↔ `populacao_18_24`: correlação 0.997
- `populacao_homens_35_39` ↔ `populacao_19_21`: correlação 0.997
- `populacao_homens_35_39` ↔ `populacao_25_mais`: correlação 0.998
- `populacao_homens_35_39` ↔ `populacao_4`: correlação 0.995
- `populacao_homens_35_39` ↔ `populacao_5`: correlação 0.995
- `populacao_homens_35_39` ↔ `populacao_6`: correlação 0.996
- `populacao_homens_35_39` ↔ `populacao_6_10`: correlação 0.996
- `populacao_homens_35_39` ↔ `populacao_6_17`: correlação 0.996
- `populacao_homens_35_39` ↔ `populacao_65_mais`: correlação 0.978
- `populacao_homens_35_39` ↔ `populacao`: correlação 0.999
- `populacao_homens_35_39` ↔ `populacao_urbana`: correlação 0.999
- `populacao_homens_35_39` ↔ `populacao_dom_pp`: correlação 0.999
- `populacao_homens_35_39` ↔ `populacao_dom_pp_exc_renda_nula`: correlação 0.999
- `populacao_homens_35_39` ↔ `pea`: correlação 0.999
- `populacao_homens_35_39` ↔ `pea_10_14`: correlação 0.963
- `populacao_homens_35_39` ↔ `pea_15_17`: correlação 0.979
- `populacao_homens_35_39` ↔ `pea_18_mais`: correlação 0.999
- `populacao_homens_35_39` ↔ `pia`: correlação 0.999
- `populacao_homens_35_39` ↔ `pia_10_14`: correlação 0.997
- `populacao_homens_35_39` ↔ `pia_15_17`: correlação 0.996
- `populacao_homens_35_39` ↔ `pia_18_mais`: correlação 0.999
- `populacao_homens_40_44` ↔ `populacao_homens_45_49`: correlação 0.999
- `populacao_homens_40_44` ↔ `populacao_homens_50_54`: correlação 0.996
- `populacao_homens_40_44` ↔ `populacao_homens_55_59`: correlação 0.994
- `populacao_homens_40_44` ↔ `populacao_homens_5_9`: correlação 0.995
- `populacao_homens_40_44` ↔ `populacao_homens_60_64`: correlação 0.992
- `populacao_homens_40_44` ↔ `populacao_homens_65_69`: correlação 0.989
- `populacao_homens_40_44` ↔ `populacao_homens_70_74`: correlação 0.984
- `populacao_homens_40_44` ↔ `populacao_homens_75_79`: correlação 0.977
- `populacao_homens_40_44` ↔ `populacao_homens`: correlação 0.999
- `populacao_homens_40_44` ↔ `populacao_homens_80_mais`: correlação 0.976
- `populacao_homens_40_44` ↔ `populacao_mulheres_0_4`: correlação 0.994
- `populacao_homens_40_44` ↔ `populacao_mulheres_10_14`: correlação 0.996
- `populacao_homens_40_44` ↔ `populacao_mulheres_15_19`: correlação 0.995
- `populacao_homens_40_44` ↔ `populacao_mulheres_20_24`: correlação 0.996
- `populacao_homens_40_44` ↔ `populacao_mulheres_25_29`: correlação 0.998
- `populacao_homens_40_44` ↔ `populacao_mulheres_30_34`: correlação 0.999
- `populacao_homens_40_44` ↔ `populacao_mulheres_35_39`: correlação 0.999
- `populacao_homens_40_44` ↔ `populacao_mulheres_40_44`: correlação 1.000
- `populacao_homens_40_44` ↔ `populacao_mulheres_45_49`: correlação 0.998
- `populacao_homens_40_44` ↔ `populacao_mulheres_50_54`: correlação 0.995
- `populacao_homens_40_44` ↔ `populacao_mulheres_55_59`: correlação 0.992
- `populacao_homens_40_44` ↔ `populacao_mulheres_5_9`: correlação 0.995
- `populacao_homens_40_44` ↔ `populacao_mulheres_60_64`: correlação 0.989
- `populacao_homens_40_44` ↔ `populacao_mulheres_65_69`: correlação 0.985
- `populacao_homens_40_44` ↔ `populacao_mulheres_70_74`: correlação 0.979
- `populacao_homens_40_44` ↔ `populacao_mulheres_75_79`: correlação 0.971
- `populacao_homens_40_44` ↔ `populacao_mulheres_80_mais`: correlação 0.966
- `populacao_homens_40_44` ↔ `populacao_mulheres`: correlação 0.999
- `populacao_homens_40_44` ↔ `populacao_1_menos`: correlação 0.994
- `populacao_homens_40_44` ↔ `populacao_11_14`: correlação 0.996
- `populacao_homens_40_44` ↔ `populacao_11_13`: correlação 0.996
- `populacao_homens_40_44` ↔ `populacao_12_14`: correlação 0.996
- `populacao_homens_40_44` ↔ `populacao_1_3`: correlação 0.994
- `populacao_homens_40_44` ↔ `populacao_15_mais`: correlação 0.999
- `populacao_homens_40_44` ↔ `populacao_15_17`: correlação 0.995
- `populacao_homens_40_44` ↔ `populacao_15_24`: correlação 0.997
- `populacao_homens_40_44` ↔ `populacao_16_18`: correlação 0.995
- `populacao_homens_40_44` ↔ `populacao_18_mais`: correlação 0.999
- `populacao_homens_40_44` ↔ `populacao_18_20`: correlação 0.996
- `populacao_homens_40_44` ↔ `populacao_18_24`: correlação 0.997
- `populacao_homens_40_44` ↔ `populacao_19_21`: correlação 0.997
- `populacao_homens_40_44` ↔ `populacao_25_mais`: correlação 0.999
- `populacao_homens_40_44` ↔ `populacao_4`: correlação 0.994
- `populacao_homens_40_44` ↔ `populacao_5`: correlação 0.994
- `populacao_homens_40_44` ↔ `populacao_6`: correlação 0.995
- `populacao_homens_40_44` ↔ `populacao_6_10`: correlação 0.995
- `populacao_homens_40_44` ↔ `populacao_6_17`: correlação 0.996
- `populacao_homens_40_44` ↔ `populacao_65_mais`: correlação 0.980
- `populacao_homens_40_44` ↔ `populacao`: correlação 0.999
- `populacao_homens_40_44` ↔ `populacao_urbana`: correlação 0.999
- `populacao_homens_40_44` ↔ `populacao_dom_pp`: correlação 0.999
- `populacao_homens_40_44` ↔ `populacao_dom_pp_exc_renda_nula`: correlação 0.999
- `populacao_homens_40_44` ↔ `pea`: correlação 0.999
- `populacao_homens_40_44` ↔ `pea_10_14`: correlação 0.960
- `populacao_homens_40_44` ↔ `pea_15_17`: correlação 0.978
- `populacao_homens_40_44` ↔ `pea_18_mais`: correlação 0.999
- `populacao_homens_40_44` ↔ `pia`: correlação 0.999
- `populacao_homens_40_44` ↔ `pia_10_14`: correlação 0.996
- `populacao_homens_40_44` ↔ `pia_15_17`: correlação 0.995
- `populacao_homens_40_44` ↔ `pia_18_mais`: correlação 0.999
- `populacao_homens_45_49` ↔ `populacao_homens_50_54`: correlação 0.999
- `populacao_homens_45_49` ↔ `populacao_homens_55_59`: correlação 0.998
- `populacao_homens_45_49` ↔ `populacao_homens_5_9`: correlação 0.991
- `populacao_homens_45_49` ↔ `populacao_homens_60_64`: correlação 0.996
- `populacao_homens_45_49` ↔ `populacao_homens_65_69`: correlação 0.994
- `populacao_homens_45_49` ↔ `populacao_homens_70_74`: correlação 0.991
- `populacao_homens_45_49` ↔ `populacao_homens_75_79`: correlação 0.985
- `populacao_homens_45_49` ↔ `populacao_homens`: correlação 0.998
- `populacao_homens_45_49` ↔ `populacao_homens_80_mais`: correlação 0.983
- `populacao_homens_45_49` ↔ `populacao_mulheres_0_4`: correlação 0.990
- `populacao_homens_45_49` ↔ `populacao_mulheres_10_14`: correlação 0.993
- `populacao_homens_45_49` ↔ `populacao_mulheres_15_19`: correlação 0.992
- `populacao_homens_45_49` ↔ `populacao_mulheres_20_24`: correlação 0.993
- `populacao_homens_45_49` ↔ `populacao_mulheres_25_29`: correlação 0.995
- `populacao_homens_45_49` ↔ `populacao_mulheres_30_34`: correlação 0.996
- `populacao_homens_45_49` ↔ `populacao_mulheres_35_39`: correlação 0.998
- `populacao_homens_45_49` ↔ `populacao_mulheres_40_44`: correlação 0.999
- `populacao_homens_45_49` ↔ `populacao_mulheres_45_49`: correlação 1.000
- `populacao_homens_45_49` ↔ `populacao_mulheres_50_54`: correlação 0.998
- `populacao_homens_45_49` ↔ `populacao_mulheres_55_59`: correlação 0.996
- `populacao_homens_45_49` ↔ `populacao_mulheres_5_9`: correlação 0.991
- `populacao_homens_45_49` ↔ `populacao_mulheres_60_64`: correlação 0.994
- `populacao_homens_45_49` ↔ `populacao_mulheres_65_69`: correlação 0.992
- `populacao_homens_45_49` ↔ `populacao_mulheres_70_74`: correlação 0.987
- `populacao_homens_45_49` ↔ `populacao_mulheres_75_79`: correlação 0.980
- `populacao_homens_45_49` ↔ `populacao_mulheres_80_mais`: correlação 0.976
- `populacao_homens_45_49` ↔ `populacao_mulheres`: correlação 0.999
- `populacao_homens_45_49` ↔ `populacao_1_menos`: correlação 0.989
- `populacao_homens_45_49` ↔ `populacao_11_14`: correlação 0.993
- `populacao_homens_45_49` ↔ `populacao_11_13`: correlação 0.993
- `populacao_homens_45_49` ↔ `populacao_12_14`: correlação 0.993
- `populacao_homens_45_49` ↔ `populacao_1_3`: correlação 0.989
- `populacao_homens_45_49` ↔ `populacao_15_mais`: correlação 0.999
- `populacao_homens_45_49` ↔ `populacao_15_17`: correlação 0.992
- `populacao_homens_45_49` ↔ `populacao_15_24`: correlação 0.994
- `populacao_homens_45_49` ↔ `populacao_16_18`: correlação 0.992
- `populacao_homens_45_49` ↔ `populacao_18_mais`: correlação 0.999
- `populacao_homens_45_49` ↔ `populacao_18_20`: correlação 0.994
- `populacao_homens_45_49` ↔ `populacao_18_24`: correlação 0.994
- `populacao_homens_45_49` ↔ `populacao_19_21`: correlação 0.995
- `populacao_homens_45_49` ↔ `populacao_25_mais`: correlação 1.000
- `populacao_homens_45_49` ↔ `populacao_4`: correlação 0.990
- `populacao_homens_45_49` ↔ `populacao_5`: correlação 0.990
- `populacao_homens_45_49` ↔ `populacao_6`: correlação 0.991
- `populacao_homens_45_49` ↔ `populacao_6_10`: correlação 0.991
- `populacao_homens_45_49` ↔ `populacao_6_17`: correlação 0.992
- `populacao_homens_45_49` ↔ `populacao_65_mais`: correlação 0.987
- `populacao_homens_45_49` ↔ `populacao`: correlação 0.999
- `populacao_homens_45_49` ↔ `populacao_urbana`: correlação 0.999
- `populacao_homens_45_49` ↔ `populacao_dom_pp`: correlação 0.999
- `populacao_homens_45_49` ↔ `populacao_dom_pp_exc_renda_nula`: correlação 0.999
- `populacao_homens_45_49` ↔ `pea`: correlação 0.998
- `populacao_homens_45_49` ↔ `pea_10_14`: correlação 0.951
- `populacao_homens_45_49` ↔ `pea_15_17`: correlação 0.971
- `populacao_homens_45_49` ↔ `pea_18_mais`: correlação 0.999
- `populacao_homens_45_49` ↔ `pia`: correlação 0.999
- `populacao_homens_45_49` ↔ `pia_10_14`: correlação 0.993
- `populacao_homens_45_49` ↔ `pia_15_17`: correlação 0.992
- `populacao_homens_45_49` ↔ `pia_18_mais`: correlação 0.999
- `populacao_homens_50_54` ↔ `populacao_homens_55_59`: correlação 1.000
- `populacao_homens_50_54` ↔ `populacao_homens_5_9`: correlação 0.986
- `populacao_homens_50_54` ↔ `populacao_homens_60_64`: correlação 0.999
- `populacao_homens_50_54` ↔ `populacao_homens_65_69`: correlação 0.997
- `populacao_homens_50_54` ↔ `populacao_homens_70_74`: correlação 0.994
- `populacao_homens_50_54` ↔ `populacao_homens_75_79`: correlação 0.990
- `populacao_homens_50_54` ↔ `populacao_homens`: correlação 0.996
- `populacao_homens_50_54` ↔ `populacao_homens_80_mais`: correlação 0.988
- `populacao_homens_50_54` ↔ `populacao_mulheres_0_4`: correlação 0.984
- `populacao_homens_50_54` ↔ `populacao_mulheres_10_14`: correlação 0.988
- `populacao_homens_50_54` ↔ `populacao_mulheres_15_19`: correlação 0.987
- `populacao_homens_50_54` ↔ `populacao_mulheres_20_24`: correlação 0.988
- `populacao_homens_50_54` ↔ `populacao_mulheres_25_29`: correlação 0.991
- `populacao_homens_50_54` ↔ `populacao_mulheres_30_34`: correlação 0.993
- `populacao_homens_50_54` ↔ `populacao_mulheres_35_39`: correlação 0.995
- `populacao_homens_50_54` ↔ `populacao_mulheres_40_44`: correlação 0.996
- `populacao_homens_50_54` ↔ `populacao_mulheres_45_49`: correlação 0.999
- `populacao_homens_50_54` ↔ `populacao_mulheres_50_54`: correlação 1.000
- `populacao_homens_50_54` ↔ `populacao_mulheres_55_59`: correlação 0.999
- `populacao_homens_50_54` ↔ `populacao_mulheres_5_9`: correlação 0.986
- `populacao_homens_50_54` ↔ `populacao_mulheres_60_64`: correlação 0.997
- `populacao_homens_50_54` ↔ `populacao_mulheres_65_69`: correlação 0.995
- `populacao_homens_50_54` ↔ `populacao_mulheres_70_74`: correlação 0.991
- `populacao_homens_50_54` ↔ `populacao_mulheres_75_79`: correlação 0.986
- `populacao_homens_50_54` ↔ `populacao_mulheres_80_mais`: correlação 0.982
- `populacao_homens_50_54` ↔ `populacao_mulheres`: correlação 0.997
- `populacao_homens_50_54` ↔ `populacao_1_menos`: correlação 0.984
- `populacao_homens_50_54` ↔ `populacao_11_14`: correlação 0.989
- `populacao_homens_50_54` ↔ `populacao_11_13`: correlação 0.989
- `populacao_homens_50_54` ↔ `populacao_12_14`: correlação 0.988
- `populacao_homens_50_54` ↔ `populacao_1_3`: correlação 0.984
- `populacao_homens_50_54` ↔ `populacao_15_mais`: correlação 0.998
- `populacao_homens_50_54` ↔ `populacao_15_17`: correlação 0.987
- `populacao_homens_50_54` ↔ `populacao_15_24`: correlação 0.989
- `populacao_homens_50_54` ↔ `populacao_16_18`: correlação 0.987
- `populacao_homens_50_54` ↔ `populacao_18_mais`: correlação 0.998
- `populacao_homens_50_54` ↔ `populacao_18_20`: correlação 0.989
- `populacao_homens_50_54` ↔ `populacao_18_24`: correlação 0.989
- `populacao_homens_50_54` ↔ `populacao_19_21`: correlação 0.990
- `populacao_homens_50_54` ↔ `populacao_25_mais`: correlação 0.999
- `populacao_homens_50_54` ↔ `populacao_4`: correlação 0.985
- `populacao_homens_50_54` ↔ `populacao_5`: correlação 0.985
- `populacao_homens_50_54` ↔ `populacao_6`: correlação 0.986
- `populacao_homens_50_54` ↔ `populacao_6_10`: correlação 0.987
- `populacao_homens_50_54` ↔ `populacao_6_17`: correlação 0.988
- `populacao_homens_50_54` ↔ `populacao_65_mais`: correlação 0.992
- `populacao_homens_50_54` ↔ `populacao`: correlação 0.996
- `populacao_homens_50_54` ↔ `populacao_urbana`: correlação 0.997
- `populacao_homens_50_54` ↔ `populacao_dom_pp`: correlação 0.996
- `populacao_homens_50_54` ↔ `populacao_dom_pp_exc_renda_nula`: correlação 0.997
- `populacao_homens_50_54` ↔ `pea`: correlação 0.996
- `populacao_homens_50_54` ↔ `pea_10_14`: correlação 0.943
- `populacao_homens_50_54` ↔ `pea_15_17`: correlação 0.964
- `populacao_homens_50_54` ↔ `pea_18_mais`: correlação 0.996
- `populacao_homens_50_54` ↔ `pia`: correlação 0.997
- `populacao_homens_50_54` ↔ `pia_10_14`: correlação 0.988
- `populacao_homens_50_54` ↔ `pia_15_17`: correlação 0.987
- `populacao_homens_50_54` ↔ `pia_18_mais`: correlação 0.998
- `populacao_homens_55_59` ↔ `populacao_homens_5_9`: correlação 0.982
- `populacao_homens_55_59` ↔ `populacao_homens_60_64`: correlação 0.999
- `populacao_homens_55_59` ↔ `populacao_homens_65_69`: correlação 0.998
- `populacao_homens_55_59` ↔ `populacao_homens_70_74`: correlação 0.996
- `populacao_homens_55_59` ↔ `populacao_homens_75_79`: correlação 0.993
- `populacao_homens_55_59` ↔ `populacao_homens`: correlação 0.994
- `populacao_homens_55_59` ↔ `populacao_homens_80_mais`: correlação 0.991
- `populacao_homens_55_59` ↔ `populacao_mulheres_0_4`: correlação 0.981
- `populacao_homens_55_59` ↔ `populacao_mulheres_10_14`: correlação 0.985
- `populacao_homens_55_59` ↔ `populacao_mulheres_15_19`: correlação 0.983
- `populacao_homens_55_59` ↔ `populacao_mulheres_20_24`: correlação 0.984
- `populacao_homens_55_59` ↔ `populacao_mulheres_25_29`: correlação 0.988
- `populacao_homens_55_59` ↔ `populacao_mulheres_30_34`: correlação 0.990
- `populacao_homens_55_59` ↔ `populacao_mulheres_35_39`: correlação 0.992
- `populacao_homens_55_59` ↔ `populacao_mulheres_40_44`: correlação 0.994
- `populacao_homens_55_59` ↔ `populacao_mulheres_45_49`: correlação 0.998
- `populacao_homens_55_59` ↔ `populacao_mulheres_50_54`: correlação 0.999
- `populacao_homens_55_59` ↔ `populacao_mulheres_55_59`: correlação 0.999
- `populacao_homens_55_59` ↔ `populacao_mulheres_5_9`: correlação 0.982
- `populacao_homens_55_59` ↔ `populacao_mulheres_60_64`: correlação 0.998
- `populacao_homens_55_59` ↔ `populacao_mulheres_65_69`: correlação 0.997
- `populacao_homens_55_59` ↔ `populacao_mulheres_70_74`: correlação 0.994
- `populacao_homens_55_59` ↔ `populacao_mulheres_75_79`: correlação 0.989
- `populacao_homens_55_59` ↔ `populacao_mulheres_80_mais`: correlação 0.985
- `populacao_homens_55_59` ↔ `populacao_mulheres`: correlação 0.995
- `populacao_homens_55_59` ↔ `populacao_1_menos`: correlação 0.981
- `populacao_homens_55_59` ↔ `populacao_11_14`: correlação 0.985
- `populacao_homens_55_59` ↔ `populacao_11_13`: correlação 0.985
- `populacao_homens_55_59` ↔ `populacao_12_14`: correlação 0.985
- `populacao_homens_55_59` ↔ `populacao_1_3`: correlação 0.980
- `populacao_homens_55_59` ↔ `populacao_15_mais`: correlação 0.996
- `populacao_homens_55_59` ↔ `populacao_15_17`: correlação 0.983
- `populacao_homens_55_59` ↔ `populacao_15_24`: correlação 0.985
- `populacao_homens_55_59` ↔ `populacao_16_18`: correlação 0.983
- `populacao_homens_55_59` ↔ `populacao_18_mais`: correlação 0.997
- `populacao_homens_55_59` ↔ `populacao_18_20`: correlação 0.986
- `populacao_homens_55_59` ↔ `populacao_18_24`: correlação 0.986
- `populacao_homens_55_59` ↔ `populacao_19_21`: correlação 0.987
- `populacao_homens_55_59` ↔ `populacao_25_mais`: correlação 0.998
- `populacao_homens_55_59` ↔ `populacao_4`: correlação 0.981
- `populacao_homens_55_59` ↔ `populacao_5`: correlação 0.982
- `populacao_homens_55_59` ↔ `populacao_6`: correlação 0.982
- `populacao_homens_55_59` ↔ `populacao_6_10`: correlação 0.983
- `populacao_homens_55_59` ↔ `populacao_6_17`: correlação 0.984
- `populacao_homens_55_59` ↔ `populacao_65_mais`: correlação 0.994
- `populacao_homens_55_59` ↔ `populacao`: correlação 0.994
- `populacao_homens_55_59` ↔ `populacao_urbana`: correlação 0.995
- `populacao_homens_55_59` ↔ `populacao_dom_pp`: correlação 0.994
- `populacao_homens_55_59` ↔ `populacao_dom_pp_exc_renda_nula`: correlação 0.994
- `populacao_homens_55_59` ↔ `pea`: correlação 0.994
- `populacao_homens_55_59` ↔ `pea_10_14`: correlação 0.938
- `populacao_homens_55_59` ↔ `pea_15_17`: correlação 0.959
- `populacao_homens_55_59` ↔ `pea_18_mais`: correlação 0.994
- `populacao_homens_55_59` ↔ `pia`: correlação 0.996
- `populacao_homens_55_59` ↔ `pia_10_14`: correlação 0.985
- `populacao_homens_55_59` ↔ `pia_15_17`: correlação 0.983
- `populacao_homens_55_59` ↔ `pia_18_mais`: correlação 0.997
- `populacao_homens_5_9` ↔ `populacao_homens_60_64`: correlação 0.979
- `populacao_homens_5_9` ↔ `populacao_homens_65_69`: correlação 0.976
- `populacao_homens_5_9` ↔ `populacao_homens_70_74`: correlação 0.971
- `populacao_homens_5_9` ↔ `populacao_homens_75_79`: correlação 0.961
- `populacao_homens_5_9` ↔ `populacao_homens`: correlação 0.997
- `populacao_homens_5_9` ↔ `populacao_homens_80_mais`: correlação 0.961
- `populacao_homens_5_9` ↔ `populacao_mulheres_0_4`: correlação 1.000
- `populacao_homens_5_9` ↔ `populacao_mulheres_10_14`: correlação 1.000
- `populacao_homens_5_9` ↔ `populacao_mulheres_15_19`: correlação 0.999
- `populacao_homens_5_9` ↔ `populacao_mulheres_20_24`: correlação 0.997
- `populacao_homens_5_9` ↔ `populacao_mulheres_25_29`: correlação 0.996
- `populacao_homens_5_9` ↔ `populacao_mulheres_30_34`: correlação 0.996
- `populacao_homens_5_9` ↔ `populacao_mulheres_35_39`: correlação 0.996
- `populacao_homens_5_9` ↔ `populacao_mulheres_40_44`: correlação 0.994
- `populacao_homens_5_9` ↔ `populacao_mulheres_45_49`: correlação 0.989
- `populacao_homens_5_9` ↔ `populacao_mulheres_50_54`: correlação 0.984
- `populacao_homens_5_9` ↔ `populacao_mulheres_55_59`: correlação 0.979
- `populacao_homens_5_9` ↔ `populacao_mulheres_5_9`: correlação 1.000
- `populacao_homens_5_9` ↔ `populacao_mulheres_60_64`: correlação 0.975
- `populacao_homens_5_9` ↔ `populacao_mulheres_65_69`: correlação 0.971
- `populacao_homens_5_9` ↔ `populacao_mulheres_70_74`: correlação 0.964
- `populacao_homens_5_9` ↔ `populacao_mulheres_75_79`: correlação 0.953
- `populacao_homens_5_9` ↔ `populacao_mulheres_80_mais`: correlação 0.948
- `populacao_homens_5_9` ↔ `populacao_mulheres`: correlação 0.995
- `populacao_homens_5_9` ↔ `populacao_1_menos`: correlação 1.000
- `populacao_homens_5_9` ↔ `populacao_11_14`: correlação 1.000
- `populacao_homens_5_9` ↔ `populacao_11_13`: correlação 1.000
- `populacao_homens_5_9` ↔ `populacao_12_14`: correlação 1.000
- `populacao_homens_5_9` ↔ `populacao_1_3`: correlação 1.000
- `populacao_homens_5_9` ↔ `populacao_15_mais`: correlação 0.994
- `populacao_homens_5_9` ↔ `populacao_15_17`: correlação 0.999
- `populacao_homens_5_9` ↔ `populacao_15_24`: correlação 0.998
- `populacao_homens_5_9` ↔ `populacao_16_18`: correlação 0.999
- `populacao_homens_5_9` ↔ `populacao_18_mais`: correlação 0.993
- `populacao_homens_5_9` ↔ `populacao_18_20`: correlação 0.998
- `populacao_homens_5_9` ↔ `populacao_18_24`: correlação 0.998
- `populacao_homens_5_9` ↔ `populacao_19_21`: correlação 0.998
- `populacao_homens_5_9` ↔ `populacao_25_mais`: correlação 0.991
- `populacao_homens_5_9` ↔ `populacao_4`: correlação 1.000
- `populacao_homens_5_9` ↔ `populacao_5`: correlação 1.000
- `populacao_homens_5_9` ↔ `populacao_6`: correlação 1.000
- `populacao_homens_5_9` ↔ `populacao_6_10`: correlação 1.000
- `populacao_homens_5_9` ↔ `populacao_6_17`: correlação 1.000
- `populacao_homens_5_9` ↔ `populacao_65_mais`: correlação 0.965
- `populacao_homens_5_9` ↔ `populacao`: correlação 0.996
- `populacao_homens_5_9` ↔ `populacao_urbana`: correlação 0.994
- `populacao_homens_5_9` ↔ `populacao_dom_pp`: correlação 0.996
- `populacao_homens_5_9` ↔ `populacao_dom_pp_exc_renda_nula`: correlação 0.996
- `populacao_homens_5_9` ↔ `pea`: correlação 0.993
- `populacao_homens_5_9` ↔ `pea_10_14`: correlação 0.974
- `populacao_homens_5_9` ↔ `pea_15_17`: correlação 0.980
- `populacao_homens_5_9` ↔ `pea_18_mais`: correlação 0.993
- `populacao_homens_5_9` ↔ `pia`: correlação 0.995
- `populacao_homens_5_9` ↔ `pia_10_14`: correlação 1.000
- `populacao_homens_5_9` ↔ `pia_15_17`: correlação 0.999
- `populacao_homens_5_9` ↔ `pia_18_mais`: correlação 0.993
- `populacao_homens_60_64` ↔ `populacao_homens_65_69`: correlação 1.000
- `populacao_homens_60_64` ↔ `populacao_homens_70_74`: correlação 0.998
- `populacao_homens_60_64` ↔ `populacao_homens_75_79`: correlação 0.995
- `populacao_homens_60_64` ↔ `populacao_homens`: correlação 0.992
- `populacao_homens_60_64` ↔ `populacao_homens_80_mais`: correlação 0.994
- `populacao_homens_60_64` ↔ `populacao_mulheres_0_4`: correlação 0.977
- `populacao_homens_60_64` ↔ `populacao_mulheres_10_14`: correlação 0.982
- `populacao_homens_60_64` ↔ `populacao_mulheres_15_19`: correlação 0.980
- `populacao_homens_60_64` ↔ `populacao_mulheres_20_24`: correlação 0.981
- `populacao_homens_60_64` ↔ `populacao_mulheres_25_29`: correlação 0.984
- `populacao_homens_60_64` ↔ `populacao_mulheres_30_34`: correlação 0.987
- `populacao_homens_60_64` ↔ `populacao_mulheres_35_39`: correlação 0.989
- `populacao_homens_60_64` ↔ `populacao_mulheres_40_44`: correlação 0.992
- `populacao_homens_60_64` ↔ `populacao_mulheres_45_49`: correlação 0.996
- `populacao_homens_60_64` ↔ `populacao_mulheres_50_54`: correlação 0.999
- `populacao_homens_60_64` ↔ `populacao_mulheres_55_59`: correlação 1.000
- `populacao_homens_60_64` ↔ `populacao_mulheres_5_9`: correlação 0.979
- `populacao_homens_60_64` ↔ `populacao_mulheres_60_64`: correlação 0.999
- `populacao_homens_60_64` ↔ `populacao_mulheres_65_69`: correlação 0.998
- `populacao_homens_60_64` ↔ `populacao_mulheres_70_74`: correlação 0.996
- `populacao_homens_60_64` ↔ `populacao_mulheres_75_79`: correlação 0.992
- `populacao_homens_60_64` ↔ `populacao_mulheres_80_mais`: correlação 0.989
- `populacao_homens_60_64` ↔ `populacao_mulheres`: correlação 0.993
- `populacao_homens_60_64` ↔ `populacao_1_menos`: correlação 0.977
- `populacao_homens_60_64` ↔ `populacao_11_14`: correlação 0.982
- `populacao_homens_60_64` ↔ `populacao_11_13`: correlação 0.982
- `populacao_homens_60_64` ↔ `populacao_12_14`: correlação 0.982
- `populacao_homens_60_64` ↔ `populacao_1_3`: correlação 0.977
- `populacao_homens_60_64` ↔ `populacao_15_mais`: correlação 0.994
- `populacao_homens_60_64` ↔ `populacao_15_17`: correlação 0.980
- `populacao_homens_60_64` ↔ `populacao_15_24`: correlação 0.982
- `populacao_homens_60_64` ↔ `populacao_16_18`: correlação 0.980
- `populacao_homens_60_64` ↔ `populacao_18_mais`: correlação 0.995
- `populacao_homens_60_64` ↔ `populacao_18_20`: correlação 0.983
- `populacao_homens_60_64` ↔ `populacao_18_24`: correlação 0.983
- `populacao_homens_60_64` ↔ `populacao_19_21`: correlação 0.984
- `populacao_homens_60_64` ↔ `populacao_25_mais`: correlação 0.996
- `populacao_homens_60_64` ↔ `populacao_4`: correlação 0.977
- `populacao_homens_60_64` ↔ `populacao_5`: correlação 0.978
- `populacao_homens_60_64` ↔ `populacao_6`: correlação 0.979
- `populacao_homens_60_64` ↔ `populacao_6_10`: correlação 0.980
- `populacao_homens_60_64` ↔ `populacao_6_17`: correlação 0.981
- `populacao_homens_60_64` ↔ `populacao_65_mais`: correlação 0.997
- `populacao_homens_60_64` ↔ `populacao`: correlação 0.992
- `populacao_homens_60_64` ↔ `populacao_urbana`: correlação 0.993
- `populacao_homens_60_64` ↔ `populacao_dom_pp`: correlação 0.992
- `populacao_homens_60_64` ↔ `populacao_dom_pp_exc_renda_nula`: correlação 0.992
- `populacao_homens_60_64` ↔ `pea`: correlação 0.991
- `populacao_homens_60_64` ↔ `pea_10_14`: correlação 0.932
- `populacao_homens_60_64` ↔ `pea_15_17`: correlação 0.953
- `populacao_homens_60_64` ↔ `pea_18_mais`: correlação 0.992
- `populacao_homens_60_64` ↔ `pia`: correlação 0.994
- `populacao_homens_60_64` ↔ `pia_10_14`: correlação 0.982
- `populacao_homens_60_64` ↔ `pia_15_17`: correlação 0.980
- `populacao_homens_60_64` ↔ `pia_18_mais`: correlação 0.995
- `populacao_homens_65_69` ↔ `populacao_homens_70_74`: correlação 0.999
- `populacao_homens_65_69` ↔ `populacao_homens_75_79`: correlação 0.997
- `populacao_homens_65_69` ↔ `populacao_homens`: correlação 0.989
- `populacao_homens_65_69` ↔ `populacao_homens_80_mais`: correlação 0.996
- `populacao_homens_65_69` ↔ `populacao_mulheres_0_4`: correlação 0.974
- `populacao_homens_65_69` ↔ `populacao_mulheres_10_14`: correlação 0.979
- `populacao_homens_65_69` ↔ `populacao_mulheres_15_19`: correlação 0.977
- `populacao_homens_65_69` ↔ `populacao_mulheres_20_24`: correlação 0.978
- `populacao_homens_65_69` ↔ `populacao_mulheres_25_29`: correlação 0.981
- `populacao_homens_65_69` ↔ `populacao_mulheres_30_34`: correlação 0.983
- `populacao_homens_65_69` ↔ `populacao_mulheres_35_39`: correlação 0.986
- `populacao_homens_65_69` ↔ `populacao_mulheres_40_44`: correlação 0.989
- `populacao_homens_65_69` ↔ `populacao_mulheres_45_49`: correlação 0.994
- `populacao_homens_65_69` ↔ `populacao_mulheres_50_54`: correlação 0.997
- `populacao_homens_65_69` ↔ `populacao_mulheres_55_59`: correlação 0.999
- `populacao_homens_65_69` ↔ `populacao_mulheres_5_9`: correlação 0.976
- `populacao_homens_65_69` ↔ `populacao_mulheres_60_64`: correlação 0.999
- `populacao_homens_65_69` ↔ `populacao_mulheres_65_69`: correlação 0.999
- `populacao_homens_65_69` ↔ `populacao_mulheres_70_74`: correlação 0.997
- `populacao_homens_65_69` ↔ `populacao_mulheres_75_79`: correlação 0.994
- `populacao_homens_65_69` ↔ `populacao_mulheres_80_mais`: correlação 0.991
- `populacao_homens_65_69` ↔ `populacao_mulheres`: correlação 0.990
- `populacao_homens_65_69` ↔ `populacao_1_menos`: correlação 0.974
- `populacao_homens_65_69` ↔ `populacao_11_14`: correlação 0.979
- `populacao_homens_65_69` ↔ `populacao_11_13`: correlação 0.979
- `populacao_homens_65_69` ↔ `populacao_12_14`: correlação 0.979
- `populacao_homens_65_69` ↔ `populacao_1_3`: correlação 0.973
- `populacao_homens_65_69` ↔ `populacao_15_mais`: correlação 0.992
- `populacao_homens_65_69` ↔ `populacao_15_17`: correlação 0.977
- `populacao_homens_65_69` ↔ `populacao_15_24`: correlação 0.979
- `populacao_homens_65_69` ↔ `populacao_16_18`: correlação 0.977
- `populacao_homens_65_69` ↔ `populacao_18_mais`: correlação 0.993
- `populacao_homens_65_69` ↔ `populacao_18_20`: correlação 0.980
- `populacao_homens_65_69` ↔ `populacao_18_24`: correlação 0.980
- `populacao_homens_65_69` ↔ `populacao_19_21`: correlação 0.981
- `populacao_homens_65_69` ↔ `populacao_25_mais`: correlação 0.994
- `populacao_homens_65_69` ↔ `populacao_4`: correlação 0.974
- `populacao_homens_65_69` ↔ `populacao_5`: correlação 0.975
- `populacao_homens_65_69` ↔ `populacao_6`: correlação 0.976
- `populacao_homens_65_69` ↔ `populacao_6_10`: correlação 0.977
- `populacao_homens_65_69` ↔ `populacao_6_17`: correlação 0.978
- `populacao_homens_65_69` ↔ `populacao_65_mais`: correlação 0.998
- `populacao_homens_65_69` ↔ `populacao`: correlação 0.990
- `populacao_homens_65_69` ↔ `populacao_urbana`: correlação 0.990
- `populacao_homens_65_69` ↔ `populacao_dom_pp`: correlação 0.990
- `populacao_homens_65_69` ↔ `populacao_dom_pp_exc_renda_nula`: correlação 0.990
- `populacao_homens_65_69` ↔ `pea`: correlação 0.989
- `populacao_homens_65_69` ↔ `pea_10_14`: correlação 0.929
- `populacao_homens_65_69` ↔ `pea_15_17`: correlação 0.948
- `populacao_homens_65_69` ↔ `pea_18_mais`: correlação 0.989
- `populacao_homens_65_69` ↔ `pia`: correlação 0.991
- `populacao_homens_65_69` ↔ `pia_10_14`: correlação 0.979
- `populacao_homens_65_69` ↔ `pia_15_17`: correlação 0.977
- `populacao_homens_65_69` ↔ `pia_18_mais`: correlação 0.993
- `populacao_homens_70_74` ↔ `populacao_homens_75_79`: correlação 0.999
- `populacao_homens_70_74` ↔ `populacao_homens`: correlação 0.985
- `populacao_homens_70_74` ↔ `populacao_homens_80_mais`: correlação 0.998
- `populacao_homens_70_74` ↔ `populacao_mulheres_0_4`: correlação 0.968
- `populacao_homens_70_74` ↔ `populacao_mulheres_10_14`: correlação 0.974
- `populacao_homens_70_74` ↔ `populacao_mulheres_15_19`: correlação 0.971
- `populacao_homens_70_74` ↔ `populacao_mulheres_20_24`: correlação 0.973
- `populacao_homens_70_74` ↔ `populacao_mulheres_25_29`: correlação 0.976
- `populacao_homens_70_74` ↔ `populacao_mulheres_30_34`: correlação 0.979
- `populacao_homens_70_74` ↔ `populacao_mulheres_35_39`: correlação 0.982
- `populacao_homens_70_74` ↔ `populacao_mulheres_40_44`: correlação 0.985
- `populacao_homens_70_74` ↔ `populacao_mulheres_45_49`: correlação 0.991
- `populacao_homens_70_74` ↔ `populacao_mulheres_50_54`: correlação 0.995
- `populacao_homens_70_74` ↔ `populacao_mulheres_55_59`: correlação 0.998
- `populacao_homens_70_74` ↔ `populacao_mulheres_5_9`: correlação 0.971
- `populacao_homens_70_74` ↔ `populacao_mulheres_60_64`: correlação 0.999
- `populacao_homens_70_74` ↔ `populacao_mulheres_65_69`: correlação 0.999
- `populacao_homens_70_74` ↔ `populacao_mulheres_70_74`: correlação 0.998
- `populacao_homens_70_74` ↔ `populacao_mulheres_75_79`: correlação 0.996
- `populacao_homens_70_74` ↔ `populacao_mulheres_80_mais`: correlação 0.994
- `populacao_homens_70_74` ↔ `populacao_mulheres`: correlação 0.987
- `populacao_homens_70_74` ↔ `populacao_1_menos`: correlação 0.968
- `populacao_homens_70_74` ↔ `populacao_11_14`: correlação 0.974
- `populacao_homens_70_74` ↔ `populacao_11_13`: correlação 0.974
- `populacao_homens_70_74` ↔ `populacao_12_14`: correlação 0.974
- `populacao_homens_70_74` ↔ `populacao_1_3`: correlação 0.968
- `populacao_homens_70_74` ↔ `populacao_15_mais`: correlação 0.989
- `populacao_homens_70_74` ↔ `populacao_15_17`: correlação 0.972
- `populacao_homens_70_74` ↔ `populacao_15_24`: correlação 0.974
- `populacao_homens_70_74` ↔ `populacao_16_18`: correlação 0.972
- `populacao_homens_70_74` ↔ `populacao_18_mais`: correlação 0.989
- `populacao_homens_70_74` ↔ `populacao_18_20`: correlação 0.975
- `populacao_homens_70_74` ↔ `populacao_18_24`: correlação 0.974
- `populacao_homens_70_74` ↔ `populacao_19_21`: correlação 0.976
- `populacao_homens_70_74` ↔ `populacao_25_mais`: correlação 0.991
- `populacao_homens_70_74` ↔ `populacao_4`: correlação 0.969
- `populacao_homens_70_74` ↔ `populacao_5`: correlação 0.970
- `populacao_homens_70_74` ↔ `populacao_6`: correlação 0.970
- `populacao_homens_70_74` ↔ `populacao_6_10`: correlação 0.972
- `populacao_homens_70_74` ↔ `populacao_6_17`: correlação 0.973
- `populacao_homens_70_74` ↔ `populacao_65_mais`: correlação 0.999
- `populacao_homens_70_74` ↔ `populacao`: correlação 0.986
- `populacao_homens_70_74` ↔ `populacao_urbana`: correlação 0.986
- `populacao_homens_70_74` ↔ `populacao_dom_pp`: correlação 0.986
- `populacao_homens_70_74` ↔ `populacao_dom_pp_exc_renda_nula`: correlação 0.986
- `populacao_homens_70_74` ↔ `pea`: correlação 0.984
- `populacao_homens_70_74` ↔ `pea_10_14`: correlação 0.920
- `populacao_homens_70_74` ↔ `pea_15_17`: correlação 0.939
- `populacao_homens_70_74` ↔ `pea_18_mais`: correlação 0.985
- `populacao_homens_70_74` ↔ `pia`: correlação 0.988
- `populacao_homens_70_74` ↔ `pia_10_14`: correlação 0.974
- `populacao_homens_70_74` ↔ `pia_15_17`: correlação 0.972
- `populacao_homens_70_74` ↔ `pia_18_mais`: correlação 0.989
- `populacao_homens_75_79` ↔ `populacao_homens`: correlação 0.978
- `populacao_homens_75_79` ↔ `populacao_homens_80_mais`: correlação 0.999
- `populacao_homens_75_79` ↔ `populacao_mulheres_0_4`: correlação 0.958
- `populacao_homens_75_79` ↔ `populacao_mulheres_10_14`: correlação 0.964
- `populacao_homens_75_79` ↔ `populacao_mulheres_15_19`: correlação 0.961
- `populacao_homens_75_79` ↔ `populacao_mulheres_20_24`: correlação 0.963
- `populacao_homens_75_79` ↔ `populacao_mulheres_25_29`: correlação 0.967
- `populacao_homens_75_79` ↔ `populacao_mulheres_30_34`: correlação 0.970
- `populacao_homens_75_79` ↔ `populacao_mulheres_35_39`: correlação 0.974
- `populacao_homens_75_79` ↔ `populacao_mulheres_40_44`: correlação 0.977
- `populacao_homens_75_79` ↔ `populacao_mulheres_45_49`: correlação 0.985
- `populacao_homens_75_79` ↔ `populacao_mulheres_50_54`: correlação 0.991
- `populacao_homens_75_79` ↔ `populacao_mulheres_55_59`: correlação 0.995
- `populacao_homens_75_79` ↔ `populacao_mulheres_5_9`: correlação 0.961
- `populacao_homens_75_79` ↔ `populacao_mulheres_60_64`: correlação 0.997
- `populacao_homens_75_79` ↔ `populacao_mulheres_65_69`: correlação 0.998
- `populacao_homens_75_79` ↔ `populacao_mulheres_70_74`: correlação 0.999
- `populacao_homens_75_79` ↔ `populacao_mulheres_75_79`: correlação 0.998
- `populacao_homens_75_79` ↔ `populacao_mulheres_80_mais`: correlação 0.996
- `populacao_homens_75_79` ↔ `populacao_mulheres`: correlação 0.980
- `populacao_homens_75_79` ↔ `populacao_1_menos`: correlação 0.958
- `populacao_homens_75_79` ↔ `populacao_11_14`: correlação 0.965
- `populacao_homens_75_79` ↔ `populacao_11_13`: correlação 0.965
- `populacao_homens_75_79` ↔ `populacao_12_14`: correlação 0.965
- `populacao_homens_75_79` ↔ `populacao_1_3`: correlação 0.958
- `populacao_homens_75_79` ↔ `populacao_15_mais`: correlação 0.982
- `populacao_homens_75_79` ↔ `populacao_15_17`: correlação 0.963
- `populacao_homens_75_79` ↔ `populacao_15_24`: correlação 0.965
- `populacao_homens_75_79` ↔ `populacao_16_18`: correlação 0.962
- `populacao_homens_75_79` ↔ `populacao_18_mais`: correlação 0.983
- `populacao_homens_75_79` ↔ `populacao_18_20`: correlação 0.966
- `populacao_homens_75_79` ↔ `populacao_18_24`: correlação 0.965
- `populacao_homens_75_79` ↔ `populacao_19_21`: correlação 0.967
- `populacao_homens_75_79` ↔ `populacao_25_mais`: correlação 0.986
- `populacao_homens_75_79` ↔ `populacao_4`: correlação 0.959
- `populacao_homens_75_79` ↔ `populacao_5`: correlação 0.960
- `populacao_homens_75_79` ↔ `populacao_6`: correlação 0.961
- `populacao_homens_75_79` ↔ `populacao_6_10`: correlação 0.962
- `populacao_homens_75_79` ↔ `populacao_6_17`: correlação 0.963
- `populacao_homens_75_79` ↔ `populacao_65_mais`: correlação 0.999
- `populacao_homens_75_79` ↔ `populacao`: correlação 0.979
- `populacao_homens_75_79` ↔ `populacao_urbana`: correlação 0.979
- `populacao_homens_75_79` ↔ `populacao_dom_pp`: correlação 0.979
- `populacao_homens_75_79` ↔ `populacao_dom_pp_exc_renda_nula`: correlação 0.979
- `populacao_homens_75_79` ↔ `pea`: correlação 0.977
- `populacao_homens_75_79` ↔ `pea_10_14`: correlação 0.908
- `populacao_homens_75_79` ↔ `pea_15_17`: correlação 0.927
- `populacao_homens_75_79` ↔ `pea_18_mais`: correlação 0.978
- `populacao_homens_75_79` ↔ `pia`: correlação 0.981
- `populacao_homens_75_79` ↔ `pia_10_14`: correlação 0.965
- `populacao_homens_75_79` ↔ `pia_15_17`: correlação 0.963
- `populacao_homens_75_79` ↔ `pia_18_mais`: correlação 0.983
- `populacao_homens` ↔ `populacao_homens_80_mais`: correlação 0.977
- `populacao_homens` ↔ `populacao_mulheres_0_4`: correlação 0.996
- `populacao_homens` ↔ `populacao_mulheres_10_14`: correlação 0.997
- `populacao_homens` ↔ `populacao_mulheres_15_19`: correlação 0.997
- `populacao_homens` ↔ `populacao_mulheres_20_24`: correlação 0.997
- `populacao_homens` ↔ `populacao_mulheres_25_29`: correlação 0.998
- `populacao_homens` ↔ `populacao_mulheres_30_34`: correlação 0.999
- `populacao_homens` ↔ `populacao_mulheres_35_39`: correlação 0.999
- `populacao_homens` ↔ `populacao_mulheres_40_44`: correlação 0.999
- `populacao_homens` ↔ `populacao_mulheres_45_49`: correlação 0.998
- `populacao_homens` ↔ `populacao_mulheres_50_54`: correlação 0.995
- `populacao_homens` ↔ `populacao_mulheres_55_59`: correlação 0.992
- `populacao_homens` ↔ `populacao_mulheres_5_9`: correlação 0.997
- `populacao_homens` ↔ `populacao_mulheres_60_64`: correlação 0.989
- `populacao_homens` ↔ `populacao_mulheres_65_69`: correlação 0.986
- `populacao_homens` ↔ `populacao_mulheres_70_74`: correlação 0.980
- `populacao_homens` ↔ `populacao_mulheres_75_79`: correlação 0.971
- `populacao_homens` ↔ `populacao_mulheres_80_mais`: correlação 0.967
- `populacao_homens` ↔ `populacao_mulheres`: correlação 1.000
- `populacao_homens` ↔ `populacao_1_menos`: correlação 0.996
- `populacao_homens` ↔ `populacao_11_14`: correlação 0.998
- `populacao_homens` ↔ `populacao_11_13`: correlação 0.998
- `populacao_homens` ↔ `populacao_12_14`: correlação 0.998
- `populacao_homens` ↔ `populacao_1_3`: correlação 0.996
- `populacao_homens` ↔ `populacao_15_mais`: correlação 0.999
- `populacao_homens` ↔ `populacao_15_17`: correlação 0.997
- `populacao_homens` ↔ `populacao_15_24`: correlação 0.998
- `populacao_homens` ↔ `populacao_16_18`: correlação 0.997
- `populacao_homens` ↔ `populacao_18_mais`: correlação 0.999
- `populacao_homens` ↔ `populacao_18_20`: correlação 0.998
- `populacao_homens` ↔ `populacao_18_24`: correlação 0.998
- `populacao_homens` ↔ `populacao_19_21`: correlação 0.998
- `populacao_homens` ↔ `populacao_25_mais`: correlação 0.999
- `populacao_homens` ↔ `populacao_4`: correlação 0.996
- `populacao_homens` ↔ `populacao_5`: correlação 0.996
- `populacao_homens` ↔ `populacao_6`: correlação 0.996
- `populacao_homens` ↔ `populacao_6_10`: correlação 0.997
- `populacao_homens` ↔ `populacao_6_17`: correlação 0.997
- `populacao_homens` ↔ `populacao_65_mais`: correlação 0.981
- `populacao_homens` ↔ `populacao`: correlação 1.000
- `populacao_homens` ↔ `populacao_urbana`: correlação 0.999
- `populacao_homens` ↔ `populacao_dom_pp`: correlação 1.000
- `populacao_homens` ↔ `populacao_dom_pp_exc_renda_nula`: correlação 1.000
- `populacao_homens` ↔ `pea`: correlação 0.999
- `populacao_homens` ↔ `pea_10_14`: correlação 0.963
- `populacao_homens` ↔ `pea_15_17`: correlação 0.977
- `populacao_homens` ↔ `pea_18_mais`: correlação 0.999
- `populacao_homens` ↔ `pia`: correlação 1.000
- `populacao_homens` ↔ `pia_10_14`: correlação 0.998
- `populacao_homens` ↔ `pia_15_17`: correlação 0.997
- `populacao_homens` ↔ `pia_18_mais`: correlação 0.999
- `populacao_homens_80_mais` ↔ `populacao_mulheres_0_4`: correlação 0.958
- `populacao_homens_80_mais` ↔ `populacao_mulheres_10_14`: correlação 0.964
- `populacao_homens_80_mais` ↔ `populacao_mulheres_15_19`: correlação 0.961
- `populacao_homens_80_mais` ↔ `populacao_mulheres_20_24`: correlação 0.964
- `populacao_homens_80_mais` ↔ `populacao_mulheres_25_29`: correlação 0.967
- `populacao_homens_80_mais` ↔ `populacao_mulheres_30_34`: correlação 0.970
- `populacao_homens_80_mais` ↔ `populacao_mulheres_35_39`: correlação 0.973
- `populacao_homens_80_mais` ↔ `populacao_mulheres_40_44`: correlação 0.977
- `populacao_homens_80_mais` ↔ `populacao_mulheres_45_49`: correlação 0.984
- `populacao_homens_80_mais` ↔ `populacao_mulheres_50_54`: correlação 0.990
- `populacao_homens_80_mais` ↔ `populacao_mulheres_55_59`: correlação 0.993
- `populacao_homens_80_mais` ↔ `populacao_mulheres_5_9`: correlação 0.961
- `populacao_homens_80_mais` ↔ `populacao_mulheres_60_64`: correlação 0.996
- `populacao_homens_80_mais` ↔ `populacao_mulheres_65_69`: correlação 0.997
- `populacao_homens_80_mais` ↔ `populacao_mulheres_70_74`: correlação 0.998
- `populacao_homens_80_mais` ↔ `populacao_mulheres_75_79`: correlação 0.998
- `populacao_homens_80_mais` ↔ `populacao_mulheres_80_mais`: correlação 0.997
- `populacao_homens_80_mais` ↔ `populacao_mulheres`: correlação 0.979
- `populacao_homens_80_mais` ↔ `populacao_1_menos`: correlação 0.958
- `populacao_homens_80_mais` ↔ `populacao_11_14`: correlação 0.964
- `populacao_homens_80_mais` ↔ `populacao_11_13`: correlação 0.965
- `populacao_homens_80_mais` ↔ `populacao_12_14`: correlação 0.964
- `populacao_homens_80_mais` ↔ `populacao_1_3`: correlação 0.958
- `populacao_homens_80_mais` ↔ `populacao_15_mais`: correlação 0.981
- `populacao_homens_80_mais` ↔ `populacao_15_17`: correlação 0.962
- `populacao_homens_80_mais` ↔ `populacao_15_24`: correlação 0.965
- `populacao_homens_80_mais` ↔ `populacao_16_18`: correlação 0.962
- `populacao_homens_80_mais` ↔ `populacao_18_mais`: correlação 0.982
- `populacao_homens_80_mais` ↔ `populacao_18_20`: correlação 0.965
- `populacao_homens_80_mais` ↔ `populacao_18_24`: correlação 0.965
- `populacao_homens_80_mais` ↔ `populacao_19_21`: correlação 0.967
- `populacao_homens_80_mais` ↔ `populacao_25_mais`: correlação 0.985
- `populacao_homens_80_mais` ↔ `populacao_4`: correlação 0.959
- `populacao_homens_80_mais` ↔ `populacao_5`: correlação 0.960
- `populacao_homens_80_mais` ↔ `populacao_6`: correlação 0.960
- `populacao_homens_80_mais` ↔ `populacao_6_10`: correlação 0.962
- `populacao_homens_80_mais` ↔ `populacao_6_17`: correlação 0.963
- `populacao_homens_80_mais` ↔ `populacao_65_mais`: correlação 0.999
- `populacao_homens_80_mais` ↔ `populacao`: correlação 0.978
- `populacao_homens_80_mais` ↔ `populacao_urbana`: correlação 0.978
- `populacao_homens_80_mais` ↔ `populacao_dom_pp`: correlação 0.978
- `populacao_homens_80_mais` ↔ `populacao_dom_pp_exc_renda_nula`: correlação 0.978
- `populacao_homens_80_mais` ↔ `pea`: correlação 0.976
- `populacao_homens_80_mais` ↔ `pea_10_14`: correlação 0.910
- `populacao_homens_80_mais` ↔ `pea_15_17`: correlação 0.925
- `populacao_homens_80_mais` ↔ `pea_18_mais`: correlação 0.977
- `populacao_homens_80_mais` ↔ `pia`: correlação 0.980
- `populacao_homens_80_mais` ↔ `pia_10_14`: correlação 0.964
- `populacao_homens_80_mais` ↔ `pia_15_17`: correlação 0.962
- `populacao_homens_80_mais` ↔ `pia_18_mais`: correlação 0.982
- `populacao_mulheres_0_4` ↔ `populacao_mulheres_10_14`: correlação 0.999
- `populacao_mulheres_0_4` ↔ `populacao_mulheres_15_19`: correlação 0.998
- `populacao_mulheres_0_4` ↔ `populacao_mulheres_20_24`: correlação 0.997
- `populacao_mulheres_0_4` ↔ `populacao_mulheres_25_29`: correlação 0.996
- `populacao_mulheres_0_4` ↔ `populacao_mulheres_30_34`: correlação 0.995
- `populacao_mulheres_0_4` ↔ `populacao_mulheres_35_39`: correlação 0.995
- `populacao_mulheres_0_4` ↔ `populacao_mulheres_40_44`: correlação 0.993
- `populacao_mulheres_0_4` ↔ `populacao_mulheres_45_49`: correlação 0.988
- `populacao_mulheres_0_4` ↔ `populacao_mulheres_50_54`: correlação 0.982
- `populacao_mulheres_0_4` ↔ `populacao_mulheres_55_59`: correlação 0.977
- `populacao_mulheres_0_4` ↔ `populacao_mulheres_5_9`: correlação 1.000
- `populacao_mulheres_0_4` ↔ `populacao_mulheres_60_64`: correlação 0.973
- `populacao_mulheres_0_4` ↔ `populacao_mulheres_65_69`: correlação 0.968
- `populacao_mulheres_0_4` ↔ `populacao_mulheres_70_74`: correlação 0.961
- `populacao_mulheres_0_4` ↔ `populacao_mulheres_75_79`: correlação 0.950
- `populacao_mulheres_0_4` ↔ `populacao_mulheres_80_mais`: correlação 0.945
- `populacao_mulheres_0_4` ↔ `populacao_mulheres`: correlação 0.994
- `populacao_mulheres_0_4` ↔ `populacao_1_menos`: correlação 1.000
- `populacao_mulheres_0_4` ↔ `populacao_11_14`: correlação 0.999
- `populacao_mulheres_0_4` ↔ `populacao_11_13`: correlação 0.999
- `populacao_mulheres_0_4` ↔ `populacao_12_14`: correlação 0.999
- `populacao_mulheres_0_4` ↔ `populacao_1_3`: correlação 1.000
- `populacao_mulheres_0_4` ↔ `populacao_15_mais`: correlação 0.993
- `populacao_mulheres_0_4` ↔ `populacao_15_17`: correlação 0.999
- `populacao_mulheres_0_4` ↔ `populacao_15_24`: correlação 0.998
- `populacao_mulheres_0_4` ↔ `populacao_16_18`: correlação 0.998
- `populacao_mulheres_0_4` ↔ `populacao_18_mais`: correlação 0.992
- `populacao_mulheres_0_4` ↔ `populacao_18_20`: correlação 0.998
- `populacao_mulheres_0_4` ↔ `populacao_18_24`: correlação 0.998
- `populacao_mulheres_0_4` ↔ `populacao_19_21`: correlação 0.998
- `populacao_mulheres_0_4` ↔ `populacao_25_mais`: correlação 0.990
- `populacao_mulheres_0_4` ↔ `populacao_4`: correlação 1.000
- `populacao_mulheres_0_4` ↔ `populacao_5`: correlação 1.000
- `populacao_mulheres_0_4` ↔ `populacao_6`: correlação 1.000
- `populacao_mulheres_0_4` ↔ `populacao_6_10`: correlação 1.000
- `populacao_mulheres_0_4` ↔ `populacao_6_17`: correlação 0.999
- `populacao_mulheres_0_4` ↔ `populacao_65_mais`: correlação 0.962
- `populacao_mulheres_0_4` ↔ `populacao`: correlação 0.995
- `populacao_mulheres_0_4` ↔ `populacao_urbana`: correlação 0.993
- `populacao_mulheres_0_4` ↔ `populacao_dom_pp`: correlação 0.995
- `populacao_mulheres_0_4` ↔ `populacao_dom_pp_exc_renda_nula`: correlação 0.995
- `populacao_mulheres_0_4` ↔ `pea`: correlação 0.993
- `populacao_mulheres_0_4` ↔ `pea_10_14`: correlação 0.974
- `populacao_mulheres_0_4` ↔ `pea_15_17`: correlação 0.981
- `populacao_mulheres_0_4` ↔ `pea_18_mais`: correlação 0.992
- `populacao_mulheres_0_4` ↔ `pia`: correlação 0.994
- `populacao_mulheres_0_4` ↔ `pia_10_14`: correlação 0.999
- `populacao_mulheres_0_4` ↔ `pia_15_17`: correlação 0.999
- `populacao_mulheres_0_4` ↔ `pia_18_mais`: correlação 0.992
- `populacao_mulheres_10_14` ↔ `populacao_mulheres_15_19`: correlação 0.999
- `populacao_mulheres_10_14` ↔ `populacao_mulheres_20_24`: correlação 0.998
- `populacao_mulheres_10_14` ↔ `populacao_mulheres_25_29`: correlação 0.997
- `populacao_mulheres_10_14` ↔ `populacao_mulheres_30_34`: correlação 0.996
- `populacao_mulheres_10_14` ↔ `populacao_mulheres_35_39`: correlação 0.996
- `populacao_mulheres_10_14` ↔ `populacao_mulheres_40_44`: correlação 0.995
- `populacao_mulheres_10_14` ↔ `populacao_mulheres_45_49`: correlação 0.991
- `populacao_mulheres_10_14` ↔ `populacao_mulheres_50_54`: correlação 0.986
- `populacao_mulheres_10_14` ↔ `populacao_mulheres_55_59`: correlação 0.982
- `populacao_mulheres_10_14` ↔ `populacao_mulheres_5_9`: correlação 1.000
- `populacao_mulheres_10_14` ↔ `populacao_mulheres_60_64`: correlação 0.978
- `populacao_mulheres_10_14` ↔ `populacao_mulheres_65_69`: correlação 0.974
- `populacao_mulheres_10_14` ↔ `populacao_mulheres_70_74`: correlação 0.967
- `populacao_mulheres_10_14` ↔ `populacao_mulheres_75_79`: correlação 0.957
- `populacao_mulheres_10_14` ↔ `populacao_mulheres_80_mais`: correlação 0.952
- `populacao_mulheres_10_14` ↔ `populacao_mulheres`: correlação 0.996
- `populacao_mulheres_10_14` ↔ `populacao_1_menos`: correlação 0.999
- `populacao_mulheres_10_14` ↔ `populacao_11_14`: correlação 1.000
- `populacao_mulheres_10_14` ↔ `populacao_11_13`: correlação 1.000
- `populacao_mulheres_10_14` ↔ `populacao_12_14`: correlação 1.000
- `populacao_mulheres_10_14` ↔ `populacao_1_3`: correlação 0.999
- `populacao_mulheres_10_14` ↔ `populacao_15_mais`: correlação 0.995
- `populacao_mulheres_10_14` ↔ `populacao_15_17`: correlação 0.999
- `populacao_mulheres_10_14` ↔ `populacao_15_24`: correlação 0.999
- `populacao_mulheres_10_14` ↔ `populacao_16_18`: correlação 0.999
- `populacao_mulheres_10_14` ↔ `populacao_18_mais`: correlação 0.994
- `populacao_mulheres_10_14` ↔ `populacao_18_20`: correlação 0.999
- `populacao_mulheres_10_14` ↔ `populacao_18_24`: correlação 0.998
- `populacao_mulheres_10_14` ↔ `populacao_19_21`: correlação 0.998
- `populacao_mulheres_10_14` ↔ `populacao_25_mais`: correlação 0.993
- `populacao_mulheres_10_14` ↔ `populacao_4`: correlação 0.999
- `populacao_mulheres_10_14` ↔ `populacao_5`: correlação 0.999
- `populacao_mulheres_10_14` ↔ `populacao_6`: correlação 1.000
- `populacao_mulheres_10_14` ↔ `populacao_6_10`: correlação 1.000
- `populacao_mulheres_10_14` ↔ `populacao_6_17`: correlação 1.000
- `populacao_mulheres_10_14` ↔ `populacao_65_mais`: correlação 0.968
- `populacao_mulheres_10_14` ↔ `populacao`: correlação 0.997
- `populacao_mulheres_10_14` ↔ `populacao_urbana`: correlação 0.996
- `populacao_mulheres_10_14` ↔ `populacao_dom_pp`: correlação 0.997
- `populacao_mulheres_10_14` ↔ `populacao_dom_pp_exc_renda_nula`: correlação 0.997
- `populacao_mulheres_10_14` ↔ `pea`: correlação 0.994
- `populacao_mulheres_10_14` ↔ `pea_10_14`: correlação 0.971
- `populacao_mulheres_10_14` ↔ `pea_15_17`: correlação 0.979
- `populacao_mulheres_10_14` ↔ `pea_18_mais`: correlação 0.994
- `populacao_mulheres_10_14` ↔ `pia`: correlação 0.996
- `populacao_mulheres_10_14` ↔ `pia_10_14`: correlação 1.000
- `populacao_mulheres_10_14` ↔ `pia_15_17`: correlação 0.999
- `populacao_mulheres_10_14` ↔ `pia_18_mais`: correlação 0.994
- `populacao_mulheres_15_19` ↔ `populacao_mulheres_20_24`: correlação 0.999
- `populacao_mulheres_15_19` ↔ `populacao_mulheres_25_29`: correlação 0.997
- `populacao_mulheres_15_19` ↔ `populacao_mulheres_30_34`: correlação 0.996
- `populacao_mulheres_15_19` ↔ `populacao_mulheres_35_39`: correlação 0.996
- `populacao_mulheres_15_19` ↔ `populacao_mulheres_40_44`: correlação 0.995
- `populacao_mulheres_15_19` ↔ `populacao_mulheres_45_49`: correlação 0.991
- `populacao_mulheres_15_19` ↔ `populacao_mulheres_50_54`: correlação 0.985
- `populacao_mulheres_15_19` ↔ `populacao_mulheres_55_59`: correlação 0.980
- `populacao_mulheres_15_19` ↔ `populacao_mulheres_5_9`: correlação 0.999
- `populacao_mulheres_15_19` ↔ `populacao_mulheres_60_64`: correlação 0.976
- `populacao_mulheres_15_19` ↔ `populacao_mulheres_65_69`: correlação 0.972
- `populacao_mulheres_15_19` ↔ `populacao_mulheres_70_74`: correlação 0.965
- `populacao_mulheres_15_19` ↔ `populacao_mulheres_75_79`: correlação 0.954
- `populacao_mulheres_15_19` ↔ `populacao_mulheres_80_mais`: correlação 0.949
- `populacao_mulheres_15_19` ↔ `populacao_mulheres`: correlação 0.996
- `populacao_mulheres_15_19` ↔ `populacao_1_menos`: correlação 0.998
- `populacao_mulheres_15_19` ↔ `populacao_11_14`: correlação 0.999
- `populacao_mulheres_15_19` ↔ `populacao_11_13`: correlação 0.999
- `populacao_mulheres_15_19` ↔ `populacao_12_14`: correlação 0.999
- `populacao_mulheres_15_19` ↔ `populacao_1_3`: correlação 0.998
- `populacao_mulheres_15_19` ↔ `populacao_15_mais`: correlação 0.994
- `populacao_mulheres_15_19` ↔ `populacao_15_17`: correlação 1.000
- `populacao_mulheres_15_19` ↔ `populacao_15_24`: correlação 1.000
- `populacao_mulheres_15_19` ↔ `populacao_16_18`: correlação 1.000
- `populacao_mulheres_15_19` ↔ `populacao_18_mais`: correlação 0.994
- `populacao_mulheres_15_19` ↔ `populacao_18_20`: correlação 1.000
- `populacao_mulheres_15_19` ↔ `populacao_18_24`: correlação 0.999
- `populacao_mulheres_15_19` ↔ `populacao_19_21`: correlação 0.999
- `populacao_mulheres_15_19` ↔ `populacao_25_mais`: correlação 0.992
- `populacao_mulheres_15_19` ↔ `populacao_4`: correlação 0.998
- `populacao_mulheres_15_19` ↔ `populacao_5`: correlação 0.998
- `populacao_mulheres_15_19` ↔ `populacao_6`: correlação 0.998
- `populacao_mulheres_15_19` ↔ `populacao_6_10`: correlação 0.999
- `populacao_mulheres_15_19` ↔ `populacao_6_17`: correlação 0.999
- `populacao_mulheres_15_19` ↔ `populacao_65_mais`: correlação 0.966
- `populacao_mulheres_15_19` ↔ `populacao`: correlação 0.996
- `populacao_mulheres_15_19` ↔ `populacao_urbana`: correlação 0.995
- `populacao_mulheres_15_19` ↔ `populacao_dom_pp`: correlação 0.996
- `populacao_mulheres_15_19` ↔ `populacao_dom_pp_exc_renda_nula`: correlação 0.996
- `populacao_mulheres_15_19` ↔ `pea`: correlação 0.994
- `populacao_mulheres_15_19` ↔ `pea_10_14`: correlação 0.970
- `populacao_mulheres_15_19` ↔ `pea_15_17`: correlação 0.978
- `populacao_mulheres_15_19` ↔ `pea_18_mais`: correlação 0.994
- `populacao_mulheres_15_19` ↔ `pia`: correlação 0.995
- `populacao_mulheres_15_19` ↔ `pia_10_14`: correlação 0.999
- `populacao_mulheres_15_19` ↔ `pia_15_17`: correlação 1.000
- `populacao_mulheres_15_19` ↔ `pia_18_mais`: correlação 0.994
- `populacao_mulheres_20_24` ↔ `populacao_mulheres_25_29`: correlação 0.999
- `populacao_mulheres_20_24` ↔ `populacao_mulheres_30_34`: correlação 0.998
- `populacao_mulheres_20_24` ↔ `populacao_mulheres_35_39`: correlação 0.998
- `populacao_mulheres_20_24` ↔ `populacao_mulheres_40_44`: correlação 0.997
- `populacao_mulheres_20_24` ↔ `populacao_mulheres_45_49`: correlação 0.993
- `populacao_mulheres_20_24` ↔ `populacao_mulheres_50_54`: correlação 0.987
- `populacao_mulheres_20_24` ↔ `populacao_mulheres_55_59`: correlação 0.982
- `populacao_mulheres_20_24` ↔ `populacao_mulheres_5_9`: correlação 0.997
- `populacao_mulheres_20_24` ↔ `populacao_mulheres_60_64`: correlação 0.978
- `populacao_mulheres_20_24` ↔ `populacao_mulheres_65_69`: correlação 0.974
- `populacao_mulheres_20_24` ↔ `populacao_mulheres_70_74`: correlação 0.967
- `populacao_mulheres_20_24` ↔ `populacao_mulheres_75_79`: correlação 0.956
- `populacao_mulheres_20_24` ↔ `populacao_mulheres_80_mais`: correlação 0.952
- `populacao_mulheres_20_24` ↔ `populacao_mulheres`: correlação 0.997
- `populacao_mulheres_20_24` ↔ `populacao_1_menos`: correlação 0.997
- `populacao_mulheres_20_24` ↔ `populacao_11_14`: correlação 0.998
- `populacao_mulheres_20_24` ↔ `populacao_11_13`: correlação 0.998
- `populacao_mulheres_20_24` ↔ `populacao_12_14`: correlação 0.998
- `populacao_mulheres_20_24` ↔ `populacao_1_3`: correlação 0.997
- `populacao_mulheres_20_24` ↔ `populacao_15_mais`: correlação 0.996
- `populacao_mulheres_20_24` ↔ `populacao_15_17`: correlação 0.998
- `populacao_mulheres_20_24` ↔ `populacao_15_24`: correlação 1.000
- `populacao_mulheres_20_24` ↔ `populacao_16_18`: correlação 0.999
- `populacao_mulheres_20_24` ↔ `populacao_18_mais`: correlação 0.995
- `populacao_mulheres_20_24` ↔ `populacao_18_20`: correlação 0.999
- `populacao_mulheres_20_24` ↔ `populacao_18_24`: correlação 1.000
- `populacao_mulheres_20_24` ↔ `populacao_19_21`: correlação 0.999
- `populacao_mulheres_20_24` ↔ `populacao_25_mais`: correlação 0.994
- `populacao_mulheres_20_24` ↔ `populacao_4`: correlação 0.997
- `populacao_mulheres_20_24` ↔ `populacao_5`: correlação 0.997
- `populacao_mulheres_20_24` ↔ `populacao_6`: correlação 0.997
- `populacao_mulheres_20_24` ↔ `populacao_6_10`: correlação 0.997
- `populacao_mulheres_20_24` ↔ `populacao_6_17`: correlação 0.998
- `populacao_mulheres_20_24` ↔ `populacao_65_mais`: correlação 0.968
- `populacao_mulheres_20_24` ↔ `populacao`: correlação 0.997
- `populacao_mulheres_20_24` ↔ `populacao_urbana`: correlação 0.996
- `populacao_mulheres_20_24` ↔ `populacao_dom_pp`: correlação 0.997
- `populacao_mulheres_20_24` ↔ `populacao_dom_pp_exc_renda_nula`: correlação 0.997
- `populacao_mulheres_20_24` ↔ `pea`: correlação 0.996
- `populacao_mulheres_20_24` ↔ `pea_10_14`: correlação 0.969
- `populacao_mulheres_20_24` ↔ `pea_15_17`: correlação 0.981
- `populacao_mulheres_20_24` ↔ `pea_18_mais`: correlação 0.996
- `populacao_mulheres_20_24` ↔ `pia`: correlação 0.996
- `populacao_mulheres_20_24` ↔ `pia_10_14`: correlação 0.998
- `populacao_mulheres_20_24` ↔ `pia_15_17`: correlação 0.998
- `populacao_mulheres_20_24` ↔ `pia_18_mais`: correlação 0.995
- `populacao_mulheres_25_29` ↔ `populacao_mulheres_30_34`: correlação 1.000
- `populacao_mulheres_25_29` ↔ `populacao_mulheres_35_39`: correlação 0.999
- `populacao_mulheres_25_29` ↔ `populacao_mulheres_40_44`: correlação 0.998
- `populacao_mulheres_25_29` ↔ `populacao_mulheres_45_49`: correlação 0.995
- `populacao_mulheres_25_29` ↔ `populacao_mulheres_50_54`: correlação 0.990
- `populacao_mulheres_25_29` ↔ `populacao_mulheres_55_59`: correlação 0.985
- `populacao_mulheres_25_29` ↔ `populacao_mulheres_5_9`: correlação 0.996
- `populacao_mulheres_25_29` ↔ `populacao_mulheres_60_64`: correlação 0.982
- `populacao_mulheres_25_29` ↔ `populacao_mulheres_65_69`: correlação 0.978
- `populacao_mulheres_25_29` ↔ `populacao_mulheres_70_74`: correlação 0.971
- `populacao_mulheres_25_29` ↔ `populacao_mulheres_75_79`: correlação 0.961
- `populacao_mulheres_25_29` ↔ `populacao_mulheres_80_mais`: correlação 0.957
- `populacao_mulheres_25_29` ↔ `populacao_mulheres`: correlação 0.998
- `populacao_mulheres_25_29` ↔ `populacao_1_menos`: correlação 0.996
- `populacao_mulheres_25_29` ↔ `populacao_11_14`: correlação 0.997
- `populacao_mulheres_25_29` ↔ `populacao_11_13`: correlação 0.997
- `populacao_mulheres_25_29` ↔ `populacao_12_14`: correlação 0.997
- `populacao_mulheres_25_29` ↔ `populacao_1_3`: correlação 0.996
- `populacao_mulheres_25_29` ↔ `populacao_15_mais`: correlação 0.997
- `populacao_mulheres_25_29` ↔ `populacao_15_17`: correlação 0.997
- `populacao_mulheres_25_29` ↔ `populacao_15_24`: correlação 0.999
- `populacao_mulheres_25_29` ↔ `populacao_16_18`: correlação 0.997
- `populacao_mulheres_25_29` ↔ `populacao_18_mais`: correlação 0.997
- `populacao_mulheres_25_29` ↔ `populacao_18_20`: correlação 0.998
- `populacao_mulheres_25_29` ↔ `populacao_18_24`: correlação 0.999
- `populacao_mulheres_25_29` ↔ `populacao_19_21`: correlação 0.998
- `populacao_mulheres_25_29` ↔ `populacao_25_mais`: correlação 0.996
- `populacao_mulheres_25_29` ↔ `populacao_4`: correlação 0.996
- `populacao_mulheres_25_29` ↔ `populacao_5`: correlação 0.996
- `populacao_mulheres_25_29` ↔ `populacao_6`: correlação 0.996
- `populacao_mulheres_25_29` ↔ `populacao_6_10`: correlação 0.996
- `populacao_mulheres_25_29` ↔ `populacao_6_17`: correlação 0.997
- `populacao_mulheres_25_29` ↔ `populacao_65_mais`: correlação 0.971
- `populacao_mulheres_25_29` ↔ `populacao`: correlação 0.998
- `populacao_mulheres_25_29` ↔ `populacao_urbana`: correlação 0.998
- `populacao_mulheres_25_29` ↔ `populacao_dom_pp`: correlação 0.998
- `populacao_mulheres_25_29` ↔ `populacao_dom_pp_exc_renda_nula`: correlação 0.998
- `populacao_mulheres_25_29` ↔ `pea`: correlação 0.998
- `populacao_mulheres_25_29` ↔ `pea_10_14`: correlação 0.966
- `populacao_mulheres_25_29` ↔ `pea_15_17`: correlação 0.980
- `populacao_mulheres_25_29` ↔ `pea_18_mais`: correlação 0.998
- `populacao_mulheres_25_29` ↔ `pia`: correlação 0.998
- `populacao_mulheres_25_29` ↔ `pia_10_14`: correlação 0.997
- `populacao_mulheres_25_29` ↔ `pia_15_17`: correlação 0.997
- `populacao_mulheres_25_29` ↔ `pia_18_mais`: correlação 0.997
- `populacao_mulheres_30_34` ↔ `populacao_mulheres_35_39`: correlação 1.000
- `populacao_mulheres_30_34` ↔ `populacao_mulheres_40_44`: correlação 0.999
- `populacao_mulheres_30_34` ↔ `populacao_mulheres_45_49`: correlação 0.996
- `populacao_mulheres_30_34` ↔ `populacao_mulheres_50_54`: correlação 0.992
- `populacao_mulheres_30_34` ↔ `populacao_mulheres_55_59`: correlação 0.988
- `populacao_mulheres_30_34` ↔ `populacao_mulheres_5_9`: correlação 0.996
- `populacao_mulheres_30_34` ↔ `populacao_mulheres_60_64`: correlação 0.984
- `populacao_mulheres_30_34` ↔ `populacao_mulheres_65_69`: correlação 0.980
- `populacao_mulheres_30_34` ↔ `populacao_mulheres_70_74`: correlação 0.974
- `populacao_mulheres_30_34` ↔ `populacao_mulheres_75_79`: correlação 0.964
- `populacao_mulheres_30_34` ↔ `populacao_mulheres_80_mais`: correlação 0.960
- `populacao_mulheres_30_34` ↔ `populacao_mulheres`: correlação 0.999
- `populacao_mulheres_30_34` ↔ `populacao_1_menos`: correlação 0.995
- `populacao_mulheres_30_34` ↔ `populacao_11_14`: correlação 0.997
- `populacao_mulheres_30_34` ↔ `populacao_11_13`: correlação 0.997
- `populacao_mulheres_30_34` ↔ `populacao_12_14`: correlação 0.996
- `populacao_mulheres_30_34` ↔ `populacao_1_3`: correlação 0.995
- `populacao_mulheres_30_34` ↔ `populacao_15_mais`: correlação 0.998
- `populacao_mulheres_30_34` ↔ `populacao_15_17`: correlação 0.996
- `populacao_mulheres_30_34` ↔ `populacao_15_24`: correlação 0.998
- `populacao_mulheres_30_34` ↔ `populacao_16_18`: correlação 0.996
- `populacao_mulheres_30_34` ↔ `populacao_18_mais`: correlação 0.998
- `populacao_mulheres_30_34` ↔ `populacao_18_20`: correlação 0.997
- `populacao_mulheres_30_34` ↔ `populacao_18_24`: correlação 0.998
- `populacao_mulheres_30_34` ↔ `populacao_19_21`: correlação 0.998
- `populacao_mulheres_30_34` ↔ `populacao_25_mais`: correlação 0.997
- `populacao_mulheres_30_34` ↔ `populacao_4`: correlação 0.995
- `populacao_mulheres_30_34` ↔ `populacao_5`: correlação 0.995
- `populacao_mulheres_30_34` ↔ `populacao_6`: correlação 0.996
- `populacao_mulheres_30_34` ↔ `populacao_6_10`: correlação 0.996
- `populacao_mulheres_30_34` ↔ `populacao_6_17`: correlação 0.996
- `populacao_mulheres_30_34` ↔ `populacao_65_mais`: correlação 0.974
- `populacao_mulheres_30_34` ↔ `populacao`: correlação 0.999
- `populacao_mulheres_30_34` ↔ `populacao_urbana`: correlação 0.998
- `populacao_mulheres_30_34` ↔ `populacao_dom_pp`: correlação 0.999
- `populacao_mulheres_30_34` ↔ `populacao_dom_pp_exc_renda_nula`: correlação 0.999
- `populacao_mulheres_30_34` ↔ `pea`: correlação 0.999
- `populacao_mulheres_30_34` ↔ `pea_10_14`: correlação 0.964
- `populacao_mulheres_30_34` ↔ `pea_15_17`: correlação 0.979
- `populacao_mulheres_30_34` ↔ `pea_18_mais`: correlação 0.999
- `populacao_mulheres_30_34` ↔ `pia`: correlação 0.998
- `populacao_mulheres_30_34` ↔ `pia_10_14`: correlação 0.996
- `populacao_mulheres_30_34` ↔ `pia_15_17`: correlação 0.996
- `populacao_mulheres_30_34` ↔ `pia_18_mais`: correlação 0.998
- `populacao_mulheres_35_39` ↔ `populacao_mulheres_40_44`: correlação 1.000
- `populacao_mulheres_35_39` ↔ `populacao_mulheres_45_49`: correlação 0.997
- `populacao_mulheres_35_39` ↔ `populacao_mulheres_50_54`: correlação 0.994
- `populacao_mulheres_35_39` ↔ `populacao_mulheres_55_59`: correlação 0.990
- `populacao_mulheres_35_39` ↔ `populacao_mulheres_5_9`: correlação 0.996
- `populacao_mulheres_35_39` ↔ `populacao_mulheres_60_64`: correlação 0.987
- `populacao_mulheres_35_39` ↔ `populacao_mulheres_65_69`: correlação 0.983
- `populacao_mulheres_35_39` ↔ `populacao_mulheres_70_74`: correlação 0.977
- `populacao_mulheres_35_39` ↔ `populacao_mulheres_75_79`: correlação 0.968
- `populacao_mulheres_35_39` ↔ `populacao_mulheres_80_mais`: correlação 0.964
- `populacao_mulheres_35_39` ↔ `populacao_mulheres`: correlação 0.999
- `populacao_mulheres_35_39` ↔ `populacao_1_menos`: correlação 0.995
- `populacao_mulheres_35_39` ↔ `populacao_11_14`: correlação 0.997
- `populacao_mulheres_35_39` ↔ `populacao_11_13`: correlação 0.997
- `populacao_mulheres_35_39` ↔ `populacao_12_14`: correlação 0.996
- `populacao_mulheres_35_39` ↔ `populacao_1_3`: correlação 0.995
- `populacao_mulheres_35_39` ↔ `populacao_15_mais`: correlação 0.999
- `populacao_mulheres_35_39` ↔ `populacao_15_17`: correlação 0.996
- `populacao_mulheres_35_39` ↔ `populacao_15_24`: correlação 0.997
- `populacao_mulheres_35_39` ↔ `populacao_16_18`: correlação 0.996
- `populacao_mulheres_35_39` ↔ `populacao_18_mais`: correlação 0.999
- `populacao_mulheres_35_39` ↔ `populacao_18_20`: correlação 0.997
- `populacao_mulheres_35_39` ↔ `populacao_18_24`: correlação 0.998
- `populacao_mulheres_35_39` ↔ `populacao_19_21`: correlação 0.998
- `populacao_mulheres_35_39` ↔ `populacao_25_mais`: correlação 0.998
- `populacao_mulheres_35_39` ↔ `populacao_4`: correlação 0.995
- `populacao_mulheres_35_39` ↔ `populacao_5`: correlação 0.995
- `populacao_mulheres_35_39` ↔ `populacao_6`: correlação 0.995
- `populacao_mulheres_35_39` ↔ `populacao_6_10`: correlação 0.996
- `populacao_mulheres_35_39` ↔ `populacao_6_17`: correlação 0.996
- `populacao_mulheres_35_39` ↔ `populacao_65_mais`: correlação 0.978
- `populacao_mulheres_35_39` ↔ `populacao`: correlação 0.999
- `populacao_mulheres_35_39` ↔ `populacao_urbana`: correlação 0.999
- `populacao_mulheres_35_39` ↔ `populacao_dom_pp`: correlação 0.999
- `populacao_mulheres_35_39` ↔ `populacao_dom_pp_exc_renda_nula`: correlação 0.999
- `populacao_mulheres_35_39` ↔ `pea`: correlação 0.999
- `populacao_mulheres_35_39` ↔ `pea_10_14`: correlação 0.961
- `populacao_mulheres_35_39` ↔ `pea_15_17`: correlação 0.977
- `populacao_mulheres_35_39` ↔ `pea_18_mais`: correlação 0.999
- `populacao_mulheres_35_39` ↔ `pia`: correlação 0.999
- `populacao_mulheres_35_39` ↔ `pia_10_14`: correlação 0.996
- `populacao_mulheres_35_39` ↔ `pia_15_17`: correlação 0.996
- `populacao_mulheres_35_39` ↔ `pia_18_mais`: correlação 0.999
- `populacao_mulheres_40_44` ↔ `populacao_mulheres_45_49`: correlação 0.999
- `populacao_mulheres_40_44` ↔ `populacao_mulheres_50_54`: correlação 0.996
- `populacao_mulheres_40_44` ↔ `populacao_mulheres_55_59`: correlação 0.992
- `populacao_mulheres_40_44` ↔ `populacao_mulheres_5_9`: correlação 0.994
- `populacao_mulheres_40_44` ↔ `populacao_mulheres_60_64`: correlação 0.990
- `populacao_mulheres_40_44` ↔ `populacao_mulheres_65_69`: correlação 0.987
- `populacao_mulheres_40_44` ↔ `populacao_mulheres_70_74`: correlação 0.981
- `populacao_mulheres_40_44` ↔ `populacao_mulheres_75_79`: correlação 0.972
- `populacao_mulheres_40_44` ↔ `populacao_mulheres_80_mais`: correlação 0.968
- `populacao_mulheres_40_44` ↔ `populacao_mulheres`: correlação 0.999
- `populacao_mulheres_40_44` ↔ `populacao_1_menos`: correlação 0.993
- `populacao_mulheres_40_44` ↔ `populacao_11_14`: correlação 0.995
- `populacao_mulheres_40_44` ↔ `populacao_11_13`: correlação 0.995
- `populacao_mulheres_40_44` ↔ `populacao_12_14`: correlação 0.995
- `populacao_mulheres_40_44` ↔ `populacao_1_3`: correlação 0.993
- `populacao_mulheres_40_44` ↔ `populacao_15_mais`: correlação 0.999
- `populacao_mulheres_40_44` ↔ `populacao_15_17`: correlação 0.995
- `populacao_mulheres_40_44` ↔ `populacao_15_24`: correlação 0.997
- `populacao_mulheres_40_44` ↔ `populacao_16_18`: correlação 0.995
- `populacao_mulheres_40_44` ↔ `populacao_18_mais`: correlação 0.999
- `populacao_mulheres_40_44` ↔ `populacao_18_20`: correlação 0.997
- `populacao_mulheres_40_44` ↔ `populacao_18_24`: correlação 0.997
- `populacao_mulheres_40_44` ↔ `populacao_19_21`: correlação 0.997
- `populacao_mulheres_40_44` ↔ `populacao_25_mais`: correlação 0.999
- `populacao_mulheres_40_44` ↔ `populacao_4`: correlação 0.993
- `populacao_mulheres_40_44` ↔ `populacao_5`: correlação 0.993
- `populacao_mulheres_40_44` ↔ `populacao_6`: correlação 0.994
- `populacao_mulheres_40_44` ↔ `populacao_6_10`: correlação 0.994
- `populacao_mulheres_40_44` ↔ `populacao_6_17`: correlação 0.995
- `populacao_mulheres_40_44` ↔ `populacao_65_mais`: correlação 0.981
- `populacao_mulheres_40_44` ↔ `populacao`: correlação 0.999
- `populacao_mulheres_40_44` ↔ `populacao_urbana`: correlação 0.999
- `populacao_mulheres_40_44` ↔ `populacao_dom_pp`: correlação 0.999
- `populacao_mulheres_40_44` ↔ `populacao_dom_pp_exc_renda_nula`: correlação 0.999
- `populacao_mulheres_40_44` ↔ `pea`: correlação 0.999
- `populacao_mulheres_40_44` ↔ `pea_10_14`: correlação 0.957
- `populacao_mulheres_40_44` ↔ `pea_15_17`: correlação 0.975
- `populacao_mulheres_40_44` ↔ `pea_18_mais`: correlação 0.999
- `populacao_mulheres_40_44` ↔ `pia`: correlação 0.999
- `populacao_mulheres_40_44` ↔ `pia_10_14`: correlação 0.995
- `populacao_mulheres_40_44` ↔ `pia_15_17`: correlação 0.995
- `populacao_mulheres_40_44` ↔ `pia_18_mais`: correlação 0.999
- `populacao_mulheres_45_49` ↔ `populacao_mulheres_50_54`: correlação 0.999
- `populacao_mulheres_45_49` ↔ `populacao_mulheres_55_59`: correlação 0.997
- `populacao_mulheres_45_49` ↔ `populacao_mulheres_5_9`: correlação 0.989
- `populacao_mulheres_45_49` ↔ `populacao_mulheres_60_64`: correlação 0.995
- `populacao_mulheres_45_49` ↔ `populacao_mulheres_65_69`: correlação 0.993
- `populacao_mulheres_45_49` ↔ `populacao_mulheres_70_74`: correlação 0.988
- `populacao_mulheres_45_49` ↔ `populacao_mulheres_75_79`: correlação 0.981
- `populacao_mulheres_45_49` ↔ `populacao_mulheres_80_mais`: correlação 0.978
- `populacao_mulheres_45_49` ↔ `populacao_mulheres`: correlação 0.999
- `populacao_mulheres_45_49` ↔ `populacao_1_menos`: correlação 0.988
- `populacao_mulheres_45_49` ↔ `populacao_11_14`: correlação 0.992
- `populacao_mulheres_45_49` ↔ `populacao_11_13`: correlação 0.992
- `populacao_mulheres_45_49` ↔ `populacao_12_14`: correlação 0.991
- `populacao_mulheres_45_49` ↔ `populacao_1_3`: correlação 0.988
- `populacao_mulheres_45_49` ↔ `populacao_15_mais`: correlação 0.999
- `populacao_mulheres_45_49` ↔ `populacao_15_17`: correlação 0.991
- `populacao_mulheres_45_49` ↔ `populacao_15_24`: correlação 0.993
- `populacao_mulheres_45_49` ↔ `populacao_16_18`: correlação 0.991
- `populacao_mulheres_45_49` ↔ `populacao_18_mais`: correlação 0.999
- `populacao_mulheres_45_49` ↔ `populacao_18_20`: correlação 0.993
- `populacao_mulheres_45_49` ↔ `populacao_18_24`: correlação 0.993
- `populacao_mulheres_45_49` ↔ `populacao_19_21`: correlação 0.994
- `populacao_mulheres_45_49` ↔ `populacao_25_mais`: correlação 1.000
- `populacao_mulheres_45_49` ↔ `populacao_4`: correlação 0.988
- `populacao_mulheres_45_49` ↔ `populacao_5`: correlação 0.988
- `populacao_mulheres_45_49` ↔ `populacao_6`: correlação 0.989
- `populacao_mulheres_45_49` ↔ `populacao_6_10`: correlação 0.990
- `populacao_mulheres_45_49` ↔ `populacao_6_17`: correlação 0.991
- `populacao_mulheres_45_49` ↔ `populacao_65_mais`: correlação 0.989
- `populacao_mulheres_45_49` ↔ `populacao`: correlação 0.998
- `populacao_mulheres_45_49` ↔ `populacao_urbana`: correlação 0.999
- `populacao_mulheres_45_49` ↔ `populacao_dom_pp`: correlação 0.998
- `populacao_mulheres_45_49` ↔ `populacao_dom_pp_exc_renda_nula`: correlação 0.998
- `populacao_mulheres_45_49` ↔ `pea`: correlação 0.998
- `populacao_mulheres_45_49` ↔ `pea_10_14`: correlação 0.948
- `populacao_mulheres_45_49` ↔ `pea_15_17`: correlação 0.968
- `populacao_mulheres_45_49` ↔ `pea_18_mais`: correlação 0.998
- `populacao_mulheres_45_49` ↔ `pia`: correlação 0.999
- `populacao_mulheres_45_49` ↔ `pia_10_14`: correlação 0.991
- `populacao_mulheres_45_49` ↔ `pia_15_17`: correlação 0.991
- `populacao_mulheres_45_49` ↔ `pia_18_mais`: correlação 0.999
- `populacao_mulheres_50_54` ↔ `populacao_mulheres_55_59`: correlação 0.999
- `populacao_mulheres_50_54` ↔ `populacao_mulheres_5_9`: correlação 0.984
- `populacao_mulheres_50_54` ↔ `populacao_mulheres_60_64`: correlação 0.998
- `populacao_mulheres_50_54` ↔ `populacao_mulheres_65_69`: correlação 0.997
- `populacao_mulheres_50_54` ↔ `populacao_mulheres_70_74`: correlação 0.993
- `populacao_mulheres_50_54` ↔ `populacao_mulheres_75_79`: correlação 0.988
- `populacao_mulheres_50_54` ↔ `populacao_mulheres_80_mais`: correlação 0.985
- `populacao_mulheres_50_54` ↔ `populacao_mulheres`: correlação 0.996
- `populacao_mulheres_50_54` ↔ `populacao_1_menos`: correlação 0.982
- `populacao_mulheres_50_54` ↔ `populacao_11_14`: correlação 0.987
- `populacao_mulheres_50_54` ↔ `populacao_11_13`: correlação 0.987
- `populacao_mulheres_50_54` ↔ `populacao_12_14`: correlação 0.986
- `populacao_mulheres_50_54` ↔ `populacao_1_3`: correlação 0.982
- `populacao_mulheres_50_54` ↔ `populacao_15_mais`: correlação 0.997
- `populacao_mulheres_50_54` ↔ `populacao_15_17`: correlação 0.985
- `populacao_mulheres_50_54` ↔ `populacao_15_24`: correlação 0.988
- `populacao_mulheres_50_54` ↔ `populacao_16_18`: correlação 0.985
- `populacao_mulheres_50_54` ↔ `populacao_18_mais`: correlação 0.998
- `populacao_mulheres_50_54` ↔ `populacao_18_20`: correlação 0.988
- `populacao_mulheres_50_54` ↔ `populacao_18_24`: correlação 0.988
- `populacao_mulheres_50_54` ↔ `populacao_19_21`: correlação 0.989
- `populacao_mulheres_50_54` ↔ `populacao_25_mais`: correlação 0.999
- `populacao_mulheres_50_54` ↔ `populacao_4`: correlação 0.982
- `populacao_mulheres_50_54` ↔ `populacao_5`: correlação 0.983
- `populacao_mulheres_50_54` ↔ `populacao_6`: correlação 0.984
- `populacao_mulheres_50_54` ↔ `populacao_6_10`: correlação 0.985
- `populacao_mulheres_50_54` ↔ `populacao_6_17`: correlação 0.986
- `populacao_mulheres_50_54` ↔ `populacao_65_mais`: correlação 0.994
- `populacao_mulheres_50_54` ↔ `populacao`: correlação 0.996
- `populacao_mulheres_50_54` ↔ `populacao_urbana`: correlação 0.996
- `populacao_mulheres_50_54` ↔ `populacao_dom_pp`: correlação 0.996
- `populacao_mulheres_50_54` ↔ `populacao_dom_pp_exc_renda_nula`: correlação 0.996
- `populacao_mulheres_50_54` ↔ `pea`: correlação 0.995
- `populacao_mulheres_50_54` ↔ `pea_10_14`: correlação 0.940
- `populacao_mulheres_50_54` ↔ `pea_15_17`: correlação 0.960
- `populacao_mulheres_50_54` ↔ `pea_18_mais`: correlação 0.996
- `populacao_mulheres_50_54` ↔ `pia`: correlação 0.997
- `populacao_mulheres_50_54` ↔ `pia_10_14`: correlação 0.987
- `populacao_mulheres_50_54` ↔ `pia_15_17`: correlação 0.985
- `populacao_mulheres_50_54` ↔ `pia_18_mais`: correlação 0.998
- `populacao_mulheres_55_59` ↔ `populacao_mulheres_5_9`: correlação 0.979
- `populacao_mulheres_55_59` ↔ `populacao_mulheres_60_64`: correlação 1.000
- `populacao_mulheres_55_59` ↔ `populacao_mulheres_65_69`: correlação 0.999
- `populacao_mulheres_55_59` ↔ `populacao_mulheres_70_74`: correlação 0.997
- `populacao_mulheres_55_59` ↔ `populacao_mulheres_75_79`: correlação 0.993
- `populacao_mulheres_55_59` ↔ `populacao_mulheres_80_mais`: correlação 0.990
- `populacao_mulheres_55_59` ↔ `populacao_mulheres`: correlação 0.993
- `populacao_mulheres_55_59` ↔ `populacao_1_menos`: correlação 0.977
- `populacao_mulheres_55_59` ↔ `populacao_11_14`: correlação 0.982
- `populacao_mulheres_55_59` ↔ `populacao_11_13`: correlação 0.982
- `populacao_mulheres_55_59` ↔ `populacao_12_14`: correlação 0.982
- `populacao_mulheres_55_59` ↔ `populacao_1_3`: correlação 0.977
- `populacao_mulheres_55_59` ↔ `populacao_15_mais`: correlação 0.995
- `populacao_mulheres_55_59` ↔ `populacao_15_17`: correlação 0.980
- `populacao_mulheres_55_59` ↔ `populacao_15_24`: correlação 0.983
- `populacao_mulheres_55_59` ↔ `populacao_16_18`: correlação 0.980
- `populacao_mulheres_55_59` ↔ `populacao_18_mais`: correlação 0.995
- `populacao_mulheres_55_59` ↔ `populacao_18_20`: correlação 0.983
- `populacao_mulheres_55_59` ↔ `populacao_18_24`: correlação 0.983
- `populacao_mulheres_55_59` ↔ `populacao_19_21`: correlação 0.984
- `populacao_mulheres_55_59` ↔ `populacao_25_mais`: correlação 0.997
- `populacao_mulheres_55_59` ↔ `populacao_4`: correlação 0.977
- `populacao_mulheres_55_59` ↔ `populacao_5`: correlação 0.978
- `populacao_mulheres_55_59` ↔ `populacao_6`: correlação 0.979
- `populacao_mulheres_55_59` ↔ `populacao_6_10`: correlação 0.980
- `populacao_mulheres_55_59` ↔ `populacao_6_17`: correlação 0.981
- `populacao_mulheres_55_59` ↔ `populacao_65_mais`: correlação 0.997
- `populacao_mulheres_55_59` ↔ `populacao`: correlação 0.993
- `populacao_mulheres_55_59` ↔ `populacao_urbana`: correlação 0.993
- `populacao_mulheres_55_59` ↔ `populacao_dom_pp`: correlação 0.992
- `populacao_mulheres_55_59` ↔ `populacao_dom_pp_exc_renda_nula`: correlação 0.993
- `populacao_mulheres_55_59` ↔ `pea`: correlação 0.992
- `populacao_mulheres_55_59` ↔ `pea_10_14`: correlação 0.931
- `populacao_mulheres_55_59` ↔ `pea_15_17`: correlação 0.952
- `populacao_mulheres_55_59` ↔ `pea_18_mais`: correlação 0.992
- `populacao_mulheres_55_59` ↔ `pia`: correlação 0.994
- `populacao_mulheres_55_59` ↔ `pia_10_14`: correlação 0.982
- `populacao_mulheres_55_59` ↔ `pia_15_17`: correlação 0.980
- `populacao_mulheres_55_59` ↔ `pia_18_mais`: correlação 0.995
- `populacao_mulheres_5_9` ↔ `populacao_mulheres_60_64`: correlação 0.975
- `populacao_mulheres_5_9` ↔ `populacao_mulheres_65_69`: correlação 0.971
- `populacao_mulheres_5_9` ↔ `populacao_mulheres_70_74`: correlação 0.964
- `populacao_mulheres_5_9` ↔ `populacao_mulheres_75_79`: correlação 0.953
- `populacao_mulheres_5_9` ↔ `populacao_mulheres_80_mais`: correlação 0.948
- `populacao_mulheres_5_9` ↔ `populacao_mulheres`: correlação 0.995
- `populacao_mulheres_5_9` ↔ `populacao_1_menos`: correlação 1.000
- `populacao_mulheres_5_9` ↔ `populacao_11_14`: correlação 1.000
- `populacao_mulheres_5_9` ↔ `populacao_11_13`: correlação 1.000
- `populacao_mulheres_5_9` ↔ `populacao_12_14`: correlação 1.000
- `populacao_mulheres_5_9` ↔ `populacao_1_3`: correlação 1.000
- `populacao_mulheres_5_9` ↔ `populacao_15_mais`: correlação 0.994
- `populacao_mulheres_5_9` ↔ `populacao_15_17`: correlação 0.999
- `populacao_mulheres_5_9` ↔ `populacao_15_24`: correlação 0.998
- `populacao_mulheres_5_9` ↔ `populacao_16_18`: correlação 0.999
- `populacao_mulheres_5_9` ↔ `populacao_18_mais`: correlação 0.993
- `populacao_mulheres_5_9` ↔ `populacao_18_20`: correlação 0.998
- `populacao_mulheres_5_9` ↔ `populacao_18_24`: correlação 0.998
- `populacao_mulheres_5_9` ↔ `populacao_19_21`: correlação 0.998
- `populacao_mulheres_5_9` ↔ `populacao_25_mais`: correlação 0.991
- `populacao_mulheres_5_9` ↔ `populacao_4`: correlação 1.000
- `populacao_mulheres_5_9` ↔ `populacao_5`: correlação 1.000
- `populacao_mulheres_5_9` ↔ `populacao_6`: correlação 1.000
- `populacao_mulheres_5_9` ↔ `populacao_6_10`: correlação 1.000
- `populacao_mulheres_5_9` ↔ `populacao_6_17`: correlação 1.000
- `populacao_mulheres_5_9` ↔ `populacao_65_mais`: correlação 0.965
- `populacao_mulheres_5_9` ↔ `populacao`: correlação 0.996
- `populacao_mulheres_5_9` ↔ `populacao_urbana`: correlação 0.994
- `populacao_mulheres_5_9` ↔ `populacao_dom_pp`: correlação 0.996
- `populacao_mulheres_5_9` ↔ `populacao_dom_pp_exc_renda_nula`: correlação 0.996
- `populacao_mulheres_5_9` ↔ `pea`: correlação 0.993
- `populacao_mulheres_5_9` ↔ `pea_10_14`: correlação 0.973
- `populacao_mulheres_5_9` ↔ `pea_15_17`: correlação 0.979
- `populacao_mulheres_5_9` ↔ `pea_18_mais`: correlação 0.993
- `populacao_mulheres_5_9` ↔ `pia`: correlação 0.995
- `populacao_mulheres_5_9` ↔ `pia_10_14`: correlação 1.000
- `populacao_mulheres_5_9` ↔ `pia_15_17`: correlação 0.999
- `populacao_mulheres_5_9` ↔ `pia_18_mais`: correlação 0.993
- `populacao_mulheres_60_64` ↔ `populacao_mulheres_65_69`: correlação 1.000
- `populacao_mulheres_60_64` ↔ `populacao_mulheres_70_74`: correlação 0.998
- `populacao_mulheres_60_64` ↔ `populacao_mulheres_75_79`: correlação 0.995
- `populacao_mulheres_60_64` ↔ `populacao_mulheres_80_mais`: correlação 0.993
- `populacao_mulheres_60_64` ↔ `populacao_mulheres`: correlação 0.991
- `populacao_mulheres_60_64` ↔ `populacao_1_menos`: correlação 0.972
- `populacao_mulheres_60_64` ↔ `populacao_11_14`: correlação 0.978
- `populacao_mulheres_60_64` ↔ `populacao_11_13`: correlação 0.978
- `populacao_mulheres_60_64` ↔ `populacao_12_14`: correlação 0.978
- `populacao_mulheres_60_64` ↔ `populacao_1_3`: correlação 0.972
- `populacao_mulheres_60_64` ↔ `populacao_15_mais`: correlação 0.992
- `populacao_mulheres_60_64` ↔ `populacao_15_17`: correlação 0.977
- `populacao_mulheres_60_64` ↔ `populacao_15_24`: correlação 0.979
- `populacao_mulheres_60_64` ↔ `populacao_16_18`: correlação 0.976
- `populacao_mulheres_60_64` ↔ `populacao_18_mais`: correlação 0.993
- `populacao_mulheres_60_64` ↔ `populacao_18_20`: correlação 0.979
- `populacao_mulheres_60_64` ↔ `populacao_18_24`: correlação 0.979
- `populacao_mulheres_60_64` ↔ `populacao_19_21`: correlação 0.981
- `populacao_mulheres_60_64` ↔ `populacao_25_mais`: correlação 0.995
- `populacao_mulheres_60_64` ↔ `populacao_4`: correlação 0.973
- `populacao_mulheres_60_64` ↔ `populacao_5`: correlação 0.974
- `populacao_mulheres_60_64` ↔ `populacao_6`: correlação 0.975
- `populacao_mulheres_60_64` ↔ `populacao_6_10`: correlação 0.976
- `populacao_mulheres_60_64` ↔ `populacao_6_17`: correlação 0.977
- `populacao_mulheres_60_64` ↔ `populacao_65_mais`: correlação 0.998
- `populacao_mulheres_60_64` ↔ `populacao`: correlação 0.990
- `populacao_mulheres_60_64` ↔ `populacao_urbana`: correlação 0.991
- `populacao_mulheres_60_64` ↔ `populacao_dom_pp`: correlação 0.990
- `populacao_mulheres_60_64` ↔ `populacao_dom_pp_exc_renda_nula`: correlação 0.990
- `populacao_mulheres_60_64` ↔ `pea`: correlação 0.989
- `populacao_mulheres_60_64` ↔ `pea_10_14`: correlação 0.925
- `populacao_mulheres_60_64` ↔ `pea_15_17`: correlação 0.945
- `populacao_mulheres_60_64` ↔ `pea_18_mais`: correlação 0.989
- `populacao_mulheres_60_64` ↔ `pia`: correlação 0.991
- `populacao_mulheres_60_64` ↔ `pia_10_14`: correlação 0.978
- `populacao_mulheres_60_64` ↔ `pia_15_17`: correlação 0.977
- `populacao_mulheres_60_64` ↔ `pia_18_mais`: correlação 0.993
- `populacao_mulheres_65_69` ↔ `populacao_mulheres_70_74`: correlação 0.999
- `populacao_mulheres_65_69` ↔ `populacao_mulheres_75_79`: correlação 0.997
- `populacao_mulheres_65_69` ↔ `populacao_mulheres_80_mais`: correlação 0.995
- `populacao_mulheres_65_69` ↔ `populacao_mulheres`: correlação 0.988
- `populacao_mulheres_65_69` ↔ `populacao_1_menos`: correlação 0.968
- `populacao_mulheres_65_69` ↔ `populacao_11_14`: correlação 0.974
- `populacao_mulheres_65_69` ↔ `populacao_11_13`: correlação 0.975
- `populacao_mulheres_65_69` ↔ `populacao_12_14`: correlação 0.974
- `populacao_mulheres_65_69` ↔ `populacao_1_3`: correlação 0.968
- `populacao_mulheres_65_69` ↔ `populacao_15_mais`: correlação 0.990
- `populacao_mulheres_65_69` ↔ `populacao_15_17`: correlação 0.973
- `populacao_mulheres_65_69` ↔ `populacao_15_24`: correlação 0.975
- `populacao_mulheres_65_69` ↔ `populacao_16_18`: correlação 0.972
- `populacao_mulheres_65_69` ↔ `populacao_18_mais`: correlação 0.990
- `populacao_mulheres_65_69` ↔ `populacao_18_20`: correlação 0.976
- `populacao_mulheres_65_69` ↔ `populacao_18_24`: correlação 0.975
- `populacao_mulheres_65_69` ↔ `populacao_19_21`: correlação 0.977
- `populacao_mulheres_65_69` ↔ `populacao_25_mais`: correlação 0.992
- `populacao_mulheres_65_69` ↔ `populacao_4`: correlação 0.969
- `populacao_mulheres_65_69` ↔ `populacao_5`: correlação 0.970
- `populacao_mulheres_65_69` ↔ `populacao_6`: correlação 0.971
- `populacao_mulheres_65_69` ↔ `populacao_6_10`: correlação 0.972
- `populacao_mulheres_65_69` ↔ `populacao_6_17`: correlação 0.973
- `populacao_mulheres_65_69` ↔ `populacao_65_mais`: correlação 0.999
- `populacao_mulheres_65_69` ↔ `populacao`: correlação 0.987
- `populacao_mulheres_65_69` ↔ `populacao_urbana`: correlação 0.988
- `populacao_mulheres_65_69` ↔ `populacao_dom_pp`: correlação 0.987
- `populacao_mulheres_65_69` ↔ `populacao_dom_pp_exc_renda_nula`: correlação 0.987
- `populacao_mulheres_65_69` ↔ `pea`: correlação 0.985
- `populacao_mulheres_65_69` ↔ `pea_10_14`: correlação 0.920
- `populacao_mulheres_65_69` ↔ `pea_15_17`: correlação 0.939
- `populacao_mulheres_65_69` ↔ `pea_18_mais`: correlação 0.986
- `populacao_mulheres_65_69` ↔ `pia`: correlação 0.989
- `populacao_mulheres_65_69` ↔ `pia_10_14`: correlação 0.974
- `populacao_mulheres_65_69` ↔ `pia_15_17`: correlação 0.973
- `populacao_mulheres_65_69` ↔ `pia_18_mais`: correlação 0.990
- `populacao_mulheres_70_74` ↔ `populacao_mulheres_75_79`: correlação 0.999
- `populacao_mulheres_70_74` ↔ `populacao_mulheres_80_mais`: correlação 0.998
- `populacao_mulheres_70_74` ↔ `populacao_mulheres`: correlação 0.983
- `populacao_mulheres_70_74` ↔ `populacao_1_menos`: correlação 0.961
- `populacao_mulheres_70_74` ↔ `populacao_11_14`: correlação 0.968
- `populacao_mulheres_70_74` ↔ `populacao_11_13`: correlação 0.968
- `populacao_mulheres_70_74` ↔ `populacao_12_14`: correlação 0.968
- `populacao_mulheres_70_74` ↔ `populacao_1_3`: correlação 0.961
- `populacao_mulheres_70_74` ↔ `populacao_15_mais`: correlação 0.985
- `populacao_mulheres_70_74` ↔ `populacao_15_17`: correlação 0.966
- `populacao_mulheres_70_74` ↔ `populacao_15_24`: correlação 0.968
- `populacao_mulheres_70_74` ↔ `populacao_16_18`: correlação 0.966
- `populacao_mulheres_70_74` ↔ `populacao_18_mais`: correlação 0.986
- `populacao_mulheres_70_74` ↔ `populacao_18_20`: correlação 0.969
- `populacao_mulheres_70_74` ↔ `populacao_18_24`: correlação 0.969
- `populacao_mulheres_70_74` ↔ `populacao_19_21`: correlação 0.970
- `populacao_mulheres_70_74` ↔ `populacao_25_mais`: correlação 0.988
- `populacao_mulheres_70_74` ↔ `populacao_4`: correlação 0.962
- `populacao_mulheres_70_74` ↔ `populacao_5`: correlação 0.963
- `populacao_mulheres_70_74` ↔ `populacao_6`: correlação 0.963
- `populacao_mulheres_70_74` ↔ `populacao_6_10`: correlação 0.965
- `populacao_mulheres_70_74` ↔ `populacao_6_17`: correlação 0.966
- `populacao_mulheres_70_74` ↔ `populacao_65_mais`: correlação 1.000
- `populacao_mulheres_70_74` ↔ `populacao`: correlação 0.982
- `populacao_mulheres_70_74` ↔ `populacao_urbana`: correlação 0.982
- `populacao_mulheres_70_74` ↔ `populacao_dom_pp`: correlação 0.981
- `populacao_mulheres_70_74` ↔ `populacao_dom_pp_exc_renda_nula`: correlação 0.982
- `populacao_mulheres_70_74` ↔ `pea`: correlação 0.979
- `populacao_mulheres_70_74` ↔ `pea_10_14`: correlação 0.910
- `populacao_mulheres_70_74` ↔ `pea_15_17`: correlação 0.927
- `populacao_mulheres_70_74` ↔ `pea_18_mais`: correlação 0.980
- `populacao_mulheres_70_74` ↔ `pia`: correlação 0.984
- `populacao_mulheres_70_74` ↔ `pia_10_14`: correlação 0.968
- `populacao_mulheres_70_74` ↔ `pia_15_17`: correlação 0.966
- `populacao_mulheres_70_74` ↔ `pia_18_mais`: correlação 0.986
- `populacao_mulheres_75_79` ↔ `populacao_mulheres_80_mais`: correlação 0.999
- `populacao_mulheres_75_79` ↔ `populacao_mulheres`: correlação 0.975
- `populacao_mulheres_75_79` ↔ `populacao_1_menos`: correlação 0.950
- `populacao_mulheres_75_79` ↔ `populacao_11_14`: correlação 0.957
- `populacao_mulheres_75_79` ↔ `populacao_11_13`: correlação 0.958
- `populacao_mulheres_75_79` ↔ `populacao_12_14`: correlação 0.957
- `populacao_mulheres_75_79` ↔ `populacao_1_3`: correlação 0.950
- `populacao_mulheres_75_79` ↔ `populacao_15_mais`: correlação 0.977
- `populacao_mulheres_75_79` ↔ `populacao_15_17`: correlação 0.955
- `populacao_mulheres_75_79` ↔ `populacao_15_24`: correlação 0.957
- `populacao_mulheres_75_79` ↔ `populacao_16_18`: correlação 0.955
- `populacao_mulheres_75_79` ↔ `populacao_18_mais`: correlação 0.978
- `populacao_mulheres_75_79` ↔ `populacao_18_20`: correlação 0.959
- `populacao_mulheres_75_79` ↔ `populacao_18_24`: correlação 0.958
- `populacao_mulheres_75_79` ↔ `populacao_19_21`: correlação 0.960
- `populacao_mulheres_75_79` ↔ `populacao_25_mais`: correlação 0.981
- `populacao_mulheres_75_79` ↔ `populacao_4`: correlação 0.951
- `populacao_mulheres_75_79` ↔ `populacao_5`: correlação 0.952
- `populacao_mulheres_75_79` ↔ `populacao_6`: correlação 0.953
- `populacao_mulheres_75_79` ↔ `populacao_6_10`: correlação 0.954
- `populacao_mulheres_75_79` ↔ `populacao_6_17`: correlação 0.956
- `populacao_mulheres_75_79` ↔ `populacao_65_mais`: correlação 0.999
- `populacao_mulheres_75_79` ↔ `populacao`: correlação 0.973
- `populacao_mulheres_75_79` ↔ `populacao_urbana`: correlação 0.974
- `populacao_mulheres_75_79` ↔ `populacao_dom_pp`: correlação 0.973
- `populacao_mulheres_75_79` ↔ `populacao_dom_pp_exc_renda_nula`: correlação 0.973
- `populacao_mulheres_75_79` ↔ `pea`: correlação 0.971
- `populacao_mulheres_75_79` ↔ `pea_15_17`: correlação 0.913
- `populacao_mulheres_75_79` ↔ `pea_18_mais`: correlação 0.972
- `populacao_mulheres_75_79` ↔ `pia`: correlação 0.976
- `populacao_mulheres_75_79` ↔ `pia_10_14`: correlação 0.957
- `populacao_mulheres_75_79` ↔ `pia_15_17`: correlação 0.955
- `populacao_mulheres_75_79` ↔ `pia_18_mais`: correlação 0.978
- `populacao_mulheres_80_mais` ↔ `populacao_mulheres`: correlação 0.971
- `populacao_mulheres_80_mais` ↔ `populacao_1_menos`: correlação 0.945
- `populacao_mulheres_80_mais` ↔ `populacao_11_14`: correlação 0.952
- `populacao_mulheres_80_mais` ↔ `populacao_11_13`: correlação 0.953
- `populacao_mulheres_80_mais` ↔ `populacao_12_14`: correlação 0.952
- `populacao_mulheres_80_mais` ↔ `populacao_1_3`: correlação 0.945
- `populacao_mulheres_80_mais` ↔ `populacao_15_mais`: correlação 0.973
- `populacao_mulheres_80_mais` ↔ `populacao_15_17`: correlação 0.951
- `populacao_mulheres_80_mais` ↔ `populacao_15_24`: correlação 0.953
- `populacao_mulheres_80_mais` ↔ `populacao_16_18`: correlação 0.950
- `populacao_mulheres_80_mais` ↔ `populacao_18_mais`: correlação 0.974
- `populacao_mulheres_80_mais` ↔ `populacao_18_20`: correlação 0.954
- `populacao_mulheres_80_mais` ↔ `populacao_18_24`: correlação 0.954
- `populacao_mulheres_80_mais` ↔ `populacao_19_21`: correlação 0.956
- `populacao_mulheres_80_mais` ↔ `populacao_25_mais`: correlação 0.978
- `populacao_mulheres_80_mais` ↔ `populacao_4`: correlação 0.945
- `populacao_mulheres_80_mais` ↔ `populacao_5`: correlação 0.947
- `populacao_mulheres_80_mais` ↔ `populacao_6`: correlação 0.948
- `populacao_mulheres_80_mais` ↔ `populacao_6_10`: correlação 0.949
- `populacao_mulheres_80_mais` ↔ `populacao_6_17`: correlação 0.951
- `populacao_mulheres_80_mais` ↔ `populacao_65_mais`: correlação 0.997
- `populacao_mulheres_80_mais` ↔ `populacao`: correlação 0.969
- `populacao_mulheres_80_mais` ↔ `populacao_urbana`: correlação 0.970
- `populacao_mulheres_80_mais` ↔ `populacao_dom_pp`: correlação 0.969
- `populacao_mulheres_80_mais` ↔ `populacao_dom_pp_exc_renda_nula`: correlação 0.969
- `populacao_mulheres_80_mais` ↔ `pea`: correlação 0.967
- `populacao_mulheres_80_mais` ↔ `pea_15_17`: correlação 0.906
- `populacao_mulheres_80_mais` ↔ `pea_18_mais`: correlação 0.968
- `populacao_mulheres_80_mais` ↔ `pia`: correlação 0.972
- `populacao_mulheres_80_mais` ↔ `pia_10_14`: correlação 0.952
- `populacao_mulheres_80_mais` ↔ `pia_15_17`: correlação 0.950
- `populacao_mulheres_80_mais` ↔ `pia_18_mais`: correlação 0.974
- `populacao_mulheres` ↔ `populacao_1_menos`: correlação 0.994
- `populacao_mulheres` ↔ `populacao_11_14`: correlação 0.997
- `populacao_mulheres` ↔ `populacao_11_13`: correlação 0.997
- `populacao_mulheres` ↔ `populacao_12_14`: correlação 0.997
- `populacao_mulheres` ↔ `populacao_1_3`: correlação 0.994
- `populacao_mulheres` ↔ `populacao_15_mais`: correlação 1.000
- `populacao_mulheres` ↔ `populacao_15_17`: correlação 0.996
- `populacao_mulheres` ↔ `populacao_15_24`: correlação 0.997
- `populacao_mulheres` ↔ `populacao_16_18`: correlação 0.996
- `populacao_mulheres` ↔ `populacao_18_mais`: correlação 1.000
- `populacao_mulheres` ↔ `populacao_18_20`: correlação 0.997
- `populacao_mulheres` ↔ `populacao_18_24`: correlação 0.997
- `populacao_mulheres` ↔ `populacao_19_21`: correlação 0.998
- `populacao_mulheres` ↔ `populacao_25_mais`: correlação 0.999
- `populacao_mulheres` ↔ `populacao_4`: correlação 0.994
- `populacao_mulheres` ↔ `populacao_5`: correlação 0.995
- `populacao_mulheres` ↔ `populacao_6`: correlação 0.995
- `populacao_mulheres` ↔ `populacao_6_10`: correlação 0.996
- `populacao_mulheres` ↔ `populacao_6_17`: correlação 0.996
- `populacao_mulheres` ↔ `populacao_65_mais`: correlação 0.983
- `populacao_mulheres` ↔ `populacao`: correlação 1.000
- `populacao_mulheres` ↔ `populacao_urbana`: correlação 1.000
- `populacao_mulheres` ↔ `populacao_dom_pp`: correlação 1.000
- `populacao_mulheres` ↔ `populacao_dom_pp_exc_renda_nula`: correlação 1.000
- `populacao_mulheres` ↔ `pea`: correlação 0.999
- `populacao_mulheres` ↔ `pea_10_14`: correlação 0.959
- `populacao_mulheres` ↔ `pea_15_17`: correlação 0.973
- `populacao_mulheres` ↔ `pea_18_mais`: correlação 0.999
- `populacao_mulheres` ↔ `pia`: correlação 1.000
- `populacao_mulheres` ↔ `pia_10_14`: correlação 0.997
- `populacao_mulheres` ↔ `pia_15_17`: correlação 0.996
- `populacao_mulheres` ↔ `pia_18_mais`: correlação 1.000
- `populacao_1_menos` ↔ `populacao_11_14`: correlação 0.999
- `populacao_1_menos` ↔ `populacao_11_13`: correlação 0.999
- `populacao_1_menos` ↔ `populacao_12_14`: correlação 0.999
- `populacao_1_menos` ↔ `populacao_1_3`: correlação 1.000
- `populacao_1_menos` ↔ `populacao_15_mais`: correlação 0.993
- `populacao_1_menos` ↔ `populacao_15_17`: correlação 0.998
- `populacao_1_menos` ↔ `populacao_15_24`: correlação 0.998
- `populacao_1_menos` ↔ `populacao_16_18`: correlação 0.998
- `populacao_1_menos` ↔ `populacao_18_mais`: correlação 0.992
- `populacao_1_menos` ↔ `populacao_18_20`: correlação 0.998
- `populacao_1_menos` ↔ `populacao_18_24`: correlação 0.998
- `populacao_1_menos` ↔ `populacao_19_21`: correlação 0.998
- `populacao_1_menos` ↔ `populacao_25_mais`: correlação 0.990
- `populacao_1_menos` ↔ `populacao_4`: correlação 1.000
- `populacao_1_menos` ↔ `populacao_5`: correlação 1.000
- `populacao_1_menos` ↔ `populacao_6`: correlação 1.000
- `populacao_1_menos` ↔ `populacao_6_10`: correlação 0.999
- `populacao_1_menos` ↔ `populacao_6_17`: correlação 0.999
- `populacao_1_menos` ↔ `populacao_65_mais`: correlação 0.962
- `populacao_1_menos` ↔ `populacao`: correlação 0.995
- `populacao_1_menos` ↔ `populacao_urbana`: correlação 0.993
- `populacao_1_menos` ↔ `populacao_dom_pp`: correlação 0.995
- `populacao_1_menos` ↔ `populacao_dom_pp_exc_renda_nula`: correlação 0.995
- `populacao_1_menos` ↔ `pea`: correlação 0.993
- `populacao_1_menos` ↔ `pea_10_14`: correlação 0.974
- `populacao_1_menos` ↔ `pea_15_17`: correlação 0.981
- `populacao_1_menos` ↔ `pea_18_mais`: correlação 0.992
- `populacao_1_menos` ↔ `pia`: correlação 0.994
- `populacao_1_menos` ↔ `pia_10_14`: correlação 0.999
- `populacao_1_menos` ↔ `pia_15_17`: correlação 0.998
- `populacao_1_menos` ↔ `pia_18_mais`: correlação 0.992
- `populacao_11_14` ↔ `populacao_11_13`: correlação 1.000
- `populacao_11_14` ↔ `populacao_12_14`: correlação 1.000
- `populacao_11_14` ↔ `populacao_1_3`: correlação 0.999
- `populacao_11_14` ↔ `populacao_15_mais`: correlação 0.995
- `populacao_11_14` ↔ `populacao_15_17`: correlação 0.999
- `populacao_11_14` ↔ `populacao_15_24`: correlação 0.999
- `populacao_11_14` ↔ `populacao_16_18`: correlação 0.999
- `populacao_11_14` ↔ `populacao_18_mais`: correlação 0.995
- `populacao_11_14` ↔ `populacao_18_20`: correlação 0.999
- `populacao_11_14` ↔ `populacao_18_24`: correlação 0.998
- `populacao_11_14` ↔ `populacao_19_21`: correlação 0.999
- `populacao_11_14` ↔ `populacao_25_mais`: correlação 0.993
- `populacao_11_14` ↔ `populacao_4`: correlação 0.999
- `populacao_11_14` ↔ `populacao_5`: correlação 0.999
- `populacao_11_14` ↔ `populacao_6`: correlação 1.000
- `populacao_11_14` ↔ `populacao_6_10`: correlação 1.000
- `populacao_11_14` ↔ `populacao_6_17`: correlação 1.000
- `populacao_11_14` ↔ `populacao_65_mais`: correlação 0.968
- `populacao_11_14` ↔ `populacao`: correlação 0.997
- `populacao_11_14` ↔ `populacao_urbana`: correlação 0.996
- `populacao_11_14` ↔ `populacao_dom_pp`: correlação 0.997
- `populacao_11_14` ↔ `populacao_dom_pp_exc_renda_nula`: correlação 0.997
- `populacao_11_14` ↔ `pea`: correlação 0.995
- `populacao_11_14` ↔ `pea_10_14`: correlação 0.971
- `populacao_11_14` ↔ `pea_15_17`: correlação 0.979
- `populacao_11_14` ↔ `pea_18_mais`: correlação 0.994
- `populacao_11_14` ↔ `pia`: correlação 0.996
- `populacao_11_14` ↔ `pia_10_14`: correlação 1.000
- `populacao_11_14` ↔ `pia_15_17`: correlação 0.999
- `populacao_11_14` ↔ `pia_18_mais`: correlação 0.995
- `populacao_11_13` ↔ `populacao_12_14`: correlação 1.000
- `populacao_11_13` ↔ `populacao_1_3`: correlação 0.999
- `populacao_11_13` ↔ `populacao_15_mais`: correlação 0.995
- `populacao_11_13` ↔ `populacao_15_17`: correlação 0.999
- `populacao_11_13` ↔ `populacao_15_24`: correlação 0.999
- `populacao_11_13` ↔ `populacao_16_18`: correlação 0.999
- `populacao_11_13` ↔ `populacao_18_mais`: correlação 0.995
- `populacao_11_13` ↔ `populacao_18_20`: correlação 0.999
- `populacao_11_13` ↔ `populacao_18_24`: correlação 0.998
- `populacao_11_13` ↔ `populacao_19_21`: correlação 0.998
- `populacao_11_13` ↔ `populacao_25_mais`: correlação 0.993
- `populacao_11_13` ↔ `populacao_4`: correlação 0.999
- `populacao_11_13` ↔ `populacao_5`: correlação 0.999
- `populacao_11_13` ↔ `populacao_6`: correlação 1.000
- `populacao_11_13` ↔ `populacao_6_10`: correlação 1.000
- `populacao_11_13` ↔ `populacao_6_17`: correlação 1.000
- `populacao_11_13` ↔ `populacao_65_mais`: correlação 0.969
- `populacao_11_13` ↔ `populacao`: correlação 0.997
- `populacao_11_13` ↔ `populacao_urbana`: correlação 0.996
- `populacao_11_13` ↔ `populacao_dom_pp`: correlação 0.997
- `populacao_11_13` ↔ `populacao_dom_pp_exc_renda_nula`: correlação 0.997
- `populacao_11_13` ↔ `pea`: correlação 0.995
- `populacao_11_13` ↔ `pea_10_14`: correlação 0.971
- `populacao_11_13` ↔ `pea_15_17`: correlação 0.979
- `populacao_11_13` ↔ `pea_18_mais`: correlação 0.994
- `populacao_11_13` ↔ `pia`: correlação 0.996
- `populacao_11_13` ↔ `pia_10_14`: correlação 1.000
- `populacao_11_13` ↔ `pia_15_17`: correlação 0.999
- `populacao_11_13` ↔ `pia_18_mais`: correlação 0.995
- `populacao_12_14` ↔ `populacao_1_3`: correlação 0.999
- `populacao_12_14` ↔ `populacao_15_mais`: correlação 0.995
- `populacao_12_14` ↔ `populacao_15_17`: correlação 1.000
- `populacao_12_14` ↔ `populacao_15_24`: correlação 0.999
- `populacao_12_14` ↔ `populacao_16_18`: correlação 0.999
- `populacao_12_14` ↔ `populacao_18_mais`: correlação 0.994
- `populacao_12_14` ↔ `populacao_18_20`: correlação 0.999
- `populacao_12_14` ↔ `populacao_18_24`: correlação 0.998
- `populacao_12_14` ↔ `populacao_19_21`: correlação 0.999
- `populacao_12_14` ↔ `populacao_25_mais`: correlação 0.993
- `populacao_12_14` ↔ `populacao_4`: correlação 0.999
- `populacao_12_14` ↔ `populacao_5`: correlação 0.999
- `populacao_12_14` ↔ `populacao_6`: correlação 0.999
- `populacao_12_14` ↔ `populacao_6_10`: correlação 1.000
- `populacao_12_14` ↔ `populacao_6_17`: correlação 1.000
- `populacao_12_14` ↔ `populacao_65_mais`: correlação 0.968
- `populacao_12_14` ↔ `populacao`: correlação 0.997
- `populacao_12_14` ↔ `populacao_urbana`: correlação 0.996
- `populacao_12_14` ↔ `populacao_dom_pp`: correlação 0.997
- `populacao_12_14` ↔ `populacao_dom_pp_exc_renda_nula`: correlação 0.997
- `populacao_12_14` ↔ `pea`: correlação 0.994
- `populacao_12_14` ↔ `pea_10_14`: correlação 0.971
- `populacao_12_14` ↔ `pea_15_17`: correlação 0.979
- `populacao_12_14` ↔ `pea_18_mais`: correlação 0.994
- `populacao_12_14` ↔ `pia`: correlação 0.996
- `populacao_12_14` ↔ `pia_10_14`: correlação 1.000
- `populacao_12_14` ↔ `pia_15_17`: correlação 1.000
- `populacao_12_14` ↔ `pia_18_mais`: correlação 0.994
- `populacao_1_3` ↔ `populacao_15_mais`: correlação 0.993
- `populacao_1_3` ↔ `populacao_15_17`: correlação 0.999
- `populacao_1_3` ↔ `populacao_15_24`: correlação 0.998
- `populacao_1_3` ↔ `populacao_16_18`: correlação 0.998
- `populacao_1_3` ↔ `populacao_18_mais`: correlação 0.992
- `populacao_1_3` ↔ `populacao_18_20`: correlação 0.998
- `populacao_1_3` ↔ `populacao_18_24`: correlação 0.998
- `populacao_1_3` ↔ `populacao_19_21`: correlação 0.998
- `populacao_1_3` ↔ `populacao_25_mais`: correlação 0.990
- `populacao_1_3` ↔ `populacao_4`: correlação 1.000
- `populacao_1_3` ↔ `populacao_5`: correlação 1.000
- `populacao_1_3` ↔ `populacao_6`: correlação 1.000
- `populacao_1_3` ↔ `populacao_6_10`: correlação 1.000
- `populacao_1_3` ↔ `populacao_6_17`: correlação 0.999
- `populacao_1_3` ↔ `populacao_65_mais`: correlação 0.962
- `populacao_1_3` ↔ `populacao`: correlação 0.995
- `populacao_1_3` ↔ `populacao_urbana`: correlação 0.993
- `populacao_1_3` ↔ `populacao_dom_pp`: correlação 0.995
- `populacao_1_3` ↔ `populacao_dom_pp_exc_renda_nula`: correlação 0.995
- `populacao_1_3` ↔ `pea`: correlação 0.993
- `populacao_1_3` ↔ `pea_10_14`: correlação 0.975
- `populacao_1_3` ↔ `pea_15_17`: correlação 0.980
- `populacao_1_3` ↔ `pea_18_mais`: correlação 0.992
- `populacao_1_3` ↔ `pia`: correlação 0.994
- `populacao_1_3` ↔ `pia_10_14`: correlação 0.999
- `populacao_1_3` ↔ `pia_15_17`: correlação 0.999
- `populacao_1_3` ↔ `pia_18_mais`: correlação 0.992
- `populacao_15_mais` ↔ `populacao_15_17`: correlação 0.995
- `populacao_15_mais` ↔ `populacao_15_24`: correlação 0.996
- `populacao_15_mais` ↔ `populacao_16_18`: correlação 0.994
- `populacao_15_mais` ↔ `populacao_18_mais`: correlação 1.000
- `populacao_15_mais` ↔ `populacao_18_20`: correlação 0.996
- `populacao_15_mais` ↔ `populacao_18_24`: correlação 0.996
- `populacao_15_mais` ↔ `populacao_19_21`: correlação 0.997
- `populacao_15_mais` ↔ `populacao_25_mais`: correlação 1.000
- `populacao_15_mais` ↔ `populacao_4`: correlação 0.993
- `populacao_15_mais` ↔ `populacao_5`: correlação 0.993
- `populacao_15_mais` ↔ `populacao_6`: correlação 0.993
- `populacao_15_mais` ↔ `populacao_6_10`: correlação 0.994
- `populacao_15_mais` ↔ `populacao_6_17`: correlação 0.995
- `populacao_15_mais` ↔ `populacao_65_mais`: correlação 0.985
- `populacao_15_mais` ↔ `populacao`: correlação 1.000
- `populacao_15_mais` ↔ `populacao_urbana`: correlação 1.000
- `populacao_15_mais` ↔ `populacao_dom_pp`: correlação 1.000
- `populacao_15_mais` ↔ `populacao_dom_pp_exc_renda_nula`: correlação 1.000
- `populacao_15_mais` ↔ `pea`: correlação 0.999
- `populacao_15_mais` ↔ `pea_10_14`: correlação 0.957
- `populacao_15_mais` ↔ `pea_15_17`: correlação 0.973
- `populacao_15_mais` ↔ `pea_18_mais`: correlação 0.999
- `populacao_15_mais` ↔ `pia`: correlação 1.000
- `populacao_15_mais` ↔ `pia_10_14`: correlação 0.995
- `populacao_15_mais` ↔ `pia_15_17`: correlação 0.995
- `populacao_15_mais` ↔ `pia_18_mais`: correlação 1.000
- `populacao_15_17` ↔ `populacao_15_24`: correlação 0.999
- `populacao_15_17` ↔ `populacao_16_18`: correlação 1.000
- `populacao_15_17` ↔ `populacao_18_mais`: correlação 0.994
- `populacao_15_17` ↔ `populacao_18_20`: correlação 0.999
- `populacao_15_17` ↔ `populacao_18_24`: correlação 0.999
- `populacao_15_17` ↔ `populacao_19_21`: correlação 0.999
- `populacao_15_17` ↔ `populacao_25_mais`: correlação 0.992
- `populacao_15_17` ↔ `populacao_4`: correlação 0.998
- `populacao_15_17` ↔ `populacao_5`: correlação 0.998
- `populacao_15_17` ↔ `populacao_6`: correlação 0.999
- `populacao_15_17` ↔ `populacao_6_10`: correlação 0.999
- `populacao_15_17` ↔ `populacao_6_17`: correlação 1.000
- `populacao_15_17` ↔ `populacao_65_mais`: correlação 0.967
- `populacao_15_17` ↔ `populacao`: correlação 0.997
- `populacao_15_17` ↔ `populacao_urbana`: correlação 0.995
- `populacao_15_17` ↔ `populacao_dom_pp`: correlação 0.997
- `populacao_15_17` ↔ `populacao_dom_pp_exc_renda_nula`: correlação 0.996
- `populacao_15_17` ↔ `pea`: correlação 0.994
- `populacao_15_17` ↔ `pea_10_14`: correlação 0.970
- `populacao_15_17` ↔ `pea_15_17`: correlação 0.978
- `populacao_15_17` ↔ `pea_18_mais`: correlação 0.994
- `populacao_15_17` ↔ `pia`: correlação 0.995
- `populacao_15_17` ↔ `pia_10_14`: correlação 0.999
- `populacao_15_17` ↔ `pia_15_17`: correlação 1.000
- `populacao_15_17` ↔ `pia_18_mais`: correlação 0.994
- `populacao_15_24` ↔ `populacao_16_18`: correlação 1.000
- `populacao_15_24` ↔ `populacao_18_mais`: correlação 0.996
- `populacao_15_24` ↔ `populacao_18_20`: correlação 1.000
- `populacao_15_24` ↔ `populacao_18_24`: correlação 1.000
- `populacao_15_24` ↔ `populacao_19_21`: correlação 1.000
- `populacao_15_24` ↔ `populacao_25_mais`: correlação 0.994
- `populacao_15_24` ↔ `populacao_4`: correlação 0.998
- `populacao_15_24` ↔ `populacao_5`: correlação 0.998
- `populacao_15_24` ↔ `populacao_6`: correlação 0.998
- `populacao_15_24` ↔ `populacao_6_10`: correlação 0.998
- `populacao_15_24` ↔ `populacao_6_17`: correlação 0.999
- `populacao_15_24` ↔ `populacao_65_mais`: correlação 0.969
- `populacao_15_24` ↔ `populacao`: correlação 0.998
- `populacao_15_24` ↔ `populacao_urbana`: correlação 0.997
- `populacao_15_24` ↔ `populacao_dom_pp`: correlação 0.998
- `populacao_15_24` ↔ `populacao_dom_pp_exc_renda_nula`: correlação 0.998
- `populacao_15_24` ↔ `pea`: correlação 0.996
- `populacao_15_24` ↔ `pea_10_14`: correlação 0.969
- `populacao_15_24` ↔ `pea_15_17`: correlação 0.980
- `populacao_15_24` ↔ `pea_18_mais`: correlação 0.996
- `populacao_15_24` ↔ `pia`: correlação 0.997
- `populacao_15_24` ↔ `pia_10_14`: correlação 0.999
- `populacao_15_24` ↔ `pia_15_17`: correlação 0.999
- `populacao_15_24` ↔ `pia_18_mais`: correlação 0.996
- `populacao_16_18` ↔ `populacao_18_mais`: correlação 0.994
- `populacao_16_18` ↔ `populacao_18_20`: correlação 1.000
- `populacao_16_18` ↔ `populacao_18_24`: correlação 0.999
- `populacao_16_18` ↔ `populacao_19_21`: correlação 0.999
- `populacao_16_18` ↔ `populacao_25_mais`: correlação 0.992
- `populacao_16_18` ↔ `populacao_4`: correlação 0.998
- `populacao_16_18` ↔ `populacao_5`: correlação 0.998
- `populacao_16_18` ↔ `populacao_6`: correlação 0.998
- `populacao_16_18` ↔ `populacao_6_10`: correlação 0.999
- `populacao_16_18` ↔ `populacao_6_17`: correlação 0.999
- `populacao_16_18` ↔ `populacao_65_mais`: correlação 0.966
- `populacao_16_18` ↔ `populacao`: correlação 0.996
- `populacao_16_18` ↔ `populacao_urbana`: correlação 0.995
- `populacao_16_18` ↔ `populacao_dom_pp`: correlação 0.996
- `populacao_16_18` ↔ `populacao_dom_pp_exc_renda_nula`: correlação 0.996
- `populacao_16_18` ↔ `pea`: correlação 0.994
- `populacao_16_18` ↔ `pea_10_14`: correlação 0.970
- `populacao_16_18` ↔ `pea_15_17`: correlação 0.978
- `populacao_16_18` ↔ `pea_18_mais`: correlação 0.994
- `populacao_16_18` ↔ `pia`: correlação 0.995
- `populacao_16_18` ↔ `pia_10_14`: correlação 0.999
- `populacao_16_18` ↔ `pia_15_17`: correlação 1.000
- `populacao_16_18` ↔ `pia_18_mais`: correlação 0.994
- `populacao_18_mais` ↔ `populacao_18_20`: correlação 0.996
- `populacao_18_mais` ↔ `populacao_18_24`: correlação 0.996
- `populacao_18_mais` ↔ `populacao_19_21`: correlação 0.996
- `populacao_18_mais` ↔ `populacao_25_mais`: correlação 1.000
- `populacao_18_mais` ↔ `populacao_4`: correlação 0.992
- `populacao_18_mais` ↔ `populacao_5`: correlação 0.992
- `populacao_18_mais` ↔ `populacao_6`: correlação 0.993
- `populacao_18_mais` ↔ `populacao_6_10`: correlação 0.993
- `populacao_18_mais` ↔ `populacao_6_17`: correlação 0.994
- `populacao_18_mais` ↔ `populacao_65_mais`: correlação 0.986
- `populacao_18_mais` ↔ `populacao`: correlação 1.000
- `populacao_18_mais` ↔ `populacao_urbana`: correlação 0.999
- `populacao_18_mais` ↔ `populacao_dom_pp`: correlação 1.000
- `populacao_18_mais` ↔ `populacao_dom_pp_exc_renda_nula`: correlação 1.000
- `populacao_18_mais` ↔ `pea`: correlação 0.999
- `populacao_18_mais` ↔ `pea_10_14`: correlação 0.955
- `populacao_18_mais` ↔ `pea_15_17`: correlação 0.972
- `populacao_18_mais` ↔ `pea_18_mais`: correlação 0.999
- `populacao_18_mais` ↔ `pia`: correlação 1.000
- `populacao_18_mais` ↔ `pia_10_14`: correlação 0.995
- `populacao_18_mais` ↔ `pia_15_17`: correlação 0.994
- `populacao_18_mais` ↔ `pia_18_mais`: correlação 1.000
- `populacao_18_20` ↔ `populacao_18_24`: correlação 1.000
- `populacao_18_20` ↔ `populacao_19_21`: correlação 1.000
- `populacao_18_20` ↔ `populacao_25_mais`: correlação 0.994
- `populacao_18_20` ↔ `populacao_4`: correlação 0.998
- `populacao_18_20` ↔ `populacao_5`: correlação 0.998
- `populacao_18_20` ↔ `populacao_6`: correlação 0.998
- `populacao_18_20` ↔ `populacao_6_10`: correlação 0.998
- `populacao_18_20` ↔ `populacao_6_17`: correlação 0.999
- `populacao_18_20` ↔ `populacao_65_mais`: correlação 0.970
- `populacao_18_20` ↔ `populacao`: correlação 0.998
- `populacao_18_20` ↔ `populacao_urbana`: correlação 0.996
- `populacao_18_20` ↔ `populacao_dom_pp`: correlação 0.998
- `populacao_18_20` ↔ `populacao_dom_pp_exc_renda_nula`: correlação 0.998
- `populacao_18_20` ↔ `pea`: correlação 0.996
- `populacao_18_20` ↔ `pea_10_14`: correlação 0.968
- `populacao_18_20` ↔ `pea_15_17`: correlação 0.979
- `populacao_18_20` ↔ `pea_18_mais`: correlação 0.996
- `populacao_18_20` ↔ `pia`: correlação 0.997
- `populacao_18_20` ↔ `pia_10_14`: correlação 0.999
- `populacao_18_20` ↔ `pia_15_17`: correlação 0.999
- `populacao_18_20` ↔ `pia_18_mais`: correlação 0.996
- `populacao_18_24` ↔ `populacao_19_21`: correlação 1.000
- `populacao_18_24` ↔ `populacao_25_mais`: correlação 0.994
- `populacao_18_24` ↔ `populacao_4`: correlação 0.997
- `populacao_18_24` ↔ `populacao_5`: correlação 0.997
- `populacao_18_24` ↔ `populacao_6`: correlação 0.998
- `populacao_18_24` ↔ `populacao_6_10`: correlação 0.998
- `populacao_18_24` ↔ `populacao_6_17`: correlação 0.998
- `populacao_18_24` ↔ `populacao_65_mais`: correlação 0.969
- `populacao_18_24` ↔ `populacao`: correlação 0.998
- `populacao_18_24` ↔ `populacao_urbana`: correlação 0.997
- `populacao_18_24` ↔ `populacao_dom_pp`: correlação 0.998
- `populacao_18_24` ↔ `populacao_dom_pp_exc_renda_nula`: correlação 0.998
- `populacao_18_24` ↔ `pea`: correlação 0.997
- `populacao_18_24` ↔ `pea_10_14`: correlação 0.969
- `populacao_18_24` ↔ `pea_15_17`: correlação 0.981
- `populacao_18_24` ↔ `pea_18_mais`: correlação 0.997
- `populacao_18_24` ↔ `pia`: correlação 0.997
- `populacao_18_24` ↔ `pia_10_14`: correlação 0.998
- `populacao_18_24` ↔ `pia_15_17`: correlação 0.999
- `populacao_18_24` ↔ `pia_18_mais`: correlação 0.996
- `populacao_19_21` ↔ `populacao_25_mais`: correlação 0.995
- `populacao_19_21` ↔ `populacao_4`: correlação 0.997
- `populacao_19_21` ↔ `populacao_5`: correlação 0.997
- `populacao_19_21` ↔ `populacao_6`: correlação 0.998
- `populacao_19_21` ↔ `populacao_6_10`: correlação 0.998
- `populacao_19_21` ↔ `populacao_6_17`: correlação 0.998
- `populacao_19_21` ↔ `populacao_65_mais`: correlação 0.971
- `populacao_19_21` ↔ `populacao`: correlação 0.998
- `populacao_19_21` ↔ `populacao_urbana`: correlação 0.997
- `populacao_19_21` ↔ `populacao_dom_pp`: correlação 0.998
- `populacao_19_21` ↔ `populacao_dom_pp_exc_renda_nula`: correlação 0.998
- `populacao_19_21` ↔ `pea`: correlação 0.997
- `populacao_19_21` ↔ `pea_10_14`: correlação 0.968
- `populacao_19_21` ↔ `pea_15_17`: correlação 0.980
- `populacao_19_21` ↔ `pea_18_mais`: correlação 0.997
- `populacao_19_21` ↔ `pia`: correlação 0.997
- `populacao_19_21` ↔ `pia_10_14`: correlação 0.998
- `populacao_19_21` ↔ `pia_15_17`: correlação 0.999
- `populacao_19_21` ↔ `pia_18_mais`: correlação 0.996
- `populacao_25_mais` ↔ `populacao_4`: correlação 0.990
- `populacao_25_mais` ↔ `populacao_5`: correlação 0.990
- `populacao_25_mais` ↔ `populacao_6`: correlação 0.991
- `populacao_25_mais` ↔ `populacao_6_10`: correlação 0.992
- `populacao_25_mais` ↔ `populacao_6_17`: correlação 0.992
- `populacao_25_mais` ↔ `populacao_65_mais`: correlação 0.988
- `populacao_25_mais` ↔ `populacao`: correlação 0.999
- `populacao_25_mais` ↔ `populacao_urbana`: correlação 0.999
- `populacao_25_mais` ↔ `populacao_dom_pp`: correlação 0.999
- `populacao_25_mais` ↔ `populacao_dom_pp_exc_renda_nula`: correlação 0.999
- `populacao_25_mais` ↔ `pea`: correlação 0.999
- `populacao_25_mais` ↔ `pea_10_14`: correlação 0.952
- `populacao_25_mais` ↔ `pea_15_17`: correlação 0.969
- `populacao_25_mais` ↔ `pea_18_mais`: correlação 0.999
- `populacao_25_mais` ↔ `pia`: correlação 1.000
- `populacao_25_mais` ↔ `pia_10_14`: correlação 0.993
- `populacao_25_mais` ↔ `pia_15_17`: correlação 0.992
- `populacao_25_mais` ↔ `pia_18_mais`: correlação 1.000
- `populacao_4` ↔ `populacao_5`: correlação 1.000
- `populacao_4` ↔ `populacao_6`: correlação 1.000
- `populacao_4` ↔ `populacao_6_10`: correlação 1.000
- `populacao_4` ↔ `populacao_6_17`: correlação 0.999
- `populacao_4` ↔ `populacao_65_mais`: correlação 0.963
- `populacao_4` ↔ `populacao`: correlação 0.995
- `populacao_4` ↔ `populacao_urbana`: correlação 0.993
- `populacao_4` ↔ `populacao_dom_pp`: correlação 0.995
- `populacao_4` ↔ `populacao_dom_pp_exc_renda_nula`: correlação 0.995
- `populacao_4` ↔ `pea`: correlação 0.993
- `populacao_4` ↔ `pea_10_14`: correlação 0.974
- `populacao_4` ↔ `pea_15_17`: correlação 0.981
- `populacao_4` ↔ `pea_18_mais`: correlação 0.992
- `populacao_4` ↔ `pia`: correlação 0.994
- `populacao_4` ↔ `pia_10_14`: correlação 0.999
- `populacao_4` ↔ `pia_15_17`: correlação 0.998
- `populacao_4` ↔ `pia_18_mais`: correlação 0.992
- `populacao_5` ↔ `populacao_6`: correlação 1.000
- `populacao_5` ↔ `populacao_6_10`: correlação 1.000
- `populacao_5` ↔ `populacao_6_17`: correlação 1.000
- `populacao_5` ↔ `populacao_65_mais`: correlação 0.964
- `populacao_5` ↔ `populacao`: correlação 0.995
- `populacao_5` ↔ `populacao_urbana`: correlação 0.994
- `populacao_5` ↔ `populacao_dom_pp`: correlação 0.995
- `populacao_5` ↔ `populacao_dom_pp_exc_renda_nula`: correlação 0.995
- `populacao_5` ↔ `pea`: correlação 0.993
- `populacao_5` ↔ `pea_10_14`: correlação 0.974
- `populacao_5` ↔ `pea_15_17`: correlação 0.980
- `populacao_5` ↔ `pea_18_mais`: correlação 0.993
- `populacao_5` ↔ `pia`: correlação 0.994
- `populacao_5` ↔ `pia_10_14`: correlação 0.999
- `populacao_5` ↔ `pia_15_17`: correlação 0.998
- `populacao_5` ↔ `pia_18_mais`: correlação 0.992
- `populacao_6` ↔ `populacao_6_10`: correlação 1.000
- `populacao_6` ↔ `populacao_6_17`: correlação 1.000
- `populacao_6` ↔ `populacao_65_mais`: correlação 0.964
- `populacao_6` ↔ `populacao`: correlação 0.996
- `populacao_6` ↔ `populacao_urbana`: correlação 0.994
- `populacao_6` ↔ `populacao_dom_pp`: correlação 0.996
- `populacao_6` ↔ `populacao_dom_pp_exc_renda_nula`: correlação 0.996
- `populacao_6` ↔ `pea`: correlação 0.993
- `populacao_6` ↔ `pea_10_14`: correlação 0.974
- `populacao_6` ↔ `pea_15_17`: correlação 0.980
- `populacao_6` ↔ `pea_18_mais`: correlação 0.993
- `populacao_6` ↔ `pia`: correlação 0.994
- `populacao_6` ↔ `pia_10_14`: correlação 1.000
- `populacao_6` ↔ `pia_15_17`: correlação 0.999
- `populacao_6` ↔ `pia_18_mais`: correlação 0.993
- `populacao_6_10` ↔ `populacao_6_17`: correlação 1.000
- `populacao_6_10` ↔ `populacao_65_mais`: correlação 0.966
- `populacao_6_10` ↔ `populacao`: correlação 0.996
- `populacao_6_10` ↔ `populacao_urbana`: correlação 0.995
- `populacao_6_10` ↔ `populacao_dom_pp`: correlação 0.996
- `populacao_6_10` ↔ `populacao_dom_pp_exc_renda_nula`: correlação 0.996
- `populacao_6_10` ↔ `pea`: correlação 0.994
- `populacao_6_10` ↔ `pea_10_14`: correlação 0.973
- `populacao_6_10` ↔ `pea_15_17`: correlação 0.979
- `populacao_6_10` ↔ `pea_18_mais`: correlação 0.993
- `populacao_6_10` ↔ `pia`: correlação 0.995
- `populacao_6_10` ↔ `pia_10_14`: correlação 1.000
- `populacao_6_10` ↔ `pia_15_17`: correlação 0.999
- `populacao_6_10` ↔ `pia_18_mais`: correlação 0.993
- `populacao_6_17` ↔ `populacao_65_mais`: correlação 0.967
- `populacao_6_17` ↔ `populacao`: correlação 0.997
- `populacao_6_17` ↔ `populacao_urbana`: correlação 0.995
- `populacao_6_17` ↔ `populacao_dom_pp`: correlação 0.997
- `populacao_6_17` ↔ `populacao_dom_pp_exc_renda_nula`: correlação 0.997
- `populacao_6_17` ↔ `pea`: correlação 0.994
- `populacao_6_17` ↔ `pea_10_14`: correlação 0.972
- `populacao_6_17` ↔ `pea_15_17`: correlação 0.979
- `populacao_6_17` ↔ `pea_18_mais`: correlação 0.994
- `populacao_6_17` ↔ `pia`: correlação 0.996
- `populacao_6_17` ↔ `pia_10_14`: correlação 1.000
- `populacao_6_17` ↔ `pia_15_17`: correlação 1.000
- `populacao_6_17` ↔ `pia_18_mais`: correlação 0.994
- `populacao_65_mais` ↔ `populacao`: correlação 0.982
- `populacao_65_mais` ↔ `populacao_urbana`: correlação 0.983
- `populacao_65_mais` ↔ `populacao_dom_pp`: correlação 0.982
- `populacao_65_mais` ↔ `populacao_dom_pp_exc_renda_nula`: correlação 0.982
- `populacao_65_mais` ↔ `pea`: correlação 0.980
- `populacao_65_mais` ↔ `pea_10_14`: correlação 0.912
- `populacao_65_mais` ↔ `pea_15_17`: correlação 0.930
- `populacao_65_mais` ↔ `pea_18_mais`: correlação 0.981
- `populacao_65_mais` ↔ `pia`: correlação 0.984
- `populacao_65_mais` ↔ `pia_10_14`: correlação 0.968
- `populacao_65_mais` ↔ `pia_15_17`: correlação 0.967
- `populacao_65_mais` ↔ `pia_18_mais`: correlação 0.986
- `populacao` ↔ `populacao_urbana`: correlação 0.999
- `populacao` ↔ `populacao_dom_pp`: correlação 1.000
- `populacao` ↔ `populacao_dom_pp_exc_renda_nula`: correlação 1.000
- `populacao` ↔ `pea`: correlação 0.999
- `populacao` ↔ `pea_10_14`: correlação 0.961
- `populacao` ↔ `pea_15_17`: correlação 0.975
- `populacao` ↔ `pea_18_mais`: correlação 0.999
- `populacao` ↔ `pia`: correlação 1.000
- `populacao` ↔ `pia_10_14`: correlação 0.997
- `populacao` ↔ `pia_15_17`: correlação 0.997
- `populacao` ↔ `pia_18_mais`: correlação 1.000
- `populacao_urbana` ↔ `populacao_dom_pp`: correlação 0.999
- `populacao_urbana` ↔ `populacao_dom_pp_exc_renda_nula`: correlação 1.000
- `populacao_urbana` ↔ `pea`: correlação 0.999
- `populacao_urbana` ↔ `pea_10_14`: correlação 0.956
- `populacao_urbana` ↔ `pea_15_17`: correlação 0.973
- `populacao_urbana` ↔ `pea_18_mais`: correlação 0.999
- `populacao_urbana` ↔ `pia`: correlação 1.000
- `populacao_urbana` ↔ `pia_10_14`: correlação 0.996
- `populacao_urbana` ↔ `pia_15_17`: correlação 0.995
- `populacao_urbana` ↔ `pia_18_mais`: correlação 0.999
- `populacao_dom_pp` ↔ `populacao_dom_pp_exc_renda_nula`: correlação 1.000
- `populacao_dom_pp` ↔ `pea`: correlação 0.999
- `populacao_dom_pp` ↔ `pea_10_14`: correlação 0.961
- `populacao_dom_pp` ↔ `pea_15_17`: correlação 0.975
- `populacao_dom_pp` ↔ `pea_18_mais`: correlação 0.999
- `populacao_dom_pp` ↔ `pia`: correlação 1.000
- `populacao_dom_pp` ↔ `pia_10_14`: correlação 0.997
- `populacao_dom_pp` ↔ `pia_15_17`: correlação 0.997
- `populacao_dom_pp` ↔ `pia_18_mais`: correlação 1.000
- `populacao_dom_pp_exc_renda_nula` ↔ `pea`: correlação 0.999
- `populacao_dom_pp_exc_renda_nula` ↔ `pea_10_14`: correlação 0.961
- `populacao_dom_pp_exc_renda_nula` ↔ `pea_15_17`: correlação 0.975
- `populacao_dom_pp_exc_renda_nula` ↔ `pea_18_mais`: correlação 0.999
- `populacao_dom_pp_exc_renda_nula` ↔ `pia`: correlação 1.000
- `populacao_dom_pp_exc_renda_nula` ↔ `pia_10_14`: correlação 0.997
- `populacao_dom_pp_exc_renda_nula` ↔ `pia_15_17`: correlação 0.996
- `populacao_dom_pp_exc_renda_nula` ↔ `pia_18_mais`: correlação 1.000
- `pea` ↔ `pea_10_14`: correlação 0.961
- `pea` ↔ `pea_15_17`: correlação 0.980
- `pea` ↔ `pea_18_mais`: correlação 1.000
- `pea` ↔ `pia`: correlação 0.999
- `pea` ↔ `pia_10_14`: correlação 0.994
- `pea` ↔ `pia_15_17`: correlação 0.994
- `pea` ↔ `pia_18_mais`: correlação 0.999
- `pea_10_14` ↔ `pea_15_17`: correlação 0.977
- `pea_10_14` ↔ `pea_18_mais`: correlação 0.959
- `pea_10_14` ↔ `pia`: correlação 0.958
- `pea_10_14` ↔ `pia_10_14`: correlação 0.971
- `pea_10_14` ↔ `pia_15_17`: correlação 0.970
- `pea_10_14` ↔ `pia_18_mais`: correlação 0.955
- `pea_15_17` ↔ `pea_18_mais`: correlação 0.979
- `pea_15_17` ↔ `pia`: correlação 0.974
- `pea_15_17` ↔ `pia_10_14`: correlação 0.978
- `pea_15_17` ↔ `pia_15_17`: correlação 0.978
- `pea_15_17` ↔ `pia_18_mais`: correlação 0.972
- `pea_18_mais` ↔ `pia`: correlação 0.999
- `pea_18_mais` ↔ `pia_10_14`: correlação 0.994
- `pea_18_mais` ↔ `pia_15_17`: correlação 0.994
- `pea_18_mais` ↔ `pia_18_mais`: correlação 0.999
- `pia` ↔ `pia_10_14`: correlação 0.996
- `pia` ↔ `pia_15_17`: correlação 0.995
- `pia` ↔ `pia_18_mais`: correlação 1.000
- `pia_10_14` ↔ `pia_15_17`: correlação 0.999
- `pia_10_14` ↔ `pia_18_mais`: correlação 0.995
- `pia_15_17` ↔ `pia_18_mais`: correlação 0.994
- `indice_frequencia_escolar` ↔ `idhm_e`: correlação 0.913
- `idhm` ↔ `idhm_e`: correlação 0.951
- `idhm` ↔ `idhm_r`: correlação 0.948

### 8. Relação de cada coluna com o alvo

- Coluna `alfabetizado` ausente neste dataset.

### 9. A NULIDADE de cada coluna prediz o alvo? (item novo — não estava no checklist)

Item acrescentado em 2026-08-18. O item 6 conta nulos mas nunca os cruza com o alvo — e foi por essa fresta que `peso_aluno` passou: 835 nulos que eram os alunos ausentes, todos com alvo "Não". Ver Cap. 9 do diário de bordo interno (não publicado).

- Sem alvo neste dataset, item não aplicável.

## Contexto estrutural (não é gate, mas decide o que é possível)

- **municípios**: 5.565 · 1.00 alunos por município · 100.0% com 1 aluno só
- **anos**: [2010]
