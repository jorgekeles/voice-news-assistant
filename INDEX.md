# 📋 Índice del Proyecto - Voice News Assistant

## 📂 Estructura de Archivos

```
voice-news-assistant/
│
├── 📄 app.py                      # Aplicación principal Streamlit (10KB)
├── 📄 utils.py                    # Módulo con clases y utilidades (8KB)
├── 📄 run_locally.py             # Script CLI alternativo (4KB)
│
├── 📄 sources.json               # Configuración de feeds RSS
├── 📄 requirements.txt           # Dependencias Python
├── 📄 .env.example               # Template de variables de entorno
│
├── 🐳 Dockerfile                 # Configuración Docker
├── 🐳 docker-compose.yml         # Docker Compose para despliegue
│
├── 📚 README.md                  # Documentación completa
├── 🚀 QUICK_START.md             # Guía de inicio rápido
├── ☁️ DEPLOYMENT.md              # Guías de despliegue
├── 📋 INDEX.md                   # Este archivo
│
├── 🔧 quick_start.sh             # Script de instalación automática (macOS/Linux)
├── ✅ test_components.py         # Script de pruebas de componentes
├── 🎯 .streamlit/config.toml     # Configuración de Streamlit
│
├── 🔺 .pre-commit-config.yaml    # Configuración de pre-commit hooks
├── 🚫 .gitignore                 # Archivos a ignorar en Git
└── .git/                         # Repositorio Git
```

## 🎯 Archivos Principales Explicados

### **app.py** (Aplicación Principal)
- **Propósito**: Interfaz web interactiva con Streamlit
- **Características**:
  - Interfaz sidebar con controles
  - Carga y visualización de artículos
  - Generación de resúmenes con IA
  - Síntesis de voz integrada
  - Reproducción de audio en navegador
  - Operación asíncrona para TTS
- **Dependencias**: streamlit, utils

### **utils.py** (Módulo de Utilidades)
Contiene 4 clases principales:

1. **NewsAggregator**
   - Carga feeds RSS de `sources.json`
   - Parsea múltiples fuentes
   - Manejo de errores por feed

2. **NewsAnalyzer**
   - Integra API de Gemini
   - Genera resúmenes con tono de locutor
   - Soporta múltiples idiomas
   - Procesamiento de headlines

3. **TextToSpeech**
   - Soporta edge-tts y gTTS
   - Devuelve audio en bytes
   - Operaciones asíncronas

4. **VoiceActivation**
   - Escucha comandos de voz
   - Detecta palabra de activación
   - Usa SpeechRecognition

### **run_locally.py** (Versión CLI)
- Alternativa a Streamlit para terminal
- Flujo lineal: fetch → summarize → TTS
- Guarda archivos MP3
- Útil para automatización

### **sources.json** (Configuración de Feeds)
```json
{
  "sources": [
    {
      "name": "Nombre del feed",
      "url": "https://ejemplo.com/feed.xml",
      "enabled": true  // false para desactivar
    }
  ]
}
```

### **.env.example** (Plantilla de Configuración)
Variables de entorno necesarias:
- `GEMINI_API_KEY`: Tu clave de API de Google
- `LANGUAGE`: Idioma (es, en, fr, de)
- `TTS_PROVIDER`: edge-tts o gtts
- `VOICE`: Selección de voz específica
- `AUDIO_DURATION_SECONDS`: Duración de escucha

## 🔧 Scripts Auxiliares

### **quick_start.sh** ⚙️
Instalación automática completa:
```bash
chmod +x quick_start.sh
./quick_start.sh
```
- Crea entorno virtual
- Instala dependencias
- Configura portaudio (macOS)
- Crea archivo .env

### **test_components.py** ✅
Verifica que todos los componentes funcionen:
```bash
python3 test_components.py
```
Prueba: feedparser, Gemini, SpeechRecognition, TTS, Streamlit

## 📚 Documentación

### **README.md** 📖
- Descripción general del proyecto
- Características principales
- Información de instalación
- Uso básico
- Solución de problemas
- Dependencias principales

### **QUICK_START.md** 🚀
- Guía de 5 pasos para empezar rápido
- Configuración de APIkey
- Primer uso
- Problemas comunes
- Personalización básica

