import pandas as pd

# Load CSV
df = pd.read_csv("traffic_violations.csv")

# Data Cleaning
df["violation_datetime"] = pd.to_datetime(df["violation_datetime"])

df["Year"] = df["violation_datetime"].dt.year
df["Month"] = df["violation_datetime"].dt.month
df["Hour"] = df["violation_datetime"].dt.hour

df["plate_number"] = df["plate_number"].str.upper()

df["speed_over_limit"] = (
    df["measured_speed_kmh"] - df["speed_limit_kmh"]
)

# =========================
# Analysis by City
# =========================

city_summary = (
    df.groupby("city")
    .agg(
        total_violations=("violation_id", "count"),
        average_fine=("fine_amount_irr", "mean"),
        paid_percentage=("paid", "mean"),
    )
)

city_summary["paid_percentage"] *= 100

print("===== City Summary =====")
print(city_summary)

# =========================
# Analysis by Vehicle Type
# =========================

vehicle_summary = (
    df.groupby("vehicle_type")
    .agg(
        total_violations=("violation_id", "count"),
        average_speed_over_limit=("speed_over_limit", "mean"),
    )
)

print("\n===== Vehicle Summary =====")
print(vehicle_summary)