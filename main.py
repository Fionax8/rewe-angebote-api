from flask import Flask, jsonify
import json

app = Flask(__name__)

@app.route("/")
def index():
    return "REWE Angebots-API läuft!"

@app.route("/angebote", methods=["GET"])
def get_offers():
    try:
        with open("rewe_angebote.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        return jsonify(data)
    except FileNotFoundError:
        return jsonify({"error": "Noch keine Angebotsdaten verfügbar."}), 404

if __name__ == "__main__":
    app.run()
