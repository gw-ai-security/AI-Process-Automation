"""Mock integration endpoints for n8n routing demos."""

from datetime import UTC, datetime

from fastapi import APIRouter
from pydantic import BaseModel, Field


class MockIntegrationPayload(BaseModel):
    """Payload consumed by mock integration endpoints."""

    workflow_id: int = Field(..., ge=1)
    correlation_id: str
    summary: str
    priority: str
    route_to: str


router = APIRouter(prefix="/mock", tags=["mock-integrations"])


@router.post("/jira")
def post_mock_jira(payload: MockIntegrationPayload) -> dict[str, str]:
    """Simulate Jira ticket creation."""
    return {
        "status": "accepted",
        "target": "mock_jira",
        "ticket_ref": f"JIRA-{payload.workflow_id}",
        "received_at": datetime.now(UTC).isoformat(),
    }


@router.post("/slack")
def post_mock_slack(payload: MockIntegrationPayload) -> dict[str, str]:
    """Simulate Slack alert dispatch."""
    return {
        "status": "accepted",
        "target": "mock_slack",
        "message_ref": f"SLACK-{payload.workflow_id}",
        "received_at": datetime.now(UTC).isoformat(),
    }
