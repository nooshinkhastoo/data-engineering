import numpy as np

temps = np.array([22, 25, 19, 30, 28, 31, 24, 18, 35, 27])

# 1
mask = temps > 28
print(f"Temperatures > 28 mask: {mask}")

# 2
high_temps = temps[mask]
print(f"Temperatures > 28: {high_temps}")

# 3
temps_with_nan = temps.astype(float)
temps_with_nan[temps_with_nan < 20] = np.nan
print(f"Temperatures with NaN:{temps_with_nan}")

# 4
avg_temp = np.nanmean(temps_with_nan)
print(f"Average temperature: {avg_temp}")