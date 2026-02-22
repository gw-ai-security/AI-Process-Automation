# Glossar

## Audit Trail
- **Definition (Nicht‑IT):** Chronologische Aufzeichnung, wer wann was mit einem Lead gemacht hat.
- **Technische Notiz:** In `audit_events` (Spalten `event_type`, `actor`, `payload`) werden `lead_received` und `health_check` dokumentiert.
- **Vorkommen:** `docs/02_architecture.md`, `docs/05_audit_kpi.md`

## Container
- **Definition (Nicht‑IT):** Abgeschlossene Laufzeit-Umgebung, die einen Dienst mit allen Abhängigkeiten bündelt.
- **Technische Notiz:** Die Services `n8n`, `processor` und `postgres` laufen jeweils in eigenen Docker-Containern mit definierten Ports.
- **Vorkommen:** `docs/02_architecture.md`, `docs/03_setup_runbook.md`

## DLQ
- **Definition (Nicht‑IT):** Sammelplatz für Leads, die nicht sofort verarbeitet werden konnten.
- **Technische Notiz:** Tabelle `dlq` mit `reason`, `payload`, `retry_count` und Statuswerten `open|retrying|resolved|dead`.
- **Vorkommen:** `docs/02_architecture.md`, `docs/05_audit_kpi.md`

## Docker Compose
- **Definition (Nicht‑IT):** Werkzeug zum gleichzeitigen Start mehrerer Container.
- **Technische Notiz:** `docker-compose.yml` startet `postgres`, `n8n` und `processor` mit Volumes, Ports und Healthchecks.
- **Vorkommen:** `docs/01_overview.md`, `docs/03_setup_runbook.md`

## Endpoint
- **Definition (Nicht‑IT):** Adresse, an die Systeme Daten schicken oder abrufen.
- **Technische Notiz:** FastAPI stellt `/health` und `/webhook/lead` bereit; beide liefern JSON-Antworten.
- **Vorkommen:** `docs/04_api_contracts.md`

## FastAPI
- **Definition (Nicht‑IT):** Framework für moderne Web-APIs, das Python nutzt.
- **Technische Notiz:** `processor/app/main.py` definiert die Endpunkte und integriert Header-/JSON-Prüfungen sowie DB-Zugriffe via `psycopg`.
- **Vorkommen:** `docs/02_architecture.md`, `docs/04_api_contracts.md`

## HTTP Header
- **Definition (Nicht‑IT):** Metadaten im HTTP-Request, z. B. wer der Absender ist.
- **Technische Notiz:** Der Processor erwartet `X-Idempotency-Key` (Pflicht) und `X-Source` (optional).
- **Vorkommen:** `docs/04_api_contracts.md`

## Idempotency
- **Definition (Nicht‑IT):** Mehrmaliges Senden derselben Nachricht führt nicht zu doppelten Ergebnissen.
- **Technische Notiz:** Unique-Index `runs_idempotency_key_uq` plus Prüfung vor Insert verhindern doppelte `run_id`-Einträge.
- **Vorkommen:** `docs/02_architecture.md`, `docs/04_api_contracts.md`

## JSON Payload
- **Definition (Nicht‑IT):** Strukturierte Daten im JSON-Format, die Inhalte wie Name oder E-Mail enthalten.
- **Technische Notiz:** `/webhook/lead` erwarten Felder wie `email`, `name`, `note`, mögliche `idempotency_key`-Angabe im Body.
- **Vorkommen:** `docs/04_api_contracts.md`

## n8n
- **Definition (Nicht‑IT):** Low-Code-Workflow-Plattform für Automatisierungen.
- **Technische Notiz:** Nutzt Port 5678, lädt Workflows aus `n8n/workflows` und ruft `http://processor:8000/webhook/lead` auf.
- **Vorkommen:** `docs/01_overview.md`, `docs/02_architecture.md`, `docs/03_setup_runbook.md`

## PostgreSQL
- **Definition (Nicht‑IT):** Datenbank zum Speichern von Runs, Audits, DLQ- und KPI-Daten.
- **Technische Notiz:** Version 16, läuft im Container `postgres`, benötigt `DATABASE_URL=postgresql://...` für `psycopg`.
- **Vorkommen:** `docs/03_setup_runbook.md`, `docs/05_audit_kpi.md`

## Run
- **Definition (Nicht‑IT):** Eine durchgeführte Lead-Verarbeitung vom Eingang bis zum Audit.
- **Technische Notiz:** Tabelle `runs` enthält `run_id`, `received_at`, `status` sowie Fehlerdetails.
- **Vorkommen:** `docs/02_architecture.md`, `docs/05_audit_kpi.md`

## Status
- **Definition (Nicht‑IT):** Zeigt an, ob ein Lead verarbeitet, ausstehend oder fehlgeschlagen ist.
- **Technische Notiz:** `runs.status` erlaubt nur die Werte `accepted`, `processed`, `failed` via Check-Constraint.
- **Vorkommen:** `docs/02_architecture.md`, `docs/05_audit_kpi.md`

## Uvicorn
- **Definition (Nicht‑IT):** Laufzeitumgebung, die FastAPI-Anwendungen bereitstellt.
- **Technische Notiz:** `uvicorn==0.30.6` ist in `processor/requirements.txt` aufgeführt und dient als ASGI-Server.
- **Vorkommen:** `docs/03_setup_runbook.md`, `docs/02_architecture.md`

## Webhook
- **Definition (Nicht‑IT):** Automatisierter HTTP-Aufruf, der einen Lead auslöst.
- **Technische Notiz:** n8n sendet POSTs an `/webhook/lead` mit idempotenter Header/JSON-Kombination.
- **Vorkommen:** `docs/01_overview.md`, `docs/04_api_contracts.md`

## Workflow
- **Definition (Nicht‑IT):** Abfolge von Schritten zur Datenverarbeitung.
- **Technische Notiz:** In `n8n/workflows` liegen (derzeit keine) JSON-Definitionen, die bei Bedarf die Processor-URL kontaktieren.
- **Vorkommen:** `docs/01_overview.md`, `docs/03_setup_runbook.md`
