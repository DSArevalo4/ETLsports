ETLsports — ETL y visualización de estadísticas de jugadores NBA

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
```
python -m venv .venv
.venv\\Scripts\\activate   # Windows PowerShell
# source .venv/bin/activate  # macOS/Linux
```

2) Instalar dependencias
```
pip install -r requeriments.txt
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
1) Interfaz Streamlit (exploración y visualización)
La app de `main.py` lista los .xlsx en `NBAplayers/`, permite una limpieza básica y genera gráficos.
```
streamlit run main.py
```
Notas:
- La ruta de datos en `main.py` está fijada en `DATA_DIR = '/workspaces/ETLsports/NBAplayers'`.
- En Windows, ajusta esa constante si tu ruta local difiere, por ejemplo:
```
DATA_DIR = 'C:/Users/SANTY/ETLsports/NBAplayers'
```

2) Flujo ETL programático (batch)
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
- No se listan archivos en la app: confirma que `DATA_DIR` apunta a `NBAplayers/` y que hay `.xlsx` válidos.
- Error al leer Excel: verifica la instalación de `openpyxl` y que el archivo no esté corrupto o bloqueado.
- Error de ruta en `Config`: ajusta las rutas a tu entorno y evita rutas absolutas de otro workspace.
- Gráficos vacíos: revisa que las columnas (`Age`, `TRB`, `PTS`, `Pos`) existan en tu dataset.

Licencia
Libre uso educativo y personal. Ajusta según tus necesidades.
