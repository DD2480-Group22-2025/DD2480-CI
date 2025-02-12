# Utility functions
import os
import subprocess
import shutil
import stat
import time

def check_syntax(repo):
    # this function checks the syntax of the code using pylint
    # returns true or false based on if the syntax passes

    if not os.path.exists(repo):
        print("File does not exist")
        return False
    
    try:
        syntax = subprocess.run(["pylint", f"{repo}", "--errors-only"], capture_output=True, text=True)
    
    except Exception as e:
        print("Error in syntax check: ", e)
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