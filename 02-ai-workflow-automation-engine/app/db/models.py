"""Database model placeholders for future persistence layers.

Phase 1 uses raw SQL bootstrap files and keeps Python-side DB modeling minimal.
"""

from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class WorkflowInputRecord:
    """Represents a future persisted workflow input."""

    id: int
    correlation_id: str
    source_type: str
    created_at: datetime
