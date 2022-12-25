import board, time, busio, math, adafruit_icm20x, neopixel
i2c = busio.I2C(board.SCL1, board.SDA1)
icm = adafruit_icm20x.ICM20649(i2c)

#Accelerometer setup
adafruit_icm20x.ICM20649.accelerometer_range = 4
adafruit_icm20x.accelerometer_data_rate = 5000

#Board LED setup
led0 = neopixel.NeoPixel(board.NEOPIXEL, 1)

#x/y calibration setup and initial timer
led0[0] = (0, 255, 0)
time.sleep(20)

cum_x = 0
cum_y = 0
i = 1

#x/y calibration
for i in range(2000):
    led0[0] = (255, 0, 0)
    
    cum_x += icm.acceleration[0]
    cum_y += icm.acceleration[1]
    avg_x = cum_x / i
    avg_y = cum_y / i

#z calibration setup and timer
cum_z = 0
i = 1
led0[0] = (0, 255, 0)

#z calibration
for i in range(2000):
    led0[0] = (255, 0, 0)
    cum_z += icm.acceleration[2]
    avg_z = cum_z / i
