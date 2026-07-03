import pandas as pd
import matplotlib.pyplot as plt

# ==========================
# Load and Prepare Data
# ==========================

df = pd.read_csv("traffic_violations.csv")

df["violation_datetime"] = pd.to_datetime(df["violation_datetime"])

df["Year"] = df["violation_datetime"].dt.year
df["Month"] = df["violation_datetime"].dt.month
df["Hour"] = df["violation_datetime"].dt.hour

df["plate_number"] = df["plate_number"].str.upper()

df["speed_over_limit"] = (
    df["measured_speed_kmh"] - df["speed_limit_kmh"]
)

# ==========================
# Data for Charts
# ==========================

monthly = df.groupby("Month")["violation_id"].count()

city_summary = (
    df.groupby("city")
      .agg(
          average_fine=("fine_amount_irr", "mean"),
          payment_rate=("paid", "mean"),
          total_violations=("violation_id", "count")
      )
)

city_summary["payment_rate"] *= 100

# ==========================
# Figure with 3 Subplots
# ==========================

fig, axes = plt.subplots(3, 1, figsize=(12, 16))

# ==================================================
# 1. Monthly Line Chart
# ==================================================

axes[0].plot(
    monthly.index,
    monthly.values,
    marker="o",
    linewidth=2
)

axes[0].set_title("Monthly Traffic Violations")
axes[0].set_xlabel("Month")
axes[0].set_ylabel("Number of Violations")
axes[0].grid(True)

max_month = monthly.idxmax()
max_value = monthly.max()

axes[0].annotate(
    "Highest",
    xy=(max_month, max_value),
    xytext=(max_month + 0.3, max_value + 1000),
    arrowprops=dict(arrowstyle="->")
)

# ==================================================
# 2. Histogram
# ==================================================

axes[1].hist(
    df["speed_over_limit"],
    bins=30,
    color="skyblue",
    edgecolor="black",
    label="Speed Over Limit"
)

axes[1].set_title("Distribution of Speed Over Limit")
axes[1].set_xlabel("Speed Over Limit (km/h)")
axes[1].set_ylabel("Frequency")
axes[1].legend()
axes[1].grid(True)

# ==================================================
# 3. Scatter Plot
# ==================================================

scatter = axes[2].scatter(
    city_summary["average_fine"],
    city_summary["payment_rate"],
    s=city_summary["total_violations"] / 200,
    alpha=0.7
)

axes[2].set_title("Average Fine vs Payment Rate")
axes[2].set_xlabel("Average Fine (IRR)")
axes[2].set_ylabel("Payment Rate (%)")
axes[2].grid(True)

for city, row in city_summary.iterrows():
    axes[2].annotate(
        city,
        (row["average_fine"], row["payment_rate"])
    )

plt.tight_layout()
plt.show()