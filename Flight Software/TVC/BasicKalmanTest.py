import board
import time
import busio
import math
import adafruit_icm20x
import numpy as np
import scipy
from filterpy.kalman import kalman_filter, predict, update


i2c = board.i2c
icm = adafruit_icm20x.ICM20649(i2c)

#No idea what these do except uncertainty. Setting them to None should hopefully get it to handle itself
F = None #Transition state matrix
R = None #Uncertainty
Q = None #Process noise matrix

#Kalman filter loop using acceleration data as an example
while True:
    z, R = icm.acceleration
    x, P = predict(x, P, F, Q)
    x, P = update(x, P, z, R)
    
    print("z: " str(z), " ", "x: " str(x))
