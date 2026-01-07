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

ESTRATOS_VALIDOS = {
    "UF": "UFINFORM",
    "municipio": "CODMUNRES",
    "sexo": "SEXO",
    "raca": "RACACOR",
    "idade_mae": "IDADEMAE",
    "faixa_idade_mae": "faixa_idade_mae",
    "escolaridade": "ESCMAE",
}

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
    return (
        df
        .with_columns(
            pl.col("DTNASC")
            .str.strptime(pl.Date, "%d%m%Y", strict=False)
            .alias("data_nascimento")
        )
        .with_columns(
            pl.col("data_nascimento").dt.year().alias("ano"),
            pl.col("data_nascimento").dt.month().alias("mes"),
        )
    )



def indicador_malformacao(
    df: pl.LazyFrame,
    cid: str | None = None
) -> pl.LazyFrame:

    if cid is None:
        return df.with_columns(pl.lit(0).alias("caso"))

    return df.with_columns(
        (
            (pl.col("IDANOMAL") == "1") &
            pl.col("CODANOMAL")
            .fill_null("")
            .str.contains(f"^{cid}")
        )
        .cast(pl.Int8)
        .alias("caso")
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

def derivar_variaveis(df: pl.LazyFrame) -> pl.LazyFrame:
    idade = pl.col("IDADEMAE").cast(pl.Int32, strict=False)

    return df.with_columns(
        # 1. Criação da Faixa Etária (com a correção do pl.lit)
        pl.when(idade < 15).then(pl.lit("<15"))
        .when(idade < 20).then(pl.lit("15-19"))
        .when(idade < 25).then(pl.lit("20-24"))
        .when(idade < 30).then(pl.lit("25-29"))
        .when(idade < 35).then(pl.lit("30-34"))
        .when(idade < 40).then(pl.lit("35-39"))
        .otherwise(pl.lit("40+"))
        .alias("faixa_idade_mae"),

        # 2. NOVA PARTE: Extração da UF a partir do código do município de residência
        pl.col("CODMUNRES")
        .cast(pl.Utf8)        # Garante que tratamos como texto
        .str.slice(0, 2)      # Pega os 2 primeiros dígitos (Ex: 355030 -> 35)
        .alias("UFINFORM")    # Cria a coluna que o seu main() está pedindo
    )

def obter_taxa_sinasc(
    anos: list[int],
    cid: str | None = None,
    tempo: str = "ano",                 # "ano" ou "mes"
    estratos: list[str] | None = None,
    k: int = 100_000
) -> pl.DataFrame:

    if estratos is None:
        estratos = []

    # Resolver tempo
    if tempo not in {"ano", "mes"}:
        raise ValueError("tempo deve ser 'ano' ou 'mes'")

    group_cols = [tempo] + estratos

    df = (
        abrir_sinasc(anos)
        .pipe(padronizar_tempo)
        .pipe(derivar_variaveis)
        .pipe(indicador_malformacao, cid)
    )

    return (
        df
        .group_by(group_cols)
        .agg([
            pl.len().alias("n_nascidos_vivos"),
            pl.col("caso").sum().alias("n_casos"),
        ])
        .with_columns(
            (pl.col("n_casos") / pl.col("n_nascidos_vivos") * k)
            .alias(f"taxa_por_{k}")
        )
        .sort(group_cols)
        .collect()
    )

def main():
    anos = [2020,2021]
    CID="Q20"
    resultado = obter_taxa_sinasc(
        anos=anos,
        cid="Q20",
        tempo="ano",
        estratos=["UFINFORM"]
    )
    print(resultado)

if __name__ == "__main__":
    main()
