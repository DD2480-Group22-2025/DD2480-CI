from fastapi import FastAPI
from app.routers import notify
import uvicorn

app = FastAPI()

app.include_router(notify.router)

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

