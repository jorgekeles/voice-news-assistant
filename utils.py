import feedparser
import json
import os
import io
from datetime import datetime
from typing import List, Dict, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

try:
    from google import genai as google_genai
except ImportError:
    google_genai = None

try:
    import google.generativeai as legacy_genai
except ImportError:
    legacy_genai = None

class NewsAggregator:
    """Handles RSS feed fetching and processing"""
    
    def __init__(self, sources_file: str = "sources.json"):
        self.sources_file = sources_file
        self.config = self._load_sources()
        self.sources = self.config.get("sources", [])
        self.demo_mode = self.config.get("demo_mode", False)
        self.demo_articles = self.config.get("demo_articles", [])
    
    def _load_sources(self) -> Dict:
        """Load RSS sources from JSON file"""
        if not os.path.exists(self.sources_file):
            return {}
        
        with open(self.sources_file, 'r', encoding='utf-8') as f:
            return json.load(f)

    def _get_demo_articles(self) -> List[Dict]:
        """Return configured demo articles or the built-in fallback set."""
        if self.demo_articles:
            return self.demo_articles

        return [
            {
                "source": "TechNews",
                "title": "Inteligencia Artificial revoluciona el desarrollo de software",
                "summary": "Los últimos avances en IA están transformando cómo los desarrolladores escriben código, mejorando significativamente la productividad y la calidad del software.",
                "link": "https://ejemplo.com/ai-software",
                "published": "2026-04-24T10:00:00Z"
            },
            {
                "source": "Ciencia",
                "title": "Descubrimiento revolucionario en física cuántica",
                "summary": "Científicos logran avance importante en computación cuántica que podría cambiar la industria tecnológica en los próximos años.",
                "link": "https://ejemplo.com/quantum",
                "published": "2026-04-24T09:30:00Z"
            },
            {
                "source": "Tecnología",
                "title": "Nuevas regulaciones sobre privacidad de datos en Europa",
                "summary": "La Unión Europea implementa nuevas normas para proteger datos personales de ciudadanos en plataformas digitales.",
                "link": "https://ejemplo.com/privacy",
                "published": "2026-04-24T08:45:00Z"
            },
            {
                "source": "Ciberseguridad",
                "title": "Ataque cibernético masivo afecta a múltiples empresas",
                "summary": "Expertos alertan sobre vulnerabilidad crítica en software ampliamente utilizado que fue explotada en ataque coordinado.",
                "link": "https://ejemplo.com/cyber",
                "published": "2026-04-24T07:20:00Z"
            },
            {
                "source": "Startup",
                "title": "Nueva startup de IA recauda 50 millones en inversión",
                "summary": "Empresa emergente de inteligencia artificial obtiene financiación de inversores reconocidos para expandir plataforma.",
                "link": "https://ejemplo.com/startup",
                "published": "2026-04-24T06:00:00Z"
            }
        ]
    
    def fetch_feeds(self) -> List[Dict]:
        """Fetch all enabled RSS feeds"""
        if self.demo_mode:
            return sorted(self._get_demo_articles(), key=lambda x: x.get("source", ""))[:20]

        all_articles = []
        
        # User-Agent to avoid blocking
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        for source in self.sources:
            if not source.get("enabled", True):
                continue
            
            try:
                # Parse with request headers
                feed = feedparser.parse(
                    source["url"],
                    request_headers=headers
                )
                
                if not feed.entries:
                    print(f"⚠️ {source['name']} returned no entries")
                    continue
                
                for entry in feed.entries[:5]:  # Get top 5 from each source
                    article = {
                        "source": source.get("name", "Unknown"),
                        "title": entry.get("title", "Sin título"),
                        "summary": entry.get("summary", entry.get("description", "")),
                        "link": entry.get("link", ""),
                        "published": entry.get("published", ""),
                    }
                    all_articles.append(article)
            
            except Exception as e:
                print(f"⚠️ Error fetching from {source['name']}: {str(e)}")
        
        # If no articles found, use demo articles
        if not all_articles:
            print("📢 No articles from feeds, using demo articles...")
            all_articles = self._get_demo_articles()
        
        # Sort by source and limit to top articles
        return sorted(all_articles, key=lambda x: x.get("source", ""))[:20]


