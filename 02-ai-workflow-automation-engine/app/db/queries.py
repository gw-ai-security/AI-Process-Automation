"""Database query layer with DB-first behavior and local fallback store."""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from datetime import UTC, datetime
from decimal import Decimal
import json
from typing import Any

from app.db.connection import get_connection
from app.schemas.intake import IntakeRequest


ROUTES = ("sales", "ops", "support", "product")


@dataclass
class _MemoryStore:
    next_input_id: int
    inputs: dict[int, dict[str, Any]]
    outputs: dict[int, dict[str, Any]]
    events: list[dict[str, Any]]
    errors: list[dict[str, Any]]
    metrics: list[dict[str, Any]]


_STORE = _MemoryStore(
    next_input_id=1,
    inputs={},
    outputs={},
    events=[],
    errors=[],
    metrics=[],
)


def _now_iso() -> str:
    return datetime.now(UTC).isoformat()


def reset_memory_store() -> None:
    """Reset in-memory fallback data. Used by tests for isolation."""
    _STORE.next_input_id = 1
    _STORE.inputs.clear()
    _STORE.outputs.clear()
    _STORE.events.clear()
    _STORE.errors.clear()
    _STORE.metrics.clear()


def _insert_workflow_input_memory(correlation_id: str, payload: IntakeRequest) -> int:
    workflow_id = _STORE.next_input_id
    _STORE.next_input_id += 1
    _STORE.inputs[workflow_id] = {
        "id": workflow_id,
        "correlation_id": correlation_id,
        "source_type": payload.source_type,
        "source_system": payload.source_system,
        "submitted_by": payload.submitted_by,
        "priority": payload.priority,
        "content": payload.content,
        "tags": payload.tags,
        "created_at": _now_iso(),
    }
    return workflow_id


def insert_workflow_input(correlation_id: str, payload: IntakeRequest) -> int:
    """Persist intake input row and return workflow ID."""
    try:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO workflow_inputs (
                        correlation_id, source_type, source_system, submitted_by, priority, content, tags
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s::jsonb)
                    RETURNING id
                    """,
                    (
                        correlation_id,
                        payload.source_type,
                        payload.source_system,
                        payload.submitted_by,
                        payload.priority,
                        payload.content,
                        json.dumps(payload.tags),
                    ),
                )
                workflow_id = cursor.fetchone()["id"]
            connection.commit()
        return workflow_id
    except Exception:
        return _insert_workflow_input_memory(correlation_id, payload)


def _insert_workflow_output_memory(workflow_id: int, output_payload: dict[str, Any]) -> None:
    _STORE.outputs[workflow_id] = deepcopy(output_payload)


def insert_workflow_output(workflow_id: int, output_payload: dict[str, Any]) -> None:
    """Persist structured workflow output."""
    try:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO workflow_outputs (
                        input_id, summary, action_items, priority, route_to, confidence, reasoning_short,
                        saved_minutes, processing_time_ms, payload
                    )
                    VALUES (%s, %s, %s::jsonb, %s, %s, %s, %s, %s, %s, %s::jsonb)
                    """,
                    (
                        workflow_id,
                        output_payload["summary"],
                        json.dumps(output_payload["action_items"]),
                        output_payload["priority"],
                        output_payload["route_to"],
                        output_payload.get("confidence"),
                        output_payload.get("reasoning_short"),
                        output_payload["saved_minutes"],
                        output_payload["processing_time_ms"],
                        json.dumps(output_payload),
                    ),
                )
            connection.commit()
        return
    except Exception:
        try:
            # Compatibility path for initial schema versions.
            with get_connection() as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        INSERT INTO workflow_outputs (input_id, output_type, payload)
                        VALUES (%s, %s, %s::jsonb)
                        """,
                        (workflow_id, "workflow_result", json.dumps(output_payload)),
                    )
                connection.commit()
            return
        except Exception:
            _insert_workflow_output_memory(workflow_id, output_payload)


def insert_workflow_event(correlation_id: str, event_type: str, event_payload: dict[str, Any]) -> None:
    """Persist workflow lifecycle events."""
    try:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO workflow_events (correlation_id, event_type, event_payload)
                    VALUES (%s, %s, %s::jsonb)
                    """,
                    (correlation_id, event_type, json.dumps(event_payload)),
                )
            connection.commit()
        return
    except Exception:
        _STORE.events.append(
            {
                "correlation_id": correlation_id,
                "event_type": event_type,
                "event_payload": deepcopy(event_payload),
                "created_at": _now_iso(),
            }
        )


