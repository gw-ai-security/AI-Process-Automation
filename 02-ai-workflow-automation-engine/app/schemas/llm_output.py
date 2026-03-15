"""Schema for structured LLM extraction outputs."""

from pydantic import BaseModel, Field


class LLMOutput(BaseModel):
    """Structured output returned by the LLM service."""

    summary: str = Field(..., min_length=10, description="Condensed summary of the intake text.")
    action_items: list[str] = Field(default_factory=list, description="Actionable next steps.")
    priority: str = Field(..., description="Classified priority: low, medium, or high.")
    route_to: str = Field(..., description="Suggested destination: sales, ops, support, or product.")
    confidence: float | None = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="Optional confidence score for the classification output.",
    )
    reasoning_short: str | None = Field(
        default=None,
        description="Optional short rationale for explainability in demos.",
    )
