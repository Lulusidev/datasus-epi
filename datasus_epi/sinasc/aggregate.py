import polars as pl

def agregar(
    df: pl.LazyFrame,
    group_cols: list[str],
    k: int = 100_000
) -> pl.LazyFrame:
    """
    Aggregates SINASC data to calculate live births, cases, and rates
    per specified grouping columns.

    Parameters
    ----------
    df : pl.LazyFrame
        The input Polars LazyFrame containing SINASC data.
    group_cols : list[str]
        A list of column names to group the data by (e.g., ["year", "UFINFORM"]).
    k : int, default 100_000
        The constant to multiply the rate by (e.g., rate per 100,000).

    Returns
    -------
    pl.LazyFrame
        A Polars LazyFrame with aggregated data, including 'live_births',
        'cases', and 'rate'.
    """
    return (
        df
        .group_by(group_cols)
        .agg([
            pl.len().alias("live_births"),
            pl.col("case").sum().alias("cases"),
        ])
        .with_columns(
            (pl.col("cases") / pl.col("live_births") * k)
            .alias(f"rate")
        )
        .sort(group_cols)
    )
