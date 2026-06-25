import numpy as np
import pandas as pd

sales = np.array([
    [120, 135, 150, 160, 145, 170, 180],
    [130, 140, 155, 165, 150, 175, 190]
])

days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

# 1
df = pd.DataFrame(
    sales,
    index=["Week1", "Week2"],
    columns=days
)

print(f"Sales DataFrame:\n{df}")

# 2
weekly_sales = df.sum(axis=1)
print(f"\nTotal sales per week:\n{weekly_sales}")

# 3
daily_sales = df.sum(axis=0)
print(f"\nTotal sales per day:\n{daily_sales}")

# 4
best_day = daily_sales.idxmax()
print(f"\nDay with highest sales: {best_day}")

# 5
average_sales = df.values.mean()

high_sales_days = df[df > average_sales]

print(f"\nAverage sales: {average_sales}")
print(f"\nSales greater than average:\n{high_sales_days}")