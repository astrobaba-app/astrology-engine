@echo off
REM Astro Engine Startup Script for Windows

echo Starting Astro Engine...

REM Check if virtual environment exists
if not exist ".venv" (
    echo Virtual environment not found. Creating...
    uv venv
)

REM Activate virtual environment
call .venv\Scripts\activate

REM Check if dependencies are installed
python -c "import fastapi" 2>nul
if errorlevel 1 (
    echo Installing dependencies...
    uv pip install -e .
)

REM Check if .env exists
if not exist ".env" (
    echo Creating .env from .env.example...
    copy .env.example .env
    echo Please edit .env with your configuration
)

REM Check if ephemeris data exists
if not exist "ephemeris_data\seas_18.se1" (
    echo Warning: Swiss Ephemeris data not found!
    echo Please download ephemeris files from:
    echo https://www.astro.com/ftp/swisseph/ephe/
    echo Required files: seas_18.se1, semo_18.se1, sepl_18.se1
    echo.
)

REM Start the server
echo Starting Uvicorn server...
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
