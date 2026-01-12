import polars as pl

def agregar(
    df: pl.LazyFrame,
    group_cols: list[str],
    multiplicador: int = 100_000
) -> pl.LazyFrame:
    """
    Agrega os dados do SINASC para calcular nascidos vivos, casos e taxas
    por colunas de agrupamento especificadas.

    Parâmetros
    ----------
    df : pl.LazyFrame
        O LazyFrame de entrada do Polars contendo os dados do SINASC.
    group_cols : list[str]
        Uma lista de nomes de colunas para agrupar os dados (ex: ["ano", "UFINFORM"]).
    multiplicador : int, padrão 100.000
        A constante pela qual multiplicar a taxa (ex: taxa por 100.000).

    Retorna
    -------
    pl.LazyFrame
        Um LazyFrame do Polars com dados agregados, incluindo 'n_nascidos_vivos',
        'casos' e 'taxa_por_100000'.
    """
    return (
        df
        .group_by(group_cols)
        .agg([
            pl.len().alias("n_nascidos_vivos"),
            pl.col("casos").sum().alias("casos"),
        ])
        .with_columns(
            (pl.col("casos") / pl.col("n_nascidos_vivos") * multiplicador)
            .alias(f"taxa_por_{multiplicador}")
        )
        .sort(group_cols)
    )