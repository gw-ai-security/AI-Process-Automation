# Prompt Design

## Objective

Force stable structured output for downstream routing and persistence.

## Prompt Contract

The LLM must return JSON with:

- `summary`
- `action_items`
- `priority`
- `route_to`
- optional `confidence`
- optional `reasoning_short`

## Stability Controls

- system message requires JSON-only output
- response format uses `json_object` in OpenAI-compatible mode
- parser normalizes invalid category values to safe defaults

## Modes

- `LLM_MODE=mock`: deterministic classifier for local and CI-safe runs
- `LLM_MODE=openai`: real API call with OpenAI-compatible endpoint

## Risks

- model drift can affect category consistency
- strict parsing and fallback normalization reduce runtime breakage
