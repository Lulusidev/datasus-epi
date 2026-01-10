import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def plotar_grafico_tendencia(df: pd.DataFrame, title: str):
    """
    Plots a trend graph for multiple groups in a single figure.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame where the index represents the groups and the columns represent the years.
    title : str
        The title of the graph.
    """
    years = list(map(int, df.columns))
    groups = df.index

    fig, ax = plt.subplots(figsize=(8, 6))

    grayscale_values = np.linspace(0.2, 0.8, len(groups))
    linestyles = ['-', '--', '-.', ':']

    for i, group in enumerate(groups):
        color = str(grayscale_values[i])
        style = linestyles[i % len(linestyles)]

        ax.plot(
            years,
            df.loc[group],
            marker='o',
            linestyle=style,
            color=color,
            label=group
        )

    ax.set_xlabel("Year", fontsize=12)
    ax.set_ylabel("Rate", fontsize=10)
    ax.set_title(title, fontsize=14)

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
        ncol=int(len(groups) / 2),
        fontsize=9
    )

    plt.xticks(years, rotation=45)
    plt.tight_layout()
    plt.show()


def plotar_grade_tendencia(df: pd.DataFrame, results: pd.DataFrame, title: str):
    """
    Plots a grid of trend graphs for multiple groups,
    including the linear regression line.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame where the index represents the groups and the columns represent the years.
    results : pd.DataFrame
        DataFrame containing the results of the linear regression (B0, B1, P-value, etc.).
    title : str
        The main title of the grid of graphs.
    """
    years = list(map(int, df.columns))
    groups = df.index.tolist()

    if len(groups) > 6:
        groups = groups[:6]

    fig, axes = plt.subplots(
        nrows=3,
        ncols=2,
        sharex=False,
        figsize=(12, 8)
    )

    axes = axes.flatten()

    for i, (ax, group) in enumerate(zip(axes, groups)):
        ax.plot(
            years,
            df.loc[group],
            marker='o',
            linestyle='-',
            color='0.2',
            label='Observed'
        )

        row = results[
            results['Group']
            .str.replace('*', '', regex=False)
            .str.strip() == group
        ]

        if not row.empty:
            beta0 = row["B0"].values[0]
            beta1 = row["B1"].values[0]

            trend_line = [beta0 + beta1 * year for year in years]

            p = row["P-value"].values[0]
            p_val = f"p={p:.3f}" if p > 0.001 else "p<0.001"

            lr_label = (
                f"Linear Regression ({p_val}, B1: {beta1:.3f})"
            )

            ax.plot(
                years,
                trend_line,
                linestyle='--',
                color='0.5',
                label=lr_label
            )

        ax.set_title(group, fontsize=12, pad=5)
        ax.set_ylabel("Rate", fontsize=10)
        ax.legend(fontsize=9)

        ax.grid(
            True,
            which='both',
            linestyle='--',
            linewidth=0.5,
            alpha=0.7
        )

        ax.set_xticks(years)
        ax.set_xticklabels(
            years,
            rotation=45,
            ha='right',
            fontsize=8
        )

        if i >= 4:
            ax.set_xlabel("Year", fontsize=12)

    for i in range(len(groups), len(axes)):
        fig.delaxes(axes[i])

    plt.suptitle(title, fontsize=14, y=0.98)
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.show()
