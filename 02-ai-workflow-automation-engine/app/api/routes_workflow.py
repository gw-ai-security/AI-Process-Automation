"""Workflow detail endpoint."""

from fastapi import APIRouter, HTTPException

from app.schemas.workflow import WorkflowDetailResponse
from app.services.workflow_service import get_workflow_by_id

router = APIRouter(prefix="/workflow", tags=["workflow"])


@router.get("/{workflow_id}", response_model=WorkflowDetailResponse)
def read_workflow(workflow_id: int) -> WorkflowDetailResponse:
    """Return persisted workflow input and output details."""
    workflow = get_workflow_by_id(workflow_id)
    if workflow is None:
        raise HTTPException(status_code=404, detail="Workflow not found")
    return workflow
