"""
Flight system to send and receive GPS coords and flight data using
a LoRa RFM95 radio
"""

version = "Tax Fraud v0.2 (Host)"
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
#TIMEDATE = time_and_date
TIMEDATE = "no"
FILE_NAME = "tf data " + TIMEDATE + ".csv"
#FILE_NAME = "tf data.csv"
file_location = "/home/pi/Desktop/" 


# options


# storage
start_launch = bytes("start_launch\r\n", "utf-8")
log_list = []
last_lat = None
last_lon = None
has_logged = False

with open(file_location + FILE_NAME, "a") as f: 
    f.write("\n")

try:
    def recovery(): # Flight has ended
        # log the data to the file
        """with open(file_location + FILE_NAME, "a") as f: 
        f.write(+ str(time_date) + "\n")"""
        while True:
            #
            """
            rfm9x SEND enter recovery mode 
            make it do TF can enter recovery mode manually via a
            radio command during whatever state is in incase it never gets
            to recovery mode
            """
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
 

    def main():     # Logic
        global has_logged
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

            # fetch the data from the returned packet
            packet = None
            packet = rfm9x.receive(keep_listening=True)
        
            if packet is None:
                print("Received nothing! Listening again...")
            else:
                packet_text = str(packet, "ascii")
                mode = packet_text.split(",")[0]

                # ----------- pad mode -----------          (waiting for liftoff)
                if mode == "pad_mode":  
                    has_fix = packet_text.split(",")[1]
                    sat_count = packet_text.split(",")[2]
                    print("Waiting for liftoff...")
                    if has_fix == "False": print("Has GPS fix: " + Fore.RED + "False, DO NOT LAUNCH!")
                    elif has_fix == "True": print("Has GPS fix: " + Fore.GREEN + "True")
                    else: print("some kind of error")
                    print("Sat count: " + str(sat_count))   
                    print()                     

                # ----------- launch mode -----------       (logging data)
                if mode == "launch_mode":
                    
                    dt_time = datetime.datetime.now()
                    time_date = dt_time.strftime("%m-%d-%Y, %H:%M:%S") 

                    # returned data
                    """this might not be needed, just log packet_text"""
                    all_data = (
                        packet_text.split(",")[1],  # bmp_alt
                        packet_text.split(",")[2],  # lat
                        packet_text.split(",")[3],  # long
                        packet_text.split(",")[4],  # gps_alt
                        packet_text.split(",")[5],  # gps_speed
                        packet_text.split(",")[6],  # gps_time
                        packet_text.split(",")[7],  # sat_count
                        packet_text.split(",")[8],  # tf_batt
                        packet_text.split(",")[9],  # time_stamp
                    )
                    log_list.extend([all_data])

                    """bmp_alt = packet_text.split(",")[1]
                    lat = packet_text.split(",")[2]
                    lon = packet_text.split(",")[3]
                    gps_alt = packet_text.split(",")[4]
                    gps_speed = packet_text.split(",")[5]
                    gps_time = packet_text.split(",")[6]
                    sat_count = packet_text.split(",")[7]
                    tf_batt = packet_text.split(",")[8]
                    time_stamp = packet_text.split(",")[9]
                    
                    print()
                    print(
                        "Local Time: " + str(time_date) + "\n"
                        "Mode: " + str(mode) + "\n"
                        "Baro Alt: " + bmp_alt + "\n"
                        "GPS Alt: " + gps_alt +"\n"
                        "Latitude: " + lat + "\n"
                        "Longitude: " + lon + "\n"
                        "GPS Speed: " + gps_speed + "\n"       # knots
                        "GPS Time (UTC): " + gps_time + "\n"   # Phoenix UTC offset is -07:00
                        "Sat Count: " + sat_count + "\n"
                        "Batt Voltage: " + tf_batt + "\n"
                        "Loop time: " + time_stamp + "\n"
                        "RSSI: " + str(rfm9x.last_rssi) + "\n"  # dBm
                        "SoC Temp: " + str(cpu.temperature)
                        )
                    """


                    print(
                        "Local Time: " + str(time_date) + "\n"
                        "Mode: " + str(mode) + "\n"
                        "Baro Alt: " + all_data[0] + "\n"
                        "GPS Alt: " + all_data[1] +"\n"
                        "Latitude: " + all_data[2] + "\n"
                        "Longitude: " + all_data[3] + "\n"
                        "GPS Speed: " + all_data[4] + "\n"       # knots
                        "GPS Time (UTC): " + all_data[5] + "\n"   # Phoenix UTC offset is -07:00
                        "Sat Count: " + all_data[6] + "\n"
                        "Batt Voltage: " + all_data[7] + "\n"
                        "Loop time: " + all_data[8] + "\n"
                        "RSSI: " + str(rfm9x.last_rssi) + "\n"  # dBm
                        "SoC Temp: " + str(cpu.temperature))

                # ----------- recovery mode -----------     (goes to recovery func)
                if mode == "recovery_mode" and has_logged == False:
                    with open(file_location + FILE_NAME, "a") as f: 
                        f.write(str(all_data) + "\n")
                    has_logged = True

                    recovery()
                
                # ----------- wait for GPS mode -----------
                if mode == "gps_fix_wait":
                    print("Waiting for GPS fix...")
                    print()


            display.show()
    main()


except Exception:
    # sometimes the radio receives its own request for some reason
    # make a print command that diplsays the error message
    print(Fore.YELLOW + traceback.format_exc())   
    print(Fore.YELLOW + "Error, going to recovery mode in 3 seconds")
    print("Last known lat: " + str(last_lat))
    print("Last known lon: " + str(last_lon))

    with open(file_location + FILE_NAME, "a") as f: 
        f.write(str(log_list) + "\n")

    time.sleep(3)
    recovery()



 