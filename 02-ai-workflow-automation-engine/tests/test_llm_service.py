import json

from app.schemas.intake import IntakeRequest
from app.services.llm_service import extract_structured_output, parse_llm_json


def test_parse_llm_json_enforces_required_shape() -> None:
    raw = json.dumps(
        {
            "summary": "Customer escalation about delayed onboarding.",
            "action_items": ["Contact legal", "Update customer"],
            "priority": "high",
            "route_to": "support",
            "confidence": 0.91,
            "reasoning_short": "Escalation language and customer impact detected.",
        }
    )
    parsed = parse_llm_json(raw)
    assert parsed.priority == "high"
    assert parsed.route_to == "support"
    assert parsed.action_items == ["Contact legal", "Update customer"]
    assert parsed.confidence == 0.91


def test_extract_structured_output_mock_mode_returns_valid_categories() -> None:
    payload = IntakeRequest(
        source_type="support_text",
        source_system="helpdesk",
        content="Urgent customer incident with repeated outage symptoms.",
        submitted_by="support.agent@example.com",
        tags=["incident", "customer"],
        priority="medium",
    )
    output = extract_structured_output(payload)
    assert output.priority in {"low", "medium", "high"}
    assert output.route_to in {"sales", "ops", "support", "product"}
    assert len(output.summary) >= 10
