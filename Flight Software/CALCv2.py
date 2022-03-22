version = "CALC v2.0-beta.3"
code_revision_date = "March 2022"


from random import randint
import board
import adafruit_icm20x
import adafruit_bmp3xx
import neopixel
#import storage
from rainbowio import colorwheel
from gpiozero import CPUTemperature
from gpiozero import DigitalOutputDevice
from gpiozero import InputDevice

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
import random


# Setup Bits
# I2C Bus
i2c = board.I2C() 

# LED pins and setup
led_neo = neopixel.NeoPixel(board.D12, 1)     
led_neo.brightness = 1

# BMP388
bmp = adafruit_bmp3xx.BMP3XX_I2C(i2c)
bmp.pressure_oversampling = 4    #NOTE This was 8 by default
bmp.temperature_oversampling = 2

# ICM20649
icm =  adafruit_icm20x.ICM20649(i2c)

# Beeper
beeper = DigitalOutputDevice(21)

# Low battery alarm
low_batt = InputDevice(4, pull_up=True)  # pull_up inverts the reading. it was backwards before

# Timestamp
now = datetime.now()
time_and_date = now.strftime("%m-%d-%Y  %H:%M")
TIMEDATE = time_and_date
global_current_time = now.strftime("%H:%M")
global_current_date = now.strftime("%m-%d-%Y")

# Relays
chute_relay = DigitalOutputDevice(19) 
motor_relay = DigitalOutputDevice(26)
# note that the LEDs on the sheild are to the left of the relays

# general options
#debug = 0
launch_countdown = 3 # also acts as storage

# weather options
zip_code = "85054"
use_zip = 0
city_name = "phoenix"
weather_api_key = "1392d31baeec1ab9f5d2bd99d5ec04aa"

# general storage
preflight_errors = 0
view_sensor_count = 50
LAUNCH_COUNTDOWN_INIT = launch_countdown # resets 
wrote_to_log_list = 0 # this is so a log write isnt attemped when a keyboard interrupt happens
ran_launch = 0 # same thing as above

"""# rocket storage
fire_chute_alt = 100    # default value in m, changes based on user input
arm_chute_alt = fire_chute_alt - 2"""

#sea_level_pressure is below all_weather

# this is for dev purposes, it shows the file has been reloaded
RELOAD_RNG = randint(0, 1000)

def cc():   # shortens this long command to just cc()
    os.system("cls" if os.name == "nt" else "clear")    # clears terminal
    #for i in range(20): #above code doesnt work, this is a crappy fix for now
        #print()
cc()


