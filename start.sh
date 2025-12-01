#!/bin/bash

# Astro Engine Startup Script

echo "Starting Astro Engine..."

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "Virtual environment not found. Creating..."
    uv venv
fi

# Activate virtual environment
source .venv/bin/activate

# Check if dependencies are installed
if ! python -c "import fastapi" 2>/dev/null; then
    echo "Installing dependencies..."
    uv pip install -e .
fi

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "Creating .env from .env.example..."
    cp .env.example .env
    echo "Please edit .env with your configuration"
fi

# Check if ephemeris data exists
if [ ! -f "ephemeris_data/seas_18.se1" ]; then
    echo "Warning: Swiss Ephemeris data not found!"
    echo "Please download ephemeris files from:"
    echo "https://www.astro.com/ftp/swisseph/ephe/"
    echo "Required files: seas_18.se1, semo_18.se1, sepl_18.se1"
    echo ""
fi

# Start the server
echo "Starting Uvicorn server..."
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
