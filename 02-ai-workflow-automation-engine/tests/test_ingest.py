from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_intake_endpoint_processes_workflow_payload() -> None:
    response = client.post(
        "/intake",
        json={
            "source_type": "meeting_note",
            "source_system": "ops-handoff",
            "content": "The onboarding task is blocked until procurement completes approval.",
            "submitted_by": "ops.team@example.com",
            "tags": ["Onboarding", " Approval "],
            "priority": "high",
        },
    )

    assert response.status_code == 200

    payload = response.json()
    assert payload["status"] == "accepted"
    assert payload["message"] == "Workflow intake processed successfully."
    assert payload["normalized_payload"]["tags"] == ["onboarding", "approval"]
    assert payload["priority"] in {"low", "medium", "high"}
    assert payload["route_to"] in {"sales", "ops", "support", "product"}
    assert payload["workflow_id"] >= 1
    assert payload["saved_minutes"] >= 0
    assert payload["processing_time_ms"] >= 0
    assert payload["correlation_id"]

    workflow_response = client.get(f"/workflow/{payload['workflow_id']}")
    assert workflow_response.status_code == 200
    workflow_payload = workflow_response.json()
    assert workflow_payload["workflow_id"] == payload["workflow_id"]
    assert workflow_payload["output_payload"]["route_to"] == payload["route_to"]
