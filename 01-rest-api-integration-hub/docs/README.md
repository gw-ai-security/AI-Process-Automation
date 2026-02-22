# Dokumentation: REST-API Integration Hub

## Für Nicht-IT (Kurz)
- Das Modul fängt Webhook-Leads ab, dokumentiert jeden Schritt und stellt ein zentrales Reporting sicher.
- Ein Docker-Stack mit n8n, Processor und PostgreSQL macht die Umgebung lokal reproduzierbar.
- Glossar und Runbook ermöglichen klare Abstimmung zwischen Fachseite und Technik.

## Für IT (Details)
- Die Dokumentation bündelt die wichtigsten Artefakte (Übersicht, Architektur/Sequenz, Setup-Runbook, API-Verträge, Audit/KPI-Tables, Changelog) in einem durchsuchbaren Ordner und verweist auf die Glossareinträge sowie die Wartungsroutine.
- Sie bezieht sich auf die aktuellen Compose-Ports (n8n:5678, Processor:8000, PostgreSQL:5432), die FastAPI-Endpoints (/health, /webhook/lead), die Laufzeiten in PostgreSQL (Runs/Audit/DLQ/KPI) und die Idempotenzlogik im Processor.
- Änderungen an Services, Endpunkten oder Tabellen lösen gemäß Maintenance-Skill konkrete Dokumentations- und Glossar-Updates aus.

## Dokumentübersicht
1. [01_overview.md](01_overview.md) – Projektziele, Scope und Verantwortlichkeiten.
2. [02_architecture.md](02_architecture.md) – Komponenten, Datenfluss, Idempotenz und Audit-Logging.
3. [03_setup_runbook.md](03_setup_runbook.md) – Lokales Setup auf Windows/Docker Desktop sowie bekannte Fallstricke.
4. [04_api_contracts.md](04_api_contracts.md) – Endpunkte, Header, Payloads, Antworten und Idempotenzregeln.
5. [05_audit_kpi.md](05_audit_kpi.md) – Datenbanktabellen für Runs, Audit, DLQ und KPI sowie Beispielabfragen.
6. [06_change_log.md](06_change_log.md) – Datiertes Änderungsprotokoll mit technischer und geschäftlicher Bewertung.
7. [glossary.md](glossary.md) – Begriffsdefinitionen mit Non-IT- und IT-Notizen.
8. [kpis.md](kpis.md) – KPI-Definitionen, Aggregationslogik und Reporting-Hinweise.
9. [threat_model.md](threat_model.md) – Assets, Bedrohungen und Sicherheitskontrollen im Projekt.
10. [rc_checklist.md](rc_checklist.md) – Release-Candidate-Checkliste inklusive Smoke/Fehlerfälle und Dokumentationsprüfung.
11. [DOCS_MAINTENANCE_SKILL.md](DOCS_MAINTENANCE_SKILL.md) – Wartungsprozess, Vorlagen und Checkliste für Dokumentupdates.
