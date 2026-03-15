"""Schemas for workflow retrieval endpoints."""

from datetime import datetime

from pydantic import BaseModel, Field

from app.schemas.intake import IntakeRequest


class WorkflowOutputPayload(BaseModel):
    """Structured workflow output stored after intake processing."""

    summary: str
    action_items: list[str]
    priority: str
    route_to: str
    confidence: float | None = None
    reasoning_short: str | None = None
    saved_minutes: int
    processing_time_ms: int


class WorkflowDetailResponse(BaseModel):
    """Response for `GET /workflow/{id}`."""

    workflow_id: int = Field(..., description="Workflow input record ID.")
    correlation_id: str = Field(..., description="Request correlation ID.")
    source_type: str
    source_system: str
    submitted_by: str
    priority_requested: str
    created_at: datetime
    input_payload: IntakeRequest
    output_payload: WorkflowOutputPayload | None = None
