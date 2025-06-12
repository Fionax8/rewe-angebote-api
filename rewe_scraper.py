import requests
from bs4 import BeautifulSoup
import json

def scrape_rewe_offers():
    url = "https://www.rewe.de/angebote/nationale-angebote/"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    result = {
        "valid_from_to": "",
        "categories": []
    }

    # Zeitraum finden (gültig von ... bis ...)
    date_tag = soup.find("div", class_="offer-period")
    if date_tag:
        result["valid_from_to"] = date_tag.get_text(strip=True)

    # Kategorien & Produkte
    category_blocks = soup.find_all("div", class_="product-group")

    for block in category_blocks:
        category_name = block.find("h2")
        if not category_name:
            continue

        category = {
            "name": category_name.text.strip(),
            "products": []
        }

        product_cards = block.find_all("li", class_="product-item")
        for card in product_cards:
            title_tag = card.find("span", class_="product-title")
            price_tag = card.find("span", class_="product-price__price")
            image_tag = card.find("img")

            product = {
                "title": title_tag.text.strip() if title_tag else None,
                "price": price_tag.text.strip() if price_tag else None,
                "image": image_tag["src"] if image_tag else None
            }

            category["products"].append(product)

        result["categories"].append(category)

    # In JSON speichern
    with open("offers.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
