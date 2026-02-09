import pandas as pd

def compute_spending_aggregates(df: pd.DataFrame) -> dict:
    """
    Computes observed spending aggregates:
    - total debit spend
    - weekend vs weekday total spend
    - weekend vs weekday average spend per transaction
    """

    expenses = df[df["debit_amount"] > 0].copy()

    weekend_mask = expenses["is_weekend"]
    weekday_mask = ~expenses["is_weekend"]

    weekend_total = expenses.loc[weekend_mask, "debit_amount"].sum()
    weekday_total = expenses.loc[weekday_mask, "debit_amount"].sum()

    weekend_txn_count = weekend_mask.sum()
    weekday_txn_count = weekday_mask.sum()

    weekend_avg = (
        weekend_total / weekend_txn_count
        if weekend_txn_count > 0 else 0.0
    )

    weekday_avg = (
        weekday_total / weekday_txn_count
        if weekday_txn_count > 0 else 0.0
    )
    
    monthly_total_spend = (
    expenses
    .groupby("year_month")["debit_amount"]
    .sum()
    .mean()
)


    total_spend = weekend_total + weekday_total

    return {
        "monthly_total_spend": monthly_total_spend,
        "weekend_total": weekend_total,
        "weekday_total": weekday_total,
        "weekend_avg": weekend_avg,
        "weekday_avg": weekday_avg,
        "weekend_txn_count": weekend_txn_count,
        "weekday_txn_count": weekday_txn_count
    }
