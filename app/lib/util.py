# Utility functions
import os
import subprocess

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