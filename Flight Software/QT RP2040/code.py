"""
This is the flight software for the QT Py RP2040
"""
version = "v1.1"

import time
import board
import adafruit_bmp3xx
import neopixel
from rainbowio import colorwheel
import digitalio
import busio
from digitalio import DigitalInOut, Direction, Pull
import gc
import storage


# LED pins and setup
led_neo = neopixel.NeoPixel(board.NEOPIXEL, 1)     

# BMP388
i2c = busio.I2C(board.SCL1, board.SDA1)
bmp = adafruit_bmp3xx.BMP3XX_I2C(i2c)
bmp.pressure_oversampling = 2
bmp.temperature_oversampling = 2



# On board button (its the boot select one, in front of the I2C port)
button = DigitalInOut(board.BUTTON)
button.direction = Direction.INPUT


"""
How to set up filesystem:
For launch: Uncomment prep_files(), press button, and you are ready

For REPL viewing and code execution: set dev mode to true, upload that to the drive, 
then plug into computer with with pin A0 jumped to ground

For editing code/changing files on the drive: just plug in and do whatever
"""

# Be able to write to storage
# Needs to be disableed when connect to a computer in order to allow code to execute




# ------------------------- options ------------------------
launch_delay = 20
development_mode = 1
led_neo.brightness = 1
file_name = "launch.csv"  
bmp.sea_level_pressure = 1014       
event_comma_count = ",,,," # makes sure events go in their own column on the far right 

# ------------------------- storage ------------------------
STARTING_ALTITUDE = bmp.altitude
data_cycles = 0
log_list = []
i = 0


def prep_files():
    print("Waiting for button press to allow writing to storage")
    led_neo[0] = (255, 255, 0)
    while True:
        if button.value == False:
            break
    storage.remount("/", False)
if development_mode == 0:
    prep_files()


while True: # press button to start the countdown
    i = (i + 1) % 256  # run from 0 to 255
    led_neo.fill(colorwheel(i)) # Unicorn barf
    time.sleep(0.01)
    if button.value == False:
        break


with open(file_name, "a") as f:     # might need to be with open("/" + file_name, "a") as f:
    f.write(",,,,\n")
    f.write("Software version: " + version + "\n")
    f.write("Starting altitude: " + str(STARTING_ALTITUDE) + "\n")
    f.write("Barometer pressure: {:5.2f},".format(bmp.pressure,) + "\n")
    f.write("Temperature: {:5.2f},".format(bmp.temperature) + "\n")
    #f.write("Pressure (mbar),Temperature (°c),Altitude (m),Time (s)\n")   
    f.write("Altitude (m),Time (s)\n") 

# Countdown
if development_mode == 0:
    for i in range(launch_delay):   
        led_neo[0] = (255, 255, 255)
        launch_delay -= 1
        print("T- " + str(launch_delay))
        time.sleep(0.5)
        led_neo[0] = (0, 0, 0)
        time.sleep(0.5)
else:
    dev_countdown = 3
    for i in range(3):   
        led_neo[0] = (255, 0, 255)
        launch_delay -= 1
        print("T- " + str(dev_countdown))
        time.sleep(0.5)
        led_neo[0] = (0, 0, 0)
        time.sleep(0.5)

led_neo[0] = (0, 255, 128)
print("Waiting for liftoff...")

if development_mode == 0:
    while True:
        if bmp.altitude >= STARTING_ALTITUDE + 2:
            break

led_neo[0] = (0, 0, 255) # this is for dev purposes, you wont see it because the rocket will be in the air already


#                          ------------------------ Main data logging code ------------------------
print("Logging...")
initial_time = time.monotonic() # needs to be here and not in the time set ups bits code for reasons
try:
    while True:    
        current_time = time.monotonic()
        time_stamp = current_time - initial_time
        bmp_alt = bmp.altitude
        log_list.extend([
        "\n"
        #"{:5.2f},".format(bmp.pressure),
        #"{:5.2f}".format(bmp.temperature),
        "{:5.2f}".format(bmp_alt),
        "{:5.2f}".format(time_stamp)
        ])
        # stops the logging of data
        if data_cycles > 300:
            if bmp_alt <= STARTING_ALTITUDE + 8: 
                with open(file_name, "a") as f: 
                    f.write("Stopped logging; low altitude met.\n")
                    break

        remainder = data_cycles % 120
        is_divisible = remainder == 0
        if is_divisible == True:   # this prevents the RAM from running out
            with open(file_name, "a") as f:
                f.write(','.join(log_list))
            #gc.collect()
            log_list.clear()
            print("RAM flushed")


        data_cycles += 1 
        print("Data cycles: " + str(data_cycles)) # for debugging while editing code
    #                          ------------------------ End of main data logging code ------------------------
except MemoryError: 
    #gc.collect()
    pass # log data incase there is an error that stopped the data logging

print("writing data to file system...")
with open(file_name, "a") as f:
    f.write(','.join(log_list))
print("write done")

while True:
    led_neo[0] = (0, 255, 0)
    