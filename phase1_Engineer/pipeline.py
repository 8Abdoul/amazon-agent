# phase1_Engineer/pipeline.py
from __future__ import annotations
import os
from fetcher import fetch_and_save, KEYWORDS
from cleaner import clean

def run():
    print("=== PHASE 1 : DATA ENGINEERING ===\n")

    os.makedirs("../data", exist_ok=True)

    print("[1/2] Recuperation des donnees...")
    fetch_and_save(KEYWORDS, pages=2, out_path="../data/amazon_raw.csv")

    print("\n[2/2] Nettoyage des donnees...")
    df = clean(in_path="../data/amazon_raw.csv", out_path="../data/amazon_clean.csv")

    print(f"\n=== PIPELINE TERMINE : {df.shape[0]} produits prets ===")

if __name__ == "__main__":
    run()