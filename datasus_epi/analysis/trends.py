import pandas as pd
import statsmodels.api as sm
import pymannkendall as mk

def calcular_regressao_linear(df: pd.DataFrame) -> pd.DataFrame:
    """
    Performs simple linear regression on time series data.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame where index represents groups and columns represent time points (e.g., years).

    Returns
    -------
    pd.DataFrame
        DataFrame with regression results including coefficients, R-squared, and p-value.
    """
    results = []

    years = df.columns.astype(int).values
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
            "Group": group,
            "First Value": first,
            "Last Value": last,
            "B0": beta0,
            "B1": beta1,
            "B1 CI lower": b1_lower.round(2),
            "B1 CI upper": b1_upper.round(2),
            "R^2": res.rsquared.round(2),
            "P-value": res.pvalues[1].round(5)
            if len(res.pvalues) > 1 else None,
            "Variation(%)": variation.round(2)
        })

    df_results = pd.DataFrame(results)
    return df_results

def calcular_mann_kendall(df: pd.DataFrame) -> pd.DataFrame:
    """
    Performs Mann-Kendall trend test on time series data.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame where index represents groups and columns represent time points (e.g., years).

    Returns
    -------
    pd.DataFrame
        DataFrame with Mann-Kendall test results including trend, p-value, and slope.
    """
    results = df.apply(
        lambda row: mk.original_test(row.astype(float)),
        axis=1
    ).apply(pd.Series)
    
    results.columns = ['Trend', 'h', 'p-value', 'z', 'Tau', 'Score', 'Variance', 'Slope', 'Intercept']
    
    # Add first and last values
    results['First Value'] = df.iloc[:, 0]
    results['Last Value'] = df.iloc[:, -1]
    
    return results

def hamed_rao(data: pd.Series) -> dict:
    """
    Performs Hamed-Rao modified Mann-Kendall trend test.
    (Placeholder - actual implementation needs to be added)
    """
    # TODO: Implement Hamed-Rao test
    return {"result": "Hamed-Rao placeholder"}