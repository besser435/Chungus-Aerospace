"""
---Chungus Aerospace Program---
https://github.com/besser435/Chungus-Aerospace

Flight Software for the CircuitPython platform by Joe Mama and besser
This current code is meant to run an a Feather M4. Thats what the 
pinouts are configured for.

Currenty this only collects data, it doesn't control anything (yet)

"""


version = "v0.2.2"
date = "January 2022"

# idea: add wifi module so it can fetch the current pressure in phoenix. this way we
# dont have to get it manually then update the code or whateverD
import adafruit_bmp3xx
import time
import analogio
import board
import digitalio
import storage
import adafruit_sdcard
from rainbowio import colorwheel
import adafruit_dotstar
import neopixel
import microcontroller


#vbat_voltage = analogio.AnalogIn(board.D9)

i2c = board.I2C() # uses board.SCL and board.SDA

SD_CS = board.D10   # pin D10 for Feather M4 Express
spi = board.SPI()
cs = digitalio.DigitalInOut(SD_CS)

sdcard = adafruit_sdcard.SDCard(spi, cs)
vfs = storage.VfsFat(sdcard)
storage.mount(vfs, "/sd")

# For Feather M0 Express, Metro M0 Express, Metro M4 Express, Circuit Playground Express, QT Py M0
led = neopixel.NeoPixel(board.NEOPIXEL, 1)
led = digitalio.DigitalInOut(board.D13)
led.direction = digitalio.Direction.OUTPUT

# I2C setup
i2c = board.I2C()  # uses board.SCL and board.SDA
bmp = adafruit_bmp3xx.BMP3XX_I2C(i2c)

# BMP388
bmp.sea_level_pressure = 1016
bmp.pressure_oversampling = 8
bmp.temperature_oversampling = 2


#print("Waiting for launch...")
#time.sleep(20)  # allows time for the rocket to be set up and have the launch started. This is awful and will be addressed later


"""
Old logging code that I dont want to delete incase the new stuff bungs up

while True:
    # open file for append
    with open("/sd/launch_stats.txt", "a") as f:    # a means to append to the file, not overwrite it
        led.value = True  # turn on LED to indicate we're writing to the file
        f.write("Pressure: {:5.2f}  Temperature: {:5.2f}  Altitude: {:5.2f}\n".format(bmp.pressure, bmp.temperature, bmp.altitude))
        led.value = False  # turn off LED to indicate we're done
    # file is saved
    print("Logged to file")
    time.sleep(0.1)

      
    LED colors:
    White - idle
    Yellow flash - countdown
    Green flash - executing code/logging data

    
  
"""

# check if there is a file on the SD card. if there is, create a new one with
# a different file name so the old one isnt overwritten


writes_to_file = 0

with open("/sd/launch_stats.txt", "a") as f:
    f.write("Pressure, Temperature, Altitude\n")
    writes_to_file += 1

while True:
    # open file for append
    with open("/sd/launch_stats.txt", "a") as f:    # a means to append to the file, not overwrite it
        led.value = True  # turn on LED to indicate we're writing to the file

        f.write("{:5.2f},{:5.2f},{:5.2f}\n".format(bmp.pressure, bmp.temperature, bmp.altitude))

        led.value = False  # turn off LED to indicate we're done

    writes_to_file += 1
    print("Writes to file: " + str(writes_to_file)) # for debugging while editing code

    time.sleep(0.05)











#add RTC code and include it in the log


def get_voltage(pin):
    return (pin.value * 3.3) / 65536 * 2


"""
It should still be enabled to be tested tho
# proof of concept parachute code
while True:
    if bmp.altitude >= 50:  # arms at 50 meters
        #log the arm event
        # currently on a while loop so once armed it will just continue to log it. do a check to see if it has been logged already
            if bmp.altitude <= 49:  # one the rocket sinks below 50 meters it fires the chute
                #do your mom    # deploys chute
                #log the deploy event
                break # get out of this loop somehow so the charge doesnt constantly fire. i dont think this break works
"""


while True:
    print(
        "Pressure: {:5.2f}  Temperature: {:5.2f}  Altitude: {:5.2f}".format(bmp.pressure, bmp.temperature, bmp.altitude))
    time.sleep(0.5)