def main():
    try:
    
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

        bmp.sea_level_pressure = current_pressure   # calibrates barometer
        sea_level_pressure = current_pressure   
        STARTING_ALTITUDE = (round(bmp.altitude, 2)) # needs to be below the calibrated pressure so its accurate


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
            print("Description = " + weather_description)
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
                #beeper.on()
                time.sleep(1)
                motor_relay.off()
                beeper.off()
                main_menu()

            elif test_type == "Parachute Test":
                print("chute test")
                chute_relay.on()
                #beeper.on()
                time.sleep(1)
                chute_relay.off()
                beeper.off()
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
            print("Current altitude: {:5.2f}".format(bmp.altitude) + "m")
            time.sleep(2.5)
            main_menu()



        # -------------------------------Main flight code-------------------------------

        def flight_software():
            cc()
            global ran_launch
            ran_launch += 1
            global current_time
            global file_location
            global FILE_NAME
            global log_list
            global wrote_to_log_list

            # logging options
            log_stop_count = 300        # when to stop logging after an amount of data points are collected, backup to low altitude condition
            FILE_NAME = "launch " + TIMEDATE + ".csv" 
            file_location = "/home/pi/Desktop/" 
            event_comma_count = ",,," # makes sure events go in their own column on the far right 

            # logging storage
            log_list = []
            data_cycles = 0
            logged_liftoff = 0
            chute_armed = 0 
            chute_deployed = 0
            logged_chute_deploy = 0
  
            # .csv creation and formatting
            with open(file_location + FILE_NAME, "a") as f: 
                f.write(",,,,\n")  # creates the right amount of columns 
                f.write("Software version: " + version + ",,,,,\n")
                f.write("Date: " + global_current_date + ",,,,,\n")   # The extra commas is so GitHub doesnt get cranky
                f.write("Time: " + global_current_time + ",,,,,\n")
                f.write("Temperature: {:5.2f}".format(bmp.temperature) + ",,,,,\n")
                #f.write("Temperature: " + str(bmp.temperature) + ",,,,,\n")
                f.write("Starting altitude: " + str(STARTING_ALTITUDE) + ",,,,,\n")
                f.write("Current Barometer pressure: {:5.2f}".format(bmp.pressure) + ",,,,,\n")
                f.write("Current weather API pressure: " + str(current_pressure) + ",,,,,\n")
                f.write("Data points cutoff: " + str(log_stop_count) + ",,,,,\n")
                f.write(",,,,,,\n")
                f.write("Altitude (m), Accel on xyz (m/s^2), Gyro on xyz (deg/s), Elapsed Seconds, Events\n")
                led_neo[0] = (20, 235, 35)    # indicates the motor has been fired and is waiting for liftoff detection to run log code

            print("Motor Lit...")
            motor_relay.on()    # lauches the rocket 

            while True: # wait for liftoff then go to logging
                if bmp.altitude >= STARTING_ALTITUDE + 0:
                    if logged_liftoff == 0:
                        with open(file_location + FILE_NAME, "a") as f:
                            f.write("{:5.2f},".format(bmp.altitude,))
                            f.write("%.2f %.2f %.2f," % icm.acceleration,)
                            f.write("%.2f %.2f %.2f," % icm.gyro,)
                            f.write(",Liftoff detected")
                            print("Liftoff detected")
                    
                            led_neo[0] = (255, 255, 255)    # indicates liftoff has been detected and it passed to the logging code.
                            # this is for dev purposes, you wont see it because the rocket will be in the air already

                        motor_relay.off()
                        logged_liftoff += 1
                        break

            #                          ------------------------ Main data logging code ------------------------
            initial_time = time.monotonic() # needs to be here and not in the time set ups bits code for reasons
            while True: 
                current_time = time.monotonic()
                time_stamp = current_time - initial_time

                #with open(file_location + FILE_NAME, "a") as f: 
                # if adding back temp and pressure, add ,, to event_comma_count and to the column creation
                # also add pressure and temp to the column naming
                log_list.extend([
                "\n"
                "{:5.2f}".format(bmp.altitude),
                "%.2f %.2f %.2f" % (icm.acceleration),
                "%.2f %.2f %.2f" % (icm.gyro),
                "{:5.2f}".format(time_stamp),
                ])
                # This is for when its connected wirelessly through a computer. This way we
                # can get live telem data (for as long as the rocket is in wireless range)
                print("Alt: {:5.2f}".format(bmp.altitude) + "m", end = "   ")   
                print("Time: {:5.2f}".format(time_stamp) + "s")
                

                # NOTE this parachute code drastically slows down the code. if the Pi isnt controlling the chute comment out this code
                # Arm parachute
                if chute_armed == 0: # this is so the event isnt logged repeatedly
                    if bmp.altitude >= STARTING_ALTITUDE + 0: #50  # I know that and statements are a thing, but this is easier to read imo
                        log_list.extend(["Armed parachute. Current alt: {:5.2f}".format(bmp.altitude) + "m . Time: {:5.2f}".format(time_stamp) + ","])
                        print(Fore.LIGHTMAGENTA_EX + "Armed parachute")
                        chute_armed += 1

                    # the arm code could just be the deploy code. if bmp.altitude >= STARTING_ALTITUDE + 50: deploy
                    # keep for now for reasons
                    #f.write(event_comma_count + "Deployed parachute. Current alt: " + str(bmp.altitude) + "m. Time: {:5.2f}".format(time_stamp) + "\n")

                    # Deploy parachute
                if chute_armed == 1: #if bmp.altitude >= STARTING_ALTITUDE + 50:
                    if chute_deployed == 0: # prevents the event from being ran repeatedly 
                        if bmp.altitude <= STARTING_ALTITUDE + 0: #47 # once the rocket sinks below this it fires the chute
                            DATA_CYCLES_CHUTE = data_cycles 
                            chute_relay.on()
                            log_list.extend(["Deployed parachute,"])
                            print(Fore.LIGHTMAGENTA_EX + "Deployed parachute")
                            chute_deployed +=1

                    # Open chute relay
                    if chute_deployed == 1:   
                        if logged_chute_deploy == 0:  # prevents the event from being ran repeatedly
                            if data_cycles > DATA_CYCLES_CHUTE + 20:  # waits 20 data cyles before opening the relay. pure autism
                                chute_relay.off()
                                log_list.extend(["Parachute relay off,"])
                                print(Fore.LIGHTMAGENTA_EX + "Parachute relay off")
                                logged_chute_deploy += 1 


                # stops the logging of data
                if data_cycles > 100:    
                    if bmp.altitude <= STARTING_ALTITUDE + 4:   # + 4 is incase it lands above the starting elevation or the sensor drifts
                        with open(file_location + FILE_NAME, "a") as f:
                            #f.write(event_comma_count + "Stopped logging low alt met ({:5.2f}".format(bmp.altitude) + "m)\n")
                            print(Fore.LIGHTCYAN_EX + "Stopped logging low alt met ({:5.2f}".format(bmp.altitude) + "m)")
                            break

                """ if data_cycles >= log_stop_count:   # backup to the code above
                    with open(file_location + FILE_NAME, "a") as f:
                        f.write(event_comma_count + "Stopped logging; writes to file met. (" + str(data_cycles) + " writes) ")
                        f.write(event_comma_count + "This means altitude code did not execute.\n")
                        break"""
                
                
                data_cycles += 1 # this seems simple but its crucial to some things so dont mess with it 
            with open(file_location + FILE_NAME, "a") as f: 
                f.write(','.join(log_list))
                wrote_to_log_list += 1

                
            #                          ------------------------ End of main data logging code ------------------------
            post_flight()


        def post_flight():
            print(Fore.LIGHTGREEN_EX + "Done")
            main_menu()
            while True:
                r = random.randint(0,255)
                g = random.randint(0,255)
                b = random.randint(0,255)
                led_neo[0] = (r, g, b)  
                #beeper.on()
                time.sleep(0.3)
                beeper.off()
                led_neo[0] = (0, 0, 0)
                time.sleep(2)


        def preflight_checks():
            global preflight_errors
            print(Fore.LIGHTMAGENTA_EX + now.strftime("Time & date: %H:%M %m-%d-%Y"))
            if low_batt.is_active == True: print(Fore.RED + "Low battery warning: " + str(low_batt.is_active))
            else: print(Fore.LIGHTMAGENTA_EX + "Low battery warning: " + str(low_batt.is_active)) 
            print(Fore.LIGHTMAGENTA_EX + "Barometer altitude: {:5.2f}".format(bmp.altitude) + "m")
            print(Fore.LIGHTMAGENTA_EX + "Starting Altitude: " + str(STARTING_ALTITUDE) + "m")
            print(Fore.LIGHTMAGENTA_EX + "Barometer pressure: {:5.2f}".format(bmp.pressure) + "mbar")
            print(Fore.LIGHTMAGENTA_EX + "Weather API pressure = " + str(current_pressure) + "mbar")
            print()
            print("Temperature: {:5.2f}".format(bmp.temperature) + "°c")
            print("Acceration: %.2f %.2f %.2f" % icm.acceleration + " m/s²")
            print("Gyroscope: %.2f %.2f %.2f" % icm.gyro + " deg/s")
            print("Weather API URL sent: " + complete_url)
            print()

            value_check = input("Are these values correct? y/n ")
            if value_check == "y":
                pass # autism
            else:
                preflight_errors =+ 1
            
            # ----------------------Error checking----------------------
            if low_batt.is_active == True:
                print(Fore.YELLOW + "Low battery warning: " + str(low_batt.is_active))
                preflight_errors += 1

            #if STARTING_ALTITUDE varies from bmp.alt by 2m, throw error
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
                    #beeper.on()
                    time.sleep(0.5)
                    led_neo[0] = (0, 0, 0)
                    beeper.off()
                    time.sleep(0.5)

                    #check if the connection between my pc and the Pi is active.
                    #that way if the connection stops it automatically stops the countdown
                    #this is incase we need to cancel the countdown
                launch_countdown = LAUNCH_COUNTDOWN_INIT  # resets count
 
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
            while view_sensor_count > 1:
                cc()
                print(now.strftime("Time & date:  %H:%M %m-%d-%Y"))
                print("Low battery warning: " + str(low_batt.is_active))
                print("Barometer altitude: {:5.2f}".format(bmp.altitude) + "m")
                print("Barometer pressure: {:5.2f}".format(bmp.pressure) + "mbar")
                print("Weather API pressure = " + str(current_pressure))
                print("Temperature: {:5.2f}".format(bmp.temperature) + "°c")
                print("Acceration: %.2f %.2f %.2f" % icm.acceleration + " m/s²")
                print("Gyroscope: %.2f %.2f %.2f" % icm.gyro + " deg/s")
                time.sleep(0.1)
                view_sensor_count -= 1
            main_menu()


        def main_menu():  
            #beeper.on()
            time.sleep(0.1)
            beeper.off()  
            led_neo[0] = (0, 255, 0)
            # set LED to rainbow barf RGB 
            print("Chungus Aerospace Logic Controller By Besser and Joe Mamma")
            print(version)
            print(code_revision_date)
            print("Time: " + global_current_time)
            print("Confirm reload: " + str(RELOAD_RNG)) # for dev, makes sure the file is reloaded
            #print(ran_launch)

            #cpu = CPUTemperature()  #test
            #print("Pi CPU Temp: " + str(cpu.temperature))

            print()
            print(Fore.CYAN + "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            print(Fore.LIGHTGREEN_EX + "Options:")
            # reorder this text in an order that makes sense
            print("1: Start Launch Wizard")     
            #print("2: Checklist")
            #print("3: Display last launch summary")
            #print("4. Push last launch folder to GitHub")
            print("5. View current sensor data")
            print("6. View weather")
            print("7. Test Fire Charges")
            #print("9. CSV Flight Data Analyzer")
            #print("10. Rocket Settings")
            print()
            print("R: Rocket settings")
            #print("S: Software settings")   # disable any wifi code, 
            
            print("L: Reload software")
            print("X: Shutdown")
            print("Q: Quit")

            which_option = input("What would you like to do? ")
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
                main_menu()
            elif "5" == which_option:
                cc()
                view_sensor_count == 50
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
            elif "l" == which_option:
                print(Fore.GREEN + "Rebooting...")
                time.sleep(0.1)
                os.execl(sys.executable, sys.executable, *sys.argv)
            elif "q" == which_option:
                cc()
                beeper.off()
                motor_relay.off()
                chute_relay.off()
                led_neo[0] = (0, 0, 0)
                sys.exit()
            elif "x" == which_option:
                cc()
                beeper.off()
                motor_relay.off()
                chute_relay.off()
                led_neo[0] = (0, 0, 0)
                shut = input("Are you sure you want to shutdown? y/n")
                if shut == "y":
                    os.system("systemctl poweroff") 
                else:
                    cc()
                    main_menu()
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
    except KeyboardInterrupt:
        if ran_launch == 1:
            if wrote_to_log_list == 0:
                with open(file_location + FILE_NAME, "a") as f: 
                    f.write(','.join(log_list))
        print()
        print()
        beeper.off()
        motor_relay.off()
        chute_relay.off()
        print(Fore.YELLOW + "Keyboard Interrupt")
        main()                
main()
