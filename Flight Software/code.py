"""
NOTE
---Chungus Aerospace Program---
https://github.com/besser435/Chungus-Aerospace

Flight Software for the CALC flight system by Joe Mama and besser.
This current code is meant to run on a Feather M4. Thats what the 
pinouts are configured for.

In the future this might run off of a Raspberry Pi Zero
for better I/O, camera support, and a few other things.


"""


version = "v1.6"
date = "January 2022"


import adafruit_bmp3xx
import adafruit_adxl34x
import adafruit_pcf8523
import adafruit_sdcard
import neopixel
import board
import digitalio
import storage
import time
from rainbowio import colorwheel
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

# ADXL345
accel = adafruit_adxl34x.ADXL345(i2c)

# Real time clock
#i2c = busio.I2C(board.SCL, board.SDA)
rtc = adafruit_pcf8523.PCF8523(i2c)
t = rtc.datetime

# Relay to deploy chute
chute_relay = digitalio.DigitalInOut(board.A1)  # NOTE change this pin to whatever pin is good. 
chute_relay.direction = digitalio.Direction.OUTPUT


# ------------------------- options ------------------------
development_mode = 0        # edits things like countdown so the code can be tested easier without having to change several other options
bmp.sea_level_pressure = 1024
log_stop_count = 400        # when to stop logging after an amount of data points are collected, backup to low altitude condition
log_interval = 0.0          # Unlikely to be the actual number due to the polling rate of the sensors
log_delay = 10              # Waits this many seconds before the logging starts. Delay so the rocket can be set up to launch before logging starts
file_name = "launch.csv"  

# storage
#launched = 0
STARTING_ALTITUDE = bmp.altitude
launch_delay_count = 0
max_altitude = 0
data_cycles = 0
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
    time.sleep(2)
    led_neo[0] = (0, 0, 0)


"""
# Sets the real time clock if enabled. Maybe make this a seperate script to clean up this one and so the time isnt reset by accident
days = ("Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday")
if False:   # change to True to write the time. remember to set to false before running the code again
    #                     year, mon, date, hour, min, sec, wday, yday, isdst
    t = time.struct_time((2022,  1,   7,   15,   43,   0,  5,    -1,  -1))

    rtc.datetime = t
"""


# Add check to see if there is an SD card. this prevents data loss if something went wrong. if so, flash LED with error
with open("/sd/" + file_name, "a") as f: 
    f.write(str("Date: %d/%d/%d" % (t.tm_mon, t.tm_mday, t.tm_year) + "\n"))
    f.write("Time: %d:%02d:%02d" % (t.tm_hour, t.tm_min, t.tm_sec) + "\n")
    f.write("Voltage: {:.2f}".format(battery_voltage) + "\n")   # If USB is connected it will read that voltage instead
    f.write("Starting altitude: " + str(STARTING_ALTITUDE) + "\n")
    f.write("Data points to collect: " + str(log_stop_count) + "\n")
    f.write("Pressure (mbar),Temperature (°c),Altitude (m),V Speed (m/s),Accel on xyz (m/s^2),Elapsed Seconds\n")


initial_time = time.monotonic() # needs to be here and not in the time set ups bits code for reasons


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


        # potential way of starting the logging in the future. needs to be proven to work tho, which is what this is
        # this should be in the main loop for now, but should be above it if this works.
        logged_liftoff = 0  
        if bmp.altitude >= STARTING_ALTITUDE + 3:
            f.write("Liftoff detected. Current alt: " + bmp.altitude +  "\n")
            logged_liftoff += 1


        f.write("{:5.2f},{:5.2f},{:5.2f},{:5.2f},".format(bmp.pressure, bmp.temperature, bmp.altitude, v_speed,))
        f.write("%.2f %.2f %.2f," % accel.acceleration,)
        f.write("{:5.2f}" .format(time_stamp) + "\n") # logs elapsed time 


        # possible relay code to send power to the parachute charge
        #https://learn.adafruit.com/circuitpython-digital-inputs-and-outputs/digital-outputs for relay pin and stuff
        if bmp.altitude >= STARTING_ALTITUDE + 50: 
            if chute_armed == 0: # this is so the event isnt logged repeatedly
                f.write("Armed parachute. Current alt: " + str(bmp.altitude) + "\n")
                chute_armed += 1

        if chute_armed == 1:
            if bmp.altitude <= STARTING_ALTITUDE + 49:  # once the rocket sinks below 50 meters it fires the chute
                for x in range(3):  # to ensure ignition
                    chute_relay.value = True
                    time.sleep(1)
                    chute_relay.value = False
                    time.sleep(0.5)

                if logged_chute_deploy == 0:
                    f.write("Deployed parachute. Current alt: " + str(bmp.altitude) + "\n")
                    logged_chute_deploy +=1


    speed_1 = bmp.altitude 
    t_s_1 = time_stamp

    
    with open("/sd/" + file_name, "a") as f:
        # stops the logging of data
        if data_cycles > 100:    # makes sure the code below isnt just executed on the pad   #if data_cycles > 100 and (bmp.altitude <= STARTING_ALTITUDE + 5):# does this work?
        #if launched == 1:   # possible way of doing the line of code above but more reliable. disabled as its not implimented 
            if bmp.altitude <= STARTING_ALTITUDE + 5:   # + 5 is incase it lands above the starting elevation or the sensor drifts
                f.write("Stopped logging; low altitude met. (" + str(bmp.altitude) + "m)\n")
                break

        if data_cycles >= log_stop_count:   # backup to the code above
            if logged_chute_deploy == 1:    # ensures the chute deployed before breaking
                f.write("Stopped logging; writes to file met. (" + str(data_cycles) + " writes) ")
                f.write("This means altitude code did not execute.\n")
                break


    if bmp.altitude >= max_altitude:
        max_altitude = bmp.altitude
    #if past apogee:
        #log max altitude


    data_cycles += 1 # not an exact number. it should maybe be moved to the end of the code an renamed to cycles
    print("Data cycles: " + str(data_cycles)) # for debugging while editing code


    led.value = False  # turn off LED to indicate writting is done
    time.sleep(log_interval)
#                          ------------------------ End of main data logging code ------------------------


with open("/sd/" + file_name, "a") as f:
    f.write("Max altitude: " + str(max_altitude) + "\n")

while True:     # indicates that the data recording is done
    i = (i + 1) % 256  # run from 0 to 255
    led_neo.fill(colorwheel(i)) # Unicorn barf
    time.sleep(0.01)

