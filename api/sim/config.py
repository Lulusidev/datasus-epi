from pathlib import Path

# --- FTP Configuration ---
# Path specific for SIM (Mortality Information System)
FTP_PATH_SIM = "/dissemin/publicos/SIM/CID10/DORES/"

# --- Local Directories ---
# Reusing the shared data directories
PASTA_DBC = Path("data/dbc")
PASTA_PARQUET = Path("data/parquet")

# Ensure directories exist
PASTA_DBC.mkdir(parents=True, exist_ok=True)
PASTA_PARQUET.mkdir(parents=True, exist_ok=True)
