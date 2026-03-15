"""Health and readiness endpoints."""

from datetime import UTC, datetime

from fastapi import APIRouter

from app.db.connection import check_database_connection

router = APIRouter(tags=["health"])


@router.get("/health")
def get_health() -> dict[str, object]:
    """Return basic service and database health status."""
    return {
        "status": "ok",
        "timestamp": datetime.now(UTC).isoformat(),
        "database_connected": check_database_connection(),
    }
