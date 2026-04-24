import streamlit as st
import asyncio
import os
from datetime import datetime
from dotenv import load_dotenv
from utils import NewsAggregator, NewsAnalyzer, TextToSpeech, VoiceActivation

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Voice News Assistant",
    page_icon="📢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-title {
        text-align: center;
        color: #1f77b4;
        font-size: 3em;
        margin-bottom: 10px;
    }
    .subtitle {
        text-align: center;
        color: #666;
        font-size: 1.2em;
        margin-bottom: 30px;
    }
    .news-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 15px;
        border-left: 5px solid #1f77b4;
    }
    .source-badge {
        display: inline-block;
        background-color: #1f77b4;
        color: white;
        padding: 5px 10px;
        border-radius: 20px;
        font-size: 0.8em;
        margin-bottom: 10px;
    }
    .status-box {
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 15px;
    }
    .status-success {
        background-color: #d4edda;
        color: #155724;
        border: 1px solid #c3e6cb;
    }
    .status-info {
        background-color: #d1ecf1;
        color: #0c5460;
        border: 1px solid #bee5eb;
    }
    .status-error {
        background-color: #f8d7da;
        color: #721c24;
        border: 1px solid #f5c6cb;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'news_articles' not in st.session_state:
    st.session_state.news_articles = []
if 'summary' not in st.session_state:
    st.session_state.summary = ""
if 'audio_data' not in st.session_state:
    st.session_state.audio_data = None

# Title
st.markdown('<h1 class="main-title">📢 Voice News Assistant</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Tu asistente de noticias por voz impulsado por IA</p>', unsafe_allow_html=True)

# Sidebar configuration
with st.sidebar:
    st.header("⚙️ Configuración")
    
    # API Key configuration
    api_key = st.text_input(
        "🔑 Gemini API Key",
        value=os.getenv("GEMINI_API_KEY", ""),
        type="password",
        help="Tu clave de API de Google Gemini"
    )
    
    if api_key and api_key != os.getenv("GEMINI_API_KEY", ""):
        os.environ["GEMINI_API_KEY"] = api_key
        st.success("✅ Clave API configurada")
    
    # Language preferences
    language = st.selectbox(
        "🌐 Idioma",
        ["es", "en", "fr", "de"],
        index=0,
        help="Idioma para resúmenes y síntesis de voz"
    )
    
    # TTS Provider selection
    tts_provider = st.radio(
        "🔊 Proveedor de Síntesis de Voz",
        ["edge-tts", "gtts"],
        help="Elige el proveedor de texto a voz"
    )
    
    # Voice selection for edge-tts
    if tts_provider == "edge-tts":
        voice_options = {
            "es-ES-AlvaroNeural": "Álvaro (Español - España)",
            "es-MX-JorgeNeural": "Jorge (Español - México)",
            "en-US-AriaNeural": "Aria (Inglés - USA)",
            "en-GB-RyanNeural": "Ryan (Inglés - UK)",
            "fr-FR-DeniseNeural": "Denise (Francés)",
        }
        voice = st.selectbox(
            "🎙️ Voz",
            list(voice_options.keys()),
            format_func=lambda x: voice_options[x],
            help="Selecciona la voz para la síntesis de voz"
        )
        os.environ["VOICE"] = voice
    
    # Number of articles to summarize
    num_articles = st.slider(
        "📰 Artículos a resumir",
        1, 10, 5,
        help="Número de artículos a incluir en el resumen"
    )
    
    st.divider()
    
    # Information
    st.subheader("ℹ️ Información")
    st.info(
        """
        **Voice News Assistant** es un MVP que:
        - 📡 Obtiene noticias de múltiples feeds RSS
        - 🤖 Genera resúmenes con IA (Gemini)
        - 🎙️ Convierte texto a voz automáticamente
        - 🎧 Reproduce el resumen en la interfaz web
        
        **Configuración requerida:**
        1. Ingresa tu clave de API de Gemini
        2. Haz clic en "Cargar Noticias"
        3. El resumen se generará automáticamente
        """
    )

# Main content area
col1, col2 = st.columns([2, 1])

with col2:
    st.subheader("🎮 Controles")
    
    # Buttons for main actions
    col_btn1, col_btn2 = st.columns(2)
    
    with col_btn1:
        fetch_button = st.button("📡 Cargar Noticias", use_container_width=True)
    
    with col_btn2:
        summarize_button = st.button("✨ Generar Resumen", use_container_width=True)
    
    st.divider()
    
    # Voice activation option
    if st.checkbox("🎤 Activación por voz"):
        st.info("Nota: Requiere micrófono y SpeechRecognition configurado")
        if st.button("🔊 Escuchar comando", use_container_width=True):
            with st.spinner("Escuchando..."):
                voice = VoiceActivation()
                if voice.listen_for_activation():
                    st.success("✅ Comando 'noticias' detectado!")
                    fetch_button = True
                else:
                    st.warning("⚠️ Comando no detectado")

with col1:
    st.subheader("📰 Noticias")

# Process fetch button
if fetch_button:
    with st.spinner("Cargando noticias..."):
        try:
            aggregator = NewsAggregator()
            st.session_state.news_articles = aggregator.fetch_feeds()
            
            if st.session_state.news_articles:
                st.markdown(
                    f'<div class="status-box status-success">✅ Se cargaron {len(st.session_state.news_articles)} artículos</div>',
                    unsafe_allow_html=True
                )
                st.session_state.summary = ""  # Reset summary
            else:
                st.markdown(
                    '<div class="status-box status-error">❌ No se pudieron cargar noticias</div>',
                    unsafe_allow_html=True
                )
        except Exception as e:
            st.markdown(
                f'<div class="status-box status-error">❌ Error: {str(e)}</div>',
                unsafe_allow_html=True
            )

# Display loaded articles
if st.session_state.news_articles:
    with st.expander(f"📋 Artículos cargados ({len(st.session_state.news_articles)})", expanded=False):
        for i, article in enumerate(st.session_state.news_articles, 1):
            st.markdown(f"<div class='news-card'>", unsafe_allow_html=True)
            st.markdown(f"<span class='source-badge'>{article['source']}</span>", unsafe_allow_html=True)
            st.write(f"**{article['title']}**")
            if article.get('summary'):
                st.write(f"_{article['summary'][:200]}..._")
            if article.get('link'):
                st.write(f"[Leer más →]({article['link']})")
            st.markdown("</div>", unsafe_allow_html=True)

# Process summarize button
if summarize_button:
    if not st.session_state.news_articles:
        st.warning("⚠️ Por favor, carga las noticias primero")
    elif not os.getenv("GEMINI_API_KEY"):
        st.error("❌ Por favor, configura tu clave de API de Gemini en la barra lateral")
    else:
        with st.spinner("Generando resumen con IA..."):
            try:
                analyzer = NewsAnalyzer(language=language)
                st.session_state.summary = analyzer.summarize_articles(
                    st.session_state.news_articles,
                    max_articles=num_articles
                )
                st.markdown(
                    '<div class="status-box status-success">✅ Resumen generado exitosamente</div>',
                    unsafe_allow_html=True
                )
            except Exception as e:
                st.markdown(
                    f'<div class="status-box status-error">❌ Error al generar resumen: {str(e)}</div>',
                    unsafe_allow_html=True
                )

# Display summary
if st.session_state.summary:
    st.divider()
    st.subheader("🗣️ Resumen Generado")
    st.write(st.session_state.summary)
    
    # TTS Controls
    st.divider()
    col_audio1, col_audio2 = st.columns([2, 1])
    
    with col_audio2:
        if st.button("🔊 Generar Audio", use_container_width=True):
            with st.spinner("Sintetizando voz..."):
                try:
                    tts = TextToSpeech(provider=tts_provider, language=language)
                    
                    # Run async function
                    async def generate_audio():
                        return await tts.synthesize(st.session_state.summary)
                    
                    audio_bytes = asyncio.run(generate_audio())
                    
                    if audio_bytes:
                        st.session_state.audio_data = audio_bytes
                        st.markdown(
                            '<div class="status-box status-success">✅ Audio generado</div>',
                            unsafe_allow_html=True
                        )
                    else:
                        st.markdown(
                            '<div class="status-box status-error">❌ Error al generar audio</div>',
                            unsafe_allow_html=True
                        )
                except Exception as e:
                    st.markdown(
                        f'<div class="status-box status-error">❌ Error: {str(e)}</div>',
                        unsafe_allow_html=True
                    )
    
    with col_audio1:
        if st.session_state.audio_data:
            st.audio(st.session_state.audio_data, format="audio/mp3")

# Footer
st.divider()
st.markdown("""
    <div style='text-align: center; color: #999; font-size: 0.9em; margin-top: 30px;'>
        <p>🤖 Voice News Assistant v1.0 | Powered by Streamlit, Gemini AI & Edge-TTS</p>
        <p>Made with ❤️ for news enthusiasts</p>
    </div>
""", unsafe_allow_html=True)
