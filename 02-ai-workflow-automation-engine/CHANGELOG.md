# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [0.2.0] - 2026-03-06

### Added

- end-to-end processing in `POST /intake` with structured LLM output fields
- `GET /workflow/{id}` endpoint for persisted workflow retrieval
- mock integrations: `POST /mock/jira` and `POST /mock/slack`
- n8n export workflow `n8n/workflows/operational-intake-mvp.json`
- KPI aggregation for success rate, route distribution, processing time, and saved minutes
- tests for LLM service, routing, metrics, and workflow retrieval
- architecture diagram source and screenshot artifacts for demo use

### Changed

- upgraded schema and query layer from phase scaffolding to MVP persistence
- updated documentation set from Phase 1 baseline to MVP operating guide
- extended `docker-compose.yml` with n8n service

### Planned

- add authenticated deployment profile for non-local environments
- replace mock integrations with toggleable real connectors
- add background queue for high-volume ingestion

## [0.1.0] - 2026-03-06

### Added

- Phase 1 FastAPI scaffold with health, intake, and metrics endpoints
- PostgreSQL Docker Compose service and SQL bootstrap scripts
- Pydantic schemas for intake and metrics responses
- placeholder service and DB layers for later phases
- Pytest coverage for health and intake endpoints
- README and baseline documentation set
- agent manifests, skill definitions, and project skill mapping
- sample payloads and helper scripts for local demo/testing
