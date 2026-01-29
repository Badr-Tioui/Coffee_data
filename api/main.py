from fastapi import FastAPI, Request, HTTPException
from fastapi.templating import Jinja2Templates
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sqlalchemy import create_engine
import os
import uvicorn

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "1234badrtiwi")
DB_NAME = os.getenv("DB_NAME", "db_Rank")
DB_PORT = os.getenv("DB_PORT", "5432")

URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@localhost:{DB_PORT}/{DB_NAME}"
engine = create_engine(URL)

@app.get("/dashboard")
def dashboard(request: Request, country: str = "Brazil"):
    # Use view
    query = "SELECT * FROM vw_coffee_fact"
    df = pd.read_sql(query, engine)

    if country not in df["country"].unique():
        raise HTTPException(status_code=404, detail="Country not found")

    total_consumption = df["consumption"].sum()
    avg_consumption = df["consumption"].mean()

    years_sorted = sorted(df["year"].unique())
    start_val = df[df["year"] == years_sorted[0]]["consumption"].sum()
    end_val = df[df["year"] == years_sorted[-1]]["consumption"].sum()
    growth_pct = ((end_val - start_val) / start_val) * 100 if start_val != 0 else 0

    global_trend = df.groupby("year")["consumption"].mean().reset_index()
    fig_global = px.line(global_trend, x="year", y="consumption", title="Global Trend", markers=True)

    country_trend = df[df["country"] == country].groupby("year")["consumption"].mean().reset_index()
    fig_country = px.line(country_trend, x="year", y="consumption", title=f"Trend - {country}", markers=True)

    top10 = df.groupby("country")["consumption"].sum().nlargest(10).index
    heat_data = df[df["country"].isin(top10)]
    fig_heat = px.density_heatmap(heat_data, x="year", y="country", z="consumption", title="Top 10 Heatmap")

    fig_waterfall = go.Figure(go.Waterfall(
        name="Growth",
        orientation="v",
        measure=["relative", "relative", "total"],
        x=["Start", "Growth", "End"],
        y=[global_trend["consumption"].iloc[0],
           global_trend["consumption"].iloc[-1] - global_trend["consumption"].iloc[0],
           global_trend["consumption"].iloc[-1]]
    ))
    fig_waterfall.update_layout(title="Global Growth")

    fig_box = px.box(df[df["country"].isin(top10)], x="country", y="consumption", title="Top 10 Distribution")

    map_data = df.groupby(["year", "iso3"])["consumption"].sum().reset_index()
    fig_map = px.choropleth(map_data, locations="iso3", color="consumption", animation_frame="year", title="World Map")

    top_countries = df.groupby("country")["consumption"].sum().nlargest(5).index
    sankey_data = df[df["country"].isin(top_countries)]
    sankey_agg = sankey_data.groupby(["coffee_type", "country"])["consumption"].sum().reset_index()

    labels = list(sankey_agg["coffee_type"].unique()) + list(sankey_agg["country"].unique())
    sources, targets, values = [], [], []

    for _, row in sankey_agg.iterrows():
        sources.append(labels.index(row["coffee_type"]))
        targets.append(labels.index(row["country"]))
        values.append(row["consumption"])

    fig_sankey = go.Figure(go.Sankey(
        node=dict(label=labels),
        link=dict(source=sources, target=targets, value=values)
    ))
    fig_sankey.update_layout(title="Sankey: Coffee Type → Country")

    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "total_consumption": f"{total_consumption:,.0f}",
        "avg_consumption": f"{avg_consumption:,.2f}",
        "growth_pct": f"{growth_pct:.2f}%",
        "fig_global": fig_global.to_html(full_html=False),
        "fig_country": fig_country.to_html(full_html=False),
        "fig_heat": fig_heat.to_html(full_html=False),
        "fig_waterfall": fig_waterfall.to_html(full_html=False),
        "fig_box": fig_box.to_html(full_html=False),
        "fig_map": fig_map.to_html(full_html=False),
        "fig_sankey": fig_sankey.to_html(full_html=False),
        "country": country
    })

    

if __name__ == "__main__":
    uvicorn.run("api.main:app", host="127.0.0.1", port=8000, reload=True)
