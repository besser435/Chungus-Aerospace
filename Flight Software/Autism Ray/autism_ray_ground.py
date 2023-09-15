from digitalio import DigitalInOut
import time, busio, digitalio, board, adafruit_rfm9x, adafruit_ssd1306
from digitalio import DigitalInOut, Direction, Pull
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
Revised May 2023

Autism Ray is Chungus Aerospace's system to locate a rocket
using LoRa 915MHz radios. Once the rocket lands, we will
scan the area for the radio beacon using a directional antenna.
We will keep moving the antenna back and forth until the signal
strength is the strongest. Then we will know what direction
to head in to find the rocket. Not sure if this will even work, 
but we might as well try.

This is the ground station code, it will help us find the rocket.
"""
version = "Autism Ray v1.2 (Ground)"

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

# Button A
btnA = DigitalInOut(board.D5)
btnA.direction = Direction.INPUT
btnA.pull = Pull.UP

# Buzzer
GPIO.setmode(GPIO.BCM)
GPIO.setup(12, GPIO.OUT)  
buzz = GPIO.PWM(12, 1000) 
GPIO.setwarnings(False)

# other stuff
beeper_toggle = 1
FILE_LOCATION = "/home/pi/Desktop/" 
cpu = CPUTemperature()

while True:
    try:   
        now = datetime.datetime.now()
        time_and_date = now.strftime("%m-%d-%Y %H:%M")
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
            print(Fore.CYAN + "RSSI: " + str(rssi) + "dB", "at", time_and_date)
            #print("Pi CPU Temp: " + str(cpu.temperature))

            if beeper_toggle:
                buzz_freq = 2**(rssi / 20) * 10000
                #print("DEBUG RSSI buzzer freq:", buzz_freq)
                buzz.start(50)
                buzz.ChangeFrequency(buzz_freq)            
            else:
                buzz.start(0)

            display.fill(0)
            display.text(packet_text[11:], 0, 0, 1)
            display.text("RSSI: " + str(rssi) + "  HB: " + packet_text[44:] , 0, 13, 1)
            display.text(time_and_date, 0, 25, 1)
            display.show()

        if not btnA.value:
            beeper_toggle = not beeper_toggle
            print(Fore.GREEN + "Toggled Beeper to "  + str(beeper_toggle))

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
