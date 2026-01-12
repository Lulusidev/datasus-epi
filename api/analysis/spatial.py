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
    Cria uma matriz de vizinhança espacial.

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



def calcular_moran_global(
    gdf,
    coluna: str,
    w
):
    """
    Calcula o I de Moran Global.
    """
    values = gdf[coluna].fillna(0).values
    mi = Moran(values, w)

    return mi.I, mi.p_sim

def calcular_lisa_local(
    gdf,
    coluna: str,
    w
):
    """
    Calcula o LISA (Moran Local).
    """
    values = gdf[coluna].values
    lisa = Moran_Local(values, w)

    # Identificar clusters significantes (p < 0.05)
    sig = lisa.p_sim < 0.05
    
    # Categorias de clusters
    categories = {
        1: 'Alto-Alto',
        2: 'Baixo-Alto',
        3: 'Baixo-Baixo',
        4: 'Alto-Baixo'
    }
    
    gdf['lisa_cluster'] = 'Não significante'
    gdf.loc[sig, 'lisa_cluster'] = [categories[q] for q in lisa.q[sig]]

    return gdf

def suavizar_taxa(
    gdf,
    coluna_casos: str,
    coluna_populacao: str,
    nome_saida: str = "taxa_suavizada"
):
    """
    Suavização Bayesiana Empírica clássica.
    """
    # Tratamento para evitar divisão por zero
    pop_vals = gdf[coluna_populacao].fillna(0).values
    pop_vals = np.where(pop_vals == 0, 1, pop_vals)

    eb = Empirical_Bayes(
        gdf[coluna_casos].fillna(0).values,
        pop_vals
    )

    # Multiplica por 100.000 para manter a escala da taxa
    gdf[nome_saida] = eb.r * 100000
    return gdf


def obter_geometria_municipios(
    ano: int = 2022,
    uf: str = None,
    simplificado: bool = True
) -> gpd.GeoDataFrame:
    """
    Baixa (ou carrega do cache) a malha municipal do IBGE.
    
    uf: Sigla (ex: 'PI', 'CE') ou código do estado (ex: 22). 
        Se None, baixa todo o Brasil.
    """
    code = uf if uf else "all"
    
    gdf = geobr.read_municipality(
        code_muni=code,
        year=ano,
        simplified=simplificado
    )

    # Padronização de colunas
    gdf["code_muni"] = gdf["code_muni"].astype(str)

    return gdf

def juntar_com_geometria(
    df,
    coluna_codigo: str = "codmunres",
    ano_malha: int = 2022,
    uf: str = None
):
    """
    Junta a tabela agregada do SINASC com a malha municipal ou estadual.
    """
    
    if coluna_codigo not in df.columns:
        raise KeyError(f"Coluna '{coluna_codigo}' não encontrada no DataFrame. Colunas disponíveis: {list(df.columns)}")
    
    # Lógica para Estados (UF)
    if coluna_codigo == "codufres":
        gdf_shape = geobr.read_state(year=ano_malha, simplified=True)
        col_geo = "code_state"
        
        # Se houver filtro de UF
        if uf:
            if str(uf).isdigit():
                gdf_shape = gdf_shape[gdf_shape["code_state"] == float(uf)]
            else:
                gdf_shape = gdf_shape[gdf_shape["abbrev_state"] == str(uf).upper()]
        
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
    gdf_shape = obter_geometria_municipios(ano=ano_malha, uf=uf)

    # Padroniza para 6 dígitos para garantir o join (SINASC costuma ser 6, Geobr 7)
    df[coluna_codigo] = df[coluna_codigo].astype(str)
    df["_cod_join"] = df[coluna_codigo].str.slice(0, 6)
    
    gdf_shape["code_muni"] = gdf_shape["code_muni"].astype(str)
    gdf_shape["_cod_join"] = gdf_shape["code_muni"].str.slice(0, 6)

    gdf = gdf_shape.merge(
        df,
        on="_cod_join",
        how="left"
    )
    
    return gdf
