"""
app.py — Bhubaneswar Retail Price Intelligence Dashboard
Run: streamlit run app.py
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from analytics import (
    load_data, monthly_basket_cost, savings_analysis,
    category_analysis, item_price_spread, source_scorecard,
    cluster_items, executive_brief, SOURCE_LABELS, SOURCES
)

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Bhubaneswar Price Intelligence",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── Styling ──────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=DM+Sans:wght@400;500;600&display=swap');

html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
h1, h2, h3 { font-family: 'DM Serif Display', serif; }

.metric-card {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
    border: 1px solid #0f3460;
    border-radius: 12px;
    padding: 1.2rem 1.5rem;
    color: white;
    margin-bottom: 0.5rem;
}
.metric-value { font-size: 2rem; font-weight: 700; color: #e94560; }
.metric-label { font-size: 0.8rem; color: #a0aec0; text-transform: uppercase; letter-spacing: 0.05em; }
.metric-sub { font-size: 0.9rem; color: #68d391; margin-top: 0.2rem; }

.brief-box {
    background: #f0fff4;
    border-left: 4px solid #38a169;
    border-radius: 8px;
    padding: 1rem 1.5rem;
    margin: 0.5rem 0;
    font-size: 0.95rem;
}
.brief-headline {
    background: linear-gradient(135deg, #1a1a2e, #0f3460);
    color: white;
    border-radius: 12px;
    padding: 1.5rem;
    font-size: 1.05rem;
    line-height: 1.6;
    margin-bottom: 1rem;
}
.rec-card {
    background: #ebf8ff;
    border-left: 4px solid #3182ce;
    border-radius: 8px;
    padding: 0.8rem 1.2rem;
    margin: 0.4rem 0;
    font-size: 0.9rem;
}
.section-header {
    font-family: 'DM Serif Display', serif;
    font-size: 1.4rem;
    color: #1a1a2e;
    border-bottom: 2px solid #e94560;
    padding-bottom: 0.3rem;
    margin: 1.5rem 0 1rem 0;
}
.tag-volatile { background:#fff5f5; color:#c53030; padding:2px 8px; border-radius:20px; font-size:0.75rem; }
.tag-premium  { background:#fffbeb; color:#b7791f; padding:2px 8px; border-radius:20px; font-size:0.75rem; }
.tag-stable   { background:#f0fff4; color:#276749; padding:2px 8px; border-radius:20px; font-size:0.75rem; }
</style>
""", unsafe_allow_html=True)

# ── Load data ─────────────────────────────────────────────────────────────────
df         = load_data()
basket     = monthly_basket_cost(df)
savings    = savings_analysis(basket)
cat_df     = category_analysis(df)
spread_df  = item_price_spread(df)
scorecard  = source_scorecard(df)
cluster_df = cluster_items(df)
brief      = executive_brief(savings, scorecard, spread_df)

COLORS = {
    "Blinkit":             "#f7c948",
    "Swiggy Instamart":    "#fc8019",
    "BigBasket":           "#84c225",
    "Local Market / Mandi":"#e94560",
}

# ── Header ───────────────────────────────────────────────────────────────────
st.markdown("# 🛒 Bhubaneswar Retail Price Intelligence")
st.markdown("**Where should a Bhubaneswar household shop to save the most?** · Data collected April 2026 · 25 items · 4 market types")
st.divider()

