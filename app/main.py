from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(
    title="Consumer Intelligence Platform",
    version="1.0.0",
    description=(
        "Evidence-grounded consumer intelligence "
        "and brand insight platform."
    ),
)

app.include_router(router)

@app.get("/")
def root() -> dict[str, str]:
    return {
        "service": "consumer-intelligence",
        "status": "running",
    }