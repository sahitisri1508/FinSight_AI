import pandas as pd

# --------------------------------------------------
# Expense Category Mapping
# --------------------------------------------------

CATEGORY_KEYWORDS = {
    "Food": [
        "swiggy",
        "zomato",
        "restaurant",
        "cafe",
        "pizza",
        "burger",
        "food",
        "kfc",
        "dominos",
        "mcdonald"
    ],

    "Groceries": [
        "dmart",
        "reliance",
        "grocery",
        "supermarket",
        "bigbasket",
        "blinkit",
        "zepto"
    ],

    "Shopping": [
        "amazon",
        "flipkart",
        "myntra",
        "ajio",
        "shopping"
    ],

    "Travel": [
        "flight",
        "air",
        "hotel",
        "booking"
    ],

    "Transportation": [
        "uber",
        "ola",
        "metro",
        "fuel",
        "petrol",
        "diesel"
    ],

    "Bills": [
        "electricity",
        "water",
        "internet",
        "wifi",
        "gas",
        "bill"
    ],

    "Entertainment": [
        "netflix",
        "spotify",
        "prime",
        "youtube",
        "movie"
    ],

    "Healthcare": [
        "hospital",
        "medical",
        "pharmacy",
        "apollo"
    ],

    "Education": [
        "college",
        "school",
        "udemy",
        "coursera",
        "book"
    ],

    "Salary": [
        "salary",
        "credit salary",
        "payroll"
    ]
}


# --------------------------------------------------
# Categorize Transaction
# --------------------------------------------------

def categorize(description):

    if pd.isna(description):
        return "Others"

    description = str(description).lower()

    for category, words in CATEGORY_KEYWORDS.items():
        for word in words:
            if word in description:
                return category

    return "Others"


# --------------------------------------------------
# Analyze Expenses
# --------------------------------------------------

def analyze_expenses(df):

    df = df.copy()

    # Categorize transactions
    if "Description" in df.columns:
        df["Category"] = df["Description"].apply(categorize)
    else:
        df["Category"] = "Others"

    # ---------------- Income & Expense ----------------

    if "Transaction_Type" in df.columns:

        income = df[
            df["Transaction_Type"].str.lower() == "credit"
        ]["Amount"].sum()

        expense = df[
            df["Transaction_Type"].str.lower() == "debit"
        ]["Amount"].sum()

        expense_df = df[
            df["Transaction_Type"].str.lower() == "debit"
        ]

    elif "Transaction Type" in df.columns:

        income = df[
            df["Transaction Type"].str.lower() == "credit"
        ]["Amount"].sum()

        expense = df[
            df["Transaction Type"].str.lower() == "debit"
        ]["Amount"].sum()

        expense_df = df[
            df["Transaction Type"].str.lower() == "debit"
        ]

    else:

        income = df[df["Amount"] > 0]["Amount"].sum()

        expense = abs(df[df["Amount"] < 0]["Amount"].sum())

        expense_df = df[df["Amount"] < 0]

    # ---------------- Savings ----------------

    savings = income - expense

    # ---------------- Category Summary ----------------

    category_summary = (
        expense_df
        .groupby("Category")["Absolute Amount"]
        .sum()
        .sort_values(ascending=False)
    )

    # ---------------- Merchant Summary ----------------

    if "Description" in expense_df.columns:

        merchant_summary = (
            expense_df
            .groupby("Description")["Absolute Amount"]
            .sum()
            .sort_values(ascending=False)
        )

    else:

        merchant_summary = pd.Series(dtype=float)

    return {

        "income": income,

        "expense": expense,

        "savings": savings,

        "category_summary": category_summary,

        "merchant_summary": merchant_summary,

        "data": df

    }