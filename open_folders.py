"""
Abre las carpetas necesarias para copiar manualmente
"""
import os
import subprocess
from pathlib import Path

BASE_DIR = Path(__file__).parent
INPUT_DIR = BASE_DIR / "data" / "input"
INPUT_DIR.mkdir(parents=True, exist_ok=True)

DOWNLOADS = Path.home() / "Downloads"

print("=" * 60)
print("  Abriendo carpetas para copia manual")
print("=" * 60)

# Abrir carpeta Downloads
if DOWNLOADS.exists():
    print(f"\n📂 Abriendo Downloads...")
    os.startfile(DOWNLOADS)

# Abrir carpeta data/input
print(f"📂 Abriendo data/input...")
os.startfile(INPUT_DIR)

print("\n✅ Carpetas abiertas")
print("\n📋 Instrucciones:")
print("   1. En Downloads: busca 'stock_senti_analysis.csv'")
print("   2. Cópialo (Ctrl+C)")
print("   3. En data/input: pégalo (Ctrl+V)")
print("\n🚀 Luego ejecuta: streamlit run main.py")
