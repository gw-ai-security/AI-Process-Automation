"""Routing decision service for workflow output."""

from app.schemas.intake import IntakeRequest


VALID_ROUTES = {"sales", "ops", "support", "product"}


def resolve_route(payload: IntakeRequest, llm_route: str) -> str:
    """Resolve final route from LLM suggestion and input hints."""
    normalized_route = llm_route.strip().lower()
    if normalized_route in VALID_ROUTES:
        return normalized_route

    tags = {tag.lower() for tag in payload.tags}
    if {"customer", "support", "incident"} & tags:
        return "support"
    if {"lead", "deal", "crm"} & tags:
        return "sales"
    if {"bug", "feature", "release"} & tags:
        return "product"
    return "ops"
