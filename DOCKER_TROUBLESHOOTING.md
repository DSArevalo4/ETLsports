# ⚠️ Instrucciones para Solucionar Problema de Docker

## Problema Detectado
Docker Desktop no está respondiendo correctamente al API.

## Solución Paso a Paso

### 1. Reiniciar Docker Desktop

**Opción A: Desde la Interfaz**
1. Click derecho en el icono de Docker en la bandeja del sistema (🐳)
2. Selecciona "Quit Docker Desktop"
3. Espera 10 segundos
4. Abre Docker Desktop nuevamente desde el menú Inicio
5. Espera a que aparezca "Docker Desktop is running" en verde

**Opción B: Desde PowerShell (Administrador)**
```powershell
# Detener Docker Desktop
Stop-Process -Name "Docker Desktop" -Force

# Esperar 10 segundos
Start-Sleep -Seconds 10

# Iniciar Docker Desktop
Start-Process "C:\Program Files\Docker\Docker\Docker Desktop.exe"
```

### 2. Verificar que Docker está funcionando

```powershell
# Debe mostrar información sin errores
docker info

# Debe mostrar la versión
docker --version
```

### 3. Ejecutar el Build

Una vez que Docker esté funcionando correctamente:

**Opción A: Usar el script automático**
```powershell
.\docker-run.ps1
```
Selecciona la opción 1 (Build y Run)

**Opción B: Comandos manuales**
```powershell
# Build de la imagen
docker compose build

# Ejecutar el contenedor
docker compose up -d

# Ver logs
docker compose logs -f
```

### 4. Acceder a la Aplicación

Abre tu navegador en: **http://localhost:8501**

---

## Si el Problema Persiste

### Reinstalar Docker Desktop

1. Desinstala Docker Desktop desde Panel de Control
2. Descarga la última versión desde: https://www.docker.com/products/docker-desktop
3. Instala Docker Desktop
4. Reinicia tu computadora
5. Abre Docker Desktop
6. Vuelve a intentar el build

### Verificar Configuración de WSL2 (Windows)

```powershell
# Verificar WSL2
wsl --list --verbose

# Debe mostrar "VERSION 2"
# Si muestra VERSION 1, actualiza:
wsl --set-default-version 2
```

### Contacto

Si sigues teniendo problemas, reporta el issue en:
https://github.com/DSArevalo4/ETLsports/issues

Incluye:
- Sistema operativo y versión
- Versión de Docker Desktop
- Logs completos del error
