# Router running syntax check
from fastapi import APIRouter, Request
import uvicorn
import sys
sys.path.append('app/lib')
from util import check_syntax, clone_repo

router = APIRouter()

REPO_PATH = "https://github.com/rtyley/small-test-repo"

@router.post("/check_syntax")
async def compile(request: Request):
    print(":SLKEFSEFSEO")

    if clone_repo(REPO_PATH):
        print("Repo cloned successfully")
    
        if check_syntax("./cloned_repo"):
            print("Syntax check passed")
            return {"status": "ok"}   
    
    return {"status": "not ok"}

