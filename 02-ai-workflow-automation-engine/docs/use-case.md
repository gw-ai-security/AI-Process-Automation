# Use Case: Operational Intake Automation

## Input

Unstructured operational text from:

- meeting notes
- support cases
- onboarding handoffs
- issue reports

## Automated Output

For each intake, the system generates:

- concise summary
- action items
- priority (`low|medium|high`)
- route decision (`sales|ops|support|product`)
- estimated minutes saved

## Workflow

1. submit intake to `POST /intake`
2. system validates and processes text through LLM adapter
3. output is persisted and exposed via `GET /workflow/{id}`
4. KPI aggregates are exposed via `GET /metrics/summary`
5. n8n can branch high/medium/low to mock targets

## Why This Is Recruiter-Relevant

- demonstrates end-to-end backend design
- shows API + persistence + orchestration integration
- includes practical KPI instrumentation and documented limits
