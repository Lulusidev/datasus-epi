import libpysal
import numpy as np
from esda.moran import Moran
from esda.moran import Moran_Local
from esda.smoothing import Empirical_Bayes
import pandas as pd
import geopandas as gpd
import geobr

def criar_matriz_vizinhanca(
    gdf,
    metodo: str = "queen",
    k: int = 8
):
    """
    Cria matriz de vizinhança espacial

    metodo:
        - 'queen' : contiguidade
        - 'knn'   : k-vizinhos mais próximos
    """

    if metodo == "queen":
        w = libpysal.weights.Queen.from_dataframe(gdf, use_index=True)
    elif metodo == "knn":
        w = libpysal.weights.KNN.from_dataframe(gdf, k=k, use_index=True)
    else:
        raise ValueError("metodo deve ser 'queen' ou 'knn'")

    w.transform = "r"  # row-standardized
    return w



def moran_global(
    gdf,
    coluna: str,
    w
):
    """
    Calcula Moran Global
    """
    valores = gdf[coluna].fillna(0).values
    mi = Moran(valores, w)

    return mi.I, mi.p_sim

def lisa_local(
    gdf,
    coluna: str,
    w
):
    """
    Calcula LISA (Moran Local)
    """
    valores = gdf[coluna].fillna(0).values
    lisa = Moran_Local(valores, w)

    # Identificar clusters significantes (p < 0.05)
    sig = lisa.p_sim < 0.05
    
    # Categorias de clusters (conforme seu notebook)
    categories = {
        1: 'HH',  # Alto-Alto
        2: 'LH',  # Baixo-Alto
        3: 'LL',  # Baixo-Baixo
        4: 'HL'   # Alto-Baixo
    }
    
    gdf['lisa_cluster'] = 'Não significante'
    gdf.loc[sig, 'lisa_cluster'] = [categories[q] for q in lisa.q[sig]]

    return gdf

def suavizar_taxa_empirical_bayes(
    gdf,
    casos: str,
    populacao: str,
    nome_saida: str = "taxa_suavizada"
):
    """
    Suavização Empirical Bayes clássica
    """
    # Tratamento para evitar divisão por zero
    pop_vals = gdf[populacao].fillna(0).values
    pop_vals = np.where(pop_vals == 0, 1, pop_vals)

    eb = Empirical_Bayes(
        gdf[casos].fillna(0).values,
        pop_vals
    )

    # Multiplica por 100.000 para manter a escala da taxa (por 100k habitantes)
    gdf[nome_saida] = eb.r * 100000
    return gdf


def obter_malha_municipal(
    ano: int = 2022,
    simplificada: bool = True
) -> gpd.GeoDataFrame:
    """
    Baixa (ou carrega do cache) a malha municipal do IBGE.
    """
    gdf = geobr.read_municipality(
        year=ano,
        simplified=simplificada
    )

    # Padronização de colunas
    gdf["code_muni"] = gdf["code_muni"].astype(str)

    return gdf

def juntar_geometria(
    df,
    coluna_codigo: str = "CODMUNRES",
    ano_malha: int = 2022
):
    """
    Junta tabela SINASC agregada à malha municipal ou estadual.
    """
    
    if coluna_codigo not in df.columns:
        raise KeyError(f"A coluna '{coluna_codigo}' não foi encontrada no DataFrame. Colunas disponíveis: {list(df.columns)}")
    
    # Lógica para Estados (UF)
    if coluna_codigo in ["CODUFRES", "UFINFORM"]:
        gdf_shape = geobr.read_state(year=ano_malha, simplified=True)
        col_geo = "code_state"
        
        # Padronização
        gdf_shape[col_geo] = gdf_shape[col_geo].astype(str)
        df[coluna_codigo] = df[coluna_codigo].astype(str)
        
        gdf = gdf_shape.merge(
            df,
            left_on=col_geo,
            right_on=coluna_codigo,
            how="left"
        )
        return gdf

    # Lógica para Municípios (Padrão)
    gdf_shape = obter_malha_municipal(ano=ano_malha)

    # Padronizar para 6 dígitos para garantir o cruzamento (SINASC costuma ser 6, Geobr 7)
    df[coluna_codigo] = df[coluna_codigo].astype(str)
    df["_cod_join"] = df[coluna_codigo].str.slice(0, 6)
    
    gdf_shape["code_muni"] = gdf_shape["code_muni"].astype(str)
    gdf_shape["_cod_join"] = gdf_shape["code_muni"].str.slice(0, 6)

    # DEBUG: Verificar códigos antes do merge
    print(f"--- DEBUG JUNTAR GEOMETRIA ---")
    print(f"Malha (geobr) - Primeiros 5 códigos: {gdf_shape['_cod_join'].head().tolist()}")
    print(f"Dados (SINASC) - Primeiros 5 códigos: {df['_cod_join'].head().tolist()}")
    print(f"Total Malha: {len(gdf_shape)} | Total Dados: {len(df)}")

    gdf = gdf_shape.merge(
        df,
        on="_cod_join",
        how="left"
    )
    
    # Remover coluna auxiliar se desejar, ou manter para debug
    # del gdf["_cod_join"]

    return gdf

def plotar_mapa_quartis(
    gdf,
    coluna: str,
    ax,
    cmap: str = "YlOrRd",
    titulo_legenda: str = "Quartis",
    fmt: str = "{:.1f}"
):
    """
    Plota mapa coroplético estático usando quartis.
    """
    gdf.plot(
        column=coluna,
        cmap=cmap,
        scheme="quantiles",
        k=4,
        legend=True,
        legend_kwds={'loc': 'lower right', 'title': titulo_legenda, 'fmt': fmt},
        edgecolor='black',
        linewidth=0.1,
        ax=ax
    )
