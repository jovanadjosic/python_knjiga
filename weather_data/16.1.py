from pathlib import Path
import csv
from datetime import datetime

import matplotlib.pyplot as plt

path = Path("sitka_weather_2021_full.csv")
lines = path.read_text().splitlines()

reader = csv.reader(lines)
header_row = next(reader)

for index, column_header in enumerate(header_row):
    print(index, column_header)

# Extract dates and high temperatures.
rainfall, dates = [], []
for row in reader:
    current_date = datetime.strptime(row[2], "%Y-%m-%d")
    try:
        rainfall_value = int(row[5])
    except ValueError:
        print(f"Missing data for {current_date}")
    else:
        dates.append(current_date)
        rainfall.append(rainfall_value)

# Plot the high temperatures.
plt.style.use("seaborn-v0_8")
fig, ax = plt.subplots()
ax.plot(dates, rainfall, color="blue")

# Format plot
ax.set_title("Daily Rainfall, 2021", fontsize=24)
ax.set_xlabel("", fontsize=16)
fig.autofmt_xdate()
ax.set_ylabel("Daily Rainfall", fontsize=16)
ax.tick_params(labelsize=16)

plt.show()
