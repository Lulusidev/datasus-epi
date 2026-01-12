import polars as pl
import quadrosdesaude as qds
from pathlib import Path
from .config import CAMINHO_FTP, PASTA_DBC, PASTA_PARQUET
from .derive import derivar_variaveis

def _garantir_sinasc_parquet(year: int) -> Path:
    name = f"DNBR{year}"
    parquet_file = PASTA_PARQUET / f"{name}.parquet"

    if parquet_file.exists():
        print(f"✅ Parquet {year} already exists - using it directly")
        return parquet_file

    dbc_file = PASTA_DBC / f"{name}.dbc"

    if not dbc_file.exists():
        print(f"⬇️ Downloading SINASC {year}")
        qds.ftp_download_arquivo(
            ftp_path=CAMINHO_FTP,
            filename=dbc_file.name,
            destination_folder=str(PASTA_DBC)
        )

    print(f"🔄 Converting {year} to Parquet")
    qds.dbc2parquet(
        caminho_dbc=str(dbc_file),
        destino_parquet=str(PASTA_PARQUET),
        tamanho_lote=250_000
    )

    return parquet_file

def _abrir_sinasc(years: list[int]) -> pl.LazyFrame:
    parquets = [_garantir_sinasc_parquet(year) for year in years]

    return pl.scan_parquet(
        parquets,
        extra_columns="ignore"
    )

def carregar(years: list[int]) -> pl.LazyFrame:
    print("Starting SINASC loading...")
    df = _abrir_sinasc(years)
    df = derivar_variaveis(df)
    # TODO: Implement canonical schema application and official dictionaries
    # TODO: Implement deterministic cleaning
    print("SINASC loading complete.")
    return df