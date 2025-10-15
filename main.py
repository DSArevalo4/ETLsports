import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from pathlib import Path
import time

# Configuración de la página
st.set_page_config(page_title="ETL Stock Sentiment Analysis", layout="wide", page_icon="📈")

st.title("📈 ETL Stock Sentiment Analysis")
st.markdown("### Pipeline de Análisis de Sentimientos de Acciones")

# Directorio donde se encuentran los archivos
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / 'data' / 'input'

# Crear directorio si no existe
DATA_DIR.mkdir(parents=True, exist_ok=True)

# Listar archivos CSV disponibles
csv_files = [f.name for f in DATA_DIR.glob("*.csv")]

if not csv_files:
    st.warning("⚠️ No hay archivos CSV en la carpeta `data/input/`. Por favor, añade archivos para analizar.")
    st.info("💡 Coloca el archivo `stock_senti_analysis.csv` en la carpeta `data/input/`")
    st.stop()

# Seleccionar archivo
uploaded_file = st.selectbox("📁 Selecciona un archivo CSV", csv_files)

if uploaded_file:
    try:
        # Cargar el archivo CSV con manejo robusto de errores
        file_path = DATA_DIR / uploaded_file
        
        # Intentar leer el archivo con múltiples estrategias
        max_retries = 3
        retry_delay = 1
        df = None
        
        for attempt in range(max_retries):
            try:
                df = pd.read_csv(file_path, encoding='utf-8')
                break
            except PermissionError:
                if attempt < max_retries - 1:
                    st.warning(f"⚠️ El archivo está siendo usado por otro programa. Reintentando ({attempt + 1}/{max_retries})...")
                    time.sleep(retry_delay)
                else:
                    st.error("❌ No se puede acceder al archivo. Por favor:")
                    st.markdown("""
                    1. **Cierra Excel** si tienes el archivo abierto
                    2. **Cierra el Explorador de Windows** si está previsualizando el archivo
                    3. **Recarga esta página** (F5)
                    
                    O intenta con otro archivo CSV.
                    """)
                    st.stop()
            except UnicodeDecodeError:
                try:
                    df = pd.read_csv(file_path, encoding='latin-1')
                    break
                except:
                    df = pd.read_csv(file_path, encoding='ISO-8859-1')
                    break
        
        if df is None:
            st.error("❌ No se pudo cargar el archivo después de varios intentos.")
            st.stop()
        
        st.success(f"✅ Archivo cargado: **{uploaded_file}**")
        st.write(f"📊 **Dimensiones originales:** {df.shape[0]} filas × {df.shape[1]} columnas")
        
        # Mostrar primeras filas
        with st.expander("👀 Vista previa de datos originales", expanded=True):
            st.dataframe(df.head(20), use_container_width=True)
        
        # TRANSFORMACIÓN Y LIMPIEZA
        st.subheader("🧹 Transformación de Datos")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            remove_duplicates = st.checkbox("Eliminar duplicados", value=True)
        with col2:
            remove_na = st.checkbox("Eliminar valores nulos", value=True)
        with col3:
            normalize_cols = st.checkbox("Normalizar columnas", value=True)
        
        # Aplicar transformaciones
        df_clean = df.copy()
        
        # Normalizar nombres de columnas
        if normalize_cols:
            df_clean.columns = df_clean.columns.str.strip().str.replace(' ', '_')
        
        # Parsear fechas si existe columna Date
        date_cols = [col for col in df_clean.columns if 'date' in col.lower()]
        if date_cols:
            df_clean[date_cols[0]] = pd.to_datetime(df_clean[date_cols[0]], errors='coerce')
        
        # Eliminar duplicados
        if remove_duplicates:
            before_dup = len(df_clean)
            df_clean = df_clean.drop_duplicates()
            st.info(f"🗑️ Duplicados eliminados: {before_dup - len(df_clean)}")
        
        # Eliminar NA
        if remove_na:
            before_na = len(df_clean)
            df_clean = df_clean.dropna()
            st.info(f"🗑️ Filas con NA eliminadas: {before_na - len(df_clean)}")
        
        st.write(f"📊 **Dimensiones finales:** {df_clean.shape[0]} filas × {df_clean.shape[1]} columnas")
        
        with st.expander("👀 Vista previa de datos limpios"):
            st.dataframe(df_clean.head(20), use_container_width=True)
        
        # Añadir características derivadas
        if date_cols:
            df_clean['Year'] = df_clean[date_cols[0]].dt.year
            df_clean['Month'] = df_clean[date_cols[0]].dt.month
            df_clean['Month_Name'] = df_clean[date_cols[0]].dt.month_name()
            df_clean['Day_of_Week'] = df_clean[date_cols[0]].dt.day_name()
        
        # ANÁLISIS EXPLORATORIO (EDA)
        st.subheader("📊 Análisis Exploratorio de Datos (EDA)")
        
        # Detectar columnas clave
        sentiment_col = [col for col in df_clean.columns if 'sentiment' in col.lower()]
        price_col = [col for col in df_clean.columns if 'price' in col.lower() or 'close' in col.lower()]
        volume_col = [col for col in df_clean.columns if 'volume' in col.lower()]
        stock_col = [col for col in df_clean.columns if 'stock' in col.lower() or 'ticker' in col.lower() or 'symbol' in col.lower()]
        
        # GRÁFICA 1: Distribución de Sentimientos
        if sentiment_col:
            st.markdown("#### 1️⃣ Distribución de Sentimientos")
            col1, col2 = st.columns(2)
            
            with col1:
                fig, ax = plt.subplots(figsize=(10, 6))
                if pd.api.types.is_numeric_dtype(df_clean[sentiment_col[0]]):
                    sns.histplot(df_clean[sentiment_col[0]], kde=True, color='steelblue', bins=30, ax=ax)
                    ax.set_title("Distribución de Sentimiento (Numérico)")
                else:
                    df_clean[sentiment_col[0]].value_counts().plot(kind='bar', color='steelblue', ax=ax)
                    ax.set_title("Distribución de Sentimiento (Categórico)")
                ax.set_xlabel("Sentimiento")
                ax.set_ylabel("Frecuencia")
                st.pyplot(fig)
            
            with col2:
                if pd.api.types.is_numeric_dtype(df_clean[sentiment_col[0]]):
                    # Categorizar sentimiento
                    sentiment_cat = pd.cut(
                        df_clean[sentiment_col[0]],
                        bins=[-float('inf'), -0.3, 0.3, float('inf')],
                        labels=['Negativo', 'Neutral', 'Positivo']
                    )
                    fig = px.pie(
                        values=sentiment_cat.value_counts().values,
                        names=sentiment_cat.value_counts().index,
                        title="Proporción de Sentimientos",
                        color_discrete_sequence=px.colors.sequential.RdBu
                    )
                    st.plotly_chart(fig, use_container_width=True)
        
        # GRÁFICA 2: Serie temporal de precios
        if price_col and date_cols:
            st.markdown("#### 2️⃣ Evolución Temporal de Precios")
            fig = px.line(
                df_clean.sort_values(date_cols[0]),
                x=date_cols[0],
                y=price_col[0],
                color=stock_col[0] if stock_col else None,
                title="Evolución de Precios en el Tiempo"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # GRÁFICA 3: Relación Sentimiento vs Precio
        if sentiment_col and price_col:
            st.markdown("#### 3️⃣ Relación entre Sentimiento y Precio")
            fig, ax = plt.subplots(figsize=(12, 6))
            if pd.api.types.is_numeric_dtype(df_clean[sentiment_col[0]]):
                sns.scatterplot(
                    data=df_clean,
                    x=sentiment_col[0],
                    y=price_col[0],
                    hue=stock_col[0] if stock_col else None,
                    alpha=0.6,
                    ax=ax
                )
                # Línea de tendencia
                z = np.polyfit(df_clean[sentiment_col[0]], df_clean[price_col[0]], 1)
                p = np.poly1d(z)
                ax.plot(df_clean[sentiment_col[0]], p(df_clean[sentiment_col[0]]), 
                       "r--", alpha=0.8, label='Tendencia')
                ax.legend()
            ax.set_title("Sentimiento vs Precio de Acción")
            st.pyplot(fig)
        
        # GRÁFICA 4: Análisis por acción (Top stocks)
        if stock_col:
            st.markdown("#### 4️⃣ Análisis por Acción")
            top_stocks = df_clean[stock_col[0]].value_counts().head(10)
            
            col1, col2 = st.columns(2)
            with col1:
                fig, ax = plt.subplots(figsize=(10, 6))
                top_stocks.plot(kind='barh', color='coral', ax=ax)
                ax.set_title("Top 10 Acciones más Mencionadas")
                ax.set_xlabel("Frecuencia")
                st.pyplot(fig)
            
            with col2:
                if price_col:
                    top_stock_names = top_stocks.index[:5]
                    df_top = df_clean[df_clean[stock_col[0]].isin(top_stock_names)]
                    fig = px.box(
                        df_top,
                        x=stock_col[0],
                        y=price_col[0],
                        title="Distribución de Precios - Top 5 Acciones",
                        color=stock_col[0]
                    )
                    st.plotly_chart(fig, use_container_width=True)
        
        # GRÁFICA 5: Análisis temporal (por mes/año)
        if 'Month_Name' in df_clean.columns:
            st.markdown("#### 5️⃣ Análisis Temporal por Mes")
            
            if sentiment_col and pd.api.types.is_numeric_dtype(df_clean[sentiment_col[0]]):
                monthly_sentiment = df_clean.groupby('Month_Name')[sentiment_col[0]].mean().reindex([
                    'January', 'February', 'March', 'April', 'May', 'June',
                    'July', 'August', 'September', 'October', 'November', 'December'
                ])
                
                fig = go.Figure()
                fig.add_trace(go.Bar(
                    x=monthly_sentiment.index,
                    y=monthly_sentiment.values,
                    marker_color=monthly_sentiment.values,
                    marker_colorscale='RdYlGn',
                    text=monthly_sentiment.values.round(2),
                    textposition='auto'
                ))
                fig.update_layout(
                    title="Sentimiento Promedio por Mes",
                    xaxis_title="Mes",
                    yaxis_title="Sentimiento Promedio"
                )
                st.plotly_chart(fig, use_container_width=True)
        
        # GRÁFICA EXTRA: Volumen si está disponible
        if volume_col and date_cols:
            st.markdown("#### 6️⃣ Volumen de Transacciones")
            fig = px.bar(
                df_clean.sort_values(date_cols[0]),
                x=date_cols[0],
                y=volume_col[0],
                color=stock_col[0] if stock_col else None,
                title="Volumen de Transacciones en el Tiempo"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # ESTADÍSTICAS DESCRIPTIVAS
        st.subheader("📋 Estadísticas Descriptivas")
        st.dataframe(df_clean.describe(), use_container_width=True)
        
        # OPCIONES DE DESCARGA
        st.subheader("💾 Descargar Datos Limpios")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            csv_data = df_clean.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Descargar CSV",
                data=csv_data,
                file_name=f"{uploaded_file.replace('.csv', '')}_clean.csv",
                mime="text/csv"
            )
        
        with col2:
            # Guardar en la carpeta output
            output_dir = BASE_DIR / 'data' / 'output'
            output_dir.mkdir(parents=True, exist_ok=True)
            output_path = output_dir / f"{uploaded_file.replace('.csv', '')}_clean.csv"
            df_clean.to_csv(output_path, index=False)
            st.success(f"✅ Guardado en: `{output_path}`")
        
    except Exception as e:
        st.error(f"❌ Error al procesar el archivo: {str(e)}")
        st.exception(e)

else:
    st.warning("Por favor, selecciona un archivo de la lista.")