class NewsAnalyzer:
    """Handles AI processing of news using Gemini API"""
    
    def __init__(self, language: str = "es", api_key: Optional[str] = None):
        self.language = language
        self.api_key = os.getenv("GEMINI_API_KEY", "") if api_key is None else api_key
        self.client = None
        self.model = None
        self.uses_legacy_sdk = False

        if google_genai and self.api_key:
            self.client = google_genai.Client(api_key=self.api_key)
            self.model_name = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
        elif legacy_genai and self.api_key:
            legacy_genai.configure(api_key=self.api_key)
            self.model_name = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
            self.model = legacy_genai.GenerativeModel(self.model_name)
            self.uses_legacy_sdk = True
        else:
            self.model_name = ""

    def _build_fallback_summary(self, selected_articles: List[Dict]) -> str:
        """Create a readable local fallback summary without AI."""
        lines = ["Resumen de noticias principales:", ""]
        for i, article in enumerate(selected_articles, 1):
            lines.append(f"{i}. {article['title']}")
            if article.get("summary"):
                lines.append(f"   {article['summary'][:150]}...")
            lines.append("")
        return "\n".join(lines).strip()

    def _generate_with_gemini(self, prompt: str) -> str:
        """Generate content using the best available Gemini SDK."""
        if self.client:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
            )
            return response.text

        if self.model:
            response = self.model.generate_content(prompt)
            return response.text

        raise RuntimeError("Gemini API no está configurada")
    
    def summarize_articles(self, articles: List[Dict], max_articles: int = 5) -> str:
        """Generate a news summary with broadcaster tone using Gemini"""
        if not articles:
            return "No hay noticias disponibles en este momento."
        
        # Select top articles
        selected_articles = articles[:max_articles]
        
        # Prepare article text
        articles_text = "\n".join([
            f"- {article['title']} (Fuente: {article['source']})"
            for article in selected_articles
        ])
        
        # Create prompt for Gemini
        prompt = f"""Eres un locutor de noticias profesional. Tu tarea es generar un resumen de noticias 
        con un tono profesional, amigable y dinámico, como si estuvieras leyendo noticias en la radio.
        
        Noticias a resumir:
        {articles_text}
        
        Genera un resumen coherente y fluido en {self.language} que:
        1. Sea entretenido y profesional
        2. Cubra los puntos principales de las noticias
        3. Tenga un tono cálido y accesible
        4. Dure aproximadamente 2-3 minutos cuando se lea en voz alta
        5. Incluya transiciones naturales entre temas
        
        Comienza directamente con el resumen, sin introducción adicional."""
        
        try:
            return self._generate_with_gemini(prompt)
        except Exception as e:
            # Fallback: Create a simple summary without Gemini
            print(f"⚠️ Gemini API no disponible: {str(e)[:50]}")
            print("📢 Usando resumen automático sin IA...")
            return self._build_fallback_summary(selected_articles)
    
    def generate_headline_summary(self, articles: List[Dict], count: int = 5) -> str:
        """Generate a quick headline summary"""
        if not articles:
            return "No hay titulares disponibles."
        
        headlines = "\n".join([
            f"{i+1}. {article['title']}"
            for i, article in enumerate(articles[:count])
        ])
        
        prompt = f"""Como locutor de radio profesional, presenta estos titulares de manera 
        dinámica y concisa en {self.language}:
        
        {headlines}
        
        Presenta los titulares de forma fluida y entretenida, como si estuvieras leyendo 
        en la radio. Sé breve y directo."""
        
        try:
            return self._generate_with_gemini(prompt)
        except Exception as e:
            print(f"⚠️ Gemini API no disponible: {str(e)[:50]}")
            return "\n".join([
                f"{i + 1}. {article['title']}"
                for i, article in enumerate(articles[:count])
            ])


class TextToSpeech:
    """Handles text-to-speech conversion"""
    
    def __init__(self, provider: str = "edge-tts", language: str = "es"):
        self.provider = provider
        self.language = language
        self.voice = os.getenv("VOICE") or self._default_voice_for_language()

    def _default_voice_for_language(self) -> str:
        """Choose a sensible default voice for the selected language."""
        default_voices = {
            "es": "es-ES-AlvaroNeural",
            "en": "en-US-AriaNeural",
            "fr": "fr-FR-DeniseNeural",
            "de": "de-DE-KatjaNeural",
        }
        return default_voices.get(self.language[:2], "es-ES-AlvaroNeural")
    
    async def synthesize_gtts(self, text: str) -> Optional[bytes]:
        """Generate speech using gTTS"""
        try:
            from gtts import gTTS
            
            tts = gTTS(text=text, lang=self.language[:2], slow=False)
            audio_buffer = io.BytesIO()
            tts.write_to_fp(audio_buffer)
            audio_buffer.seek(0)
            return audio_buffer.getvalue()
        except Exception as e:
            print(f"Error with gTTS: {str(e)}")
            return None
    
    async def synthesize_edge_tts(self, text: str) -> Optional[bytes]:
        """Generate speech using edge-tts"""
        try:
            import edge_tts
            
            audio_buffer = io.BytesIO()
            
            async def tts_task():
                async for chunk in edge_tts.Communicate(text, voice=self.voice).stream():
                    if chunk["type"] == "audio":
                        audio_buffer.write(chunk["data"])
            
            await tts_task()
            audio_buffer.seek(0)
            return audio_buffer.getvalue()
        except Exception as e:
            print(f"Error with edge-tts: {str(e)}")
            return None
    
    async def synthesize(self, text: str) -> Optional[bytes]:
        """Generate speech using configured provider"""
        # Try edge-tts first, fallback to gTTS if it fails
        if self.provider == "edge-tts":
            result = await self.synthesize_edge_tts(text)
            if result:
                return result
            print("⚠️ edge-tts falló, intentando con gTTS...")
        
        return await self.synthesize_gtts(text)


class VoiceActivation:
    """Handles voice recognition and activation"""
    
    def __init__(self, activation_phrase: str = "noticias"):
        self.activation_phrase = activation_phrase.lower()
    
    def listen_for_activation(self, timeout: int = 5) -> bool:
        """Listen for activation phrase using microphone"""
        try:
            import speech_recognition as sr
            
            recognizer = sr.Recognizer()
            
            with sr.Microphone() as source:
                print(f"Escuchando... (esperando '{self.activation_phrase}')")
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                
                try:
                    audio = recognizer.listen(source, timeout=timeout)
                    text = recognizer.recognize_google(audio, language="es-ES")
                    print(f"Detectado: {text}")
                    
                    return self.activation_phrase in text.lower()
                
                except sr.UnknownValueError:
                    print("No se entendieron las palabras claras")
                    return False
                except sr.RequestError as e:
                    print(f"Error del servicio de reconocimiento: {e}")
                    return False
        
        except ImportError:
            print("SpeechRecognition no está disponible")
            return False
        except Exception as e:
            print(f"Error en reconocimiento de voz: {e}")
            return False


def get_timestamp() -> str:
    """Get current timestamp"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
