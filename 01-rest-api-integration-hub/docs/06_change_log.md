# Änderungslog

## Für Nicht-IT (Kurz)
- Das Modul dokumentiert den Start der Integrationszentrale (Docker-Compose-Stack, FastAPI-Processor, Schema, Audit) für nachvollziehbare Leads.
- Jeder Log-Eintrag enthält Geschäfts- und Technikbegründung sowie einen Hinweis, wenn die Information aus der aktuellen Chat-Session stammt.

## Für IT (Details)
- Das Changelog wird bei jeder sinnvollen Änderung (neues Service, Endpoint, Schema, Workflow, bekanntes Problem) aktualisiert. Die Einträge enthalten jeweils Business-Motivation, technische Umsetzung und die Quelle der Information.

### Historische Einträge
- **2026-02-22:** Docker Compose-Baseline (n8n + PostgreSQL + Processor) eingeführt (aus Chat-Session). Business: Sinnvolle lokale Testumgebung für interne Lead-Workflows. Technik: Compose startet n8n:5678, PostgreSQL:5432 und den FastAPI-Processor auf 8000 inklusive Volumes/Healthchecks.
- **2026-02-22:** Processor-Container + uvicorn/psycopg dependencies validiert (aus Chat-Session). Business: Sicherstellung, dass verarbeitende Logik stabil läuft und Leads gemeldet werden können. Technik: Neben FastAPI ist uvicorn als ASGI-Server und `psycopg[binary]` für DB-Verbindungen festgelegt.
- **2026-02-22:** Datenbankschema angewendet (aus Chat-Session). Business: Audit- und KPI-Anforderungen abgedeckt, um Status, Fehler und Metriken nachzuverfolgen. Technik: Tabellen `runs`, `audit_events`, `dlq` und `kpi_daily` mit Constraints, Indizes und Statuswerten erstellt.
- **2026-02-22:** Lead-Flow mit n8n und Audit-Logging beschrieben (aus Chat-Session). Business: Nachweis des End-to-End-Flows für Stakeholder. Technik: `/webhook/lead` schreibt `runs` und `audit_events`, verhindert Duplikate über `idempotency_key` und liefert die erwarteten JSON-Antworten.
