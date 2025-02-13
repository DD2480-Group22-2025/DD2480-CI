import os
import subprocess
import shutil
import stat
import time
from github import Github, Auth 
from typing import Dict, Any
def run_tests(repo_path: str) -> Dict[str, Any]:
    """
    Run tests in the specified repository path.
    Returns a dictionary with test results.
    """
    try:
        # Store current directory
        original_dir = os.getcwd()
        
        # Change to repo directory
        os.chdir(repo_path)
        
        # Run tests and capture output
        result = subprocess.run(['pytest'], capture_output=True, text=True)
        
        # Change back to original directory
        os.chdir(original_dir)
        
        return {
            "success": result.returncode == 0,
            "output": result.stdout,
            "error": result.stderr,
            "return_code": result.returncode
        }
    except Exception as e:
        if os.getcwd() != original_dir:
            os.chdir(original_dir)
        return {
            "success": False,
            "output": "",
            "error": str(e),
            "return_code": -1
        }


def check_syntax(repo):
    if not os.path.exists(repo):
        print("File does not exist")
        return False
    try:
        # Find all Python files in the repository
        python_files = [os.path.join(root, file) 
                       for root, _, files in os.walk(repo)
                       for file in files if file.endswith('.py')]
        
        if not python_files:
            print("No Python files found to check")
            return True
            
        # Check all Python files in a single pylint call
        syntax = subprocess.run(["pylint"] + python_files + ["--errors-only"], 
                              capture_output=True, text=True)
        
        # Check both stdout and stderr for syntax errors
        output = syntax.stdout + syntax.stderr
        if "syntax-error" in output.lower():
            print("Syntax errors found")
            return False
        
        print("Syntax check passed with no errors.")
        return True
        
    except Exception as e:
        print("Error in syntax check:", e)
        return False

def clone_repo(repo_url, id, branch):
    if not repo_url.startswith("https://github.com"):
        print("Invalid GitHub repo URL")
        return False

    repo_name = f"{repo_url.split('/')[-1].split('.')[0]}-{id}"
    repo_path = f"./cloned_repo/{repo_name}"

    try:
        subprocess.run(["git", "clone", repo_url, repo_path], check=True)
        subprocess.run(["git", "-C", repo_path, "checkout", branch], check=True)
        subprocess.run(["git", "-C", repo_path, "pull"], check=True)
        print(f"GitHub repo cloned successfully to {repo_path}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error in cloning {repo_name}: {e}")
        return False

def update_commit_status(commit_sha: str, state: str, description: str, context: str = "CI Notification", target_url: str = "") -> dict:
    """
    Update the commit status on GitHub using PyGithub.

    Valid states:
      - "pending"
      - "success"
      - "failure"
      - "error"

    Requires:
      - CI_SERVER_AUTH_TOKEN
      - REPO_OWNER
      - REPO_NAME

    Returns GitHub API's raw response data.
    """
    VALID_STATES = {"pending", "success", "failure", "error"}

    if state not in VALID_STATES:
        raise ValueError(f"Invalid commit status state: {state}. Must be one of {VALID_STATES}")

    token = os.getenv("CI_SERVER_AUTH_TOKEN")
    repo_owner = os.getenv("REPO_OWNER")
    repo_name = os.getenv("REPO_NAME")

    if not token or not repo_owner or not repo_name:
        raise Exception("Missing GitHub configuration. Please check the environment variables.")

    try:
        # Create Github instance with new auth method and timeout
        auth = Auth.Token(token)
        g = Github(auth=auth, timeout=10)
        
        # Get repository with timeout
        repo = g.get_repo(f"{repo_owner}/{repo_name}")
        
        # Get commit with timeout
        commit = repo.get_commit(commit_sha)
        
        # Create the new status directly without cleaning up old ones
        status = commit.create_status(
            state=state,
            target_url=target_url,
            description=description,
            context=context
        )
        
        # Close the Github connection
        g.close()
        
        return status.raw_data
    except Exception as e:
        print(f"GitHub API Error: {str(e)}")
        # Return a dummy response to prevent blocking
        return {
            "state": state,
            "description": description,
            "context": context,
            "error": str(e)
        }
    
        
def delete_repo(repo_name):
    # delete the cloned repo
    repo_path = os.path.join("./cloned_repo", repo_name)
    if os.path.exists(repo_path):
        try:
            for root, dirs, files in os.walk(repo_path):
                for directory in files:
                    os.chmod(os.path.join(root, directory), stat.S_IRWXU)
                for name in dirs:
                    os.chmod(os.path.join(root, name), stat.S_IRWXU)
            os.chmod(root, stat.S_IRWXU)
            shutil.rmtree(repo_path, ignore_errors=False)
            print(f"{repo_name} was deleted successfully!")
            
            return True
        except Exception as e:
            print(f"Error in removing {repo_name}: ", e)
            return False
    else:
        print(f"{repo_name} does not exist")
        return False
