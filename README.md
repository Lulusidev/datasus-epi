# Analysis of Congenital Malformations in Brazil

This project provides a set of Python tools for the epidemiological analysis of data on congenital malformations from SINASC (Information System on Live Births) in Brazil.

## Installation

It is recommended to use `uv` to install the dependencies from `pyproject.toml`:

```bash
uv pip install -e .
```

## How to use the package

The `datasus_epi` package is designed to be a flexible API for use in Jupyter notebooks or other Python projects. It abstracts the download, cleaning, and standardization of SINASC data, allowing the researcher to focus on the analysis.

### Calling the API

The main entry point for the analysis is the `get_rate_sinasc` function. It orchestrates the entire pipeline, from data loading to rate aggregation.

```python
from datasus_epi.sinasc.taxas import get_rate_sinasc

# Example: Calculate the rate of ALL congenital anomalies (CID Q)
# by Region of Brazil, for the years 2015 to 2024.
grouped_rates = get_rate_sinasc(
    anos=list(range(2015, 2025)),
    cid="Q",  # "Q" is the prefix for all anomalies in Ch. XVII of ICD-10
    estratos=["REGIAO", "ano"] # Grouping by region and year
)

print(grouped_rates)
```

### Performing Analyses

With the aggregated data in hand, you can use the analysis modules to investigate trends and spatial patterns.

#### Trend Analysis

Use the functions of the `datasus_epi.analysis.trends` module to apply statistical tests to time series.

```python
from datasus_epi.analysis.trends import linear_regression, mann_kendall
import pandas as pd

# 1. Prepare the table (pivot)
time_series_table = grouped_rates.pivot(
    index="REGIAO", 
    columns="ano", 
    values="taxa_por_100000"
)

# 2. Apply the tests
regression_results = linear_regression(time_series_table)
mk_results = mann_kendall(time_series_table)

print("\nLinear Regression Results:")
print(regression_results)

print("\nMann-Kendall Test Results:")
print(mk_results)
```

#### Spatial Analysis

The `datasus_epi.analysis.spatial` module offers tools for spatial autocorrelation analysis.

*Note: Spatial analysis is usually done in a single time period and with a finer geographical granularity (municipalities or states).*

```python
from datasus_epi.analysis.spatial import create_neighborhood_matrix, global_moran, local_lisa

# Example with 2021 data by municipality
rates_2021_mun = get_rate_sinasc(
    anos=[2021],
    cid="Q",
    estratos=["CODMUNRES"],
    retorno="geopandas" # Essential for spatial analysis
)

# Create neighborhood matrix
w = create_neighborhood_matrix(rates_2021_mun, method="queen")

# Calculate Global Moran
moran_i, moran_p = global_moran(rates_2021_mun, "taxa_por_100000", w)
print(f"\nGlobal Moran's I: {moran_i:.4f} (p-value: {moran_p:.4f})")

# Calculate LISA
gdf_lisa = local_lisa(rates_2021_mun, "taxa_por_100000", w)
print("\nLISA Clusters:")
print(gdf_lisa["lisa_cluster"].value_counts())

```

## Project Structure

```
datasus_epi/
├── __init__.py
├── sinasc/
│   ├── __init__.py
│   ├── load.py
│   ├── aggregate.py
│   ├── dictionaries.py
│   ├── derive.py
│   ├── indicadores.py
│   ├── tempo.py
│   └── taxas.py
├── analysis/
│   ├── __init__.py
│   ├── trends.py
│   └── spatial.py
└── viz/
    ├── __init__.py
    ├── maps.py
    └── trends.py
```
