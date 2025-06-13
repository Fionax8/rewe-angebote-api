import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

URL = "https://www.rewe.de/angebote/nationale-angebote/"
HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def fetch_offers():
    response = requests.get(URL, headers=HEADERS)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    data = {
        "angebote": {}
    }

    categories = soup.find_all("section", class_="sos-category")

    for category in categories:
        # Kategorie-Titel (z. B. "Top-Angebote")
        header = category.find("h2")
        category_title = header.get_text(strip=True) if header else "Unbekannte Kategorie"
        data["angebote"][category_title] = []

        # Alle Produktangebote in dieser Kategorie
        offers = category.find_all("div", class_="sos-offer")

        for offer in offers:
            title_tag = offer.find("h3")
            title = title_tag.get_text(strip=True) if title_tag else "Kein Titel"

            price_tag = offer.find("div", class_="sos-offer__skeleton-footer-price-value")
            price = price_tag.get_text(strip=True) if price_tag else "Kein Preis"

            image_tag = offer.find("img")
            image_url = image_tag.get("data-src", None) if image_tag else None

            product = {
                "title": title,
                "price": price,
                "image": image_url
            }

            data["angebote"][category_title].append(product)

    return data

def save_to_json(data):
    with open("offers.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print("✅ JSON-Datei wurde gespeichert: offers.json")

if __name__ == "__main__":
    offers = fetch_offers()
    save_to_json(offers)
