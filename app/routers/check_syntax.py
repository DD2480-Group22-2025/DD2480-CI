# Router running syntax check
from fastapi import APIRouter, Request
# from "../lib/util" import compile_project

router = APIRouter()

REPO_PATH = "/test_repo/git_repo"

@router.post("/check_syntax")
async def compile(request: Request):
    
    data = await request.json()

    data = data['data']
    
    # run syntax check 
    
    return {"status": "ok"}

