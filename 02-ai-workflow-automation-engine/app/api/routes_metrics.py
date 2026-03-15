"""Metrics endpoints for MVP reporting placeholders."""

from fastapi import APIRouter

from app.schemas.metrics import MetricsSummaryResponse
from app.services.roi_service import get_metrics_summary_response

router = APIRouter(prefix="/metrics", tags=["metrics"])


@router.get("/summary", response_model=MetricsSummaryResponse)
def read_metrics_summary() -> MetricsSummaryResponse:
    """Return aggregated KPI summary for processed workflows."""
    return get_metrics_summary_response()
