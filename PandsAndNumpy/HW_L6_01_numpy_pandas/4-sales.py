import pandas as pd

data = {
    "product": ["A", "B", "C", "A", "B", "C"],
    "store": ["X", "X", "X", "Y", "Y", "Y"],
    "sales": [120, 150, 90, 200, 130, 160]
}

df = pd.DataFrame(data)

# 1
product_sales = df.groupby("product")["sales"].sum()
print(f"Total sales for each product: {product_sales}")

# 2
store_avg = df.groupby("store")["sales"].mean()
print(f"\nAverage sales for each store: {store_avg}")

# 3
high_sales = df[df["sales"] > 120]
print(f"\nSales greater than 120: {high_sales}")

# 4
df["sales_normalized"] = df["sales"] / df["sales"].max()

print(f" DataFrame with normalized sales: {df}")