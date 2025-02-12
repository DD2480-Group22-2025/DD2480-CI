import os
import subprocess
import shutil
import stat
import time
from github import Github  # PyGithub library

def check_syntax(repo):
    """
    Check the syntax of the code using pylint.
    Returns True if no syntax errors, otherwise False.
    """
    if not os.path.exists(repo):
        print("File does not exist")
        return False
    try:
        syntax = subprocess.run(["pylint", f"{repo}", "--errors-only"], capture_output=True, text=True)
    except Exception as e:
        print("Error in syntax check:", e)
        return False
    return "syntax-error" not in syntax.stdout

def clone_repo(repo_url, identifier, branch):
    """
    Clone the given repo from GitHub.
    Returns True if cloning is successful, otherwise False.
    """
    if "https://github.com" not in repo_url:
        print("Invalid GitHub repo URL")
        return False

    repo_name = repo_url.split("/")[-1].split(".")[0] + "-" + str(identifier)
    clone_dir = f"./cloned_repo/{repo_name}"

    if os.path.exists(clone_dir):
        shutil.rmtree(clone_dir)
        time.sleep(1)

    try:
        subprocess.run(["git", "clone", repo_url, clone_dir], check=True)
        subprocess.run(["git", "checkout", branch], cwd=clone_dir, check=True)
        subprocess.run(["git", "pull"], cwd=clone_dir, check=True)
    except Exception as e:
        print(f"Error in cloning {repo_name} ", e)
        return False

    return os.path.exists(clone_dir) and len(os.listdir(clone_dir)) > 0

def update_commit_status(commit_sha: str, state: str, description: str, context: str = "CI Notification") -> dict:
    """
    Update the commit status on GitHub using PyGithub.
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

    commit = repo.get_commit(commit_sha)
    status = commit.create_status(
        state=state,  # "pending", "success", or "failure"
        target_url="",  # Optionally add a URL for build logs
        description=description,
        context=context
    )
    return status.raw_data

def delete_repo(repo_name):
    """
    Delete the cloned repository directory.
    """
    repo_path = os.path.join("./cloned_repo", repo_name)
    if os.path.exists(repo_path):
        shutil.rmtree(repo_path)
        print(f"Deleted cloned repo: {repo_name}")
        return True
    return False
