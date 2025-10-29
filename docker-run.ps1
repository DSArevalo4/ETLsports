# Script de PowerShell para ejecutar ETL Sentiment Analysis con Docker
# Autor: Daniel Arevalo

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  ETL News Sentiment Analysis - Docker" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Verificar que Docker está instalado
if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
    Write-Host "[ERROR] Docker no está instalado o no está en el PATH" -ForegroundColor Red
    Write-Host "Descárgalo desde: https://www.docker.com/products/docker-desktop" -ForegroundColor Yellow
    exit 1
}

# Verificar que Docker está corriendo
$dockerInfo = docker info 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERROR] Docker no está corriendo" -ForegroundColor Red
    Write-Host "Por favor, inicia Docker Desktop" -ForegroundColor Yellow
    exit 1
}

Write-Host "[OK] Docker está corriendo" -ForegroundColor Green
Write-Host ""

# Crear directorios necesarios
Write-Host "Creando directorios necesarios..." -ForegroundColor Yellow
New-Item -ItemType Directory -Path "data\input" -Force | Out-Null
New-Item -ItemType Directory -Path "data\output" -Force | Out-Null
Write-Host "[OK] Directorios creados" -ForegroundColor Green
Write-Host ""

# Menú de opciones
Write-Host "Selecciona una opción:" -ForegroundColor Cyan
Write-Host "1. Build y Run (primera vez o después de cambios)" -ForegroundColor White
Write-Host "2. Run (usar imagen existente)" -ForegroundColor White
Write-Host "3. Stop y Remove containers" -ForegroundColor White
Write-Host "4. Build solamente" -ForegroundColor White
Write-Host "5. Ver logs" -ForegroundColor White
Write-Host "6. Salir" -ForegroundColor White
Write-Host ""

$opcion = Read-Host "Opción"

switch ($opcion) {
    "1" {
        Write-Host ""
        Write-Host "Building imagen Docker..." -ForegroundColor Yellow
        docker-compose build --no-cache
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "[OK] Imagen construida exitosamente" -ForegroundColor Green
            Write-Host ""
            Write-Host "Iniciando contenedor..." -ForegroundColor Yellow
            docker-compose up -d
            
            if ($LASTEXITCODE -eq 0) {
                Write-Host "[OK] Contenedor iniciado" -ForegroundColor Green
                Write-Host ""
                Write-Host "========================================" -ForegroundColor Cyan
                Write-Host "  Aplicación disponible en:" -ForegroundColor Green
                Write-Host "  http://localhost:8501" -ForegroundColor Yellow
                Write-Host "========================================" -ForegroundColor Cyan
                Write-Host ""
                Write-Host "Para ver logs: docker-compose logs -f" -ForegroundColor Gray
                Write-Host "Para detener: docker-compose down" -ForegroundColor Gray
                
                # Abrir navegador automáticamente
                Start-Sleep -Seconds 3
                Start-Process "http://localhost:8501"
            }
        }
    }
    
    "2" {
        Write-Host ""
        Write-Host "Iniciando contenedor..." -ForegroundColor Yellow
        docker-compose up -d
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "[OK] Contenedor iniciado" -ForegroundColor Green
            Write-Host ""
            Write-Host "Aplicación disponible en: http://localhost:8501" -ForegroundColor Yellow
            Start-Sleep -Seconds 3
            Start-Process "http://localhost:8501"
        }
    }
    
    "3" {
        Write-Host ""
        Write-Host "Deteniendo y removiendo contenedores..." -ForegroundColor Yellow
        docker-compose down
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "[OK] Contenedores detenidos y removidos" -ForegroundColor Green
        }
    }
    
    "4" {
        Write-Host ""
        Write-Host "Building imagen Docker..." -ForegroundColor Yellow
        docker-compose build --no-cache
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "[OK] Imagen construida exitosamente" -ForegroundColor Green
        }
    }
    
    "5" {
        Write-Host ""
        Write-Host "Mostrando logs (Ctrl+C para salir)..." -ForegroundColor Yellow
        docker-compose logs -f
    }
    
    "6" {
        Write-Host "Saliendo..." -ForegroundColor Yellow
        exit 0
    }
    
    default {
        Write-Host "[ERROR] Opción inválida" -ForegroundColor Red
        exit 1
    }
}

Write-Host ""
