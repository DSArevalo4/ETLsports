import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from pathlib import Path
import time
from scipy import stats

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
        
        # Añadir características derivadas
        if date_cols:
            df_clean['Year'] = df_clean[date_cols[0]].dt.year
            df_clean['Month'] = df_clean[date_cols[0]].dt.month
            df_clean['Month_Name'] = df_clean[date_cols[0]].dt.month_name()
            df_clean['Day_of_Week'] = df_clean[date_cols[0]].dt.day_name()
            df_clean['Quarter'] = df_clean[date_cols[0]].dt.quarter
        
        # ANÁLISIS EXPLORATORIO (EDA)
        st.subheader("📊 Análisis Exploratorio de Datos (EDA)")
        
        # Detectar columnas clave
        sentiment_col = [col for col in df_clean.columns if 'sentiment' in col.lower()]
        price_col = [col for col in df_clean.columns if 'price' in col.lower() or 'close' in col.lower()]
        volume_col = [col for col in df_clean.columns if 'volume' in col.lower()]
        stock_col = [col for col in df_clean.columns if 'stock' in col.lower() or 'ticker' in col.lower() or 'symbol' in col.lower()]
        
        # ============================================
        # GRÁFICA 1: Distribución de Sentimientos con Estadísticas
        # ============================================
        if sentiment_col:
            st.markdown("#### 1️⃣ Distribución de Sentimientos")
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
                
                if pd.api.types.is_numeric_dtype(df_clean[sentiment_col[0]]):
                    # Histograma con KDE
                    sns.histplot(df_clean[sentiment_col[0]], kde=True, color='steelblue', 
                                bins=40, ax=ax1, stat='density')
                    ax1.axvline(df_clean[sentiment_col[0]].mean(), color='red', 
                               linestyle='--', label=f'Media: {df_clean[sentiment_col[0]].mean():.3f}')
                    ax1.axvline(df_clean[sentiment_col[0]].median(), color='green', 
                               linestyle='--', label=f'Mediana: {df_clean[sentiment_col[0]].median():.3f}')
                    ax1.set_title("Distribución de Sentimiento (Numérico)", fontsize=12, fontweight='bold')
                    ax1.set_xlabel("Sentimiento")
                    ax1.set_ylabel("Densidad")
                    ax1.legend()
                    
                    # Boxplot
                    sns.boxplot(y=df_clean[sentiment_col[0]], color='lightblue', ax=ax2)
                    ax2.set_title("Boxplot - Detección de Outliers", fontsize=12, fontweight='bold')
                    ax2.set_ylabel("Sentimiento")
                else:
                    sentiment_counts = df_clean[sentiment_col[0]].value_counts()
                    sentiment_counts.plot(kind='bar', color='steelblue', ax=ax1)
                    ax1.set_title("Distribución de Sentimiento (Categórico)", fontsize=12, fontweight='bold')
                    ax1.set_xlabel("Categoría")
                    ax1.set_ylabel("Frecuencia")
                    
                    # Porcentajes
                    sentiment_pct = (sentiment_counts / len(df_clean) * 100)
                    sentiment_pct.plot(kind='barh', color='coral', ax=ax2)
                    ax2.set_title("Proporción (%)", fontsize=12, fontweight='bold')
                    ax2.set_xlabel("Porcentaje")
                
                plt.tight_layout()
                st.pyplot(fig)
            
            with col2:
                # Estadísticas descriptivas
                st.markdown("**📊 Estadísticas**")
                if pd.api.types.is_numeric_dtype(df_clean[sentiment_col[0]]):
                    stats_df = pd.DataFrame({
                        'Métrica': ['Media', 'Mediana', 'Desv. Est.', 'Mínimo', 'Máximo', 
                                   'Q1 (25%)', 'Q3 (75%)', 'Asimetría', 'Curtosis'],
                        'Valor': [
                            f"{df_clean[sentiment_col[0]].mean():.4f}",
                            f"{df_clean[sentiment_col[0]].median():.4f}",
                            f"{df_clean[sentiment_col[0]].std():.4f}",
                            f"{df_clean[sentiment_col[0]].min():.4f}",
                            f"{df_clean[sentiment_col[0]].max():.4f}",
                            f"{df_clean[sentiment_col[0]].quantile(0.25):.4f}",
                            f"{df_clean[sentiment_col[0]].quantile(0.75):.4f}",
                            f"{df_clean[sentiment_col[0]].skew():.4f}",
                            f"{df_clean[sentiment_col[0]].kurt():.4f}"
                        ]
                    })
                    st.dataframe(stats_df, use_container_width=True, hide_index=True)
                    
                    # Interpretación
                    sentiment_mean = df_clean[sentiment_col[0]].mean()
                    if sentiment_mean > 0.3:
                        st.success("😊 Sentimiento generalmente **POSITIVO**")
                    elif sentiment_mean < -0.3:
                        st.error("😟 Sentimiento generalmente **NEGATIVO**")
                    else:
                        st.info("😐 Sentimiento generalmente **NEUTRAL**")
        
        # ============================================
        # GRÁFICA 2: Correlación entre Sentimiento y Precio (Heatmap + Scatter)
        # ============================================
        if sentiment_col and price_col:
            st.markdown("#### 2️⃣ Relación Sentimiento-Precio (Análisis de Correlación)")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Scatter plot con regresión
                fig = px.scatter(
                    df_clean, 
                    x=sentiment_col[0], 
                    y=price_col[0],
                    color=stock_col[0] if stock_col else None,
                    trendline="ols",
                    title="Sentimiento vs Precio (con línea de tendencia)",
                    labels={sentiment_col[0]: "Sentimiento", price_col[0]: "Precio"},
                    opacity=0.6,
                    hover_data=[date_cols[0]] if date_cols else None
                )
                fig.update_layout(height=500)
                st.plotly_chart(fig, use_container_width=True)
                
                # Calcular correlación
                if pd.api.types.is_numeric_dtype(df_clean[sentiment_col[0]]):
                    corr = df_clean[sentiment_col[0]].corr(df_clean[price_col[0]])
                    st.metric("Correlación de Pearson", f"{corr:.4f}", 
                             help="Valores cercanos a 1 o -1 indican correlación fuerte")
            
            with col2:
                # Heatmap de correlación entre variables numéricas
                numeric_cols = df_clean.select_dtypes(include=[np.number]).columns
                if len(numeric_cols) > 2:
                    corr_matrix = df_clean[numeric_cols].corr()
                    
                    fig, ax = plt.subplots(figsize=(10, 8))
                    sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm', 
                               center=0, square=True, linewidths=1, ax=ax,
                               cbar_kws={"shrink": 0.8})
                    ax.set_title("Matriz de Correlación", fontsize=14, fontweight='bold')
                    st.pyplot(fig)
                    
                    st.markdown("""
                    **📖 Interpretación:**
                    - 🟥 Rojo: Correlación positiva fuerte
                    - 🟦 Azul: Correlación negativa fuerte
                    - ⬜ Blanco: Sin correlación
                    """)
        
        # ============================================
        # GRÁFICA 3: Evolución Temporal Interactiva con Doble Eje
        # ============================================
        if price_col and date_cols and sentiment_col:
            st.markdown("#### 3️⃣ Evolución Temporal: Precio vs Sentimiento")
            
            # Crear figura con doble eje Y
            fig = go.Figure()
            
            # Si hay múltiples stocks, permitir selección
            if stock_col and df_clean[stock_col[0]].nunique() > 1:
                selected_stocks = st.multiselect(
                    "Selecciona acciones para visualizar",
                    options=df_clean[stock_col[0]].unique(),
                    default=df_clean[stock_col[0]].value_counts().head(3).index.tolist()
                )
                df_plot = df_clean[df_clean[stock_col[0]].isin(selected_stocks)]
            else:
                df_plot = df_clean
            
            df_plot = df_plot.sort_values(date_cols[0])
            
            # Línea de precio
            fig.add_trace(go.Scatter(
                x=df_plot[date_cols[0]],
                y=df_plot[price_col[0]],
                name="Precio",
                line=dict(color='#1f77b4', width=2),
                yaxis='y'
            ))
            
            # Línea de sentimiento
            if pd.api.types.is_numeric_dtype(df_plot[sentiment_col[0]]):
                fig.add_trace(go.Scatter(
                    x=df_plot[date_cols[0]],
                    y=df_plot[sentiment_col[0]],
                    name="Sentimiento",
                    line=dict(color='#ff7f0e', width=2, dash='dash'),
                    yaxis='y2'
                ))
            
            # Configurar layout con doble eje
            fig.update_layout(
                title="Evolución Temporal: Precio y Sentimiento",
                xaxis=dict(title="Fecha"),
                yaxis=dict(title="Precio ($)", side='left'),
                yaxis2=dict(title="Sentimiento", overlaying='y', side='right'),
                hovermode='x unified',
                height=500
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        # ============================================
        # GRÁFICA 4: Análisis por Acción (Top Stocks)
        # ============================================
        if stock_col:
            st.markdown("#### 4️⃣ Análisis Detallado por Acción")
            
            tab1, tab2, tab3 = st.tabs(["📊 Frecuencia", "💰 Precio Promedio", "😊 Sentimiento Promedio"])
            
            with tab1:
                col1, col2 = st.columns(2)
                
                with col1:
                    # Top 15 acciones más mencionadas
                    top_stocks = df_clean[stock_col[0]].value_counts().head(15)
                    
                    fig = px.bar(
                        x=top_stocks.values,
                        y=top_stocks.index,
                        orientation='h',
                        title="Top 15 Acciones más Mencionadas",
                        labels={'x': 'Frecuencia', 'y': 'Acción'},
                        color=top_stocks.values,
                        color_continuous_scale='Blues'
                    )
                    fig.update_layout(height=500, showlegend=False)
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    # Treemap de distribución
                    top_20 = df_clean[stock_col[0]].value_counts().head(20)
                    fig = px.treemap(
                        names=top_20.index,
                        parents=["" for _ in range(len(top_20))],
                        values=top_20.values,
                        title="Distribución de Menciones (Top 20)"
                    )
                    fig.update_layout(height=500)
                    st.plotly_chart(fig, use_container_width=True)
            
            with tab2:
                if price_col:
                    # Precio promedio por acción
                    avg_price = df_clean.groupby(stock_col[0])[price_col[0]].agg(['mean', 'std', 'count'])
                    avg_price = avg_price[avg_price['count'] >= 5].sort_values('mean', ascending=False).head(15)
                    
                    fig = go.Figure()
                    fig.add_trace(go.Bar(
                        x=avg_price.index,
                        y=avg_price['mean'],
                        error_y=dict(type='data', array=avg_price['std']),
                        marker_color='lightseagreen',
                        name='Precio Promedio'
                    ))
                    fig.update_layout(
                        title="Precio Promedio por Acción (Top 15)",
                        xaxis_title="Acción",
                        yaxis_title="Precio Promedio ($)",
                        height=500
                    )
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Tabla con detalles
                    st.dataframe(avg_price.round(2), use_container_width=True)
            
            with tab3:
                if sentiment_col and pd.api.types.is_numeric_dtype(df_clean[sentiment_col[0]]):
                    # Sentimiento promedio por acción
                    avg_sentiment = df_clean.groupby(stock_col[0])[sentiment_col[0]].agg(['mean', 'count'])
                    avg_sentiment = avg_sentiment[avg_sentiment['count'] >= 5].sort_values('mean', ascending=False).head(20)
                    
                    # Categorizar sentimientos
                    avg_sentiment['Categoría'] = pd.cut(
                        avg_sentiment['mean'],
                        bins=[-np.inf, -0.3, 0.3, np.inf],
                        labels=['Negativo', 'Neutral', 'Positivo']
                    )
                    
                    fig = px.bar(
                        x=avg_sentiment.index,
                        y=avg_sentiment['mean'],
                        color=avg_sentiment['Categoría'],
                        title="Sentimiento Promedio por Acción (Top 20)",
                        labels={'x': 'Acción', 'y': 'Sentimiento Promedio'},
                        color_discrete_map={'Positivo': 'green', 'Neutral': 'gray', 'Negativo': 'red'},
                        height=500
                    )
                    fig.add_hline(y=0, line_dash="dash", line_color="black", opacity=0.5)
                    st.plotly_chart(fig, use_container_width=True)
        
        # ============================================
        # GRÁFICA 5: Análisis Temporal Avanzado
        # ============================================
        if date_cols:
            st.markdown("#### 5️⃣ Análisis Temporal Avanzado")
            
            tab1, tab2, tab3 = st.tabs(["📅 Por Mes", "📆 Por Día de Semana", "📈 Por Trimestre"])
            
            with tab1:
                col1, col2 = st.columns(2)
                
                with col1:
                    # Sentimiento por mes
                    if sentiment_col and pd.api.types.is_numeric_dtype(df_clean[sentiment_col[0]]):
                        monthly_data = df_clean.groupby('Month_Name').agg({
                            sentiment_col[0]: ['mean', 'std', 'count']
                        }).reset_index()
                        monthly_data.columns = ['Month', 'Sentiment_Mean', 'Sentiment_Std', 'Count']
                        
                        # Ordenar meses
                        month_order = ['January', 'February', 'March', 'April', 'May', 'June',
                                     'July', 'August', 'September', 'October', 'November', 'December']
                        monthly_data['Month'] = pd.Categorical(monthly_data['Month'], categories=month_order, ordered=True)
                        monthly_data = monthly_data.sort_values('Month')
                        
                        fig = go.Figure()
                        fig.add_trace(go.Bar(
                            x=monthly_data['Month'],
                            y=monthly_data['Sentiment_Mean'],
                            marker_color=monthly_data['Sentiment_Mean'],
                            marker_colorscale='RdYlGn',
                            marker_cmin=-1,
                            marker_cmax=1,
                            text=monthly_data['Sentiment_Mean'].round(3),
                            textposition='outside'
                        ))
                        fig.add_hline(y=0, line_dash="dash", line_color="black")
                        fig.update_layout(
                            title="Sentimiento Promedio por Mes",
                            xaxis_title="Mes",
                            yaxis_title="Sentimiento",
                            height=400
                        )
                        st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    # Precio por mes
                    if price_col:
                        monthly_price = df_clean.groupby('Month_Name')[price_col[0]].mean().reindex(month_order)
                        
                        fig = go.Figure()
                        fig.add_trace(go.Scatter(
                            x=monthly_price.index,
                            y=monthly_price.values,
                            mode='lines+markers',
                            line=dict(color='royalblue', width=3),
                            marker=dict(size=10),
                            fill='tozeroy'
                        ))
                        fig.update_layout(
                            title="Precio Promedio por Mes",
                            xaxis_title="Mes",
                            yaxis_title="Precio ($)",
                            height=400
                        )
                        st.plotly_chart(fig, use_container_width=True)
            
            with tab2:
                # Análisis por día de la semana
                if 'Day_of_Week' in df_clean.columns:
                    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        # Volumen de menciones por día
                        day_counts = df_clean['Day_of_Week'].value_counts().reindex(day_order)
                        
                        fig = px.bar(
                            x=day_counts.index,
                            y=day_counts.values,
                            title="Volumen de Menciones por Día de la Semana",
                            labels={'x': 'Día', 'y': 'Cantidad'},
                            color=day_counts.values,
                            color_continuous_scale='Viridis'
                        )
                        st.plotly_chart(fig, use_container_width=True)
                    
                    with col2:
                        # Sentimiento por día
                        if sentiment_col and pd.api.types.is_numeric_dtype(df_clean[sentiment_col[0]]):
                            day_sentiment = df_clean.groupby('Day_of_Week')[sentiment_col[0]].mean().reindex(day_order)
                            
                            fig = go.Figure()
                            fig.add_trace(go.Scatterpolar(
                                r=day_sentiment.values,
                                theta=day_sentiment.index,
                                fill='toself',
                                name='Sentimiento'
                            ))
                            fig.update_layout(
                                polar=dict(radialaxis=dict(visible=True)),
                                title="Sentimiento por Día (Radar Chart)",
                                height=400
                            )
                            st.plotly_chart(fig, use_container_width=True)
            
            with tab3:
                # Análisis por trimestre
                if 'Quarter' in df_clean.columns:
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        # Precio por trimestre
                        if price_col:
                            quarter_data = df_clean.groupby('Quarter').agg({
                                price_col[0]: ['mean', 'min', 'max', 'count']
                            }).reset_index()
                            quarter_data.columns = ['Quarter', 'Mean', 'Min', 'Max', 'Count']
                            
                            fig = go.Figure()
                            fig.add_trace(go.Scatter(
                                x=quarter_data['Quarter'],
                                y=quarter_data['Mean'],
                                mode='lines+markers',
                                name='Promedio',
                                line=dict(width=3)
                            ))
                            fig.add_trace(go.Scatter(
                                x=quarter_data['Quarter'],
                                y=quarter_data['Max'],
                                mode='lines',
                                name='Máximo',
                                line=dict(dash='dash')
                            ))
                            fig.add_trace(go.Scatter(
                                x=quarter_data['Quarter'],
                                y=quarter_data['Min'],
                                mode='lines',
                                name='Mínimo',
                                line=dict(dash='dash')
                            ))
                            fig.update_layout(
                                title="Precio por Trimestre",
                                xaxis_title="Trimestre",
                                yaxis_title="Precio ($)"
                            )
                            st.plotly_chart(fig, use_container_width=True)
                    
                    with col2:
                        # Tabla resumen por trimestre
                        if sentiment_col:
                            quarter_summary = df_clean.groupby('Quarter').agg({
                                sentiment_col[0]: 'mean',
                                price_col[0]: 'mean' if price_col else sentiment_col[0],
                                stock_col[0]: 'count' if stock_col else sentiment_col[0]
                            }).round(3)
                            quarter_summary.columns = ['Sentimiento Promedio', 'Precio Promedio', 'Total Menciones']
                            st.dataframe(quarter_summary, use_container_width=True)
        
        # ============================================
        # GRÁFICA 6: Volatilidad y Riesgo
        # ============================================
        if price_col and stock_col:
            st.markdown("#### 6️⃣ Análisis de Volatilidad y Riesgo")
            
            # Calcular volatilidad (desviación estándar) por acción
            volatility = df_clean.groupby(stock_col[0])[price_col[0]].agg(['std', 'mean', 'count'])
            volatility = volatility[volatility['count'] >= 10].sort_values('std', ascending=False).head(20)
            volatility['cv'] = (volatility['std'] / volatility['mean']) * 100  # Coeficiente de variación
            
            col1, col2 = st.columns(2)
            
            with col1:
                fig = px.scatter(
                    x=volatility['mean'],
                    y=volatility['std'],
                    size=volatility['count'],
                    text=volatility.index,
                    title="Riesgo vs Retorno (Top 20 Acciones)",
                    labels={'x': 'Precio Promedio ($)', 'y': 'Volatilidad (Desv. Est.)'},
                    color=volatility['cv'],
                    color_continuous_scale='Reds'
                )
                fig.update_traces(textposition='top center')
                fig.update_layout(height=500)
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                fig = px.bar(
                    x=volatility.head(15).index,
                    y=volatility.head(15)['cv'],
                    title="Coeficiente de Variación (Top 15)",
                    labels={'x': 'Acción', 'y': 'CV (%)'},
                    color=volatility.head(15)['cv'],
                    color_continuous_scale='YlOrRd'
                )
                fig.update_layout(height=500)
                st.plotly_chart(fig, use_container_width=True)
                
                st.info("📊 **CV más alto** = Mayor volatilidad relativa al precio")
        
        # ESTADÍSTICAS DESCRIPTIVAS
        st.subheader("📋 Estadísticas Descriptivas Completas")
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
        
        with col3:
            # Estadísticas en JSON
            import json
            stats_dict = df_clean.describe().to_dict()
            stats_json = json.dumps(stats_dict, indent=2).encode('utf-8')
            st.download_button(
                label="📊 Descargar Estadísticas (JSON)",
                data=stats_json,
                file_name=f"{uploaded_file.replace('.csv', '')}_stats.json",
                mime="application/json"
            )
        
    except Exception as e:
        st.error(f"❌ Error al procesar el archivo: {str(e)}")
        st.exception(e)

else:
    st.warning("Por favor, selecciona un archivo de la lista.")
