"""Operational intake endpoint."""

from fastapi import APIRouter

from app.schemas.intake import IntakeRequest, IntakeResponse
from app.services.workflow_service import process_intake

router = APIRouter(tags=["intake"])


@router.post("/intake", response_model=IntakeResponse)
def post_intake(payload: IntakeRequest) -> IntakeResponse:
    """Accept operational intake and execute end-to-end workflow processing."""
    return process_intake(payload)
