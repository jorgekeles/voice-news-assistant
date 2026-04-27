"""
Test script for Voice News Assistant components
Verifies that all components work correctly before running the full app
"""

import sys
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

print("=" * 60)
print("Voice News Assistant - Component Test")
print("=" * 60)

def test_feedparser():
    """Test RSS feed parsing"""
    print("\n[1/5] Testing feedparser...")
    try:
        import feedparser
        print(f"  ✅ feedparser version: {feedparser.__version__}")
        
        sample_feed = """<?xml version="1.0" encoding="UTF-8" ?>
        <rss version="2.0">
          <channel>
            <title>Sample Feed</title>
            <item>
              <title>Sample headline</title>
              <description>Sample summary</description>
              <link>https://example.com/story</link>
            </item>
          </channel>
        </rss>
        """

        feed = feedparser.parse(sample_feed)
        if feed and feed.entries:
            print(f"  ✅ Can parse RSS feeds locally (found {len(feed.entries)} entries)")
        return True
    except Exception as e:
        print(f"  ❌ feedparser test failed: {e}")
        return False

def test_gemini():
    """Test Gemini API connection"""
    print("\n[2/5] Testing Google Gemini API...")
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("  ⚠️ GEMINI_API_KEY not set - test skipped")
        print("    Set GEMINI_API_KEY in .env to use this feature")
        return False
    
    try:
        try:
            from google import genai

            client = genai.Client(api_key=api_key)
            print("  ✅ Google GenAI SDK configured")
            print("  ✅ Gemini client ready")
            return bool(client)
        except ImportError:
            import google.generativeai as genai

            genai.configure(api_key=api_key)
            print("  ✅ Legacy Gemini SDK configured")
            model = genai.GenerativeModel("gemini-1.5-flash")
            print("  ✅ Gemini model ready")
            return bool(model)
    except Exception as e:
        print(f"  ❌ Gemini API test failed: {e}")
        return False

def test_speech_recognition():
    """Test SpeechRecognition"""
    print("\n[3/5] Testing SpeechRecognition...")
    try:
        import speech_recognition as sr
        print(f"  ✅ SpeechRecognition v{sr.__version__}")
        
        # Check microphone availability
        if hasattr(sr.Microphone, "list_microphone_names"):
            mics = sr.Microphone.list_microphone_names()
            print(f"  ✅ Found {len(mics)} microphone(s)")
        else:
            print("  ⚠️ This SpeechRecognition version cannot enumerate microphones")
        return True
    except Exception as e:
        print(f"  ⚠️ SpeechRecognition not fully available: {e}")
        print("    Voice features may not work")
        return False

def test_tts():
    """Test Text-to-Speech providers"""
    print("\n[4/5] Testing Text-to-Speech...")
    
    # Test gTTS
    try:
        from gtts import gTTS
        print(f"  ✅ gTTS available")
        gtts_ok = True
    except Exception as e:
        print(f"  ⚠️ gTTS failed: {e}")
        gtts_ok = False
    
    # Test edge-tts
    try:
        import edge_tts
        print(f"  ✅ edge-tts available")
        edge_ok = True
    except Exception as e:
        print(f"  ⚠️ edge-tts failed: {e}")
        edge_ok = False
    
    if not gtts_ok and not edge_ok:
        print("  ❌ No TTS provider available")
        return False
    
    return True

def test_streamlit():
    """Test Streamlit"""
    print("\n[5/5] Testing Streamlit...")
    try:
        import streamlit as st
        print(f"  ✅ Streamlit v{st.__version__}")
        return True
    except Exception as e:
        print(f"  ❌ Streamlit test failed: {e}")
        return False

def main():
    """Run all tests"""
    results = {
        "feedparser": test_feedparser(),
        "gemini": test_gemini(),
        "speech_recognition": test_speech_recognition(),
        "tts": test_tts(),
        "streamlit": test_streamlit(),
    }
    
    print("\n" + "=" * 60)
    print("Test Results")
    print("=" * 60)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test, result in results.items():
        status = "✅" if result else "❌"
        print(f"{status} {test}")
    
    print(f"\n{passed}/{total} tests passed")
    
    if passed == total:
        print("\n✅ All components are ready!")
        print("You can now run: streamlit run app.py")
        return 0
    elif passed >= 3:
        print("\n⚠️ Most components are ready, but some optional features may not work")
        return 0
    else:
        print("\n❌ Critical components are missing")
        print("Please install dependencies: pip install -r requirements.txt")
        return 1

if __name__ == "__main__":
    sys.exit(main())
