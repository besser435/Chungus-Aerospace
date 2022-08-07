from digitalio import DigitalInOut, Direction, Pull
from analogio import AnalogIn
import time, busio, digitalio, board, neopixel, adafruit_rfm9x, storage, random
import adafruit_bmp3xx, adafruit_sdcard, analogio, traceback, adafruit_gps

# https://github.com/UnexpectedMaker/esp32s3/tree/main/code/circuitpython/shipping%20files/feathers3

version = "Tax Fraud v0.1 (Rocket)"
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


# SD card
"""SD_CS = board.D10   
spi = board.SPI()
cs = digitalio.DigitalInOut(SD_CS)
sdcard = adafruit_sdcard.SDCard(spi, cs)
vfs = storage.VfsFat(sdcard)
storage.mount(vfs, "/sd")"""

# Batt voltage
vbat_voltage = AnalogIn(board.BATTERY)
def get_battery_voltage():
    global battery_voltage
    """Get the approximate battery voltage."""
    # This formula should show the nominal 4.2V max capacity (approximately) when 5V is present and the
    # VBAT is in charge state for a 1S LiPo battery with a max capacity of 4.2V   
    global vbat_voltage
    ADC_RESOLUTION = 2 ** 16 -1
    AREF_VOLTAGE = 3.3
    R1 = 442000
    R2 = 160000
    battery_voltage = vbat_voltage.value/ADC_RESOLUTION*AREF_VOLTAGE*(R1+R2)/R2
    #print(battery_voltage)
get_battery_voltage()

# RFM95
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
cs = digitalio.DigitalInOut(board.D18)
reset = digitalio.DigitalInOut(board.D19)
rfm9x = adafruit_rfm9x.RFM9x(spi, cs, reset, 915.0)
rfm9x.tx_power = 23
prev_packet = None

# options
bmp.sea_level_pressure = 1010
debug_mode = 1
file_name = "tf_launch.csv" 
led_neo.brightness = 1

# storage
data_cycles = 0
log_list = []
is_logging = False


# GPS
gps = adafruit_gps.GPS_GtopI2C(i2c, debug=False)
gps.send_command(b"PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0")
gps.send_command(b"PMTK220,100") #1000 is the default, set to 10Hz


def get_fix():
    while True:
        gps.update()
        
        if not gps.has_fix:
            led_neo.fill((255, 200, 0))
            print("Waiting for fix...")
        else:
            led_neo.fill((0, 0, 255))
            print("Fix Found")

            if gps.satellites is not None:
                print("# satellites: {}".format(gps.satellites))
                break
get_fix()
 

def csv_setup():
    # this will be the time the fix was achieved, not the current time
    gps_time = "{}/{}/{} {:02}:{:02}:{:02}".format(
        gps.timestamp_utc.tm_mon,  # Grab parts of the time from the
        gps.timestamp_utc.tm_mday,  # struct_time object that holds
        gps.timestamp_utc.tm_year,  # the fix time.  Note you might
        gps.timestamp_utc.tm_hour,  # not get all data like year, day,
        gps.timestamp_utc.tm_min,  # month!
        gps.timestamp_utc.tm_sec,)

    #with open("/sd/" + file_name, "a") as f: 
    log_list.extend([
        (",,,,,,\n"),  # creates the right amount of columns 
        ("Software version: " + version + "\n"),
        ("Pressure: " + str(bmp.pressure) + "\n"),
        ("Altitude: " + str(bmp.altitude) + "\n"),
        ("Temperature: " + str(bmp.temperature) + "\n"),
        #("Batt Voltage: {:.2f}".format(battery_voltage)),

        ("GPS Time: ".format(gps_time)),
        ("Satellites: {}".format(gps.satellites)),
        ("Altitude: {} meters".format(gps.altitude_m)),
        ("Speed: {} knots".format(gps.speed_knots)),
        ("Track angle: {} degrees".format(gps.track_angle_deg)),
        ("Horizontal dilution: {}".format(gps.horizontal_dilution)),
        ("Height geoid: {} meters".format(gps.height_geoid)),
        ("Baro_alt, Lat, Lon, GPS_alt, GPS_knots, time")
        ])#f.write(','.join(log_list))
csv_setup()    


def main():
    global data_cycles

    # Liftoff detection
    STARTING_ALT = bmp.altitude
    if debug_mode == 0 and gps.has_fix == True: # test without true, might not be needed
        led_neo[0] = (0, 0, 255)
        while True:
            if bmp.altitude >= STARTING_ALT + 4:
                break
    

    # main flight loop
    initial_time = time.monotonic()
    led_neo[0] = (0, 255, 0)
    while True:
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
            #str("launch") + "," +
            str(bmp_alt) + "," +
            str("{0:.6f}".format(gps.latitude)) + "," +
            str("{0:.6f}".format(gps.longitude)) + "," +
            str(gps.altitude_m) + "," +
            str(gps.speed_knots) + "," + 
            str(gps_time) + "," + 
            str(gps.satellites) + "," +
            str("%0.2f" % battery_voltage) + "," +
            str("%0.3f" % time_stamp)
            )
            
            # write data
            log_list.extend([data])

            # send data
            send_data = bytes(data, "\r\n","utf-8")
            rfm9x.send(send_data)

            data_cycles += 1
            print(data_cycles)
            print(str(battery_voltage))
            print(gps_time)

        # stops the logging of data
        if True:
        #if debug_mode == 0:
            #if data_cycles > 200:
                #if bmp_alt <= STARTING_ALT + 8: 
                    #recovery()
                    break
        
main()


def recovery(): 
    # this transmits location data and blinks an LED. It doesn't log any data,
    # thats why this is separate from the main loop

    while True:
        time.sleep(0.1)
        
        get_battery_voltage()
        gps.update()

        led_neo[0] = (255, 255, 255)
        gps_time = "{}/{}/{} {:02}:{:02}:{:02}".format(
            gps.timestamp_utc.tm_mon,  # Grab parts of the time from the
            gps.timestamp_utc.tm_mday,  # struct_time object that holds
            gps.timestamp_utc.tm_year,  # the fix time.  Note you might
            gps.timestamp_utc.tm_hour,  # not get all data like year, day,
            gps.timestamp_utc.tm_min,  # month!
            gps.timestamp_utc.tm_sec,)


        if gps.has_fix == True:
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
        led_neo[0] = (0, 0, 0)


    # lat, lon, alt, sats, last update time, batt voltage

recovery()


