# Utility functions
import os
import subprocess

def check_syntax(repo):
    # this function checks the syntax of the code using pylint
    # returns true or false based on if the syntax passes

    # make sure the file exists
    if not os.path.exists(repo):
        print("File does not exist")
        return False
    
    try:
        # Check syntax
        syntax = subprocess.run(["pylint", f"{repo}", "--errors-only"], capture_output=True, text=True)
    
    except Exception as e:
        print("Error in syntax check: ", e)
        return False
    
    # check if there is a syntax error
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
            subprocess.run(["rm", "-rf", "./cloned_repo/"])
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
    
    