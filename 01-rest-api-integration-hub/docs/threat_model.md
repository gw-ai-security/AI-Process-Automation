# Threat Model

## Für Nicht-IT (Kurz)
- Die wichtigsten Assets sind der Lead-Webhook, die Integrationsdatenbank und die Alerts, die Stakeholder über Fehler informieren.
- Angriffe könnten durch falsche Signaturen, Replay-Versuche oder ungesicherte DB-Zugänge passieren; wir setzen deshalb auf HMAC, Timestamp-Skew und DLQ-Tracking.
- Mock-Services, die Alerts schreiben, erlauben schnelle Demonstrationen ohne echte Drittsysteme und dienen gleichzeitig als Alarmquelle für Fehlerpfade.

## Für IT (Details)
- **Assets & Mitigation:**
  - *Webhook-Eingang:* geschützt durch `X-Timestamp` + `X-Signature` (HMAC-SHA256); Replay wird durch `WEBHOOK_MAX_SKEW_SECONDS` limitiert, fehlende/malformate Signaturen liefern HTTP 401/409.
  - *PostgreSQL & Runs:* `runs`, `audit_events`, `dlq` und `kpi_daily` befinden sich im Compose-Cluster; `email_hash`/`email_masked` verhindern Roh-PII, DLQ sammelt Fehler zur Nachbearbeitung.
  - *Mock CRM/Jira:* laufen in eigenen Containern (`mock-crm`, `mock-jira-confluence`) in der Compose-Umgebung; Alerts aus `alerts/` zeigen Fehler und dienen als Auslöser für Beobachtungslösungen.
- **Erkennung & Aktion:**
  - Exceptions beim DMZ-Call (z.?B. `mock-crm`-Timeout) landen im DLQ + Audit (`dlq_created`), außerdem schreibt n8n `alert`-Dateien und `scripts/smoke.sh` erzeugt reproduzierbare Fehlerfälle.
  - Dokumentation, Glossar und Maintenance Skill unterstützen, damit neue Services, Endpunkte oder Fehlerfälle stets datiert, versioniert und getestet bleiben.
