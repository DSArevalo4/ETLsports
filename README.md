# 📈 ETL Stock Sentiment Analysis

Pipeline ETL completo para análisis de sentimientos de acciones con visualizaciones interactivas.

## 🎯 Objetivo

Construir un pipeline ETL en Python que:
- **Extraiga** datos de archivos CSV con análisis de sentimientos de acciones
- **Transforme** y limpie los datos (fechas, duplicados, nulos, normalizaciones)
- **Cargue** datasets limpios (CSV/Parquet/SQLite)
- **Genere** al menos 5 gráficas de análisis exploratorio (EDA)

## 📁 Estructura del Proyecto

```
ETLsports/
├── Config/
│   └── configuraciones.py         # Configuraciones centralizadas
├── Extract/
│   └── stockExtract.py           # Clase Extractor para CSV
├── Transform/
│   └── stockTransform.py         # Clase Transformer (limpieza)
├── Load/
│   └── stockLoad.py              # Clase Loader (CSV/Parquet/SQLite)
├── data/
│   ├── input/                    # Archivos CSV de entrada (git ignored)
│   └── output/                   # Datos procesados (git ignored)
├── .venv/                        # Entorno virtual (git ignored)
├── main.py                       # App Streamlit interactiva
├── requirements.txt              # Dependencias del proyecto
├── .gitignore                    # Archivos excluidos de Git
└── README.md
```

## 🚀 Instalación

### 1. Clonar el repositorio
```bash
git clone <tu-repositorio>
cd ETLsports
```

### 2. Crear entorno virtual
```bash
python -m venv .venv
.venv\Scripts\activate   # Windows
# source .venv/bin/activate  # macOS/Linux
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Preparar los datos
Coloca el archivo `stock_senti_analysis.csv` en la carpeta `data/input/`:
```
ETLsports/data/input/stock_senti_analysis.csv
```

## 💻 Uso

### Opción 1: Interfaz Streamlit (Recomendado)

```bash
streamlit run main.py
```

**Funcionalidades:**
- ✅ Seleccionar archivo CSV
- 🧹 Limpiar datos (duplicados, nulos, normalización)
- 📊 Visualizar 6 gráficas interactivas
- 💾 Descargar datos limpios

### Opción 2: Pipeline ETL Programático

```python
from Extract.stockExtract import Extractor
from Transform.stockTransform import Transformer
from Load.stockLoad import Loader

# Extracción
extractor = Extractor("data/input/stock_senti_analysis.csv")
df = extractor.extract()

# Transformación
df_clean = Transformer.clean_data(
    df,
    remove_duplicates=True,
    remove_na=True,
    normalize_columns=True,
    parse_dates=True
)

# Características derivadas
df_enhanced = Transformer.add_derived_features(df_clean)

