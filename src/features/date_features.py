import pandas as pd

def add_date_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Ensure date column is datetime
    df["date"] = pd.to_datetime(df["date"])

    # Weekend flag
    df["is_weekend"] = df["date"].dt.dayofweek >= 5

    # Year-month grouping
    df["year_month"] = df["date"].dt.to_period("M").astype(str)

    return df
