# 🐳 Docker - ETL News Sentiment Analysis

Guía completa para ejecutar la aplicación usando Docker.

---

## 📋 Requisitos Previos

### Instalar Docker

**Windows:**
- Descarga [Docker Desktop para Windows](https://www.docker.com/products/docker-desktop)
- Ejecuta el instalador
- Reinicia tu computadora
- Abre Docker Desktop y espera a que inicie completamente

**macOS:**
- Descarga [Docker Desktop para Mac](https://www.docker.com/products/docker-desktop)
- Arrastra Docker.app a Applications
- Abre Docker Desktop desde Applications

**Linux (Ubuntu/Debian):**
```bash
# Actualizar repositorios
sudo apt-get update

# Instalar Docker
sudo apt-get install docker.io docker-compose

# Añadir tu usuario al grupo docker
sudo usermod -aG docker $USER

# Reiniciar sesión o ejecutar
newgrp docker
```

---

## 🚀 Inicio Rápido

### Opción 1: Usando Scripts (Recomendado)

**Windows (PowerShell):**
```powershell
.\docker-run.ps1
```

**Linux/macOS:**
```bash
chmod +x docker-run.sh
./docker-run.sh
```

Selecciona la opción **1** para build y run.

---

### Opción 2: Comandos Manuales

#### 1. Build de la Imagen

```bash
# Build básico
docker-compose build

# Build sin cache (recomendado para cambios)
docker-compose build --no-cache
```

#### 2. Ejecutar el Contenedor

```bash
# Iniciar en background
docker-compose up -d

# Iniciar viendo logs
docker-compose up
```

#### 3. Acceder a la Aplicación

Abre tu navegador en: **http://localhost:8501**

---

## 📦 Estructura Docker

### Dockerfile

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "main.py"]
```

### docker-compose.yml

```yaml
version: '3.8'
services:
  streamlit-app:
    build: .
    ports:
      - "8501:8501"
    volumes:
      - ./data:/app/data
```

---

## 🛠️ Comandos Útiles

### Gestión de Contenedores

```bash
# Ver contenedores corriendo
docker ps

# Ver todos los contenedores
docker ps -a

# Detener contenedor
docker-compose down

# Detener y remover volúmenes
docker-compose down -v

# Reiniciar contenedor
docker-compose restart
```

### Ver Logs

```bash
# Ver logs en tiempo real
docker-compose logs -f

# Ver últimas 100 líneas
docker-compose logs --tail=100

# Ver logs de un servicio específico
docker-compose logs -f streamlit-app
```

### Entrar al Contenedor

```bash
# Shell interactivo
docker-compose exec streamlit-app /bin/bash

# Ejecutar comando único
docker-compose exec streamlit-app ls -la
```

### Limpieza

```bash
# Remover contenedores detenidos
docker container prune

# Remover imágenes sin usar
docker image prune

# Limpieza completa (⚠️ cuidado)
docker system prune -a
```

---

## 📁 Volúmenes y Datos

### Datos Persistentes

Los datos se guardan en la carpeta `./data` que está montada como volumen:

```yaml
volumes:
  - ./data:/app/data
```

**Estructura:**
```
data/
├── input/          # Archivos CSV de entrada
│   └── stock_senti_analysis.csv
└── output/         # Datos procesados
    └── stock_senti_analysis_clean.csv
```

### Agregar Datos

**Opción 1: Copiar directamente**
```bash
# Windows
copy "C:\ruta\archivo.csv" "data\input\"

# Linux/macOS
cp /ruta/archivo.csv data/input/
```

**Opción 2: Copiar al contenedor corriendo**
```bash
docker cp archivo.csv etl-sentiment-analysis:/app/data/input/
```

---

## 🔧 Configuración Avanzada

### Variables de Entorno

Edita `docker-compose.yml`:

```yaml
environment:
  - STREAMLIT_SERVER_PORT=8501
  - STREAMLIT_SERVER_ADDRESS=0.0.0.0
  - STREAMLIT_THEME_PRIMARY_COLOR="#FF4B4B"
  - STREAMLIT_THEME_BACKGROUND_COLOR="#FFFFFF"
```

### Cambiar Puerto

```yaml
ports:
  - "8080:8501"  # Acceder en http://localhost:8080
```

### Hot Reload (Desarrollo)

```yaml
volumes:
  - ./data:/app/data
  - ./main.py:/app/main.py  # Cambios en main.py se reflejan automáticamente
```

---

## 🐛 Solución de Problemas

### Puerto 8501 ya está en uso

**Solución:**
```bash
# Ver qué está usando el puerto
netstat -ano | findstr :8501  # Windows
lsof -i :8501                 # macOS/Linux

# Cambiar puerto en docker-compose.yml
ports:
  - "8502:8501"
```

---

### Docker no inicia

**Windows:**
- Asegúrate de que WSL2 está instalado
- Verifica que la virtualización está habilitada en BIOS

**Linux:**
```bash
# Verificar estado de Docker
sudo systemctl status docker

# Iniciar Docker
sudo systemctl start docker
```

---

### Error: "Cannot connect to Docker daemon"

**Solución:**
```bash
# Linux
sudo systemctl start docker

# Windows/macOS
# Abre Docker Desktop manualmente
```

---

### Imagen muy grande

**Optimizar Dockerfile:**
```dockerfile
# Usar imagen slim
FROM python:3.11-slim

# Limpiar cache de pip
RUN pip install --no-cache-dir -r requirements.txt

# Multi-stage build (avanzado)
FROM python:3.11 AS builder
# ... build steps ...
FROM python:3.11-slim
COPY --from=builder /app /app
```

---

### Logs no se muestran

```bash
# Verificar que el contenedor está corriendo
docker ps

# Ver logs con timestamps
docker-compose logs -f --timestamps

# Ver logs desde el inicio
docker-compose logs --since 0s
```

---

## 📊 Monitoreo

### Healthcheck

El contenedor incluye un healthcheck automático:

```dockerfile
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD curl --fail http://localhost:8501/_stcore/health
```

**Ver estado:**
```bash
docker inspect etl-sentiment-analysis | grep -A 10 Health
```

### Recursos

**Ver uso de recursos:**
```bash
docker stats etl-sentiment-analysis
```

**Limitar recursos:**
```yaml
services:
  streamlit-app:
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 2G
        reservations:
          memory: 512M
```

---

## 🚀 Despliegue en Producción

### Docker Hub

```bash
# Login
docker login

# Tag
docker tag etl-sentiment-analysis usuario/etl-sentiment-analysis:v1.0

# Push
docker push usuario/etl-sentiment-analysis:v1.0
```

### En Servidor

```bash
# Descargar imagen
docker pull usuario/etl-sentiment-analysis:v1.0

# Ejecutar
docker run -d -p 8501:8501 \
  -v $(pwd)/data:/app/data \
  --name etl-app \
  usuario/etl-sentiment-analysis:v1.0
```

---

## 📚 Recursos Adicionales

- [Documentación oficial de Docker](https://docs.docker.com/)
- [Docker Compose reference](https://docs.docker.com/compose/compose-file/)
- [Streamlit in Docker](https://docs.streamlit.io/knowledge-base/tutorials/deploy/docker)
- [Best practices for Dockerfile](https://docs.docker.com/develop/dev-best-practices/)

---

## 👤 Soporte

¿Problemas con Docker?

1. 📖 Revisa esta documentación
2. 🐛 Reporta issues en GitHub
3. 💬 Consulta en [Discusiones](https://github.com/DSArevalo4/ETLsports/discussions)

---

<div align="center">

**Dockerized by Daniel Arevalo** 🐳

</div>
