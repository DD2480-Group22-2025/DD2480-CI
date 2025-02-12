import os
import subprocess
import shutil
import stat
import time
from github import Github  # PyGithub library

def check_syntax(repo):
    if not os.path.exists(repo):
        print("File does not exist")
        return False
    try:
        syntax = subprocess.run(["pylint", f"{repo}", "--errors-only"], capture_output=True, text=True)
    except Exception as e:
        print("Error in syntax check:", e)
        return False
    if "syntax-error" not in syntax.stdout:
        print("Syntax check passed with no errors.")
        return True
    else:
        print("Syntax check failed. There is a syntax error.")
        return False

def clone_repo(repo_url, identifier, branch):
    # Clone the repo into a directory named "cloned_repo/<repo_name>-<identifier>"
    # Validate URL
    if "https://github.com" not in repo_url:
        print("Invalid GitHub repo URL")
        return False
    clone_dir = f"./cloned_repo/{repo_url.split('/')[-1].split('.')[0]}-{identifier}"
    # Remove previous clone if it exists
    if os.path.exists(clone_dir):
        try:
            shutil.rmtree(clone_dir)
            print("Removed previous clone directory.")
            time.sleep(2)
        except Exception as e:
            print("Error removing cloned repo:", e)
            return False
    try:
        subprocess.run(["git", "clone", repo_url, clone_dir], check=True)
    except Exception as e:
        print("Error cloning the repo:", e)
        return False
    if os.path.exists(clone_dir) and len(os.listdir(clone_dir)) > 0:
        print(f"GitHub repo cloned successfully to {clone_dir}")
        return True
    else:
        print("Repo cloning failed.")
        return False

def update_commit_status(commit_sha: str, state: str, description: str, context: str = "CI Notification") -> dict:
    """
    Update the commit status on GitHub using PyGithub.
    
    Requires:
      - CI_SERVER_AUTH_TOKEN
      - REPO_OWNER
      - REPO_NAME
      
    Returns GitHub API's raw response data.
    """
    token = os.getenv("CI_SERVER_AUTH_TOKEN")
    repo_owner = os.getenv("REPO_OWNER")
    repo_name = os.getenv("REPO_NAME")
    
    if not token or not repo_owner or not repo_name:
        raise Exception("Missing GitHub configuration. Please check the environment variables.")
    
    g = Github(token)
    try:
        repo = g.get_repo(f"{repo_owner}/{repo_name}")
    except Exception as e:
        raise Exception(f"Error accessing repository: {str(e)}")
    
    try:
        commit = repo.get_commit(commit_sha)
        status = commit.create_status(
            state=state,           # "pending", "success", or "failure"
            target_url="",         # Optionally add a URL for build logs
            description=description,
            context=context
        )
        return status.raw_data
    except Exception as e:
        raise Exception(f"Error updating commit status: {str(e)}")

def delete_repo(repo_name):
    """
    Delete the cloned repository directory.
    Assumes the clone is in "./cloned_repo/<repo_name>"
    """
    clone_path = f"./cloned_repo/{repo_name}"
    if os.path.exists(clone_path):
        try:
            shutil.rmtree(clone_path)
            print(f"Deleted cloned repo directory: {clone_path}")
        except Exception as e:
            print("Error deleting repo:", e)
