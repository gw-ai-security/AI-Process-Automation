"""Workflow orchestration service for end-to-end intake processing."""

from __future__ import annotations

from datetime import datetime
from time import perf_counter
from uuid import uuid4

from app.db.queries import (
    get_workflow_detail,
    insert_workflow_error,
    insert_workflow_event,
    insert_workflow_input,
    insert_workflow_metric,
    insert_workflow_output,
)
from app.schemas.intake import IntakeRequest, IntakeResponse
from app.schemas.workflow import WorkflowDetailResponse, WorkflowOutputPayload
from app.services.llm_service import extract_structured_output
from app.services.roi_service import estimate_saved_minutes
from app.services.routing_service import resolve_route


def process_intake(payload: IntakeRequest) -> IntakeResponse:
    """Execute intake processing and persist workflow artifacts."""
    correlation_id = str(uuid4())
    started = perf_counter()
    workflow_id = insert_workflow_input(correlation_id=correlation_id, payload=payload)
    insert_workflow_event(
        correlation_id=correlation_id,
        event_type="intake_received",
        event_payload={"workflow_id": workflow_id, "source_type": payload.source_type},
    )

    try:
        llm_output = extract_structured_output(payload)
        final_route = resolve_route(payload, llm_output.route_to)
        saved_minutes = estimate_saved_minutes()
        processing_time_ms = int((perf_counter() - started) * 1000)

        output_payload = {
            "summary": llm_output.summary,
            "action_items": llm_output.action_items,
            "priority": llm_output.priority,
            "route_to": final_route,
            "confidence": llm_output.confidence,
            "reasoning_short": llm_output.reasoning_short,
            "saved_minutes": saved_minutes,
            "processing_time_ms": processing_time_ms,
        }
        insert_workflow_output(workflow_id=workflow_id, output_payload=output_payload)
        insert_workflow_event(
            correlation_id=correlation_id,
            event_type="workflow_completed",
            event_payload={"workflow_id": workflow_id, "route_to": final_route},
        )

        insert_workflow_metric(correlation_id, "processed_input", 1, "count")
        insert_workflow_metric(correlation_id, "saved_minutes", saved_minutes, "minutes")
        insert_workflow_metric(correlation_id, "processing_time_ms", processing_time_ms, "ms")
        insert_workflow_metric(correlation_id, f"route_{final_route}", 1, "count")

        return IntakeResponse(
            workflow_id=workflow_id,
            correlation_id=correlation_id,
            status="accepted",
            message="Workflow intake processed successfully.",
            normalized_payload=payload,
            summary=output_payload["summary"],
            action_items=output_payload["action_items"],
            priority=output_payload["priority"],
            route_to=output_payload["route_to"],
            saved_minutes=output_payload["saved_minutes"],
            processing_time_ms=output_payload["processing_time_ms"],
        )
    except Exception as exc:
        insert_workflow_error(
            correlation_id=correlation_id,
            error_code="workflow_processing_error",
            error_message=str(exc),
            error_context={"workflow_id": workflow_id},
        )
        insert_workflow_event(
            correlation_id=correlation_id,
            event_type="workflow_failed",
            event_payload={"workflow_id": workflow_id, "error": str(exc)},
        )
        raise


def get_workflow_by_id(workflow_id: int) -> WorkflowDetailResponse | None:
    """Return workflow detail payload by ID."""
    row = get_workflow_detail(workflow_id)
    if row is None:
        return None

    output_payload = row.get("output_payload")
    workflow_output = WorkflowOutputPayload(**output_payload) if output_payload else None
    created_at = row["created_at"]
    if isinstance(created_at, str):
        created_at = datetime.fromisoformat(created_at)

    return WorkflowDetailResponse(
        workflow_id=row["workflow_id"],
        correlation_id=row["correlation_id"],
        source_type=row["source_type"],
        source_system=row["source_system"],
        submitted_by=row["submitted_by"],
        priority_requested=row["priority_requested"],
        created_at=created_at,
        input_payload=IntakeRequest(
            source_type=row["source_type"],
            source_system=row["source_system"],
            content=row["content"],
            submitted_by=row["submitted_by"],
            tags=row["tags"] or [],
            priority=row["priority_requested"],
        ),
        output_payload=workflow_output,
    )
