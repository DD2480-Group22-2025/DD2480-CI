from fastapi import APIRouter, Request, HTTPException
import os
import sys
import subprocess
import subprocess
sys.path.append('app/lib')
from util import check_syntax, clone_repo, update_commit_status, delete_repo
from typing import Any, Optional
from pydantic import BaseModel
from dotenv import load_dotenv

# Load environment variables from a .env file, if present
load_dotenv()

router = APIRouter()

class Repository(BaseModel):
    clone_url: str
    full_name: str
    pushed_at: str

class HeadCommit(BaseModel):
    id: str

class Repository(BaseModel):
    clone_url: str
    full_name: str
    pushed_at: str

class HeadCommit(BaseModel):
    id: str

class WebhookPayload(BaseModel):
    ref: str
    repository: Repository
    head_commit: HeadCommit
    ref: str
    repository: Repository
    head_commit: HeadCommit

@router.post("/webhook")
async def notify(payload: WebhookPayload):
    try:
        # Extract repository info and branch
        repo_url = payload.repository.clone_url
        identifier = payload.repository.pushed_at
        branch = payload.ref.split("/")[-1]
        
        # Extract and set repo owner and name from the payload
        owner, name = payload.repository.full_name.split("/")
        os.environ["REPO_OWNER"] = owner
        os.environ["REPO_NAME"] = name
        
async def notify(payload: WebhookPayload):
    try:
        # Extract repository info and branch
        repo_url = payload.repository.clone_url
        identifier = payload.repository.pushed_at
        branch = payload.ref.split("/")[-1]
        
        # Extract and set repo owner and name from the payload
        owner, name = payload.repository.full_name.split("/")
        os.environ["REPO_OWNER"] = owner
        os.environ["REPO_NAME"] = name
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing payload: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Error processing payload: {str(e)}")
    
    print(f"Push event to {repo_url} on branch {branch}")
    print("Attempting to clone repo...")
    
    # Attempt to clone the repository using repo_url, identifier, and branch
    if not clone_repo(repo_url, identifier, branch):
        return {"message": "Repo not cloned."}
    
    print("Repo cloned successfully!")
    
    # Construct the cloned repo directory name
    repo_dir_name = repo_url.split("/")[-1].split(".")[0] + "-" + str(identifier)
    repo_path = f"./cloned_repo/{repo_dir_name}"
    
    # Get the commit SHA from the payload
    commit_sha = payload.head_commit.id

    try:
        # Set overall build status to pending
        update_commit_status(commit_sha, "pending", "CI process started", "CI/overall")
        
        # Run syntax check
        print("Running syntax check...")
        update_commit_status(commit_sha, "pending", "Running syntax check", "CI/syntax")
        if not check_syntax(repo_path):
            update_commit_status(commit_sha, "failure", "Syntax check failed", "CI/syntax")
            update_commit_status(commit_sha, "failure", "Build failed at syntax check", "CI/overall")
            delete_repo(repo_dir_name)
            return {"status": "syntax error"}
        update_commit_status(commit_sha, "success", "Syntax check passed", "CI/syntax")
        
        # Run tests
        print("Running tests...")
        update_commit_status(commit_sha, "pending", "Running unit tests", "CI/tests")
        try:
            # Change to repo directory and run tests
            os.chdir(repo_path)
            result = subprocess.run(['pytest'], capture_output=True, text=True)
            os.chdir('../../..')  # Return to original directory
            
            if result.returncode == 0:
                update_commit_status(commit_sha, "success", "All tests passed", "CI/tests")
                update_commit_status(commit_sha, "success", "All checks passed successfully", "CI/overall")
            else:
                update_commit_status(commit_sha, "failure", "Tests failed", "CI/tests")
                update_commit_status(commit_sha, "failure", "Build failed at test stage", "CI/overall")
                
        except Exception as e:
            update_commit_status(commit_sha, "failure", f"Error running tests: {str(e)}", "CI/tests")
            update_commit_status(commit_sha, "failure", "Build failed at test stage", "CI/overall")
            
    except Exception as e:
        try:
            update_commit_status(commit_sha, "error", f"CI process error: {str(e)}", "CI/overall")
        except:
            pass  # If we can't even update the status, just continue to cleanup
    
    # Clean up the cloned repository
    delete_repo(repo_dir_name)
    
    # Return a success response
    return {"status": "ok"}
