"""
Configuraciones centralizadas del proyecto ETL Stock Sentiment Analysis
"""
from pathlib import Path

class Config:
    # Rutas base
    BASE_DIR = Path(__file__).parent.parent
    INPUT_PATH = BASE_DIR / "data" / "input"
    OUTPUT_PATH = BASE_DIR / "data" / "output"
    
    # Base de datos
    SQLITE_DB_PATH = OUTPUT_PATH / "stock_sentiment.db"
    SQLITE_TABLE = "stock_sentiment_clean"
    
    # Archivo CSV de salida
    OUTPUT_CSV = OUTPUT_PATH / "stock_sentiment_clean.csv"
    OUTPUT_PARQUET = OUTPUT_PATH / "stock_sentiment_clean.parquet"
    
    # Columnas esperadas
    EXPECTED_COLUMNS = ['Date', 'Stock', 'Sentiment', 'Price', 'Volume']
    
    # Parámetros de limpieza
    DATE_FORMAT = "%Y-%m-%d"
    REMOVE_DUPLICATES = True
    REMOVE_NA = True
    
    @classmethod
    def create_directories(cls):
        """Crea los directorios necesarios si no existen"""
        cls.INPUT_PATH.mkdir(parents=True, exist_ok=True)
        cls.OUTPUT_PATH.mkdir(parents=True, exist_ok=True)
