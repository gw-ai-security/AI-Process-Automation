"""ROI and KPI aggregation services."""

from app.core.config import get_settings
from app.db.queries import get_metrics_summary
from app.schemas.metrics import MetricsSummaryResponse


def estimate_saved_minutes() -> int:
    """Estimate per-case savings using baseline minus automated minutes."""
    settings = get_settings()
    return max(0, settings.manual_baseline_minutes - settings.automated_minutes)


def get_metrics_summary_response() -> MetricsSummaryResponse:
    """Return aggregated KPI summary from storage."""
    summary = get_metrics_summary()
    return MetricsSummaryResponse(**summary)
