import libpysal
import numpy as np
from esda.moran import Moran
from esda.moran import Moran_Local
from esda.smoothing import Empirical_Bayes
import pandas as pd
import geopandas as gpd
import geobr

def criar_matriz_pesos_espaciais(
    gdf,
    method: str = "queen",
    k: int = 8
):
    """
    Creates a spatial neighborhood matrix.

    method:
        - 'queen' : contiguity
        - 'knn'   : k-nearest neighbors
    """

    if method == "queen":
        w = libpysal.weights.Queen.from_dataframe(gdf, use_index=True)
    elif method == "knn":
        w = libpysal.weights.KNN.from_dataframe(gdf, k=k, use_index=True)
    else:
        raise ValueError("method must be 'queen' or 'knn'")

    w.transform = "r"  # row-standardized
    return w



def calcular_moran_global(
    gdf,
    column: str,
    w
):
    """
    Calculates Global Moran's I.
    """
    values = gdf[column].fillna(0).values
    mi = Moran(values, w)

    return mi.I, mi.p_sim

def calcular_lisa_local(
    gdf,
    column: str,
    w
):
    """
    Calculates LISA (Local Moran).
    """
    values = gdf[column].fillna(0).values
    lisa = Moran_Local(values, w)

    # Identify significant clusters (p < 0.05)
    sig = lisa.p_sim < 0.05
    
    # Cluster categories
    categories = {
        1: 'HH',  # High-High
        2: 'LH',  # Low-High
        3: 'LL',  # Low-Low
        4: 'HL'   # High-Low
    }
    
    gdf['lisa_cluster'] = 'Not significant'
    gdf.loc[sig, 'lisa_cluster'] = [categories[q] for q in lisa.q[sig]]

    return gdf

def suavizar_taxa(
    gdf,
    cases_column: str,
    population_column: str,
    output_name: str = "smoothed_rate"
):
    """
    Classical Empirical Bayes smoothing.
    """
    # Treatment to avoid division by zero
    pop_vals = gdf[population_column].fillna(0).values
    pop_vals = np.where(pop_vals == 0, 1, pop_vals)

    eb = Empirical_Bayes(
        gdf[cases_column].fillna(0).values,
        pop_vals
    )

    # Multiplies by 100,000 to maintain the rate scale (per 100k inhabitants)
    gdf[output_name] = eb.r * 100000
    return gdf


def obter_geometria_municipios(
    year: int = 2022,
    simplified: bool = True
) -> gpd.GeoDataFrame:
    """
    Downloads (or loads from cache) the municipal mesh from IBGE.
    """
    gdf = geobr.read_municipality(
        year=year,
        simplified=simplified
    )

    # Column standardization
    gdf["code_muni"] = gdf["code_muni"].astype(str)

    return gdf

def juntar_com_geometria(
    df,
    code_column: str = "municipality_residence_code",
    mesh_year: int = 2022
):
    """
    Joins aggregated SINASC table to the municipal or state mesh.
    """
    
    if code_column not in df.columns:
        raise KeyError(f"Column '{code_column}' not found in DataFrame. Available columns: {list(df.columns)}")
    
    # Logic for States (UF)
    if code_column == "uf_residence_code":
        gdf_shape = geobr.read_state(year=mesh_year, simplified=True)
        col_geo = "code_state"
        
        # Standardization
        gdf_shape[col_geo] = gdf_shape[col_geo].astype(str)
        df[code_column] = df[code_column].astype(str)
        
        gdf = gdf_shape.merge(
            df,
            left_on=col_geo,
            right_on=code_column,
            how="left"
        )
        return gdf

    # Logic for Municipalities (Default)
    gdf_shape = obter_geometria_municipios(year=mesh_year)

    # Standardize to 6 digits to ensure the join (SINASC is usually 6, Geobr 7)
    df[code_column] = df[code_column].astype(str)
    df["_cod_join"] = df[code_column].str.slice(0, 6)
    
    gdf_shape["code_muni"] = gdf_shape["code_muni"].astype(str)
    gdf_shape["_cod_join"] = gdf_shape["code_muni"].str.slice(0, 6)

    gdf = gdf_shape.merge(
        df,
        on="_cod_join",
        how="left"
    )
    
    # Optionally remove auxiliary column, or keep for debugging
    # del gdf["_cod_join"]

    return gdf
