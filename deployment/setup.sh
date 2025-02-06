#!/bin/bash

# Install ngrok if not present
if [ ! -f ~/bin/ngrok ]; then
    mkdir -p ~/bin
    cd ~/bin
    wget https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.tgz
    tar xvzf ngrok-v3-stable-linux-amd64.tgz
    rm ngrok-v3-stable-linux-amd64.tgz
fi

# Create systemd user directory
mkdir -p ~/.config/systemd/user/

# Copy service files
cp deployment/ci-server.service ~/.config/systemd/user/
cp deployment/ngrok.service ~/.config/systemd/user/

# Reload and start services
systemctl --user daemon-reload
systemctl --user enable ci-server.service ngrok.service
systemctl --user start ci-server.service ngrok.service

echo "Services installed and started. Check status with:"
echo "systemctl --user status ci-server.service"
echo "systemctl --user status ngrok.service"