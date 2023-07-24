#Literally just the regular code with the calibration part removed

import board, time, busio, math, adafruit_icm20x
import accel_cfg as cfg
i2c = busio.I2C(board.SCL1, board.SDA1)
icm = adafruit_icm20x.ICM20649(i2c)
adafruit_icm20x.ICM20649.accelerometer_range = 30
adafruit_icm20x.accelerometer_data_rate = 5000

#Measurement setup
initial_time = time.monotonic()
vel_0x = 0
vel_0y = 0
vel_0z = 0
vel_mag0 = 0
time_0 = 0
accel_0x = icm.acceleration[0] - cfg.accel_x_offset
accel_0y = icm.acceleration[1] - cfg.accel_y_offset
accel_0z = icm.acceleration[2] - cfg.accel_z_offset

while True: #accel_mag > 30 or vel_0 > 10: for actual flight
    current_time = time.monotonic()
    time_1 = current_time - initial_time
    
    icm_accel = icm.acceleration
    accel_1x, accel_1y, accel_1z = icm_accel
    
    vel_1x = vel_0x + (accel_1x + accel_0x - cfg.accel_x_offset) * (time_1 - time_0) * 0.5
    vel_1y = vel_0y + (accel_1y + accel_0y - cfg.accel_y_offset) * (time_1 - time_0) * 0.5
    vel_1z = vel_0y + (accel_1z + accel_0z - cfg.accel_z_offset) * (time_1 - time_0) * 0.5
    vel_mag = math.sqrt(pow(vel_1x, 2) + pow(vel_1y, 2) + pow(vel_1z, 2)) - cfg.g * (time_1 - time_0)

    #Redefining variables for next step
    delta_v = vel_mag - vel_mag0 #vel_mag0 only exists for this step and should probably be removed for the actual flight
    time_0 = time_1
    vel_0x = vel_1x
    vel_0y = vel_1y
    vel_0z = vel_1z
    accel_0x = accel_1x
    accel_0y = accel_1y
    accel_0z = accel_1z
    vel_mag0 = vel_mag
    print(f"accel data: {str(icm_accel)} accel magnitude: {str(math.sqrt(pow(accel_1x - cfg.accel_x_offset, 2) + pow(accel_1y - cfg.accel_y_offset, 2) + pow(accel_1z - cfg.accel_z_offset)))} integrated accel data (v): {str(vel_1x)} {str(vel_1y)} {str(vel_1z)} velocity magnitude: {str(vel_mag)} dv: {str(delta_v)} time: {str(time_1)}")