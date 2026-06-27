import os
import streamlit as st
from dotenv import load_dotenv

# ---------------- Utility Modules ---------------- #

from utils.preprocess import load_data
from utils.expense_analyzer import analyze_expenses

from utils.charts import (
    expense_pie_chart,
    monthly_trend_chart,
    income_vs_expense_chart,
    category_bar_chart,
    merchant_chart,
    daily_expense_chart,
)

from utils.health_score import (
    calculate_health_score,
    get_health_label,
)

from utils.insights import generate_ai_insights
from utils.chatbot import ask_finance_ai
from utils.forecast import forecast_next_month
from utils.anomaly_detector import detect_anomalies
from streamlit_option_menu import option_menu

# ---------------- Load Environment ---------------- #

load_dotenv()

print("Current API Key:", os.getenv("GEMINI_API_KEY"))
print(os.getenv("GEMINI_API_KEY")[:15])
# ---------------- Page Config ---------------- #

st.set_page_config(
    page_title="FinSight AI",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="auto",
)

# ---------------- Load CSS ---------------- #

css_path = "assets/styles.css"

if os.path.exists(css_path):
    with open(css_path) as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )

# ---------------- Session State ---------------- #

if "df" not in st.session_state:
    st.session_state.df = None

# ---------------- Sidebar ---------------- #

st.sidebar.title("💰 FinSight AI")
st.sidebar.markdown("---")

with st.sidebar:

    selected = option_menu(
        menu_title="Navigation",
        options=[
            "Dashboard",
            "AI Insights",
            "Ask AI",
            "Settings"
        ],
        icons=[
            "house-fill",
            "robot",
            "chat-dots-fill",
            "gear-fill"
        ],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {
                "padding": "5px",
                "background-color": "#0F172A"
            },
            "icon": {
                "color": "#60A5FA",
                "font-size": "18px"
            },
            "nav-link": {
                "font-size": "16px",
                "text-align": "left",
                "margin": "6px",
                "border-radius": "10px",
            },
            "nav-link-selected": {
                "background-color": "#2563EB",
                "color": "white",
            },
        }
    )

st.sidebar.markdown("---")
st.sidebar.caption("Powered by Gemini AI")

# ==========================================================
# DASHBOARD
# ==========================================================

if selected == "Dashboard":

    st.markdown("""
    <h1 style='font-size:42px;margin-bottom:0'>
    💰 FinSight AI
    </h1>
    """, unsafe_allow_html=True)

    st.markdown("""
    <p style='font-size:18px;color:#64748B'>
    AI Powered Personal Finance Analytics Platform
    </p>
    """, unsafe_allow_html=True)

    st.markdown("""
    ## 👋 Welcome Back

    Upload your bank statement and let AI analyze your spending,
    savings, financial health and future expenses.
    """)

    uploaded_file = st.file_uploader(
        "📂 Upload Bank Statement",
        type=["csv", "xlsx"]
    )

    if uploaded_file is not None:

        df = load_data(uploaded_file)
        
        st.session_state.df = df

    df = st.session_state.df

    if df is None:

        st.info("Upload a CSV or Excel file to begin.")

        c1, c2, c3, c4 = st.columns(4)

        c1.metric("Income", "₹0")
        c2.metric("Expense", "₹0")
        c3.metric("Savings", "₹0")
        c4.metric("Health Score", "0/100")

    else:

        result = analyze_expenses(df)

        income = result["income"]
        expense = result["expense"]
        savings = result["savings"]

        score = calculate_health_score(
            income,
            expense,
            savings
        )

        c1, c2, c3, c4 = st.columns(4)

        c1.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">💰 Total Income</div>
            <div class="metric-value">₹{income:,.0f}</div>
        </div>
        """, unsafe_allow_html=True)

        c2.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">💸 Total Expense</div>
            <div class="metric-value">₹{expense:,.0f}</div>
        </div>
        """, unsafe_allow_html=True)

        c3.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">🏦 Savings</div>
            <div class="metric-value">₹{savings:,.0f}</div>
        </div>
        """, unsafe_allow_html=True)

        c4.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">❤️ Health Score</div>
            <div class="metric-value">{score}/100</div>
        </div>
        """, unsafe_allow_html=True)

        st.success(get_health_label(score))

        st.divider()

                # ==========================================================
        # Charts
        # ==========================================================

        left, right = st.columns(2)

        with left:
            st.plotly_chart(
                expense_pie_chart(df),
                use_container_width=True
            )

        with right:
            st.plotly_chart(
                monthly_trend_chart(df),
                use_container_width=True
            )

        st.divider()

        st.plotly_chart(
            income_vs_expense_chart(df),
            use_container_width=True
        )

        st.divider()

        left, right = st.columns(2)

        with left:
            st.plotly_chart(
                category_bar_chart(df),
                use_container_width=True
            )

        with right:
            merchant_fig = merchant_chart(df)

            if merchant_fig is not None:
                st.plotly_chart(
                    merchant_fig,
                    use_container_width=True
                )

        st.divider()

        st.plotly_chart(
            daily_expense_chart(df),
            use_container_width=True
        )

        # ==========================================================
        # Forecast
        # ==========================================================

        prediction = forecast_next_month(df)

        if prediction is not None:

            st.divider()

            st.subheader("📈 Spending Forecast")

            st.info(
                f"Estimated Next Month Expense: ₹{prediction:,.2f}"
            )

        # ==========================================================
        # Anomaly Detection
        # ==========================================================

        st.divider()

        st.subheader("🚨 Unusual Transactions")

        anomalies = detect_anomalies(df)

        if anomalies.empty:

            st.success(
                "✅ No unusual transactions detected."
            )

        else:

            st.warning(
                f"⚠ {len(anomalies)} unusual transaction(s) detected."
            )

            st.dataframe(
                anomalies,
                use_container_width=True,
                height=250
            )

        # ==========================================================
        # Transaction Preview
        # ==========================================================

        st.divider()

        st.subheader("📋 All Transactions")

        st.dataframe(
            df,
            use_container_width=True,
            height=350
        )

        # ==========================================================
