# Router for running tests
from fastapi import APIRouter, Request

router = APIRouter()

@router.post("/run_tests")
async def run_tests(request: Request):
    return {"message": "Tests run"}
