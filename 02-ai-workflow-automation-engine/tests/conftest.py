import pytest

from app.db.queries import reset_memory_store


@pytest.fixture(autouse=True)
def _reset_store() -> None:
    reset_memory_store()
