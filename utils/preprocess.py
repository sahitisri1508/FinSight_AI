import pandas as pd
import streamlit as st


def load_data(uploaded_file):
    """
    Load CSV or Excel file and preprocess it.
    """

    try:

        # Read file
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)

        elif uploaded_file.name.endswith(".xlsx"):
            df = pd.read_excel(uploaded_file)

        else:
            st.error("Unsupported file format.")
            return None

        # Remove duplicate rows
        df.drop_duplicates(inplace=True)

        # Remove empty rows
        df.dropna(how="all", inplace=True)

        # Remove extra spaces from column names
        df.columns = [col.strip() for col in df.columns]

        # Detect date column
        date_cols = [
            "Date",
            "date",
            "Transaction Date",
            "Transaction_Date",
        ]

        for col in date_cols:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors="coerce")
                df.rename(columns={col: "Date"}, inplace=True)
                break

        # Detect amount column
        amount_cols = [
            "Amount",
            "amount",
            "Transaction Amount",
            "Debit",
            "Credit",
        ]

        found = False

        for col in amount_cols:

            if col in df.columns:

                df.rename(columns={col: "Amount"}, inplace=True)

                df["Amount"] = (
                    df["Amount"]
                    .astype(str)
                    .str.replace(",", "")
                    .str.replace("₹", "")
                )

                df["Amount"] = pd.to_numeric(
                    df["Amount"],
                    errors="coerce"
                )

                found = True
                break

        if not found:

            st.error("Amount column not found.")

            return None

        # Detect description column
        description_cols = [
            "Description",
            "Narration",
            "Merchant",
            "Transaction Details",
            "Details",
        ]

        for col in description_cols:

            if col in df.columns:

                df.rename(columns={col: "Description"}, inplace=True)

                break

        # Drop missing amounts
        df.dropna(subset=["Amount"], inplace=True)

        # Create Transaction Type
        

        # Absolute values for charts
        df["Absolute Amount"] = df["Amount"].abs()

        return df

    except Exception as e:

        st.error(f"Error while reading file: {e}")

        return None