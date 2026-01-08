import libpysal
import numpy as np
from esda.moran import Moran
from esda.moran import Moran_Local
from esda.smoothing import Empirical_Bayes

def criar_matriz_vizinhanca(
    gdf,
    metodo: str = "queen",
    k: int = 8
):
    """
    Cria matriz de vizinhança espacial

    metodo:
        - 'queen' : contiguidade
        - 'knn'   : k-vizinhos mais próximos
    """

    if metodo == "queen":
        w = libpysal.weights.Queen.from_dataframe(gdf)
    elif metodo == "knn":
        w = libpysal.weights.KNN.from_dataframe(gdf, k=k)
    else:
        raise ValueError("metodo deve ser 'queen' ou 'knn'")

    w.transform = "r"  # row-standardized
    return w



def moran_global(
    valores: np.ndarray,
    w
):
    """
    Calcula Moran Global
    """
    valores = np.nan_to_num(valores)
    mi = Moran(valores, w)

    return {
        "I": mi.I,
        "p_value": mi.p_sim
    }

def lisa_local(
    valores: np.ndarray,
    w
):
    """
    Calcula LISA (Moran Local)
    """
    valores = np.nan_to_num(valores)
    lisa = Moran_Local(valores, w)

    return {
        "Ii": lisa.Is,
        "p_values": lisa.p_sim,
        "quadrant": lisa.q
    }

def suavizar_taxa_empirical_bayes(
    gdf,
    casos: str,
    populacao: str,
    nome_saida: str = "taxa_suavizada"
):
    """
    Suavização Empirical Bayes clássica
    """
    eb = Empirical_Bayes(
        gdf[casos].fillna(0).values,
        gdf[populacao].fillna(1).values
    )

    gdf[nome_saida] = eb.eb
    return gdf


def preparar_dados_bym(
    gdf,
    casos: str,
    populacao: str
):
    """
    Prepara arrays para o modelo BYM
    """
    casos_arr = gdf[casos].fillna(0).values
    pop_arr = gdf[populacao].replace(0, 1).values

    E = pop_arr * (casos_arr.sum() / pop_arr.sum())

    return casos_arr, pop_arr, E
