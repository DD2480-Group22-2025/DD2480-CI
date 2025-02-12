from fastapi import APIRouter, Request, HTTPException
import os
import sys
sys.path.append('app/lib')

from util import check_syntax, clone_repo, update_commit_status, delete_repo
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

router = APIRouter()

@router.post("/webhook")
async def notify(request: Request):
    try:
        payload = await request.json()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid JSON payload: {str(e)}")

    try:
        repo_url = payload["repository"]["clone_url"]
        identifier = payload["repository"].get("pushed_at", "default_id")
        branch = payload["ref"].split("/")[-1]
        commit_sha = payload.get("commit") or payload.get("head_commit", {}).get("id")
    except KeyError as e:
        raise HTTPException(status_code=400, detail=f"Missing required field: {str(e)}")

    if not commit_sha:
        raise HTTPException(status_code=400, detail="Payload must include commit SHA (commit or head_commit.id).")

    print(f"Push event received for repo: {repo_url} on branch {branch}")

    if not clone_repo(repo_url, identifier, branch):
        return {"message": "Repo not cloned."}

    repo_dir_name = repo_url.split("/")[-1].split(".")[0] + "-" + str(identifier)

    build_state = "success"
    build_description = "Build passed"

    if not check_syntax(f"./cloned_repo/{repo_dir_name}"):
        build_state = "failure"
        build_description = "Syntax errors found"

    try:
        notification_result = update_commit_status(commit_sha, build_state, build_description)
    except Exception as e:
        delete_repo(repo_dir_name)
        raise HTTPException(status_code=500, detail=f"Error updating commit status: {str(e)}")

    delete_repo(repo_dir_name)

    return {"status": build_state, "notification": notification_result}
