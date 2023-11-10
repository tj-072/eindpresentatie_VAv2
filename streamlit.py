import pandas as pd
import geopandas as gpd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pyproj import Transformer
import plotly.graph_objects as go
import streamlit as st

api_data = pd.read_csv('apidata_2021.csv')
api_data = api_data.drop(columns=['Unnamed: 0'])
api_data['datetime'] = pd.to_datetime(api_data['datetime'])
api_data = api_data.groupby([api_data['datetime'].dt.date, api_data['station_id']])[['Windsnelheid (km/h)', 'Windrichting (Graden)', 'Luchtdruk (ps)', 'Zichtbaarheid (Decimeter ver kunnen kijken)', 'Regenval (mm/h)', 'Temperatuur (C)',	'Weercode']].mean().reset_index()
api_data['station_id'] = api_data['station_id'].astype(str)


tab1, tab2, tab3 = st.tabs(['Gegevens KNMI Weer', 'Gegevens ongelukken', 'Vegelijking'])

with tab1:
    st.title('Gegevens KNMI weer')

    st.subheader('Kaart met weerstations per datum')
    

    st.subheader('Lijndiagram')
    Weermeting = st.selectbox('Selecteer weermeting:', key='Weermeting', options=('Windsnelheid (km/h)', 'Windrichting (Graden)', 'Luchtdruk (ps)', 'Zichtbaarheid (Decimeter ver kunnen kijken)', 'Regenval (mm/h)',	'Temperatuur (C)', 'Weercode'))
    Station = st.selectbox('Selecteer station:', key='Station', options=('6209', '6225', '6235', '6240', '6242', '6248'
                                                                , '6249', '6257','6258', '6260', '6267'))

    station_filter = api_data[api_data['station_id'] == Station]
    titel = Weermeting+' voor station '+Station

    fig = plt.figure()
    ax = sns.lineplot(data=station_filter, x='datetime', y=Weermeting)
    ax.set(title=titel)
    ax.set_xticks(['2021-01-15', '2021-02-15', '2021-03-15', '2021-04-15', '2021-05-15','2021-06-15',
                '2021-07-15', '2021-08-15','2021-09-15', '2021-10-15','2021-11-15', '2021-12-15'])
    ax.set_xticklabels(['2021-01', '2021-02', '2021-03', '2021-04', '2021-05','2021-06',
                '2021-07', '2021-08','2021-09', '2021-10','2021-11', '2021-12'])

    ax.tick_params(axis='x', rotation=45)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0)

    st.pyplot(fig)

    st.write("""
    In de bovenstaande lijndiagram is per weermeting de verloop over het jaar 2021 te zien. Om de verschillende
            stations met elkaar te vergelijken is het mogelijk om ze individueel te observeren. We hebben
            deze keuze gemaakt omdat, wanneer alle stations geselecteerd zijn de diagram onoverzichtelijk wordt.
            Niet elk station heeft alle waardes gemeten, daarom zullen er ook vlakke lijnen tussen staan.
    """)

    st.subheader('Histogram')

    fig1 = plt.figure()
    ax = sns.boxplot(data=api_data, y=Weermeting, hue='station_id')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0)
    st.pyplot(fig1)

    st.write("""
    In de bovenstaande boxplot is te zien hoe verschillende metingen zijn verdeeld. Door deze
            visualisatie is goed te zien op welke manier de temperatuur, windsnelheid etc. opgedeeld is.
    """)

    st.subheader('Normaalverdeling')
    zonder_nul = st.checkbox('Zonder nul')

    if zonder_nul == False:
        fig2 = plt.figure()
        sns.histplot(data=station_filter, x=Weermeting)
        st.pyplot(fig2)

    if zonder_nul:
        fig3 = plt.figure()
        zonder_nul_frame = station_filter[station_filter[Weermeting] > 0]
        sns.histplot(data=zonder_nul_frame, x=Weermeting)
        st.pyplot(fig3)

    st.write("""
            In de bovenstaande visualisatie is een normaalverdeling te zien. Sommige gegevens waren
            origineel een NaN en zijn vervangen met een 0, om deze nullen weg te nemen is het mogelijk om dat te doen
            via de 'Zonder nul' knop. Door deze visualisatie is goed te zien wat normaal is voor dat gegeven en weerstation.
    """)



with tab2:
    st.write('Gegevens ongelukken 2021')

with tab3:
    st.write('Vergelijkingen tussen weer en ongelukken')
