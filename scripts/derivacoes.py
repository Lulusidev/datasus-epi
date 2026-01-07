import polars as pl

def derivar_variaveis(df: pl.LazyFrame) -> pl.LazyFrame:
    idade = pl.col("IDADEMAE").cast(pl.Int32, strict=False)

    return df.with_columns(
        pl.when(idade < 15).then(pl.lit("<15"))
        .when(idade < 20).then(pl.lit("15-19"))
        .when(idade < 25).then(pl.lit("20-24"))
        .when(idade < 30).then(pl.lit("25-29"))
        .when(idade < 35).then(pl.lit("30-34"))
        .when(idade < 40).then(pl.lit("35-39"))
        .otherwise(pl.lit("40+"))
        .alias("faixa_idade_mae"),

        pl.col("CODMUNRES")
        .cast(pl.Utf8)
        .str.slice(0, 2)
        .alias("UFINFORM")
    )
