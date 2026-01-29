CREATE TABLE IF NOT EXISTS dim_country (
    country_id SERIAL PRIMARY KEY,
    country VARCHAR(255),
    iso3 CHAR(3)
);

CREATE TABLE IF NOT EXISTS dim_coffee_type (
    coffee_id SERIAL PRIMARY KEY,
    coffee_type VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS dim_date (
    date_id SERIAL PRIMARY KEY,
    year INT
);

CREATE TABLE IF NOT EXISTS fact_coffee_consumption (
    id SERIAL PRIMARY KEY,
    date_id INT REFERENCES dim_date(date_id),
    country_id INT REFERENCES dim_country(country_id),
    coffee_id INT REFERENCES dim_coffee_type(coffee_id),
    consumption FLOAT
);
