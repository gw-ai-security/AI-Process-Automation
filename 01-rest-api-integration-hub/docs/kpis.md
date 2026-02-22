# KPI-Definitionen & Messkonzept

## Für Nicht-IT (Kurz)
- Die wichtigsten KPIs („Success Rate“, „Manual Rework Rate“, „Saved Minutes“) zeigen, ob Leads automatisiert ankommen bzw. wie viele manuell nachgearbeitet werden müssen.
- `kpi_daily` führt die Tageszahlen (Empfangen, Verarbeitet, Fehler) in einer Tabelle zusammen und erlaubt schnelle Reporting-Screens.
- Alert-Dateien aus `alerts/` und das `scripts/smoke.sh`-Szenario liefern Beispiele für Erfolg/Fehler und machen Abweichungen sichtbar.

## Für IT (Details)
- Die Tabelle `kpi_daily` (Spalten `day`, `received_count`, `processed_count`, `failed_count`, `dlq_open_count`, `avg_processing_ms`) wird nach jedem Lauf aktualisiert oder kann per SQL/Cron nachgezogen werden (z.?B. `INSERT ... ON CONFLICT (day)`).
- Die KPI-Metriken im Überblick:
  - `success_rate = processed_count / nullif(received_count, 0)` (Watch out for Division-by-Zero)
  - `manual_rework_rate = failed_count / nullif(received_count, 0)` (Proxy für DLQ-Aufwand)
  - `saved_minutes = processed_count * 2` (konservative Annahme: 2 Minuten pro Lead gegenüber manueller Erfassung)
  - `avg_processing_ms` aus den Run-Latenzen (muss je nach Implementierung nachträglich gefüllt werden)
- `scripts/smoke.sh` aktualisiert `kpi_daily`, sodass nach dem Testlauf die Tageszeilen sichtbar werden; die Alerts aus `mock-jira-confluence` zeigen `alert=true` bei Fehlern.
- Beispiel-SQL zur Validierung:
  ```sql
  SELECT day, received_count, processed_count, failed_count, dlq_open_count FROM kpi_daily ORDER BY day DESC LIMIT 7;
  SELECT (processed_count::float / NULLIF(received_count,0)) AS success_rate FROM kpi_daily WHERE day = CURRENT_DATE;
  SELECT saved_minutes FROM kpi_daily WHERE day = CURRENT_DATE;
  ```
- Die KPI-Dokumentation in `docs/05_audit_kpi.md` zeigt, wie diese Tabellen in das Audit-Reporting eingebettet sind und wie `dlq_created`/`crm_upserted` Events die Numerik füttern.
