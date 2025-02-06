#!/bin/bash

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Create necessary directories
echo "Creating config directories..."
mkdir -p ~/.config/systemd/user/
mkdir -p ~/.config/ngrok/

# Copy configuration files with absolute paths
echo "Copying configuration files..."
cp -v "${SCRIPT_DIR}/deployment/ngrok.yml" ~/.config/ngrok/
cp -v "${SCRIPT_DIR}/deployment/ci-server.service" ~/.config/systemd/user/
cp -v "${SCRIPT_DIR}/deployment/ngrok.service" ~/.config/systemd/user/

# Verify files exist
echo -e "\nVerifying files..."
echo "Checking ngrok config:"
ls -l ~/.config/ngrok/ngrok.yml
echo -e "\nChecking service files:"
ls -l ~/.config/systemd/user/ci-server.service
ls -l ~/.config/systemd/user/ngrok.service

# Reload systemd daemon
echo -e "\nReloading systemd daemon..."
systemctl --user daemon-reload

# Stop services if they're running
echo "Stopping any existing services..."
systemctl --user stop ci-server.service ngrok.service 2>/dev/null

# Start services in correct order
echo -e "\nStarting CI server..."
systemctl --user start ci-server.service
echo "Starting ngrok..."
systemctl --user start ngrok.service

# Enable services to start on boot
echo -e "\nEnabling services..."
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