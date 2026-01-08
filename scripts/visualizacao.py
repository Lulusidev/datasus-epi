import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm

def plot_grafico_tendencia_unico(df, titulo_):
    # Transpor o dataframe para que os anos fiquem no eixo x
    anos = list(map(int, df.columns))
    grupos = df.index

    # Cria figura única
    fig, ax = plt.subplots(figsize=(8, 6))

    # Define tons de cinza e estilos de linha
    grayscale_values = np.linspace(0.2, 0.8, len(grupos))
    linestyles = ['-', '--', '-.', ':']

    for i, grupo in enumerate(grupos):
        cor = str(grayscale_values[i])
        estilo = linestyles[i % len(linestyles)]

        ax.plot(
            anos,
            df.loc[grupo],
            marker='o',
            linestyle=estilo,
            color=cor,
            label=grupo
        )

    ax.set_xlabel("Year", fontsize=12)
    ax.set_ylabel("Rate", fontsize=10)
    ax.set_title(titulo_, fontsize=14)

    ax.grid(
        True,
        which='both',
        linestyle='--',
        linewidth=0.5,
        alpha=0.7
    )

    # Legenda centralizada abaixo do gráfico
    ax.legend(
        loc='upper center',
        bbox_to_anchor=(0.5, -0.15),
        ncol=int(len(grupos) / 2),
        fontsize=9
    )

    plt.xticks(anos, rotation=45)
    plt.tight_layout()
    plt.show()


def regressaolinear(df):
    results = []

    anos = df.columns.astype(int).values
    anos_len = len(anos) - 1

    X = sm.add_constant(anos)

    for fe in df.index:
        first = df.loc[fe].iloc[0]
        last = df.loc[fe].iloc[anos_len]

        var = ((last - first) / first) * 100

        data = df.loc[fe].astype(float).values
        X = sm.add_constant(anos)

        mod = sm.OLS(data, X)
        res = mod.fit()

        beta0, beta1 = res.params
        b1_lower, b1_upper = res.conf_int(alpha=0.05)[1]

        results.append({
            "Faixa Etária": fe,
            "First Value": first,
            "Last Value": last,
            "B0": beta0,
            "B1": beta1,
            "IC B1 lower": b1_lower.round(2),
            "IC B1 upper": b1_upper.round(2),
            "R^2": res.rsquared.round(2),
            "P-value": res.pvalues[1].round(5)
            if len(res.pvalues) > 1 else None,
            "Variação(%)": var.round(2)
        })

    df_results = pd.DataFrame(results)
    return df_results


def plot_trend_grid_gray(df, results_, title_):
    # Define eixo x (anos) e grupos
    years = list(map(int, df.columns))
    groups = df.index.tolist()

    # Limita a 6 grupos
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
        # Série observada
        ax.plot(
            years,
            df.loc[group],
            marker='o',
            linestyle='-',
            color='0.2',
            label='Observed'
        )

        row = results_[
            results_['Faixa Etária']
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

        # Força todos os anos no eixo x
        ax.set_xticks(years)
        ax.set_xticklabels(
            years,
            rotation=45,
            ha='right',
            fontsize=8
        )

        # Rótulo do eixo x apenas na última linha
        if i >= 4:
            ax.set_xlabel("Year", fontsize=12)

    # Remove subplots extras
    for i in range(len(groups), len(axes)):
        fig.delaxes(axes[i])

    plt.suptitle(title_, fontsize=14, y=0.98)
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.show()
