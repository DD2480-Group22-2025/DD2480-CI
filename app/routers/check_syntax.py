# Router running syntax check
from fastapi import APIRouter, Request

router = APIRouter()

@router.post("/check_syntax")
async def check_syntax(request: Request):
    return {"message": "Syntax check"}
