#!/bin/bash

echo "========================================"
echo "Honey-Pot API - Quick Start"
echo "========================================"
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo ""
    echo "IMPORTANT: Edit .env file and set your API keys!"
    echo "- API_KEY: Your secure API key"
    echo "- OPENAI_API_KEY: Your OpenAI API key"
    echo ""
    read -p "Press enter to continue after editing .env..."
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo ""
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt
echo ""

# Start the server
echo "Starting Honey-Pot API server..."
echo "Server will be available at http://localhost:8000"
echo "Press Ctrl+C to stop the server"
echo ""
python run.py
