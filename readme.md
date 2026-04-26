# Bhubaneswar Retail Price Intelligence

**Where should a middle-income Bhubaneswar household shop to minimise monthly grocery spend?**

A full-stack data and ML project built on **self-collected pricing data** from 4 market types across Bhubaneswar — Blinkit, Swiggy Instamart, BigBasket, and local kirana/mandi markets.

---

## Key Findings

| Metric | Result |
|--------|--------|
| Monthly saving opportunity | **₹1,238/month** |
| Annual saving opportunity | **₹14,856/year** |
| Saving as % of food spend | **25.9%** |
| Cheapest source overall | **Local Market / Mandi** (cheapest in 18/25 items) |
| Costliest source overall | **Swiggy Instamart** (costliest in 20/25 items, avg 31.9% premium) |
| Highest price volatility | Tomato (44%), Onion (38%), Ginger (37%) |

**Headline:** A Bhubaneswar household buying the same 18-item basket monthly pays ₹4,771 on Swiggy Instamart vs ₹3,533 on BigBasket — a ₹14,856 annual gap for the same groceries.

---

## What's Built

```
price-intel/
├── data/
│   └── prices.py           # Seed dataset — self-collected April 2026
├── analytics.py            # Business logic: basket cost, savings, scorecard, clustering
├── app.py                  # Streamlit dashboard (6 views)
└── README.md
```

### Modules

**`data/prices.py`** — structured dataset of 25 items × 4 sources. Prices are midpoints of observed ranges collected directly from Blinkit, Instamart, BigBasket apps and local market knowledge (April 2026, Bhubaneswar).

**`analytics.py`** — all analytical logic, cleanly separated from UI:
- `monthly_basket_cost()` — total monthly spend per source across 18 common household items
- `savings_analysis()` — cheapest vs costliest source delta, monthly + annual
- `category_analysis()` — average price per category per source
- `item_price_spread()` — cross-source volatility per item
- `source_scorecard()` — how often each source is cheapest/costliest
- `cluster_items()` — KMeans (k=3) clustering items by price level and volatility
- `executive_brief()` — generates ranked findings and recommendations

**`app.py`** — Streamlit dashboard with 6 views: KPI cards, executive brief, basket cost comparison, price spread chart, category breakdown, ML cluster scatter, raw data table with CSV export.

---

## ML Component

KMeans (k=3) clusters all 25 items by:
- **Average price** across sources
- **Cross-source price spread %** (proxy for volatility / negotiation opportunity)

Resulting clusters:
- 🔴 **High Volatility** — Fresh vegetables; highest source-switching benefit
- 🟡 **Premium Items** — Oils, pulses; moderate switching benefit
- 🟢 **Stable & Affordable** — Salt, sugar, packaged FMCG; low switching priority

---

## Data Collection Method

Prices collected manually from:
- **Blinkit app** (Bhubaneswar delivery zone)
- **Swiggy Instamart app** (Bhubaneswar delivery zone)
- **BigBasket app/website** (Bhubaneswar)
- **Local market estimate** — based on direct observation of Bhubaneswar kirana and weekly sabzi mandi prices

All prices are midpoints of the observed price range per item per source. Collection date: April 2026.

---

## Business Recommendation (Ranked)

1. **Buy fresh produce from local market / mandi** — 33–44% cheaper than quick commerce platforms
2. **Use Blinkit/Instamart only for FMCG branded items** — price gap vs BigBasket is under 5% but convenience is high
3. **Use BigBasket for branded staples** (Aashirvaad, Fortune) — 8–12% cheaper than quick commerce with scheduled delivery
4. **Hybrid strategy** (local market for fresh + BigBasket for branded) minimises monthly food spend without sacrificing convenience

---

## Stack

`Python` · `Pandas` · `Scikit-learn` · `Plotly` · `Streamlit` · `KMeans` · `StandardScaler`

---

## Run Locally

```bash
git clone https://github.com/karankavyanjali77-sys/price-intel
cd price-intel
pip install -r requirements.txt
streamlit run app.py
```

---

*Built by Kavyanjali Karan · Bhubaneswar, Odisha · April 2026*