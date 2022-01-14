"""
NOTE
---Chungus Aerospace Program---
https://github.com/besser435/Chungus-Aerospace

Flight Software for the CircuitPython platform by Joe Mama and besser
This current code is meant to run on a Feather M4. Thats what the 
pinouts are configured for.

Currenty this only collects data, it doesn't control anything (yet)

"""


version = "v1.4"
date = "January 2022"


import adafruit_bmp3xx
import time
#import analogio
#import busio
import adafruit_pcf8523
import board
import digitalio
import storage
import adafruit_sdcard
from rainbowio import colorwheel
import neopixel
from analogio import AnalogIn




# Setup Bits
# I2C
i2c = board.I2C() 

# Batt voltage
vbat_voltage = AnalogIn(board.VOLTAGE_MONITOR)
def get_voltage(pin):
    return (pin.value * 3.3) / 65536 * 2
battery_voltage = get_voltage(vbat_voltage)

# pin D10 for Feather M4 Express
SD_CS = board.D10   
spi = board.SPI()
cs = digitalio.DigitalInOut(SD_CS)

# SD mount
sdcard = adafruit_sdcard.SDCard(spi, cs)
vfs = storage.VfsFat(sdcard)
storage.mount(vfs, "/sd")

# LED pins and setup
led_neo = neopixel.NeoPixel(board.NEOPIXEL, 1)
led = digitalio.DigitalInOut(board.D13)           
led.direction = digitalio.Direction.OUTPUT         

# BMP388
bmp = adafruit_bmp3xx.BMP3XX_I2C(i2c)
bmp.pressure_oversampling = 8
bmp.temperature_oversampling = 2

# Real time clock
#i2c = busio.I2C(board.SCL, board.SDA)
rtc = adafruit_pcf8523.PCF8523(i2c)
t = rtc.datetime

# Relay to deploy chute
chute_relay = digitalio.DigitalInOut(board.A1)  # NOTE change this pin to whatever pin is good. 
chute_relay.direction = digitalio.Direction.OUTPUT


# ------------------------- options ------------------------
development_mode = 0        # edits things like countdown so the code can be tested easier without having to change several other options
bmp.sea_level_pressure = 1023
log_stop_count = 400        # when to stop logging after an amount of data points are collected
log_interval = 0.0          # Unlikely to be the actual number due to the polling rate of the sensors
log_delay = 20              # Waits this many seconds before the logging starts. Delay so the rocket can be set up to launch before logging starts
file_name = "launch.csv"  

# storage
#launched = 0
STARTING_ALTITUDE = bmp.altitude
launch_delay_count = 0
writes_to_file = 0
chute_armed = 0
logged_chute_deploy = 0
speed_1 = 0
t_s_1 = 0
i = 0


if development_mode == 1:
    led_neo.brightness = 0.3  # prevents flashbang   
    while launch_delay_count <= 1:
        launch_delay_count += 1
        led_neo[0] = (255, 255, 0)
        time.sleep(0.5)
        led_neo[0] = (0, 0, 0)
        time.sleep(0.5)

else:
    led_neo.brightness = 1
    # shows that the code is running
    led_neo[0] = (255, 0, 0)
    time.sleep(0.3)
    led_neo[0] = (0, 255, 0)
    time.sleep(0.3)
    led_neo[0] = (0, 0, 255)
    time.sleep(0.3)
    led_neo[0] = (255, 255, 255)
    time.sleep(0.3)
    led_neo[0] = (0, 0, 0)

    while launch_delay_count <= log_delay:
        launch_delay_count += 1
        led_neo[0] = (255, 255, 0)
        time.sleep(0.5)
        led_neo[0] = (0, 0, 0)
        time.sleep(0.5)
    led_neo[0] = (0, 255, 0)    # shows that code execution is about to start
    time.sleep(1)
    led_neo[0] = (0, 0, 0)



# Sets the real time clock if enabled. Maybe make this a seperate script to clean up this one and so the time isnt reset by accident
days = ("Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday")
if False:   # change to True to write the time. remember to set to false before running the code again
    #                     year, mon, date, hour, min, sec, wday, yday, isdst
    t = time.struct_time((2022,  1,   7,   15,   43,   0,  5,    -1,  -1))

    rtc.datetime = t
    print()


