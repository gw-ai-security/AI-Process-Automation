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
4) run `bash scripts/smoke.sh` (Git Bash/WSL) to verify Happy + Error Paths and populate `alerts/`.

## Dokumentation & Testlinks
- Alle Dokumente (Übersicht, Architektur, Runbook, API Contracts, Audit/KPI, KPIs, Threat Model, Changelog, Glossar, Maintenance Skill) leben in `docs/README.md`.
- `scripts/sign_webhook.py` erzeugt `X-Timestamp` / `X-Signature`, die Curl-Tests (`scripts/curl_*.sh`) und `scripts/smoke.sh` nutzen, damit HMAC, Replay und Invalid-Payload aussagekräftig bleiben.
- `mock-crm`/`mock-jira-confluence` liefern die Demo-Targets, `alerts/` enthält JSON-Dateien pro Fehler, und `kpi_daily` sammelt Tagesmetriken (siehe `docs/kpis.md`).
