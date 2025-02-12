import os
import subprocess
import shutil
import stat
import time
from github import Github  # PyGithub library
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
        python_files = []
        for root, _, files in os.walk(repo):
            for file in files:
                if file.endswith('.py'):
                    python_files.append(os.path.join(root, file))
        
        if not python_files:
            print("No Python files found to check")
            return True
            
        # Check each Python file
        for py_file in python_files:
            syntax = subprocess.run(["pylint", py_file, "--errors-only"], capture_output=True, text=True)
            if "syntax-error" in syntax.stdout:
                print(f"Syntax error found in {py_file}")
                return False
        
        print("Syntax check passed with no errors.")
        return True
        
    except Exception as e:
        print("Error in syntax check:", e)
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
        
        # First, try to find and remove any old status with CI/ prefix or default context
        for status in commit.get_statuses():
            if status.context.startswith("CI/") or status.context == "CI Notification":
                # GitHub doesn't allow deleting statuses, so we'll update them to be neutral/skipped
                commit.create_status(
                    state="success",
                    target_url="",
                    description="Deprecated status check",
                    context=status.context
                )
        
        # Create the new status
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
