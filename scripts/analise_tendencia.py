from .taxas import obter_taxa_sinasc
from .visualizacao import (
    plot_grafico_tendencia_unico,
    regressaolinear,
    plot_trend_grid_gray
)
from .dicionarios import UF_CODIGO_PARA_SIGLA, UF_SIGLA_PARA_NOME

import pandas as pd

def preparar_tabela_tendencia(
    anos: list[int],
    cid: str,
    estrato: str,
    tempo: str = "ano",
    k: int = 100_000,
    nome_estado: bool = True
) -> pd.DataFrame:

    df = obter_taxa_sinasc(
        anos=anos,
        cid=cid,
        tempo=tempo,
        estratos=[estrato],
        k=k
    ).to_pandas()

    # 🔹 Traduz UF
    if estrato == "UFINFORM":
        df["UF"] = (
            df["UFINFORM"]
            .astype(str)
            .map(UF_CODIGO_PARA_SIGLA)
        )

        if nome_estado:
            df["UF"] = df["UF"].map(UF_SIGLA_PARA_NOME)

        estrato = "UF"

    return (
        df
        .pivot(index=estrato, columns=tempo, values=f"taxa_por_{k}")
        .sort_index(axis=1)
    )


def main():
    anos = list(range(2020, 2022))
    cid = "Q20"
    titulo = f"{anos[0]}-{anos[-1]} {cid}"
    estrato="UFINFORM"
    tabela = preparar_tabela_tendencia(
        anos=anos,
        cid=cid,
        estrato=estrato
    )

    plot_grafico_tendencia_unico(
        tabela,
        titulo
    )

    resultados = regressaolinear(tabela)
    plot_trend_grid_gray(
        tabela,
        resultados,
        titulo
    )
    resultados.to_csv(f"{titulo}.csv")


if __name__ == "__main__":
    main()
