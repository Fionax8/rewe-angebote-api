from fastapi import FastAPI
from rewe_scraper import get_offers

app = FastAPI()

@app.get("https://rewe-angebote-api.onrender.com/angebote")
def read_offers():
    return get_offers()
