import pandas as pd
import statsmodels.api as sm
import pymannkendall as mk

def calcular_regressao_linear(df: pd.DataFrame) -> pd.DataFrame:
    """
    Realiza regressão linear simples em dados de série temporal.

    Parâmetros
    ----------
    df : pd.DataFrame
        DataFrame onde o índice representa os grupos e as colunas representam os pontos no tempo (ex: anos).

    Retorna
    -------
    pd.DataFrame
        DataFrame com resultados da regressão, incluindo coeficientes, R-quadrado e p-valor.
    """
    results = []

    years = df.columns.map(int).values
    years_len = len(years) - 1

    for group in df.index:
        first = df.loc[group].iloc[0]
        last = df.loc[group].iloc[years_len]

        variation = ((last - first) / first) * 100

        data = df.loc[group].astype(float).values
        X = sm.add_constant(years)

        mod = sm.OLS(data, X)
        res = mod.fit()

        beta0, beta1 = res.params
        b1_lower, b1_upper = res.conf_int(alpha=0.05)[1]

        results.append({
            "Grupo": group,
            "Valor Inicial": first,
            "Valor Final": last,
            "Intercepto": beta0,
            "Inclinacao": beta1,
            "Inclinacao IC inferior": b1_lower.round(2),
            "Inclinacao IC superior": b1_upper.round(2),
            "R^2": res.rsquared.round(2),
            "p-valor": res.pvalues[1].round(5)
            if len(res.pvalues) > 1 else None,
            "Variacao(%)": variation.round(2)
        })

    df_results = pd.DataFrame(results)
    return df_results

def calcular_mann_kendall(df: pd.DataFrame) -> pd.DataFrame:
    """
    Realiza o teste de tendência de Mann-Kendall em séries temporais.

    Parâmetros
    ----------
    df : pd.DataFrame
        DataFrame onde o índice representa grupos e as colunas representam pontos no tempo (ex: anos).

    Retorna
    -------
    pd.DataFrame
        DataFrame com resultados do teste de Mann-Kendall.
    """
    results = df.apply(
        lambda row: mk.original_test(row.astype(float)),
        axis=1
    ).apply(pd.Series)
    
    results.columns = ['Tendencia', 'h', 'p-valor', 'z', 'Tau', 'Score', 'Variancia', 'Inclinacao', 'Intercepto']
    
    # Adiciona valores iniciais e finais
    results['Valor Inicial'] = df.iloc[:, 0]
    results['Valor Final'] = df.iloc[:, -1]
    
    return results

def hamed_rao(data: pd.Series) -> dict:
    """
    Performs Hamed-Rao modified Mann-Kendall trend test.
    (Placeholder - actual implementation needs to be added)
    """
    # TODO: Implement Hamed-Rao test
    return {"result": "Hamed-Rao placeholder"}