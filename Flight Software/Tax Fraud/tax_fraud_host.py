"""
Flight system to send and receive GPS coords and flight data using
a LoRa RFM95 radio
"""

version = "Tax Fraud v0.1 (Host)"
print(version)

from colorama import init
init()
from colorama import Fore
init(autoreset=True)
import traceback
import time
from datetime import datetime
import datetime
import busio
from digitalio import DigitalInOut, Direction, Pull
import board
import adafruit_ssd1306 # OLED display, this libary is deprecated. update to displayio
import adafruit_rfm9x
from gpiozero import CPUTemperature
cpu = CPUTemperature()

# Button A
btnA = DigitalInOut(board.D5)
btnA.direction = Direction.INPUT
btnA.pull = Pull.UP

# Button B
btnB = DigitalInOut(board.D6)
btnB.direction = Direction.INPUT
btnB.pull = Pull.UP

# Button C
btnC = DigitalInOut(board.D12)
btnC.direction = Direction.INPUT
btnC.pull = Pull.UP

# I2C
i2c = busio.I2C(board.SCL, board.SDA)

# 128x32 OLED Display
reset_pin = DigitalInOut(board.D4)
display = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c, reset=reset_pin) # OLD
display.fill(0)
display.show()
width = display.width
height = display.height

# Configure Packet Radio
CS = DigitalInOut(board.CE1)
RESET = DigitalInOut(board.D25)
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, 915.0)
prev_packet = None
# Optionally set an encryption key (16 byte AES key). MUST match both
# on the transmitter and receiver (or be set to None to disable/the default).
#rfm69.encryption_key = b"\x01\x02\x03\x04\x05\x06\x07\x08\x01\x02\x03\x04\x05\x06\x07\x08"

# File stuff
now = datetime.datetime.now()
time_and_date = now.strftime("%m-%d-%Y  %H:%M")
TIMEDATE = time_and_date
FILE_NAME = "tf data " + TIMEDATE + ".csv"
#FILE_NAME = "tf data.csv"
file_location = "/home/pi/Desktop/" 


# options


# storage
start_launch = bytes("start_launch\r\n", "utf-8")


with open(file_location + FILE_NAME, "a") as f: 
    f.write("\n")

try:
    def recovery():
        while True:
            packet = None
            packet = rfm9x.receive(keep_listening=True)
            if packet is None:
                #print("Received nothing! Listening again...")
                #print("SoC Temp: " + str(cpu.temperature))
                pass
            else:
                packet_text = str(packet, "ascii")

                mode = packet_text.split(",")[0]
                lat = packet_text.split(",")[1]
                lon = packet_text.split(",")[2]
                gps_alt = packet_text.split(",")[3]
                gps_time = packet_text.split(",")[4]
                sat_count = packet_text.split(",")[5]
                tf_batt = packet_text.split(",")[6]

                print(
                    #"Raw packet: " + packet_text + "\n" # formatted
                    "Mode: " + str(mode) + "\n"
                    "Latitude: " + lat + "\n"
                    "Longitude: " + lon + "\n"
                    "Altitude: " + gps_alt +"\n"
                    "GPS Time (UTC): " + gps_time + "\n"   # Phoenix UTC offset is -07:00
                    "Sat Count: " + sat_count + "\n"
                    "Batt Voltage: " + tf_batt + "\n"
                    "RSSI: " + str(rfm9x.last_rssi) + "\n"  # dBm
                    )
            #time.sleep(1)






    while True:
        display.fill(0)
        display.text(version, 0, 0, 1)
        display.show()
        

        if not btnA.value:
            # display start stats, like batt voltage, TF status, # of satellites, etc.
            pass
        if not btnB.value:
            # display current rocket launch info, alt, speed
            pass
        if not btnC.value:
            # display ground info, location batt voltage
            pass
        #maybe do all this automatically 


        # the code below should be in a function that the two conditions above call
        # fetch the data from the returned packet
        packet = None
        packet = rfm9x.receive(keep_listening=True)
        if packet is None:
            #print("Received nothing! Listening again...")
            #print("SoC Temp: " + str(cpu.temperature))
            pass
        else:
            prev_packet = packet
            packet_text = str(packet, "ascii")
           
            dt_time = datetime.datetime.now()
            time_date = dt_time.strftime("%m-%d-%Y, %H:%M:%S") 


            if packet_text.split(",")[0] == "recovery_mode":
                print(Fore.RED + "Recovery Mode1")
                recovery()
                break
         

            # returned data
            #mode = packet_text.split(",")[0]
            bmp_alt = packet_text.split(",")[0]
            lat = packet_text.split(",")[1]
            lon = packet_text.split(",")[2]
            gps_alt = packet_text.split(",")[3]
            gps_speed = packet_text.split(",")[4]
            gps_time = packet_text.split(",")[5]
            sat_count = packet_text.split(",")[6]
            tf_batt = packet_text.split(",")[7]
            time_stamp = packet_text.split(",")[8]   
            


            print()
            print(
                #"Raw packet: " + packet_text + "\n" # formatted
                "Local Time: " + str(time_date) + "\n"
                "Baro Alt: " + bmp_alt + "\n"
                "GPS Alt: " + gps_alt +"\n"
                "Latitude: " + lat + "\n"
                "Longitude: " + lon + "\n"
                "GPS Speed: " + gps_speed + "\n"    # knots
                "GPS Time (UTC): " + gps_time + "\n"   # Phoenix UTC offset is -07:00
                "Sat Count: " + sat_count + "\n"
                "Batt Voltage: " + tf_batt + "\n"
                "Loop time: " + time_stamp + "\n"
                "RSSI: " + str(rfm9x.last_rssi) + "\n"  # dBm
                "SoC Temp: " + str(cpu.temperature)
                )


            # log the data to the file
            #with open(file_location + FILE_NAME, "a") as f: 
                #f.write(+ str(time_date) + "\n")


        display.show()







except Exception:
    # sometimes the radio receives its own request for some reason
    #print("F-fucky wucky detected! IndexError bwyte awway out of wange!") # war crime soup :)
    # make a print command that diplsays the error message
    print(traceback.format_exc())   


 