version = "CALC v2.0-alpha.6"
code_revision_date = "March 2022"


import board
import adafruit_icm20x
import adafruit_bmp3xx
import adafruit_icm20x
import adafruit_sdcard
import neopixel
import storage
from rainbowio import colorwheel
from analogio import AnalogIn
from gpiozero import CPUTemperature
from gpiozero import DigitalOutputDevice

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
from datetime import datetime
#import traceback


# Setup Bits
# I2C Bus
i2c = board.I2C() 

# Low battery alarm pin

# SD mount
#SD_CS = board.D10   
#spi = board.SPI()
#cs = digitalio.DigitalInOut(SD_CS)
#sdcard = adafruit_sdcard.SDCard(spi, cs)
#vfs = storage.VfsFat(sdcard)
#storage.mount(vfs, "/sd")

# LED pins and setup
led_neo = neopixel.NeoPixel(board.NEOPIXEL, 1)     
led_neo.brightness = 1  

# BMP388
bmp = adafruit_bmp3xx.BMP3XX_I2C(i2c)
bmp.pressure_oversampling = 8
bmp.temperature_oversampling = 2

# ICM20649 IMU
icm =  adafruit_icm20x.ICM20649(i2c)

# Beeper
beeper = DigitalOutputDevice(21)

# Timestamp
now = datetime.now()
time_and_date = now.strftime("%m-%d-%Y  %H:%M")
current_time = now.strftime("%H:%M")
current_date = now.strftime("%m-%d-%Y")

# Chute ignition relay
chute_relay = DigitalOutputDevice(13)

# Motor ignition relay
motor_relay = DigitalOutputDevice(6)

# general options
debug = 0
launch_countdown = 11    # how long the countdown is in seconds - 1

# weather options
zip_code = "85054"
use_zip = 0
city_name = "phoenix"
weather_api_key = "1392d31baeec1ab9f5d2bd99d5ec04aa"

# general storage
preflight_errors = 0
locate_cycles = 0
view_sensor_count = 100

# rocket storage
fire_chute_alt = 100    # default value in m, changes based on user input
arm_chute_alt = fire_chute_alt - 2
#sea_level_pressure is below all_weather



def cc():   # shortens this long command to just cc()
    os.system("cls" if os.name == "nt" else "clear")    # clears terminal
cc()


def fetch_weather():  # this fetches weather data but doesnt display it. Used for getting the current pressure
    global current_pressure
    global current_temperature
    global current_wind_speed
    global weather_description
    global complete_url
    global x
    base_url = "http://api.openweathermap.org/data/2.5/weather?"

    if use_zip == 0:
        complete_url = base_url + "appid=" + weather_api_key + "&q=" + city_name
    else:
        complete_url = base_url + "appid=" + weather_api_key + "&q=" + zip_code

    response = requests.get(complete_url)
    x = response.json()

    if x["cod"] != "404":
        y = x["main"]
        current_temperature = y["temp"]
        current_pressure = y["pressure"]
        z = x["weather"]
        weather_description = z[0]["description"]
        w = x["wind"]
        current_wind_speed = w["speed"]
fetch_weather()
#bmp.sea_level_pressure = current_pressure
sea_level_pressure = current_pressure   
STARTING_ALTITUDE = 1000 #bmp.altitude # needs to be below the calibrated pressure so its accurate


def weather():  # this displays the weather data from all_weather()
    fetch_weather()  # updates info
    print("URL sent: " + complete_url)
    if x["cod"] != "404":
        if use_zip == 0:
            print("Check weather! Requesting cities can return the wrong info")
            print("Weather in " + city_name)
        else:
            print("Weather in " + str(zip_code))
    else:
        print("City Not Found")


    print("Temp in Kelvin = " + str(math.trunc(current_temperature)))
    print("Temp in Celsius = " + str(math.trunc(current_temperature - 273.15)))
    print("Temp in Fahrenheit = " + str(math.trunc((1.8 * current_temperature) - 459.67)))
    print("Description = " + str(weather_description))
    print("Pressure in millibars = " + str(current_pressure))
    print("Pressure in inches of Hg = " + str(round(current_pressure / 33.864, 2)))
    print("Wind Speed in m/s = " + str(round(current_wind_speed, 2)))
    print("Wind Speed in mph = " + str(round(current_wind_speed * 2.237, 2)))
    #print(x) # prints raw json data


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
        print("motor test")
        motor_relay.on()
        time.sleep(1)
        motor_relay.off()
        main_menu()

    elif test_type == "Parachute Test":
        print("chute test")
        chute_relay.on()
        time.sleep(1)
        chute_relay.off()
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
    print("Parachute will deploy at " + str(fire_chute_alt))
    print("Parachute will arm at " + str(arm_chute_alt))
    time.sleep(2.5)
    main_menu()



