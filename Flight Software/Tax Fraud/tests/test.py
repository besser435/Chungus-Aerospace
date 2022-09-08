import digitalio
import traceback
import time
from datetime import datetime
import datetime
import busio
from digitalio import DigitalInOut, Direction, Pull
import board
import adafruit_ssd1306 # OLED display, this libary is deprecated. update to displayio
import adafruit_rfm9x

# Configure Packet Radio
CS = DigitalInOut(board.CE1)
RESET = DigitalInOut(board.D25)
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, 915.0)
prev_packet = None
i2c = busio.I2C(board.SCL, board.SDA)
# 128x32 OLED Display
reset_pin = DigitalInOut(board.D4)
display = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c, reset=reset_pin) # OLD
display.fill(0)
display.show()
width = display.width
height = display.height

#rfm9x.coding_rate = 5-8
#rfm9x.spreading_factor = 7 # only 7 seems to work as its the default
rfm9x.tx_power = 23
#rfm9x.enable_crc = True # Default is False
x = 0
try:
    while True:
        packet = None
        packet = rfm9x.receive(keep_listening=True)
        if packet is None:
            print("Received nothing! Listening again...")
            display.fill(0)
            display.text("Received nothing!", 0, 13, 1)
            display.show()
            #print("SoC Temp: " + str(cpu.temperature))
            pass
        else:
            prev_packet = packet
            #packet_text = str(packet)
            packet_text = str(packet, "ascii")
            print("Received: " + packet_text)
            print("RSSI: " + str(rfm9x.last_rssi))
            print("SNR: " + str(rfm9x.snr))
            print()
            display.fill(0)
            display.text("RSSI: " + str(rfm9x.last_rssi), 0, 0, 1)
            display.text("SNR: " + str(rfm9x.snr), 0, 13, 1)
            display.text("Received: " + str(packet_text), 0, 25, 1)
            display.show()
except Exception:
    display.fill(0)
    display.text("Exception!", 0, 0, 1)
    display.text(traceback.format_exc(), 13, 0, 1)
    display.show()
    print(traceback.format_exc())