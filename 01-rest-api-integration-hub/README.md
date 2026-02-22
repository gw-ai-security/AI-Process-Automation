# REST-API Integration Hub (Docker + n8n + FastAPI + Postgres)

## Goal
Local, reproducible integration hub: signed webhook lead intake -> validate/transform -> mock CRM upsert -> mock Jira/Confluence payload logging, with audit/DLQ/KPIs.

## Quickstart (later)
1) cp .env.example .env
2) docker compose up -d --build
3) open http://localhost:5678