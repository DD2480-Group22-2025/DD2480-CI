from fastapi import FastAPI
from app.routers import notify, builds
import uvicorn

app = FastAPI()

app.include_router(notify.router)
app.include_router(builds.router)

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

