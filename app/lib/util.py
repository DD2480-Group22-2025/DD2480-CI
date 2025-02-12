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
    
def clone_repo(repo_url):
    # clone the given repo
    # eventually need to checkout the given branch
    
    # check if the repo url is valid
    if "https://github.com" not in repo_url:
        print("Invalid GitHub repo URL")
        return False

    if os.path.exists("./cloned_repo"):
        try:
            for root, dirs, files in os.walk("./cloned_repo"):
                for directory in files:
                    os.chmod(os.path.join(root, directory), stat.S_IRWXU)
                for name in dirs:
                    os.chmod(os.path.join(root, name), stat.S_IRWXU)
            os.chmod(root, stat.S_IRWXU)
            shutil.rmtree("./cloned_repo", ignore_errors=False)
            print("removed cloned_repo")
            time.sleep(2)
        except Exception as e:
            print("Error in removing cloned_repo: ", e)
            return False

    try:
        subprocess.run(["git", "clone", f"{repo_url}", "./cloned_repo/"])
    
    except Exception as e:
        print("Error in cloning the repo: ", e)
        return False
    
    if os.path.exists("./cloned_repo") and len(os.listdir("./cloned_repo")) > 0:
        print("GitHub repo cloned successfully to ./cloned_repo")
        return True
    
    else:
        print("Repo cloning failed.")
        return False
    
