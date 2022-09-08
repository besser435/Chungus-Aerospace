# ICM20649
import adafruit_icm20x
import board
import time
i2c = board.I2C() 
icm = adafruit_icm20x.ICM20649(i2c)
adafruit_icm20x.ICM20649.accelerometer_range = 16

"""adafruit_icm20x.ICM20649.gyro_data_rate = 5000
adafruit_icm20x.ICM20649.accelerometer_data_rate = 5000"""
#adafruit_icm20x.ICM20649.accelerometer_data_rate_divisor = 1  # maximum
icm.accelerometer_data_rate_divisor = 1


def flight_software():
    # https://en.wikipedia.org/wiki/Code_refactoring
    # https://en.wikipedia.org/wiki/Spaghetti_code
    global ran_launch
    ran_launch = 1
    global current_time
    global file_location
    global FILE_NAME
    global log_list
    global wrote_to_log_list


    TIMEDATE = "yes"
    # logging options
    FILE_NAME = "launch " + TIMEDATE + ".csv" 
    file_location = "/home/pi/Desktop/"  

    # logging storage
    log_list = []
    data_cycles = 0


    # .csv creation and formatting
    with open(file_location + FILE_NAME, "a") as f: 
        f.write("Altitude (m), Accel on xyz (m/s^2), Gyro on xyz (deg/s), Time (s), Events\n") # creates right amount of column
        f.write(",,,,,,\n")

        

    initial_time = time.monotonic() # needs to be here and not in the time set ups bits code for reasons
    while True: 
    
        #bmp_press = bmp.pressure
        icm_accel = icm.acceleration
        current_time = time.monotonic()
        time_stamp = current_time - initial_time

        log_list.extend([
        "\n"
        #"{:5.2f}".format(bmp_alt),
        #"%.2f %.2f %.2f" % (icm_accel),
        "%.2f %.2f %.2f" % (icm_accel),
        "{:5.2f}".format(time_stamp),
        ])


        print("Time: {:5.2f}".format(time_stamp) + "s", end = "   ")
        print("Data cycles: " + str(data_cycles))
        data_cycles += 1 
            


        if data_cycles > 150:  # ensures that the logging is not stopped on the pad  
            print("done")
            break



            
    with open(file_location + FILE_NAME, "a") as f: 
        f.write(','.join(log_list))
        print("wrote data")
flight_software()