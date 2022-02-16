version = "CALC v2.0-alpha.4"
date = "Febuary 2022"

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
from gpiozero import CPUTemperature
"""
import time 
import sys
import os
from unittest import main  
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
led_neo.brightness = 1  

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

# Motor ignition relay
motor_relay = digitalio.DigitalInOut(board.A0)  # NOTE change this pin to whatever pin is good. 
motor_relay.direction = digitalio.Direction.OUTPUT

"""
# options
debug = 0
#bmp.sea_level_pressure = 1024 # NOTE get this from weather data
launch_countdown = 11    # how long the countdown is in seconds

# storage
weather_api_key = "1392d31baeec1ab9f5d2bd99d5ec04aa"
preflight_errors = 0

# rocket storage
STARTING_ALTITUDE = 1000 #bmp.altitude
fire_chute_alt = 100    # default value in m, changes based on user input
arm_chute_alt = fire_chute_alt - 2

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
        main_menu()

    elif test_type == "Parachute Test":
        #relay chute pin
        print("chute test")
        main_menu()

    else:
        cc()
        print(Fore.RED + "Test error, test not found: " + test_type)
        main_menu()

def rocket_settings():
    global fire_chute_alt
    global arm_chute_alt    
    cc()  
    print(Fore.LIGHTGREEN_EX + "Rocket Settings:")
    print(Fore.CYAN + "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print()
    ask_chute_alt = input("What is the altitude the parachute should deploy at? (m) ")
    fire_chute_alt = STARTING_ALTITUDE + int(ask_chute_alt)
    arm_chute_alt = fire_chute_alt - 2 # 
    main_menu()

def a():
    print("Deploy parachute at " + str(fire_chute_alt) + "m")
    print("Arm parachute at " + str(arm_chute_alt) + "m")




# -------------------------------Main flight code-------------------------------
def flight_software():
    cc()
    # options
    log_stop_count = 400        # when to stop logging after an amount of data points are collected, backup to low altitude condition
    log_interval = 0.0          # Unlikely to be the actual number due to the polling rate of the sensors
    file_name = "launch " + str(t.tm_mon) + "-" + str(t.tm_mday) + "-" + str(t.tm_year) + ".csv"  # pure stupidity
    event_comma_count = ",,,,,," # makes sure events go in their own column on the far right 

    # storage
    data_cycles = 0
    logged_liftoff = 0
    chute_armed = 0 
    logged_chute_deploy = 0
    alt_1 = 0
    t_s_1 = 0
    
    # .csv creation and formatting
    with open("/sd/" + file_name, "a") as f: 
        f.write(",,,,,\n")  # creates the right amount of columns 
        f.write(str("Date: %d/%d/%d" % (t.tm_mon, t.tm_mday, t.tm_year) + ",,,,,\n"))   # The extra commas is so GitHub doesnt get cranky
        f.write("Time: %d:%02d:%02d" % (t.tm_hour, t.tm_min, t.tm_sec) + ",,,,,\n")
        f.write("Software version: " + version + ",,,,,\n")
        f.write("Starting altitude: " + str(STARTING_ALTITUDE) + ",,,,,\n")
        f.write("Data points cutoff: " + str(log_stop_count) + ",,,,,\n")
        f.write("Pressure (mbar),Temperature (°c),Altitude (m),Accel on xyz (m/s^2),v_speed (m/s),Elapsed Seconds,Events\n")

    with open("/sd/" + file_name, "a") as f:  # ignite motor 
        led_neo[0] = (20, 235, 35)    # indicates the motor has been fired and is waiting for liftoff detection to run log code
        f.write(event_comma_count + "Motor lit\n")
        motor_relay.value = True    # lauches the rocket 


    while True: # wait for liftoff then go to logging
        if bmp.altitude >= STARTING_ALTITUDE + 2:
            if logged_liftoff == 0:
                with open("/sd/" + file_name, "a") as f:
                    f.write("{:5.2f},{:5.2f},{:5.2f},".format(bmp.pressure, bmp.temperature, bmp.altitude,))
                    f.write("%.2f %.2f %.2f," % accel.acceleration,)
                    f.write(",Liftoff detected\n")
            
                    led_neo[0] = (0, 0, 255)    # indicates liftoff has been detected and it passed to the logging code.
                    # this is for dev purposes, you wont see it because the rocket will be in the air already

                motor_relay.value = False
                logged_liftoff += 1
                break

    #                          ------------------------ Main data logging code ------------------------
    initial_time = time.monotonic() # needs to be here and not in the time set ups bits code for reasons
    while True:   
        t_s_0 = time_stamp
        vert_speed = (bmp.altitude - alt_1) / (t_s_0 - t_s_1)

        with open("/sd/" + file_name, "a") as f:    
            current_time = time.monotonic()
            time_stamp = current_time - initial_time

            f.write("{:5.2f},{:5.2f},{:5.2f},".format(bmp.pressure, bmp.temperature, bmp.altitude, vert_speed,))
            f.write("%.2f %.2f %.2f," % accel.acceleration,)
            f.write("{:5.2f}".format(time_stamp) + ",\n") # logs elapsed time 
            # This is for when its connected wirelessly through a computer. This way we
            # can get live telem data (for as long as the rocket is in wireless range)
            print("Alt: " + str(bmp.altitude), end = ",   ")   
            print("Time:{:5.2f}".format(time_stamp))
            #print(vertical_speed)
            

            #https://learn.adafruit.com/circuitpython-digital-inputs-and-outputs/digital-outputs for relay pin and stuff
            # Arm
            if bmp.altitude >= STARTING_ALTITUDE + 50:  # I know that and statements are a thing, but this is easier to read imo
                if chute_armed == 0: # this is so the event isnt logged repeatedly
                    f.write(event_comma_count + "Armed parachute. Current alt: " + str(bmp.altitude) +  "m . Current time: " + str(time_stamp) + "m\n")
                    chute_armed += 1
                    print("Armed parachute")

            # Deploy - close relay
            if chute_armed == 1:
                if bmp.altitude <= STARTING_ALTITUDE + 49:  # once the rocket sinks below 50 meters it fires the chute  BUG adds logging delay
                    DATA_CYCLES_CHUTE = data_cycles 
                    chute_relay.value = True
                    print("Parachute relay on")

                    if logged_chute_deploy == 0:
                        f.write(event_comma_count + "Deployed parachute. Current alt: " + str(bmp.altitude) + "m. Current time: " + str(time_stamp) + "\n")
                        logged_chute_deploy +=1

                # Close relay
                if logged_chute_deploy == 1:    # this might not work. 
                    if DATA_CYCLES_CHUTE >= 10: # waits 10 data cyles before opening the relay
                        chute_relay.value = False   # this was True before and idk why. Does it actually need to be True?
                        f.write(event_comma_count + "Parachute relay off. Current time: " + str(time_stamp) + "\n")
                        print("Parachute relay off")


        # stops the logging of data
        if data_cycles > 50:    
            if bmp.altitude <= STARTING_ALTITUDE + 5:   # + 5 is incase it lands above the starting elevation or the sensor drifts
                with open("/sd/" + file_name, "a") as f:
                    f.write(event_comma_count + "Stopped logging; low altitude met. (" + str(bmp.altitude) + "m)\n")
                    break


        if data_cycles >= log_stop_count:   # backup to the code above
            with open("/sd/" + file_name, "a") as f:
                f.write(event_comma_count + "Stopped logging; writes to file met. (" + str(data_cycles) + " writes) ")
                f.write(event_comma_count + "This means altitude code did not execute.\n")
                break

        
        data_cycles += 1 # this seems simple but its crucial to some things so dont mess with it

        alt_1 = bmp.altitude 
        t_s_1 = time_stamp

        time.sleep(log_interval)
    #                          ------------------------ End of main data logging code ------------------------
    post_flight()


def post_flight():
    while True:     # indicates that the data recording is done
        i = (i + 1) % 256  # run from 0 to 255
        led_neo.fill(colorwheel(i)) # Unicorn barf
        time.sleep(0.01)

    end_flight = input("Press enter to end the flight")
    if end_flight:
        cc()
        main_menu()


def preflight_checks():
    global preflight_errors
    # get weather
    #print("Barometer pressure: " + bmp.altitude)
    #print("Weather pressure: ")
    print("Starting Altitude: " + str(STARTING_ALTITUDE))
    print()
    value_check = input("Are these values corrent? y/n ")
    if value_check == "y":
        pass # autism
    else:
        preflight_errors =+ 1
    
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
            print(Fore.YELLOW + "Launch aborted")
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
            time.sleep(0.5)
            #led_neo[0] = (0, 0, 0)
            time.sleep(0.5)

            #check if the connection between my pc and the Pi is active.
            #that way if the connection stops it automatically stops the countdown
            #this is incase we need to cancel the countdown
    else:
        cc()
        print(Fore.YELLOW + "Countdown aborted")
        main_menu()


    if type == "Launch":
        flight_software()

    elif type == "Motor Test":
        test_charge("Motor Test")

    elif type == "Parachute Test":
        test_charge("Parachute Test")




def view_sensors():
    
    """while True:
        print("Voltage: {:.2f}".format(battery_voltage) + "v")
        print("Time: %d:%02d:%02d" % (t.tm_hour, t.tm_min, t.tm_sec))
        print("Altitude: {:5.2f}" + bmp.altitude + "m")
        print("Pressure: {:5.2f}" + bmp.pressure + "mbar")
        print("Temperature: " + bmp.temperature + "°c")
        print("Acceration: %.2f %.2f %.2f," % accel.acceleration)
        print("hi")
        time.sleep(0.1)
        cc()"""

    wait = 0
    while True:
        print("hi")
        time.sleep(0.1)
        cc()
        wait += 1

        if wait >= 50:  # after 50 updates the loop ends. maybe try keyboard module to break instead of hard update cap
            break

    cc()
    main_menu()


def main_menu():    
    # set LED to rainbow barf RGB 
    print("Chungus Aerospace Logic Controller By Besser and Joe Mamma")
    print(version)
    print(date)


    #cpu = CPUTemperature()  #test
    #print(cpu.temperature)

    print()
    print(Fore.CYAN + "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print(Fore.LIGHTGREEN_EX + "Options:")
    # reorder this code in a way that makes sense
    print("1: Start Launch Wizard")     
    print("2: Checklist")
    print("3: Display last launch summary")
    #print("4. Push last launch folder to GitHub")
    print("5. View current sensor data")
    print("6. View weather")
    print("7. Test Fire Charges")
    print("9. CSV Flight Data Analyzer")
    print("10. Rocket Settings NOT IMPLIMENTED, DOESNT FUNCTION")
    print()
    #print("R: Rocket settings")
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

    elif "10" == which_option:
        cc()
        rocket_settings()

    elif "r" == which_option:   
        cc()
        rocket_settings()

    elif "s" == which_option:   
        cc()
        #settings_menu()
        main_menu()

    elif "d" == which_option:   # d is for development. I can just put whatever I want there to run it quickly
        cc()
        a()
        main_menu()

    elif "q" == which_option:
        sys.exit()

    else:
        cc()
        print(Fore.RED + "Invalid input")
        main_menu()


main_menu()
