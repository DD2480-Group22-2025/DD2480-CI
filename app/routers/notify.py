# Webhook notification router
from fastapi import APIRouter, Request
import uvicorn
import sys
sys.path.append('app/lib')
from util import check_syntax, clone_repo
from typing import Any
from pydantic import BaseModel

router = APIRouter()

class WebhookPayload(BaseModel):
    data: Any

@router.post("/webhook")
async def notify(payload: dict):

    repo_url = payload["repository"]["clone_url"]
    # TODO: get branch from payload

    print(f"push to {repo_url}")

    print("Cloning repo...")

    if clone_repo(repo_url):
        print("Repo cloned successfully!")
    
        if check_syntax("./cloned_repo"):
            # TODO: run tests
            
            return {"status": "ok"}    

    return {"message": "repo not cloned. "}