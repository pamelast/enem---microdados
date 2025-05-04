import pandas as pd
import numpy as np

import streamlit as st
import plotly.express as px


@st.cache_data()
def gera_dataframe_principal():
    df = pd.read_parquet('MICRODADOS_ENEM_2021.parquet')
    df = df.sample(50_000, random_state = 42)
    r = {0: "Não Declarado", 
                 1: "Branca", 
                 2: "Preta", 
                 3: "Parda", 
                 4: "Amarela", 
                 5: "Indígena", 
                 6: "Sem Informação"}
    df['TP_COR_RACA'] = df['TP_COR_RACA'].replace(r)
    return df

df = gera_dataframe_principal()

st.sidebar.header("Filtros")
genero_selecionado = st.sidebar.multiselect(
    "GENERO", options=df["TP_SEXO"].unique(), default=df['TP_SEXO'].unique()
)
cor_selecionada = st.sidebar.multiselect(
    "COR", options = df['TP_COR_RACA'].unique(), default = df['TP_COR_RACA'].unique()
)
ano_conclusao = st.sidebar.slider("CONCLUIU O E.M EM ATE ", 0, 110)
nota_mat = st.sidebar.slider('NOTA MINIMA MAT', 0, 1000)
nota_redacao = st.sidebar.slider('NOTA MINIMA REDACAO', 0, 1000)
nota_ch = st.sidebar.slider('NU_NOTA_CH', 0, 1000)

mask = f'(TP_SEXO in {genero_selecionado}) & (TP_COR_RACA in {cor_selecionada}) & (TP_ANO_CONCLUIU <= {ano_conclusao}) & (NU_NOTA_REDACAO >= {nota_redacao}) & (NU_NOTA_MT >= {nota_mat}) & (NU_NOTA_CH >= {nota_ch})'
# df_redacao = pd.crosstab(index = pd.cut(df.query(mask)['NU_NOTA_REDACAO'], bins = [-1, 100, 200, 300, 500, 600, 700, 800, 900, 1000],
#                                        labels = ['F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9']), 
#             columns = 'quant', normalize = True)
# df_mat = pd.crosstab(index = pd.cut(df.query(mask)['NU_NOTA_MT'], bins = [-1, 100, 200, 300, 500, 600, 700, 800, 900, 1000],
#                                        labels = ['F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9']), 
#             columns = 'quant', normalize = True)
# df_ch = pd.crosstab(index = pd.cut(df.query(mask)['NU_NOTA_CH'], bins = [-1, 100, 200, 300, 500, 600, 700, 800, 900, 1000],
#                                        labels = ['F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9']), 
#             columns = 'quant', normalize = True)


# tab1, tab2, tab3 = st.tabs(["Redação", "Matematica", 'Humanas'])
# tab1.dataframe(df_redacao, use_container_width=False, height=350, width = 400)
# tab2.dataframe(df_mat, use_container_width=False, height=350, width = 400)
# tab3.dataframe(df_ch, use_container_width=False, height=350, width = 400)

df_media = pd.DataFrame(df.query(mask)[['NU_NOTA_REDACAO', 'NU_NOTA_MT', 'NU_NOTA_CH']].mean()).reset_index().rename(columns = {0:'Media', 'index':'Caderno'}).round(2)
fig_media = px.bar(df_media, x = 'Caderno', y = 'Media')

st.write('Base selecionada', df.query(mask).shape[0])
st.subheader('Media de Notas')
tab1, tab2 = st.tabs(["DataFrame", "Plot"])
tab1.dataframe(df_media, height = 200, width = 400)
tab2.plotly_chart(fig_media)