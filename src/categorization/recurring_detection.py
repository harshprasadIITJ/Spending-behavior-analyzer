import pandas as pd

def detect_recurring_merchants(
    df: pd.DataFrame,
    min_months: int = 2
) -> list:
    """
    Detects merchants with debit transactions appearing
    in at least `min_months` distinct months.

    Returns a list of merchant names.
    """

    # consider only expenses
    expenses = df[df["debit_amount"] > 0].copy()

    merchant_month_counts = (
        expenses
        .groupby("description")["year_month"]
        .nunique()
    )

    recurring_merchants = merchant_month_counts[
        merchant_month_counts >= min_months
    ].index.tolist()

    return recurring_merchants
