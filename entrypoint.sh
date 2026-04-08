#!/bin/bash
set -e

if [ -z "$GEMINI_API_KEY" ]; then
    echo ""
    echo "┌─────────────────────────────────────────────────────┐"
    echo "│  Gemini API Key (optional — for AI Doubt Explainer) │"
    echo "│  Press Enter to skip and run without AI.            │"
    echo "└─────────────────────────────────────────────────────┘"
    read -r -p "  Enter key: " user_key
    if [ -n "$user_key" ]; then
        export GEMINI_API_KEY="$user_key"
        echo "  AI feature enabled."
    else
        echo "  Skipped. AI feature will be unavailable."
    fi
    echo ""
fi

echo "Running migrations..."
python manage.py migrate --noinput

echo "Starting development server..."
exec python manage.py runserver 0.0.0.0:8000
