import board, time, busio, math, adafruit_icm20x, neopixel, csv
i2c = busio.I2C(board.SCL1, board.SDA1)
icm = adafruit_icm20x.ICM20649(i2c)

#Accelerometer setup
adafruit_icm20x.ICM20649.accelerometer_range = 4
adafruit_icm20x.accelerometer_data_rate = 5000

#Board LED setup
led0 = neopixel.NeoPixel(board.NEOPIXEL, 1)

#x/y calibration setup and initial timer
led0[0] = (0, 255, 0)
print("X/Y delay")
time.sleep(20)
cum_x = 0
cum_y = 0
i = 1

#x/y calibration
led0[0] = (255, 0, 0)
print("Running X/Y calibration")
for i in range(2000):
    cum_x += icm.acceleration[0]
    cum_y += icm.acceleration[1]
    avg_x = cum_x / i
    avg_y = cum_y / i
    print("x: " + str(avg_x) + "y: " + str(avg_y) + "z: " + "g: ")

#z calibration setup and timer
led0[0] = (0, 255, 0)
print("Z/G delay")
time.sleep(20)
cum_z = 0
i = 1

#z calibration
led0[0] = (255, 0, 0)
print("Running Z calibration")
for i in range(2000):
    cum_z += icm.acceleration[2]
    avg_z = cum_z / i
    print("x: " + str(avg_x) + "y: " + str(avg_y) + "z: " + str(avg_z) + "g: ")

#g calibration
print("Running G calibration")
i = 1
cum_g = 0
for i in range(2000):
    accel_x, accel_y, accel_z = icm.acceleration

    accel_mag = math.sqrt(pow(accel_x - avg_x, 2) + pow(accel_y - avg_y, 2) + pow(accel_z - avg_z, 2))
    cum_g += accel_mag
    g = cum_g / i
    print("x: " + str(avg_x) + "y: " + str(avg_y) + "z: " + str(avg_z) + "g: " + str(g))

print("Calibration complete")
led0[0] = (255, 255, 255)
#Printing the values and manually putting them in the code is janky as fuck, but idk how to improve it