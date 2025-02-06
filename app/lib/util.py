# Utility functions
import os
import subprocess
from routers.check_syntax import REPO_PATH

def compile_project(repo_url):
    # os.system(f"git clone {repo_url} {REPO_PATH} || (cd {REPO_PATH} && git pull)")  # Clone or pull latest

    # # Install dependencies
    # pip_install = subprocess.run(["pip", "install", "-r", f"{REPO_PATH}/requirements.txt"], capture_output=True, text=True)

    # # Check syntax
    # syntax_check = subprocess.run(["python", "-m", "py_compile", f"{REPO_PATH}/*.py"], capture_output=True, text=True)

    # # Linting
    # lint_check = subprocess.run(["flake8", REPO_PATH], capture_output=True, text=True)

    # if pip_install.returncode == 0 and syntax_check.returncode == 0 and lint_check.returncode == 0:
    #     return True, "Compilation Successful"
    
    return False
