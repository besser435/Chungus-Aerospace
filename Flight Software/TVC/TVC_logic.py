import board
import time
import busio
import math
import adafruit_icm20x
import numpy as np
#import scipy
import tvc_cfg as cfg

"""Quaternion logic for TVC using ICM20649 IMU"""

#i2c = busio.I2C(board.SCL1, board.SDA1)
#icm = adafruit_icm20x.ICM20649(i2c)

time_initial = time.monotonic()
quat_initial = np.array([1, 0, 0, 0])   # Defines initial reference relative to earth
quat_orientation_int = quat_initial    # Sets initial conditions for integration
radconv = 3.14159265358979 / 180    # Radian conversion constant

time_0 = time.monotonic()
time.sleep(0.05) # Exists to prevent nan errors due to time_1 - time_0 being considered equal to 0, can be commented out if program runs slower than 100Hz
while True:
    # Rate gyro values
    angular_vx_uncorrected = 0#icm.gyro[0]
    angular_vy_uncorrected = 0#icm.gyro[1]
    angular_vz_uncorrected = 1#icm.gyro[2]
    angular_vx = angular_vx_uncorrected #- cfg.gyro_x_offset_deg
    angular_vy = angular_vy_uncorrected #- cfg.gyro_y_offset_deg
    angular_vz = angular_vz_uncorrected #- cfg.gyro_z_offset_deg

    # IMU Kalman filter
    filt_angular_vx = angular_vx
    filt_angular_vy = angular_vy
    filt_angular_vz = angular_vz #PLACEHOLDER FOR KALMAN FILTER
    
    quat_v = np.array([0, filt_angular_vx, filt_angular_vy, filt_angular_vz]) * radconv # Representation of angular velocity measurements as quaternions
    # Quaternion multiplication
        # Product for each element
    quat_v_relative_1 = quat_initial[0] * quat_v[0] - quat_initial[1] * quat_v[1] - quat_initial[2] * quat_v[2] - quat_initial[3] * quat_v[3]
    quat_v_relative_2 = quat_initial[0] * quat_v[1] + quat_initial[1] * quat_v[0] + quat_initial[2] * quat_v[3] - quat_initial[3] * quat_v[2]
    quat_v_relative_3 = quat_initial[0] * quat_v[2] - quat_initial[1] * quat_v[3] + quat_initial[2] * quat_v[0] + quat_initial[3] * quat_v[1]
    quat_v_relative_4 = quat_initial[0] * quat_v[3] + quat_initial[1] * quat_v[2] - quat_initial[2] * quat_v[1] + quat_initial[3] * quat_v[0]
    
    quat_v_relative = np.array([quat_v_relative_1, quat_v_relative_2, quat_v_relative_3, quat_v_relative_4]) * 0.5  # Array with each new quaternion element, representing change relative to earth

    time_1 = time.monotonic()
    quat_orientation_int = np.add(quat_orientation_int, quat_v_relative * (time_1 - time_0))    # Riemann sum integral 
    norm = math.sqrt(quat_orientation_int[0]**2 + quat_orientation_int[1]**2 + quat_orientation_int[2]**2 + quat_orientation_int[3]**2) # Normalization for quaternion
    quat_orientation = quat_orientation_int / norm   # Final quaternion measurement
    
    # Conversion to Euler angles (radians)
    quat_1, quat_2, quat_3, quat_4 = quat_orientation
    Euler_phi = math.atan2(2 * (quat_1 * quat_2 + quat_3 * quat_4), quat_1**2 - quat_2**2 - quat_3**2 + quat_4**2)  # x axis when in initial orientation
    Euler_theta = math.asin(2 * (quat_2 * quat_4 - quat_1 * quat_3))    # y axis when in initial orientation   
    Euler_psi = math.atan2(2 * (quat_2 * quat_3 + quat_1 * quat_4), quat_1**2 + quat_2**2 - quat_3**2 - quat_4**2)  # z axis when in initial orientation



    # TODO maybe add line breaks so this looks a bit better
    print(f"Quaternion orientation: {quat_orientation} Psi: {Euler_psi} Theta: {Euler_theta} Phi: {Euler_phi} (rad)")
    time_0 = time_1
    quat_initial = quat_orientation
    time.sleep(0.05)    # Exists to prevent nan errors when running faster than 100Hz, can be commented out when running slower