def notes():
    """
    NOTE
    Chungus Aerospace AIO Rocket Software
    https://github.com/besser435/Chungus-Aerospace

    """



version = "CALC v2.0-alpha.2.3"
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
from colorama import init


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
launch_countdown = 3    # how long the countdown is in seconds


# storage
weather_api_key = "1392d31baeec1ab9f5d2bd99d5ec04aa"
preflight_errors = 0



def cc():   # shortens this long command to just cc()
    os.system("cls" if os.name == "nt" else "clear")    # clears terminal
cc()


def weather():
    global current_pressure
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    zip_code = "85054"
    use_zip = 0
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

    input("Press enter to return to the main menu ")
    cc()
    main_menu()


"""def push_github():
    This has been shelved for now. Moving the folder containing the launch logs
    to the host PC is a lot easier for a few reasons.

    print("Push to Github")
    print()

    ask_dir = input("Enter folder path to push: ")"""
    

def test_pyros_menu():
    test_type_ask = input("Would you like to test a motor or parachute? m/p ")

    if test_type_ask == "m":
        begin_countdown("Motor Test")

    elif test_type_ask == "p":
        begin_countdown("Parachute Test")

    else:
        cc()
        main_menu()


def test_charge(test_type):
    if test_type == "Motor Test":
        #relay motor pin + load cell logging
        print("motor test")

    elif test_type == "Parachute Test":
        #relay chute pin
        print("chute test")

    else:
        cc()
        print(Fore.RED + "Test error, test not found: " + test_type)
        main_menu()



# -------------------------------Main flight code-------------------------------
def flight_software():
    cc()
    print("Get lastest version from other file.")
    #bmp.sea_level_pressure = pressure
    
    main_menu()


def preflight_checks():
    # get weather
    #print("Is pressure correct?")
    


    # ----------------------Error checking----------------------
    #if battery voltage is low:
    #print(Fore.YELLOW + "Low battery voltage! (" + str(1) + ")")
        #preflight_errors += 1


    #if wind > x:
    #print(Fore.YELLOW + "High winds! (" + str(1) + ")")
        #preflight_errors += 1

    


    if preflight_errors > 0:
        print(Fore.RED + "Stopping the countdown. There are " + str(preflight_errors) + " preflight errors" )
        continue_launch = input("Continue with the launch? y/n ")

        if continue_launch == "y":
            cc()
            begin_countdown("Launch")

        else:
            cc()
            print(Fore.YELLOW + "Countdown aborted")
            main_menu()

    else:
        begin_countdown("Launch")


def begin_countdown(type):  # The type param is so other code can also use the countdown
    global launch_countdown
    cc()
    print("Countdown for " + Fore.GREEN + type)

    confirm_countdown = input("Are you sure you want to start the countdown? y/n ")
    if confirm_countdown == "y":

        cc()
        print(Fore.CYAN + "Starting " + type + " Countdown. Press CTRL + C to cancel")   
        print()

        for i in range(launch_countdown):
            launch_countdown -= 1
            print(Fore.LIGHTYELLOW_EX + str(launch_countdown))
            #led_neo[0] = (255, 255, 255)
            time.sleep(1)
            #led_neo[0] = (0, 0, 0)

            #check if the connection between my pc and the Pi is active.
            #that way if the connection stops it automatically stops the countdown
            #this is incase we need to cancel the countdown
    else:
        cc()
        main_menu()


    if type == "Launch":
        flight_software()
        # print the data in the main loop, but make sure prints dont slow down the logging

    elif type == "Motor Test":
        test_charge("Motor Test")

    elif type == "Parachute Test":
        test_charge("Parachute Test")




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


def main_menu():    
    # set LED to rainbow barf RGB 
    print("Chungus Aerospace Logic Controller By Besser and Joe Mamma")
    print(version)
    print(date)
    

    print()
    print(Fore.CYAN + "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print(Fore.LIGHTGREEN_EX + "Options:")
    print("1: Start Launch Wizard")     
    print("2: Checklist")
    print("3: Display last launch summary")
    #print("4. Push last launch folder to GitHub")
    print("5. View current sensor data")
    print("6. View weather")
    print("7. Test Fire Charges")
    print("9. CSV Flight Data Analyzer")
    print()
    print("S: Software settings")   # disable any wifi code, 
    print("Q: Quit")
  
    which_option = input("What would you like to do? ")


    # FUNCTIONS SHOULD CALL EACH OTHER, NOT JUST RAN HERE. THAT WAY ERRORS ARE CAUGHT


    if "1" == which_option:
        cc()
        preflight_checks()
        
    elif "2" == which_option:
        cc()
        main_menu()
        
    elif "3" == which_option:
        cc()
        main_menu()

    elif "4" == which_option:
        cc()
        #push_github()

    elif "5" == which_option:
        cc()
        view_sensors()

    elif "6" == which_option:
        cc()
        weather()

    elif "7" == which_option:
        cc()
        test_pyros_menu()

    elif "d" == which_option:   # d is for development. I can just put whatever I want there to run it quickly
        cc()
        test_pyros_menu()

    elif "q" == which_option:
        sys.exit()
    
    elif "a" == which_option:  # shortcut to current work
        pass 

    else:
        cc()
        print(Fore.RED + "Invalid input")
        main_menu()


main_menu()
