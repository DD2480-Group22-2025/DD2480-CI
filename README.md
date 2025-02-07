# DD2480-CI

## Setup

### Prerequisites

1. Python 3.8 or higher
2. ngrok account and authtoken (get it from https://dashboard.ngrok.com/get-started/your-authtoken)

### Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/DD2480-CI.git
cd DD2480-CI
```

2. Configure ngrok:

```bash
# Install ngrok if not already installed
mkdir -p ~/bin
cd ~/bin
wget https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.tgz
tar xvzf ngrok-v3-stable-linux-amd64.tgz
rm ngrok-v3-stable-linux-amd64.tgz

# Add your authtoken (get it from ngrok dashboard)
~/bin/ngrok config add-authtoken YOUR_AUTH_TOKEN
```

3. Start the services:

```bash
./start_services.sh
```

4. Stop the services:

```bash
./stop_services.sh
```

## Usage

The CI server will be available at:

- Local FastAPI server: http://localhost:8022
- Public ngrok URL: Check the output of start_services.sh or the ngrok dashboard

## FastAPI server

```bash
fastapi dev app/main.py
```
