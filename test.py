import pandas as pd
from api.sinasc import obter_taxa_sinasc
import matplotlib.pyplot as plt
from api.analysis.trends import calcular_regressao_linear, calcular_mann_kendall
from api.viz.trends import plotar_grafico_tendencia, plotar_grade_tendencia
from api.analysis.spatial import criar_matriz_vizinhanca, calcular_moran_global, calcular_lisa_local
from api.viz.maps import plotar_mapa_coropletico

# Definir parâmetros da análise
anos = list(range(2015, 2025))
cid_prefixo = 'Q' # Todas as anomalias congênitas

print(f"Analisando o período de {anos[0]} a {anos[-1]} para o CID '{cid_prefixo}'...")

# Obter taxas agregadas por região e ano
taxas_regionais = obter_taxa_sinasc(
    anos=anos,
    cid=cid_prefixo,
    estratos=['REGIAO'],
    retorno='polars'
).to_pandas()

# O nome da coluna de taxa agora depende do multiplicador (padrão 100000)
col_taxa = "taxa_por_100000"

print(f"\nTaxas de prevalência por 100.000 nascidos vivos (por Região e Ano):")
print(taxas_regionais.head())

# Pivotar a tabela para o formato de série temporal (índex=Região, colunas=Anos)
tabela_temporal = taxas_regionais.pivot(
    index="REGIAO",
    columns="ano",
    values=col_taxa
)

print(f"\nTabela de Séries Temporais ({col_taxa}):")
print(tabela_temporal)

# Aplicar os testes de tendência
resultados_regressao = calcular_regressao_linear(tabela_temporal)
resultados_mk = calcular_mann_kendall(tabela_temporal)

print("\nResultados da Regressão Linear por Região:")
print(resultados_regressao)

print("\nResultados do Teste de Mann-Kendall por Região:")
print(resultados_mk)

titulo_grafico = f"Prevalência de Anomalias Congênitas por Região ({anos[0]}-{anos[-1]})"

# Gráfico com todas as regiões juntas
plotar_grafico_tendencia(tabela_temporal, titulo_grafico)
# plt.show() # Removido para não bloquear a execução se rodar via CLI

# Grade de gráficos com linha de tendência
plotar_grade_tendencia(tabela_temporal, resultados_regressao, titulo_grafico)
# plt.show()

anos_espacial = [2015, 2020, 2024]

for ano in anos_espacial:
    print(f"\n--- Iniciando análise espacial para o ano de {ano}... ---")

    gdf = obter_taxa_sinasc(
        anos=[ano],
        cid=cid_prefixo,
        estratos=["codmunres"],
        retorno="geopandas"
    )

    gdf_analise = gdf[gdf['n_nascidos_vivos'].notna()].copy()
    print(f"{len(gdf_analise)} municípios com dados encontrados.")

    if not gdf_analise.empty:
        w = criar_matriz_vizinhanca(gdf_analise, metodo="queen")

        moran_i, moran_p = calcular_moran_global(gdf_analise, col_taxa, w)
        print(f"I de Moran Global ({ano}): {moran_i:.4f} (p-valor: {moran_p:.4f})")

        gdf_lisa = calcular_lisa_local(gdf_analise, col_taxa, w)

        print(f"Contagem de clusters LISA ({ano}):")
        print(gdf_lisa["lisa_cluster"].value_counts())

        fig, axes = plt.subplots(1, 2, figsize=(18, 8))

        plotar_mapa_coropletico(
            gdf_lisa,
            coluna=col_taxa,
            ax=axes[0],
            titulo_legenda="Taxa por 100k (Quartis)"
        )
        axes[0].set_title(f"Mapa de Taxa Bruta por Município ({ano})")
        axes[0].axis('off')

        cluster_colors = {
            'Não significante': 'lightgrey',
            'Alto-Alto': '#d7191c',
            'Baixo-Baixo': '#2c7bb6',
            'Baixo-Alto': '#abd9e9',
            'Alto-Baixo': '#fdae61'
        }

        # Mapeamento manual de cores para o plot do Geopandas
        gdf_lisa.plot(
            column='lisa_cluster',
            categorical=True,
            legend=True,
            legend_kwds={'title': "Clusters LISA", 'loc': 'lower right'},
            ax=axes[1],
            edgecolor='white',
            linewidth=0.1,
            # Note: passed colors must match the order of categories if using categorical
        )
        axes[1].set_title(f"Mapa de Clusters LISA ({ano})")
        axes[1].axis('off')

        plt.tight_layout()
        # plt.show()
    else:
        print("Nenhum dado para plotar os mapas.")