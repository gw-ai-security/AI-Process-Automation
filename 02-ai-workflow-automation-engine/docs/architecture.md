# Architecture

## Overview

The MVP is a single backend service with one orchestrated workflow:

1. intake request arrives via API or n8n webhook
2. payload is validated
3. LLM service returns strict JSON structure
4. route is resolved
5. input/output/events/errors/metrics are persisted
6. workflow result and KPIs are queryable

## Diagram

See `docs/architecture-diagram.mmd` for a Mermaid diagram source.

## Components

- FastAPI API layer: `app/api/`
- Processing orchestrator: `app/services/workflow_service.py`
- LLM adapter: `app/services/llm_service.py`
- Routing: `app/services/routing_service.py`
- KPI/ROI: `app/services/roi_service.py`
- Data access: `app/db/queries.py`
- PostgreSQL schema: `sql/001_init.sql`
- n8n workflow: `n8n/workflows/operational-intake-mvp.json`

## Data Contracts

Structured output fields:

- `summary`
- `action_items`
- `priority`
- `route_to`
- optional `confidence`
- optional `reasoning_short`

## Reliability Notes

- DB-first operations with in-memory fallback for local test execution
- health endpoint exposes application and DB connectivity status
