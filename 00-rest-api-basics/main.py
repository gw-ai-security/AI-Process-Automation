import requests
from datetime import datetime

def log_to_file(action, status, data):
    """Speichert jede API-Aktion in einer Textdatei."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("logs/api_log.txt", "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {action} | Status: {status} | Info: {data}\n")

def rest_basics_demo():
    base_url = "https://jsonplaceholder.typicode.com/posts"
    
    print("--- 1. GET (Daten abrufen) ---")
    # Wir holen uns den Beitrag mit der ID 1
    res_get = requests.get(f"{base_url}/1")
    if res_get.status_code == 200:
        post = res_get.json()
        print(f"Titel: {post['title']}\n")
        log_to_file("GET", res_get.status_code, f"Titel erhalten: {post['title'][:20]}...")

    print("--- 2. POST (Daten erstellen) ---")
    # Wir simulieren das Erstellen eines neuen Blog-Beitrags
    neuer_beitrag = {
        "title": "Mein erstes API Projekt",
        "body": "REST ist eigentlich ganz simpel!",
        "userId": 1
    }
    res_post = requests.post(base_url, json=neuer_beitrag)
    if res_post.status_code == 201: # 201 = Created
        print(f"Erfolg! Neuer Beitrag erstellt mit ID: {res_post.json()['id']}\n")
        log_to_file("POST", res_post.status_code, "Neuer Beitrag angelegt")

    print("--- 3. PUT (Daten aktualisieren) ---")
    # Wir ändern den Titel von Beitrag ID 1
    update_daten = {"title": "Update: REST ist super!"}
    res_put = requests.put(f"{base_url}/1", json=update_daten)
    print(f"Update Status: {res_put.status_code} (OK)\n")
    log_to_file("PUT", res_put.status_code, "Titel aktualisiert")

    print("--- 4. DELETE (Daten löschen) ---")
    res_del = requests.delete(f"{base_url}/1")
    print(f"Lösch Status: {res_del.status_code} (Kein Inhalt mehr da)\n")
    log_to_file("DELETE", res_del.status_code, "Beitrag gelöscht")

if __name__ == "__main__":
    print("=== START: REST API BASICS DEMO ===\n")
    rest_basics_demo()
    print("Fertig! Check mal die 'api_log.txt' in deinem Ordner.")