# -------------------------------Main flight code-------------------------------
def emergency_chute_deploy():   # Not implemented yet
    """ if the sensors dont see the velocty slowing down after closing the relay for a second
    it will run this code. It will pulse the relay in order to try to ignite the charge.
    The chute deploy just used to do this, but it would lose logging data because of the delay.

    Im not sure how to do continuity detection on the Pi. I would just use that if possible """
    # log emergency deploy
    #print error. might show up if still connected to WiFi
    for i in range (5):             # motor ignition (loops to ensure it happens)
        chute_relay.on()
        time.sleep(1)
        chute_relay.off()
        time.sleep(0.5)
    # if deploy is detected by a reduction in velocity return to the logging code
    # you can use the same code that triggers this function to do it


def flight_software():
    cc()
    global current_time
    # logging options
    log_stop_count = 400        # when to stop logging after an amount of data points are collected, backup to low altitude condition
    log_interval = 0.0          # Unlikely to be the actual number due to the polling rate of the sensors
    FILE_NAME = "launch " + time_and_date + ".csv"  
    event_comma_count = ",,,,,,," # makes sure events go in their own column on the far right 

    # logging storage
    data_cycles = 0
    logged_liftoff = 0
    chute_armed = 0 
    logged_chute_deploy = 0
    alt_1 = 0
    t_s_1 = 0
    
    # .csv creation and formatting
    with open("/sd/" + FILE_NAME, "a") as f: 
        f.write(",,,,,,\n")  # creates the right amount of columns 
        f.write(str("Date: " + current_date + ",,,,,\n"))   # The extra commas is so GitHub doesnt get cranky
        f.write("Time: " + current_time + ",,,,,\n")
        f.write("Software version: " + version + ",,,,,\n")
        f.write("Starting altitude: " + str(STARTING_ALTITUDE) + ",,,,,\n")
        f.write("Data points cutoff: " + str(log_stop_count) + ",,,,,\n")
        f.write("Pressure (mbar), Temperature (°c), Altitude (m), Accel on xyz (m/s^2), Gyro on xyz (deg/s), v_speed (m/s), Elapsed Seconds, Events\n")

    with open("/sd/" + FILE_NAME, "a") as f:  # ignite motor 
        led_neo[0] = (20, 235, 35)    # indicates the motor has been fired and is waiting for liftoff detection to run log code
        f.write(event_comma_count + "Motor lit\n")
        motor_relay.on()    # lauches the rocket 


    while True: # wait for liftoff then go to logging
        if bmp.altitude >= STARTING_ALTITUDE + 2:
            if logged_liftoff == 0:
                with open("/sd/" + FILE_NAME, "a") as f:
                    f.write("{:5.2f},{:5.2f},{:5.2f},".format(bmp.pressure, bmp.temperature, bmp.altitude,))
                    f.write("%.2f %.2f %.2f," % (icm.acceleration),)
                    f.write("%.2f %.2f %.2f," % icm.gyro,)
                    f.write(",Liftoff detected\n")
            
                    led_neo[0] = (255, 255, 255)    # indicates liftoff has been detected and it passed to the logging code.
                    # this is for dev purposes, you wont see it because the rocket will be in the air already

                motor_relay.off()
                logged_liftoff += 1
                break

    #                          ------------------------ Main data logging code ------------------------
    initial_time = time.monotonic() # needs to be here and not in the time set ups bits code for reasons
    print("Begin Logging")
    while True:   
        t_s_0 = time_stamp
        vert_speed = (bmp.altitude - alt_1) / (t_s_0 - t_s_1)

        with open("/sd/" + FILE_NAME, "a") as f:    
            current_time = time.monotonic()
            time_stamp = current_time - initial_time

            f.write("{:5.2f},{:5.2f},{:5.2f},{:5.2f}".format(bmp.pressure, bmp.temperature, bmp.altitude, vert_speed,))
            f.write("%.2f %.2f %.2f," % icm.acceleration,)
            f.write("%.2f %.2f %.2f," % icm.gyro,)
            f.write("{:5.2f}".format(time_stamp) + ",\n") # logs elapsed time 

            # This is for when its connected wirelessly through a computer. This way we
            # can get live telem data (for as long as the rocket is in wireless range)
            print("Alt: " + str(bmp.altitude), end = ",   ")   
            print("Time:{:5.2f}".format(time_stamp))
            #print(vertical_speed)
            
            
            # Arm parachute
            if bmp.altitude >= STARTING_ALTITUDE + 50:  # I know that and statements are a thing, but this is easier to read imo
                if chute_armed == 0: # this is so the event isnt logged repeatedly
                    f.write(event_comma_count + "Armed parachute. Current alt: " + str(bmp.altitude) +  "m . Current time: " + str(time_stamp) + "m\n")
                    chute_armed += 1
                    print("Armed parachute")

            # Deploy parachute - close relay
            if chute_armed == 1:
                if bmp.altitude <= STARTING_ALTITUDE + 48:  # once the rocket sinks below 50 meters it fires the chute
                    DATA_CYCLES_CHUTE = data_cycles 
                    chute_relay.on()
                    print("Parachute relay on")

                    if logged_chute_deploy == 0:
                        f.write(event_comma_count + "Deployed parachute. Current alt: " + str(bmp.altitude) + "m. Current time: " + str(time_stamp) + "\n")
                        logged_chute_deploy +=1

                # Close relay
                if logged_chute_deploy == 1:    # this might not work. 
                    if DATA_CYCLES_CHUTE >= 10: # waits 10 data cyles before opening the relay
                        chute_relay.off()   # this was True before and idk why. Does it actually need to be True?
                        f.write(event_comma_count + "Parachute relay off. Current time: " + str(time_stamp) + "\n")
                        print("Parachute relay off")


        # stops the logging of data
        if data_cycles > 50:    
            if bmp.altitude <= STARTING_ALTITUDE + 5:   # + 5 is incase it lands above the starting elevation or the sensor drifts
                with open("/sd/" + FILE_NAME, "a") as f:
                    f.write(event_comma_count + "Stopped logging; low altitude met. (" + str(bmp.altitude) + "m)\n")
                    break

        if data_cycles >= log_stop_count:   # backup to the code above
            with open("/sd/" + FILE_NAME, "a") as f:
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
    global locate_cycles
    while True:
        led_neo[0] = (255, 255, 255)
        beeper.on()
        time.sleep(0.2)
        beeper.off()
        led_neo[0] = (0, 0, 0)
        time.sleep(2)
        locate_cycles += 1


