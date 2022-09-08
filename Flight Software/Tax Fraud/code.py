from digitalio import DigitalInOut
from analogio import AnalogIn
import os, time, busio, digitalio, board, neopixel, adafruit_rfm9x
import adafruit_bmp3xx, analogio, traceback, adafruit_gps, gc

# https://github.com/UnexpectedMaker/esp32s3/tree/main/code/circuitpython/shipping%20files/feathers3

version = "Tax Fraud v1.0 (Rocket)"
print(version)


# I2C
i2c = busio.I2C(board.SCL, board.SDA)

# Neopixel
led_neo = neopixel.NeoPixel(board.NEOPIXEL, 1)

# BMP388
bmp = adafruit_bmp3xx.BMP3XX_I2C(i2c)
bmp.pressure_oversampling = 2   #NOTE This was 8 by default
bmp._wait_time = 0
bmp.temperature_oversampling = 2

# Batt voltage
vbat_voltage = AnalogIn(board.BATTERY)
def get_battery_voltage():
    global battery_voltage
    # Get the approximate battery voltage.
    # This formula should show the nominal 4.2V max capacity (approximately) when 5V is present and the
    # VBAT is in charge state for a 1S LiPo battery with a max capacity of 4.2V   
    global vbat_voltage
    ADC_RESOLUTION = 2 ** 16 -1
    AREF_VOLTAGE = 3.3
    R1 = 442000
    R2 = 160000
    #print(battery_voltage)
    battery_voltage = vbat_voltage.value/ADC_RESOLUTION*AREF_VOLTAGE*(R1+R2)/R2
get_battery_voltage()

# RFM95
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
cs = digitalio.DigitalInOut(board.D18)
reset = digitalio.DigitalInOut(board.D19)
rfm9x = adafruit_rfm9x.RFM9x(spi, cs, reset, 915.0)
rfm9x.tx_power = 23
prev_packet = None

# GPS
gps = adafruit_gps.GPS_GtopI2C(i2c, debug=False, )
gps.send_command(b"PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0")
gps.send_command(b"PMTK220,100") #1000 is the default, set to 10Hz

# options
bmp.sea_level_pressure = 1010
debug_mode = 0
FILE_NAME = "tf_launch.csv" 
led_neo.brightness = 1

# storage
data_cycles = 0
log_list = []
is_logging = False


"""
How to set up filesystem:
For launch: set dev mode to 0, press button, and you are ready

For REPL viewing and code execution: set dev mode to true, upload that to the drive, 
then plug into computer with with pin A0 jumped to ground

For editing code/changing files on the drive: just plug in and do whatever
"""


# this checks if the file system is not write protected.


with open(FILE_NAME, "a") as f: 
    f.write("\n")



"""
for some reason, the except statements cant access the regular
recovery function, so I have this here as a last resort.

"""
def backup_recovery(): 
        # this transmits location data and blinks an LED. It doesn't log any data,
        # thats why this is separate from the main loop

    with open(FILE_NAME, "a") as f:
        f.write(','.join(log_list))
        print("wrote data")

    while True:
        time.sleep(0.1)
        
        get_battery_voltage()
        gps.update()
        led_neo[0] = (255, 255, 255)

        if gps.has_fix == True:
            gps_time = "{}/{}/{} {:02}:{:02}:{:02}".format(
                gps.timestamp_utc.tm_mon,  # Grab parts of the time from the
                gps.timestamp_utc.tm_mday,  # struct_time object that holds
                gps.timestamp_utc.tm_year,  # the fix time.  Note you might
                gps.timestamp_utc.tm_hour,  # not get all data like year, day,
                gps.timestamp_utc.tm_min,  # month!
                gps.timestamp_utc.tm_sec,)
        
            recovery_data = (
            str("recovery_mode") + "," +
            str("{0:.6f}".format(gps.latitude)) + "," +
            str("{0:.6f}".format(gps.longitude)) + "," +
            str(gps.altitude_m) + "," +
            str(gps_time) + "," + 
            str(gps.satellites) + "," +
            str("%0.2f" % battery_voltage)
            )
            
            send_data = bytes(recovery_data, "\r\n","utf-8")
            rfm9x.send(send_data)
            print(recovery_data)
        else:
            #this code is kinda redundant, probably best to call get_fix() again, but this works and doesnt break
            print("Waiting for fix... (recovery)")
            print("Batt. voltage: %0.2f" % battery_voltage)
            send_data = bytes(str("gps_fix_wait") + ",", "\r\n","utf-8")
            rfm9x.send(send_data)
        led_neo[0] = (0, 0, 0)


