def notes():
    """
    NOTE
    ---Chungus Aerospace AIO Rocket Software---
    https://github.com/besser435/Chungus-Aerospace

    This program has everything that Chungus Aerospace needs.


    """

    # potential menu concept
    """
    This will display telem data, it should update about every second.
    Maybe put the menu in a for loop with a 1 second sleep
    Make a GUI rather than CLI UI, only if the hanging issue is solved. use pygame_menu or something

    CALC v2
    Status: Idle
    Pi Temp: 30c

    Options:
    1.  Prep for launch
    2.  Checklist
    3.  Display last launch data summary
    4.  Push last launch to GitHub (maybe automate this, or dont that could be a disaster) # engineering nighmare for me



    """

    """
    Last Launch Summary
    Total burn time:
    Apogee:
    Max speed:


    """


version = "v0.1.3"
date = "January 2022"

"""
import adafruit_bmp3xx
import adafruit_adxl34x
import adafruit_pcf8523
import adafruit_sdcard
import neopixel
import board
import digitalio
import storage
from rainbowio import colorwheel
from analogio import AnalogIn
"""
import random
import time 
import sys
import os  
from colorama import init   # pip install colorama
init()
from colorama import Fore, Back, Style
init(autoreset=True)
import requests
from requests.structures import CaseInsensitiveDict
import math 

"""
# Setup Bits
# I2C
i2c = board.I2C() 

# Batt voltage
vbat_voltage = AnalogIn(board.VOLTAGE_MONITOR)
def get_voltage(pin):
    return (pin.value * 3.3) / 65536 * 2
battery_voltage = get_voltage(vbat_voltage)

# pin D10 for Feather M4 Express
SD_CS = board.D10   
spi = board.SPI()
cs = digitalio.DigitalInOut(SD_CS)

# SD mount
sdcard = adafruit_sdcard.SDCard(spi, cs)
vfs = storage.VfsFat(sdcard)
storage.mount(vfs, "/sd")

# LED pins and setup
led_neo = neopixel.NeoPixel(board.NEOPIXEL, 1)
led = digitalio.DigitalInOut(board.D13)           
led.direction = digitalio.Direction.OUTPUT         

# BMP388
bmp = adafruit_bmp3xx.BMP3XX_I2C(i2c)
bmp.pressure_oversampling = 8
bmp.temperature_oversampling = 2

# ADXL345
accel = adafruit_adxl34x.ADXL345(i2c)

# Real time clock
#i2c = busio.I2C(board.SCL, board.SDA)
rtc = adafruit_pcf8523.PCF8523(i2c)
t = rtc.datetime

# Relay to deploy chute
chute_relay = digitalio.DigitalInOut(board.A1)  # NOTE change this pin to whatever pin is good. 
chute_relay.direction = digitalio.Direction.OUTPUT
"""

# options
debug = 0
launch_countdown = 4    # how long the countdown is in seconds


# storage
weather_api_key = "1392d31baeec1ab9f5d2bd99d5ec04aa"


def cc():   # shortens this long command to just cc()
    os.system("cls" if os.name == "nt" else "clear")    # clears terminal


def flight_software():
    cc()
    print("Get lastest version from other file.")
    main_menu()

    
