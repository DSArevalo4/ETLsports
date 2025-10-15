"""
Script para verificar que todas las dependencias están instaladas correctamente
"""
import sys

print("=" * 60)
print("Verificación de Instalación - ETL Stock Sentiment")
print("=" * 60)

# Verificar versión de Python
print(f"\n✓ Python version: {sys.version}")
print(f"✓ Python executable: {sys.executable}")

# Lista de dependencias requeridas
required_packages = [
    'streamlit',
    'pandas',
    'numpy',
    'matplotlib',
    'seaborn',
    'plotly',
    'openpyxl',
    'sqlalchemy',
    'pyarrow'
]

print("\n" + "=" * 60)
print("Verificando paquetes instalados:")
print("=" * 60)

missing_packages = []

for package in required_packages:
    try:
        if package == 'openpyxl':
            __import__('openpyxl')
        else:
            __import__(package)
        print(f"✅ {package:<20} - INSTALADO")
    except ImportError:
        print(f"❌ {package:<20} - NO ENCONTRADO")
        missing_packages.append(package)

print("\n" + "=" * 60)

if missing_packages:
    print("⚠️  Paquetes faltantes detectados:")
    print("   Ejecuta: pip install " + " ".join(missing_packages))
else:
    print("✅ Todas las dependencias están instaladas correctamente")
    print("\n🚀 Puedes ejecutar la aplicación con:")
    print("   streamlit run main.py")

print("=" * 60)