try:
    def get_fix():
        while True:
            gps.update()
            get_battery_voltage()

            if not gps.has_fix:
                led_neo.fill((255, 200, 0))
                print("Waiting for fix...")
                print("Batt. voltage: %0.2f" % battery_voltage)

                #data = str("gps_fix_wait") + ","
                send_data = bytes(str("gps_fix_wait") + ",", "\r\n","utf-8")
                rfm9x.send(send_data)
            else:
                led_neo.fill((0, 0, 255))
                print("Fix Found, waiting for stability (10s)")
                time.sleep(10) 
                # sometimes it only gets a blip, and that triggers a false fix.
                # this helps to ensure that the fix is reliable
                if gps.satellites is not None:
                    print("# satellites: {}".format(gps.satellites))
                    break
                break
    get_fix()
    

    def csv_setup():
        get_battery_voltage()
        gps.update()
        # this will be the time the fix was achieved, not the current time
        if gps.has_fix:
            gps_time = "{}/{}/{} {:02}:{:02}:{:02}".format(
                gps.timestamp_utc.tm_mon,  
                gps.timestamp_utc.tm_mday,  
                gps.timestamp_utc.tm_year,  
                gps.timestamp_utc.tm_hour,  
                gps.timestamp_utc.tm_min, 
                gps.timestamp_utc.tm_sec,)
        else:
            gps_time = None

        with open(FILE_NAME, "a") as f: 
            f.write("Mode, Baro_alt, Lat, Lon, GPS_alt, GPS_knots, GPS_time, Sats, Batt_voltage, loop_time, \n")
            f.write("Software version: " + str(version) + "\n")
            f.write("Pressure: " + str(bmp.pressure) + "\n")
            f.write("BMP Altitude: " + str(bmp.altitude) + "\n")
            f.write("Temperature: " + str(bmp.temperature) + "\n")
            f.write("Batt Voltage: {:.2f}".format(battery_voltage) + "\n")
            f.write("GPS Time: ".format(gps_time) + "\n")
            f.write("Satellites: {}".format(gps.satellites) + "\n")
            f.write("GPS Altitude: {} meters".format(gps.altitude_m) + "\n")
            f.write("Speed: {} knots".format(gps.speed_knots) + "\n")
            f.write("Track angle: {} degrees".format(gps.track_angle_deg) + "\n")
            f.write("Horizontal dilution: {}".format(gps.horizontal_dilution) + "\n")
            f.write("Height geoid: {} meters".format(gps.height_geoid) + "\n")
            f.write("Mode, Baro_alt, Lat, Lon, GPS_alt, GPS_knots, GPS_time, Sats, Batt_voltage, loop_time, \n")                
    csv_setup()    


    def recovery(): 
            # this transmits location data and blinks an LED. It doesn't log any data,
            # thats why this is separate from the main loop

        with open(FILE_NAME, "a") as f:
            f.write(','.join(log_list))
            print("wrote data")

        while True:
            time.sleep(0.1)
            
            get_battery_voltage()
            gps.update()
            led_neo[0] = (255, 255, 255)

            if gps.has_fix == True:
                gps_time = "{}/{}/{} {:02}:{:02}:{:02}".format(
                    gps.timestamp_utc.tm_mon,  # Grab parts of the time from the
                    gps.timestamp_utc.tm_mday,  # struct_time object that holds
                    gps.timestamp_utc.tm_year,  # the fix time.  Note you might
                    gps.timestamp_utc.tm_hour,  # not get all data like year, day,
                    gps.timestamp_utc.tm_min,  # month!
                    gps.timestamp_utc.tm_sec,)
            
                recovery_data = (
                str("recovery_mode") + "," +
                str("{0:.6f}".format(gps.latitude)) + "," +
                str("{0:.6f}".format(gps.longitude)) + "," +
                str(gps.altitude_m) + "," +
                str(gps_time) + "," + 
                str(gps.satellites) + "," +
                str("%0.2f" % battery_voltage)
                )
                
                send_data = bytes(recovery_data, "\r\n","utf-8")
                rfm9x.send(send_data)
                print(recovery_data)
            else:
                #this code is kinda redundant, probably best to call get_fix() again, but this works and doesnt break
                print("Waiting for fix... (recovery)")
                print("Batt. voltage: %0.2f" % battery_voltage)
                send_data = bytes(str("gps_fix_wait") + ",", "\r\n","utf-8")
                rfm9x.send(send_data)
            led_neo[0] = (0, 0, 0)
            

    def main():
        global data_cycles

        # Liftoff detection
        STARTING_ALT = bmp.altitude
        #if debug_mode == 0: 
        if True:
            # add method od manually bypassing this via a radio command incase this gets stuck somehow
            # that command would go to recovery()
            #it = 0 # debug 
            while True: # liftoff detection
                gps.update()
                has_fix = gps.has_fix
                sat_count = gps.satellites

                #it += 1

                send_data = bytes("pad_mode," + str(has_fix) + "," + str(sat_count), "\r\n","utf-8")
                rfm9x.send(send_data)
                led_neo[0] = (0, 0, 255)

                print()
                print("Waiting for liftoff...")
                print("Has GPS fix: " + str(has_fix))
                """add starting alt"""
                print("Sat count: " + str(sat_count))
                
                #if it > 10: break # debug 
                if bmp.altitude >= STARTING_ALT + 5:
                    break

        
        initial_time = time.monotonic()
        led_neo[0] = (0, 255, 0)

        
        while True: # main flight loop
            get_battery_voltage()
            gps.update()
            gps_time = "{}/{}/{} {:02}:{:02}:{:02}".format(
                gps.timestamp_utc.tm_mon,  # Grab parts of the time from the
                gps.timestamp_utc.tm_mday,  # struct_time object that holds
                gps.timestamp_utc.tm_year,  # the fix time.  Note you might
                gps.timestamp_utc.tm_hour,  # not get all data like year, day,
                gps.timestamp_utc.tm_min,  # month!
                gps.timestamp_utc.tm_sec,)
            current_time = time.monotonic()
            time_stamp = current_time - initial_time

            bmp_alt = bmp.altitude
            
            if gps.has_fix == True:
                data = (
                str("log_mode") + "," +
                str(bmp_alt) + "," +
                str("{0:.6f}".format(gps.latitude)) + "," +
                str("{0:.6f}".format(gps.longitude)) + "," +
                str(gps.altitude_m) + "," +
                str(gps.speed_knots) + "," + 
                str(gps_time) + "," + 
                str(gps.satellites) + "," +
                str("%0.2f" % battery_voltage) + "," +
                str("%0.3f" % time_stamp) + "\n"
                """add data cycle count"""
                )
                
                # write data
                log_list.extend([data])

                # send data
                send_data = bytes(data, "\r\n","utf-8")
                rfm9x.send(send_data)
                print("Sent data: ")
                print(send_data)
                print("Data cycle: " + str(data_cycles))
                print("Free RAM: " + str(gc.mem_free()))

            
            # and never go to the recovery function
            # stops the logging of data
            #if True:
            if debug_mode == 0:
                if data_cycles > 30:
                    if bmp_alt <= STARTING_ALT + 20: 
                        recovery()
                        break  
            data_cycles += 1 # out of the if gps.has_fix == True: bit incase it never happens. then it would be stuck  
    main()


except OSError as e: # sometimes the GPS module doesn't work, this is a failsafe
    print("OSError, trying again in a bit")
    print(e)
    #rfm send error
    led_neo.fill((255, 0, 0))
    with open("OSError.csv", "a") as f:
        f.write(str(e) + "\n")
        
    if debug_mode == 0:
        time.sleep(10)
    backup_recovery()


except Exception as e:
    print("Exception, trying again in a bit")
    print(e)
    #rfm send error
    with open("Exception.csv", "a") as f:
        f.write(str(e) + "\n")

    led_neo.fill((255, 0, 0))
    if debug_mode == 0:
        time.sleep(10)
    backup_recovery()
    

