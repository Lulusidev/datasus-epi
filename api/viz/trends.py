import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def plotar_grafico_tendencia(df: pd.DataFrame, titulo: str):
    """
    Plota um gráfico de tendência para múltiplos grupos em uma única figura.

    Parâmetros
    ----------
    df : pd.DataFrame
        DataFrame onde o índice representa os grupos e as colunas representam os anos.
    titulo : str
        O título do gráfico.
    """
    anos = list(map(int, df.columns))
    grupos = df.index

    fig, ax = plt.subplots(figsize=(8, 6))

    grayscale_values = np.linspace(0.2, 0.8, len(grupos))
    linestyles = ['-', '--', '-.', ':']

    for i, grupo in enumerate(grupos):
        color = str(grayscale_values[i])
        style = linestyles[i % len(linestyles)]

        ax.plot(
            anos,
            df.loc[grupo],
            marker='o',
            linestyle=style,
            color=color,
            label=grupo
        )

    ax.set_xlabel("Ano", fontsize=12)
    ax.set_ylabel("Taxa", fontsize=10)
    ax.set_title(titulo, fontsize=14)

    ax.grid(
        True,
        which='both',
        linestyle='--',
        linewidth=0.5,
        alpha=0.7
    )

    ax.legend(
        loc='upper center',
        bbox_to_anchor=(0.5, -0.15),
        ncol=int(len(grupos) / 2) if len(grupos) > 1 else 1,
        fontsize=9
    )

    plt.xticks(anos, rotation=45)
    plt.tight_layout()
    plt.show()


def plotar_grade_tendencia(df: pd.DataFrame, resultados: pd.DataFrame, titulo: str):
    """
    Plota uma grade de gráficos de tendência para múltiplos grupos,
    incluindo a linha de regressão linear.

    Parâmetros
    ----------
    df : pd.DataFrame
        DataFrame onde o índice representa os grupos e as colunas representam os anos.
    resultados : pd.DataFrame
        DataFrame contendo os resultados da regressão linear (Intercepto, Inclinacao, p-valor, etc.).
    titulo : str
        O título principal da grade de gráficos.
    """
    anos = list(map(int, df.columns))
    grupos = df.index.tolist()

    if len(grupos) > 6:
        grupos = grupos[:6]

    fig, axes = plt.subplots(
        nrows=3,
        ncols=2,
        sharex=False,
        figsize=(12, 8)
    )

    axes = axes.flatten()

    for i, (ax, grupo) in enumerate(zip(axes, grupos)):
        ax.plot(
            anos,
            df.loc[grupo],
            marker='o',
            linestyle='-',
            color='0.2',
            label='Observado'
        )

        row = resultados[
            resultados['Grupo']
            .str.replace('*', '', regex=False)
            .str.strip() == grupo
        ]

        if not row.empty:
            intercepto = row["Intercepto"].values[0]
            inclinacao = row["Inclinacao"].values[0]

            trend_line = [intercepto + inclinacao * ano for ano in anos]

            p = row["p-valor"].values[0]
            p_val = f"p={p:.3f}" if p > 0.001 else "p<0.001"

            lr_label = (
                f"Regressão Linear ({p_val}, Inclin.: {inclinacao:.3f})"
            )

            ax.plot(
                anos,
                trend_line,
                linestyle='--',
                color='0.5',
                label=lr_label
            )

        ax.set_title(grupo, fontsize=12, pad=5)
        ax.set_ylabel("Taxa", fontsize=10)
        ax.legend(fontsize=9)

        ax.grid(
            True,
            which='both',
            linestyle='--',
            linewidth=0.5,
            alpha=0.7
        )

        ax.set_xticks(anos)
        ax.set_xticklabels(
            anos,
            rotation=45,
            ha='right',
            fontsize=8
        )

        if i >= 4:
            ax.set_xlabel("Ano", fontsize=12)

    for i in range(len(grupos), len(axes)):
        fig.delaxes(axes[i])

    plt.suptitle(titulo, fontsize=14, y=0.98)
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.show()