import random
# generate RNG altitude numbers for a flight in the shape of a parabola

# options
flight_time = 20  # seconds from ignition to landing
data_cycles_s = 30  # data cycles per second

"""
Scratch this for now. 

# storage
time = [0]
altitude = [0]
def rng():
    return round(random.uniform(0, 8), 2)
for i in range(flight_time):
    altitude.append(rng() + altitude[i])
print(altitude)
#print(rng())
rng()"""


altitude = [0]
# maybe start with a parabola, then take those numbers and randomize them slightly
