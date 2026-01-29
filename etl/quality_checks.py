# etl/quality_checks.py

import pandas as pd

def check_missing_values(df: pd.DataFrame):
    missing = df.isna().mean() * 100
    return missing.sort_values(ascending=False)

def check_negative_consumption(df: pd.DataFrame):
    return df[df["Consumption"] < 0]

def check_duplicates(df: pd.DataFrame):
    return df[df.duplicated()]

def run_quality_checks(df: pd.DataFrame):
    print("=== MISSING VALUES (%) ===")
    print(check_missing_values(df))
    print("=== NEGATIVE CONSUMPTION ===")
    print(check_negative_consumption(df))
    print("=== DUPLICATES ===")
    print(check_duplicates(df))
