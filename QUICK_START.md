# 🚀 Quick Start Guide

Para empezar con Voice News Assistant en 5 minutos.

## 1️⃣ Instalación Automática (Recomendado)

```bash
chmod +x quick_start.sh
./quick_start.sh
```

Este script:
- ✅ Crea un entorno virtual
- ✅ Instala todas las dependencias
- ✅ Crea el archivo `.env`
- ✅ En macOS, instala portaudio para audio

## 2️⃣ Obtener tu Clave de API de Gemini

1. Ve a [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Haz clic en "Create API Key"
3. Copia la clave generada

## 3️⃣ Configurar el Proyecto

```bash
# Edita .env con tu editor favorito
nano .env
# O abre con VS Code
code .env
```

Busca esta línea y añade tu clave:
```
GEMINI_API_KEY=tu_clave_aqui
```

## 4️⃣ Ejecutar la Aplicación

```bash
# Activar el entorno virtual (si no está activo)
source venv/bin/activate

# Iniciar Streamlit
streamlit run app.py
```

**Resultado**: Se abrirá `http://localhost:8501` automáticamente

## 5️⃣ Usar la Aplicación

### Desde la Interfaz Web (Recomendado)

1. La barra lateral se abrirá automáticamente
2. Pega tu API key en el primer campo
3. Haz clic en "📡 Cargar Noticias"
4. Espera a que carguen los artículos
5. Haz clic en "✨ Generar Resumen"
6. Haz clic en "🔊 Generar Audio"
7. ¡Presiona play para escuchar!

### Desde Terminal (Alternativo)

```bash
source venv/bin/activate
python3 run_locally.py
```

Esto cargará noticias, generará resumen y guardará un archivo `.mp3`

## ⚙️ Opciones de Configuración

En la barra lateral puedes:
- 🌐 Cambiar idioma (es, en, fr, de)
- 🔊 Elegir proveedor de voz (edge-tts o gTTS)
- 🎙️ Seleccionar voz específica
- 📰 Ajustar número de artículos

## 🎤 Activación por Voz (Opcional)

1. Marca "🎤 Activación por voz"
2. Haz clic en "🔊 Escuchar comando"
3. Di "noticias" en el micrófono
4. El sistema cargará y resumirá automáticamente

## 🆘 Problemas Comunes

### "ModuleNotFoundError: google.generativeai"
```bash
pip install google-generativeai
```

### "No module named pyaudio" (macOS)
```bash
brew install portaudio
pip install pyaudio
```

### El micrófono no funciona
```bash
# Verifica disponibilidad de micrófonos
python3 -c "import speech_recognition as sr; print(sr.Microphone.list_microphone_indexes())"
```

### Feeds RSS vacíos
Algunos feeds pueden estar bloqueados. Edita `sources.json` con URLs válidas.

## 📝 Personalización

### Añadir nuevas fuentes de noticias

Edita `sources.json`:
```json
{
  "sources": [
    {
      "name": "Mi Fuente Favorita",
      "url": "https://ejemplo.com/feed.xml",
      "enabled": true
    }
  ]
}
```

### Cambiar voces disponibles

En `.env`:
```
VOICE=es-ES-AlvaroNeural  # Español
# o
VOICE=en-US-AriaNeural    # Inglés
```

## 📚 Recursos

- [Documentación Streamlit](https://docs.streamlit.io/)
- [Google Gemini API Docs](https://ai.google.dev/)
- [FeedParser Documentation](https://pythonhosted.org/feedparser/)
- [SpeechRecognition Docs](https://github.com/Uberi/speech_recognition)

## 🎯 Próximos Pasos

Una vez funcionando correctamente:
1. Personaliza `sources.json` con tus fuentes favoritas
2. Ajusta el número de artículos y preferencias de idioma
3. Experimenta con diferentes voces y velocidades
4. ¡Disfruta tus noticias resumidas automáticamente!

---

**¿Necesitas ayuda?** Consulta README.md para documentación completa.
