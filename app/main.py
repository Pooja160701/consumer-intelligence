from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from app.api.routes import router

BASE_DIR = Path(__file__).resolve().parent.parent
DASHBOARD_DIR = BASE_DIR / "dashboard"

app = FastAPI(
    title="Consumer Intelligence Platform",
    version="1.0.0",
    description=(
        "Evidence-grounded consumer intelligence "
        "and brand insight platform."
    ),
)

app.include_router(router)

if DASHBOARD_DIR.exists():
    app.mount(
        "/dashboard",
        StaticFiles(directory=DASHBOARD_DIR),
        name="dashboard",
    )

@app.get("/")
def root() -> dict[str, str]:
    return {
        "service": "consumer-intelligence",
        "status": "running",
        "dashboard": "/dashboard/",
        "docs": "/docs",
    }

@app.get("/dashboard")
def dashboard():
    return FileResponse(
        DASHBOARD_DIR / "index.html"
    )