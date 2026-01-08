import polars as pl
from .io import abrir_sinasc
from .tempo import padronizar_tempo
from .derivacoes import derivar_variaveis
from .indicadores import indicador_malformacao

def obter_taxa_sinasc(
    anos: list[int],
    cid: str | None = None,
    tempo: str = "ano",
    estratos: list[str] | None = None,
    k: int = 100_000,
    retorno: str = "pandas"
):
    """
    Parâmetros
    ----------
    retorno :
        - 'pandas'    -> pandas.DataFrame
        - 'geopandas' -> geopandas.GeoDataFrame (se houver coluna geometry)
        - 'polars'    -> polars.DataFrame
    """

    if estratos is None:
        estratos = []

    if tempo not in {"ano", "mes"}:
        raise ValueError("tempo deve ser 'ano' ou 'mes'")

    group_cols = [tempo] + estratos


    # Pipeline principal

    lf = (
        abrir_sinasc(anos)
        .pipe(padronizar_tempo)
        .pipe(derivar_variaveis)
        .pipe(indicador_malformacao, cid)
        .group_by(group_cols)
        .agg([
            pl.len().alias("n_nascidos_vivos"),
            pl.col("caso").sum().alias("n_casos"),
        ])
        .with_columns(
            (pl.col("n_casos") / pl.col("n_nascidos_vivos") * k)
            .alias(f"taxa_por_{k}")
        )
        .sort(group_cols)
    )

    df = lf.collect()

    if retorno == "polars":
        return df

    elif retorno == "pandas":
        return df.to_pandas()

    elif retorno == "geopandas":
        import geopandas as gpd

        if "geometry" not in df.columns:
            raise ValueError(
                "retorno='geopandas' exige coluna 'geometry'"
            )

        return gpd.GeoDataFrame(
            df.to_pandas(),
            geometry="geometry",
            crs="EPSG:4674"
        )

    else:
        raise ValueError(
            "retorno inválido. Use: 'polars', 'pandas' ou 'geopandas'"
        )