from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_endpoint_returns_status_and_timestamp() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    payload = response.json()

    assert payload["status"] == "ok"
    assert "timestamp" in payload
    assert "database_connected" in payload
