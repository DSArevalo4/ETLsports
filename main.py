import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import os

# Configuración de la página
st.set_page_config(page_title="ETL NBA Player Stats", layout="wide")

st.title("ETL NBA Player Stats ")

# Directorio donde se encuentran los archivos
DATA_DIR = '/workspaces/ETLsports/NBAplayers'

# Listar los archivos disponibles en la carpeta
csv_files = [f for f in os.listdir(DATA_DIR) if f.lower().endswith(".xlsx") and os.path.isfile(os.path.join(DATA_DIR, f))]

if not csv_files:
    st.warning("No hay archivos .xlsx en la carpeta indicada.")
    st.stop()

# Seleccionar un archivo de la lista
uploaded_file = st.selectbox("Selecciona un archivo", csv_files)

if uploaded_file is not None:
    # Cargar el archivo Excel
    df = pd.read_excel(os.path.join(DATA_DIR, uploaded_file))
    st.write(f"Filas antes de limpieza: {df.shape[0]}, Columnas: {df.shape[1]})")

    # Limpieza de datos (normalización, eliminar duplicados, NA)
    st.subheader("Vista previa de los datos cargados")
    st.dataframe(df.head(50))

    # Limpiar datos: eliminar duplicados, eliminar NA
    df_cleaned = df.dropna().drop_duplicates()  
    st.write(f"Filas después de limpieza: {df_cleaned.shape[0]}, Columnas: {df_cleaned.shape[1]})")

    st.dataframe(df_cleaned.head(50))

    # Gráficos con Seaborn
    st.subheader("Gráficos de los datos limpios")

    # 1. Distribución de la Edad de los Jugadores
    plt.figure(figsize=(10, 6))
    sns.histplot(df_cleaned['Age'], kde=True, color="skyblue", bins=30)
    plt.title("Distribución de la Edad de los Jugadores")
    plt.xlabel("Edad")
    plt.ylabel("Frecuencia")
    st.pyplot(plt)

    # 2. Relación entre Rebotes (TRB) y Puntos (PTS)
    if 'TRB' in df_cleaned.columns and 'PTS' in df_cleaned.columns:
        plt.figure(figsize=(10, 6))
        sns.scatterplot(x=df_cleaned['TRB'], y=df_cleaned['PTS'], color="green")
        plt.title("Relación entre Rebotes (TRB) y Puntos (PTS)")
        plt.xlabel("Rebotes")
        plt.ylabel("Puntos")
        st.pyplot(plt)

    # Mapeo de posiciones
    position_map = {
        'PF': 'Ala-pívot',
        'SG': 'Escolta',
        'C': 'Pívot',
        'PG': 'Base',
        'SF': 'Alero'
    }

    # Reemplazar las abreviaturas por los nombres completos en la columna 'Pos'
    df_cleaned['Pos'] = df_cleaned['Pos'].map(position_map).fillna(df_cleaned['Pos'])
    # 3. Conteo de Jugadores por Posición (Gráfico de pastel)
    pos_counts = df_cleaned['Pos'].value_counts()

    # Crear el gráfico de pastel
    plt.figure(figsize=(8, 8))
    plt.pie(pos_counts, labels=pos_counts.index, autopct='%1.1f%%', startangle=90, colors=sns.color_palette("Set2", len(pos_counts)))
    plt.title("Distribución de Jugadores por Posición")
    plt.axis('equal')  # Para que el gráfico sea circular
    st.pyplot(plt)


else:
    st.warning("Por favor, selecciona un archivo de la lista.")
