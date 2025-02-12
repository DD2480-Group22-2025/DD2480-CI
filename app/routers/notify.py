# Webhook notification router
from fastapi import APIRouter, Request
import uvicorn
import sys
sys.path.append('app/lib')
from util import check_syntax, clone_repo, delete_repo
from typing import Any
from pydantic import BaseModel

router = APIRouter()

class WebhookPayload(BaseModel):
    data: Any

@router.post("/webhook")
async def notify(payload: dict):

    repo_url = payload["repository"]["clone_url"]
    id = payload["repository"]["pushed_at"]
    branch = payload["ref"].split("/")[-1]

    print(f"Push event to {repo_url} on branch {branch}")

    print("Attempting to clone repo...")

    if clone_repo(repo_url, id, branch):

        print("Repo cloned successfully!")
        repo_name = repo_url.split("/")[-1].split(".")[0] + "-" + str(id)

        if check_syntax(f"./cloned_repo/{repo_name}"):
            # TODO: run tests
            # TODO: send notification
            return_msg = {"status": "ok"}
        else:
            return_msg = {"status": "syntax error"}

        delete_repo(repo_name)

    return return_msg