from app.schemas.intake import IntakeRequest
from app.services.routing_service import resolve_route


def test_resolve_route_keeps_valid_llm_route() -> None:
    payload = IntakeRequest(
        source_type="meeting_note",
        source_system="ops-sync",
        content="Procurement blocker still open.",
        submitted_by="ops@example.com",
        tags=["ops"],
        priority="medium",
    )
    assert resolve_route(payload, "product") == "product"


def test_resolve_route_uses_tag_fallback_for_invalid_llm_route() -> None:
    payload = IntakeRequest(
        source_type="support_text",
        source_system="helpdesk",
        content="Customer ticket escalated.",
        submitted_by="support@example.com",
        tags=["support", "incident"],
        priority="high",
    )
    assert resolve_route(payload, "invalid-target") == "support"
