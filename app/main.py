from fastapi import FastAPI
from app.routers import check_syntax, notify, run_tests

app = FastAPI()

app.include_router(check_syntax.router)
app.include_router(notify.router)
app.include_router(run_tests.router)

# Mock build history
builds = [
    {"id": 1, "commit": "abc123", "date": "2024-02-09", "logs": "Build successful"},
    {"id": 2, "commit": "def456", "date": "2024-02-08", "logs": "Build failed"},
]

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

@app.get("/builds")
def get_builds():
    return {"builds": builds}