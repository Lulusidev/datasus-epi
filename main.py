import pandas as pd
import quadrosdesaude as qds
import matplotlib.pyplot as plt
from pathlib import Path
import polars as pl

FTP_PATH = "dissemin/publicos/SINASC/1996_/Dados/DNRES/"

PASTA_DBC = Path("data/dbc")
PASTA_PARQUET = Path("data/parquet")

PASTA_DBC.mkdir(parents=True, exist_ok=True)
PASTA_PARQUET.mkdir(parents=True, exist_ok=True)

def garantir_parquet_sinasc(ano: int) -> Path:
    nome = f"DNBR{ano}"

    arquivo_parquet = PASTA_PARQUET / f"{nome}.parquet"
    if arquivo_parquet.exists():
        print(f"✅ Parquet {ano} já existe — usando direto")
        return arquivo_parquet

    # Só chega aqui se o parquet NÃO existir
    arquivo_dbc = PASTA_DBC / f"{nome}.dbc"

    if not arquivo_dbc.exists():
        print(f"⬇️ Baixando SINASC {ano}")
        qds.ftp_download_arquivo(
            ftp_path=FTP_PATH,
            filename=arquivo_dbc.name,
            destination_folder=str(PASTA_DBC)
        )

    print(f"🔄 Convertendo {ano} para Parquet")
    sucesso = qds.dbc2parquet(
        caminho_dbc=str(arquivo_dbc),
        destino_parquet=str(PASTA_PARQUET),
        tamanho_lote=250_000
    )

    if not sucesso:
        raise RuntimeError(f"Falha na conversão do SINASC {ano}")

    return arquivo_parquet

def abrir_sinasc(anos: list[int]) -> pl.LazyFrame:
    parquets = [garantir_parquet_sinasc(ano) for ano in anos]
    return pl.scan_parquet(parquets)

def padronizar_tempo(df: pl.LazyFrame) -> pl.LazyFrame:

    return df.with_columns([
        pl.col("DTNASC")
        .str.strptime(pl.Date, "%d%m%Y", strict=False)
        .alias("data_nascimento")
    ]).with_columns([
        pl.col("data_nascimento").dt.year().alias("ano"),
        pl.col("data_nascimento").dt.month().alias("mes"),
    ])

def indicador_malformacao(
    df: pl.LazyFrame,
    cids: list[str] | None = None
) -> pl.LazyFrame:

    base = pl.col("IDANOMAL") == "1"

    if cids is None:
        return df.with_columns(
            base.alias("caso")
        )

    padrao = "|".join(cids)

    return df.with_columns(
        (
            base &
            pl.col("CODANOMAL")
            .fill_null("")
            .str.contains(padrao)
        ).alias("caso")
    )

def serie_ecologica_nascidos_vivos(
    df: pl.LazyFrame,
    nivel_tempo: str = "ano",     # "ano" ou "mes"
    k: int = 100000
) -> pl.DataFrame:

    if nivel_tempo not in {"ano", "mes"}:
        raise ValueError("nivel_tempo deve ser 'ano' ou 'mes'")

    group_cols = ["ano"] if nivel_tempo == "ano" else ["ano", "mes"]

    return (
        df.group_by(group_cols)
        .agg([
            pl.len().alias("n_nascidos_vivos"),
            pl.col("caso").sum().alias("n_casos"),
        ])
        .with_columns(
            (pl.col("n_casos") / pl.col("n_nascidos_vivos") * k)
            .alias(f"taxa_por_{k/1000}")
        )
        .sort(group_cols)
        .collect()
    )

def obter_serie_malformacao(
    anos: list[int],
    cids: list[str] | None = None,
    nivel_tempo: str = "ano"
) -> pl.DataFrame:

    df = abrir_sinasc(anos)        # DataFrame
    df = padronizar_tempo(df)      # DataFrame
    df = indicador_malformacao(df, cids)

    return serie_ecologica_nascidos_vivos(
        df,
        nivel_tempo=nivel_tempo
    )

def main():
    anos_ = [2020,2021]

    print(obter_serie_malformacao(anos_,"Q20","ano"))

if __name__ == "__main__":
    main()
