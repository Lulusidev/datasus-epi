import polars as pl

def padronizar_tempo(df: pl.LazyFrame) -> pl.LazyFrame:
    return (
        df
        .with_columns(
            pl.col("DTNASC")
            .str.strptime(pl.Date, "%d%m%Y", strict=False)
            .alias("data_nascimento")
        )
        .with_columns(
            pl.col("data_nascimento").dt.year().alias("ano"),
            pl.col("data_nascimento").dt.month().alias("mes"),
        )
    )