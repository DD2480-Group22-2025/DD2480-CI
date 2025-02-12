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

def clone_repo(repo_url, id, branch):

    # clone the given repo
    
    # check if the repo url is valid
    if "https://github.com" not in repo_url:
        print("Invalid GitHub repo URL")
        return False

    # extract the repo name
    repo_name = repo_url.split("/")[-1].split(".")[0] + "-" + str(id)

    try:
        subprocess.run(["git", "clone", f"{repo_url}", f"./cloned_repo/{repo_name}"])
        subprocess.run(["git", "checkout", f"{branch}"], cwd=f"./cloned_repo/{repo_name}")
        subprocess.run(["git", "pull"], cwd=f"./cloned_repo/{repo_name}")

    except Exception as e:
        print(f"Error in cloning {repo_name} ", e)
        return False
    
    if os.path.exists(f"./cloned_repo/{repo_name}") and len(os.listdir(f"./cloned_repo/{repo_name}")) > 0:
        print(f"GitHub repo cloned successfully to ./cloned_repo/{repo_name}")

        return True
    else:
        print(f"Cloning {repo_name} failed")
        return False

def update_commit_status(commit_sha: str, state: str, description: str, context: str = "CI Notification") -> dict:
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

    g = Github(token)
    try:
        repo = g.get_repo(f"{repo_owner}/{repo_name}")
    except Exception as e:
        raise Exception(f"Error accessing repository: {str(e)}")

    try:
        commit = repo.get_commit(commit_sha)
        status = commit.create_status(
            state=state,           
            target_url="",  
            description=description,
            context=context
        )
        return status.raw_data
    except Exception as e:
        raise Exception(f"Error updating commit status: {str(e)}")
    
        
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
