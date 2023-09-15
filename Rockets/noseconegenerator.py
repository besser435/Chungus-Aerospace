import math
import os
# Nose cone radius and length (cm)
R = 7.84 / 2 -0.14
L = 15 - 0.14

datapointcount = 200

for i in range(datapointcount + 1):
    x = L * i / datapointcount
    y = (R / math.sqrt(math.pi)) * math.sqrt(math.acos(1 - (2*x / L)) - math.sin(2 * math.acos(1 - (2*x / L))) / 2)

    with open("cone.csv", "a") as f:
        f.write(f"{x},{y},{0}\n")