# AI INSIGHTS
# ==========================================================

elif selected == "AI Insights":

    st.title("🤖 AI Financial Advisor")

    df = st.session_state.df

    if df is None:

        st.warning(
            "Please upload a bank statement from the Dashboard first."
        )

    else:

        st.info(
            "Gemini AI will analyze your financial data and provide personalized recommendations."
        )

        if st.button("Generate AI Report"):

            with st.spinner("Analyzing your finances..."):

                insights = generate_ai_insights(df)

            st.markdown("### 📑 Financial Report")
            st.info(insights)


# ==========================================================
# ASK AI
# ==========================================================

elif selected == "Ask AI":

    st.title("💬 Ask AI About Your Expenses")

    df = st.session_state.df

    if df is None:

        st.warning(
            "Please upload a bank statement from the Dashboard first."
        )

    else:

        question = st.text_input(
            "Ask a question about your transactions",
            placeholder="Example: How much did I spend on food?"
        )

        if st.button("Ask AI"):

            if question.strip() == "":

                st.warning("Please enter a question.")

            else:

                with st.spinner("Thinking..."):

                    answer = ask_finance_ai(
                        df,
                        question
                    )

                st.markdown("### 🤖 AI Response")
                st.markdown(f"""
<div style="
background:#F8FAFC;
padding:20px;
border-radius:15px;
border-left:5px solid #2563EB;
font-size:16px;
line-height:1.8;
">
{answer}
</div>
""", unsafe_allow_html=True)

# ==========================================================
# SETTINGS
# ==========================================================

elif selected == "Settings":

    st.title("⚙ Settings")

    st.subheader("Preferences")

    dark_mode = st.toggle(
        "Enable Dark Mode",
        value=True
    )

    show_animation = st.toggle(
        "Enable Animations",
        value=True
    )

    currency = st.selectbox(

        "Currency",

        [
            "₹ INR",
            "$ USD",
            "€ EUR"
        ]

    )

    st.divider()

    st.subheader("About FinSight AI")

    st.info(
        """
FinSight AI is an AI-powered Personal Finance Analytics Platform.

Features:

• Expense Analysis

• Spending Forecast

• AI Insights

• AI Chat Assistant

• Financial Health Score

• Anomaly Detection

Version: 1.0
"""
    )

    # ==========================================================
# FOOTER
# ==========================================================

st.markdown("---")

st.markdown(
    """
    <div style='text-align:center; color:#64748B; padding:15px;'>

    <h4>💰 FinSight AI</h4>

    AI Powered Personal Finance Analytics Platform

    Built with ❤️ using Streamlit, Plotly and Google Gemini AI

    </div>
    """,
    unsafe_allow_html=True
)

st.caption("Version 1.0.0")