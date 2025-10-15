# 📰 ETL News Sentiment Analysis# 📰 ETL News Sentiment Analysis



![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)

![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)

![License](https://img.shields.io/badge/License-MIT-green.svg)![License](https://img.shields.io/badge/License-MIT-green.svg)



Pipeline ETL completo para análisis de sentimientos en noticias con visualizaciones interactivas avanzadas y procesamiento de lenguaje natural.Pipeline ETL completo para análisis de sentimientos en noticias con visualizaciones interactivas avanzadas y procesamiento de lenguaje natural.



------



## 📋 Tabla de Contenidos## 📋 Tabla de Contenidos



- [Descripción](#-descripción)- [Descripción](#-descripción)

- [Características](#-características)- [Características](#-características)

- [Estructura del Proyecto](#-estructura-del-proyecto)- [Estructura del Proyecto](#-estructura-del-proyecto)

- [Instalación](#-instalación)- [Instalación](#-instalación)

- [Uso](#-uso)- [Uso](#-uso)

- [Gráficas de Análisis](#-gráficas-de-análisis-eda)- [Gráficas de Análisis (EDA)](#-gráficas-de-análisis-eda)

- [Estructura de Datos](#-estructura-de-datos)- [Estructura de Datos](#-estructura-de-datos)

- [Solución de Problemas](#-solución-de-problemas)- [Solución de Problemas](#-solución-de-problemas)

- [Contribuciones](#-contribuciones)- [Contribuciones](#-contribuciones)

- [Autor](#-autor)- [Autor](#-autor)



------



## 🎯 Descripción## 🎯 Descripción



Este proyecto implementa un **pipeline ETL (Extract, Transform, Load)** especializado en el análisis de sentimientos de noticias. Permite procesar grandes volúmenes de datos de noticias, limpiarlos, transformarlos y generar visualizaciones interactivas que revelan patrones temporales, tendencias de sentimiento y análisis de contenido textual.Este proyecto implementa un **pipeline ETL (Extract, Transform, Load)** especializado en el análisis de sentimientos de noticias. Permite procesar grandes volúmenes de datos de noticias, limpiarlos, transformarlos y generar visualizaciones interactivas que revelan patrones temporales, tendencias de sentimiento y análisis de contenido textual.



### ¿Para qué sirve?### ¿Para qué sirve?



- 📊 **Análisis de tendencias** de sentimientos en noticias a lo largo del tiempo- 📊 **Análisis de tendencias** de sentimientos en noticias a lo largo del tiempo

- 🔍 **Identificación de patrones** estacionales y temporales- 🔍 **Identificación de patrones** estacionales y temporales

- 💬 **Minería de texto** para extraer palabras clave más relevantes- 💬 **Minería de texto** para extraer palabras clave más relevantes

- 📈 **Visualización interactiva** de métricas y estadísticas- 📈 **Visualización interactiva** de métricas y estadísticas

- 🧹 **Limpieza automática** de datos (duplicados, nulos, normalización)- 🧹 **Limpieza automática** de datos (duplicados, nulos, normalización)



------



## ✨ Características## ✨ Características



### Pipeline ETL Completo### Pipeline ETL Completo

- ✅ **Extracción**: Lectura de archivos CSV con manejo robusto de errores- ✅ **Extracción**: Lectura de archivos CSV con manejo robusto de errores

- ✅ **Transformación**: Limpieza, normalización y enriquecimiento de datos- ✅ **Transformación**: Limpieza, normalización y enriquecimiento de datos

- ✅ **Carga**: Exportación a múltiples formatos (CSV, JSON, SQLite)- ✅ **Carga**: Exportación a múltiples formatos (CSV, JSON, SQLite)



### Análisis Avanzado### Análisis Avanzado

- 🔤 **Procesamiento de Lenguaje Natural**: Extracción de palabras clave con filtrado de stopwords- 🔤 **Procesamiento de Lenguaje Natural**: Extracción de palabras clave con filtrado de stopwords

- 📅 **Análisis Temporal**: Patrones por día, semana, mes, trimestre y año- 📅 **Análisis Temporal**: Patrones por día, semana, mes, trimestre y año

- 📊 **Visualizaciones Interactivas**: 7 gráficas especializadas con Plotly y Matplotlib- 📊 **Visualizaciones Interactivas**: 7 gráficas especializadas con Plotly y Matplotlib

- 🎨 **Interfaz Intuitiva**: Dashboard construido con Streamlit- 🎨 **Interfaz Intuitiva**: Dashboard construido con Streamlit



### Tecnologías Utilizadas### Tecnologías Utilizadas

- **Python 3.9+**- **Python 3.9+**

- **Streamlit** - Interfaz web interactiva- **Streamlit** - Interfaz web interactiva

- **Pandas** - Manipulación de datos- **Pandas** - Manipulación de datos

- **Plotly** - Visualizaciones interactivas- **Plotly** - Visualizaciones interactivas

- **Matplotlib & Seaborn** - Gráficos estadísticos- **Matplotlib & Seaborn** - Gráficos estadísticos

- **NumPy & SciPy** - Cálculos científicos- **NumPy & SciPy** - Cálculos científicos



------



## 📁 Estructura del Proyecto## 📁 Estructura del Proyecto



``````

ETLsports/ETLsports/

├── Config/├── Config/

│   ├── configuraciones.py          # Configuraciones centralizadas│   ├── configuraciones.py          # Configuraciones centralizadas

│   └── __pycache__/│   └── __pycache__/

├── Extract/├── Extract/

│   ├── nbaExtract.py              # Clase Extractor (CSV reader)│   ├── nbaExtract.py              # Clase Extractor (CSV reader)

│   └── __pycache__/│   └── __pycache__/

├── Transform/├── Transform/

│   ├── nbaTransform.py            # Clase Transformer (limpieza)│   ├── nbaTransform.py            # Clase Transformer (limpieza)

│   └── __pycache__/│   └── __pycache__/

├── Load/├── Load/

│   ├── nbaLoad.py                 # Clase Loader (exportación)│   ├── nbaLoad.py                 # Clase Loader (exportación)

│   └── __pycache__/│   └── __pycache__/

├── data/├── data/

│   ├── input/                     # 📥 Archivos CSV de entrada│   ├── input/                     # 📥 Archivos CSV de entrada

│   │   └── stock_senti_analysis.csv│   │   └── stock_senti_analysis.csv

│   └── output/                    # 📤 Datos procesados│   └── output/                    # 📤 Datos procesados

│       └── stock_senti_analysis_clean.csv│       └── stock_senti_analysis_clean.csv

├── .venv/                         # Entorno virtual (no en Git)├── .venv/                         # Entorno virtual (no en Git)

├── .gitignore                     # Archivos excluidos de Git├── .gitignore                     # Archivos excluidos de Git

├── main.py                        # 🚀 Aplicación Streamlit principal├── main.py                        # 🚀 Aplicación Streamlit principal

├── requirements.txt               # 📦 Dependencias del proyecto├── requirements.txt               # 📦 Dependencias del proyecto

├── fix_permissions.py             # 🛠️ Script de diagnóstico├── fix_permissions.py             # 🛠️ Script de diagnóstico

├── setup_data.py                  # 🔧 Script de configuración├── setup_data.py                  # 🔧 Script de configuración

├── open_folders.py                # 📂 Utilidad para copiar archivos├── open_folders.py                # 📂 Utilidad para copiar archivos

└── README.md                      # 📖 Documentación└── README.md                      # 📖 Documentación

``````



------



## 🚀 Instalación## 🚀 Instalación



### Requisitos Previos### Requisitos Previos

- Python 3.9 o superior- Python 3.9 o superior

- pip (gestor de paquetes de Python)- pip (gestor de paquetes de Python)

- Git (para clonar el repositorio)- Git (para clonar el repositorio)



### Paso 1: Clonar el Repositorio### Paso 1: Clonar el Repositorio



```bash```bash

git clone https://github.com/DSArevalo4/ETLsports.gitgit clone https://github.com/DSArevalo4/ETLsports.git

cd ETLsportscd ETLsports

``````



### Paso 2: Crear Entorno Virtual### Paso 2: Crear Entorno Virtual



**Windows:****Windows:**

```bash```bash

python -m venv .venvpython -m venv .venv

.venv\Scripts\activate.venv\Scripts\activate

``````



**macOS/Linux:****macOS/Linux:**

```bash```bash

python3 -m venv .venvpython3 -m venv .venv

source .venv/bin/activatesource .venv/bin/activate

``````



### Paso 3: Instalar Dependencias### Paso 3: Instalar Dependencias



```bash```bash

pip install -r requirements.txtpip install -r requirements.txt

``````



### Paso 4: Preparar los Datos### Paso 4: Preparar los Datos



Coloca tu archivo CSV en la carpeta `data/input/`:Coloca tu archivo CSV en la carpeta `data/input/`:



```bash```bash

# Crear estructura de directorios# Crear estructura de directorios

mkdir data\input data\outputmkdir -p data/input data/output



# Copiar tu archivo CSV (Windows PowerShell)# Copiar tu archivo CSV

Copy-Item "C:\ruta\a\tu\archivo.csv" "data\input\stock_senti_analysis.csv"# Windows PowerShell:

```Copy-Item "C:\ruta\a\tu\archivo.csv" "data\input\stock_senti_analysis.csv"



O usa el script auxiliar:# Linux/macOS:

```bashcp /ruta/a/tu/archivo.csv data/input/stock_senti_analysis.csv

python setup_data.py```

```

O usa el script auxiliar:

---```bash

python setup_data.py

## 💻 Uso```



### Opción 1: Interfaz Streamlit (Recomendado)---



```bash## 💻 Uso

streamlit run main.py

```### Opción 1: Interfaz Streamlit (Recomendado)



La aplicación se abrirá automáticamente en `http://localhost:8501````bash

streamlit run main.py

**Funcionalidades:**```

1. 📁 Selección de archivo CSV desde interfaz

2. 🧹 Opciones de limpieza configurables (duplicados, nulos, normalización)La aplicación se abrirá automáticamente en tu navegador en `http://localhost:8501`

3. 📊 Generación automática de 7 gráficas interactivas

4. 💾 Descarga de datos limpios en CSV/JSON**Funcionalidades:**

5. 📈 Visualización en tiempo real de estadísticas1. 📁 Selección de archivo CSV desde interfaz

2. 🧹 Opciones de limpieza configurables (duplicados, nulos, normalización)

### Opción 2: Pipeline ETL Programático3. 📊 Generación automática de 7 gráficas interactivas

4. 💾 Descarga de datos limpios en CSV/JSON

```python5. 📈 Visualización en tiempo real de estadísticas

from Extract.nbaExtract import Extractor

from Transform.nbaTransform import Transformer### Opción 2: Pipeline ETL Programático

from Load.nbaLoad import Loader

```python

# 1. EXTRACCIÓNfrom Extract.nbaExtract import Extractor

extractor = Extractor("data/input/stock_senti_analysis.csv")from Transform.nbaTransform import Transformer

df = extractor.extract()from Load.nbaLoad import Loader



# 2. TRANSFORMACIÓN# 1. EXTRACCIÓN

df_clean = Transformer.clean_data(extractor = Extractor("data/input/stock_senti_analysis.csv")

    df,df = extractor.extract()

    remove_duplicates=True,

    remove_na=True,# 2. TRANSFORMACIÓN

    normalize_columns=True,df_clean = Transformer.clean_data(

    parse_dates=True    df,

)    remove_duplicates=True,

    remove_na=True,

# Añadir características derivadas    normalize_columns=True,

df_enhanced = Transformer.add_derived_features(df_clean)    parse_dates=True,

    date_column='Date'

# 3. CARGA)

loader = Loader(df_enhanced)

loader.to_csv("data/output/sentiments_clean.csv")# Añadir características derivadas

loader.to_sqlite("data/output/sentiments.db", "sentiments_clean")df_enhanced = Transformer.add_derived_features(df_clean)

```

# 3. CARGA

---loader = Loader(df_enhanced)

loader.to_csv("data/output/sentiments_clean.csv")

## 📊 Gráficas de Análisis (EDA)loader.to_parquet("data/output/sentiments_clean.parquet")

loader.to_sqlite("data/output/sentiments.db", "sentiments_clean")

La aplicación genera **7 gráficas especializadas**:```



### 1️⃣ Distribución de Sentimientos---

- Gráfico de barras con cantidad de noticias positivas/negativas

- Gráfico de dona con proporciones## 📊 Gráficas de Análisis (EDA)

- Métricas en tiempo real (%, totales)

La aplicación genera **7 gráficas especializadas** para análisis exhaustivo:

### 2️⃣ Evolución Temporal del Sentimiento

- Serie temporal de volumen de noticias### 1️⃣ Distribución de Sentimientos

- Índice de sentimiento con media móvil de 7 días**Visualizaciones:**

- Línea de referencia neutral- Gráfico de barras con cantidad de noticias positivas/negativas

- Gráfico de dona con proporciones

### 3️⃣ Patrones Temporales (3 tabs)- Métricas en tiempo real (% positivo, % negativo, total)

- **Por Año**: Distribución anual y tabla resumen

- **Por Mes**: Sentimiento promedio y volumen mensual**Insights:**

- **Por Día de Semana**: Radar chart + volumen- Balance general del sentimiento en el dataset

- Detección de sesgo en los datos

### 4️⃣ Análisis de Palabras Clave (3 tabs)- Estadísticas descriptivas completas

- **Top Palabras**: Top 20 palabras más frecuentes

- **Palabras Positivas**: Treemap contextual---

- **Palabras Negativas**: Treemap contextual

### 2️⃣ Evolución Temporal del Sentimiento

### 5️⃣ Longitud de Títulos vs Sentimiento**Visualizaciones:**

- Boxplot comparativo- Serie temporal de volumen de noticias por sentimiento

- Violin plot con distribución detallada- Índice de sentimiento con media móvil de 7 días (suavizado)

- Tabla estadística completa- Línea de referencia neutral (0.5)



### 6️⃣ Mapa de Calor Mes-Año**Insights:**

- Heatmap interactivo (Plotly)- Identificación de períodos de sentimiento positivo/negativo

- Escala de colores: Rojo → Verde- Tendencias a largo plazo

- Patrones estacionales- Detección de eventos anómalos



### 7️⃣ Análisis por Trimestre---

- Tendencia trimestral suavizada

- Gráfico de barras Q1-Q4### 3️⃣ Patrones Temporales

- Tabla resumen**3 Pestañas Interactivas:**



---**📆 Por Año:**

- Distribución anual agrupada

## 📝 Estructura de Datos- Tabla resumen con % de sentimiento positivo



### CSV de Entrada**📅 Por Mes:**

- Sentimiento promedio mensual (gráfico de barras coloreado)

```csv- Volumen de noticias por mes (gráfico de líneas)

Date,Label,Top1,Top2,Top3,...,Top25

2024-01-15,1,"Breaking News","Tech Stocks",...**🗓️ Por Día de Semana:**

2024-01-16,0,"Economic Concerns","Inflation",...- Radar chart del sentimiento por día

```- Gráfico de barras del volumen por día



### Columnas Requeridas**Insights:**

- Patrones estacionales

| Columna | Tipo | Descripción | Valores |- Días de mayor/menor actividad

|---------|------|-------------|---------|- Tendencias anuales

| `Date` | datetime | Fecha | YYYY-MM-DD |

| `Label` | int | Sentimiento | 0=Negativo, 1=Positivo |---

| `Top1-Top25` | string | Títulos de noticias | Texto libre |

### 4️⃣ Análisis de Palabras Clave en Títulos

### Columnas Generadas**3 Pestañas Especializadas:**



- `Year`, `Month`, `Month_Name`, `Day_of_Week`**📊 Top Palabras:**

- `Quarter`, `Week`- Top 20 palabras más frecuentes (todas las noticias)

- `Sentiment_Text` (Positivo/Negativo)- Gráfico de barras horizontal ordenado

- `Avg_Title_Length`

**😊 Palabras Positivas:**

---- Treemap de palabras en noticias positivas

- Tamaño proporcional a frecuencia

## 🛠️ Solución de Problemas

**😞 Palabras Negativas:**

### Error: `streamlit: command not found`- Treemap de palabras en noticias negativas

```bash- Identificación de temas críticos

.venv\Scripts\activate  # Windows

pip install streamlit**Características:**

streamlit --version- Filtrado automático de stopwords en inglés

```- Procesamiento con expresiones regulares

- Análisis contextual por sentimiento

### Error: `PermissionError` al leer CSV

**Solución:**---

1. Cierra Excel completamente

2. Cierra Explorador de Windows### 5️⃣ Longitud de Títulos vs Sentimiento

3. Ejecuta: `python fix_permissions.py`**Visualizaciones:**

- Boxplot comparativo (detección de outliers)

### No se listan archivos- Violin plot con distribución detallada

```bash- Tabla estadística completa

dir data\input\  # Windows

# Debe contener archivos .csv**Insights:**

```- ¿Las noticias positivas tienen títulos más largos/cortos?

- Identificación de patrones en longitud textual

### JSON Serialization Error- Detección de anomalías en formato

✅ **Ya solucionado** - Conversión automática de Timestamps

---

---

### 6️⃣ Mapa de Calor Mes-Año

## 📚 Dependencias**Visualización:**

- Heatmap interactivo (Plotly)

```plaintext- Eje X: Años | Eje Y: Meses

streamlit>=1.28.0- Escala de colores: Rojo (negativo) → Verde (positivo)

pandas>=2.0.0

numpy>=1.24.0**Insights:**

matplotlib>=3.7.0- Identificación de patrones estacionales

seaborn>=0.12.0- Comparación año tras año

plotly>=5.14.0- Detección de períodos críticos

scipy>=1.10.0

openpyxl>=3.1.0---

sqlalchemy>=2.0.0

pyarrow>=12.0.0### 7️⃣ Análisis por Trimestre

```**Visualizaciones:**

- Tendencia trimestral con spline suavizado

---- Gráfico de barras de % positivo por trimestre (Q1-Q4)

- Tabla resumen con estadísticas

## 🤝 Contribuciones

**Insights:**

### Convenciones de Commits- Comparación de desempeño trimestral

- `feat:` Nueva funcionalidad- Identificación de trimestres críticos

- `fix:` Corrección de bug- Análisis de ciclos empresariales

- `docs:` Documentación

- `refactor:` Refactorización---



### Proceso## 📝 Estructura de Datos

```bash

git clone https://github.com/TU_USUARIO/ETLsports.git### Formato del CSV de Entrada

git checkout -b feature/nueva-funcionalidad

git commit -m "feat: Añade X funcionalidad"El archivo `stock_senti_analysis.csv` debe tener la siguiente estructura:

git push origin feature/nueva-funcionalidad

``````csv

Date,Label,Top1,Top2,Top3,...,Top25

---2024-01-15,1,"Breaking News: Markets Rally","Tech Stocks Surge",...

2024-01-16,0,"Economic Concerns Grow","Inflation Worries",...

## 👤 Autor```



**Daniel Arevalo**  ### Columnas Requeridas

🔗 GitHub: [@DSArevalo4](https://github.com/DSArevalo4)  

📧 Email: daniel.arevalo@example.com| Columna | Tipo | Descripción | Valores |

|---------|------|-------------|---------|

---| `Date` | datetime | Fecha de la noticia | YYYY-MM-DD |

| `Label` | int | Sentimiento de la noticia | 0=Negativo, 1=Positivo |

## 📄 Licencia| `Top1` - `Top25` | string | Títulos de noticias principales | Texto libre |



MIT License - Uso educativo y personal### Columnas Generadas Automáticamente



---Durante la transformación, se añaden:

- `Year`: Año extraído de Date

## 🙏 Agradecimientos- `Month`: Mes (1-12)

- `Month_Name`: Nombre del mes (January, February, ...)

- **Streamlit Team** - Librería de visualización- `Day_of_Week`: Día de la semana (Monday, Tuesday, ...)

- **Plotly** - Gráficos interactivos- `Quarter`: Trimestre (Q1, Q2, Q3, Q4)

- **Pandas Community** - Ecosistema de datos- `Week`: Número de semana del año

- **GitHub Copilot** - Asistencia en desarrollo- `Sentiment_Text`: "Positivo" o "Negativo" (categórico)

- `Avg_Title_Length`: Longitud promedio de títulos

---

---

## 📈 Roadmap

## 🛠️ Parámetros de Configuración

- [ ] API de noticias en tiempo real

- [ ] Modelos ML (BERT, LSTM)### Opciones de Limpieza

- [ ] Dashboard multi-página

- [ ] Soporte multiidioma```python

- [ ] Contenedorización DockerTransformer.clean_data(

- [ ] CI/CD con GitHub Actions    df,

    remove_duplicates=True,      # Elimina filas duplicadas

---    remove_na=True,               # Elimina filas con valores nulos

    normalize_columns=True,       # Normaliza nombres de columnas

## 📞 Soporte    parse_dates=True,             # Convierte Date a datetime

    date_column='Date'            # Nombre de columna de fecha

1. 📖 Lee la documentación)

2. 🐛 Reporta en [Issues](https://github.com/DSArevalo4/ETLsports/issues)```

3. 💬 [Discusiones](https://github.com/DSArevalo4/ETLsports/discussions)

4. ⭐ Dale estrella si te fue útil### Formatos de Exportación



---| Formato | Ventajas | Uso Recomendado |

|---------|----------|-----------------|

<div align="center">| **CSV** | Compatibilidad universal | Compartir datos, Excel |

| **Parquet** | Alta compresión, rápido | Big Data, almacenamiento |

**Hecho con ❤️ por Daniel Arevalo**| **SQLite** | Consultas SQL, relacional | Análisis complejo, joins |

| **JSON** | Estructura flexible | APIs, intercambio web |

[![Stars](https://img.shields.io/github/stars/DSArevalo4/ETLsports?style=social)](https://github.com/DSArevalo4/ETLsports)

[![Forks](https://img.shields.io/github/forks/DSArevalo4/ETLsports?style=social)](https://github.com/DSArevalo4/ETLsports)---



</div>## 🐛 Solución de Problemas


### Error: `streamlit: command not found`
**Solución:**
```bash
# Verifica que el entorno virtual esté activado
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # macOS/Linux

# Reinstala streamlit
pip install streamlit

# Verifica la instalación
streamlit --version
```

---

### Error: `PermissionError` al leer CSV
**Causas comunes:**
- Excel tiene el archivo abierto
- El Explorador de Windows está previsualizando el archivo

**Soluciones:**
1. Cierra Excel completamente
2. Cierra todas las ventanas del Explorador
3. Ejecuta el script auxiliar:
```bash
python fix_permissions.py
```
4. O crea una copia del archivo:
```bash
copy data\input\archivo.csv data\input\archivo_backup.csv
```

---

### Error: No se listan archivos en la aplicación
**Solución:**
```bash
# Verifica la estructura de carpetas
ls data/input/  # Linux/macOS
dir data\input\  # Windows

# Debe contener al menos un archivo .csv
# Si no existe, créala:
mkdir -p data/input  # Linux/macOS
mkdir data\input  # Windows
```

---

### Error: `TypeError: Object of type Timestamp is not JSON serializable`
✅ **Ya solucionado** en la versión actual. El código convierte automáticamente Timestamps a strings.

---

### Warnings de Git (LF/CRLF)
**Solución:**
```bash
# Configura Git para manejar finales de línea
git config core.autocrlf true  # Windows
git config core.autocrlf input  # macOS/Linux

# El .gitignore ya excluye archivos innecesarios
```

---

## 📚 Dependencias del Proyecto

```plaintext
streamlit>=1.28.0        # Interfaz web interactiva
pandas>=2.0.0            # Manipulación de datos
numpy>=1.24.0            # Cálculos numéricos
matplotlib>=3.7.0        # Gráficos estáticos
seaborn>=0.12.0          # Visualizaciones estadísticas
plotly>=5.14.0           # Gráficos interactivos
scipy>=1.10.0            # Estadísticas avanzadas
openpyxl>=3.1.0          # Lectura de Excel (legacy)
sqlalchemy>=2.0.0        # ORM para bases de datos
pyarrow>=12.0.0          # Formato Parquet
```

---

## 🤝 Contribuciones

Las contribuciones son bienvenidas! Sigue estos pasos:

### 1. Fork el Proyecto
```bash
# Crea un fork en GitHub, luego clónalo:
git clone https://github.com/TU_USUARIO/ETLsports.git
cd ETLsports
```

### 2. Crea una Rama
```bash
git checkout -b feature/nueva-funcionalidad
```

### 3. Realiza tus Cambios
```bash
git add .
git commit -m "feat: Añade nueva funcionalidad X"
```

### 4. Push y Pull Request
```bash
git push origin feature/nueva-funcionalidad
```

Luego abre un Pull Request en GitHub explicando tus cambios.

### Convenciones de Commits
Usamos [Conventional Commits](https://www.conventionalcommits.org/):
- `feat:` Nueva funcionalidad
- `fix:` Corrección de bug
- `docs:` Documentación
- `style:` Formato de código
- `refactor:` Refactorización
- `test:` Tests
- `chore:` Mantenimiento

---

## 👤 Autor

**Daniel Arevalo**  
🔗 GitHub: [@DSArevalo4](https://github.com/DSArevalo4)  
📧 Email: [Contacto](mailto:daniel.arevalo@example.com)

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - mira el archivo [LICENSE](LICENSE) para más detalles.

---

## 🎓 Uso Educativo

Este proyecto fue desarrollado con fines educativos y de investigación. Puede ser utilizado como:
- 📚 Material de aprendizaje para ETL pipelines
- 🎯 Ejemplo de análisis de sentimientos
- 💡 Plantilla para proyectos similares
- 🔬 Base para investigación académica

---

## 🙏 Agradecimientos

- **Streamlit Team** - Por la increíble librería de visualización
- **Plotly** - Por gráficos interactivos de alta calidad
- **Pandas Community** - Por el ecosistema de análisis de datos
- **GitHub Copilot** - Por asistencia en desarrollo

---

## 📈 Roadmap Futuro

- [ ] Integración con APIs de noticias en tiempo real
- [ ] Análisis de sentimiento con modelos ML (BERT, LSTM)
- [ ] Dashboard multi-página con Streamlit
- [ ] Soporte para múltiples idiomas
- [ ] Exportación a PowerBI/Tableau
- [ ] Contenedorización con Docker
- [ ] CI/CD con GitHub Actions
- [ ] Despliegue en Streamlit Cloud

---

## 📞 Soporte

¿Tienes preguntas o problemas?

1. 📖 Lee la [documentación completa](#)
2. 🐛 Reporta bugs en [Issues](https://github.com/DSArevalo4/ETLsports/issues)
3. 💬 Únete a las [Discusiones](https://github.com/DSArevalo4/ETLsports/discussions)
4. ⭐ Dale una estrella al proyecto si te fue útil!

---

<div align="center">

**Hecho con ❤️ por Daniel Arevalo**

[![GitHub Stars](https://img.shields.io/github/stars/DSArevalo4/ETLsports?style=social)](https://github.com/DSArevalo4/ETLsports/stargazers)
[![GitHub Forks](https://img.shields.io/github/forks/DSArevalo4/ETLsports?style=social)](https://github.com/DSArevalo4/ETLsports/network/members)

</div>

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
