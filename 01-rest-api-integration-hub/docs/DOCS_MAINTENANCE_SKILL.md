# Documentation & Glossary Maintenance Skill

## Für Nicht-IT (Kurz)
- Dieses Verfahren beschreibt, wann und wie die Dokumentation oder das Glossar aktualisiert werden muss.
- Es enthält Trigger, Regeln, Vorlagen und eine kurze Checkliste vor jedem Merge.
- Damit bleiben Projektwissen und Business-Kontext über alle Dokumente hinweg konsistent.

## Für IT (Details)
- Die Richtlinie definiert Update-Triggertypen (z. B. neue Endpunkte/Services, Schema-Änderungen, Workflows, erkannte Fehler), harmonisiert Terminologie (Glossar) und verlangt datierte Änderungseinträge.
- Jede Änderung nutzt die Templates für neue Endpunkte, neue Services oder neue Fallstricke, damit Struktur, Heading-Namen und die Non-IT/IT-Aufteilung einheitlich bleiben.
- Vor jedem PR muss die Checkliste beachtet werden: Alle Dokumente, das Glossar und der Changelog müssen aktualisiert werden, Links überprüft und insbesondere die Nicht-IT/IT-Abschnitte in jedem betroffenen File gepflegt sein.

## Update-Trigger
1. **Neuer Endpoint** – ein weiterer Route/h HTTP-Handler wird eingeführt, z. B. `/webhook/lead` oder `/health`.
2. **Neuer Service/Container** – jeder zusätzliche Docker-Service (z. B. Mock-CRM, Alert-Service) muss dokumentiert werden.
3. **Schema-/Tabellenänderung** – Anpassungen an `./db/schema.sql` oder an der Datenbankstruktur triggern Audit/KPI-Updates.
4. **Workflow-Änderung** – neue oder geänderte n8n-Workflows (Dateien in `n8n/workflows/`) benötigen Beschreibung und Status im Glossar.
5. **Fehlerfall/Fallstrick erkannt** – neue Docker-, PowerShell- oder Dependency-Probleme erfordern Dokumentation im Runbook.

## Regeln
- Glossar aktualisieren, sobald Begriffe hinzukommen oder sich ändern.
- Widersprüche zwischen Dokumenten vermeiden; Abweichungen müssen explizit im Changelog erläutert werden.
- Sprache immer Deutsch; jede Dokumentstruktur behält die Abschnitte “Für Nicht-IT (Kurz)” und “Für IT (Details)”.
- Neue Abschnitte oder Begriffe verlinken auf `docs/glossary.md` und bleiben im selben Ordner.
- Jedes sinnvolle Update führt zu einem neuen Eintrag in `docs/06_change_log.md`.

## Templates
### Neue Endpoint-Beschreibung
- **Abschnittstitel:** `## Endpoint: <Methode> <Pfad>`
- **Nicht-IT:** 3–4 Bulletpoints mit Zweck/Impact.
- **IT:** Header, Payload/Felder, Antwortbeispiele, Statuscodes, Idempotenz / Fehlerbehandlung.
- **Glossar:** Begriff eintragen (z. B. `Webhook`, `Endpoint`).

### Neuer Service
- **Abschnittstitel:** `## Dienst: <Name>`
- **Nicht-IT:** Nutzen, Business-Impact, Beziehung zu Fachprozessen.
- **IT:** Ports, Environment-Variablen, Volumes, Healthchecks, Kommunikation (Service-zu-Service).
- **Changelog:** Neuer Eintrag mit Business-/Technik-Reasoning.

### Neuer Pitfall
- **Abschnittstitel:** `## Fallstrick: <Kurzbeschreibung>`
- **Nicht-IT:** Was passiert aus User-Perspektive.
- **IT:** Technischer Grund (z. B. Redirect, Missing Dependency) und exakte Lösung/Command.
- **Links:** Ggf. Referenz auf die ausführende Datei (z. B. `docs/03_setup_runbook.md`).

## Checkliste vor PR/Commit
- Dokumente aktualisiert? (Nein → Änderungen in `docs/*.md` ergänzen.)
- Glossar gepflegt? (Neue Begriffe ergänzen oder bestehende anpassen.)
- Changelog ergänzt? (Datierten Eintrag mit Business- und Technikhinweis.)
- Verlinkungen geprüft? (Relative Links zu allen betroffenen Kapiteln.)
