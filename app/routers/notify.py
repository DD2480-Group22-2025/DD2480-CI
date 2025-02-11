# Webhook notification router
from fastapi import APIRouter, Request
import uvicorn
import sys
sys.path.append('app/lib')
from util import check_syntax, clone_repo
router = APIRouter()

# REPO_PATH = ""

@router.post("/webhook")
async def notify(request: Request):

    # payload = await request.json()

    # print(payload)
    # repo_url = payload["clone_url"]
    # todo: get branch from payload

    # print(f"push to {repo_url}")

    # print("Cloning repo...")

    # if clone_repo(REPO_PATH):
    #     print("Repo cloned successfully!")
    
    #     if check_syntax("./cloned_repo"):
    #         print("Syntax check passed")
    #         
    #         # run tests
    #         # run_tests()
    #           return {"status": "ok"}    
    # return {"status": "not ok"}
    return {"message": "Notify"}