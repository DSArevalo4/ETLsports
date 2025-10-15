# ETLsports — ETL y visualización de estadísticas de jugadores NBA

Descripción
Este repositorio implementa un flujo ETL sencillo para archivos Excel con estadísticas históricas de jugadores de la NBA y una interfaz ligera en Streamlit para explorar y visualizar los datos. El proyecto está organizado en tres etapas clásicas: Extract, Transform y Load, además de una pequeña app para visualizar.

Características
- Extracción: lectura de archivos .xlsx con pandas (`openpyxl` como engine).
- Transformación: limpieza configurable (normalización de nombres de columnas, eliminación de duplicados y NAs).
- Carga: exportación a CSV o a base de datos SQLite.
- Visualización: app en Streamlit para explorar dataset, limpiar rápidamente y graficar distribuciones y relaciones.

Estructura del proyecto
```
ETLsports/
├─ Config/
│  └─ configuraciones.py         # Rutas y constantes (INPUT_PATH, DB, tabla)
├─ Extract/
│  └─ nbaExtract.py              # Clase Extractor (lee Excel)
├─ Transform/
│  └─ nbaTransform.py            # Clase Transformer (limpieza/normalización)
├─ Load/
│  └─ nbaLoad.py                 # Clase Loader (CSV/SQLite)
├─ NBAplayers/                   # Archivos .xlsx de entrada (datos fuente)
├─ main.py                       # App Streamlit de exploración y gráficos
├─ requeriments.txt              # Dependencias del proyecto
└─ README.md
```

Requisitos
- Python 3.9+ (recomendado)
- Sistema operativo: Windows, macOS o Linux

Instalación
1) Crear y activar un entorno virtual (opcional, recomendado)
```bash
python -m venv .venv
.venv\Scripts\activate   # Windows
# source .venv/bin/activate  # macOS/Linux
```

2) Instalar dependencias
```bash
pip install -r requirements.txt
```

Configuración
El archivo `Config/configuraciones.py` define rutas por defecto para el flujo batch (no para Streamlit):
```
class Config:
    INPUT_PATH = "/workspaces/ATPtour/NBAplayers/1963 - NBA Player Stats.xlsx"
    SQLITE_DB_PATH = "/workspaces/ATPtour/Extract/nba_player_stats_1963.db"
    SQLITE_TABLE = "nba_player_stats"
```

Recomendaciones:
- Ajusta `INPUT_PATH` para que apunte a un archivo existente dentro de `NBAplayers/` en tu máquina.
- Cambia `SQLITE_DB_PATH` a una ruta válida local (por ejemplo `./Extract/nba_player_stats_1963.db`).

Uso
### 1) Interfaz Streamlit (exploración y visualización)
La app de `main.py` lista los .xlsx en `NBAplayers/`, permite una limpieza básica y genera gráficos.
```bash
streamlit run main.py
```

**Nota**: El proyecto ahora usa rutas relativas automáticas, por lo que funcionará en cualquier sistema operativo sin modificar código.

### 2) Flujo ETL programático (batch)
Puedes usar las clases `Extractor`, `Transformer` y `Loader` desde un script Python:
```
from Extract.nbaExtract import Extractor
from Transform.nbaTransform import Transformer
from Load.nbaLoad import Loader

extractor = Extractor(file_path="NBAplayers/1963 - NBA Player Stats.xlsx")
df = extractor.extract()

df_clean = Transformer.clean_data(
    df,
    remove_duplicates=True,
    remove_na=False,
    normalize_columns=True,
)

loader = Loader(df_clean)
loader.to_csv("output/nba_player_stats_1963.csv")
loader.to_sqlite("Extract/nba_player_stats_1963.db", "nba_player_stats")
```

Parámetros de limpieza
- normalize_columns: normaliza nombres (trim, minúsculas, guiones bajos).
- remove_duplicates: elimina duplicados.
- remove_na: elimina filas con valores nulos.

