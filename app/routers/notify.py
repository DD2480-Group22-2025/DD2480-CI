# Webhook notification router
from fastapi import APIRouter, Request
from typing import Any
from pydantic import BaseModel

router = APIRouter()

class WebhookPayload(BaseModel):
    data: Any

@router.post("/webhook")
async def notify(payload: WebhookPayload):
    return {"message": "Notify", "received_data": payload}