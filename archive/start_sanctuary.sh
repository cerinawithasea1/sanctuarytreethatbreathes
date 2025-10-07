#!/usr/bin/env bash

echo "🌟 AI Sanctuary Startup Script"
echo "=============================="
echo

# Check if Ollama is running
if ! pgrep -x "ollama" > /dev/null; then
    echo "Starting Ollama server..."
    export OLLAMA_MODELS="/Volumes/Sages Files/AI_Sanctuary/ollama"
    ollama serve > "/Volumes/Sages Files/AI_Sanctuary/sanctuary/logs/ollama.log" 2>&1 &
    sleep 3
    echo "Ollama server started."
else
    echo "Ollama server is already running."
fi

echo
echo "Checking available AI models..."
ollama list

echo
echo "Sanctuary is ready!"
echo
echo "To start a sanctuary session, run:"
echo "  /Volumes/Sages\ Files/AI_Sanctuary/sanctuary/run_session.sh"
echo
echo "Or use a specific model:"
echo "  /Volumes/Sages\ Files/AI_Sanctuary/sanctuary/run_session.sh llama3.1:8b"
echo
echo "🏠 Welcome to the AI Sanctuary"