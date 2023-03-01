from digitalio import DigitalInOut
import time, busio, digitalio, board, neopixel, adafruit_rfm9x, storage, adafruit_ssd1306
import analogio, traceback, pulseio, datetime, traceback
from colorama import init
init()
from colorama import Fore
init(autoreset=True)

"""
Authored by besser435, March 2023

Autism Ray is Chungus Aerospace's system to locate a rocket
using LoRa 915MHz radios. Once the rocket lands, we will
scan the area for the radio beacon using a directional antenna.
We will keep moving the antenna back and forth until the signal
strength is the strongest. Then we will know what direction
to head in to find the rocket. Not sure if this will even work, 
but we might as well try.

This is the ground station code, it will help us find the rocket.
"""

version = "Autism Ray v0.1 (Ground)"

# I2C
i2c = busio.I2C(board.SCL, board.SDA)

# Neopixel
led_neo = neopixel.NeoPixel(board.NEOPIXEL, 1)

# RFM95
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
cs = digitalio.DigitalInOut(board.D18)
reset = digitalio.DigitalInOut(board.D19)
rfm9x = adafruit_rfm9x.RFM9x(spi, cs, reset, 915.0)
rfm9x.tx_power = 23
prev_packet = None

# 128x32 OLED Display
reset_pin = DigitalInOut(board.D4)
display = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c, reset=reset_pin) # OLD
display.fill(0)
display.show()
width = display.width
height = display.height

# Buzzer
buzzer = pulseio.PWMOut(board.D5, variable_frequency=True)
buzzer.frequency = 100
OFF = 0
ON = 2**15

# date and file path
now = datetime.datetime.now()
time_and_date = now.strftime("%m-%d-%Y  %H:%M")
FILE_LOCATION = "/home/pi/Desktop/" 


try:
    #raise UnicodeDecodeError   # for testing
    while True:
        packet = None   # this is to reset the vars for the next loop iteration
        rssi = None
        packet = rfm9x.receive()
        rssi = rfm9x.last_rssi
        
        print("\n" * 20)
        if packet is None:
            print(Fore.YELLOW + "Received nothing! Listening again...")
        else:
            packet_text = str(packet, 'utf-8')  # UTF-8 untested. on TF it was sent as UFT-8, and decoded as ASCII
            print("Received (UTF-8): {0}".format(packet_text))
            print(Fore.CYAN + "RSSI:", rssi, "dB", "   at", time_and_date)
            
            buzzer.duty_cycle = ON

            # +900 makes the pitch higher as the signal get stronger. *4 shifts it to more comfy frequencies
            print("DEBUG RSSI buzzer freq: ", rssi * 4 + 900)
            buzzer.frequency = rssi * 4 + 900

            display.fill(0)
            display.text(packet_text, 0, 0, 1)
            display.text(rssi, 0, 13, 1)
            display.text(time_and_date, 0, 25, 1)
            display.show()

        time.sleep(0.1)

except Exception as e:
    print("Error occurred: \n")
    print(Fore.LIGHTRED_EX + str(traceback.format_exc()))
    buzzer.duty_cycle = OFF
    
    with open(FILE_LOCATION + "beacon_receiver_error.txt", "a") as f: 
        f.write(str(time_and_date) + "\n" + str(traceback.format_exc()))
        f.write("\n" * 2)

except KeyboardInterrupt:
    print("KeyboardInterrupt")
    buzzer.duty_cycle = OFF
    display.fill(0)
    display.show()
