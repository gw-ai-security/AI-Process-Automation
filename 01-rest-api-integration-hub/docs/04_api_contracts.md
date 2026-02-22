# API-Verträge

## Für Nicht-IT (Kurz)
- Zwei Endpunkte existieren: `/health` zur Überwachung und `/webhook/lead` zum Einreichen von Leads.
- Für `/webhook/lead` ist ein eindeutiger `X-Idempotency-Key` erforderlich, um Doppelerfassungen zu verhindern.
- Antworten liefern jeweils den Status (`ok`, `accepted`, `duplicate`) samt zugehöriger Run-ID und können daher einfach in Automatisierungen ausgewertet werden.

## Für IT (Details)
- Der FastAPI-Processor bietet unter Port 8000 zwei definierte Endpunkte: `GET /health` für automatische Checks und `POST /webhook/lead` für Lead-Intake aus n8n oder anderen Systemen.
- Alle Anfragen werden in PostgreSQL protokolliert, erstellen Runs/Audit-Events und bedienen Idempotenz über eine Unique-Constraint-Abfrage vor dem Insert.
- Fehlende Header (z. B. X-Idempotency-Key) liefern eine HTTP 400-Antwort mit Klartext-Fehlermeldung; erfolgreiche Calls liefern HTTP 200 mit JSON.

## Endpunkt: GET /health
- **Zweck:** sagt `status: ok`, schreibt ein Audit-Event `health_check` in `audit_events`.
- **Header:** keine.
- **Antwort:** `{"status": "ok"}` (HTTP 200).  
- **Audit:** `actor: system`, `payload` enthält `check` und Zeitstempel (siehe `processor/app/main.py`).

## Endpunkt: POST /webhook/lead
- **Zweck:** neuer Lead-Run, mit Idempotenz, Audit-Eintrag und Status `accepted`.
- **Headers:**
  - `X-Idempotency-Key` (Pflicht) – eindeutiger Wert zum Schutz vor Doppelerfassung.
  - `X-Source` (optional, Standard `unknown`) – erlaubt die Klassifikation der Herkunft.
  - `X-Fail-After-Accept` (optional, Testmodus) – bei Wert `1` wird unmittelbar nach `runs`/`audit_events` ein RuntimeError ausgelöst, damit DLQ/Audit-Pfade und Fehlerantworten verifiziert werden können.
  - `X-Timestamp` (Pflicht) – Unix Sekunden des Bodys, wird gegen `WEBHOOK_MAX_SKEW_SECONDS` geprüft.
  - `X-Signature` (Pflicht) – `sha256=<hex>` aus `timestamp + raw-body`, abhängig vom `WEBHOOK_HMAC_SECRET`.
- **JSON-Payload-Felder:**
  - `email` (z. B. `max@example.com`)
  - `name` (Name des Leads)
  - `note` (optional, z. B. `Testlead`)
  - `idempotency_key` (optional im Payload, wird nicht direkt ausgewertet; der Header entscheidet)
- **Hinweis:** Der Processor sanitized Payloads, schreibt nur `email_masked`/`email_hash` in `runs`, `audit_events` und `dlq`.
- **Antwortbeispiele:**
  - **Erster Aufruf:** `200 {"status":"accepted","run_id":"..."}`
  - **Duplikat:** `200 {"status":"duplicate","run_id":"...","existing_status":"accepted"}`
  - **Fehlender Header:** HTTP 400 mit `{detail: "Missing X-Idempotency-Key header"}`
  - **Simulierter Downstream-Failure:** HTTP 500 mit `{"detail":"Processing failed; written to DLQ"}` nachdem Header `X-Fail-After-Accept: 1` gesendet wurde.
  - **Falsche Signatur / zu alter Timestamp:** HTTP 401 bei fehlerhaftem HMAC, HTTP 409 bei Timestamp-Skew über `WEBHOOK_MAX_SKEW_SECONDS`.

## Idempotenzregeln
- Vor dem Einfügen prüft der Processor, ob ein `runs`-Eintrag mit dem gleichen `idempotency_key` existiert; das verhindert doppelte Inserts.
- Die Datenbank erzwingt Idempotenz per Unique-Index `runs_idempotency_key_uq` auf `idempotency_key`.
- Status und Run-ID werden bei Duplikaten wiederverwendet; es erfolgt kein neuer Audit-Eintrag für `lead_received`.
- Der Failure-Header `X-Fail-After-Accept` löst beim Wert `1` einen kontrollierten RuntimeError aus. Die Antwort gibt HTTP 500 zurück und verweist im Changelog auf den DLQ-Eintrag, der `runs.status` optional auf `failed` setzt.

## Security & Signature Flow
- **Für Nicht-IT:** Webhooks ohne gültige Uhrzeit oder Signatur werden abgewiesen; nur korrekt signierte Leads gelangen weiter und werden maskiert protokolliert.
- **Für IT:** Processor berechnet `signature = "sha256=" + hmac(secret, f"{timestamp}.{rawBody}")` mit `WEBHOOK_HMAC_SECRET`. `X-Timestamp` wird gegen `WEBHOOK_MAX_SKEW_SECONDS` geprüft (409), `X-Signature` wird über `hmac.compare_digest` validiert (401). Erfolgreiche Payloads werden an `mock-crm` weitergegeben und in `mock-jira-confluence` / `alerts/` festgehalten.
