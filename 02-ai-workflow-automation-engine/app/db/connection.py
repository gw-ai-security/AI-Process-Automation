"""Database connection helpers."""

from psycopg import connect
from psycopg.rows import dict_row

from app.core.config import get_settings


def get_connection():
    """Create a new psycopg connection using the configured database URL."""
    settings = get_settings()
    return connect(settings.database_url, row_factory=dict_row, connect_timeout=2)


def check_database_connection() -> bool:
    """Best-effort DB connectivity check used by the health endpoint."""
    try:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1;")
                cursor.fetchone()
        return True
    except Exception:
        return False
