import pandas as pd
import pycountry
import os
from sqlalchemy import create_engine, text

# -------------------------------
# PostgreSQL connection config
# -------------------------------
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "1234badrtiwi")
DB_NAME = os.getenv("DB_NAME", "db_Rank")
DB_PORT = os.getenv("DB_PORT", "5432")

URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@localhost:{DB_PORT}/{DB_NAME}"
engine = create_engine(URL, pool_size=10)


# -------------------------------
# Helper : get ISO3
# -------------------------------
def get_iso3(country):
    try:
        return pycountry.countries.lookup(country).alpha_3
    except:
        return None


# -------------------------------
# Load CSV
# -------------------------------
df = pd.read_csv("./data/Coffee.csv")

# Convert years columns
years = [c for c in df.columns if "/" in c]

df_long = df.melt(
    id_vars=["Country", "Coffee type"],
    value_vars=years,
    var_name="Year",
    value_name="Consumption"
)

# Clean
df_long["Consumption"] = df_long["Consumption"].replace(0, pd.NA)
df_long["Consumption"] = pd.to_numeric(df_long["Consumption"], errors="coerce")
df_long = df_long.dropna(subset=["Consumption"])

# Add ISO3
df_long["iso3"] = df_long["Country"].apply(get_iso3)

# Rename columns (optional but clean)
df_long.columns = ["country", "coffee_type", "year", "consumption", "iso3"]


# -------------------------------
# Load to PostgreSQL
# -------------------------------
df_long.to_sql(
    "fact_coffee_consumption",
    engine,
    if_exists="replace",
    index=False
)


# -------------------------------
# Create VIEW
# -------------------------------
create_view_sql = """
CREATE OR REPLACE VIEW vw_coffee_fact AS
SELECT
    country,
    coffee_type,
    year,
    consumption,
    iso3
FROM fact_coffee_consumption
WHERE consumption IS NOT NULL;
"""

with engine.connect() as conn:
    conn.execute(text(create_view_sql))
    conn.commit()


# -------------------------------
# Check view exists
# -------------------------------
with engine.connect() as conn:
    result = conn.execute(text("SELECT COUNT(*) FROM vw_coffee_fact"))
    count = result.scalar()

print("ETL + VIEW complete.")
print(f"Rows in view vw_coffee_fact: {count}")
