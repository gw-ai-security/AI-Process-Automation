# How to use

## 1. Start the stack

```bash
cp .env.example .env
docker compose up --build
```

## 2. Verify health

```bash
curl http://localhost:8000/health
```

Expected: `status=ok` and `database_connected=true` when DB is up.

## 3. Process intake

```bash
curl -X POST http://localhost:8000/intake \
  -H "Content-Type: application/json" \
  -d @samples/support_case.json
```

Output contains:

- `workflow_id`
- `summary`
- `action_items`
- `priority`
- `route_to`
- `saved_minutes`

## 4. Fetch workflow details

```bash
curl http://localhost:8000/workflow/1
```

## 5. Read KPI summary

```bash
curl http://localhost:8000/metrics/summary
```

## 6. Run tests

```bash
pytest
```

## 7. n8n orchestration demo

1. Open `http://localhost:5678`.
2. Import `n8n/workflows/operational-intake-mvp.json`.
3. Trigger webhook with a sample payload.
4. Observe high/medium/low branches to mock endpoints.
