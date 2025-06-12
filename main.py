from flask import Flask, jsonify
import json
import os

app = Flask(__name__)

@app.route("/")
def index():
    return "REWE Angebots-API läuft!"

@app.route("/angebote", methods=["GET"])
def get_offers():
    if not os.path.exists("offers.json"):
        return jsonify({"error": "Noch keine Angebotsdaten verfügbar."}), 404
    with open("offers.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    return jsonify(data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)  # wichtig für Render!
