"""
modified version of the Tax Fraud boot file
This needs to be modified to work with the board that it is going to run on.
Those modifications are what pins are used
"""

import board
import digitalio
import neopixel
import storage
import time

led_neo = neopixel.NeoPixel(board.NEOPIXEL, 1)
switch = digitalio.DigitalInOut(board.A0) 
switch.direction = digitalio.Direction.INPUT
switch.pull = digitalio.Pull.UP

# NOTE to be able to write to the drive for uploading and deleting files, the wire must be pulled to 5V
# if the write test is successful, the LED lights up green

storage.remount("/", not switch.value) # Pull switch to ground to enable onboard writes to the drive

try:
    with open("write_test.txt", "a") as f: 
        f.write("write success poggers\n")
    led_neo[0] = (0, 255, 0)
    time.sleep(1)

except Exception:
    led_neo[0] = (255, 0, 0)
    time.sleep(2)