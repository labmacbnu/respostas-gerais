import streamlit as st 
import json
import pandas as pd
import plotly.express as px
import requests
from datafunc import dados_df



if __name__ == "__main__":
    df_origin = dados_df()
    escolaridade = st.selectbox("Escolha uma cidade", df_origin.escolaridade.unique())
    df = df_origin.query("escolaridade == @escolaridade")
   
    f"""# Respostas Gerais"""

    tab_graficos, tab_tabelas = st.tabs(["Gráficos", "Tabelas"])
    agrupados = df.groupby("curso").agg({"stamp": 'count'}).sort_values(by='stamp', ascending=False).reset_index().rename(columns={'stamp': 'quantidade'})
    with tab_graficos:
        "### 10 cursos mais escolhidos"
        fig = px.bar(agrupados.head(n=10).reset_index(),
             x='curso', y='quantidade')
        st.plotly_chart(fig, use_container_width=True)

    with tab_tabelas:
        st.caption("Clique nas colunas da tabela para ordenar os dados")
        st.dataframe(agrupados)