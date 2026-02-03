@echo off
echo ========================================
echo Honey-Pot API - Quick Start
echo ========================================
echo.

REM Check if .env exists
if not exist .env (
    echo Creating .env file from template...
    copy .env.example .env
    echo.
    echo IMPORTANT: Edit .env file and set your API keys!
    echo - API_KEY: Your secure API key
    echo - OPENAI_API_KEY: Your OpenAI API key
    echo.
    pause
)

REM Check if virtual environment exists
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
    echo.
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt
echo.

REM Start the server
echo Starting Honey-Pot API server...
echo Server will be available at http://localhost:8000
echo Press Ctrl+C to stop the server
echo.
python run.py
