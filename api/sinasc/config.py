from pathlib import Path

# --- FTP Configuration ---
CAMINHO_FTP = "ftp.datasus.gov.br"

# --- Local Directories ---
# Use Path for OS-independent path handling
PASTA_DBC = Path("data/dbc")
PASTA_PARQUET = Path("data/parquet")

# Ensure directories exist
PASTA_DBC.mkdir(parents=True, exist_ok=True)
PASTA_PARQUET.mkdir(parents=True, exist_ok=True)