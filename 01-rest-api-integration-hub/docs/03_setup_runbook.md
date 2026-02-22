# Setup-Runbook

## Für Nicht-IT (Kurz)
- Die Umgebung wird mit Docker Desktop via `docker compose up -d` gestartet und stellt n8n, Processor und PostgreSQL lokal bereit.
- Die Schritte umfassen Schema-Anwendung, Health-Check und Test-Webhook, damit Leads fälschungssicher angenommen werden.
- Gängige Stolperfallen (Docker-Engine, PowerShell-Redirects, fehlende Abhängigkeiten) sind dokumentiert, damit der Betrieb nicht ins Stocken gerät.

## Für IT (Details)
- Windows + Docker Desktop erlauben das schnelle Hochfahren eines Netzwerks mit `n8n:5678`, `processor:8000` und `postgres:5432`. Die `.env`-Datei (siehe `.env` bzw. `.env.example`) liefert die Zugangsdaten, den `DATABASE_URL`-String sowie Secrets für Webhooks und Mock-Ports.
- Das Runbook beschreibt den Start der Container, das Aufbringen der Schema-Datei (`db/schema.sql`), das Überprüfen des Health-Endpunkts und das Absenden eines Test-Lead-Webhooks inklusive Idempotenz-Headern.
- Troubleshooting-Abschnitte behandeln den typischen Fehler „Pipe-Fehler durch nicht laufenden Docker-Daemon“, PowerShell-Redirect-Limits bei Schema-Anwendung, fehlende `uvicorn`-Installationen und die korrekte psycopg-Verbindungszeichenfolge.

## Schritt-für-Schritt
1. **Umweltvariablen kopieren** – `cp .env.example .env` (oder `Copy-Item .env.example .env` in PowerShell) und bei Bedarf Secrets anpassen (`WEBHOOK_HMAC_SECRET`, `EMAIL_HASH_SALT`).  
2. **Container starten** – `docker compose up -d --build`.  
3. **Status prüfen** – `docker compose ps` zeigt, dass `postgres`, `n8n` und `processor` laufen.  
4. **Logs beobachten** – Beispiel: `docker compose logs -f processor` oder `docker compose logs n8n`.  
5. **Schema anwenden** – PowerShell unterstützt kein `<`, daher `Get-Content db/schema.sql | docker compose exec -T postgres psql -U integrationhub -d integrationhub`.  
6. **Health testen** – `Invoke-RestMethod http://localhost:8000/health` liefert `{"status":"ok"}`; zusätzlich schreibt der Endpoint `audit_events` vom Typ `health_check`.  
7. **Test-Webhook senden** (PowerShell):
   ```powershell
   $payload = @{email='max@example.com'; name='Max Mustermann'; note='Testlead'; idempotency_key='2026-02-22-test'} | ConvertTo-Json
   Invoke-RestMethod -Uri http://localhost:8000/webhook/lead -Method Post -Headers @{ 'X-Idempotency-Key' = '2026-02-22-test'; 'X-Source' = 'n8n-test' } -ContentType 'application/json' -Body $payload
   ```
   Der Processor antwortet mit `{"status":"accepted","run_id":"..."}`; ein zweiter Aufruf mit demselben `X-Idempotency-Key` liefert `{"status":"duplicate",...}`.

## Häufige Fallstricke & Lösungen
- **Docker-Engine nicht gestartet / Pipe-Fehler (`docker compose` bricht ab)**: Vor dem Start Docker Desktop öffnen, Status prüfen und `docker info` ausführen. Anschließend `docker compose ps` erneut.
- **PowerShell-Redirect `<` nicht unterstützt**: Schema mit `Get-Content db/schema.sql | docker compose exec -T postgres psql -U integrationhub -d integrationhub` laden.
- **uvicorn fehlt**: Innerhalb des Processor-Containers `pip install -r requirements.txt` (der Container basiert auf `requirements`, die FastAPI + uvicorn + psycopg[binary] definieren). In lokalen Tests `python -m pip install -r processor/requirements.txt` ausführen, wenn der Processor manuell gestartet wird.
- **psycopg-Verbindungsstring nicht akzeptiert**: `psycopg` 3 benötigt das Schema `postgresql://...`; der `.env.example` zeigt `postgresql+psycopg://`, was zu Fehlern führt. In `.env` muss zwingend `DATABASE_URL=postgresql://integrationhub:integrationhub_pw@postgres:5432/integrationhub` stehen.