Gráficos disponibles en la app
- Histograma de edad con KDE.
- Dispersión TRB vs PTS (si existen columnas).
- Distribución por posición (mapeando abreviaturas a nombres en español).

Buenas prácticas y notas
- Mantén los archivos fuente `.xlsx` dentro de `NBAplayers/`.
- Verifica que las columnas esperadas existan antes de graficar en `main.py`.
- Si ejecutas en Windows, usa rutas con `\\` o `r"C:\\ruta\\..."` para evitar errores de escape.
- Para `pandas.read_excel` asegúrate de tener `openpyxl` instalado (incluido en `requeriments.txt`).

Solución de problemas
- **No se listan archivos en la app**: Asegúrate de que la carpeta `NBAplayers/` exista en el mismo directorio que `main.py` y contenga archivos `.xlsx` válidos.
- **Error al leer Excel**: Verifica la instalación de `openpyxl`: `pip install openpyxl`
- **Gráficos no se muestran**: El código ahora valida que las columnas existan antes de graficar
- **Error de ruta**: Usa rutas relativas o el módulo `pathlib` para compatibilidad multiplataforma

Licencia
Libre uso educativo y personal. Ajusta según tus necesidades.

# 📰 ETL News Sentiment Analysis

Pipeline ETL completo para análisis de sentimientos en noticias con visualizaciones interactivas avanzadas.

## 🚀 Descripción del Proyecto

Este proyecto implementa un pipeline ETL para el análisis de sentimientos en noticias, permitiendo la visualización interactiva de datos históricos y resultados de análisis de sentimiento.

## 📊 Gráficas de Análisis (EDA)

La aplicación genera **7 gráficas especializadas** para análisis de sentimientos de noticias:

### 1️⃣ Distribución de Sentimientos
- **Gráfico de barras** con cantidad de noticias positivas/negativas
- **Gráfico de dona** con proporciones
- **Métricas clave** (porcentajes y totales)

### 2️⃣ Evolución Temporal del Sentimiento
- **Serie temporal** de volumen de noticias por sentimiento
- **Índice de sentimiento** con media móvil de 7 días
- Identificación de períodos positivos/negativos

### 3️⃣ Patrones Temporales
- **Por Año**: Distribución y tabla resumen con porcentajes
- **Por Mes**: Sentimiento promedio y volumen mensual
- **Por Día de Semana**: Radar chart + volumen por día

### 4️⃣ Análisis de Palabras Clave
- **Top 20 palabras** más frecuentes en títulos
- **Treemap de palabras positivas** (contexto de noticias positivas)
- **Treemap de palabras negativas** (contexto de noticias negativas)

### 5️⃣ Longitud de Títulos vs Sentimiento
- **Boxplot** comparando longitud de títulos positivos/negativos
- **Violin plot** mostrando distribución detallada
- **Tabla estadística** con media, mediana, desviación estándar

### 6️⃣ Mapa de Calor Mes-Año
- **Heatmap interactivo** mostrando sentimiento promedio
- Identificación de **patrones estacionales**
- Colores intuitivos (verde=positivo, rojo=negativo)

### 7️⃣ Análisis por Trimestre
- **Tendencia trimestral** del sentimiento
- **Comparación de Q1, Q2, Q3, Q4**
- Porcentaje de noticias positivas por trimestre

## 📝 Estructura del CSV

El archivo `stock_senti_analysis.csv` debe contener:
- **Date**: Fecha de la noticia (formato: YYYY-MM-DD)
- **Label**: Sentimiento (0=Negativo, 1=Positivo)
- **Top1 a Top25**: Títulos de noticias principales del día

## 🔍 Características del Análisis

✅ **Limpieza automática** de datos (duplicados, nulos)
✅ **Detección de patrones temporales** (diario, semanal, mensual, trimestral, anual)
✅ **Análisis de lenguaje natural** (palabras clave más frecuentes)
✅ **Visualizaciones interactivas** con zoom, hover y filtros
✅ **Métricas estadísticas avanzadas** (correlaciones, distribuciones)
✅ **Exportación de datos limpios** (CSV/JSON)
