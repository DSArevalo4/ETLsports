import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from pathlib import Path
import time
from collections import Counter
import re

# Configuración de la página
st.set_page_config(page_title="ETL News Sentiment Analysis", layout="wide", page_icon="📰")

st.title("📰 ETL News Sentiment Analysis")
st.markdown("### Pipeline de Análisis de Sentimientos en Noticias")

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
        with st.expander("👀 Vista previa de datos originales", expanded=False):
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
        
        # Detectar columnas
        date_cols = [col for col in df_clean.columns if 'date' in col.lower()]
        label_cols = [col for col in df_clean.columns if 'label' in col.lower()]
        news_cols = [col for col in df_clean.columns if 'top' in col.lower()]
        
        # Añadir características derivadas
        if date_cols:
            df_clean[date_cols[0]] = pd.to_datetime(df_clean[date_cols[0]], errors='coerce')
            df_clean['Year'] = df_clean[date_cols[0]].dt.year
            df_clean['Month'] = df_clean[date_cols[0]].dt.month
            df_clean['Month_Name'] = df_clean[date_cols[0]].dt.month_name()
            df_clean['Day_of_Week'] = df_clean[date_cols[0]].dt.day_name()
            df_clean['Quarter'] = df_clean[date_cols[0]].dt.quarter
            df_clean['Week'] = df_clean[date_cols[0]].dt.isocalendar().week
        
        # Convertir Label a categórico
        if label_cols:
            df_clean['Sentiment_Text'] = df_clean[label_cols[0]].map({0: 'Negativo', 1: 'Positivo'})
        
        # ANÁLISIS EXPLORATORIO (EDA)
        st.subheader("📊 Análisis Exploratorio de Datos (EDA)")
        
        # ============================================
        # GRÁFICA 1: Distribución de Sentimientos con Métricas
        # ============================================
        if label_cols:
            st.markdown("#### 1️⃣ Distribución de Sentimientos en Noticias")
            
            col1, col2, col3 = st.columns([2, 1, 1])
            
            with col1:
                # Gráfico de barras con proporciones
                sentiment_counts = df_clean['Sentiment_Text'].value_counts()
                
                fig = go.Figure()
                fig.add_trace(go.Bar(
                    x=sentiment_counts.index,
                    y=sentiment_counts.values,
                    text=sentiment_counts.values,
                    textposition='outside',
                    marker=dict(
                        color=['#FF6B6B', '#4ECDC4'],
                        line=dict(color='white', width=2)
                    )
                ))
                fig.update_layout(
                    title="Distribución de Sentimientos",
                    xaxis_title="Sentimiento",
                    yaxis_title="Cantidad de Noticias",
                    height=400
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Métricas
                total_news = len(df_clean)
                positive_pct = (df_clean[label_cols[0]] == 1).sum() / total_news * 100
                negative_pct = (df_clean[label_cols[0]] == 0).sum() / total_news * 100
                
                st.metric("📈 Noticias Positivas", f"{positive_pct:.1f}%")
                st.metric("📉 Noticias Negativas", f"{negative_pct:.1f}%")
                st.metric("📰 Total Noticias", f"{total_news:,}")
            
            with col3:
                # Gráfico de dona
                fig = go.Figure(data=[go.Pie(
                    labels=sentiment_counts.index,
                    values=sentiment_counts.values,
                    hole=.4,
                    marker=dict(colors=['#FF6B6B', '#4ECDC4'])
                )])
                fig.update_layout(
                    title="Proporción",
                    height=300,
                    showlegend=False
                )
                st.plotly_chart(fig, use_container_width=True)
        
        # ============================================
        # GRÁFICA 2: Evolución Temporal del Sentimiento
        # ============================================
        if date_cols and label_cols:
            st.markdown("#### 2️⃣ Evolución Temporal del Sentimiento")
            
            tab1, tab2 = st.tabs(["📅 Por Día", "📈 Tendencia Suavizada"])
            
            with tab1:
                # Sentimiento diario
                daily_sentiment = df_clean.groupby([date_cols[0], 'Sentiment_Text']).size().reset_index(name='Count')
                
                fig = px.line(
                    daily_sentiment,
                    x=date_cols[0],
                    y='Count',
                    color='Sentiment_Text',
                    title="Volumen de Noticias por Sentimiento a lo Largo del Tiempo",
                    color_discrete_map={'Positivo': '#4ECDC4', 'Negativo': '#FF6B6B'}
                )
                fig.update_layout(height=500)
                st.plotly_chart(fig, use_container_width=True)
            
            with tab2:
                # Índice de sentimiento (rolling average)
                df_sorted = df_clean.sort_values(date_cols[0])
                df_sorted['Sentiment_Index'] = df_sorted[label_cols[0]].rolling(window=7, min_periods=1).mean()
                
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=df_sorted[date_cols[0]],
                    y=df_sorted['Sentiment_Index'],
                    mode='lines',
                    name='Índice de Sentimiento (Media móvil 7 días)',
                    line=dict(width=3, color='#2E86AB'),
                    fill='tozeroy'
                ))
                fig.add_hline(y=0.5, line_dash="dash", line_color="gray", 
                             annotation_text="Neutral (0.5)")
                fig.update_layout(
                    title="Índice de Sentimiento Promedio (0=Negativo, 1=Positivo)",
                    xaxis_title="Fecha",
                    yaxis_title="Índice de Sentimiento",
                    height=500
                )
                st.plotly_chart(fig, use_container_width=True)
        
        # ============================================
        # GRÁFICA 3: Análisis por Año, Mes y Día de la Semana
        # ============================================
        if 'Year' in df_clean.columns or 'Month_Name' in df_clean.columns:
            st.markdown("#### 3️⃣ Patrones Temporales del Sentimiento")
            
            tab1, tab2, tab3 = st.tabs(["📆 Por Año", "📅 Por Mes", "🗓️ Por Día de Semana"])
            
            with tab1:
                if 'Year' in df_clean.columns:
                    yearly_sentiment = df_clean.groupby(['Year', 'Sentiment_Text']).size().reset_index(name='Count')
                    
                    fig = px.bar(
                        yearly_sentiment,
                        x='Year',
                        y='Count',
                        color='Sentiment_Text',
                        title="Distribución de Sentimientos por Año",
                        barmode='group',
                        color_discrete_map={'Positivo': '#4ECDC4', 'Negativo': '#FF6B6B'}
                    )
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Tabla resumen
                    pivot = yearly_sentiment.pivot(index='Year', columns='Sentiment_Text', values='Count').fillna(0)
                    pivot['% Positivo'] = (pivot.get('Positivo', 0) / (pivot.get('Positivo', 0) + pivot.get('Negativo', 0)) * 100).round(2)
                    st.dataframe(pivot, use_container_width=True)
            
            with tab2:
                if 'Month_Name' in df_clean.columns:
                    month_order = ['January', 'February', 'March', 'April', 'May', 'June',
                                 'July', 'August', 'September', 'October', 'November', 'December']
                    
                    monthly_sentiment = df_clean.groupby('Month_Name')[label_cols[0]].agg(['mean', 'count']).reindex(month_order)
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        fig = go.Figure()
                        fig.add_trace(go.Bar(
                            x=monthly_sentiment.index,
                            y=monthly_sentiment['mean'],
                            marker_color=monthly_sentiment['mean'],
                            marker_colorscale='RdYlGn',
                            marker_cmin=0,
                            marker_cmax=1,
                            text=monthly_sentiment['mean'].round(3),
                            textposition='outside'
                        ))
                        fig.add_hline(y=0.5, line_dash="dash", line_color="gray")
                        fig.update_layout(
                            title="Sentimiento Promedio por Mes",
                            xaxis_title="Mes",
                            yaxis_title="Índice de Sentimiento",
                            height=400
                        )
                        st.plotly_chart(fig, use_container_width=True)
                    
                    with col2:
                        fig = px.line(
                            x=monthly_sentiment.index,
                            y=monthly_sentiment['count'],
                            title="Volumen de Noticias por Mes",
                            markers=True
                        )
                        fig.update_layout(
                            xaxis_title="Mes",
                            yaxis_title="Cantidad de Noticias",
                            height=400
                        )
                        st.plotly_chart(fig, use_container_width=True)
            
            with tab3:
                if 'Day_of_Week' in df_clean.columns:
                    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
                    
                    daily_pattern = df_clean.groupby('Day_of_Week')[label_cols[0]].agg(['mean', 'count']).reindex(day_order)
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        fig = go.Figure()
                        fig.add_trace(go.Scatterpolar(
                            r=daily_pattern['mean'].values,
                            theta=daily_pattern.index,
                            fill='toself',
                            name='Sentimiento',
                            marker=dict(color='#2E86AB')
                        ))
                        fig.update_layout(
                            polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
                            title="Sentimiento por Día de la Semana (Radar)",
                            height=400
                        )
                        st.plotly_chart(fig, use_container_width=True)
                    
                    with col2:
                        fig = px.bar(
                            x=daily_pattern.index,
                            y=daily_pattern['count'],
                            title="Volumen de Noticias por Día de la Semana",
                            color=daily_pattern['count'],
                            color_continuous_scale='Blues'
                        )
                        fig.update_layout(height=400, showlegend=False)
                        st.plotly_chart(fig, use_container_width=True)
        
        # ============================================
        # GRÁFICA 4: Análisis de Palabras Clave en Títulos
        # ============================================
        if news_cols:
            st.markdown("#### 4️⃣ Análisis de Palabras Clave en Títulos de Noticias")
            
            # Extraer todas las palabras de los títulos
            all_words = []
            positive_words = []
            negative_words = []
            
            for idx, row in df_clean.iterrows():
                sentiment = row[label_cols[0]]
                for col in news_cols:
                    if pd.notna(row[col]):
                        words = re.findall(r'\b[a-zA-Z]{4,}\b', str(row[col]).lower())
                        all_words.extend(words)
                        if sentiment == 1:
                            positive_words.extend(words)
                        else:
                            negative_words.extend(words)
            
            # Stopwords comunes en inglés
            stopwords = {'that', 'this', 'with', 'from', 'have', 'been', 'will', 'they', 
                        'were', 'what', 'when', 'where', 'which', 'while', 'about', 'after',
                        'your', 'their', 'there', 'these', 'those', 'into', 'than', 'then'}
            
            all_words = [w for w in all_words if w not in stopwords]
            positive_words = [w for w in positive_words if w not in stopwords]
            negative_words = [w for w in negative_words if w not in stopwords]
            
            tab1, tab2, tab3 = st.tabs(["📊 Top Palabras", "😊 Palabras Positivas", "😞 Palabras Negativas"])
            
            with tab1:
                word_freq = Counter(all_words).most_common(20)
                words_df = pd.DataFrame(word_freq, columns=['Palabra', 'Frecuencia'])
                
                fig = px.bar(
                    words_df,
                    x='Frecuencia',
                    y='Palabra',
                    orientation='h',
                    title="Top 20 Palabras Más Frecuentes en Títulos",
                    color='Frecuencia',
                    color_continuous_scale='Viridis'
                )
                fig.update_layout(height=500, yaxis={'categoryorder':'total ascending'})
                st.plotly_chart(fig, use_container_width=True)
            
            with tab2:
                pos_freq = Counter(positive_words).most_common(15)
                pos_df = pd.DataFrame(pos_freq, columns=['Palabra', 'Frecuencia'])
                
                fig = px.treemap(
                    pos_df,
                    path=['Palabra'],
                    values='Frecuencia',
                    title="Palabras Más Frecuentes en Noticias Positivas",
                    color='Frecuencia',
                    color_continuous_scale='Greens'
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with tab3:
                neg_freq = Counter(negative_words).most_common(15)
                neg_df = pd.DataFrame(neg_freq, columns=['Palabra', 'Frecuencia'])
                
                fig = px.treemap(
                    neg_df,
                    path=['Palabra'],
                    values='Frecuencia',
                    title="Palabras Más Frecuentes en Noticias Negativas",
                    color='Frecuencia',
                    color_continuous_scale='Reds'
                )
                st.plotly_chart(fig, use_container_width=True)
        
        # ============================================
        # GRÁFICA 5: Longitud de Títulos y Sentimiento
        # ============================================
        if news_cols and label_cols:
            st.markdown("#### 5️⃣ Análisis de Longitud de Títulos")
            
            # Calcular longitud promedio de títulos por fila
            df_clean['Avg_Title_Length'] = df_clean[news_cols].apply(
                lambda row: np.mean([len(str(val)) if pd.notna(val) else 0 for val in row]), 
                axis=1
            )
            
            col1, col2 = st.columns(2)
            
            with col1:
                fig = px.box(
                    df_clean,
                    x='Sentiment_Text',
                    y='Avg_Title_Length',
                    color='Sentiment_Text',
                    title="Distribución de Longitud de Títulos por Sentimiento",
                    color_discrete_map={'Positivo': '#4ECDC4', 'Negativo': '#FF6B6B'}
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                fig = px.violin(
                    df_clean,
                    x='Sentiment_Text',
                    y='Avg_Title_Length',
                    color='Sentiment_Text',
                    title="Distribución de Longitud (Violin Plot)",
                    box=True,
                    color_discrete_map={'Positivo': '#4ECDC4', 'Negativo': '#FF6B6B'}
                )
                st.plotly_chart(fig, use_container_width=True)
            
            # Estadísticas
            stats_length = df_clean.groupby('Sentiment_Text')['Avg_Title_Length'].describe().round(2)
            st.dataframe(stats_length, use_container_width=True)
        
        # ============================================
        # GRÁFICA 6: Heatmap de Sentimientos por Mes y Año
        # ============================================
        if 'Year' in df_clean.columns and 'Month' in df_clean.columns:
            st.markdown("#### 6️⃣ Mapa de Calor: Sentimiento por Mes y Año")
            
            heatmap_data = df_clean.groupby(['Year', 'Month'])[label_cols[0]].mean().reset_index()
            pivot_heatmap = heatmap_data.pivot(index='Month', columns='Year', values=label_cols[0])
            
            fig = go.Figure(data=go.Heatmap(
                z=pivot_heatmap.values,
                x=pivot_heatmap.columns,
                y=['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 
                   'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'][:len(pivot_heatmap)],
                colorscale='RdYlGn',
                zmid=0.5,
                text=pivot_heatmap.values.round(3),
                texttemplate='%{text}',
                textfont={"size": 10},
                colorbar=dict(title="Sentimiento<br>Promedio")
            ))
            fig.update_layout(
                title="Sentimiento Promedio por Mes y Año",
                xaxis_title="Año",
                yaxis_title="Mes",
                height=500
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # ============================================
        # GRÁFICA 7: Comparación de Trimestres
        # ============================================
        if 'Quarter' in df_clean.columns:
            st.markdown("#### 7️⃣ Análisis por Trimestre")
            
            quarterly_data = df_clean.groupby(['Year', 'Quarter'])[label_cols[0]].agg(['mean', 'count']).reset_index()
            quarterly_data['Year_Quarter'] = quarterly_data['Year'].astype(str) + '-Q' + quarterly_data['Quarter'].astype(str)
            
            col1, col2 = st.columns(2)
            
            with col1:
                fig = px.line(
                    quarterly_data,
                    x='Year_Quarter',
                    y='mean',
                    title="Tendencia de Sentimiento por Trimestre",
                    markers=True,
                    line_shape='spline'
                )
                fig.add_hline(y=0.5, line_dash="dash", line_color="gray")
                fig.update_layout(
                    xaxis_title="Año-Trimestre",
                    yaxis_title="Sentimiento Promedio",
                    height=400
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                quarter_summary = df_clean.groupby('Quarter')[label_cols[0]].agg(['mean', 'count'])
                quarter_summary['% Positivo'] = (quarter_summary['mean'] * 100).round(2)
                
                fig = px.bar(
                    x=['Q1', 'Q2', 'Q3', 'Q4'][:len(quarter_summary)],
                    y=quarter_summary['% Positivo'],
                    title="Porcentaje de Sentimiento Positivo por Trimestre",
                    color=quarter_summary['% Positivo'],
                    color_continuous_scale='RdYlGn',
                    text=quarter_summary['% Positivo']
                )
                fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
        
        # ESTADÍSTICAS DESCRIPTIVAS
        st.subheader("📋 Estadísticas Descriptivas Completas")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Resumen General**")
            st.dataframe(df_clean.describe(include='all').T, use_container_width=True)
        
        with col2:
            st.markdown("**Correlaciones**")
            numeric_cols = df_clean.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) > 1:
                corr_matrix = df_clean[numeric_cols].corr()
                fig = px.imshow(
                    corr_matrix,
                    text_auto='.2f',
                    aspect='auto',
                    color_continuous_scale='RdBu_r',
                    title="Matriz de Correlación"
                )
                st.plotly_chart(fig, use_container_width=True)
        
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
            output_dir = BASE_DIR / 'data' / 'output'
            output_dir.mkdir(parents=True, exist_ok=True)
            output_path = output_dir / f"{uploaded_file.replace('.csv', '')}_clean.csv"
            df_clean.to_csv(output_path, index=False)
            st.success(f"✅ Guardado en: `{output_path}`")
        
        with col3:
            import json
            # Convertir estadísticas a formato JSON-serializable
            stats_dict = df_clean.describe(include='all').to_dict()
            
            # Función para convertir objetos no serializables
            def convert_to_serializable(obj):
                if pd.isna(obj):
                    return None
                elif isinstance(obj, (pd.Timestamp, pd.DatetimeTZDtype)):
                    return obj.isoformat()
                elif isinstance(obj, np.integer):
                    return int(obj)
                elif isinstance(obj, np.floating):
                    return float(obj)
                elif isinstance(obj, np.ndarray):
                    return obj.tolist()
                else:
                    return str(obj)
            
            # Convertir todas las estadísticas a tipos serializables
            serializable_stats = {}
            for col, values in stats_dict.items():
                serializable_stats[col] = {
                    k: convert_to_serializable(v) 
                    for k, v in values.items()
                }
            
            stats_json = json.dumps(serializable_stats, indent=2, default=str).encode('utf-8')
            st.download_button(
                label="📊 Estadísticas (JSON)",
                data=stats_json,
                file_name=f"{uploaded_file.replace('.csv', '')}_stats.json",
                mime="application/json"
            )
        
    except Exception as e:
        st.error(f"❌ Error al procesar el archivo: {str(e)}")
        st.exception(e)

else:
    st.warning("Por favor, selecciona un archivo de la lista.")
