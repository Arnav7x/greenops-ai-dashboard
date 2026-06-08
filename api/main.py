from fastapi import FastAPI
import pandas as pd
import joblib
import os

app = FastAPI(title="GreenOps API")

DATASET_PATH = os.getenv(
    "DATASET_PATH",
    "data/cloud_usage_enriched.csv"
)

MODEL_PATH = os.getenv(
    "MODEL_PATH",
    "model/co2e_model.pkl"
)

df = pd.read_csv(
    DATASET_PATH,
    parse_dates=["date"]
)

model = joblib.load(
    MODEL_PATH
)

@app.get("/health")
def health():
    """Liveness probe."""
    return {"status": "ok"}

@app.get("/metrics/summary")
def summary():
    """Summary sustainability metrics."""

    total_co2e = float(
        df["co2e_kg"].sum()
    )

    total_cost = float(
        df["cost_usd"].sum()
    )

    top_team = (
        df.groupby("team")["co2e_kg"]
        .sum()
        .idxmax()
    )

    top_region = (
        df.groupby("region")["co2e_kg"]
        .sum()
        .idxmax()
    )

    return {
        "total_co2e": total_co2e,
        "total_cost": total_cost,
        "top_team": top_team,
        "top_region": top_region,
    }

@app.get("/metrics/daily")
def daily_metrics():
    """Daily CO2e trend."""

    daily = (
        df.groupby("date")["co2e_kg"]
        .sum()
        .reset_index()
    )

    return daily.to_dict(
        orient="records"
    )

@app.get("/forecast")
def forecast():
    """30 day forecast."""

    daily = (
        df.groupby("date")["co2e_kg"]
        .sum()
        .reset_index()
    )

    daily["lag_7"] = daily["co2e_kg"].shift(7)
    daily["lag_14"] = daily["co2e_kg"].shift(14)
    daily["rolling_7"] = (
        daily["co2e_kg"]
        .rolling(7)
        .mean()
    )

    daily["dow"] = (
        daily["date"]
        .dt.dayofweek
    )

    daily = daily.dropna()

    latest = daily.iloc[-1]

    X = [[
        latest["lag_7"],
        latest["lag_14"],
        latest["rolling_7"],
        latest["dow"]
    ]]

    prediction = float(
        model.predict(X)[0]
    )

    return {
        "forecast_30_days":
            [prediction] * 30
    }