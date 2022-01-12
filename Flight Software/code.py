"""
NOTE
---Chungus Aerospace Program---
https://github.com/besser435/Chungus-Aerospace

Flight Software for the CircuitPython platform by Joe Mama and besser
This current code is meant to run on a Feather M4. Thats what the 
pinouts are configured for.

Currenty this only collects data, it doesn't control anything (yet)

"""


version = "v1.2"
date = "January 2022"


import adafruit_bmp3xx
import time
import analogio
import busio
import adafruit_pcf8523
import board
import digitalio
import storage
import adafruit_sdcard
from rainbowio import colorwheel
import neopixel
import microcontroller
import neopixel
import adafruit_dotstar


#vbat_voltage = analogio.AnalogIn(board.D9)     #log this

# Setup Bits
# I2C
i2c = board.I2C() 

# pin D10 for Feather M4 Express
SD_CS = board.D10   
spi = board.SPI()
cs = digitalio.DigitalInOut(SD_CS)

# SD mount
sdcard = adafruit_sdcard.SDCard(spi, cs)
vfs = storage.VfsFat(sdcard)
storage.mount(vfs, "/sd")

# For Feather M0 Express, Metro M0 Express, Metro M4 Express, Circuit Playground Express, QT Py M0
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
initial_time = time.monotonic()


# ------------------------- options ------------------------
#devlopment_mode = 0         # edits things like countdown so the code can be tested easier without having to changing several other options
bmp.sea_level_pressure = 1019
log_stop_count = 300        # when to stop logging after an amount of data points are collected
log_interval = 0.01         # Unlikely to be the actual number due to the polling rate of the barometer
led_neo.brightness = 1      # should be 1 for launch so it can be seen easier
file_name = "launch.csv"  

# storage
#launched = 0
STARTING_ALTITUDE = bmp.altitude


# Add check to see if there is an SD card. this prevents data loss if something went wrong and should be added ASAP


def show_boot():    # shows that the code is running. also moar RGB is moar good
    led_neo[0] = (255, 0, 0)
    time.sleep(0.3)
    led_neo[0] = (0, 255, 0)
    time.sleep(0.3)
    led_neo[0] = (0, 0, 255)
    time.sleep(0.3)
    led_neo[0] = (255, 255, 255)
    time.sleep(0.7)
    led_neo[0] = (0, 0, 0)
    # this should also change an LED color based on batt volatge. batt specs on adafruit
    # https://www.adafruit.com/product/3898
    # https://cdn-shop.adafruit.com/product-files/3898/3898_specsheet_LP801735_400mAh_3.7V_20161129.pdf
    # look at page 3
    # voltage range from 4.2-3v????
show_boot()


"""
unicorn barf
i = 0
while True:
    i = (i + 1) % 256  # run from 0 to 255
    led_neo.fill(colorwheel(i))
    time.sleep(0.01)
"""


"""while True: # tests for launch conditions then runs the rest of the code
    if launch/countdown, 
        break

"""

time_delay_count = 0
print("Waiting for launch...")  # allows time for the rocket to be set up and have the launch started. This is awful and will be addressed later

while time_delay_count <= 1:
    time_delay_count += 1
    led_neo[0] = (255, 255, 0)
    time.sleep(0.5)
    led_neo[0] = (0, 0, 0)
    time.sleep(0.5)


# check if there is a file on the SD card. if there is, create a new one with
# a different file name so the old one isnt overwritten


# Sets the real time clock if enabled
days = ("Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday")
if False:   # change to True to write the time. remember to set to false before running the code again
    #                     year, mon, date, hour, min, sec, wday, yday, isdst
    t = time.struct_time((2022,  1,   7,   15,   43,   0,  5,    -1,  -1))

    rtc.datetime = t
    print()


# log bat voltage at the start
# add date logging heres
writes_to_file = 0
with open("/sd/" + file_name, "a") as f: # a means to append to the file, not overwrite it
    f.write(str("Date: %d/%d/%d" % (t.tm_mon, t.tm_mday, t.tm_year) + "\n"))

with open("/sd/" + file_name, "a") as f:
    f.write("Time: %d:%02d:%02d" % (t.tm_hour, t.tm_min, t.tm_sec) + "\n")

with open("/sd/" + file_name, "a") as f: 
    f.write("Starting altitude: (test to see if parachute code works, idk how constants work) " + str(STARTING_ALTITUDE) + "\n")

with open("/sd/" + file_name, "a") as f: 
    f.write("Data points to collect: " + str(log_stop_count) + "\n")

with open("/sd/" + file_name, "a") as f: 
    f.write("Pressure(mbar),Temperature(°c),Altitude(m),Elapsed Seconds\n")




#                          ------------------------ Main data logging code ------------------------
while True:    
    # open file for append
    with open("/sd/" + file_name, "a") as f:    
        led.value = True  # turn on LED to indicate writting has started


        f.write("{:5.2f},{:5.2f},{:5.2f},".format(bmp.pressure, bmp.temperature, bmp.altitude))
        
        current_time = time.monotonic()
        time_stamp = current_time - initial_time
        f.write("{:5.2f}" .format(time_stamp) + "\n") # logs elapsed time


        # proof of concept parachute code
        logged_arm = 0
        logged_chute = 0
        if bmp.altitude >= STARTING_ALTITUDE + 50:  # arms at 50 meters
            if logged_arm == 0:
                f.write("Arm parachute. Current alt: " + str(bmp.altitude))
                logged_arm += 1 # this is so the event isnt logged repeatedly
            
            if bmp.altitude <= STARTING_ALTITUDE + 49:  # once the rocket sinks below 50 meters it fires the chute
                #do your mom    # deploys chute
                if logged_chute == 0:
                    f.write("Deploy parachute. Current alt: " + str(bmp.altitude))
                    logged_chute +=1
              

        led.value = False  # turn off LED to indicate writting is done
    time.sleep(log_interval)


    # add some code that detects if the altitude stops changing and if it does it stops logging


    writes_to_file += 1
    print("Writes to file: " + str(writes_to_file)) # for debugging while editing code

    
    if writes_to_file >= log_stop_count:    # stops the logging of data
        break

    """ replaces the above code
    If change in altitude > x
    then:
    If change in altitude > x (again)
    then: 
    If change in altitude > x (again)
    then liftoff has been detected
    code to stop logging
    
    
    
    """
#                          ------------------------ End of main data logging code ------------------------



with open("/sd/" + file_name, "a") as f: 
    f.write("Starting altitude: (test to see if parachute code works, idk how constants work) " + str(STARTING_ALTITUDE) + "\n")


while True:     # indicates that the data recording is done
    led_neo[0] = (50, 255, 0)
    time.sleep(0.5)
    led_neo[0] = (0, 100, 255)
    time.sleep(0.5)



"""
while True:
    print(
        "Pressure: {:5.2f}  Temperature: {:5.2f}  Altitude: {:5.2f}".format(bmp.pressure, bmp.temperature, bmp.altitude))
    time.sleep(0.05)
    """

