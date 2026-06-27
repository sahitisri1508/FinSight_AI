import pandas as pd


def detect_anomalies(df):
    """
    Detect unusually large expense transactions.
    """

    if df is None or df.empty:
        return pd.DataFrame()

    expense_df = df[df["Amount"] < 0].copy()

    if expense_df.empty:
        return pd.DataFrame()

    mean = expense_df["Absolute Amount"].mean()
    std = expense_df["Absolute Amount"].std()

    threshold = mean + (2 * std)

    anomalies = expense_df[
        expense_df["Absolute Amount"] > threshold
    ]

    return anomalies.sort_values(
        by="Absolute Amount",
        ascending=False
    )