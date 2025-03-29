import plotly.express as px
import random

from die import Die

# Create two D6.
die_1 = Die()
die_2 = Die()

# Make some rolls, and store results in a list.
def generator_kockice(n):
    for i in range(n):
        yield random.randit(1,6)
bacanja = generator_kockice(1000)

# Analize the results.
frequencies = []
max_result = die_1.num_sides + die_2.num_sides
poss_results = range(2, max_result+1)
for value in poss_results:
    frequency = results.count(value)
    frequencies.append(frequency)

# Visualise the results.
title = "Results of Rolling Two D6 Dice 1,000 Times"
labels = {"x": "Result", "y": "Frequency of Result"}
fig = px.bar(x=poss_results, y=frequencies, title=title, labels=labels)

# Further customize chart.
fig.update_layout(xaxis_dtick=1)

fig.show()