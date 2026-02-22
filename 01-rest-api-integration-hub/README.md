# REST-API Integration Hub (Docker + n8n + FastAPI + Postgres)

## Goal
Local, reproducible integration hub: signed webhook lead intake -> validate/transform -> mock CRM upsert -> mock Jira/Confluence payload logging, with audit/DLQ/KPIs.

## Dokumentation
- Die modulare Dokumentation (Overview, Architektur, Runbook, API-Verträge, Audit/KPI, Glossar, Maintenance Skill) befindet sich in `docs/README.md`.
- Für Änderungen an Endpunkten, Services oder Tabellen gilt die Wartungsroutine in `docs/DOCS_MAINTENANCE_SKILL.md`.

## Quickstart (later)
1) cp .env.example .env
2) docker compose up -d --build
3) open http://localhost:5678