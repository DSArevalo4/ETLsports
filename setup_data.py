"""
Script auxiliar para copiar archivos CSV a la carpeta data/input/
"""
import shutil
import os
from pathlib import Path

# Rutas
BASE_DIR = Path(__file__).parent
INPUT_DIR = BASE_DIR / "data" / "input"
DOWNLOADS = Path.home() / "Downloads"

# Crear directorio si no existe
INPUT_DIR.mkdir(parents=True, exist_ok=True)

# Buscar archivo CSV en Downloads
csv_file = DOWNLOADS / "stock_senti_analysis.csv"

if csv_file.exists():
    destination = INPUT_DIR / "stock_senti_analysis.csv"
    
    try:
        # Intentar diferentes métodos de copia
        print(f"📂 Origen: {csv_file}")
        print(f"📂 Destino: {destination}")
        print(f"📊 Tamaño origen: {csv_file.stat().st_size / 1024:.2f} KB")
        
        # Método 1: Leer y escribir (evita problemas de permisos)
        with open(csv_file, 'rb') as f_src:
            with open(destination, 'wb') as f_dst:
                f_dst.write(f_src.read())
        
        print(f"\n✅ Archivo copiado exitosamente")
        print(f"📊 Tamaño destino: {destination.stat().st_size / 1024:.2f} KB")
        print(f"\n🚀 Ahora puedes ejecutar: streamlit run main.py")
        
    except PermissionError as e:
        print(f"\n❌ Error de permisos: {e}")
        print("\n💡 Soluciones alternativas:")
        print("   1. Ejecuta PowerShell como Administrador")
        print("   2. Copia manualmente el archivo:")
        print(f"      Desde: {csv_file}")
        print(f"      Hasta: {destination}")
        print("   3. Cierra Excel u otros programas que puedan tener el archivo abierto")
        
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        print(f"\n💡 Copia manual:")
        print(f"   1. Abre el explorador en: {csv_file.parent}")
        print(f"   2. Copia 'stock_senti_analysis.csv'")
        print(f"   3. Pégalo en: {INPUT_DIR}")
        
else:
    print(f"❌ No se encontró el archivo en: {csv_file}")
    print("\n💡 Opciones:")
    print("   1. Verifica que el archivo esté en Downloads")
    print("   2. O especifica otra ubicación:")
    print("\n   Ejemplo de uso manual:")
    print("   >>> from pathlib import Path")
    print("   >>> import shutil")
    print("   >>> shutil.copy('ruta/al/archivo.csv', 'data/input/'')")
