import pandas as pd
import matplotlib.pyplot as plt

# 1. Load the CSV file
df = pd.read_csv("traffic_violations.csv")

# 2. Convert violation_datetime to datetime
df["violation_datetime"] = pd.to_datetime(df["violation_datetime"])

# 3. Create Year, Month, and Hour columns
df["Year"] = df["violation_datetime"].dt.year
df["Month"] = df["violation_datetime"].dt.month
df["Hour"] = df["violation_datetime"].dt.hour

# 4. Convert plate numbers to uppercase
df["plate_number"] = df["plate_number"].str.upper()

# 5. Create speed_over_limit column
df["speed_over_limit"] = (
    df["measured_speed_kmh"] - df["speed_limit_kmh"]
)

# Display first 5 rows to verify the results
print(
    df[
        [
            "violation_datetime",
            "Year",
            "Month",
            "Hour",
            "plate_number",
            "speed_limit_kmh",
            "measured_speed_kmh",
            "speed_over_limit",
        ]
    ].head()
)