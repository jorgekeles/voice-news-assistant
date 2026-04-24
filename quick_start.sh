#!/bin/bash
# Quick Start Script for Voice News Assistant

echo "📢 Voice News Assistant - Quick Start"
echo "===================================="
echo ""

# Check Python version
python_version=$(python3 --version 2>&1 | cut -d' ' -f2 | cut -d'.' -f1,2)
echo "✅ Python version: $python_version"

# Create virtual environment
echo ""
echo "🔧 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "✅ Activating virtual environment..."
source venv/bin/activate

# Install pyaudio on macOS
if [[ "$OSTYPE" == "darwin"* ]]; then
    echo "🍎 Detected macOS - Installing portaudio for audio support..."
    if command -v brew &> /dev/null; then
        brew install portaudio
    else
        echo "⚠️ Homebrew not found. Install portaudio manually."
    fi
fi

# Install dependencies
echo ""
echo "📦 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Copy .env file
if [ ! -f .env ]; then
    echo ""
    echo "🔐 Creating .env configuration file..."
    cp .env.example .env
    echo "⚠️ Important: Edit .env and add your Gemini API key"
    echo "   You can get it from: https://makersuite.google.com/app/apikey"
fi

# Create directories if needed
mkdir -p data

echo ""
echo "✅ Installation complete!"
echo ""
echo "🚀 To start the application, run:"
echo "   source venv/bin/activate"
echo "   streamlit run app.py"
echo ""
echo "📖 For more information, see README.md"
