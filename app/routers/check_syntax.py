# Router running syntax check
from fastapi import APIRouter, Request
# from lib.util import compile_project

router = APIRouter()

REPO_PATH = ""

@router.post("/check_syntax")
async def compile(request: Request):
    # payload = await request.json()

#     # ensure it's a push event
#     if payload.get("ref") == 'refs/heads/assessment':
#         commit_id = payload['after']
#         repo_url = payload['repository']['html_url']

#         success, output = compile_project(repo_url)

#         return {"status": "compilation completed", "success": success, "output": output}
    
    return {"status": "ok"}

