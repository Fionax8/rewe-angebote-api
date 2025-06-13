from flask import Flask, jsonify
import json
import os

app = Flask(__name__)

@app.route("/")
def index():
    """Startseite der API."""
    return "REWE Angebots-API läuft! Rufe /angebote auf, um die Daten zu sehen."

@app.route("/angebote", methods=["GET"])
def get_offers():
    """
    Gibt die gespeicherten REWE Angebote als JSON zurück.
    Liest die Daten aus der 'rewe_angebote.json'-Datei.
    """
    # Der Pfad zur JSON-Datei.
    # Dieser muss mit dem Pfad übereinstimmen, in den der Scraper schreibt.
    # Hier wird die Umgebungsvariable DATA_PATH verwendet.
    # Standardwert ist 'rewe_angebote.json', falls die Variable nicht gesetzt ist.
    file_path = os.environ.get("DATA_PATH", "rewe_angebote.json")
    
    try:
        # Versuche, die Daten aus der JSON-Datei zu laden
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        # Gib die Daten als JSON-Antwort zurück
        return jsonify(data)
    except FileNotFoundError:
        print(f"❌ Datei '{file_path}' wurde nicht gefunden. Bitte stellen Sie sicher, dass der Scraper ausgeführt wurde und die Datei existiert.")
        # Wenn die Datei nicht gefunden wird, gib einen 404-Fehler zurück
        return jsonify({"error": "Noch keine Angebotsdaten verfügbar."}), 404
    except json.JSONDecodeError:
        print(f"❌ Fehler beim Dekodieren der Datei '{file_path}'. Datei ist leer oder ungültig.")
        # Wenn die JSON-Datei beschädigt oder leer ist, gib einen 500-Fehler zurück
        return jsonify({"error": "Fehlerhafte Angebotsdaten."}), 500
    except Exception as e:
        print(f"❌ Ein unerwarteter Fehler ist beim Abrufen der Angebote aufgetreten: {e}")
        return jsonify({"error": "Interner Serverfehler beim Laden der Angebote."}), 500

# Wenn Gunicorn verwendet wird, ist KEIN app.run() hier erforderlich.
# Gunicorn kümmert sich um das Starten der Anwendung.
# Die Flask-Anwendung 'app' wird direkt von Gunicorn importiert und ausgeführt.
