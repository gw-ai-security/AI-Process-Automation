# Audit, DLQ & KPI

## Für Nicht-IT (Kurz)
- Jede Lead-Annahme führt zu einem Run, einem Audit-Eintrag und ggf. einem DLQ-Eintrag, sodass das Business jederzeit nachvollziehen kann, was passiert ist.
- KPI-Zahlen (empfangene, verarbeitete, fehlgeschlagene Leads, offene DLQs) werden pro Tag gespeichert und können für Reporting genutzt werden.
- Die Dokumentation zeigt, wie die Tabellen aufgebaut sind und welche Abfragen typischerweise genutzt werden.

## Für IT (Details)
- Die Datenbank hält vier zentrale Entitäten: `runs` für den Lead-Lifecycle, `audit_events` zur Rückverfolgung jeder Aktion, `dlq` für problematische Payloads und `kpi_daily` für aggregierte Tageskennzahlen.
- Events wie `lead_received` (beim Webhook) und `health_check` (bei GET /health) füllen `audit_events`, während DLQ- und KPI-Tabellen manuell oder über zukünftige Worker gepflegt werden können.
- Dieses Kapitel liefert Tabellenbeschreibungen, Beispiel-SQL und Hinweise, wie sich DLQ und KPI in zukünftige Prozesse integrieren lassen.

## Tabellen im Überblick
- **runs** – `run_id` (PK, UUID), `idempotency_key`, `source`, `received_at`, `status` (`accepted|processed|failed`), `error_code`, `error_message`. Der Run-Status bildet ab, ob der Lead verarbeitet, noch ausstehend oder fehlgeschlagen ist.
- **audit_events** – `event_id`, `run_id` (FK), `event_time`, `event_type` (z. B. `lead_received`, `health_check`), `actor`, `payload` (JSON). Jeder Health-Check und Lead-Intake schreibt hier ein JSON-Objekt.
- **dlq** – `dlq_id`, `run_id`, `reason`, `payload`, `retry_count`, `next_retry_at`, `status` (`open|retrying|resolved|dead`). Dient zum Sammeln von Payloads, die nicht verarbeitet werden konnten.
- **kpi_daily** – `day`, `received_count`, `processed_count`, `failed_count`, `dlq_open_count`, `avg_processing_ms`. Aggregierte Tageswerte für Reporting und SLA-Messung.

## Beispiel-SQL
```sql
-- Runs nach Status
SELECT run_id, status, received_at FROM runs ORDER BY received_at DESC LIMIT 20;

-- Audit-Events zu einem Lead
SELECT event_type, payload FROM audit_events WHERE run_id = '<run_id>' ORDER BY event_time;

-- Offene DLQ-Einträge
SELECT dlq_id, reason, retry_count FROM dlq WHERE status = 'open';

-- KPI für die letzten 7 Tage
SELECT * FROM kpi_daily ORDER BY day DESC LIMIT 7;
```
Diese Abfragen lassen sich in BI-Tools oder Dashboards einbetten und bilden die Grundlage für SLA-Indikatoren.

## Nutzung von DLQ & KPI
- **DLQ:** Nutzt den `reason`-Text und `retry_count`, um Fehlermeldungen zu sammeln, die sich später manuell oder programmatisch bearbeiten lassen. Der Status wechselt von `open` zu `retrying`/`resolved`/`dead`, sobald Nachbearbeitung erfolgt.
- **KPI:** `kpi_daily` kann automatisiert aktualisiert werden (z. B. durch Cron-Jobs oder nach dem Process-Finish) und dokumentiert, wie viele Leads gelesen, verarbeitet oder als Fehler markiert wurden.
- Beide Tabellen bleiben bewusst offen für zukünftige Workers, die das Monitoring oder Fehlerhandling übernehmen; für den aktuellen Stand genügt das manuelle Befüllen über SQL.

## Ereignistypen
- **lead_received:** Wird direkt nach einer erfolgreichen Webhook-Annahme geschrieben, enthält `payload` mit Zeitstempel, `body`-Inhalt und `source`.
- **health_check:** Jeder GET /health läutet ein Event ein, typischerweise mit `actor: system` und der JSON-Payload `{check: 'health', at: ...}`.
