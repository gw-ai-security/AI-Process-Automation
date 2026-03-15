# n8n Workflow MVP

This directory contains an exportable MVP workflow:

- `n8n/workflows/operational-intake-mvp.json`

## Flow

1. Webhook trigger receives operational intake JSON.
2. HTTP Request sends payload to `POST /intake`.
3. `if priority == high` -> call `POST /mock/jira`.
4. else `if priority == medium` -> call `POST /mock/slack`.
5. else -> low-priority "store-only" path.
6. Final log node marks completion.

This satisfies the MVP requirement for two or more visible routing branches.
