import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

DATA_URL = 'uber-raw-data-sep14.csv'
DATE_COLUMN = 'Date/Time'

@st.cache_data
def load_data(number_rows):
    data = pd.read_csv(DATA_URL, nrows=number_rows)
    lowercase = lambda x: str(x).lower()
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    data.rename(lowercase, axis='columns', inplace=True)
    return data

# Título de la aplicación
st.title('Análisis de Datos de Uber')

# 1. Cargar y mostrar los datos crudos
st.subheader('Datos Crudos (1000 filas)')
data = load_data(1000) 
st.dataframe(data)

# 2. Mostrar el mapa
st.subheader('Mapa de Viajes')
st.map(data)

# 3. Crear y mostrar la gráfica con Matplotlib
st.subheader('Número de viajes por hora')

# Extraer la hora de la columna de fecha (que ahora se llama 'date/time' por el lowercase)
# Utilizamos numpy para hacer un histograma rápido de 24 rangos (uno por hora)
hist_values = np.histogram(data['date/time'].dt.hour, bins=24, range=(0, 24))[0]

# Crear la figura y el eje de Matplotlib (Forma estricta y segura para web)
fig, ax = plt.subplots(figsize=(10, 4))
ax.bar(range(24), hist_values, color='steelblue')
ax.set_xlabel('Hora del día')
ax.set_ylabel('Cantidad de viajes')
ax.set_title('Viajes por Hora')
ax.set_xticks(range(0, 24))

# Pasar la figura de Matplotlib a Streamlit
st.pyplot(fig)