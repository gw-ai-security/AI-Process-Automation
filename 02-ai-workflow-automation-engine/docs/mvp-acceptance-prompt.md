# Hard MVP Acceptance Prompt (Codex)

Nutze diesen Prompt, um das Repository strikt gegen den Ziel-MVP zu vervollstaendigen.

## Prompt

Du bist ein Senior Python Backend Engineer und Integration Architect.

Pruefe und vervollstaendige dieses Repository bis zum Status "MVP fertig" fuer den Use Case **Operational Intake Automation**.

Arbeite strikt nach diesen Regeln:

1. Liefere nur den definierten MVP-Umfang:
- 1 End-to-End Workflow
- 1 FastAPI-Service
- 1 n8n Workflow
- 1 LLM-Funktion (Summarization + Classification)
- 1 PostgreSQL Datenbank
- 1 KPI/ROI Layer
- 1-2 Mock Zielsysteme

2. Nicht bauen:
- Frontend
- Auth/User Management
- Multi-Agent Runtime
- Event-Bus Architektur
- echtes Produktions-Jira/Slack Setup
- mehrere LLM Provider parallel

3. Implementiere den fachlichen Kern:
- Kurzfassung
- Action Items
- priority: low|medium|high
- route_to: sales|ops|support|product
- estimated savings (minutes)

4. Erforderliche API Endpunkte:
- POST /intake
- GET /health
- GET /metrics/summary
- GET /workflow/{id}

5. Processing-Pipeline muss real sein:
- Request validation
- Prompt building
- LLM API call (real endpoint or mock adapter behind env flag)
- JSON-only response parsing

6. Persistenz muss real sein:
- workflow_inputs
- workflow_outputs
- workflow_events
- workflow_errors
- workflow_metrics

Mindestens: Input speichern, Output speichern, Correlation ID, Event Logging, Error Logging, KPI Logging.

7. n8n muss lauffaehig sein:
- exportierbares Workflow JSON im Repo
- webhook -> FastAPI -> branching
- high -> mock_jira
- medium -> mock_slack
- low -> store_only
- mind. 2 Routing-Pfade nachweisbar

8. KPI/ROI:
- total_inputs
- success_rate
- avg_processing_time_ms
- route_counts per route
- saved_minutes = manual_baseline_minutes - automated_minutes

9. Tests (pytest) mindestens:
- test_ingest
- test_llm_service
- test_routing
- test_metrics

10. Doku muss professionell sein:
- README, architecture.md, use-case.md, prompt-design.md, kpi-model.md, threat-model.md, demo-script.md
- README enthaelt exakt die Positionierung:
  "Webhook-driven workflow automation engine for summarization, routing and automation impact tracking."
- Grenzen/Risiken klar dokumentieren

11. Demo-Artefakte:
- 3 sample inputs
- demo script
- screenshots
- architecture diagram

12. Betrieb:
- docker compose up funktioniert
- app startet
- db startet
- n8n startet
- sample workflow ausfuehrbar

## Arbeitsweise

- Arbeite in kleinen, commit-freundlichen Schritten.
- Fuehre nach jedem groesseren Schritt Tests und Smoke Checks aus.
- Halte die Struktur sauber und ohne Overengineering.
- Markiere offene Punkte explizit mit TODO + Grund.

## Endausgabe (Pflicht)

Liefere zum Abschluss:

1. Gap-Analyse (vorher -> nachher)
2. Liste aller geaenderten Dateien
3. Exakte Run-Kommandos
4. Exakte Test-Kommandos
5. Ergebnis der Abnahme-Checkliste mit [x]/[ ]
6. Bekannte Risiken und verbleibende Grenzen

## Abnahme-Checkliste

Melde "MVP fertig" erst wenn alle Punkte [x] sind:

- [ ] End-to-End Use Case implementiert
- [ ] POST /intake ok
- [ ] GET /health ok
- [ ] GET /workflow/{id} ok
- [ ] GET /metrics/summary ok
- [ ] Validation vorhanden
- [ ] LLM call implementiert
- [ ] JSON parsing robust
- [ ] summary/action_items/priority/route_to vorhanden
- [ ] DB speichert inputs
- [ ] DB speichert outputs
- [ ] Event logging vorhanden
- [ ] Error logging vorhanden
- [ ] KPI logging vorhanden
- [ ] saved_minutes Logik vorhanden
- [ ] n8n export JSON vorhanden
- [ ] >=2 routing paths nachweisbar
- [ ] >=1 mock integration funktioniert
- [ ] pytest Kernlogik vorhanden
- [ ] README vollstaendig
- [ ] Architekturdiagramm vorhanden
- [ ] Demo Script vorhanden
- [ ] 3 sample inputs vorhanden
- [ ] Screenshots vorhanden
- [ ] Grenzen/Risiken dokumentiert
