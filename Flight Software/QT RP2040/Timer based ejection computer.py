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
relay = digitalio.DigitalInOut(board.i2c1) #pin here
relay.direction = digitalio.Direction.OUTPUT

#Delay logic
led0 = (0, 255, 0)

while True:
    if bmp.altitude > START_ALT + 3:
        led0 = (255, 0, 0)
        time.sleep(6) #Seconds delay after launch
        relay.value = True
        time.sleep(5)
        relay.value = False
        break