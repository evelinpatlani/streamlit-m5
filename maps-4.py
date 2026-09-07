import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# CORRECCIÓN: URL oficial estática de GitHub para leer archivos crudos
DATA_URL = 'https://raw.githubusercontent.com/evelinpatlani/Dataset_CreditCard/main/creditcard.zip'

@st.cache_data
def load_data(number_rows):
    # Pandas descargará el zip y leerá el CSV interno
    data = pd.read_csv(DATA_URL, compression='zip', nrows=number_rows)
    return data

st.set_page_config(layout="wide")
st.title('Análisis de Transacciones - Tarjetas de Crédito')

try:
    # Cargamos más filas para que las gráficas tengan sentido estadístico
    data = load_data(10000) 

    st.subheader('Datos Crudos (Muestra)')
    st.dataframe(data.head(100))

    st.markdown("---")

    # --- FASE 2: GRÁFICAS DE MATPLOTLIB ---
    st.header('Visualizaciones de los Datos')
    
    col1, col2 = st.columns(2)

    with col1:
        st.subheader('Distribución de Transacciones')
        # Verificamos que la columna 'Class' exista (0 = Normal, 1 = Fraude)
        if 'Class' in data.columns:
            fig1, ax1 = plt.subplots(figsize=(6, 4))
            conteo_clases = data['Class'].value_counts()
            
            # Gráfica de barras
            ax1.bar(['Normales (0)', 'Fraudes (1)'], conteo_clases.values, color=['seagreen', 'crimson'])
            ax1.set_ylabel('Cantidad de Transacciones')
            
            st.pyplot(fig1)
        else:
            st.warning("No se encontró la columna 'Class' en el dataset.")

    with col2:
        st.subheader('Distribución de Montos (Amount)')
        if 'Amount' in data.columns:
            fig2, ax2 = plt.subplots(figsize=(6, 4))
            
            # Histograma de los montos
            ax2.hist(data['Amount'], bins=30, color='steelblue', edgecolor='black')
            ax2.set_xlabel('Monto de la Transacción ($)')
            ax2.set_ylabel('Frecuencia')
            
            st.pyplot(fig2)
        else:
            st.warning("No se encontró la columna 'Amount' en el dataset.")

except Exception as e:
    st.error(f"Hubo un error al intentar descargar o leer los datos: {e}")
    st.info("Verifica que el repositorio sea público y que el archivo creditcard.zip exista en la rama 'main'.")