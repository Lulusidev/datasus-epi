import numpy as np
import pymc as pm
import aesara.tensor as at
import arviz as az


def modelo_bym(
    casos: np.ndarray,
    populacao: np.ndarray,
    W,
    draws: int = 2000,
    tune: int = 1000,
    chains: int = 4,
    target_accept: float = 0.9
):

    n = len(casos)
    E = populacao * (casos.sum() / populacao.sum())

    with pm.Model() as model:

        alpha = pm.Normal("alpha", mu=0, sigma=5)

        v = pm.Normal("v", mu=0, sigma=1, shape=n)

        tau_u = pm.Gamma("tau_u", alpha=1, beta=0.01)

        u = pm.CAR(
            "u",
            mu=at.zeros(n),
            W=W.sparse,
            alpha=1,
            tau=tau_u,
            shape=n
        )

        log_mu = at.log(E) + alpha + u + v
        mu = at.exp(log_mu)

        pm.Poisson(
            "casos_obs",
            mu=mu,
            observed=casos
        )

        trace = pm.sample(
            draws=draws,
            tune=tune,
            chains=chains,
            target_accept=target_accept,
            return_inferencedata=True
        )

    return model, trace


def extrair_risco_relativo(trace, nivel: float = 0.95):

    u_mean = trace.posterior["u"].mean(("chain", "draw")).values
    v_mean = trace.posterior["v"].mean(("chain", "draw")).values

    rr_mean = np.exp(u_mean + v_mean)

    hdi = az.hdi(
        np.exp(trace.posterior["u"] + trace.posterior["v"]),
        hdi_prob=nivel
    )

    return {
        "RR_mean": rr_mean,
        "RR_lower": hdi.sel(hdi="lower").values,
        "RR_upper": hdi.sel(hdi="higher").values
    }


def diagnostico_bym(trace):

    return az.summary(
        trace,
        var_names=["alpha", "tau_u"],
        round_to=3
    )
