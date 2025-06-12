from fastapi import FastAPI
from rewe_scraper import scrape_rewe_offers

app = FastAPI()

@app.get("https://rewe-angebote-api.onrender.com/angebote")
def read_offers():
    return scrape_rewe_offers()