def insert_workflow_error(
    correlation_id: str,
    error_code: str,
    error_message: str,
    error_context: dict[str, Any],
) -> None:
    """Persist workflow errors for troubleshooting."""
    try:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO workflow_errors (correlation_id, error_code, error_message, error_context)
                    VALUES (%s, %s, %s, %s::jsonb)
                    """,
                    (correlation_id, error_code, error_message, json.dumps(error_context)),
                )
            connection.commit()
        return
    except Exception:
        _STORE.errors.append(
            {
                "correlation_id": correlation_id,
                "error_code": error_code,
                "error_message": error_message,
                "error_context": deepcopy(error_context),
                "created_at": _now_iso(),
            }
        )


def insert_workflow_metric(
    correlation_id: str,
    metric_name: str,
    metric_value: float,
    metric_unit: str,
) -> None:
    """Persist per-workflow KPI datapoints."""
    try:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO workflow_metrics (correlation_id, metric_name, metric_value, metric_unit)
                    VALUES (%s, %s, %s, %s)
                    """,
                    (correlation_id, metric_name, metric_value, metric_unit),
                )
            connection.commit()
        return
    except Exception:
        try:
            # Compatibility path for initial schema versions without correlation_id.
            with get_connection() as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        INSERT INTO workflow_metrics (metric_name, metric_value, metric_unit)
                        VALUES (%s, %s, %s)
                        """,
                        (metric_name, metric_value, metric_unit),
                    )
                connection.commit()
            return
        except Exception:
            _STORE.metrics.append(
                {
                    "correlation_id": correlation_id,
                    "metric_name": metric_name,
                    "metric_value": metric_value,
                    "metric_unit": metric_unit,
                    "captured_at": _now_iso(),
                }
            )


def get_workflow_detail(workflow_id: int) -> dict[str, Any] | None:
    """Fetch workflow input and output by workflow ID."""
    try:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT
                        wi.id AS workflow_id,
                        wi.correlation_id::text AS correlation_id,
                        wi.source_type,
                        wi.source_system,
                        wi.submitted_by,
                        wi.priority AS priority_requested,
                        wi.content,
                        wi.tags,
                        wi.created_at,
                        wo.payload AS output_payload
                    FROM workflow_inputs wi
                    LEFT JOIN workflow_outputs wo ON wo.input_id = wi.id
                    WHERE wi.id = %s
                    """,
                    (workflow_id,),
                )
                row = cursor.fetchone()
        if row:
            return row
    except Exception:
        pass

    input_row = _STORE.inputs.get(workflow_id)
    if not input_row:
        return None
    return {
        "workflow_id": input_row["id"],
        "correlation_id": input_row["correlation_id"],
        "source_type": input_row["source_type"],
        "source_system": input_row["source_system"],
        "submitted_by": input_row["submitted_by"],
        "priority_requested": input_row["priority"],
        "content": input_row["content"],
        "tags": input_row["tags"],
        "created_at": input_row["created_at"],
        "output_payload": _STORE.outputs.get(workflow_id),
    }


def _coerce_float(value: Any) -> float:
    if value is None:
        return 0.0
    if isinstance(value, Decimal):
        return float(value)
    return float(value)


def get_metrics_summary() -> dict[str, Any]:
    """Aggregate KPI summary for API reporting."""
    try:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) AS total_inputs FROM workflow_inputs")
                total_inputs = int(cursor.fetchone()["total_inputs"])

                cursor.execute("SELECT COUNT(*) AS total_outputs FROM workflow_outputs")
                total_outputs = int(cursor.fetchone()["total_outputs"])

                cursor.execute(
                    """
                    SELECT AVG((payload->>'processing_time_ms')::numeric) AS avg_processing_time_ms,
                           COALESCE(SUM((payload->>'saved_minutes')::numeric), 0) AS total_saved_minutes
                    FROM workflow_outputs
                    """
                )
                agg_row = cursor.fetchone()

                route_counts = {route: 0 for route in ROUTES}
                cursor.execute(
                    """
                    SELECT payload->>'route_to' AS route_to, COUNT(*) AS count_per_route
                    FROM workflow_outputs
                    GROUP BY payload->>'route_to'
                    """
                )
                for row in cursor.fetchall():
                    route = row["route_to"]
                    if route in route_counts:
                        route_counts[route] = int(row["count_per_route"])
        success_rate = float(total_outputs / total_inputs) if total_inputs else 0.0
        return {
            "total_inputs": total_inputs,
            "success_rate": round(success_rate, 4),
            "avg_processing_time_ms": round(_coerce_float(agg_row["avg_processing_time_ms"]), 2),
            "route_counts": route_counts,
            "total_saved_minutes": int(_coerce_float(agg_row["total_saved_minutes"])),
        }
    except Exception:
        total_inputs = len(_STORE.inputs)
        total_outputs = len(_STORE.outputs)
        processing_times = [
            int(payload.get("processing_time_ms", 0)) for payload in _STORE.outputs.values()
        ]
        saved_minutes_list = [int(payload.get("saved_minutes", 0)) for payload in _STORE.outputs.values()]
        route_counts = {route: 0 for route in ROUTES}
        for payload in _STORE.outputs.values():
            route = payload.get("route_to")
            if route in route_counts:
                route_counts[route] += 1
        avg_processing = sum(processing_times) / len(processing_times) if processing_times else 0.0
        success_rate = float(total_outputs / total_inputs) if total_inputs else 0.0
        return {
            "total_inputs": total_inputs,
            "success_rate": round(success_rate, 4),
            "avg_processing_time_ms": round(avg_processing, 2),
            "route_counts": route_counts,
            "total_saved_minutes": int(sum(saved_minutes_list)),
        }
