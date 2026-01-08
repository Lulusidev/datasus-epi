import polars as pl
import quadrosdesaude as qds
from pathlib import Path
from .config import FTP_PATH, PASTA_DBC, PASTA_PARQUET

def garantir_parquet_sinasc(ano: int) -> Path:
    nome = f"DNBR{ano}"
    arquivo_parquet = PASTA_PARQUET / f"{nome}.parquet"

    if arquivo_parquet.exists():
        print(f"✅ Parquet {ano} já existe — usando direto")
        return arquivo_parquet

    arquivo_dbc = PASTA_DBC / f"{nome}.dbc"

    if not arquivo_dbc.exists():
        print(f"⬇️ Baixando SINASC {ano}")
        qds.ftp_download_arquivo(
            ftp_path=FTP_PATH,
            filename=arquivo_dbc.name,
            destination_folder=str(PASTA_DBC)
        )

    print(f"🔄 Convertendo {ano} para Parquet")
    qds.dbc2parquet(
        caminho_dbc=str(arquivo_dbc),
        destino_parquet=str(PASTA_PARQUET),
        tamanho_lote=250_000
    )

    return arquivo_parquet

def abrir_sinasc(anos: list[int]) -> pl.LazyFrame:
    parquets = [garantir_parquet_sinasc(ano) for ano in anos]

    return pl.scan_parquet(
        parquets,
        extra_columns="ignore"
    )