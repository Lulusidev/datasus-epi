import geopandas as gpd
import matplotlib.pyplot as plt

def plotar_mapa_coropletico(
    gdf: gpd.GeoDataFrame,
    coluna: str,
    ax,
    cmap: str = "Blues",
    titulo_legenda: str = "Quartis",
    fmt: str = "{:.1f}",
    titulo: str | None = None
):
    """
    Plota um mapa coroplético estático usando quartis.

    Parâmetros
    ----------
    gdf : geopandas.GeoDataFrame
        GeoDataFrame contendo os dados e a geometria.
    coluna : str
        Nome da coluna no GeoDataFrame a ser plotada.
    ax : matplotlib.axes.Axes
        Objeto Axes do Matplotlib onde o mapa será plotado.
    cmap : str,
        Mapa de cores a ser usado.
    titulo_legenda : str, padrão "Quartis"
        Título da legenda do mapa.
    fmt : str, padrão "{:.1f}"
        Formato de string para os rótulos da legenda.
    titulo : str, opcional
        Título do mapa.
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
    if titulo:
        ax.set_title(titulo)