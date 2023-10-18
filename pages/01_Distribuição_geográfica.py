import streamlit as st
import folium
import pandas as pd 

from streamlit_folium import st_folium

from datafunc import dados_df, brazil_geojson



if __name__ == "__main__":

    df = dados_df() 
    
    tab_mapas, tab_tabelas = st.tabs(["Mapas", "Tabelas"])
    
    with tab_tabelas:
        "## Cidades" 
        cidades = df.groupby(["estado", "cidade"]).agg({"stamp": "count"}).reset_index()
        cidades.columns = ["estado", "cidade", "contagem"]

        st.dataframe(cidades)
 
    with tab_mapas:
        "## Cidades"  
        estados = df.estado.unique()
        IDS = [x for x in df.codigo.unique() if x > 0 ]
        BOUNDARIES = brazil_geojson()  
        features_colection = [] 
        for codarea in IDS:
            cidade = df.query(f"codigo == {codarea}").iloc[0].cidade
            filtro = filter( lambda x: x['properties']['codarea'] == str(codarea), BOUNDARIES['features'])
            filtrado  = next(filtro, None)
            if filtrado is None:
                print(f"Erro ao buscar {codarea}")
                continue
            props = filtrado.copy()
            props['properties']["quantidade"] = df.query(f"codigo == {codarea}").agg({"stamp": 'count'}).tolist()[0]
            props['properties']["município"] = cidade
            features_colection.append(props) 
        SEMI_BOUNDARIES = {"type":"FeatureCollection", "features":  features_colection}
        #[ x for x in BOUNDARIES['features'] if x['properties']['id'] in IDS ] }

        abrangencia_mapa = folium.Map(width=800,height=400,location=[-26.872752975560978, -49.094156560879235],
                            zoom_start = 12, tiles="cartodbpositron") 
        
        COLOR_MAP = dict(zip( [0, 5, 10, 20, 40, 90], ['#d1e5f0','#92c5de','#4393c3','#2166ac','#053061'])) 
          
        def color_func(n: int):
            cor_final = ""
            for k, cor in COLOR_MAP.items():
                if n >= k:
                    cor_final = cor
            return cor_final



        style_function = lambda x: {
            "fillColor": color_func(x["properties"]["quantidade"]) ,
            'color': '#333333',
            'weight': 0.4,
            'fillOpacity': 0.9

        }
        folium.GeoJson(
            data=SEMI_BOUNDARIES,  
            name="Quantidade de respostas",
            style_function=style_function,
            popup=folium.GeoJsonPopup(fields=["município", "quantidade"])
        ).add_to(abrangencia_mapa)

        abrangencia_mapa.fit_bounds(abrangencia_mapa.get_bounds(), padding=(0.05,0.05))
        ST_MAPA = st_folium(abrangencia_mapa)
 
