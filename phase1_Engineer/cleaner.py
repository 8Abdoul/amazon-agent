# phase1_Engineer/cleaner.py
from __future__ import annotations
import pandas as pd

def clean(in_path: str = "data/amazon_raw.csv",
          out_path: str = "data/amazon_clean.csv") -> pd.DataFrame:

    df = pd.read_csv(in_path)
    print(f"Brut : {df.shape}")

    # 1. Supprimer les doublons
    df.drop_duplicates(subset=["title", "category"], inplace=True)

    # 2. Nettoyer le prix
    df["price"] = (df["price"]
                   .astype(str)
                   .str.replace(r"[$,]", "", regex=True)
                   .str.strip())
    df["price"] = pd.to_numeric(df["price"], errors="coerce")

    # 3. Nettoyer la note
    df["rating"] = pd.to_numeric(df["rating"], errors="coerce")

    # 4. Supprimer les lignes sans prix ni titre
    df.dropna(subset=["title", "price"], inplace=True)

    # 5. Réinitialiser l'index
    df.reset_index(drop=True, inplace=True)

    df.to_csv(out_path, index=False)
    print(f"Propre : {df.shape}")
    print(f"[OK] Sauvegarde : {out_path}")
    return df

if __name__ == "__main__":
    df = clean()
    print(df.head())