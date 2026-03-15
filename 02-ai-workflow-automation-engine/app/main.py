"""FastAPI application entrypoint for the Phase 1 MVP."""

from pathlib import Path
import sys

from fastapi import FastAPI

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.api.routes_health import router as health_router
from app.api.routes_ingest import router as ingest_router
from app.api.routes_mock import router as mock_router
from app.api.routes_metrics import router as metrics_router
from app.api.routes_workflow import router as workflow_router
from app.core.config import get_settings
from app.core.logging import configure_logging

settings = get_settings()
configure_logging(settings.log_level)

app = FastAPI(
    title=settings.app_name,
    version="0.2.0",
    description="Webhook-driven workflow automation engine for summarization, routing and automation impact tracking.",
)

app.include_router(health_router)
app.include_router(ingest_router)
app.include_router(metrics_router)
app.include_router(workflow_router)
app.include_router(mock_router)


@app.get("/", tags=["root"])
def read_root() -> dict[str, str]:
    """Provide a simple entrypoint message for local verification."""
    return {
        "service": settings.app_name,
        "status": "ready",
        "docs_url": "/docs",
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=settings.app_host,
        port=settings.app_port,
        reload=False,
    )
