import streamlit as st
import pandas as pd
import requests

API_URL = "http://127.0.0.1:8003"

st.set_page_config(
    page_title="GreenOps Dashboard",
    layout="wide"
)

st.title("🌱 GreenOps Sustainability Dashboard")

# -------------------------
# Summary Metrics
# -------------------------

summary = requests.get(
    f"{API_URL}/metrics/summary"
).json()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total CO2e (kg)",
        round(summary["total_co2e"], 2)
    )

with col2:
    st.metric(
        "Total Cost ($)",
        round(summary["total_cost"], 2)
    )

with col3:
    st.metric(
        "Top Team",
        summary["top_team"]
    )

with col4:
    st.metric(
        "Top Region",
        summary["top_region"]
    )

st.divider()

# -------------------------
# Daily Trend
# -------------------------

st.subheader("Daily CO2e Trend")

daily = requests.get(
    f"{API_URL}/metrics/daily"
).json()

daily_df = pd.DataFrame(daily)

daily_df["date"] = pd.to_datetime(
    daily_df["date"]
)

daily_df = daily_df.sort_values(
    "date"
)

st.line_chart(
    daily_df.set_index("date")["co2e_kg"]
)

st.divider()

# -------------------------
# Forecast
# -------------------------

st.subheader("30-Day Forecast")

if st.button("Generate Forecast"):

    forecast = requests.get(
        f"{API_URL}/forecast"
    ).json()

    forecast_df = pd.DataFrame(
        forecast["forecast_30_days"],
        columns=["predicted_co2e"]
    )

    st.line_chart(
        forecast_df
    )

    st.dataframe(
        forecast_df
    )