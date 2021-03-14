import csv

import matplotlib.pyplot as plt


x = []
y = []

with open("result.csv") as f:
    rows = csv.DictReader(f)
    for row in rows:
        x.append(row['height'])
        y.append(row['avgFee'])
plt.plot(x, y)
plt.title('height vs avgFee')
plt.xlabel('height')
plt.ylabel('avgFee')
plt.show()
