import polars as pl

from api.sinasc.load import carregar
from api.sinasc.tempo import padronizar_tempo
from api.sinasc.indicadores import indicador_malformacao
from api.sinasc.derive import derivar_variaveis
from api.sinasc.aggregate import agregar
from api.sinasc.dictionaries import DE_UF_CODIGO_PARA_SIGLA

from api.analysis.spatial import juntar_com_geometria


def obter_taxa_sinasc(
    anos: list[int],
    cid: str | None = None,
    unidade_tempo: str = "ano",
    estratos: list[str] | None = None,
    multiplicador: int = 100_000,
    uf: str | None = None,
    retorno: str = "pandas"
):
    """
    Parâmetros
    ----------
    uf :
        Sigla da UF (ex: 'SP', 'RJ') ou código (ex: '35'). Opcional.
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


    # Resolve UF filter if present
    filter_expr = True
    if uf:
        uf_str = str(uf).upper()
        uf_code = None
        
        # Check if it's already a code (digits)
        if uf_str.isdigit():
             uf_code = uf_str
        else:
            # Find code by sigla
            for code, sigla in DE_UF_CODIGO_PARA_SIGLA.items():
                if sigla == uf_str:
                    uf_code = code
                    break
        
        if uf_code:
            filter_expr = pl.col("codufres") == uf_code
        else:
            # If valid code/sigla not found, maybe raise warning? 
            # For now, let's assume valid input or fail silently/filter nothing if logic differs
            pass


    # Pipeline principal

    lf = (
        carregar(anos)
        .pipe(padronizar_tempo)
        .pipe(derivar_variaveis)
        .filter(filter_expr)
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
            
        return juntar_com_geometria(df_pd, coluna_codigo=geo_col, uf=uf)


