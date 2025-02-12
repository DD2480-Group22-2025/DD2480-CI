#!/bin/bash

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Create necessary directories
echo "Creating config directories..."
mkdir -p ~/.config/ngrok/

# Update ngrok configuration while preserving authtoken
echo "Updating ngrok configuration..."
if [ -f ~/.config/ngrok/ngrok.yml ]; then
    # Extract existing authtoken
    AUTH_TOKEN=$(grep "authtoken:" ~/.config/ngrok/ngrok.yml | cut -d' ' -f2)
    # Copy new config
    cp -v "${SCRIPT_DIR}/deployment/ngrok.yml" ~/.config/ngrok/ngrok.yml
    # Restore authtoken if it exists
    if [ ! -z "$AUTH_TOKEN" ]; then
        echo "authtoken: $AUTH_TOKEN" >> ~/.config/ngrok/ngrok.yml
    fi
else
    cp -v "${SCRIPT_DIR}/deployment/ngrok.yml" ~/.config/ngrok/ngrok.yml
fi

# Kill any existing processes
echo "Cleaning up any existing processes..."
pkill -f "uvicorn app.main:app" || true
pkill -f "ngrok http" || true

# Setup virtual environment if it doesn't exist or is broken
if [ ! -f "venv/bin/activate" ]; then
    echo "Creating new virtual environment..."
    rm -rf venv
    python3 -m venv venv
    chmod -R u+w venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "Installing requirements..."
pip install fastapi uvicorn

# Start the FastAPI server in the background
echo "Starting FastAPI server..."
venv/bin/python -m uvicorn app.main:app --host 0.0.0.0 --port 8022 > fastapi.log 2>&1 &
FASTAPI_PID=$!

# Wait for FastAPI to start
echo "Waiting for FastAPI to start..."
sleep 5

# Start ngrok in the background
echo "Starting ngrok..."
~/bin/ngrok http 8022 --config ~/.config/ngrok/ngrok.yml > ngrok.log 2>&1 &
NGROK_PID=$!

# Wait for ngrok to start
echo "Waiting for ngrok to start..."
sleep 5

# Show process status
echo -e "\nProcess Status:"
echo "==============="
echo "FastAPI PID: $FASTAPI_PID"
echo "Ngrok PID: $NGROK_PID"

# Show ngrok URL
echo -e "\nNgrok tunnel info:"
echo "================"
curl -s http://localhost:4022/api/tunnels | grep -o '"public_url":"[^"]*' | cut -d'"' -f4

echo -e "\nLogs are available in:"
echo "FastAPI: ${SCRIPT_DIR}/fastapi.log"
echo "Ngrok: ${SCRIPT_DIR}/ngrok.log"

# Save PIDs for later cleanup
echo "$FASTAPI_PID" > .fastapi.pid
echo "$NGROK_PID" > .ngrok.pid

# Deactivate virtual environment
deactivate
