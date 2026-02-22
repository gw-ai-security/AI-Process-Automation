# Release Candidate Checkliste

## Für Nicht-IT (Kurz)
- Die Compose-Services (`n8n`, `processor`, `postgres`, `mock-crm`, `mock-jira-confluence`) starten zusammen mit greifbaren Alerts in `alerts/`.
- Smoke-Tests (`scripts/smoke.sh`) demonstrieren Happy-Path + Error-Path und erzeugen Testdaten/Audit sowie KPI-Einträge.
- Documentation, Glossar, Threat Model und Changelog sind synchron zur Umsetzung und erklären die KPIs sowie DLQ-Logik.

## Für IT (Details)
1. `docker compose up -d --build` startet alle Container; `docker compose ps` zeigt gesunde Dienste, `processor` antwortet auf `/health`.
2. `scripts/sign_webhook.py` + `scripts/curl_valid.sh` erzeugen korrekte `X-Timestamp`/`X-Signature`; `curl_bad_sig.sh`, `curl_replay.sh`, `curl_invalid_payload.sh` erzwingen erwartete Fehlercodes.
3. `mock-crm` antwortet auf `/leads/upsert`, der Processor schreibt `crm_upserted` + sanitized Audit, `mock-jira-confluence` legt Dateien unter `alerts/` ab.
4. `Db/schema.sql` und `processor/app/main.py` verarbeiten `runs(email_hash/email_masked)`, `audit_events`, `dlq`, `kpi_daily`; SQL-Queries (`docs/kpis.md`, `docs/05_audit_kpi.md`) prüfen die Zahlen.
5. Sicherheits-Checks: `WEBHOOK_HMAC_SECRET` gesetzt, `WEBHOOK_MAX_SKEW_SECONDS` definiert, `X-Fail-After-Accept` simuliert DLQ + Audit + failure response.
6. Dokumentations-Check: `docs/README.md` verlinkt alle Kapitel, `docs/DOCS_MAINTENANCE_SKILL.md` enthält die Update-Checkliste, Glossar ist konsistent, Changelog erweitert.
