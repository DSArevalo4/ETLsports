"""
Módulo de transformación y limpieza de datos de sentimiento de acciones
"""
import pandas as pd
import numpy as np
from typing import Optional

class Transformer:
    """Clase para transformar y limpiar datos de sentimiento de acciones"""
    
    @staticmethod
    def clean_data(
        df: pd.DataFrame,
        remove_duplicates: bool = True,
        remove_na: bool = True,
        normalize_columns: bool = True,
        parse_dates: bool = True,
        date_column: str = 'Date'
    ) -> pd.DataFrame:
        """
        Limpia y transforma el DataFrame
        
        Args:
            df: DataFrame original
            remove_duplicates: Eliminar filas duplicadas
            remove_na: Eliminar filas con valores nulos
            normalize_columns: Normalizar nombres de columnas
            parse_dates: Convertir columna de fecha a datetime
            date_column: Nombre de la columna de fecha
            
        Returns:
            DataFrame limpio
        """
        df_clean = df.copy()
        
        print(f"Filas iniciales: {len(df_clean)}")
        
        # Normalizar nombres de columnas
        if normalize_columns:
            df_clean.columns = df_clean.columns.str.strip().str.replace(' ', '_')
            print("✓ Columnas normalizadas")
        
        # Parsear fechas
        if parse_dates and date_column in df_clean.columns:
            df_clean[date_column] = pd.to_datetime(df_clean[date_column], errors='coerce')
            print(f"✓ Columna '{date_column}' convertida a datetime")
        
        # Eliminar duplicados
        if remove_duplicates:
            before = len(df_clean)
            df_clean = df_clean.drop_duplicates()
            removed = before - len(df_clean)
            if removed > 0:
                print(f"✓ Eliminados {removed} duplicados")
        
        # Eliminar valores nulos
        if remove_na:
            before = len(df_clean)
            df_clean = df_clean.dropna()
            removed = before - len(df_clean)
            if removed > 0:
                print(f"✓ Eliminadas {removed} filas con valores nulos")
        
        print(f"Filas finales: {len(df_clean)}")
        
        return df_clean
    
    @staticmethod
    def add_derived_features(df: pd.DataFrame) -> pd.DataFrame:
        """
        Añade columnas derivadas para análisis
        
        Args:
            df: DataFrame limpio
            
        Returns:
            DataFrame con nuevas columnas
        """
        df_enhanced = df.copy()
        
        # Extraer año, mes, día de la semana
        if 'Date' in df_enhanced.columns:
            df_enhanced['Year'] = df_enhanced['Date'].dt.year
            df_enhanced['Month'] = df_enhanced['Date'].dt.month
            df_enhanced['Month_Name'] = df_enhanced['Date'].dt.month_name()
            df_enhanced['Day_of_Week'] = df_enhanced['Date'].dt.day_name()
            df_enhanced['Quarter'] = df_enhanced['Date'].dt.quarter
            print("✓ Características temporales añadidas")
        
        # Categorizar sentimiento si es numérico
        if 'Sentiment' in df_enhanced.columns:
            if pd.api.types.is_numeric_dtype(df_enhanced['Sentiment']):
                df_enhanced['Sentiment_Category'] = pd.cut(
                    df_enhanced['Sentiment'],
                    bins=[-np.inf, -0.3, 0.3, np.inf],
                    labels=['Negative', 'Neutral', 'Positive']
                )
                print("✓ Sentimiento categorizado")
        
        return df_enhanced
