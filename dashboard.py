import streamlit as st
import pandas as pd

from src.analysis.spending_aggregation import compute_spending_aggregates
from src.feasibility.savings_engine import evaluate_savings_feasibility
from src.genai.explanation_engine import generate_savings_explanation
from src.features.date_features import add_date_features
from src.categorization.recurring_detection import detect_recurring_merchants
from src.analysis.recurring_split import split_fixed_habitual

import plotly.express as px


# --------------------- STREAMLIT APP ---------------------

st.set_page_config(page_title="Spending Behavior Analyser",
                   layout="wide")

st.markdown("""
    <style>
    [data-testid="stMetricValue"] {
        font-size: 20px;
        font-weight: 500;
    }
    [data-testid="stMetricLabel"] {
        font-size: 16px;
        font-weight: 400;
        color: #BBBBBB;
    }
    </style>
""", unsafe_allow_html=True)

st.title("💰 Spending Behavior & Savings Feasibility Dashboard")

uploaded = st.file_uploader("Upload your bank statement CSV", type="csv")

# ----- INPUT: Savings goal -----
target_savings = st.number_input("Target monthly savings (₹)", value=20000, min_value=0)


if uploaded:
    df = pd.read_csv(uploaded)

    df = add_date_features(df)


    monthly_income = (
    df[df["credit_amount"] > 0]
    .groupby("year_month")["credit_amount"]
    .sum()
    .mean()
    )

    recurring_merchants = detect_recurring_merchants(df)

    recurring_split = split_fixed_habitual(df, recurring_merchants)

    fixed_monthly = recurring_split["fixed_monthly_avg"]
    habitual_monthly = recurring_split["habitual_monthly_avg"]

    spend_stats = compute_spending_aggregates(df)

    # ----- STEP 2: RUN SAVINGS ENGINE -----
    result = evaluate_savings_feasibility(
        monthly_income=monthly_income,
        fixed_monthly=fixed_monthly,
        habitual_monthly=habitual_monthly,
        total_spend=spend_stats["monthly_total_spend"],
        target_savings=target_savings
    )


    # ==================== DASHBOARD UI ====================

    # ----- KPIs -----
    st.subheader("📌 Monthly Summary")

    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric("Income (₹)", f"{monthly_income:,.0f}")
    col2.metric("Spend (₹)", f"{spend_stats['monthly_total_spend']:,.0f}")
    col3.metric("Available to Save (₹)", f"{result['available_to_save']:,.0f}")
    col4.metric("Target Savings (₹)", f"{target_savings:,.0f}")
    col5.metric("Status", result["feasibility"])


    # ----- FIXED vs HABITUAL -----
    st.subheader("📊 Spending Breakdown")

    breakdown_df = pd.DataFrame({
        "Type": ["Fixed", "Habitual"],
        "Amount (₹)": [fixed_monthly, habitual_monthly]
    })

    fig_breakdown = px.pie(breakdown_df, names="Type", values="Amount (₹)",
                           title="Fixed vs Habitual Monthly Spend")
    st.plotly_chart(fig_breakdown, use_container_width=True)


    # ----- WEEKDAY vs WEEKEND -----
    st.subheader("🗓️ Weekday vs Weekend Spend")

    fig_days = px.bar(
        x=["Weekend", "Weekday"],
        y=[spend_stats["weekend_total"], spend_stats["weekday_total"]],
        title="Total Spend: Weekend vs Weekday",
        labels={"x": "Day Type", "y": "Spend (₹)"}
    )
    st.plotly_chart(fig_days, use_container_width=True)

    # ----- TOP MERCHANTS / DESCRIPTION BREAKDOWN -----
    st.subheader("🏪 Top Spending Categories (Merchants)")

    # group by description and sum debit amounts
    merchant_spend = (
        df.groupby("description")["debit_amount"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    fig_merchants = px.bar(
        merchant_spend,
        x="debit_amount",
        y="description",
        orientation="h",
        title="Top 10 Spending Categories",
        labels={"debit_amount": "Total Spend (₹)", "description": "Merchant"},
    )

    fig_merchants.update_layout(yaxis=dict(categoryorder='total ascending'))

    st.plotly_chart(fig_merchants, use_container_width=True)

    # ----- DAILY SPEND TREND -----
    st.subheader("📈 Daily Spend Trend")

    df["date"] = pd.to_datetime(df["date"])
    daily_spend = df.groupby("date")["debit_amount"].sum().reset_index()

    fig_trend = px.line(daily_spend, x="date", y="debit_amount",
                        title="Daily Debit Spend")
    st.plotly_chart(fig_trend, use_container_width=True)


    # ----- GENAI EXPLANATION -----
    st.subheader("🧠 Insights")

    if st.button("Generate Natural-Language Summary"):
        explanation = generate_savings_explanation(result)
        st.write(explanation)

else:
    st.info("Upload a CSV file to view your dashboard.")
