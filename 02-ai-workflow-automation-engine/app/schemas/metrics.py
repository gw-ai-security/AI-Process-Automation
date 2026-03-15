"""Schemas for metrics reporting."""

from pydantic import BaseModel, Field


class MetricsSummaryResponse(BaseModel):
    """Aggregated KPI summary for the MVP."""

    total_inputs: int = Field(..., description="Count of processed intake requests.")
    success_rate: float = Field(..., description="Output generation success ratio.")
    avg_processing_time_ms: float = Field(..., description="Average processing latency in milliseconds.")
    route_counts: dict[str, int] = Field(
        ...,
        description="Distribution of routing decisions by destination.",
    )
    total_saved_minutes: int = Field(..., description="Estimated total saved minutes.")
