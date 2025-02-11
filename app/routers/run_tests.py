# Router for running tests
from fastapi import APIRouter, Request
import sys, subprocess

router = APIRouter()

@router.get("/run_tests")
async def run_tests(request: Request):
    try:
        return subprocess.run(sys.path[1] + '/scripts/run_tests.sh', capture_output=True).stdout
    except Exception as ex:
        return { "this went wrong":"".format(type(ex).__name__, ex.args),
                 "path" : sys.path }

