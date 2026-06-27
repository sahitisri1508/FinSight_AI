import plotly.express as px
import pandas as pd


# ----------------------------------------
# Helper Function
# ----------------------------------------

def get_expense_df(df):

    if "Transaction_Type" in df.columns:

        return df[
            df["Transaction_Type"].str.lower() == "debit"
        ]

    elif "Transaction Type" in df.columns:

        return df[
            df["Transaction Type"].str.lower() == "debit"
        ]

    else:

        return df[df["Amount"] < 0]


# ----------------------------------------
# Common Theme
# ----------------------------------------

def apply_theme(fig):

    fig.update_layout(

        template="simple_white",

        paper_bgcolor="white",
        plot_bgcolor="white",

        font=dict(
            family="Segoe UI",
            size=14,
            color="#1F2937"
        ),

        title_font=dict(
            size=22,
            color="#111827"
        ),

        margin=dict(
            l=40,
            r=20,
            t=60,
            b=40
        ),

        height=450
    )

    fig.update_xaxes(

        showgrid=False,

        tickfont=dict(
            color="#4B5563",
            size=12
        ),

        title_font=dict(
            color="#111827",
            size=14
        )
    )

    fig.update_yaxes(

        gridcolor="#E5E7EB",

        tickfont=dict(
            color="#4B5563",
            size=12
        ),

        title_font=dict(
            color="#111827",
            size=14
        )
    )

    return fig


# ----------------------------------------
# Expense Pie Chart
# ----------------------------------------

def expense_pie_chart(df):

    expense_df = get_expense_df(df)

    category_data = (
        expense_df.groupby("Category")["Absolute Amount"]
        .sum()
        .reset_index()
    )

    fig = px.pie(
        category_data,
        names="Category",
        values="Absolute Amount",
        hole=0.45,
        title="Expense Distribution"
    )

    fig.update_traces(
        textposition="inside",
        textinfo="percent+label"
    )

    apply_theme(fig)

    return fig


# ----------------------------------------
# Monthly Expense Trend
# ----------------------------------------

def monthly_trend_chart(df):

    expense_df = get_expense_df(df).copy()

    expense_df["Month"] = expense_df["Date"].dt.to_period("M").astype(str)

    monthly = (
        expense_df.groupby("Month")["Absolute Amount"]
        .sum()
        .reset_index()
    )

    fig = px.line(
        monthly,
        x="Month",
        y="Absolute Amount",
        markers=True,
        title="Monthly Expense Trend"
    )

    fig.update_traces(
        line=dict(width=4),
        marker=dict(size=8)
    )

    apply_theme(fig)

    return fig


# ----------------------------------------
# Income vs Expense
# ----------------------------------------

def income_vs_expense_chart(df):

    if "Transaction_Type" in df.columns:

        income = df[
            df["Transaction_Type"].str.lower() == "credit"
        ]["Amount"].sum()

        expense = df[
            df["Transaction_Type"].str.lower() == "debit"
        ]["Amount"].sum()

    elif "Transaction Type" in df.columns:

        income = df[
            df["Transaction Type"].str.lower() == "credit"
        ]["Amount"].sum()

        expense = df[
            df["Transaction Type"].str.lower() == "debit"
        ]["Amount"].sum()

    else:

        income = df[df["Amount"] > 0]["Amount"].sum()

        expense = abs(df[df["Amount"] < 0]["Amount"].sum())

    chart = pd.DataFrame({

        "Type": ["Income", "Expense"],

        "Amount": [income, expense]

    })

    fig = px.bar(
        chart,
        x="Type",
        y="Amount",
        color="Type",
        title="Income vs Expense"
    )

    fig.update_layout(showlegend=False)

    apply_theme(fig)

    return fig


# ----------------------------------------
# Top Spending Categories
# ----------------------------------------

def category_bar_chart(df):

    expense_df = get_expense_df(df)

    data = (
        expense_df.groupby("Category")["Absolute Amount"]
        .sum()
        .reset_index()
        .sort_values(
            by="Absolute Amount",
            ascending=False
        )
    )

    fig = px.bar(
        data,
        x="Category",
        y="Absolute Amount",
        title="Top Spending Categories"
    )

    fig.update_xaxes(tickangle=-30)

    apply_theme(fig)

    return fig


# ----------------------------------------
# Top Merchants
# ----------------------------------------

def merchant_chart(df):

    if "Description" not in df.columns:
        return None

    expense_df = get_expense_df(df)

    data = (
        expense_df.groupby("Description")["Absolute Amount"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    fig = px.bar(
        data,
        x="Absolute Amount",
        y="Description",
        orientation="h",
        title="Top Merchants"
    )

    fig.update_layout(
        yaxis=dict(
            categoryorder="total ascending"
        )
    )

    apply_theme(fig)

    return fig


# ----------------------------------------
# Daily Expense Trend
# ----------------------------------------

def daily_expense_chart(df):

    expense_df = get_expense_df(df)

    daily = (
        expense_df.groupby("Date")["Absolute Amount"]
        .sum()
        .reset_index()
    )

    fig = px.area(
        daily,
        x="Date",
        y="Absolute Amount",
        title="Daily Expense Trend"
    )

    fig.update_traces(
        line=dict(width=3)
    )

    apply_theme(fig)

    return fig