import polars as pl

def padronizar_tempo(df: pl.LazyFrame) -> pl.LazyFrame:
    """
    Standardizes time-related variables.
    """
    return (
        df
        .with_columns(
            pl.col("DTNASC")
            .str.strptime(pl.Date, "%d%m%Y", strict=False)
            .alias("birth_date")
        )
        .with_columns(
            pl.col("birth_date").dt.year().alias("year"),
            pl.col("birth_date").dt.month().alias("month"),
        )
    )