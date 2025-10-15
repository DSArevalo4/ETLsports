"""
Script interactivo para copiar CSV desde cualquier ubicación
"""
from pathlib import Path
import sys

def copy_csv_file(source_path: str):
    """Copia archivo CSV a data/input/"""
    BASE_DIR = Path(__file__).parent
    INPUT_DIR = BASE_DIR / "data" / "input"
    INPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    source = Path(source_path)
    
    if not source.exists():
        print(f"❌ El archivo no existe: {source}")
        return False
    
    if not source.suffix.lower() == '.csv':
        print(f"⚠️ El archivo no es CSV: {source.suffix}")
        response = input("¿Continuar de todos modos? (s/n): ")
        if response.lower() != 's':
            return False
    
    destination = INPUT_DIR / source.name
    
    try:
        # Leer y escribir bytes (evita problemas de permisos)
        with open(source, 'rb') as f_src:
            content = f_src.read()
        
        with open(destination, 'wb') as f_dst:
            f_dst.write(content)
        
        print(f"\n✅ Archivo copiado exitosamente")
        print(f"📂 Destino: {destination}")
        print(f"📊 Tamaño: {len(content) / 1024:.2f} KB")
        return True
        
    except Exception as e:
        print(f"❌ Error al copiar: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("  Copiar CSV a data/input/")
    print("=" * 60)
    
    # Ruta por defecto
    default_path = Path.home() / "Downloads" / "stock_senti_analysis.csv"
    
    if default_path.exists():
        print(f"\n📁 Archivo encontrado: {default_path}")
        response = input("¿Copiar este archivo? (s/n): ")
        if response.lower() == 's':
            if copy_csv_file(str(default_path)):
                print("\n🚀 Ejecuta: streamlit run main.py")
            sys.exit(0)
    
    # Pedir ruta manualmente
    print("\nIngresa la ruta completa del archivo CSV:")
    print("Ejemplo: C:\\Users\\SANTY\\Downloads\\archivo.csv")
    print("(O arrastra el archivo a esta ventana)\n")
    
    user_path = input("Ruta: ").strip().strip('"')
    
    if user_path:
        if copy_csv_file(user_path):
            print("\n🚀 Ejecuta: streamlit run main.py")
    else:
        print("❌ No se proporcionó ninguna ruta")
