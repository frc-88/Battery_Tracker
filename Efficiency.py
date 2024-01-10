import pandas as pd
df = pd.read_csv("tj-battery_1.csv")

voltage = df["voltage"]
current = df["pdp_current"]

df["time_change"] = df["timestamp"].diff()

df["energy"] = df["voltage"] * df["pdp_current"] * df["time_change"]

total_energy = df["energy"].sum()

