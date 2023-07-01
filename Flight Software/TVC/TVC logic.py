#Quaternion logic for TVC using ICM20649 IMU
import board
import time
import busio
import math
import adafruit_icm20x
import numpy as np
import scipy

import tvc_cfg as tvc

i2c = board.i2c
icm = adafruit_icm20x.ICM20649(i2c)
time_initial = time.monotonic()
quat_initial = np.array([1, 0, 0, 0]) #Defines initial reference relative to earth

time_0 = time_initial

while True:
    angular_vx_uncorrected, angular_vy_uncorrected, angular_vz_uncorrected = icm.gyro
    angular_vx = angular_vx_uncorrected - tvc.gyro_x_offset
    angular_vy = angular_vy_uncorrected - tvc.gyro_y_offset
    angular_vz = angular_vz_uncorrected - tvc.gyro_z_offset

    #IMU Kalman filter
    filt_angular_vx = angular_vx
    filt_angular_vy = angular_vy
    filt_angular_vz = angular_vz #PLACEHOLDER FOR KALMAN FILTER
    #Representation as quaternions
    quat_v = np.array([0, filt_angular_vx, filt_angular_vy, filt_angular_vz])
    quat_v_relative = np.tensordot(0.5 * quat_initial, quat_v, axes=0)

    time_1 = time.monotonic
    d_quat_orientation = quat_v_relative * (time_1 - time_0)
    dquat_1, dquat_2, dquat_3, dquat_4 = d_quat_orientation
    norm = math.sqrt(dquat_1**2 + dquat_2**2 + dquat_3**2 + dquat_4**2)
    quat_orientation_normalized = d_quat_orientation / norm
    
    #Conversion to Euler angles (radians)
    quat_1, quat_2, quat_3, quat_4 = quat_orientation_normalized
    Euler_psi = math.atan2(2 * (quat_2 * quat_3 + quat_1 * quat_4), quat_1**2 + quat_2**2 - quat_3**2 - quat_4**2)
    Euler_theta = math.asin(2 * (quat_2 * quat_4 - quat_1 * quat_3))
    Euler_phi = math.atan2(2 * (quat_1 * quat_2 + quat_3 * quat_4), quat_1**2 - quat_2**2 - quat_3**2 + quat_4**2) 

    print("Normalized quaternion: ", str(quat_orientation_normalized), " ", "Psi: ", str(Euler_psi), " ", "Theta: ", str(Euler_theta), " ", "Phi: " (Euler_phi))

    time_0 = time_1
