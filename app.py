import streamlit as st
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import streamlit.components.v1 as components

from scripts.taxas import obter_taxa_sinasc
from scripts.analise_espacial import (
    criar_matriz_vizinhanca,
    suavizar_taxa_empirical_bayes,
    moran_global,
    lisa_local,
    plotar_mapa_quartis
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

with st.sidebar.expander("ℹ️ Dicionário de CIDs (SINASC)"):
    st.markdown("**Capítulo XVII - Malformações (Q00-Q99)**")
    dados_cid = {
        "Código": ["Q00-Q07", "Q10-Q18", "Q20-Q28", "Q30-Q34", "Q35-Q37", "Q38-Q45", "Q50-Q56", "Q60-Q64", "Q65-Q79", "Q80-Q89", "Q90-Q99"],
        "Grupo": ["Sistema nervoso", "Olho, ouvido, face e pescoço", "Aparelho circulatório", "Aparelho respiratório", "Fenda labial e palatina", "Aparelho digestivo", "Órgãos genitais", "Aparelho urinário", "Sistema osteomuscular", "Outras malformações", "Anomalias cromossômicas"]
    }
    st.dataframe(pd.DataFrame(dados_cid), hide_index=True, use_container_width=True)

usar_todas = st.sidebar.checkbox("Todas as malformações (Cap. Q)", value=False)

if usar_todas:
    cid = "Q"
    st.sidebar.caption("Analisando todo o Capítulo XVII (Q00-Q99)")
else:
    cid = st.sidebar.text_input("CID ou Prefixo (ex: Q20, Q2)", value="Q20", help="Digite o código completo (Q20) ou o prefixo para agrupar (ex: 'Q2' seleciona Q20-Q29).")

lista_anos = list(range(2024, 1999, -1))
ano = st.sidebar.selectbox(
    "Ano",
    options=lista_anos,
    index=lista_anos.index(2022)
)

estrato = st.sidebar.selectbox(
    "Estrato espacial",
    ["Município", "Estado"]
)
coluna_estrato = "CODMUNRES" if estrato == "Município" else "UFINFORM"

modelo = st.sidebar.selectbox(
    "Modelo espacial",
    [
        "Taxa bruta",
        "Empirical Bayes",
        "Moran / LISA"
    ]
)

cmap = st.sidebar.selectbox(
    "Paleta de cores",
    ["YlOrRd", "OrRd", "PuBu", "Blues", "Viridis", "Plasma", "RdBu_r"]
)

vizinhanca = st.sidebar.selectbox(
    "Tipo de vizinhança",
    ["queen", "knn"]
)

k = None
if vizinhanca == "knn":
    k = st.sidebar.slider("k vizinhos", 2, 12, 8)

executar = st.sidebar.button("Executar análise")

if executar:

    st.info("Carregando e preparando dados...")

    anos = [ano]

    gdf = obter_taxa_sinasc(
        anos=anos,
        cid=cid,
        tempo="ano",
        estratos=[coluna_estrato],
        retorno="geopandas"
    )

    # --- INSPEÇÃO DE DADOS (DEBUG) ---
    with st.expander("🔍 Inspeção de Dados (Verificar Cruzamento)", expanded=True):
        st.write("Amostra do GeoDataFrame carregado:")
        st.dataframe(gdf.head())
        
        total_mun = len(gdf)
        # Verifica quantos municípios têm taxa não nula
        com_dados = gdf["taxa_por_100000"].notna().sum()
        
        st.metric("Municípios na Malha", total_mun)
        st.metric("Municípios com Dados Cruzados", com_dados, delta=f"{com_dados - total_mun}")
        
        if com_dados == 0:
            st.error("⚠️ ALERTA: Nenhum dado foi cruzado! O mapa ficará cinza. Verifique se os códigos de município do SINASC batem com os do IBGE (6 dígitos).")

    # Mapa Inicial (Estilo Matplotlib conforme notebook)
    st.subheader(f"Mapa de Taxa Bruta ({ano})")
    fig, ax = plt.subplots(figsize=(10, 8))
    plotar_mapa_quartis(
        gdf,
        coluna="taxa_por_100000",
        ax=ax,
        cmap=cmap,
        titulo_legenda="Quartis (Taxa)"
    )
    ax.axis("off")
    st.pyplot(fig)

    st.success("Dados carregados")

    w = criar_matriz_vizinhanca(
        gdf,
        metodo=vizinhanca,
        k=k
    )

    # MODELOS

    if modelo == "Empirical Bayes":

        st.subheader("Mapa – Empirical Bayes")

        gdf = suavizar_taxa_empirical_bayes(
            gdf,
            casos="n_casos",
            populacao="n_nascidos_vivos"
        )

        fig, ax = plt.subplots(figsize=(10, 8))
        plotar_mapa_quartis(
            gdf,
            coluna="taxa_suavizada",
            ax=ax,
            cmap=cmap,
            titulo_legenda="Quartis (EB)",
            fmt="{:.1f}"
        )
        ax.axis("off")
        st.pyplot(fig)

    # -------------------------
    elif modelo == "Moran / LISA":

        st.subheader("Autocorrelação espacial")

        I, p = moran_global(gdf, "taxa_por_100000", w)
        st.metric("Moran's I", f"{I:.3f}", f"p={p:.4f}")

        gdf = lisa_local(gdf, "taxa_por_100000", w)

        # Plotagem manual para garantir as cores padrão (HH=Vermelho, LL=Azul)
        fig, ax = plt.subplots(figsize=(10, 10))
        
        # 1. Fundo (Não significante)
        ns = gdf[gdf['lisa_cluster'] == 'Não significante']
        if not ns.empty:
            ns.plot(ax=ax, color='lightgrey', edgecolor='white', linewidth=0.1, label='Não significante')
            
        # 2. Alto-Alto (HH) - Vermelho
        hh = gdf[gdf['lisa_cluster'] == 'HH']
        if not hh.empty:
            hh.plot(ax=ax, color='#d7191c', edgecolor='black', linewidth=0.3, label='Alto-Alto (HH)')
            
        # 3. Baixo-Baixo (LL) - Azul
        ll = gdf[gdf['lisa_cluster'] == 'LL']
        if not ll.empty:
            ll.plot(ax=ax, color='#2c7bb6', edgecolor='black', linewidth=0.3, label='Baixo-Baixo (LL)')
            
        # 4. Baixo-Alto (LH) - Azul Claro
        lh = gdf[gdf['lisa_cluster'] == 'LH']
        if not lh.empty:
            lh.plot(ax=ax, color='#abd9e9', edgecolor='black', linewidth=0.3, label='Baixo-Alto (LH)')
            
        # 5. Alto-Baixo (HL) - Laranja/Amarelo
        hl = gdf[gdf['lisa_cluster'] == 'HL']
        if not hl.empty:
            hl.plot(ax=ax, color='#fdae61', edgecolor='black', linewidth=0.3, label='Alto-Baixo (HL)')

        # Legenda manual no canto
        ax.legend(loc='lower right', title="Clusters LISA")
        ax.axis("off")
        st.pyplot(fig)
