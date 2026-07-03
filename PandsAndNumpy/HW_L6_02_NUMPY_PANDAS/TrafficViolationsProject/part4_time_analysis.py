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

# =====================
# Monthly Analysis
# =====================

monthly_violations = (
    df.groupby("Month")
    .agg(
        total_violations=("violation_id", "count")
    )
)

print("===== Monthly Violations =====")
print(monthly_violations)

# =====================
# Hourly Analysis
# =====================

hourly_violations = (
    df.groupby("Hour")
    .agg(
        total_violations=("violation_id", "count")
    )
)

print("\n===== Hourly Violations =====")
print(hourly_violations)

# =====================
# Peak Hour
# =====================

peak_hour = hourly_violations["total_violations"].idxmax()

print("\n===== Peak Hour =====")
print(f"Most violations occur at hour: {peak_hour}")