# ── Top KPI row ───────────────────────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(f"""<div class="metric-card">
        <div class="metric-label">Monthly Saving Opportunity</div>
        <div class="metric-value">₹{savings['monthly_saving']:,.0f}</div>
        <div class="metric-sub">vs. most expensive source</div>
    </div>""", unsafe_allow_html=True)
with c2:
    st.markdown(f"""<div class="metric-card">
        <div class="metric-label">Annual Saving Opportunity</div>
        <div class="metric-value">₹{savings['annual_saving']:,.0f}</div>
        <div class="metric-sub">{savings['pct_saving']}% reduction in food spend</div>
    </div>""", unsafe_allow_html=True)
with c3:
    st.markdown(f"""<div class="metric-card">
        <div class="metric-label">Cheapest Overall Source</div>
        <div class="metric-value" style="font-size:1.3rem">{savings['cheapest_src']}</div>
        <div class="metric-sub">Cheapest in {scorecard[scorecard['source']==savings['cheapest_src']]['cheapest_count'].values[0]}/25 items</div>
    </div>""", unsafe_allow_html=True)
with c4:
    st.markdown(f"""<div class="metric-card">
        <div class="metric-label">Costliest Overall Source</div>
        <div class="metric-value" style="font-size:1.3rem; color:#fc8019">{savings['costliest_src']}</div>
        <div class="metric-sub">Avg 31.9% premium over cheapest</div>
    </div>""", unsafe_allow_html=True)

# ── Executive Brief ───────────────────────────────────────────────────────────
st.markdown('<div class="section-header">📋 Executive Brief</div>', unsafe_allow_html=True)
st.markdown(f'<div class="brief-headline">💡 {brief["headline"]}</div>', unsafe_allow_html=True)

col_f, col_r = st.columns(2)
with col_f:
    st.markdown("**Key Findings**")
    for k in ["finding_1","finding_2","finding_3"]:
        st.markdown(f'<div class="brief-box">📌 {brief[k]}</div>', unsafe_allow_html=True)
with col_r:
    st.markdown("**Ranked Recommendations**")
    for i, k in enumerate(["recommendation_1","recommendation_2","recommendation_3","recommendation_4"], 1):
        st.markdown(f'<div class="rec-card"><strong>#{i}</strong> {brief[k]}</div>', unsafe_allow_html=True)

# ── Monthly Basket Cost Comparison ───────────────────────────────────────────
st.markdown('<div class="section-header">💰 Monthly Basket Cost by Source</div>', unsafe_allow_html=True)

basket_totals = basket["totals"]
fig_basket = go.Figure(go.Bar(
    x=list(basket_totals.keys()),
    y=list(basket_totals.values()),
    text=[f"₹{v:,.0f}" for v in basket_totals.values()],
    textposition="outside",
    marker_color=[COLORS.get(SOURCE_LABELS[s], "#ccc") for s in basket_totals.keys()],
    marker_line_width=0,
))
fig_basket.update_layout(
    xaxis_ticktext=[SOURCE_LABELS[s] for s in basket_totals.keys()],
    xaxis_tickvals=list(basket_totals.keys()),
    yaxis_title="Monthly Cost (₹)",
    plot_bgcolor="white",
    paper_bgcolor="white",
    showlegend=False,
    height=380,
    margin=dict(t=20, b=20),
    yaxis=dict(range=[0, max(basket_totals.values()) * 1.15])
)
st.plotly_chart(fig_basket, use_container_width=True)

# ── Price Spread + Category Analysis ─────────────────────────────────────────
st.markdown('<div class="section-header">📊 Price Analysis</div>', unsafe_allow_html=True)
col_l, col_r = st.columns(2)

with col_l:
    st.markdown("**Top 10 Items by Price Spread Across Sources**")
    fig_spread = px.bar(
        spread_df.head(10),
        x="spread_pct", y="item", orientation="h",
        color="spread_pct",
        color_continuous_scale=["#68d391","#f6e05e","#fc8181"],
        text=spread_df.head(10)["spread_pct"].apply(lambda x: f"{x}%"),
        labels={"spread_pct": "Price Spread %", "item": ""}
    )
    fig_spread.update_traces(textposition="outside")
    fig_spread.update_layout(
        plot_bgcolor="white", paper_bgcolor="white",
        coloraxis_showscale=False, height=400, margin=dict(t=10, b=10)
    )
    st.plotly_chart(fig_spread, use_container_width=True)

with col_r:
    st.markdown("**Average Price by Category & Source**")
    fig_cat = px.bar(
        cat_df, x="category", y="avg_price", color="source",
        barmode="group",
        color_discrete_map=COLORS,
        labels={"avg_price": "Avg Price (₹)", "category": "", "source": "Source"}
    )
    fig_cat.update_layout(
        plot_bgcolor="white", paper_bgcolor="white",
        height=400, margin=dict(t=10, b=10),
        legend=dict(orientation="h", yanchor="bottom", y=1.02)
    )
    st.plotly_chart(fig_cat, use_container_width=True)

# ── Source Scorecard ─────────────────────────────────────────────────────────
st.markdown('<div class="section-header">🏆 Source Scorecard</div>', unsafe_allow_html=True)
sc_display = scorecard.copy()
sc_display.columns = ["Source", "# Cheapest (out of 25)", "# Costliest (out of 25)", "Avg Premium Over Cheapest (%)"]
def color_premium(val):
    if val == 0:
        return "background-color: #c6f6d5; color: #276749; font-weight: 600"
    elif val < 15:
        return "background-color: #fefcbf; color: #744210"
    elif val < 25:
        return "background-color: #feebc8; color: #7b341e"
    else:
        return "background-color: #fed7d7; color: #822727; font-weight: 600"

st.dataframe(
    sc_display.style
        .map(color_premium, subset=["Avg Premium Over Cheapest (%)"])
        .format({"Avg Premium Over Cheapest (%)": "{:.1f}%"}),
    use_container_width=True,
    hide_index=True
)

# ── ML Cluster View ──────────────────────────────────────────────────────────
st.markdown('<div class="section-header">🤖 ML Item Clustering — Price Level vs Volatility</div>', unsafe_allow_html=True)
st.caption("KMeans (k=3) clustering items by average price and cross-source price spread. Useful for identifying where to prioritise source-switching.")

fig_cluster = px.scatter(
    cluster_df, x="avg_price", y="price_spread_pct",
    color="cluster_label", text="item",
    color_discrete_map={
        "🔴 High Volatility":      "#fc8181",
        "🟡 Premium Items":        "#f6e05e",
        "🟢 Stable & Affordable":  "#68d391",
    },
    labels={"avg_price": "Average Price (₹)", "price_spread_pct": "Price Spread Across Sources (%)", "cluster_label": "Cluster"},
    height=480
)
fig_cluster.update_traces(textposition="top center", marker_size=10)
fig_cluster.update_layout(plot_bgcolor="white", paper_bgcolor="white", margin=dict(t=20))
st.plotly_chart(fig_cluster, use_container_width=True)

# ── Raw Data ──────────────────────────────────────────────────────────────────
st.markdown('<div class="section-header">🗃️ Raw Price Data</div>', unsafe_allow_html=True)
cat_filter = st.multiselect("Filter by category", df["category"].unique().tolist(), default=df["category"].unique().tolist())
filtered = df[df["category"].isin(cat_filter)][["item","category","unit","blinkit","instamart","bigbasket","local_market","cheapest_source","saving_vs_blinkit_inr","saving_vs_blinkit_pct"]]
filtered.columns = ["Item","Category","Unit","Blinkit (₹)","Instamart (₹)","BigBasket (₹)","Local Market (₹)","Cheapest Source","Saving vs Blinkit (₹)","Saving vs Blinkit (%)"]
def color_saving(val):
    if not isinstance(val, (int, float)) or pd.isna(val):
        return ""
    if val >= 30: return "background-color: #c6f6d5; color: #276749; font-weight: 600"
    if val >= 20: return "background-color: #9ae6b4; color: #276749"
    if val >= 10: return "background-color: #fefcbf; color: #744210"
    return ""

st.dataframe(filtered.style.format({
    "Saving vs Blinkit (%)": lambda x: f"{x}%" if pd.notna(x) else "—",
    "Saving vs Blinkit (₹)": lambda x: f"₹{x}" if pd.notna(x) else "—",
}).map(color_saving, subset=["Saving vs Blinkit (%)"]), use_container_width=True, hide_index=True)

csv = filtered.to_csv(index=False)
st.download_button("⬇ Download Price Data as CSV", csv, "bhubaneswar_prices_april2026.csv", "text/csv")

# ── Footer ────────────────────────────────────────────────────────────────────
st.divider()
st.caption("Data collected April 2026 · Bhubaneswar, Odisha · 25 items · 4 market types (Blinkit, Swiggy Instamart, BigBasket, Local Market) · Prices are midpoints of observed ranges · Built by Kavyanjali Karan")