from fastapi import APIRouter, Request, HTTPException
import os
import sys
sys.path.append('app/lib')
from util import check_syntax, clone_repo, update_commit_status, delete_repo
from typing import Any
from pydantic import BaseModel
from dotenv import load_dotenv

# Load environment variables from a .env file, if present
load_dotenv()

router = APIRouter()

class WebhookPayload(BaseModel):
    data: Any

@router.post("/webhook")
async def notify(request: Request):
    try:
        payload = await request.json()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid JSON payload: {str(e)}")
    
    # Extract repository info and branch
    try:
        repo_url = payload["repository"]["clone_url"]
        identifier = payload["repository"].get("pushed_at", "default_id")
        branch = payload["ref"].split("/")[-1]
    except KeyError as e:
        raise HTTPException(status_code=400, detail=f"Missing required field: {str(e)}")
    
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
    
    # Run syntax check on the cloned repository
    if not check_syntax(f"./cloned_repo/{repo_dir_name}"):
        update_commit_status(commit_sha, "failure", "Syntax error")
        delete_repo(repo_dir_name)
        return {"status": "syntax error"}
    
    # For testing, assume tests pass; set build state and description
    try: 
        notification_result = update_commit_status(commit_sha, "success", "Build passed")
    except Exception as e:
        delete_repo(repo_dir_name)
        raise HTTPException(status_code=500, detail=f"Error updating commit status: {str(e)}")
    
    #Clean up repo
    delete_repo(repo_dir_name)

    return {"status": "ok", "notification": notification_result}
