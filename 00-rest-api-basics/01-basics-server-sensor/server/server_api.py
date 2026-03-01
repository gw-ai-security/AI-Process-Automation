from flask import Flask, request, jsonify
import datetime

app = Flask(__name__)
print("--- SENSOR SERVER V2 (WITH LOGGING) STARTING ---")

# Ein einfacher Speicher im Arbeitsspeicher (RAM)
data_store = []

@app.route('/sensor', methods=['POST'])
def receive_data():
    # Die JSON-Daten vom Client abgreifen
    incoming_data = request.get_json()
    
    if not incoming_data:
        return jsonify({"status": "Fehler", "message": "Keine JSON-Daten empfangen"}), 400

    # Zeitstempel hinzufügen, wann die Daten bei der API ankamen
    incoming_data['received_at'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # In unserer Liste speichern
    data_store.append(incoming_data)
    
    print(f"--- NEUE MESSUNG ---")
    print(f"Zeit:   {incoming_data['received_at']}")
    print(f"Sensor: {incoming_data.get('sensor_id', 'Unknown')}")
    print(f"Wert:   {incoming_data.get('value', 'N/A')} {incoming_data.get('unit', '')}")
    print(f"--------------------")

    # In Log-Datei schreiben (absoluter Pfad zur Sicherheit)
    with open("/app/sensor_log.txt", "a", encoding="utf-8") as f:
        log_entry = f"[{incoming_data['received_at']}] Sensor: {incoming_data.get('sensor_id')}, Wert: {incoming_data.get('value')} {incoming_data.get('unit')}\n"
        f.write(log_entry)

    return jsonify({
        "status": "Erfolg",
        "message": "Daten erfolgreich empfangen und gespeichert",
        "entry": incoming_data
    }), 201

@app.route('/sensor', methods=['GET'])
def get_data():
    # Zeigt alle bisher empfangenen Daten an
    return jsonify(data_store), 200

if __name__ == '__main__':
    # host='0.0.0.0' ist wichtig, damit der Docker-Container erreichbar ist!
    app.run(host='0.0.0.0', port=5000, debug=True)