# Projektüberblick

## Für Nicht-IT (Kurz)
- Das Modul bündelt Lead-Intake über signierte Webhooks, prüft auf Duplikate und dokumentiert jeden Schritt in der Datenbank.
- Der lokale Stack (Docker Compose, n8n, FastAPI, PostgreSQL) erlaubt schnelles Testen und Audit-Reporting unabhängig von der Zielumgebung.
- Die Dokumentation erklärt Business-Ziele, technische Scope-Bestandteile und führt direkt zu Architektur-, Setup- und API-Referenzen.
- HMAC-Signaturprüfungen, Mock-CRM/Jira-Logger sowie KPI- und Alert-Dateien machen das Projekt vorführbereit für Stakeholder.

## Für IT (Details)
- Geschäftlich dient das Modul als verlässlicher Gatekeeper, der Leads zunächst per n8n-Workflow einsammelt, eine Quittung ausstellt und dann an einen Processor weiterleitet, der sowohl Fehler über DLQ/Status abbildet als auch KPI/Tagesmetriken liefert.
- Technisch besteht der Scope aus drei Containern (n8n:5678, Processor:8000, PostgreSQL:5432) innerhalb eines Docker-Compose-Netzwerks, wobei n8n den `/webhook/lead`-Endpoint des FastAPI-Processors aufruft und dieser die Laufzeitdaten in den Tabellen `runs`, `audit_events`, `dlq` und `kpi_daily` persistiert.
- Außerhalb des Scopes bleiben CRM-/Jira-Integrationen, externe Queueing-Systeme und produktive Cloud-Versionen; die aktuelle Implementation bleibt auf lokale Entwicklung und Audit-Beobachtung beschränkt.
- Die erweiterten Komponenten bestehen aus einem signaturvalidierenden FastAPI-Processor (`WEBHOOK_HMAC_SECRET`, `WEBHOOK_MAX_SKEW_SECONDS`), einem Mock-CRM-Upsert-Service, einem Mock-Jira/Confluence-Logger plus Alert-Dateien, sowie `scripts/`-Hilfen für curl-Tests und KPI-Checks.
- Die Security-Hygiene umfasst HMAC + Timestamp + Replay-Grenzen, PII-Hashing/Masking (`email_hash` / `email_masked`), DLQ Logging und die neue `docs/kpis.md` für Business-Metriken.

### Geltungsbereich
#### In Scope
- Leadaufnahme über den FastAPI-Endpoint `/webhook/lead` und Speicherung von Run-Status, Audit-Events sowie KPI/Audit-Tabellen in PostgreSQL.
- Lokales Workflow-Design mit n8n, das die Webhook-URL des Processors verwendet und bei Bedarf aus erstellten Workflows (workflow-Dateien) geladen wird.
- Dokumentation der kritischen API-Verträge, der Datenbankstruktur sowie der Setup-Schritte inklusive Troubleshooting und Glossar.
- Mock CRM + Mock Jira/Confluence Logger mit Alert-Dateien (`alerts/`), Plus `scripts/*` für Valid-, Invalid-, Replay- und Smoke-Tests.
- KPI-Metriken, einschließlich `kpi_daily` und `docs/kpis.md`, die Erfolg, Latency, DLQ-Rate und „saved minutes“ erklären.

#### Out of Scope
- Produktive Backend-Anbindungen (CRM, Jira, Confluence, Payment) außerhalb der lokalen Mock-Porteinstellungen.
- Automatische Verarbeitung über Cloud-Queueing oder geclusterte PostgreSQL-Systeme.
- Benutzeroberflächen außerhalb von n8n und der bestehenden FastAPI-Endpunkte (keine eigene UI).
