def forecast_next_month(df):
    """
    Forecast next month's expenses using
    average monthly spending.
    """

    if df is None or df.empty:
        return None

    expense_df = df[df["Amount"] < 0].copy()

    if expense_df.empty:
        return None

    expense_df["Month"] = (
        expense_df["Date"]
        .dt.to_period("M")
        .astype(str)
    )

    monthly = (
        expense_df.groupby("Month")["Absolute Amount"]
        .sum()
    )

    prediction = monthly.mean()

    return round(prediction, 2)