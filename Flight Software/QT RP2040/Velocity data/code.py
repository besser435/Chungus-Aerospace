import board, time, busio, math, adafruit_icm20x
i2c = busio.I2C(board.SCL1, board.SDA1)
icm = adafruit_icm20x.ICM20649(i2c)
adafruit_icm20x.ICM20649.accelerometer_range = 4
adafruit_icm20x.accelerometer_data_rate = 5000

version = 1.2

# Variables for determining acceleration/velocity
g_divisor = 1
cum_g = 0

time.sleep(5)

# Accelerometer g calibration (finds average g measurements to account for accelerometer fuckiness)
for i in range(2000):
    accel_x, accel_y, accel_z = icm.acceleration

    accel_mag = math.sqrt(pow(accel_x, 2) + pow(accel_y, 2) + pow(accel_z, 2))
    cum_g += accel_mag
    g = cum_g / g_divisor
    g_divisor += 1

    print(str(g))
    #if accel_mag > 30:
        #pass

adafruit_icm20x.ICM20649.accelerometer_range = 30
initial_time = time.monotonic()
vel_0 = 0
time_0 = 0
accel_0 = g

# Ascent mode
while True: #accel_mag > 30 or v0 > 10:
    current_time = time.monotonic()
    time_1 = current_time - initial_time
    
    icm_accel = icm.acceleration
    accel_x, accel_y, accel_z = icm_accel
    
    accel_mag = math.sqrt(pow(accel_x, 2) + pow(accel_y, 2) + pow(accel_z, 2))
    # USE WITH Z AXIS FACING (UP) OR ACCELEROMETER WILL GET CONFUSED

    if accel_z < 0:
        accel_sign = -1
    else:
        accel_sign = 1
    accel_1 = accel_mag * accel_sign
    vel_1 = vel_0 + (accel_1 + accel_0 - 2 * g) * (time_1 - time_0) * 0.5
    delta_v = vel_1 - vel_0
    time_0 = time_1
    vel_0 = vel_1
    accel_0 = accel_1

    print("accel data: " + str(icm_accel) + " " + str(accel_mag) + " " + str(vel_1) + " " + str(delta_v) + " " + str(time_1))
    
    
"""with open("data.csv", "a") as f:
    f.write()
    print("wrote data")"""