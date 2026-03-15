from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def _post_payload(content: str) -> None:
    response = client.post(
        "/intake",
        json={
            "source_type": "meeting_note",
            "source_system": "ops-sync",
            "content": content,
            "submitted_by": "ops.team@example.com",
            "tags": ["ops"],
            "priority": "medium",
        },
    )
    assert response.status_code == 200


def test_metrics_summary_returns_aggregated_values() -> None:
    _post_payload("Urgent customer incident requires immediate follow-up.")
    _post_payload("Feature planning note for next release refinement.")

    metrics = client.get("/metrics/summary")
    assert metrics.status_code == 200
    data = metrics.json()

    assert data["total_inputs"] == 2
    assert data["success_rate"] >= 0
    assert isinstance(data["route_counts"], dict)
    assert data["total_saved_minutes"] >= 0
