import polars as pl

def indicador_malformacao(
    df: pl.LazyFrame,
    cid: str | None = None
) -> pl.LazyFrame:
    """
    Creates a malformation indicator column.
    """
    if cid is None:
        return df.with_columns(pl.lit(0).alias("case"))

    return df.with_columns(
        (
            (pl.col("IDANOMAL") == "1") &
            pl.col("CODANOMAL")
            .fill_null("")
            .str.contains(f"^{cid}")
        )
        .cast(pl.Int8)
        .alias("case")
    )
