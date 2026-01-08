# Análise Espacial de Malformações Congênitas (SINASC)

Este projeto é uma aplicação interativa desenvolvida em Python com **Streamlit** para análise espacial de dados de malformações congênitas do **SINASC** (Sistema de Informações sobre Nascidos Vivos).

A ferramenta permite visualizar a distribuição espacial das taxas de malformações, aplicar técnicas de suavização estatística e identificar clusters espaciais significativos no Brasil.

## 🎯 Funcionalidades

*   **Visualização de Dados**:
    *   Mapas coropléticos estáticos (Matplotlib) com classificação por quartis.
    *   Seleção dinâmica de ano (2000-2024) e CID-10 (Capítulo XVII).
    *   Análise por Município ou Estado (UF).

*   **Análise Espacial**:
    *   **Taxa Bruta**: Cálculo da incidência por 100.000 nascidos vivos.
    *   **Matriz de Vizinhança**: Definição de pesos espaciais via critério *Queen* (contiguidade) ou *KNN* (vizinhos mais próximos).
    *   **Autocorrelação Global (Moran's I)**: Medida estatística para verificar se os dados são aleatórios ou agrupados espacialmente.
    *   **Clusters Locais (LISA)**: Identificação de *hotspots* (Alto-Alto), *coldspots* (Baixo-Baixo) e outliers espaciais.

*   **Suavização Estatística**:
    *   **Empirical Bayes**: Método para correção de instabilidade das taxas em municípios com populações pequenas, reduzindo o efeito de flutuações aleatórias.

## 🛠️ Tecnologias Utilizadas

*   **Interface**: [Streamlit](https://streamlit.io/)
*   **Processamento de Dados**: [Polars](https://pola.rs/) e [Pandas](https://pandas.pydata.org/)
*   **Geoprocessamento**: [Geopandas](https://geopandas.org/) e [Geobr](https://github.com/ipeaGIT/geobr)
*   **Estatística Espacial**: [PySAL](https://pysal.org/) (`esda`, `libpysal`)
*   **Visualização**: Matplotlib
*   **Get Data**: QDS(Quadros de saude)

## 🚀 Como Executar

### Pré-requisitos

Certifique-se de ter o Python instalado (recomendado 3.10+).

1.  **Clone o repositório**:
    ```bash
    git clone https://github.com/seu-usuario/maformacoes-python.git
    cd maformacoes-python
    ```

2.  **Crie um ambiente virtual (opcional, mas recomendado)**:
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # Linux/Mac
    # ou
    .venv\Scripts\activate     # Windows
    ```

3.  **Instale as dependências**:
    ```bash
    pip install streamlit geopandas pandas polars matplotlib libpysal esda geobr
    ```

4.  **Execute a aplicação**:
    ```bash
    streamlit run app.py
    ```

## 📂 Estrutura do Projeto

```text
maformacoes-python/
├── app.py                      # Aplicação principal (Streamlit)
├── scripts/
│   ├── analise_espacial.py     # Funções de Moran, LISA, Bayes e Mapas
│   ├── taxas.py                # Pipeline de cálculo de taxas (Polars)
│   ├── io.py                   # Leitura de dados (SINASC)
│   ├── tempo.py                # Tratamento temporal
│   ├── derivacoes.py           # Criação de variáveis auxiliares
│   └── indicadores.py          # Lógica de filtro por CID
└── README.md                   # Documentação do projeto
```

## 📊 Fonte de Dados

Os dados utilizados provêm do **SINASC** (Ministério da Saúde/DATASUS). A aplicação espera que os dados brutos ou pré-processados estejam acessíveis através do módulo `scripts.io`.

---

**Nota**: Este projeto é voltado para pesquisa acadêmica e epidemiológica.