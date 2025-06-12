import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json

BASE_URL = "https://www.rewe.de/angebote/nationale-angebote/"
HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def fetch_offer_period(soup: BeautifulSoup) -> str:
    """Extrahiert den Angebotszeitraum (z. B. '9.6. bis 15.6.')"""
    headline = soup.find("div", string=lambda text: text and "Diese Woche" in text)
    if headline:
        # Suche das nächste Element mit Datum nach der Überschrift
        next_date = headline.find_next(string=lambda text: text and "bis" in text)
        if next_date:
            return next_date.strip()
    return "Zeitraum nicht gefunden"

def fetch_offers():
    response = requests.get(BASE_URL, headers=HEADERS)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Angebotszeitraum extrahieren
    angebot_zeitraum = fetch_offer_period(soup)

    data = {
        "angebotszeitraum": angebot_zeitraum,
        "angebote": {}
    }

    current_category = None
    all_sections = soup.find_all(['h2', 'div'], class_=lambda x: x and ("category-section" in x or "product-tile" in x))

    for section in all_sections:
        if section.name == 'h2':
            current_category = section.get_text(strip=True)
            data["angebote"][current_category] = []
        elif section.name == 'div' and "product-tile" in section.get("class", []):
            title = section.find("span", class_="product-tile-title")
            price = section.find("div", class_="product-tile-price")
            image = section.find("img")
            link = section.find("a", href=True)

            product = {
                "title": title.get_text(strip=True) if title else "Kein Titel",
                "price": price.get_text(strip=True) if price else "Kein Preis",
                "image": image["src"] if image else None,
                "link": f"https://www.rewe.de{link['href']}" if link else None
            }

            if current_category:
                data["angebote"][current_category].append(product)

    return data

def save_to_json(data):
    filename = f"rewe_angebote_{datetime.today().strftime('%Y-%m-%d')}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"✅ Daten gespeichert unter: {filename}")

if __name__ == "__main__":
    offers = fetch_offers()
    save_to_json(offers)
