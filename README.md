# datasus_epi

**datasus_epi** is a Python library designed for the epidemiological analysis of data on congenital malformations from **SINASC** (Information System on Live Births) in Brazil.

It streamlines the process of fetching, cleaning, and aggregating public health data to calculate prevalence rates, analyze temporal trends, and explore spatial distributions using advanced statistical methods.

## Features

-   **Data Retrieval:** Easy fetching of SINASC data for specific years and CID-10 codes.
-   **Rate Calculation:** Automated calculation of prevalence rates (e.g., per 100,000 live births) stratified by region, municipality, or other variables.
-   **Trend Analysis:** Built-in support for Linear Regression and Mann-Kendall tests to identify temporal trends.
-   **Spatial Analysis:** Tools for constructing spatial weights matrices, calculating Global Moran's I, and identifying LISA (Local Indicators of Spatial Association) clusters.
-   **Visualization:** Dedicated plotting functions for time series trends and choropleth/cluster maps.

## Installation

This project is managed with `uv`. To install it in editable mode with all dependencies:

```bash
uv pip install -e .
```

Alternatively, you can use standard `pip`:

```bash
pip install -e .
```

## Quick Start

Here is a basic example of how to use the library to analyze trends and spatial clusters.

### 1. Data Loading & Aggregation

```python
import pandas as pd
from api.sinasc import obter_taxa_sinasc

# Define analysis parameters
years = list(range(2015, 2025))
cid_code = 'Q' # ICD-10 chapter for Congenital Malformations

# Fetch data aggregated by Region
df_regional = obter_taxa_sinasc(
    anos=years,
    cid=cid_code,
    estratos=['REGIAO'],
    retorno='pandas' # Can also be 'polars' or 'geopandas'
)

print(df_regional.head())
```

### 2. Trend Analysis

```python
from apianalysis.trends import calcular_regressao_linear, calcular_mann_kendall
from apiviz.trends import plotar_grafico_tendencia

# Prepare data for time-series analysis (Pivot: Index=Region, Cols=Year)
time_series = df_regional.pivot(
    index="REGIAO",
    columns="ano",
    values="taxa_por_100000"
)

# Run statistical tests
regression_results = calcular_regressao_linear(time_series)
mk_results = calcular_mann_kendall(time_series)

print("Linear Regression Trends:", regression_results)
print("Mann-Kendall Trends:", mk_results)

# Plot trends
plotar_grafico_tendencia(time_series, "Congenital Malformations Prevalence by Region")
```

### 3. Spatial Analysis

```python
from api.analysis.spatial import criar_matriz_vizinhanca, calcular_moran_global, calcular_lisa_local
from api.viz.maps import plotar_mapa_coropletico
import matplotlib.pyplot as plt

# Fetch data by Municipality with geometries
gdf = obter_taxa_sinasc(
    anos=[2024],
    cid=cid_code,
    estratos=["codmunres"],
    retorno="geopandas"
)

# Filter valid data
gdf_analise = gdf[gdf['n_nascidos_vivos'].notna()].copy()

# Create spatial weights matrix (Queen contiguity)
w = criar_matriz_vizinhanca(gdf_analise, metodo="queen")

# Global Moran's I
moran_i, moran_p = calcular_moran_global(gdf_analise, "taxa_por_100000", w)
print(f"Global Moran's I: {moran_i:.4f} (p-value: {moran_p:.4f})")

# Local LISA Clusters
gdf_lisa = calcular_lisa_local(gdf_analise, "taxa_por_100000", w)

# Plot
fig, ax = plt.subplots(figsize=(10, 10))
plotar_mapa_coropletico(gdf_lisa, coluna="taxa_por_100000", ax=ax)
plt.show()
```

## Modules Structure

*   **`api.sinasc`**: Core module for data loading (`obter_taxa_sinasc`), cleaning, and rate calculation.
*   **`api.analysis`**: Contains statistical tools.
    *   `trends`: Functions for temporal analysis (Regression, Mann-Kendall).
    *   `spatial`: Functions for spatial autocorrelation (Moran's I, LISA).
*   **`api.viz`**: Helpers for generating consistent plots.
    *   `trends`: Time series plots.
    *   `maps`: Geospatial visualizations.

## Jupyter Notebooks

This library is optimized for use in Jupyter Notebooks. The `retorno` parameter allows flexible integration with `pandas`, `polars`, or `geopandas` workflows. Check `test.ipynb` for an interactive demonstration.
