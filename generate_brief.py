"""
Generate one-page business brief PDF for Bhubaneswar Price Intelligence project.
"""
import sys, os
sys.path.insert(0, "/home/claude/price-intel")

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT

from analytics import (
    load_data, monthly_basket_cost, savings_analysis,
    item_price_spread, source_scorecard, executive_brief
)

# ── Data ──────────────────────────────────────────────────────────────────────
df        = load_data()
basket    = monthly_basket_cost(df)
savings   = savings_analysis(basket)
spread_df = item_price_spread(df)
scorecard = source_scorecard(df)
brief     = executive_brief(savings, scorecard, spread_df)

# ── Styles ────────────────────────────────────────────────────────────────────
DARK  = colors.HexColor("#1a1a2e")
RED   = colors.HexColor("#e94560")
GREEN = colors.HexColor("#38a169")
BLUE  = colors.HexColor("#3182ce")
LGRAY = colors.HexColor("#f7fafc")
MGRAY = colors.HexColor("#e2e8f0")

def style(name, **kw):
    base = {
        "fontName": "Helvetica",
        "fontSize": 10,
        "textColor": DARK,
        "leading": 14,
        "spaceAfter": 4,
    }
    base.update(kw)
    return ParagraphStyle(name, **base)

S = {
    "title":    style("title",    fontName="Helvetica-Bold", fontSize=18, textColor=DARK, leading=22),
    "subtitle": style("subtitle", fontSize=10, textColor=colors.HexColor("#718096"), leading=13),
    "section":  style("section",  fontName="Helvetica-Bold", fontSize=11, textColor=RED, leading=14, spaceBefore=10),
    "headline": style("headline", fontName="Helvetica-Bold", fontSize=10, textColor=colors.white, leading=14),
    "body":     style("body",     fontSize=9,  leading=13),
    "bullet":   style("bullet",   fontSize=9,  leading=13, leftIndent=12),
    "small":    style("small",    fontSize=7.5,textColor=colors.HexColor("#718096"), leading=11),
    "kpi_val":  style("kpi_val",  fontName="Helvetica-Bold", fontSize=18, textColor=RED, leading=20, alignment=TA_CENTER),
    "kpi_lbl":  style("kpi_lbl",  fontSize=7.5, textColor=colors.HexColor("#718096"), leading=10, alignment=TA_CENTER),
}

doc = SimpleDocTemplate(
    "bhubaneswar_price_brief.pdf",
    pagesize=A4,
    leftMargin=1.8*cm, rightMargin=1.8*cm,
    topMargin=1.5*cm, bottomMargin=1.5*cm
)

story = []

# ── Header ────────────────────────────────────────────────────────────────────
story.append(Paragraph("Bhubaneswar Retail Price Intelligence", S["title"]))
story.append(Paragraph("Where should a middle-income Bhubaneswar household shop to minimise monthly grocery spend?", S["subtitle"]))
story.append(Paragraph("Data collected April 2026 &nbsp;·&nbsp; 25 items &nbsp;·&nbsp; 4 market types: Blinkit, Swiggy Instamart, BigBasket, Local Market / Mandi", S["small"]))
story.append(HRFlowable(width="100%", thickness=2, color=RED, spaceAfter=8))

# ── KPI row ───────────────────────────────────────────────────────────────────
kpi_data = [[
    Paragraph(f"Rs.{savings['monthly_saving']:,.0f}", S["kpi_val"]),
    Paragraph(f"Rs.{savings['annual_saving']:,.0f}", S["kpi_val"]),
    Paragraph(f"{savings['pct_saving']}%", S["kpi_val"]),
    Paragraph("Local Market", style("kv2", fontName="Helvetica-Bold", fontSize=14, textColor=GREEN, leading=18, alignment=TA_CENTER)),
],[
    Paragraph("Monthly Saving", S["kpi_lbl"]),
    Paragraph("Annual Saving", S["kpi_lbl"]),
    Paragraph("Reduction in Food Spend", S["kpi_lbl"]),
    Paragraph("Cheapest Source Overall", S["kpi_lbl"]),
]]
kpi_table = Table(kpi_data, colWidths=["25%","25%","25%","25%"])
kpi_table.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,-1), LGRAY),
    ("ROWBACKGROUNDS", (0,0), (-1,-1), [LGRAY, LGRAY]),
    ("BOX", (0,0), (-1,-1), 0.5, MGRAY),
    ("INNERGRID", (0,0), (-1,-1), 0.5, MGRAY),
    ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
    ("TOPPADDING", (0,0), (-1,-1), 8),
    ("BOTTOMPADDING", (0,0), (-1,-1), 8),
]))
story.append(kpi_table)
story.append(Spacer(1, 10))

# ── Headline finding ──────────────────────────────────────────────────────────
hl_data = [[Paragraph(f"HEADLINE FINDING: {brief['headline']}", S["headline"])]]
hl_table = Table(hl_data, colWidths=["100%"])
hl_table.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,-1), DARK),
    ("TOPPADDING", (0,0), (-1,-1), 10),
    ("BOTTOMPADDING", (0,0), (-1,-1), 10),
    ("LEFTPADDING", (0,0), (-1,-1), 12),
    ("RIGHTPADDING", (0,0), (-1,-1), 12),
]))
story.append(hl_table)
story.append(Spacer(1, 8))

