import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def ask_finance_ai(df, question):

    if df is None or df.empty:
        return "No transaction data available."

    try:

        data = df[["Date", "Description", "Category", "Amount"]]

        transactions = data.to_string(index=False)

        prompt = f"""
You are an expert financial assistant.

Below are the user's bank transactions.

{transactions}

Answer ONLY using these transactions.

Question:
{question}

Keep the answer short and professional.
"""
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )

        print("Gemini responded successfully")
        return response.text

    except Exception as e:
        return f"Error: {e}"