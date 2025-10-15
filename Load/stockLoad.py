"""
Módulo de carga de datos limpios
"""
import pandas as pd
import sqlite3
from pathlib import Path
from typing import Union

class Loader:
    """Clase para cargar datos limpios en diferentes formatos"""
    
    def __init__(self, df: pd.DataFrame):
        """
        Inicializa el loader con un DataFrame
        
        Args:
            df: DataFrame a cargar
        """
        self.df = df
    
    def to_csv(self, output_path: Union[str, Path], index: bool = False) -> None:
        """
        Guarda el DataFrame como CSV
        
        Args:
            output_path: Ruta de salida
            index: Incluir índice en el CSV
        """
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        self.df.to_csv(output_path, index=index, encoding='utf-8')
        print(f"✓ Datos guardados en CSV: {output_path}")
    
    def to_parquet(self, output_path: Union[str, Path]) -> None:
        """
        Guarda el DataFrame como Parquet (más eficiente)
        
        Args:
            output_path: Ruta de salida
        """
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        self.df.to_parquet(output_path, index=False)
        print(f"✓ Datos guardados en Parquet: {output_path}")
    
    def to_sqlite(self, db_path: Union[str, Path], table_name: str) -> None:
        """
        Guarda el DataFrame en una tabla SQLite
        
        Args:
            db_path: Ruta a la base de datos
            table_name: Nombre de la tabla
        """
        db_path = Path(db_path)
        db_path.parent.mkdir(parents=True, exist_ok=True)
        
        conn = sqlite3.connect(db_path)
        self.df.to_sql(table_name, conn, if_exists='replace', index=False)
        conn.close()
        
        print(f"✓ Datos guardados en SQLite: {db_path} (tabla: {table_name})")
