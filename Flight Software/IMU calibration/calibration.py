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
print("X/Y delay")
time.sleep(20)
accelCum_x = 0
accelCum_y = 0
gyroCum_x = 0
gyroCum_y = 0
gyroCum_z = 0
i = 1
radianConversion = 3.14159 / 180

#x/y/gyro calibration
led0[0] = (255, 0, 0)
print("Running X/Y calibration")
for i in range(1, 2000):
    #accel calibration
    accelCum_x += icm.acceleration[0]
    accelCum_y += icm.acceleration[1]
    accelAvg_x = accelCum_x / i
    accelAvg_y = accelCum_y / i
    #gyro calibration
    gyroCum_x += icm.gyro(0)
    gyroCum_y += icm.gyro(1)
    gyroCum_z += icm.gyro(2)
    gyroAvg_x = gyroCum_x / i
    gyroAvg_y = gyroCum_y / i
    gyroAvg_z = gyroCum_z / i
    
    print(f"x: {str(accelAvg_x)} y: {str(accelAvg_y)} z:  g:  gyro x: {str(gyroAvg_x * radianConversion)} gyro y: {str(gyroAvg_y * radianConversion)} gyro z: {str(gyroAvg_z * radianConversion)} (rad/s)")

#z calibration setup and timer
led0[0] = (0, 255, 0)
print("Z/G delay")
time.sleep(20)
accelCum_z = 0
i = 1

#z calibration
led0[0] = (255, 0, 0)
print("Running Z calibration")
for i in range(2000):
    accelCum_z += icm.acceleration[2]
    if i >= 1:
        accelAvg_z = accelCum_z / i
        print(f"x: {str(accelAvg_x)} y: {str(accelAvg_y)} z: {str(accelAvg_z)} g:  gyro x: {str(gyroAvg_x * radianConversion)} gyro y: {str(gyroAvg_y * radianConversion)} gyro z: {str(gyroAvg_z * radianConversion)} (rad/s)")

#g calibration
print("Running G calibration")
i = 1
cum_g = 0
for i in range(2000):
    accel_x, accel_y, accel_z = icm.acceleration

    accel_mag = math.sqrt(pow(accel_x - accelAvg_x, 2) + pow(accel_y - accelAvg_y, 2) + pow(accel_z - accelAvg_z, 2))
    cum_g += accel_mag
    if i >= 1:
        g = cum_g / i
        print(f"x: {str(accelAvg_x)} y: {str(accelAvg_y)} z: {str(accelAvg_z)} g: {str(g)} gyro x: {str(gyroAvg_x * radianConversion)} gyro y: {str(gyroAvg_y * radianConversion)} gyro z: {str(gyroAvg_z * radianConversion)} (rad/s)")

print("Calibration complete")
led0[0] = (255, 255, 255)
#Printing the values and manually putting them in the code is janky as fuck, but idk how to improve it