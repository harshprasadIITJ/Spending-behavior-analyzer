import pandas as pd

def add_balance_consistency_flag(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds a boolean column `balance_consistent` indicating whether
    each transaction satisfies the balance invariant.

    Invariant:
    previous_balance + credit_amount - debit_amount == balance

    The first row is marked True by definition.
    """

    df = df.copy()

    df["prev_balance"] = df["balance"].shift(1)

    df["expected_balance"] = (
        df["prev_balance"]
        + df["credit_amount"]
        - df["debit_amount"]
    )

    df["balance_consistent"] = (
        df["expected_balance"] == df["balance"]
    )

    df.loc[df.index[0], "balance_consistent"] = True

    return df