def preflight_checks():
    global preflight_errors
    print("Acceleration: %.2f %.2f %.2f," % icm.acceleration)
    print("Gyroscope: %.2f %.2f %.2f," % icm.gyro)
    print("Barometer altitude: " + bmp.altitude)
    print("Barometer Pressure: " + bmp.pressure)
    print("Weather API Pressure: " + str(current_pressure))
    print("Starting Altitude: " + str(STARTING_ALTITUDE))

    print(now.strftime("Time & date:  %m-%d-%Y %H:%M"))
    print()
    value_check = input("Are these values correct? y/n ")
    if value_check == "y":
        pass # autism
    else:
        preflight_errors =+ 1
    
    # ----------------------Error checking----------------------
    #if battery voltage is low:
    #print(Fore.YELLOW + "Low battery!")
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
            led_neo[0] = (255, 255, 255)
            beeper.on()
            time.sleep(0.5)
            led_neo[0] = (0, 0, 0)
            beeper.off()
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
    global view_sensor_count
    while view_sensor_count <= 1:
        print("Low battery warning: ")
        print("Time: " + time_and_date)
        print("Altitude: {:5.2f}" + bmp.altitude + "m")
        print("Weather Sea Level Pressure: ")
        print("Current Pressure: {:5.2f}" + bmp.pressure + "mbar")
        print("Temperature: " + bmp.temperature + "°c")
        print("Acceration: %.2f %.2f %.2f," % icm.acceleration)
        print("Gyroscope: %.2f %.2f %.2f," % icm.gyro)
        time.sleep(0.1)
        view_sensor_count =- 1
        cc()
    main_menu()


def main_menu():    
    # set LED to rainbow barf RGB 
    print("Chungus Aerospace Logic Controller By Besser and Joe Mamma")
    print(version)
    print(code_revision_date)

    cpu = CPUTemperature()  #test
    print(cpu.temperature)

    print()
    print(Fore.CYAN + "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print(Fore.LIGHTGREEN_EX + "Options:")
    # reorder this text in an order that makes sense
    print("1: Start Launch Wizard")     
    print("2: Checklist")
    print("3: Display last launch summary")
    print("4. Push last launch folder to GitHub")
    print("5. View current sensor data")
    print("6. View weather")
    print("7. Test Fire Charges")
    print("9. CSV Flight Data Analyzer")
    #print("10. Rocket Settings")
    print()
    print("R: Rocket settings")
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
        main_menu()

    elif "q" == which_option:
        sys.exit()

    else:
        cc()
        print(Fore.RED + "Invalid input")
        main_menu()
main_menu()

"""
while True:     # indicates that the data recording is done
    i = (i + 1) % 256  # run from 0 to 255
    led_neo.fill(colorwheel(i)) # Unicorn barf
    time.sleep(0.01)
    """



"""try:
    main()
except KeyboardInterrupt:
    cc()
    print(Fore.RED + "Keyboard Interrupt")
    main_menu()"""