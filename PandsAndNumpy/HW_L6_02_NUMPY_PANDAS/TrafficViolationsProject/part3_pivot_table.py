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

# Pivot Table
pivot = pd.pivot_table(
    df,
    index="city",
    columns="violation_type",
    values="violation_id",
    aggfunc="count",
    fill_value=0,
)

print("===== Pivot Table =====")
print(pivot)

# Normalize to percentage
pivot_percent = pivot.div(pivot.sum(axis=1), axis=0) * 100

print("\n===== Normalized Pivot (%) =====")
print(pivot_percent)

# Most common violation
top_violation = pivot_percent.idxmax(axis=1)

print("\n===== Most Common Violation =====")
print(top_violation)