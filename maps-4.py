import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

DATA_URL = 'uber-raw-data-sep14.csv'
DATE_COLUMN = 'Date/Time'

# Configuración de la página para que use todo el ancho (opcional pero recomendado para dashboards)
st.set_page_config(layout="wide")

@st.cache_data
def load_data(number_rows):
    data = pd.read_csv(DATA_URL, nrows=number_rows)
    lowercase = lambda x: str(x).lower()
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    data.rename(lowercase, axis='columns', inplace=True)
    return data

st.title('Análisis de Datos de Uber - NY')

# Cargar datos
data = load_data(1000) 

# --- SECCIÓN 1: DATOS Y MAPA ---
col1, col2 = st.columns(2)

with col1:
    st.subheader('Datos Crudos (1000 filas)')
    st.dataframe(data, height=400)

with col2:
    st.subheader('Mapa de Viajes')
    st.map(data)

st.markdown("---") # Línea divisoria

# --- SECCIÓN 2: GRÁFICAS DE MATPLOTLIB ---
st.header('Análisis Temporal')

# Crear 3 columnas para las gráficas
g_col1, g_col2, g_col3 = st.columns(3)

# 1. Gráfica: Viajes por Hora
with g_col1:
    st.subheader('Por Hora')
    hist_hour = np.histogram(data['date/time'].dt.hour, bins=24, range=(0, 24))[0]
    
    fig_hour, ax_hour = plt.subplots(figsize=(6, 4))
    ax_hour.bar(range(24), hist_hour, color='steelblue')
    ax_hour.set_xlabel('Hora')
    ax_hour.set_ylabel('Viajes')
    st.pyplot(fig_hour)

# 2. Gráfica: Viajes por Día de la Semana
with g_col2:
    st.subheader('Por Día de la Semana')
    # dayofweek devuelve 0 (Lunes) a 6 (Domingo)
    hist_day = np.histogram(data['date/time'].dt.dayofweek, bins=7, range=(-0.5, 6.5))[0]
    dias = ['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom']
    
    fig_day, ax_day = plt.subplots(figsize=(6, 4))
    ax_day.bar(dias, hist_day, color='seagreen')
    ax_day.set_xlabel('Día')
    ax_day.set_ylabel('Viajes')
    st.pyplot(fig_day)

# 3. Gráfica: Viajes por Minuto
with g_col3:
    st.subheader('Por Minuto')
    hist_minute = np.histogram(data['date/time'].dt.minute, bins=60, range=(0, 60))[0]
    
    fig_minute, ax_minute = plt.subplots(figsize=(6, 4))
    # Usamos plot en lugar de bar para ver la tendencia continua
    ax_minute.plot(range(60), hist_minute, color='crimson')
    ax_minute.set_xlabel('Minuto (0-59)')
    ax_minute.set_ylabel('Viajes')
    st.pyplot(fig_minute)