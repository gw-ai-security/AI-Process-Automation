# Projekt: REST API Server-Sensor Integration

Dieses Projekt demonstriert die Kommunikation zwischen zwei unabhängigen Python-Applikationen über eine REST-Schnittstelle.

## Komponenten

1. Server (Schnittstelle): Ein Flask-basierter Webserver, der Daten über einen POST-Endpunkt entgegennimmt.
2. Client (Sensor): Ein Skript, das Sensordaten simuliert und per HTTP-Request an den Server überträgt.

## Installation

Installieren Sie die notwendigen Abhängigkeiten mit folgendem Befehl:

pip install -r requirements.txt

## Ausführung

Um die Integration zu testen, müssen zwei Terminals verwendet werden:

1. Terminal - Server starten:
   cd server
   python server_api.py

2. Terminal - Client/Sensor starten:
   cd client
   python sensor_client.py

## Endpunkte

POST /sensor
Akzeptiert JSON-Daten mit folgenden Feldern:
- sensor_id (String)
- temperatur (Float)
- zeitpunkt (String)

## Zweck des Projekts

Das Projekt zeigt, wie Hardware-nahe Daten (Sensoren) in ein IT-System eingespeist werden können. Dies ist ein Standard-Szenario in der industriellen Fertigung und Systemüberwachung.