def weather():
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    zip_code = "85054"
    use_zip = 1
    city_name = "phoenix"


    if use_zip == 0:
        complete_url = base_url + "appid=" + weather_api_key + "&q=" + city_name
    else:
        complete_url = base_url + "appid=" + weather_api_key + "&q=" + zip_code

    print("URL sent: " + complete_url)

    response = requests.get(complete_url)
    x = response.json()

    
    if x["cod"] != "404":
        if use_zip == 0:
            print("Check weather! Requesting cities can return the wrong info")
            print("Weather in " + city_name)
        else:
            print("Weather in " + str(zip_code))

        y = x["main"]
        current_temperature = y["temp"]
        z = x["weather"]
        weather_description = z[0]["description"]
        current_pressure = y["pressure"]
        

        print("Temp in Kelvin = " + str(math.trunc(current_temperature)))
        print("Temp in Celsius = " + str(math.trunc(current_temperature - 273.15)))
        print("Temp in Fahrenheit = " + str(math.trunc((1.8 * current_temperature) - 459.67)))
        print("Description = " + str(weather_description))
        print("Pressure in millibars = " + str(current_pressure))
        print("Pressure in inches of Hg = " + str(round(current_pressure/33.864, 3)))
        #print(x) # prints raw json data
    else:
        print("City Not Found")

    
    def response_code():
        headers = CaseInsensitiveDict()
        headers["Accept"] = "application/json"

        resp = requests.get(complete_url, headers=headers)
        print()

        print("Response code: ", end="")
        print(resp.status_code, end="")
        if resp.status_code == 200:
            print(" = Processed request succsessfully")
    response_code()  

    input("Press enter to return to the main menu")
    cc()
    main_menu()


def view_sensors():
    #break_sensors = input("Press enter to return to the menu")
    """while True:
        print("Voltage: {:.2f}".format(battery_voltage) + "v")
        print("Time: %d:%02d:%02d" % (t.tm_hour, t.tm_min, t.tm_sec))
        print("Altitude: {:5.2f}" + bmp.altitude + "m")
        print("Pressure: {:5.2f}" + bmp.pressure + "mbar")
        print("Temperature: " + bmp.temperature + "°c")
        print("Acceration: %.2f %.2f %.2f," % accel.acceleration)
        print("hi")
        time.sleep(0.25)
        cc()

        break_sensors = input("Press enter to return to the menu")
        if break_sensors:
            break       # test me"""
    wait = 0
    while True:
        print("hi")
        time.sleep(0.2)
        cc()
        wait += 1

        if wait >= 20:  # after 20 updates the loop ends. maybe try keyboard module to break instead of hard update cap
            break



    cc()
    main_menu()


def begin_countdown():
    global launch_countdown


    confirm_countdown = input("Are you sure you want to start the countdown? y/n ")
    if confirm_countdown == "y":


        cc()
        print(Fore.CYAN + "Starting Countdown. Press CTRL + C to cancel")   # maybe try keyboard module to cancel rather than interrupt
        print()

        for i in range(launch_countdown):
            launch_countdown -= 1
            print(Fore.LIGHTYELLOW_EX + str(launch_countdown))
            #led_neo[0] = (255, 255, 255)
            time.sleep(1)
            #led_neo[0] = (0, 0, 0)
            

        flight_software()
        #live_telem()    # this will probably just have to be in the launch software rather than a seperate function. maybe a seperate python script

    else:
        cc()
        main_menu()


def main_menu():    

    # set LED to rainbow barf RGB 
    print("Chungus Aerospace Software By Besser")
    print(version)
    print(date)
    
    if debug:
        pass
    print()
    print(Fore.CYAN + "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print(Fore.LIGHTGREEN_EX + "Options:")
    print("1: Start Launch Wizard")     # not a wizrd currently. it just starts the launch function
    print("2: Checklist")
    print("3: Display last launch summary")
    print("4. Push last launch to GitHub")
    print("5. View current sensor data")
    print("6. View weather")
    print("7. Motor Static Fire Test")
    print("8. Parachute Ejection Test")
    print("Q: Quit")
  
    which_option = input("What would you like to do? ")

    if "1" == which_option:
        cc()
        begin_countdown()
        #launch()
        
    elif "2" == which_option:
        cc()
        main_menu()
        
    elif "3" == which_option:
        cc()

    elif "4" == which_option:
        cc()

    elif "5" == which_option:
        cc()
        view_sensors()

    elif "6" == which_option:
        cc()
        weather()

    elif "q" == which_option:
        sys.exit()
    
    elif "a" == which_option:  # shortcut to current work
        pass 

    else:
        cc()
        print(Fore.RED + "Invalid input")
        main_menu()

def debug_messages():
    if debug:
        pass

main_menu()
