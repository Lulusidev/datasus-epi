import polars as pl

from datasus_epi.sinasc.load import carregar
from datasus_epi.sinasc.tempo import padronizar_tempo
from datasus_epi.sinasc.indicadores import indicador_malformacao
from datasus_epi.sinasc.aggregate import agregar

from datasus_epi.analysis.spatial import juntar_com_geometria


def obter_taxa_sinasc(
    years: list[int],
    cid: str | None = None,
    time_unit: str = "year",
    strata: list[str] | None = None,
    k: int = 100_000,
    return_format: str = "pandas"
):
    """
    Parameters
    ----------
    return_format :
        - 'pandas'    -> pandas.DataFrame
        - 'geopandas' -> geopandas.GeoDataFrame (if there is a geometry column)
        - 'polars'    -> polars.DataFrame
    """

    if strata is None:
        strata = []

    if time_unit not in {"year", "month"}:
        raise ValueError("time_unit must be 'year' or 'month'")

    group_cols = [time_unit] + strata


    # Main pipeline

    lf = (
        carregar(years)
        .pipe(padronizar_tempo)
        .pipe(indicador_malformacao, cid)
        .pipe(agregar, group_cols=group_cols, k=k)
        .sort(group_cols)
    )

    df = lf.collect()


    if return_format == "polars":
        return df

    df_pd = df.to_pandas()

    if return_format == "pandas":
        return df_pd

    if return_format == "geopandas":
        # Tries to identify the spatial column in the strata to pass to join_with_geometry
        geo_col = None
        for col in strata:
            if col in ["municipality_residence_code", "uf_residence_code"]:
                geo_col = col
                break
        
        # If no known column is found, but there are strata, use the first one (fallback)
        if geo_col is None and strata:
            geo_col = strata[0]
        elif geo_col is None:
            geo_col = "municipality_residence_code" # Last resort
            
        return juntar_com_geometria(df_pd, code_column=geo_col)


