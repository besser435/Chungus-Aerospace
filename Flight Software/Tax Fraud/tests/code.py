import os
from digitalio import DigitalInOut, Direction, Pull
from analogio import AnalogIn
import time, busio, digitalio, board, neopixel, adafruit_rfm9x, storage, random
import adafruit_bmp3xx, adafruit_sdcard, analogio, traceback, adafruit_gps

# RFM95
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
cs = digitalio.DigitalInOut(board.D18)
reset = digitalio.DigitalInOut(board.D19)
rfm9x = adafruit_rfm9x.RFM9x(spi, cs, reset, 915.0)

#rfm9x.auto_agc = True # Enable Automatic Gain Control
rfm9x.tx_power = 23
rfm9x.long_range_mode = True # default is true

prev_packet = None

x = 0
while True:
    send_data = bytes(str(x), "\r\n","utf-8")
    rfm9x.send(send_data)
    #print(rfm9x.last_rssi)
    print(rfm9x.tx_power)
    print(x)
    x += 1
    time.sleep(0.5)

    
