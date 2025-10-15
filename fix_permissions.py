"""
Script para diagnosticar y solucionar problemas de permisos con archivos CSV
"""
import os
import sys
from pathlib import Path

def check_file_access(file_path):
    """Verifica si un archivo es accesible"""
    file_path = Path(file_path)
    
    print(f"Verificando: {file_path}")
    print(f"Existe: {file_path.exists()}")
    
    if file_path.exists():
        print(f"Tamaño: {file_path.stat().st_size / 1024:.2f} KB")
        
        # Intentar abrir en modo lectura
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                f.read(100)  # Leer solo primeros bytes
            print("✅ Archivo accesible para lectura")
            return True
        except PermissionError:
            print("❌ Error de permisos - El archivo está siendo usado")
            print("\n💡 Soluciones:")
            print("   1. Cierra Excel si lo tienes abierto")
            print("   2. Cierra el Explorador de Windows")
            print("   3. Reinicia el proceso de Python/Streamlit")
            return False
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
    else:
        print("❌ El archivo no existe")
        return False

if __name__ == "__main__":
    data_dir = Path(__file__).parent / "data" / "input"
    
    print("=" * 60)
    print("  Diagnóstico de Permisos de Archivos")
    print("=" * 60)
    print()
    
    if not data_dir.exists():
        print(f"❌ La carpeta no existe: {data_dir}")
        print("Creando carpeta...")
        data_dir.mkdir(parents=True, exist_ok=True)
        print("✅ Carpeta creada")
    
    csv_files = list(data_dir.glob("*.csv"))
    
    if not csv_files:
        print(f"⚠️ No hay archivos CSV en: {data_dir}")
    else:
        print(f"Archivos encontrados: {len(csv_files)}")
        print()
        for csv_file in csv_files:
            check_file_access(csv_file)
            print()
    
    print("=" * 60)
