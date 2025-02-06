#!/bin/bash

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Create necessary directories
mkdir -p ~/.config/systemd/user/
mkdir -p ~/.config/ngrok/

# Copy configuration files with absolute paths
cp "${SCRIPT_DIR}/deployment/ngrok.yml" ~/.config/ngrok/
cp "${SCRIPT_DIR}/deployment/ci-server.service" ~/.config/systemd/user/
cp "${SCRIPT_DIR}/deployment/ngrok.service" ~/.config/systemd/user/

# Reload systemd daemon
systemctl --user daemon-reload

# Stop services if they're running
systemctl --user stop ci-server.service ngrok.service 2>/dev/null

# Start services in correct order
echo "Starting CI server..."
systemctl --user start ci-server.service
echo "Starting ngrok..."
systemctl --user start ngrok.service

# Enable services to start on boot
systemctl --user enable ci-server.service
systemctl --user enable ngrok.service

# Show status
echo -e "\nService Status:"
echo "==============="
systemctl --user status ci-server.service --no-pager
echo -e "\n"
systemctl --user status ngrok.service --no-pager

# Show ngrok URL
echo -e "\nNgrok tunnel info (may take a few seconds to establish):"
echo "==============================================="
sleep 5
curl -s http://localhost:4022/api/tunnels | grep -o '"public_url":"[^"]*' | cut -d'"' -f4