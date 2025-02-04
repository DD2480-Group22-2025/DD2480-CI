# Webhook notification router
from fastapi import APIRouter, Request

router = APIRouter()

@router.post("/webhook")
async def notify(request: Request):
    return {"message": "Notify"}