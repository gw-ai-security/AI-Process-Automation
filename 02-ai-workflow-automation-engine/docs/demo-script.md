# Demo Script

## Objective

Demonstrate end-to-end operational intake automation with persistence, routing, and KPI tracking.

## Steps

1. Start stack:
   - `docker compose up --build`
2. Open API docs:
   - `http://localhost:8000/docs`
3. Send sample request:
   - `POST /intake` with `samples/support_case.json`
4. Show processed result:
   - includes summary, action items, priority, route, saved_minutes
5. Fetch persisted workflow:
   - `GET /workflow/{id}`
6. Show KPI aggregation:
   - `GET /metrics/summary`
7. Open n8n:
   - `http://localhost:5678`
8. Import `n8n/workflows/operational-intake-mvp.json` and run webhook test.
9. Show mock integration branches:
   - high -> `/mock/jira`
   - medium -> `/mock/slack`

## Demo Success Criteria

- structured output generated
- workflow record retrievable
- KPI metrics non-empty after sample runs
- at least two routing branches executed
