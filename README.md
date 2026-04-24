# 📢 Voice News Assistant

Un MVP de asistente de noticias por voz en Python que integra feeds RSS, IA de Gemini, reconocimiento de voz y síntesis de texto a voz.

## 🎯 Características

- **📡 Agregación de Noticias**: Consume múltiples feeds RSS configurados en `sources.json`
- **🤖 Resúmenes con IA**: Utiliza Google Gemini para generar resúmenes con tono de locutor profesional
- **🎤 Activación por Voz**: Detecta el comando "noticias" mediante micrófono (SpeechRecognition)
- **🔊 Síntesis de Voz**: Convierte resúmenes a audio usando edge-tts o gTTS
- **🌐 Interfaz Web**: Streamlit para una experiencia interactiva y moderna
- **🌍 Multiidioma**: Soporte para español, inglés, francés y alemán

## 📋 Requisitos Previos

- Python 3.9+
- pip (gestor de paquetes de Python)
- Una clave de API de Google Gemini (obtén la tuya en [Google AI Studio](https://makersuite.google.com/app/apikey))
- Micrófono (opcional, para activación por voz)

## 🚀 Instalación

### 1. Clonar el repositorio

```bash
cd /Users/jorgekeles/Documents/news-assitance
```

### 2. Crear un entorno virtual

```bash
python3 -m venv venv
source venv/bin/activate  # En macOS/Linux
# o
venv\Scripts\activate  # En Windows
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

**Nota**: Si usas macOS y tienes problemas con PyAudio, prueba:
```bash
brew install portaudio
pip install pyaudio
```

### 4. Configurar variables de entorno

```bash
cp .env.example .env
```

Abre `.env` y configura tu clave de API de Gemini:
```
GEMINI_API_KEY=tu_clave_aqui
LANGUAGE=es
TTS_PROVIDER=edge-tts
VOICE=es-ES-AlvaroNeural
```

## 📱 Uso

### Ejecutar la aplicación

```bash
streamlit run app.py
```

La aplicación se abrirá en `http://localhost:8501`

### Workflow Típico

1. **Configurar la clave de Gemini** en la barra lateral
2. **Seleccionar preferencias**: idioma, proveedor de voz, número de artículos
3. **Hacer clic en "Cargar Noticias"** para obtener los feeds RSS
4. **Hacer clic en "Generar Resumen"** para crear un resumen con IA
5. **Hacer clic en "Generar Audio"** para sintetizar el resumen
6. **Reproducir el audio** en la interfaz web

### Activación por Voz (Opcional)

1. Habilita "Activación por voz" en los controles
2. Haz clic en "Escuchar comando"
3. Di "noticias" en el micrófono
4. El sistema cargará y resumirá las noticias automáticamente

## 📁 Estructura del Proyecto

```
voice-news-assistant/
├── app.py              # Aplicación principal Streamlit
├── utils.py            # Clases y utilidades (NewsAggregator, NewsAnalyzer, etc.)
├── sources.json        # Configuración de feeds RSS
├── requirements.txt    # Dependencias del proyecto
├── .env.example        # Template de variables de entorno
├── .gitignore          # Archivos a ignorar en Git
└── README.md           # Este archivo
```

## 🔧 Configuración de Feeds RSS

Edita `sources.json` para añadir o modificar fuentes de noticias:

```json
{
  "sources": [
    {
      "name": "CNN Top Stories",
      "url": "http://rss.cnn.com/rss2.0/cnn_topstories.rss",
      "enabled": true
    }
  ]
}
```

## 🎯 Componentes Principales

### NewsAggregator
Obtiene y procesa feeds RSS de múltiples fuentes:
```python
aggregator = NewsAggregator()
articles = aggregator.fetch_feeds()
```

### NewsAnalyzer
Genera resúmenes con tono de locutor usando Gemini:
```python
analyzer = NewsAnalyzer(language="es")
summary = analyzer.summarize_articles(articles)
```

### TextToSpeech
Convierte texto a audio usando edge-tts o gTTS:
```python
tts = TextToSpeech(provider="edge-tts", language="es")
audio = await tts.synthesize(text)
```

### VoiceActivation
Detecta comandos de voz:
```python
voice = VoiceActivation()
if voice.listen_for_activation():
    # Procesar noticias
```

## 🌐 Voces Disponibles (edge-tts)

- **Español**: `es-ES-AlvaroNeural`, `es-MX-JorgeNeural`
- **Inglés**: `en-US-AriaNeural`, `en-GB-RyanNeural`
- **Francés**: `fr-FR-DeniseNeural`
- Y muchas más...

## 🐛 Solución de Problemas

### Error: "ModuleNotFoundError: No module named 'google.generativeai'"
```bash
pip install google-generativeai
```

### Error: "No module named 'pyaudio'"
En macOS:
```bash
brew install portaudio
pip install pyaudio
```

### El micrófono no funciona
- Verifica que tienes un micrófono conectado
- En macOS, asegúrate de que Streamlit está autorizado para acceder al micrófono
- Prueba: `python3 -c "import speech_recognition as sr; print(sr.Microphone.list_microphone_indexes())"`

### Errores al conectar con feeds RSS
- Verifica que las URLs en `sources.json` son válidas
- Algunos feeds pueden estar bloqueados por derechos de autor
- Intenta con feeds públicos conocidos

## 🔐 Seguridad

- **Nunca** hagas commit de `.env` con tu API key
- La clave de API se envía directamente a Google, no se almacena localmente
- Considera usar una clave de API con restricciones en Google Cloud Console

## 📚 Dependencias Principales

| Paquete | Versión | Propósito |
|---------|---------|----------|
| streamlit | 1.35.0 | Framework web |
| feedparser | 6.0.10 | Parsing de RSS |
| google-generativeai | 0.3.0 | API de Gemini |
| SpeechRecognition | 3.10.0 | Reconocimiento de voz |
| edge-tts | 6.1.1 | Síntesis TTS |
| gTTS | 2.4.0 | Google TTS (alternativa) |

## 🚀 Próximas Mejoras

- [ ] Caché de noticias para reducir latencia
- [ ] Categorización automática de noticias
- [ ] Filtrado por palabras clave
- [ ] Base de datos para historial de noticias
- [ ] Notificaciones de noticias urgentes
- [ ] Interfaz móvil
- [ ] Multi-usuario
- [ ] Analytics y estadísticas

## 📝 Licencia

Proyecto educativo de código abierto.

## 👨‍💻 Autor

Desarrollado como MVP para demostrar integración de:
- Streamlit
- Gemini AI
- RSS Feeds
- Speech Recognition
- Text-to-Speech

---

**¿Preguntas o sugerencias?** Abre un issue o contribuye al proyecto.