# Carga
loader = Loader(df_enhanced)
loader.to_csv("data/output/stock_sentiment_clean.csv")
loader.to_parquet("data/output/stock_sentiment_clean.parquet")
loader.to_sqlite("data/output/stock_sentiment.db", "stock_sentiment_clean")
```

## 📊 Gráficas de Análisis (EDA)

La aplicación genera **9 gráficas interactivas** específicas para análisis de sentimientos de acciones:

### 1️⃣ Distribución de Sentimientos
- **Histograma con KDE** y estadísticas (media, mediana)
- **Boxplot** para detección de outliers
- **Estadísticas descriptivas** completas (asimetría, curtosis)

### 2️⃣ Correlación Sentimiento-Precio
- **Scatter plot** con línea de tendencia (regresión lineal)
- **Heatmap de correlación** entre todas las variables numéricas
- Coeficiente de correlación de Pearson

### 3️⃣ Evolución Temporal con Doble Eje
- **Serie temporal interactiva** con precio y sentimiento
- Selección múltiple de acciones
- Visualización comparativa

### 4️⃣ Análisis Detallado por Acción (3 tabs)
- **Frecuencia**: Top 15 acciones + Treemap de distribución
- **Precio Promedio**: Gráfico de barras con error bars
- **Sentimiento Promedio**: Categorización positivo/neutral/negativo

### 5️⃣ Análisis Temporal Avanzado (3 tabs)
- **Por Mes**: Sentimiento y precio promedio mensual
- **Por Día de Semana**: Volumen + Radar chart de sentimiento
- **Por Trimestre**: Análisis estacional con máximos y mínimos

### 6️⃣ Análisis de Volatilidad y Riesgo
- **Scatter plot Riesgo vs Retorno** (tamaño = volumen)
- **Coeficiente de Variación** para identificar acciones volátiles

## 🔧 Configuración

### Parámetros de Limpieza

| Parámetro | Descripción | Valor por defecto |
|-----------|-------------|-------------------|
| `remove_duplicates` | Elimina filas duplicadas | `True` |
| `remove_na` | Elimina filas con valores nulos | `True` |
| `normalize_columns` | Normaliza nombres de columnas | `True` |
| `parse_dates` | Convierte columnas de fecha a datetime | `True` |

### Formatos de Salida

- **CSV**: Compatibilidad universal
- **Parquet**: Formato columnar eficiente (menor tamaño)
- **SQLite**: Base de datos local para consultas SQL

## 🛠️ Solución de Problemas

| Problema | Solución |
|----------|----------|
| `streamlit: command not found` | Activa el entorno virtual: `.venv\Scripts\activate` |
| **PermissionError al leer CSV** | **1. Cierra Excel<br>2. Cierra Explorador de Windows<br>3. Ejecuta: `close_file_handles.bat`<br>4. Recarga Streamlit (F5)** |
| No se listan archivos | Verifica que `data/input/` contenga archivos `.csv` |
| Error de encoding | El código ahora detecta automáticamente UTF-8/Latin-1 |
| Gráficas vacías | Confirma que las columnas esperadas existan |

### 🔧 Solucionar "Permission Denied"

**Método 1: Cerrar programas manualmente**
```powershell
# 1. Cierra Excel completamente
# 2. Cierra todas las ventanas del Explorador de Windows
# 3. En el navegador, recarga la página de Streamlit (F5)
```

**Método 2: Script automático**
```powershell
# Ejecuta este script para cerrar Excel automáticamente
.\close_file_handles.bat

# Luego ejecuta Streamlit
streamlit run main.py
```

**Método 3: Verificar permisos**
```powershell
# Diagnosticar qué está bloqueando el archivo
python fix_permissions.py
```

**Método 4: Copiar archivo con nuevo nombre**
```powershell
# Si el problema persiste, crea una copia del archivo
cd data\input
copy stock_senti_analysis.csv stock_data_backup.csv

# Luego selecciona el archivo backup en Streamlit
```

### Comandos útiles de Git

```bash
# Ver estado del repositorio
git status

# Añadir solo archivos del proyecto (sin .venv)
git add *.py *.txt *.md .gitignore
git add Config/ Extract/ Transform/ Load/

# Commit
git commit -m "Descripción del cambio"

# Push al repositorio remoto
git push origin main
```

## 📝 Requisitos del CSV

El archivo CSV debe contener al menos:
- **Date**: Fecha de la observación
- **Stock/Ticker/Symbol**: Identificador de la acción
- **Sentiment**: Valor de sentimiento (numérico o categórico)
- **Price/Close**: Precio de la acción
- **Volume** (opcional): Volumen de transacciones

## 🤝 Contribuciones

1. Fork el proyecto
2. Crea una rama: `git checkout -b feature/nueva-funcionalidad`
3. Commit: `git commit -am 'Añade nueva funcionalidad'`
4. Push: `git push origin feature/nueva-funcionalidad`
5. Abre un Pull Request

## 📄 Licencia

Proyecto de uso educativo y personal.

## 👤 Autor

**Daniel Santiago Arevalo** - ETL Stock Sentiment Analysis Project

---

> **Nota Importante**: El entorno virtual `.venv` y los datos en `data/` están excluidos de Git por razones de seguridad y tamaño. Cada usuario debe crear su propio entorno virtual siguiendo las instrucciones de instalación.
