
class velocity:
    #Literally just the regular code with the calibration part removed

    import board, time, busio, math, adafruit_icm20x
    i2c = busio.I2C(board.SCL1, board.SDA1)
    icm = adafruit_icm20x.ICM20649(i2c)
    adafruit_icm20x.ICM20649.accelerometer_range = 30
    adafruit_icm20x.accelerometer_data_rate = 5000
    #TODO Manually insert calibration values here (This fucking sucks)
    x_adjust = None
    y_adjust = None
    z_adjust = None
    g = None

    #Measurement setup
    adafruit_icm20x.ICM20649.accelerometer_range = 30
    initial_time = time.monotonic()
    vel_0 = 0
    time_0 = 0
    accel_0 = g

    while True: #accel_mag > 30 or v0 > 10:
        current_time = time.monotonic()
        time_1 = current_time - initial_time
        
        icm_accel = icm.acceleration
        accel_x, accel_y, accel_z = icm_accel
        
        accel_mag = math.sqrt(pow(accel_x - x_adjust, 2) + pow(accel_y - y_adjust, 2) + pow(accel_z - z_adjust, 2)) #This gets the magnitude of the acceleration vector. 
        #Calculating a velocity vector by doing this step first would make my physics/calculus professors cry if it wasn't for the efficiency
    
    
        # USE WITH Z AXIS FACING (UP) OR ACCELEROMETER WILL GET CONFUSED
        if accel_z < 0:
            accel_sign = -1
        else:
            accel_sign = 1
        accel_1 = accel_mag * accel_sign
        vel_1 = vel_0 + (accel_1 + accel_0 - 2 * g) * (time_1 - time_0) * 0.5 #This is the integral of the magnitude of the acceleration vector.
        #For measurements in a way that isn't absolutely retarded, this integral will have to be done three times. Probably too much without floating point support
        delta_v = vel_1 - vel_0
        time_0 = time_1
        vel_0 = vel_1
        accel_0 = accel_1

        print("accel data: " + str(icm_accel) + " " + str(accel_mag) + " " + str(vel_1) + " " + str(delta_v) + " " + str(time_1))