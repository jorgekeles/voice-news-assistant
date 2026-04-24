#!/usr/bin/env python3
"""
Voice News Assistant - CLI Version
Script para ejecutar el asistente desde línea de comandos
"""

import sys
import asyncio
from utils import NewsAggregator, NewsAnalyzer, TextToSpeech, VoiceActivation
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def print_header(text):
    """Print formatted header"""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60 + "\n")

def print_articles(articles):
    """Print articles in a formatted way"""
    for i, article in enumerate(articles, 1):
        print(f"\n{i}. [{article['source']}] {article['title']}")
        if article.get('summary'):
            print(f"   {article['summary'][:150]}...")
        if article.get('link'):
            print(f"   🔗 {article['link']}")

async def main():
    """Main CLI function"""
    print_header("📢 VOICE NEWS ASSISTANT - CLI VERSION")
    
    # Check API key
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("❌ Error: GEMINI_API_KEY no está configurada")
        print("Por favor, configura tu .env file con tu clave de API")
        sys.exit(1)
    
    print("✅ API Key configurada")
    print("🌐 Idioma: " + os.getenv("LANGUAGE", "es"))
    
    # Step 1: Fetch news
    print_header("PASO 1: CARGANDO NOTICIAS")
    try:
        aggregator = NewsAggregator()
        articles = aggregator.fetch_feeds()
        print(f"✅ {len(articles)} artículos cargados\n")
        print_articles(articles[:10])
    except Exception as e:
        print(f"❌ Error al cargar noticias: {e}")
        sys.exit(1)
    
    # Step 2: Generate summary
    print_header("PASO 2: GENERANDO RESUMEN CON IA")
    language = os.getenv("LANGUAGE", "es")
    try:
        analyzer = NewsAnalyzer(language=language)
        summary = analyzer.summarize_articles(articles, max_articles=5)
        print("📝 RESUMEN GENERADO:\n")
        print(summary)
    except Exception as e:
        print(f"❌ Error al generar resumen: {e}")
        sys.exit(1)
    
    # Step 3: Synthesize speech
    print_header("PASO 3: GENERANDO AUDIO")
    tts_provider = os.getenv("TTS_PROVIDER", "edge-tts")
    print(f"Usando proveedor: {tts_provider}")
    
    try:
        tts = TextToSpeech(provider=tts_provider, language=language)
        audio_data = await tts.synthesize(summary)
        
        if audio_data:
            # Save audio file
            filename = f"news_summary_{int(__import__('time').time())}.mp3"
            with open(filename, 'wb') as f:
                f.write(audio_data)
            print(f"✅ Audio generado: {filename}")
            print(f"💾 Tamaño: {len(audio_data) / 1024 / 1024:.2f} MB")
            
            # Try to play audio
            try:
                import subprocess
                print("\n🎧 Reproduciendo audio...")
                subprocess.run(['open', filename], check=False)  # macOS
                # Para Linux: subprocess.run(['xdg-open', filename])
                # Para Windows: subprocess.run(['start', filename])
            except Exception as e:
                print(f"⚠️ No se pudo reproducir automáticamente: {e}")
                print(f"Abre manualmente: {filename}")
        else:
            print("❌ Error al generar audio")
            sys.exit(1)
            
    except Exception as e:
        print(f"❌ Error en síntesis de voz: {e}")
        sys.exit(1)
    
    print_header("✅ PROCESO COMPLETADO")
    print("El resumen de noticias ha sido generado y procesado exitosamente")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n⚠️ Proceso interrumpido por el usuario")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        sys.exit(1)
