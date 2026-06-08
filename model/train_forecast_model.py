import pandas as pd
import matplotlib.pyplot as plt
import joblib
import numpy as np

from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

# Load enriched dataset
df = pd.read_csv(
    "data/cloud_usage_enriched.csv",
    parse_dates=["date"]
)

# Aggregate daily CO2e
daily = (
    df.groupby("date")["co2e_kg"]
    .sum()
    .reset_index()
)

# Feature Engineering
daily["lag_7"] = daily["co2e_kg"].shift(7)
daily["lag_14"] = daily["co2e_kg"].shift(14)
daily["rolling_7"] = daily["co2e_kg"].rolling(7).mean()
daily["dow"] = daily["date"].dt.dayofweek

# Drop NaNs
daily = daily.dropna()

# Features and target
X = daily[["lag_7", "lag_14", "rolling_7", "dow"]]
y = daily["co2e_kg"]

# Last 30 days = test
X_train = X.iloc[:-30]
X_test = X.iloc[-30:]

y_train = y.iloc[:-30]
y_test = y.iloc[-30:]

# Train model
model = LinearRegression()
model.fit(X_train, y_train)

# Predict
y_pred = model.predict(X_test)

# RMSE
mse = mean_squared_error(
    y_test,
    y_pred
)

rmse = np.sqrt(mse)

print("RMSE:", rmse)

# Mean daily CO2e
mean_daily = y_test.mean()

print("Mean Daily CO2e:", mean_daily)

error_percent = (rmse / mean_daily) * 100

print("Error %:", error_percent)

# Plot
plt.figure(figsize=(10, 5))

plt.plot(
    y_test.values,
    label="Actual"
)

plt.plot(
    y_pred,
    label="Predicted"
)

plt.title("Actual vs Predicted CO2e")
plt.xlabel("Days")
plt.ylabel("CO2e (kg)")
plt.legend()

plt.tight_layout()

plt.savefig(
    "model/forecast_plot.png"
)

plt.close()

# Save model
joblib.dump(
    model,
    "model/co2e_model.pkl"
)

print("Model saved.")