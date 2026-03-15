# Intake Validation Skill

## Purpose

Define how intake payload contracts should be created and maintained.

## Responsibilities

- keep request validation explicit
- normalize fields safely
- preserve future extension points without adding premature complexity

## Rules

- validate source type, content length, and user-provided metadata
- prefer deterministic normalization over fuzzy inference
- keep error handling transparent
- do not add LLM-based validation in Phase 1

## Repo Touchpoints

- `app/schemas/intake.py`
- `app/api/routes_ingest.py`
- `tests/test_ingest.py`
