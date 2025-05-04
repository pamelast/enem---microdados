import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Título do dashboard
st.title("Dashboard Simples com Streamlit")

# Geração de dados fictícios
@st.cache_data
def gerar_dados():
    np.random.seed(42)
    datas = pd.date_range(start="2024-01-01", periods=100)
    categorias = ["A", "B", "C"]
    dados = {
        "Data": np.random.choice(datas, 300),
        "Categoria": np.random.choice(categorias, 300),
        "Valor": np.random.randint(10, 100, 300)
    }
    return pd.DataFrame(dados)

df = gerar_dados()

# Filtros interativos
st.sidebar.header("Filtros")
categoria_selecionada = st.sidebar.multiselect(
    "Categoria", options=df["Categoria"].unique(), default=df["Categoria"].unique()
)
data_min = df["Data"].min()
data_max = df["Data"].max()
data_range = st.sidebar.date_input("Período", [data_min, data_max])

# Aplicar filtros
df_filtrado = df[
    (df["Categoria"].isin(categoria_selecionada)) &
    (df["Data"] >= pd.to_datetime(data_range[0])) &
    (df["Data"] <= pd.to_datetime(data_range[1]))
]

# Mostrar tabela
st.subheader("Dados Filtrados")
st.dataframe(df_filtrado)

# Gráfico de barras
st.subheader("Soma dos Valores por Categoria")
df_agg = df_filtrado.groupby("Categoria")["Valor"].sum().reset_index()
fig = px.bar(df_agg, x="Categoria", y="Valor", color="Categoria", title="Total por Categoria")
st.plotly_chart(fig)

# Gráfico de linha
st.subheader("Evolução dos Valores ao Longo do Tempo")
df_tempo = df_filtrado.groupby("Data")["Valor"].sum().reset_index()
fig2 = px.line(df_tempo, x="Data", y="Valor", title="Soma dos Valores por Data")
st.plotly_chart(fig2)