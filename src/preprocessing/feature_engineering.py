import pandas as pd

def add_time_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds time-based features required for downstream analysis:
    - date (parsed as datetime)
    - is_weekend (boolean)
    - year_month (period, monthly)
    """

    df = df.copy()

    df["date"] = pd.to_datetime(df["date"])
    df["is_weekend"] = df["date"].dt.weekday >= 5
    df["year_month"] = df["date"].dt.to_period("M")

    return df
