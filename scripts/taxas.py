import polars as pl

from .io import abrir_sinasc
from .tempo import padronizar_tempo
from .derivacoes import derivar_variaveis
from .indicadores import indicador_malformacao

from scripts.analise_espacial import juntar_geometria


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

    df_pd = df.to_pandas()

    if retorno == "pandas":
        return df_pd

    if retorno == "geopandas":
        # Tenta identificar a coluna espacial nos estratos para passar ao juntar_geometria
        col_geo = None
        for col in estratos:
            if col in ["CODMUNRES", "MUNINFORM", "CODUFRES", "UFINFORM"]:
                col_geo = col
                break
        
        # Se não achou nenhuma conhecida, mas tem estratos, usa o primeiro (fallback)
        if col_geo is None and estratos:
            col_geo = estratos[0]
        elif col_geo is None:
            col_geo = "CODMUNRES" # Último recurso
            
        return juntar_geometria(df_pd, coluna_codigo=col_geo)
