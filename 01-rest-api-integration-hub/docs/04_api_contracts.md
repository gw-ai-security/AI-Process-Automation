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
- **JSON-Payload-Felder:**
  - `email` (z. B. `max@example.com`)
  - `name` (Name des Leads)
  - `note` (optional, z. B. `Testlead`)
  - `idempotency_key` (optional im Payload, wird nicht direkt ausgewertet; der Header entscheidet)
- **Antwortbeispiele:**
  - **Erster Aufruf:** `200 {"status":"accepted","run_id":"..."}`
  - **Duplikat:** `200 {"status":"duplicate","run_id":"...","existing_status":"accepted"}`
  - **Fehlender Header:** HTTP 400 mit `{detail: "Missing X-Idempotency-Key header"}`

## Idempotenzregeln
- Vor dem Einfügen prüft der Processor, ob ein `runs`-Eintrag mit dem gleichen `idempotency_key` existiert; das verhindert doppelte Inserts.
- Die Datenbank erzwingt Idempotenz per Unique-Index `runs_idempotency_key_uq` auf `idempotency_key`.
- Status und Run-ID werden bei Duplikaten wiederverwendet; es erfolgt kein neuer Audit-Eintrag für `lead_received`.
