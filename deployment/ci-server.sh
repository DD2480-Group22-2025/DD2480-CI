[Unit]
Description=CI Server

[Service]
ExecStart=/home/sasoder/github/DD2480-CI/venv/bin/python -m uvicorn main:app --host 0.0.0.0 --port 8022
WorkingDirectory=/home/sasoder/github/DD2480-CI
Restart=always

[Install]
WantedBy=default.target