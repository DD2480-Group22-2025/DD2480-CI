from fastapi import APIRouter, Request, HTTPException
import os
import sys
import subprocess
sys.path.append('app/lib')
from util import check_syntax, clone_repo, update_commit_status, delete_repo, run_tests
from typing import Any, Optional, Dict
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

class WebhookPayload(BaseModel):
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
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing payload: {str(e)}")
    
    print(f"Push event to {repo_url} on branch {branch}")
    
    # Extract the commit SHA
    commit_sha = payload.get("head_commit", {}).get("id")
    if not commit_sha:
        raise HTTPException(status_code=400, detail="Payload must include commit SHA (head_commit.id).")

    # Mark commit as "pending" before starting CI
    try:
        update_commit_status(commit_sha, "pending", "CI pipeline started.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating commit status: {str(e)}")

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

    result = {
        "status": "ok",
        "steps": {
            "syntax": {"status": "pending", "description": "Not started"},
            "tests": {"status": "pending", "description": "Not started"}
        }
    }

    try:
        # Run syntax check
        print("Running syntax check...")
        update_commit_status(commit_sha, "pending", "Running syntax check", "Syntax Check")
        
        syntax_passed = check_syntax(repo_path)
        if syntax_passed:
            update_commit_status(commit_sha, "success", "Syntax check passed", "Syntax Check")
            result["steps"]["syntax"] = {"status": "success", "description": "Syntax check passed"}
        else:
            update_commit_status(commit_sha, "failure", "Syntax check failed", "Syntax Check")
            result["steps"]["syntax"] = {"status": "failure", "description": "Syntax check failed"}
        
        # Run tests regardless of syntax check result
        print("Running tests...")
        update_commit_status(commit_sha, "pending", "Running unit tests", "Tests")
        
        test_results = run_tests(repo_path)
        
        if test_results["success"]:
            update_commit_status(commit_sha, "success", "All tests passed", "Tests")
            result["steps"]["tests"] = {"status": "success", "description": "All tests passed"}
        else:
            update_commit_status(commit_sha, "failure", "Tests failed", "Tests")
            result["steps"]["tests"] = {
                "status": "failure", 
                "description": "Tests failed",
                "output": test_results["output"],
                "error": test_results["error"]
            }
            
    except Exception as e:
        delete_repo(repo_dir_name)
        raise HTTPException(status_code=500, detail=f"Error updating commit status: {str(e)}")
    
    #Clean up repo
    delete_repo(repo_dir_name)
    
    return result

    return {"status": "ok", "notification": notification_result}
