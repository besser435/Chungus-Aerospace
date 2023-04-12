#Quaternion logic for TVC using ICM20649 IMU
import board
import time
import busio
import math
import adafruit_icm20x
import numpy as np
import scipy
from filterpy.kalman import KalmanFilter

i2c = board.i2c
icm = adafruit_icm20x.ICM20649(i2c)
time_initial = time.monotonic()
quat_initial = np.array[1, 0, 0, 0] #Defines initial reference relative to earth

time_0 = time_initial
while True:
    angular_vx, angular_vy, angular_vz = icm.gyro

    #IMU Kalman filter
    filt_angular_vx = angular_vx
    filt_angular_vy = angular_vy
    filt_angular_vz = angular_vz #PLACEHOLDER FOR KALMAN FILTER
    #Representation as quaternions
    quat_v = np.array[0, filt_angular_vx, filt_angular_vy, filt_angular_vz]
    quat_v_relative = np.tensordot(0.5 * quat_initial, quat_v, axes=0)

    time_1 = time.monotonic
    d_quat_orientation = quat_v_relative * (time_1 - time_0)
    quat_normalized = 

