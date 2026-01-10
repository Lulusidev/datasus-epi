import polars as pl

from datasus_epi.sinasc.load import carregar
from datasus_epi.sinasc.tempo import padronizar_tempo
from datasus_epi.sinasc.indicadores import indicador_malformacao
from datasus_epi.sinasc.derive import derivar_variaveis
from datasus_epi.sinasc.aggregate import agregar

from datasus_epi.analysis.spatial import juntar_com_geometria


def obter_taxa_sinasc(
    anos: list[int],
    cid: str | None = None,
    unidade_tempo: str = "ano",
    estratos: list[str] | None = None,
    multiplicador: int = 100_000,
    retorno: str = "pandas"
):
    """
    Parâmetros
    ----------
    retorno :
        - 'pandas'    -> pandas.DataFrame
        - 'geopandas' -> geopandas.GeoDataFrame (se houver coluna de geometria)
        - 'polars'    -> polars.DataFrame
    """

    if estratos is None:
        estratos = []

    if unidade_tempo not in {"ano", "mes"}:
        raise ValueError("unidade_tempo deve ser 'ano' ou 'mes'")

    group_cols = [unidade_tempo] + estratos


    # Pipeline principal

    lf = (
        carregar(anos)
        .pipe(padronizar_tempo)
        .pipe(derivar_variaveis)
        .pipe(indicador_malformacao, cid)
        .pipe(agregar, group_cols=group_cols, multiplicador=multiplicador)
        .sort(group_cols)
    )

    df = lf.collect()


    if retorno == "polars":
        return df

    df_pd = df.to_pandas()

    if retorno == "pandas":
        return df_pd

    if retorno == "geopandas":
        # Tenta identificar a coluna espacial nos estratos para passar para o join
        geo_col = None
        for col in estratos:
            if col.lower() in ["codmunres", "codufres", "codmun", "uf"]:
                geo_col = col
                break
        
        # Se nenhuma coluna conhecida for encontrada, mas houver estratos, usa o primeiro
        if geo_col is None and estratos:
            geo_col = estratos[0]
        elif geo_col is None:
            geo_col = "codmunres"
            
        return juntar_com_geometria(df_pd, coluna_codigo=geo_col)