### **DEPLOYMENT.md** ☁️
Guías completas de despliegue:
- Docker Compose
- Heroku, Railway, Google Cloud Run
- VPS Linux (DigitalOcean, Linode, etc.)
- Nginx como reverse proxy
- SSL/HTTPS con Let's Encrypt
- Render.com, AWS, DigitalOcean App
- Seguridad en producción

## 🐳 Docker

### **Dockerfile**
- Base: Python 3.11 slim
- Instala dependencias del sistema
- Configura Streamlit
- Health checks incluidos

### **docker-compose.yml**
- Servicio Streamlit
- Variables de entorno configurables
- Volúmenes para desarrollo
- Puerto 8501 expuesto

## 🔧 Configuración

### **.streamlit/config.toml**
- Personalización de tema (colores primarios)
- Configuración de cliente
- Logging
- Configuración de servidor
- Desactivar recolección de estadísticas

### **.pre-commit-config.yaml**
Hooks automáticos para commits:
- Trailing whitespace
- Black (formateador)
- Flake8 (linter)
- isort (organizador de imports)

### **.gitignore**
Archivos ignorados:
- .env (variables de entorno)
- __pycache__/ (bytecode Python)
- venv/ (entorno virtual)
- Archivos de audio (*.wav, *.mp3)
- .streamlit/ (caché)
- Archivos del SO (.DS_Store)

## 🚀 Flujo de Uso

### Opción 1: Interfaz Web (Recomendado)
```
1. Terminal: streamlit run app.py
2. Navegador: http://localhost:8501
3. Sidebar: Configura API key
4. Botón "Cargar Noticias"
5. Botón "Generar Resumen"
6. Botón "Generar Audio"
7. Play para escuchar
```

### Opción 2: Terminal
```
1. Terminal: python3 run_locally.py
2. Sistema carga feeds
3. IA genera resumen
4. Audio se sintetiza
5. Se abre automáticamente (o se guarda)
```

### Opción 3: Activación por Voz
```
1. Interfaz: Habilita "Activación por voz"
2. Dice "noticias" al micrófono
3. Sistema auto-carga y resume
4. Audio se reproduce
```

## 🔑 Variables de Entorno Importantes

| Variable | Valor | Obligatorio |
|----------|-------|-----------|
| `GEMINI_API_KEY` | Tu clave | ✅ Sí |
| `LANGUAGE` | es/en/fr/de | ❌ No (default: es) |
| `TTS_PROVIDER` | edge-tts/gtts | ❌ No (default: edge-tts) |
| `VOICE` | Código de voz | ❌ No |
| `AUDIO_DURATION_SECONDS` | 1-10 | ❌ No |

## 📦 Dependencias Principales

| Paquete | Versión | Uso |
|---------|---------|-----|
| streamlit | 1.35.0 | Framework web |
| feedparser | 6.0.10 | Parsing RSS |
| google-generativeai | 0.3.0 | Gemini API |
| SpeechRecognition | 3.10.0 | Voz → Texto |
| edge-tts | 6.1.1 | Texto → Voz (principal) |
| gTTS | 2.4.0 | Texto → Voz (alternativa) |
| python-dotenv | 1.0.0 | Variables .env |
| pyaudio | 0.2.13 | I/O de audio |

## 🎯 Casos de Uso

1. **Para Uso Personal**
   - Instala localmente
   - Configura feeds favoritos
   - Escucha resúmenes diarios

2. **Para Demostración**
   - Usa Quick Start
   - Muestra en navegador
   - Impresiona con IA + Voz

3. **Para Producción**
   - Despliega con Docker
   - Usa Nginx reverse proxy
   - Monitorea con uptime tools

4. **Para Desarrollo**
   - Modifica utils.py
   - Añade nuevas fuentes
   - Experimenta con prompts

## 🔄 Próximos Pasos Recomendados

1. ✅ Ejecuta `quick_start.sh`
2. ✅ Configura tu API key de Gemini
3. ✅ Ejecuta `test_components.py`
4. ✅ Inicia con `streamlit run app.py`
5. ✅ Personaliza `sources.json`
6. ✅ Experimenta con diferentes idiomas
7. ✅ Considera desplegar en la nube

## 📞 Soporte

- **Instalación**: Ver QUICK_START.md
- **Problemas**: Ver sección troubleshooting en README.md
- **Despliegue**: Ver DEPLOYMENT.md
- **Desarrollo**: Ver comentarios en código fuente

---

**Última actualización**: 24 de abril de 2026
**Versión MVP**: 1.0
**Estado**: Listo para uso local y despliegue
