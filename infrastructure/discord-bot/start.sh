#!/bin/bash
# LILA Lab Discord Bot - Quick Start Script

echo "=== LILA Lab Discord Bot ==="
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 not found"
    echo "Please install Python 3.10+"
    exit 1
fi

# Check .env
if [ ! -f .env ]; then
    echo "Error: .env file not found"
    echo "Copy .env.example to .env and fill in your bot token"
    echo ""
    echo "cp .env.example .env"
    echo ""
    exit 1
fi

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt -q

# Start bot
echo "Starting LILA Lab Bot..."
echo "Press Ctrl+C to stop"
echo ""
python3 bot.py
