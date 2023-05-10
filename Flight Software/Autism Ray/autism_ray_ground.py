from digitalio import DigitalInOut
import time, busio, digitalio, board, adafruit_rfm9x, adafruit_ssd1306
import traceback, datetime, traceback
from colorama import init
init()
from colorama import Fore
init(autoreset=True)
import RPi.GPIO as GPIO
from gpiozero import CPUTemperature

"""
Authored by besser435
Created February 2023
Revised March 2023

Autism Ray is Chungus Aerospace's system to locate a rocket
using LoRa 915MHz radios. Once the rocket lands, we will
scan the area for the radio beacon using a directional antenna.
We will keep moving the antenna back and forth until the signal
strength is the strongest. Then we will know what direction
to head in to find the rocket. Not sure if this will even work, 
but we might as well try.

This is the ground station code, it will help us find the rocket.
"""
version = "Autism Ray v1.1.2 (Ground)"

# I2C
i2c = busio.I2C(board.SCL, board.SDA)

# RFM95
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
cs = digitalio.DigitalInOut(board.CE1)
reset = digitalio.DigitalInOut(board.D25)
rfm = adafruit_rfm9x.RFM9x(spi, cs, reset, 900.0) # NOTE 900MHz, not 915
rfm.tx_power = 23
prev_packet = None

# 128x32 OLED Display
reset_pin = DigitalInOut(board.D4)
display = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c, reset=reset_pin) # OLD LIB
display.fill(0)
display.show()
width = display.width
height = display.height

# Buzzer
GPIO.setmode(GPIO.BCM)
GPIO.setup(12, GPIO.OUT)  
buzz = GPIO.PWM(12, 1000) 
GPIO.setwarnings(False)

# other stuff
now = datetime.datetime.now()
time_and_date = now.strftime("%m-%d-%Y %H:%M")
FILE_LOCATION = "/home/pi/Desktop/" 
cpu = CPUTemperature()

while True:
    try:   
        packet = None   # this is to reset the vars for the next loop iteration
        rssi = None
        packet = rfm.receive()
        rssi = rfm.last_rssi

        if packet is None:
            print(Fore.YELLOW + "Received nothing! Listening again...")
            print("Pi CPU Temp: " + str(cpu.temperature))
            buzz.start(0)
            display.fill(0)
            display.text("Received nothing!", 0, 0, 1)
            display.show()
        else:
            packet_text = str(packet, 'utf-8') 
            print("Received (UTF-8): {0}".format(packet_text))
            print(Fore.CYAN + "RSSI: " + str(rssi) + "dB", "   at", time_and_date)
            print("Pi CPU Temp: " + str(cpu.temperature))
            buzz.start(50)
            buzz.ChangeFrequency((rssi * 4 + 900))
            # +900 makes the pitch higher as the signal gets stronger. *4 shifts it to more comfy frequencies
            #print("DEBUG RSSI buzzer freq: ", rssi * 5 + 900)
            
            display.fill(0)
            display.text(packet_text[11:], 0, 0, 1)
            display.text("RSSI: " + str(rssi), 0, 13, 1)
            display.text(time_and_date, 0, 25, 1)
            display.show()
        time.sleep(0.4)

    except Exception as e:
        print("Error occurred: \n")
        print(Fore.LIGHTRED_EX + str(traceback.format_exc()))
        buzz.start(0)
        display.fill(0)
        display.show()
        with open(FILE_LOCATION + "beacon_receiver_error.txt", "a") as f: 
            f.write(version + "\n")
            f.write(str(time_and_date) + "\n" + str(traceback.format_exc()))
            f.write("\n" * 2)
        break
    
    except KeyboardInterrupt:
        print("KeyboardInterrupt")
        buzz.start(0)
        display.fill(0)
        display.show()
