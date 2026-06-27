import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def generate_ai_insights(df):

    if df is None or df.empty:
        return "No financial data available."

    try:

        income = df[df["Amount"] > 0]["Amount"].sum()
        expense = abs(df[df["Amount"] < 0]["Amount"].sum())
        savings = income - expense

        category_summary = (
            df[df["Amount"] < 0]
            .groupby("Category")["Absolute Amount"]
            .sum()
            .sort_values(ascending=False)
            .head(5)
        )

        summary = ""

        for cat, amt in category_summary.items():
            summary += f"{cat}: ₹{amt:.2f}\n"

        prompt = f"""
You are an expert financial advisor.

Financial Summary

Income:
₹{income:.2f}

Expense:
₹{expense:.2f}

Savings:
₹{savings:.2f}

Top Categories

{summary}

Generate a professional report containing:

1. Financial Health
2. Spending Habits
3. Positive Observations
4. Overspending
5. Suggestions
6. Budget Tips
7. Saving Advice

Keep it concise.
"""

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )

        print("Gemini responded successfully")
        return response.text

    except Exception as e:
        return f"AI Insight Error:\n{e}"