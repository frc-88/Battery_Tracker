import pandas as pd
i = -1
# Read the CSV file
df = pd.read_csv("tj-battery_1.csv")

# Calculate time change
df["time_change"] = df["timestamp"].diff()

# Calculate power
df["power"] = df["pdp_voltage"] * df["pdp_current"] * df["time_change"]

# Calculate total energy
total_energy = df["power"].sum()

# Calculate delta voltage directly (no loop needed)
delta_voltage = df["pdp_voltage"].iloc[i] - df["pdp_voltage"].iloc[0]

# Handle potential zero division
while delta_voltage == 0:
    i = i -1
    delta_voltage = df["pdp_voltage"].iloc[i] - df["pdp_voltage"].iloc[0]
      # Cannot calculate efficiency if there's no voltage change
else:
    efficiency = total_energy / delta_voltage

# Print the efficiency (or indicate if it's not calculable)
print(efficiency)