import requests
import time
import random

# Die Adresse deiner Docker-API
# Die Adresse deiner Docker-API (localhost, da Port-Mapping 5000:5000)
URL = "http://localhost:5000/sensor"

def send_measurement(sensor_name):
    # Wir generieren einen zufälligen Temperaturwert zwischen 18 und 25 Grad
    val = round(random.uniform(18.0, 25.0), 2)
    
    payload = {
        "sensor_id": sensor_name,
        "value": val,
        "unit": "Celsius"
    }

    try:
        print(f"Sende Daten: {payload}...")
        response = requests.post(URL, json=payload)
        
        if response.status_code == 201:
            print("Server meldet: Erfolg!")
            print(f"Antwort: {response.json()['message']}")
        else:
            print(f"Fehler vom Server: {response.status_code}")
            
    except Exception as e:
        print(f"Verbindung zum Server fehlgeschlagen: {e}")

if __name__ == "__main__":
    # Schicke eine Test-Messung
    send_measurement("IMS-CLEANROOM-01")