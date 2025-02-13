# DD2480-CI

## Project Description

This project implements a Continuous Integration (CI) server that supports CI features such as compilation, syntax checking, testing, result notifications, and build history.

https://2580-2001-6b0-1-1041-e3a-6d35-666c-2185.ngrok-free.app/

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
chmod +x start_services.sh
./start_services.sh
```

4. Stop the services:

```bash
chmod +x stop_services.sh
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

## Project structure

```
DD2480-CI/
├── requirements.txt           # Dependencies
├── start_services.sh          # Service starter script
├── stop_services.sh           # Service stop script
├── report.md                  # report
├── README.md                  # readme file
├── LICENSE                    # MIT license
├── app/
│   ├── __init__.py            # init file
│   ├── mail.py                # main endpoint
│   |── lib/
│   |    ├── database_api.py   # querying the database
│   |    └── util.py           # utility functions
|   └── routers/
│         ├── builds.py        # build pages
│         └── notify.py        # router
├── tests/
│   ├── test_syntax.py         # Tests for P1
│   ├── test_runner.py         # Tests for P2
│   ├── test_notifier.py       # Tests for P3
│   └── example_files.py       # Tests for P1
|── scripts/
|    ├── create_database.sh    # create database script
|    ├── deploy.sh             # Deployment script
|    ├── run_tests.sh          # Auto-test script
|    └── start_ngrok.sh        # ngrok starter script
├── database/
│    └── database_tables.sql   # initial table setup
└── deployment/
     ├── ci-server.service     # ci setup file
     ├── ngrok.service         # ngrok setup file
     └── ngrok.yml             # YAML file for ngrok

```
