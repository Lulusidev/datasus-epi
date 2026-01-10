import geopandas as gpd
import matplotlib.pyplot as plt

def plotar_mapa_coropletico(
    gdf: gpd.GeoDataFrame,
    column: str,
    ax,
    cmap: str = "YlOrRd",
    legend_title: str = "Quartiles",
    fmt: str = "{:.1f}"
):
    """
    Plots a static choropleth map using quartiles.

    Parameters
    ----------
    gdf : geopandas.GeoDataFrame
        GeoDataFrame containing the data and geometry.
    column : str
        Name of the column in the GeoDataFrame to be plotted.
    ax : matplotlib.axes.Axes
        Matplotlib Axes object where the map will be plotted.
    cmap : str, default "YlOrRd"
        Colormap to be used.
    legend_title : str, default "Quartiles"
        Title for the map legend.
    fmt : str, default "{:.1f}"
        String format for the legend labels.
    """
    gdf.plot(
        column=column,
        cmap=cmap,
        scheme="quantiles",
        k=4,
        legend=True,
        legend_kwds={'loc': 'lower right', 'title': legend_title, 'fmt': fmt},
        edgecolor='black',
        linewidth=0.1,
        ax=ax
    )
