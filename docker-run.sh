#!/bin/bash
# Script para ejecutar ETL Sentiment Analysis con Docker
# Autor: Daniel Arevalo

# Colores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo -e "${CYAN}========================================"
echo -e "  ETL News Sentiment Analysis - Docker"
echo -e "========================================${NC}"
echo ""

# Verificar que Docker está instalado
if ! command -v docker &> /dev/null; then
    echo -e "${RED}[ERROR] Docker no está instalado${NC}"
    echo -e "${YELLOW}Instálalo desde: https://www.docker.com/products/docker-desktop${NC}"
    exit 1
fi

# Verificar que Docker está corriendo
if ! docker info &> /dev/null; then
    echo -e "${RED}[ERROR] Docker no está corriendo${NC}"
    echo -e "${YELLOW}Por favor, inicia el daemon de Docker${NC}"
    exit 1
fi

echo -e "${GREEN}[OK] Docker está corriendo${NC}"
echo ""

# Crear directorios necesarios
echo -e "${YELLOW}Creando directorios necesarios...${NC}"
mkdir -p data/input data/output
echo -e "${GREEN}[OK] Directorios creados${NC}"
echo ""

# Menú de opciones
echo -e "${CYAN}Selecciona una opción:${NC}"
echo "1. Build y Run (primera vez o después de cambios)"
echo "2. Run (usar imagen existente)"
echo "3. Stop y Remove containers"
echo "4. Build solamente"
echo "5. Ver logs"
echo "6. Salir"
echo ""

read -p "Opción: " opcion

case $opcion in
    1)
        echo ""
        echo -e "${YELLOW}Building imagen Docker...${NC}"
        docker-compose build --no-cache
        
        if [ $? -eq 0 ]; then
            echo -e "${GREEN}[OK] Imagen construida exitosamente${NC}"
            echo ""
            echo -e "${YELLOW}Iniciando contenedor...${NC}"
            docker-compose up -d
            
            if [ $? -eq 0 ]; then
                echo -e "${GREEN}[OK] Contenedor iniciado${NC}"
                echo ""
                echo -e "${CYAN}========================================${NC}"
                echo -e "${GREEN}  Aplicación disponible en:${NC}"
                echo -e "${YELLOW}  http://localhost:8501${NC}"
                echo -e "${CYAN}========================================${NC}"
                echo ""
                echo -e "Para ver logs: docker-compose logs -f"
                echo -e "Para detener: docker-compose down"
                
                # Abrir navegador automáticamente (Linux/macOS)
                sleep 3
                if command -v xdg-open &> /dev/null; then
                    xdg-open http://localhost:8501
                elif command -v open &> /dev/null; then
                    open http://localhost:8501
                fi
            fi
        fi
        ;;
    
    2)
        echo ""
        echo -e "${YELLOW}Iniciando contenedor...${NC}"
        docker-compose up -d
        
        if [ $? -eq 0 ]; then
            echo -e "${GREEN}[OK] Contenedor iniciado${NC}"
            echo ""
            echo -e "${YELLOW}Aplicación disponible en: http://localhost:8501${NC}"
            sleep 3
            if command -v xdg-open &> /dev/null; then
                xdg-open http://localhost:8501
            elif command -v open &> /dev/null; then
                open http://localhost:8501
            fi
        fi
        ;;
    
    3)
        echo ""
        echo -e "${YELLOW}Deteniendo y removiendo contenedores...${NC}"
        docker-compose down
        
        if [ $? -eq 0 ]; then
            echo -e "${GREEN}[OK] Contenedores detenidos y removidos${NC}"
        fi
        ;;
    
    4)
        echo ""
        echo -e "${YELLOW}Building imagen Docker...${NC}"
        docker-compose build --no-cache
        
        if [ $? -eq 0 ]; then
            echo -e "${GREEN}[OK] Imagen construida exitosamente${NC}"
        fi
        ;;
    
    5)
        echo ""
        echo -e "${YELLOW}Mostrando logs (Ctrl+C para salir)...${NC}"
        docker-compose logs -f
        ;;
    
    6)
        echo -e "${YELLOW}Saliendo...${NC}"
        exit 0
        ;;
    
    *)
        echo -e "${RED}[ERROR] Opción inválida${NC}"
        exit 1
        ;;
esac

echo ""
