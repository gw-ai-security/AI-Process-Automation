import json
from pathlib import Path


def test_n8n_workflow_contains_required_routing_branches() -> None:
    workflow_path = Path("n8n/workflows/operational-intake-mvp.json")
    assert workflow_path.exists()

    workflow = json.loads(workflow_path.read_text(encoding="utf-8"))
    node_names = {node["name"] for node in workflow["nodes"]}

    assert "Webhook Trigger" in node_names
    assert "Call FastAPI Intake" in node_names
    assert "Mock Jira" in node_names
    assert "Mock Slack" in node_names
    assert "Low Priority Store Only" in node_names
