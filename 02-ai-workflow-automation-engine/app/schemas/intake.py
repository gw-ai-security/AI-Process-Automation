"""Schemas for operational intake requests and responses."""

from typing import Literal

from pydantic import BaseModel, Field, field_validator


SourceType = Literal["meeting_note", "issue", "support_text", "onboarding_note", "other"]


class IntakeRequest(BaseModel):
    """Input accepted by the Phase 1 intake endpoint."""

    source_type: SourceType = Field(
        ...,
        description="Type of operational source that produced the unstructured input.",
    )
    source_system: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="System, team, or process that generated the intake.",
    )
    content: str = Field(
        ...,
        min_length=10,
        max_length=5000,
        description="Raw operational text to be processed in later phases.",
    )
    submitted_by: str = Field(
        ...,
        min_length=3,
        max_length=255,
        description="Identifier for the human or system submitting the payload.",
    )
    tags: list[str] = Field(
        default_factory=list,
        description="Optional classification tags for routing and reporting.",
    )
    priority: Literal["low", "medium", "high"] = Field(
        default="medium",
        description="Requested urgency level for downstream handling.",
    )

    @field_validator("source_system", "submitted_by")
    @classmethod
    def strip_string_fields(cls, value: str) -> str:
        """Remove surrounding whitespace and reject empty normalized values."""
        normalized = value.strip()
        if not normalized:
            raise ValueError("value must not be blank")
        return normalized

    @field_validator("content")
    @classmethod
    def normalize_content(cls, value: str) -> str:
        """Trim content while preserving user intent."""
        normalized = value.strip()
        if len(normalized) < 10:
            raise ValueError("content must contain meaningful text")
        return normalized

    @field_validator("tags")
    @classmethod
    def normalize_tags(cls, value: list[str]) -> list[str]:
        """Normalize tags for predictable downstream processing."""
        normalized = []
        for tag in value:
            cleaned = tag.strip().lower()
            if cleaned:
                normalized.append(cleaned)
        return normalized


class IntakeResponse(BaseModel):
    """Response returned by the intake endpoint."""

    workflow_id: int = Field(..., description="Persisted workflow input identifier.")
    correlation_id: str = Field(..., description="Generated request correlation identifier.")
    status: Literal["accepted"] = Field(..., description="Current processing state.")
    message: str = Field(..., description="Human-readable processing status note.")
    normalized_payload: IntakeRequest = Field(
        ...,
        description="Echo of the validated payload.",
    )
    summary: str = Field(..., description="Generated summary from LLM processing.")
    action_items: list[str] = Field(..., description="Generated action items.")
    priority: Literal["low", "medium", "high"] = Field(..., description="Final classified priority.")
    route_to: Literal["sales", "ops", "support", "product"] = Field(
        ...,
        description="Final routing destination.",
    )
    saved_minutes: int = Field(..., ge=0, description="Estimated minutes saved for this intake.")
    processing_time_ms: int = Field(..., ge=0, description="End-to-end processing time in ms.")
