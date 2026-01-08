import numpy as np
import pytensor.tensor as pt
import pymc as pm
import arviz as az

def modelo_bym(
    casos: np.ndarray,
    populacao: np.ndarray,
    W,
    draws: int = 2000,
    tune: int = 1000
):
    """
    Modelo BYM clássico (Poisson)
    Compatível com PyMC 5 + PyTensor
    """

    n = len(casos)

    # Casos esperados
    E = populacao * (casos.sum() / populacao.sum())

    with pm.Model() as model:

        # Intercepto
        alpha = pm.Normal("alpha", mu=0, sigma=5)

        # Ruído não-estruturado
        v = pm.Normal("v", mu=0, sigma=1, shape=n)

        # Efeito espacial estruturado (CAR)
        tau_u = pm.Gamma("tau_u", alpha=1, beta=0.01)

        u = pm.CAR(
            "u",
            mu=pt.zeros(n),
            W=W.sparse,
            alpha=1.0,
            tau=tau_u,
            shape=n
        )

        # Modelo log-linear
        log_mu = pt.log(E) + alpha + u + v
        mu = pt.exp(log_mu)

        pm.Poisson("casos_obs", mu=mu, observed=casos)

        trace = pm.sample(
            draws=draws,
            tune=tune,
            chains=4,
            target_accept=0.9
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
