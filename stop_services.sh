#!/bin/bash

echo "Stopping services..."

# Kill FastAPI if running
if [ -f .fastapi.pid ]; then
    FASTAPI_PID=$(cat .fastapi.pid)
    kill $FASTAPI_PID 2>/dev/null || true
    rm .fastapi.pid
fi

# Kill ngrok if running
if [ -f .ngrok.pid ]; then
    NGROK_PID=$(cat .ngrok.pid)
    kill $NGROK_PID 2>/dev/null || true
    rm .ngrok.pid
fi

# Additional cleanup
pkill -f "uvicorn app.main:app" || true
pkill -f "ngrok http" || true

echo "Services stopped." 