# ── Two column: findings + recommendations ────────────────────────────────────
findings_content = [
    Paragraph("KEY FINDINGS", S["section"]),
    Paragraph(f"1. {brief['finding_1']}", S["bullet"]),
    Spacer(1, 3),
    Paragraph(f"2. {brief['finding_2']}", S["bullet"]),
    Spacer(1, 3),
    Paragraph(f"3. {brief['finding_3']}", S["bullet"]),
]
recs_content = [
    Paragraph("RANKED RECOMMENDATIONS", S["section"]),
    Paragraph(f"#1 &nbsp; {brief['recommendation_1']}", S["bullet"]),
    Spacer(1, 3),
    Paragraph(f"#2 &nbsp; {brief['recommendation_2']}", S["bullet"]),
    Spacer(1, 3),
    Paragraph(f"#3 &nbsp; {brief['recommendation_3']}", S["bullet"]),
    Spacer(1, 3),
    Paragraph(f"#4 &nbsp; {brief['recommendation_4']}", S["bullet"]),
]

two_col = Table(
    [[findings_content, recs_content]],
    colWidths=["48%", "52%"]
)
two_col.setStyle(TableStyle([
    ("VALIGN", (0,0), (-1,-1), "TOP"),
    ("LEFTPADDING", (0,0), (0,-1), 0),
    ("RIGHTPADDING", (0,0), (0,-1), 12),
    ("LEFTPADDING", (1,0), (1,-1), 12),
    ("LINEAFTER", (0,0), (0,-1), 0.5, MGRAY),
]))
story.append(two_col)
story.append(Spacer(1, 10))

# ── Source scorecard table ────────────────────────────────────────────────────
story.append(Paragraph("SOURCE SCORECARD — 25 Items Tracked", S["section"]))
sc_data = [["Source", "# Times Cheapest", "# Times Costliest", "Avg Premium Over Cheapest"]]
for _, row in scorecard.iterrows():
    sc_data.append([
        row["source"],
        str(int(row["cheapest_count"])),
        str(int(row["costliest_count"])),
        f"{row['avg_premium_pct']:.1f}%",
    ])
sc_table = Table(sc_data, colWidths=["35%","22%","22%","21%"])
sc_table.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), DARK),
    ("TEXTCOLOR", (0,0), (-1,0), colors.white),
    ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
    ("FONTSIZE", (0,0), (-1,-1), 8.5),
    ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, LGRAY]),
    ("GRID", (0,0), (-1,-1), 0.5, MGRAY),
    ("TOPPADDING", (0,0), (-1,-1), 5),
    ("BOTTOMPADDING", (0,0), (-1,-1), 5),
    ("LEFTPADDING", (0,0), (-1,-1), 8),
    ("ALIGN", (1,0), (-1,-1), "CENTER"),
    # Highlight local market row green, instamart row orange
    ("TEXTCOLOR", (0,1), (-1,1), GREEN),
    ("FONTNAME", (0,1), (-1,1), "Helvetica-Bold"),
    ("TEXTCOLOR", (0,4), (-1,4), RED),
    ("FONTNAME", (0,4), (-1,4), "Helvetica-Bold"),
]))
story.append(sc_table)
story.append(Spacer(1, 10))

# ── Top volatile items ────────────────────────────────────────────────────────
story.append(Paragraph("TOP 5 ITEMS BY PRICE SPREAD (Highest Source-Switching Benefit)", S["section"]))
vol_data = [["Item", "Category", "Min Price", "Max Price", "Spread %", "Cheapest Source"]]
for _, row in spread_df.head(5).iterrows():
    vol_data.append([
        row["item"], row["category"],
        f"Rs.{row['min_price']:.0f}", f"Rs.{row['max_price']:.0f}",
        f"{row['spread_pct']:.1f}%", row["cheapest"],
    ])
vol_table = Table(vol_data, colWidths=["18%","18%","12%","12%","12%","28%"])
vol_table.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), DARK),
    ("TEXTCOLOR", (0,0), (-1,0), colors.white),
    ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
    ("FONTSIZE", (0,0), (-1,-1), 8.5),
    ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, LGRAY]),
    ("GRID", (0,0), (-1,-1), 0.5, MGRAY),
    ("TOPPADDING", (0,0), (-1,-1), 5),
    ("BOTTOMPADDING", (0,0), (-1,-1), 5),
    ("LEFTPADDING", (0,0), (-1,-1), 8),
    ("ALIGN", (2,0), (4,-1), "CENTER"),
]))
story.append(vol_table)

# ── Footer ────────────────────────────────────────────────────────────────────
story.append(Spacer(1, 12))
story.append(HRFlowable(width="100%", thickness=0.5, color=MGRAY))
story.append(Spacer(1, 4))
story.append(Paragraph(
    "Prepared by Kavyanjali Karan &nbsp;·&nbsp; Data Scientist / Data Analyst &nbsp;·&nbsp; Bhubaneswar, Odisha &nbsp;·&nbsp; April 2026 &nbsp;·&nbsp; github.com/karankavyanjali77-sys",
    S["small"]
))

doc.build(story)
print("PDF generated successfully.")