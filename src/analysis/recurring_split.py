import pandas as pd
from src.config.constants import FIXED_MERCHANTS

def split_fixed_habitual(
    df: pd.DataFrame,
    recurring_merchants: list
) -> dict:
    """
    Splits recurring expenses into fixed and habitual categories
    and computes average monthly spend for each.

    Returns:
        {
            "fixed_monthly_avg": float,
            "habitual_monthly_avg": float
        }
    """

    # consider only recurring expenses
    recurring_expenses = df[
        (df["description"].isin(recurring_merchants)) &
        (df["debit_amount"] > 0)
    ].copy()

    fixed_expenses = recurring_expenses[
        recurring_expenses["description"].isin(FIXED_MERCHANTS)
    ]

    habitual_expenses = recurring_expenses[
        ~recurring_expenses["description"].isin(FIXED_MERCHANTS)
    ]

    fixed_monthly_avg = (
        fixed_expenses
        .groupby("year_month")["debit_amount"]
        .sum()
        .mean()
    )

    habitual_monthly_avg = (
        habitual_expenses
        .groupby("year_month")["debit_amount"]
        .sum()
        .mean()
    )

    return {
        "fixed_monthly_avg": fixed_monthly_avg or 0.0,
        "habitual_monthly_avg": habitual_monthly_avg or 0.0
    }
