import pandas as pd

data = {
    "student": ["A", "B", "C", "D", "E"],
    "math": [90, 85, None, 70, 88],
    "physics": [None, 80, 78, 65, 92],
    "chemistry": [85, None, 82, 60, None]
}

df = pd.DataFrame(data)

# 1
missing_values = df.isna().sum()
print(f"Missing values in each column:\n{missing_values}")

# 2
df_filled = df.copy()

df_filled["math"] = df_filled["math"].fillna(df_filled["math"].mean())
df_filled["physics"] = df_filled["physics"].fillna(df_filled["physics"].mean())
df_filled["chemistry"] = df_filled["chemistry"].fillna(df_filled["chemistry"].mean())

print(f"\nDataFrame after filling missing values:\n{df_filled}")

# 3
df_filled["average"] = df_filled[["math", "physics", "chemistry"]].mean(axis=1)

print(f"\nStudent averages:\n{df_filled[['student', 'average']]}")

# 4
best_student = df_filled.loc[df_filled["average"].idxmax(),"student"]

print(f"\nBest student: {best_student}")