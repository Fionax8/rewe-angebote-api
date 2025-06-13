import requests
from bs4 import BeautifulSoup
import json

BASE_URL = "https://www.rewe.de/angebote/nationale-angebote/"
HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def fetch_offers():
    response = requests.get(BASE_URL, headers=HEADERS)
    soup = BeautifulSoup(response.text, 'html.parser')

    data = {"angebote": []}
    product_tiles = soup.find_all("div", class_="product-tile")

    for tile in product_tiles:
        title = tile.find("span", class_="product-tile-title")
        price = tile.find("div", class_="product-tile-price")
        image = tile.find("img")
        link = tile.find("a", href=True)

        product = {
            "title": title.get_text(strip=True) if title else "Kein Titel",
            "price": price.get_text(strip=True) if price else "Kein Preis",
            "image": image["src"] if image else None,
            "link": f"https://www.rewe.de{link['href']}" if link else None
        }

        data["angebote"].append(product)

    return data

def save_to_json(data):
    with open("rewe_angebote.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print("✅ Daten gespeichert unter: rewe_angebote.json")

if __name__ == "__main__":
    offers = fetch_offers()
    save_to_json(offers)
