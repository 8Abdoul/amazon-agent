# phase1_Engineer/fetcher.py
from __future__ import annotations
import os
import time
import requests
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("RAPIDAPI_KEY")
BASE_URL = "https://real-time-amazon-data.p.rapidapi.com"
HEADERS = {
    "X-RapidAPI-Key": API_KEY,
    "X-RapidAPI-Host": "real-time-amazon-data.p.rapidapi.com"
}

KEYWORDS = [
    "laptop", "smartphone", "headphones", "keyboard", "monitor",
    "tablet", "camera", "mouse", "printer", "speaker",
    "smartwatch", "gaming chair", "webcam", "microphone", "hard drive"
]

def search_products(keyword: str, page: int = 1, country: str = "US") -> list[dict]:
    """Recherche des produits Amazon par mot-cle et page."""
    url = f"{BASE_URL}/search"
    params = {"query": keyword, "page": str(page), "country": country}

    response = requests.get(url, headers=HEADERS, params=params)
    response.raise_for_status()
    data = response.json()

    products = []
    for item in data.get("data", {}).get("products", []):
        products.append({
            "title":    item.get("product_title"),
            "price":    item.get("product_price"),
            "rating":   item.get("product_star_rating"),
            "category": keyword,
            "url":      item.get("product_url"),
        })
    return products

def fetch_and_save(
    keywords: list[str] = KEYWORDS,
    pages: int = 2,
    out_path: str = "../data/amazon_raw.csv"
) -> pd.DataFrame:
    """Recupere les produits pour plusieurs categories et pages."""
    all_products = []
    total = len(keywords) * pages

    for i, kw in enumerate(keywords):
        for page in range(1, pages + 1):
            print(f"[{i*pages+page}/{total}] {kw} - page {page}")
            try:
                products = search_products(kw, page=page)
                print(f"   -> {len(products)} produits")
                all_products.extend(products)
                time.sleep(0.5)  # eviter le rate limit
            except Exception as e:
                print(f"   [ERREUR] {kw} page {page}: {e}")

    df = pd.DataFrame(all_products)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    df.to_csv(out_path, index=False)
    print(f"\n[OK] Sauvegarde : {out_path} ({len(df)} lignes)")
    return df

if __name__ == "__main__":
    fetch_and_save()