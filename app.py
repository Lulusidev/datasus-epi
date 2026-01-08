import streamlit as st
import geopandas as gpd
import matplotlib.pyplot as plt

from scripts.taxas import obter_taxa_sinasc
from scripts.analise_espacial import (
    criar_matriz_vizinhanca,
    suavizar_taxa_empirical_bayes,
    moran_global,
    lisa_local
)
from scripts.analise_bayesiana import (
    modelo_bym,
    extrair_risco_relativo,
    diagnostico_bym
)

# -----------------------------
# CONFIGURAÇÃO DA PÁGINA
# -----------------------------
st.set_page_config(
    page_title="Análise Espacial – SINASC",
    layout="wide"
)

st.title("Análise Espacial de Malformações Congênitas – SINASC")

# -----------------------------
# SIDEBAR – CONTROLES
# -----------------------------
st.sidebar.header("Parâmetros da análise")

cid = st.sidebar.text_input("CID (ex: Q20)", value="Q20")

ano1, ano2 = st.sidebar.slider(
    "Período",
    min_value=2000,
    max_value=2023,
    value=(2015, 2023)
)

estrato = st.sidebar.selectbox(
    "Estrato espacial",
    ["UFINFORM", "MUNINFORM"]
)

modelo = st.sidebar.selectbox(
    "Modelo espacial",
    [
        "Taxa bruta",
        "Empirical Bayes",
        "Moran / LISA",
        "BYM (Bayesiano)"
    ]
)

vizinhanca = st.sidebar.selectbox(
    "Tipo de vizinhança",
    ["queen", "knn"]
)

k = None
if vizinhanca == "knn":
    k = st.sidebar.slider("k vizinhos", 2, 12, 8)

executar = st.sidebar.button("Executar análise")

# -----------------------------
# EXECUÇÃO
# -----------------------------
if executar:

    st.info("Carregando e preparando dados...")

    anos = list(range(ano1, ano2 + 1))

    gdf = obter_taxa_sinasc(
        anos=anos,
        cid=cid,
        estratos=[estrato],
        retorno="geodataframe"
    )

    st.success("Dados carregados")

    # -------------------------
    # MATRIZ DE VIZINHANÇA
    # -------------------------
    w = criar_matriz_vizinhanca(
        gdf,
        metodo=vizinhanca,
        k=k
    )

    # -------------------------
    # MODELOS
    # -------------------------
    if modelo == "Taxa bruta":

        st.subheader("Mapa de taxa bruta")

        fig, ax = plt.subplots()
        gdf.plot(
            column="taxa",
            cmap="OrRd",
            legend=True,
            ax=ax
        )
        st.pyplot(fig)

    # -------------------------
    elif modelo == "Empirical Bayes":

        st.subheader("Mapa – Empirical Bayes")

        gdf = suavizar_taxa_empirical_bayes(
            gdf,
            casos="n_casos",
            populacao="n_nascidos_vivos"
        )

        fig, ax = plt.subplots()
        gdf.plot(
            column="taxa_suavizada",
            cmap="OrRd",
            legend=True,
            ax=ax
        )
        st.pyplot(fig)

    # -------------------------
    elif modelo == "Moran / LISA":

        st.subheader("Autocorrelação espacial")

        I, p = moran_global(gdf, "taxa", w)
        st.metric("Moran's I", f"{I:.3f}", f"p={p:.4f}")

        gdf = lisa_local(gdf, "taxa", w)

        fig, ax = plt.subplots()
        gdf.plot(
            column="lisa_cluster",
            categorical=True,
            legend=True,
            ax=ax
        )
        st.pyplot(fig)

    # -------------------------
    elif modelo == "BYM (Bayesiano)":

        st.subheader("Modelo Bayesiano Espacial (BYM)")

        with st.spinner("Rodando inferência bayesiana (isso pode demorar)..."):

            model, trace = modelo_bym(
                casos=gdf["n_casos"].values,
                populacao=gdf["n_nascidos_vivos"].values,
                W=w
            )

        rr = extrair_risco_relativo(trace)

        gdf["RR_bayes"] = rr["RR_mean"]

        fig, ax = plt.subplots()
        gdf.plot(
            column="RR_bayes",
            cmap="RdBu_r",
            legend=True,
            ax=ax
        )
        st.pyplot(fig)

        st.subheader("Diagnóstico do modelo")
        st.dataframe(diagnostico_bym(trace))
