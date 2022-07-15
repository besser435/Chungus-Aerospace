#Simple timer-based program for a flight computer
#v0.1, made for education purposes by Joe Mama

import time
import board
import digitalio
import adafruit_bmp3xx
import neopixel
import busio

#LED setup
led0 = neopixel.NeoPixel(board.NEOPIXEL, 1)  

#Baro setup
i2c = busio.I2C(board.SCL1, board.SDA1)
bmp = adafruit_bmp3xx.BMP3XX_I2C(i2c)

START_ALT = bmp.altitude

#Relay setup
relay = digitalio.DigitalInOut(board.A0) #put proper pin here
relay.direction = digitalio.Direction.OUTPUT

#Delay logic
while True:
    led0[0] = (0, 255, 0)

    if bmp.altitude > START_ALT + 3:
        led0[0] = (0, 0, 255)
        time.sleep(6) #Seconds delay after launch
        relay.value = True
        time.sleep(3)
        relay.value = False
        break
