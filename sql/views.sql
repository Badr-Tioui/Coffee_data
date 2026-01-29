CREATE OR REPLACE VIEW vw_coffee_fact AS
SELECT
    country,
    "Coffee type",
    year,
    consumption,
    iso3
FROM fact_coffee_consumption
WHERE consumption IS NOT NULL;
