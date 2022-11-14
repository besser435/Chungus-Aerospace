import board, time, busio, math, adafruit_icm20x
i2c = busio.I2C(board.SCL1, board.SDA1)
icm = adafruit_icm20x.ICM20649(i2c)
adafruit_icm20x.ICM20649.accelerometer_range = 4
adafruit_icm20x.accelerometer_data_rate = 5000

version = 1.1

# Variables for determining acceleration/velocity
g_divisor = 1
cum_g = 0

time.sleep(5)
# Accelerometer calibration (which axis is up)
#up_axis = max(abs(icm.acceleration[0]), abs(icm.acceleration[1]), abs(icm.acceleration[2]))

# Accelerometer g calibration
for i in range(2000):
    icm_accel = icm.acceleration
    accel_x = icm_accel[0]
    accel_y = icm_accel[1]
    accel_z = icm_accel[2]

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
accel_0 = 0

# Ascent mode
while True: #accel_mag > 30 or v0 > 10:
    icm_accel = icm.acceleration
    current_time = time.monotonic()
    time_stamp = current_time - initial_time
    accel_x = icm_accel[0]
    accel_y = icm_accel[1]
    accel_z = icm_accel[2]
    accel_mag = math.sqrt(pow(accel_x, 2) + pow(accel_y, 2) + pow(accel_z, 2))
    # USE WITH Z AXIS FACING (UP) OR ACCELEROMETER WILL GET CONFUSED

    if accel_z < 0:
        accel_sign = -1
    else:
        accel_sign = 1
    vel_1 = accel_0 + (accel_sign * accel_mag - g - accel_0) * (time_stamp - time_0) * 0.5
    time_0 += time_stamp
    vel_0 += vel_1
    accel_0 += (accel_mag * accel_sign)

    print("accel data: " + str(icm_accel) + " " + str(accel_mag) + " " + str(vel_1) + " " + str(time_stamp))
    
    
"""with open("data.csv", "a") as f:
    f.write()
    print("wrote data")"""