import polars as pl
from .dictionaries import DE_UF_CODIGO_PARA_SIGLA, DE_UF_SIGLA_PARA_REGIAO

def derivar_variaveis(df: pl.LazyFrame) -> pl.LazyFrame:
    """
    Derives new variables from the raw SINASC data.
    """
    age = pl.col("IDADEMAE").cast(pl.Int32, strict=False)

    return df.with_columns([
        pl.when(age < 15).then(pl.lit("<15"))
        .when(age < 20).then(pl.lit("15-19"))
        .when(age < 25).then(pl.lit("20-24"))
        .when(age < 30).then(pl.lit("25-29"))
        .when(age < 35).then(pl.lit("30-34"))
        .when(age < 40).then(pl.lit("35-39"))
        .otherwise(pl.lit("40+"))
        .alias("faixa_etaria_mae"),

        pl.col("CODMUNRES")
        .cast(pl.Utf8)
        .alias("codmunres"),

        # UF derived from the municipality
        pl.col("CODMUNRES")
        .cast(pl.Utf8)
        .str.slice(0, 2)
        .alias("codufres"),
    ]).with_columns(
        pl.col("codufres")
        .replace(DE_UF_CODIGO_PARA_SIGLA)
        .replace(DE_UF_SIGLA_PARA_REGIAO)
        .alias("REGIAO")
    )
