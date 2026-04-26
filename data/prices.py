"""
Bhubaneswar Retail Price Intelligence — Seed Dataset
Prices collected: April 2026 | Source: Blinkit, Instamart, BigBasket, Local Market
Method: Midpoint of observed price range per source
"""

import pandas as pd
from datetime import date

RAW = [
    # item, category, unit, blinkit, instamart, bigbasket, local
    ("Rice",           "Staples",   "1kg",  75,  77,  70,  55),
    ("Atta",           "Staples",   "1kg",  62,  65,  57,  45),
    ("Toor Dal",       "Staples",   "1kg", 160, 162, 152, 130),
    ("Moong Dal",      "Staples",   "1kg", 142, 145, 132, 115),
    ("Sugar",          "Staples",   "1kg",  48,  48,  46,  40),
    ("Salt",           "Staples",   "1kg",  24,  25,  21,  17),
    ("Sunflower Oil",  "Oils",      "1L",  190, 192, 180, 157),
    ("Mustard Oil",    "Oils",      "1L",  240, 245, 225, 195),
    ("Soyabean Oil",   "Oils",      "1L",  175, 180, 165, 142),
    ("Milk",           "Dairy",     "1L",   65,  66,  63,  55),
    ("Curd",           "Dairy",     "400g", 45,  45,  40,  32),
    ("Paneer",         "Dairy",     "200g",102, 105,  97,  82),
    ("Butter",         "Dairy",     "100g", 60,  60,  56,  52),
    ("Potato",         "Vegetables","1kg",  45,  47,  None, 30),
    ("Onion",          "Vegetables","1kg",  60,  62,  None, 37),
    ("Tomato",         "Vegetables","1kg",  75,  80,  None, 42),
    ("Garlic",         "Vegetables","100g", 30,  32,  None, 22),
    ("Ginger",         "Vegetables","100g", 27,  30,  None, 17),
    ("Tata Salt",      "FMCG",      "1kg",  25,  26,  22,  None),
    ("Amul Butter",    "FMCG",      "100g", 60,  60,  56,  None),
    ("Aashirvaad Atta","FMCG",      "1kg",  65,  67,  60,  None),
    ("Fortune Oil",    "FMCG",      "1L",  187, 190, 177,  None),
    ("Parle-G",        "FMCG",      "200g", 34,  34,  30,  None),
    ("Maggi",          "FMCG",      "4x70g",70,  72,  65,  None),
    ("Surf Excel",     "FMCG",      "500g",150, 152, 135,  None),
]

SOURCES = ["blinkit", "instamart", "bigbasket", "local_market"]

def build_df():
    rows = []
    for item, cat, unit, b, i, bb, l in RAW:
        prices = {"blinkit": b, "instamart": i, "bigbasket": bb, "local_market": l}
        available = {k: v for k, v in prices.items() if v is not None}
        cheapest_src = min(available, key=available.get)
        costliest_src = max(available, key=available.get)
        avg = round(sum(available.values()) / len(available), 1)
        saving_vs_blinkit = round(b - available.get("local_market", b), 1) if "local_market" in available else None
        pct_saving = round(saving_vs_blinkit / b * 100, 1) if saving_vs_blinkit else None

        rows.append({
            "date": date.today().isoformat(),
            "item": item,
            "category": cat,
            "unit": unit,
            "blinkit": b,
            "instamart": i,
            "bigbasket": bb,
            "local_market": l,
            "avg_price": avg,
            "cheapest_source": cheapest_src,
            "costliest_source": costliest_src,
            "saving_vs_blinkit_inr": saving_vs_blinkit,
            "saving_vs_blinkit_pct": pct_saving,
        })
    return pd.DataFrame(rows)

if __name__ == "__main__":
    df = build_df()
    df.to_csv("prices_seed.csv", index=False)
    print(df.to_string())