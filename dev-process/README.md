1. **Infrastructure Setup Module**

   - Setting up KTH SSH server
   - Configuration for port 8022 (group number)
   - ngrok setup and configuration
   - GitHub webhook configuration
   - Auto-pulling mechanism setup

   ```bash
   # Example auto-pull script
   while true; do
     git fetch origin
     git reset --hard origin/main
     sleep 10  # Check every 10 seconds
   done
   ```

2. **Core Server Module**

   - FastAPI server implementation
   - Webhook endpoint handling
   - Security (webhook secret verification)
   - Branch detection
   - Basic logging

   ```python
   # server.py structure
   from fastapi import FastAPI, Request
   import hmac
   import logging

   app = FastAPI()
   logging.basicConfig(level=logging.INFO)
   ```

3. **Syntax Check Module (P1)**

   - Python syntax validation
   - Code style checking (pylint)
   - Branch-specific checking
   - Test suite for syntax checker

   ```python
   # syntax_checker.py structure
   import pylint
   import ast

   class SyntaxChecker:
       def check_file(self, file_path: str) -> bool
       def check_directory(self, dir_path: str) -> dict
       def generate_report(self) -> str
   ```

4. **Test Runner Module (P2)**

   - pytest execution
   - Test result collection
   - Coverage reporting
   - Test suite for test runner

   ```python
   # test_runner.py structure
   import pytest
   import coverage

   class TestRunner:
       def run_tests(self, test_path: str) -> dict
       def generate_report(self) -> str
       def get_coverage(self) -> float
   ```

5. **Notification Module (P3)**

   - GitHub Status API integration
   - Status update handling
   - Test suite for notifications

   ```python
   # notifier.py structure
   import requests

   class GitHubNotifier:
       def set_status(self, commit_sha: str, state: str, description: str)
       def get_status(self, commit_sha: str) -> dict
   ```

6. **Configuration Module**

   - Environment variable management
   - Configuration file handling
   - Secrets management

   ```python
   # config.py structure
   from dotenv import load_dotenv
   import os

   class Config:
       def __init__(self)
       def get_github_token(self) -> str
       def get_webhook_secret(self) -> str
   ```

7. **Deployment Process**

```bash
# 1. SSH setup
ssh username@student-shell.sys.kth.se

# 2. directory setup
mkdir ci_server
cd ci_server

# 3. environment setup
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 4. configuration
cp .env.example .env
# Edit .env with your tokens/secrets

# 5. start services
./start_services.sh  # Combines steps below
```

8. **Project structure**

```
project/
├── .env.example              # Template for environment variables
├── requirements.txt          # Python dependencies
├── start_services.sh         # Service starter script
├── src/
│   ├── server.py            # Main Flask application
│   ├── config.py            # Configuration management
│   ├── syntax_checker.py    # P1 implementation
│   ├── test_runner.py       # P2 implementation
│   ├── notifier.py          # P3 implementation
│   └── utils/
│       ├── github_utils.py  # GitHub API helpers
│       └── logging_utils.py # Logging helpers
├── tests/
│   ├── test_syntax.py       # Tests for P1
│   ├── test_runner.py       # Tests for P2
│   └── test_notifier.py     # Tests for P3
└── scripts/
    ├── deploy.sh            # Deployment script
    ├── auto_pull.sh         # Auto-update script
    └── start_ngrok.sh       # ngrok starter script
```

**Development Process outline**:

1. Set up infrastructure
2. Implement core server & deploy to kth server
3. Add syntax checking (P1)
4. Add test running (P2)
5. Add notifications (P3)
6. Add auto-update mechanism
7. Complete documentation
8. Test deployment
