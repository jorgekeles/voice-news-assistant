# 🚀 Deployment Guide

Guías para desplegar Voice News Assistant en diferentes entornos.

## 📦 Docker (Recomendado)

### Requisitos
- Docker y Docker Compose instalados
- Tu clave de API de Gemini

### Deployment Con Docker Compose

```bash
# Crear archivo .env
cp .env.example .env
# Editar .env y añadir tu GEMINI_API_KEY

# Iniciar el contenedor
docker-compose up -d

# Ver logs
docker-compose logs -f

# Acceder a la aplicación
# Abre http://localhost:8501
```

### Deployment Manual con Docker

```bash
# Construir imagen
docker build -t voice-news-assistant .

# Ejecutar contenedor
docker run -p 8501:8501 \
  -e GEMINI_API_KEY=tu_clave_aqui \
  -e LANGUAGE=es \
  -e TTS_PROVIDER=edge-tts \
  voice-news-assistant
```

## ☁️ Despliegues en la Nube

### Heroku

```bash
# Login a Heroku
heroku login

# Crear app
heroku create tu-app-name

# Establecer variables de entorno
heroku config:set GEMINI_API_KEY=tu_clave_aqui

# Desplegar
git push heroku main
```

**Nota**: Heroku necesita buildpack personalizado para Python.

### Railway.app

```bash
# Conectar tu repositorio de GitHub a Railway
# Railway detectará automáticamente que es una app Python
# Configurar variables de entorno en el dashboard
# Railway desplegará automáticamente cada push a main
```

### Google Cloud Run

```bash
# Autenticarse
gcloud auth login

# Desplegar
gcloud run deploy voice-news-assistant \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars=GEMINI_API_KEY=tu_clave_aqui
```

### AWS Lambda + API Gateway

No recomendado para Streamlit. Usar EC2 o Elastic Beanstalk en su lugar.

### DigitalOcean App Platform

```bash
# Conectar repositorio de GitHub
# DigitalOcean detectará app.py y configurará automáticamente
# Establecer variables de entorno en settings
# Desplegar automáticamente
```

## 🖥️ Linux VPS (DigitalOcean, Linode, etc.)

### Instalación Inicial

```bash
# SSH a tu servidor
ssh root@tu_servidor

# Actualizar sistema
apt update && apt upgrade -y

# Instalar dependencias
apt install -y python3.11 python3-pip python3-venv \
    portaudio19-dev ffmpeg git

# Clonar repositorio
git clone https://github.com/jorgekeles/voice-news-assistant.git
cd voice-news-assistant

# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar .env
cp .env.example .env
nano .env  # Editar y añadir GEMINI_API_KEY
```

### Ejecutar Con Systemd

Crear archivo `/etc/systemd/system/voice-news.service`:

```ini
[Unit]
Description=Voice News Assistant
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/home/user/voice-news-assistant
ExecStart=/home/user/voice-news-assistant/venv/bin/streamlit run app.py \
    --server.port=8501 \
    --server.address=0.0.0.0
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Activar servicio:
```bash
sudo systemctl daemon-reload
sudo systemctl enable voice-news
sudo systemctl start voice-news
sudo systemctl status voice-news
```

### Con Nginx como Reverse Proxy

Crear `/etc/nginx/sites-available/voice-news`:

```nginx
upstream streamlit {
    server 127.0.0.1:8501;
}

server {
    listen 80;
    server_name tu_dominio.com;

    client_max_body_size 50M;

    location / {
        proxy_pass http://streamlit;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Activar:
```bash
sudo ln -s /etc/nginx/sites-available/voice-news /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### SSL/HTTPS con Let's Encrypt

```bash
# Instalar Certbot
sudo apt install certbot python3-certbot-nginx

# Obtener certificado
sudo certbot --nginx -d tu_dominio.com
```

## 🍎 macOS (Local/Dev)

```bash
# Con Homebrew
brew install python@3.11
brew install portaudio

# Seguir instrucciones de "Quick Start"
./quick_start.sh
streamlit run app.py
```

## 📱 Render.com

1. Conectar repositorio a Render
2. Crear nuevo Web Service
3. Configurar:
   - Build command: `pip install -r requirements.txt`
   - Start command: `streamlit run app.py --server.port=10000`
4. Añadir variables de entorno
5. Desplegar

## 🔐 Seguridad en Producción

1. **HTTPS/SSL**: Siempre usar certificados SSL válidos
2. **API Keys**: Usar gestores de secretos, nunca en código
3. **Rate Limiting**: Implementar límites en feed fetching
4. **Authentication**: Considerar protección por contraseña
5. **Firewall**: Restringir acceso si es necesario
6. **Logs**: Monitorear logs regularmente
7. **Updates**: Mantener dependencias actualizadas

## 📊 Monitoreo

### Uptime Monitoring
- Usar Pingdom, StatusCake, o Uptime Robot
- Configurar alertas si el servicio cae

### Log Management
- Usar Sentry para error tracking
- Considerar LogRocket para sesiones de usuario

### Performance
- Monitorear tiempo de respuesta
- Trackear uso de CPU y memoria
- Optimizar queries a APIs

## 🆘 Troubleshooting

### "Port already in use"
```bash
# Cambiar puerto en Dockerfile o .streamlit/config.toml
# O matar proceso existente
lsof -i :8501
kill -9 <PID>
```

### "Connection refused"
- Verificar firewall
- Revisar configuración de Nginx/proxy
- Chequear logs: `docker-compose logs`

###  "API Key invalid"
- Verificar variable de entorno está configurada
- Revisar que la clave sea correcta
- Verificar que API esté activa en Google Cloud

## 📚 Referencias

- [Streamlit Deployment](https://docs.streamlit.io/knowledge-base/deploy/)
- [Docker Documentation](https://docs.docker.com/)
- [Nginx Reverse Proxy](https://docs.nginx.com/)
- [Systemd Services](https://www.freedesktop.org/software/systemd/man/systemd.service.html)
