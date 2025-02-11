from fastapi import FastAPI
from app.routers import check_syntax, notify, run_tests, builds
import uvicorn

app = FastAPI()

app.include_router(check_syntax.router)
app.include_router(notify.router)
app.include_router(run_tests.router)
app.include_router(builds.router)


@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