# Add check to see if there is an SD card. this prevents data loss if something went wrong. if so, flash LED with error
# check if there is a file on the SD card. if there is, create a new one with
# a different file name so the old one isnt overwritten


initial_time = time.monotonic() # needs to be here and not in the time set ups bits code for reasons


with open("/sd/" + file_name, "a") as f: 
    f.write(str("Date: %d/%d/%d" % (t.tm_mon, t.tm_mday, t.tm_year) + "\n"))
    f.write("Time: %d:%02d:%02d" % (t.tm_hour, t.tm_min, t.tm_sec) + "\n")
    f.write("Batt voltage: {:.2f}".format(battery_voltage) + "\n")    
    f.write("Starting altitude: (test to see if parachute code works, idk how constants work) " + str(STARTING_ALTITUDE) + "\n")
    f.write("Data points to collect: " + str(log_stop_count) + "\n")
    f.write("Pressure (mbar),Temperature (°c),Altitude (m),V Speed (m/s),Elapsed Seconds\n")



#                          ------------------------ Main data logging code ------------------------
while True:    
    # open file for append
    with open("/sd/" + file_name, "a") as f:    
        led.value = True  # turn on LED to indicate writting has started


        current_time = time.monotonic()
        time_stamp = current_time - initial_time


        # change speed name to altitude
        t_s_0 = time_stamp
        v_speed = (bmp.altitude - speed_1) / (t_s_0 - t_s_1)


        f.write("{:5.2f},{:5.2f},{:5.2f},{:5.2f},".format(bmp.pressure, bmp.temperature, bmp.altitude, v_speed))
        f.write("{:5.2f}" .format(time_stamp) + "\n") # logs elapsed time 


        # possible relay code to send power to the parachute charge
        #https://learn.adafruit.com/circuitpython-digital-inputs-and-outputs/digital-outputs for relay pin and stuff

        if bmp.altitude >= (STARTING_ALTITUDE + 50):  # arms at 50 meters. idk if the parenthisis are needed. ill try with and without
            if chute_armed == 0: # this is so the event isnt logged repeatedly
                f.write("Armed parachute. Current alt: " + str(bmp.altitude) + "\n")
                chute_armed += 1

        if chute_armed == 1:
            if bmp.altitude <= STARTING_ALTITUDE + 49:  # once the rocket sinks below 50 meters it fires the chute
                for x in range(3):  # to ensure ignition
                    chute_relay.value = True
                    time.sleep(0.5)
                    chute_relay.value = False
                    time.sleep(0.5)

                if logged_chute_deploy == 0:
                    f.write("Deployed parachute. Current alt: " + str(bmp.altitude) + "\n")
                    logged_chute_deploy +=1
                    
        led.value = False  # turn off LED to indicate writting is done
    time.sleep(log_interval)


    writes_to_file += 1
    print("Writes to file: " + str(writes_to_file)) # for debugging while editing code


    speed_1 = bmp.altitude 
    t_s_1 = time_stamp


    # stops the logging of data
    if writes_to_file > 100:    # makes sure the code below isnt just executed on the pad
    #if launched == 1:   # possible way of doing the line of code above but more reliable. disabled as its not implimented 
        if bmp.altitude <= STARTING_ALTITUDE + 5:   # + 5 is incase it lands above the starting elevation or the sensor drifts
                break

    if writes_to_file >= log_stop_count:    # backup to the code above
        break


#                          ------------------------ End of main data logging code ------------------------



while True:     # indicates that the data recording is done
    i = (i + 1) % 256  # run from 0 to 255
    led_neo.fill(colorwheel(i)) # Unicorn barf
    time.sleep(0.01)




"""
while True:
    print(
        "Pressure: {:5.2f}  Temperature: {:5.2f}  Altitude: {:5.2f}".format(bmp.pressure, bmp.temperature, bmp.altitude))
    time.sleep(0.05)
    """



