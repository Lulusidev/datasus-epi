from pathlib import Path

FTP_PATH = "dissemin/publicos/SINASC/1996_/Dados/DNRES/"

PASTA_DBC = Path("data/dbc")
PASTA_PARQUET = Path("data/parquet")

PASTA_DBC.mkdir(parents=True, exist_ok=True)
PASTA_PARQUET.mkdir(parents=True, exist_ok=True)