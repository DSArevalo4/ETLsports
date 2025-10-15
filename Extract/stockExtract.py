"""
Módulo de extracción de datos de sentimiento de acciones
"""
import pandas as pd
from pathlib import Path
from typing import Union

class Extractor:
    """Clase para extraer datos desde archivos CSV"""
    
    def __init__(self, file_path: Union[str, Path]):
        """
        Inicializa el extractor
        
        Args:
            file_path: Ruta al archivo CSV
        """
        self.file_path = Path(file_path)
        
    def extract(self) -> pd.DataFrame:
        """
        Lee el archivo CSV y retorna un DataFrame
        
        Returns:
            DataFrame con los datos extraídos
            
        Raises:
            FileNotFoundError: Si el archivo no existe
            pd.errors.EmptyDataError: Si el archivo está vacío
        """
        if not self.file_path.exists():
            raise FileNotFoundError(f"El archivo {self.file_path} no existe")
        
        try:
            df = pd.read_csv(self.file_path, encoding='utf-8')
            print(f"✓ Datos extraídos: {df.shape[0]} filas, {df.shape[1]} columnas")
            return df
        except pd.errors.EmptyDataError:
            raise pd.errors.EmptyDataError(f"El archivo {self.file_path} está vacío")
        except Exception as e:
            raise Exception(f"Error al leer el archivo: {str(e)}")
    
    def get_info(self) -> dict:
        """
        Obtiene información básica del archivo
        
        Returns:
            Diccionario con información del archivo
        """
        if self.file_path.exists():
            return {
                'nombre': self.file_path.name,
                'tamaño_mb': self.file_path.stat().st_size / (1024 * 1024),
                'ruta': str(self.file_path)
            }
        return {}
