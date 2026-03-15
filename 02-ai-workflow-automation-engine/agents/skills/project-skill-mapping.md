# Project Skill Mapping

## FastAPI Basics

- Skill name: FastAPI basics
- What is learned: how to create an app entrypoint, register routers, and expose OpenAPI-ready endpoints
- Where it appears in the repo: `app/main.py`, `app/api/routes_health.py`, `app/api/routes_ingest.py`, `app/api/routes_metrics.py`
- Why it matters in real jobs: backend engineers routinely need to ship clear HTTP services with maintainable route boundaries

## API Route Design

- Skill name: API route design
- What is learned: how to separate health, intake, and reporting endpoints by responsibility
- Where it appears in the repo: `app/api/`
- Why it matters in real jobs: clean routing reduces accidental coupling and makes services easier to extend and test

## Docker Compose Fundamentals

- Skill name: Docker Compose fundamentals
- What is learned: how to orchestrate an app container and a database service with shared configuration
- Where it appears in the repo: `docker-compose.yml`, `Makefile`, `.env.example`
- Why it matters in real jobs: local reproducibility is critical for onboarding, demos, and CI alignment

## PostgreSQL Service Orchestration

- Skill name: PostgreSQL service orchestration
- What is learned: how to bootstrap a DB with schema scripts and connect it through environment configuration
- Where it appears in the repo: `docker-compose.yml`, `sql/001_init.sql`, `sql/002_seed.sql`, `app/db/connection.py`
- Why it matters in real jobs: most backend systems rely on stable database startup and schema management

## Request Validation With Pydantic

- Skill name: request validation with Pydantic
- What is learned: how to define typed payload contracts, normalize inputs, and keep APIs predictable
- Where it appears in the repo: `app/schemas/intake.py`, `app/schemas/metrics.py`
- Why it matters in real jobs: validation protects downstream systems and improves API reliability

## Project Documentation Discipline

- Skill name: project documentation discipline
- What is learned: how to document architecture, scope, risks, and delivery boundaries without bloating the implementation
- Where it appears in the repo: `README.md`, `docs/`, `agents/README.md`
- Why it matters in real jobs: engineering work is judged on clarity and maintainability, not only code

## Architecture Thinking

- Skill name: architecture thinking
- What is learned: how to define service boundaries and extension paths before adding advanced features
- Where it appears in the repo: `docs/architecture.md`, `app/services/`, `app/db/`
- Why it matters in real jobs: strong decomposition reduces rewrite risk as systems grow

## Phase-Based Delivery Discipline

- Skill name: phase-based delivery discipline
- What is learned: how to ship a narrow MVP while documenting later work without implementing it prematurely
- Where it appears in the repo: `docs/phase-1.md`, `README.md`, `CHANGELOG.md`
- Why it matters in real jobs: delivery discipline keeps teams focused on business value and reduces scope creep

## Changelog Hygiene

- Skill name: changelog hygiene
- What is learned: how to communicate project evolution in a release-oriented format
- Where it appears in the repo: `CHANGELOG.md`, `agents/skills/changelog-discipline.md`
- Why it matters in real jobs: stakeholders need a readable record of what changed and what is planned next

## System Decomposition For Future Automation

- Skill name: system decomposition for future automation and AI workflows
- What is learned: how to reserve clear locations for routing, ROI, LLM output, and workflow orchestration without building them too early
- Where it appears in the repo: `app/services/`, `app/schemas/llm_output.py`, `n8n/`, `docs/prompt-design.md`
- Why it matters in real jobs: scalable systems grow from clear boundaries, not from monolithic prototype code
