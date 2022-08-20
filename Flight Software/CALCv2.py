version = "CALC v2.0-beta.6"
code_revision_date = "May 2022"

from random import randint
import board
import adafruit_icm20x
import adafruit_bmp3xx
import neopixel
import numpy as np
from rainbowio import colorwheel
from gpiozero import CPUTemperature
from gpiozero import DigitalOutputDevice
from gpiozero import InputDevice
import time
from picamera import PiCamera
import threading
import sys
import os
from colorama import init
init()
from colorama import Fore
init(autoreset=True)
import requests
from requests.structures import CaseInsensitiveDict
import math 
from datetime import datetime
import random
import traceback


# general options
enable_camera = 0
led_neo_brightness = 1
launch_countdown = 5 # also acts as storage
mute_beeper = 1

# weather options
zip_code = "85050"
use_zip = 0
city_name = "phoenix"
weather_api_key = "1392d31baeec1ab9f5d2bd99d5ec04aa"

# general storage
preflight_errors = 0
view_sensor_count = 50
LAUNCH_COUNTDOWN_INIT = launch_countdown # resets 
wrote_to_log_list = 0 # this is so a log write isnt attempted when a keyboard interrupt happens
ran_launch = 0 # same thing as above
kill_rgb = 0


# Setup Bits
# I2C Bus
i2c = board.I2C() 

# LED pins and setup
led_neo = neopixel.NeoPixel(board.D12, 8)     # NeoPixel on D12
led_neo.brightness = led_neo_brightness

# BMP390
bmp = adafruit_bmp3xx.BMP3XX_I2C(i2c)
bmp.pressure_oversampling = 2   #NOTE This was 8 by default
bmp._wait_time = 0
bmp.temperature_oversampling = 2

# ICM20649
icm = adafruit_icm20x.ICM20649(i2c)
adafruit_icm20x.ICM20649.accelerometer_range = 16
adafruit_icm20x.ICM20649.gyro_range = 500

adafruit_icm20x.gyro_data_rate = 5000
adafruit_icm20x.accelerometer_data_rate = 5000

# Beeper
beeper = DigitalOutputDevice(21)

# Low battery alarm
low_batt = InputDevice(4, pull_up=True)  # pull_up inverts the reading. it was backwards before

# Timestamp
now = datetime.now()
time_and_date = now.strftime("%m-%d-%Y  %H:%M")
TIMEDATE = time_and_date    # this is so the file name doesnt change in the middle of a flight
global_current_time = now.strftime("%H:%M")
global_current_date = now.strftime("%m-%d-%Y")

# Relays
chute_relay = DigitalOutputDevice(19) 
motor_relay = DigitalOutputDevice(26)
# note that the LEDs on the shield are to the left of the relays

# Camera
if enable_camera == 1:
    #camera.exposure_mode = "antishake"
    camera = PiCamera()
    camera.resolution = (1280, 720)
    camera.framerate = 60
    camera.awb_mode = "auto"

"""# rocket storage
arm_chute_alt = fire_chute_alt - 2
fire_chute_alt = 50    # default value in m, changes based on user input
"""


# this is for dev purposes, it shows the file has been reloaded
RELOAD_RNG = Fore.LIGHTMAGENTA_EX + str(randint(0, 1000))


def cc():   # shortens this long command to just cc()
    os.system("cls" if os.name == "nt" else "clear")    # clears terminal
cc()


def kr():  # kill RGB rainbow loop
    global kill_rgb
    kill_rgb = 1
kr()  # incase it was somehow still on before starting the program


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

        bmp.sea_level_pressure = current_pressure    # calibrates barometer 
        STARTING_ALTITUDE = (round(bmp.altitude, 2)) # needs to be below the calibrated pressure so its accurate


        def beeper(state):
            global beeper
            if mute_beeper == 0:
                if state == 1:
                    beeper.on()
                elif state == 0:
                    beeper.off()


        def weather():      # this displays the weather data from all_weather()
            fetch_weather() # updates info
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
                    print(" = Processed request successfully")
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
                beeper(1)
                time.sleep(1)
                motor_relay.off()
                beeper(0)
                main_menu()

            elif test_type == "Parachute Test":
                print("chute test")
                chute_relay.on()
                beeper(1)
                time.sleep(1)
                chute_relay.off()
                beeper(0)
                main_menu()

            else:
                cc()
                print(Fore.RED + "Test error, test not found: " + test_type)
                main_menu()


        def rocket_settings():
            global fire_chute_alt
            global arm_chute_alt    
            cc()  
            print(Fore.LIGHTGREEN_EX + "Rocket Settings")
            print("NOT IMPLEMENTED, CHANGES NOTHING")
            print(Fore.CYAN + "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            print()

            print("1: Change chute deploy altitude")
            print("2: Change launch countdown")

            ask_chute_alt = input("What is the altitude the parachute should deploy at? (m) ")
            fire_chute_alt = STARTING_ALTITUDE + int(ask_chute_alt)
            arm_chute_alt = fire_chute_alt - 2  

            print("Parachute will deploy at " + str(fire_chute_alt))
            print("Parachute will arm at " + str(arm_chute_alt))
            print("Current altitude: {:5.2f}".format(bmp.altitude) + "m")
            input("Press enter to return to the main menu ")
            #print("Change countdown time")
            main_menu()


        # ------------------------------- Main flight code -------------------------------

        def camera_func():
            print(Fore.LIGHTGREEN_EX + "Starting camera")
            camera.start_preview()
            time.sleep(3)
            #countdown_cam_check = 1 # camera is ready to record
            # this probably adds a race condition when threaded rip
            camera.start_recording("/home/pi/Desktop/video.h264")
            print(Fore.LIGHTGREEN_EX + "Camera recording")
            time.sleep(20)
            #camera.wait_recording(5) 
            # https://picamera.readthedocs.io/en/release-1.13/recipes1.html#:~:text=start_recording(%27my_video.h264%27)-,camera.wait_recording(60),-camera.stop_recording()
            camera.stop_recording()
            print(Fore.LIGHTGREEN_EX + "Stopped camera recording")
            camera.stop_preview()
            pass


        def flight_software():
            # https://en.wikipedia.org/wiki/Code_refactoring
            # https://en.wikipedia.org/wiki/Spaghetti_code
#NOTE            #cc()
            global ran_launch
            ran_launch = 1
            global current_time
            global file_location
            global FILE_NAME
            global log_list
            global wrote_to_log_list


            # logging options
            FILE_NAME = "launch " + TIMEDATE + ".csv" 
            file_location = "/home/pi/Desktop/"  

            # logging storage
            log_list = []
            data_cycles = 0
            logged_liftoff = 0
            motor_start_time = 0
            chute_armed = 0 
            chute_deployed = 0
            logged_chute_deploy = 0
        

            # .csv creation and formatting
            with open(file_location + FILE_NAME, "a") as f: 
                f.write("Altitude (m), Accel on xyz (m/s^2), Gyro on xyz (deg/s), Time (s), Events\n") # creates right amount of columns
                f.write("Software version: " + version + ",,,,,\n")
                f.write("Date: " + global_current_date + ",,,,,\n")   # The extra commas is so GitHub doesnt get cranky
                f.write("Time: " + global_current_time + ",,,,,\n")
                f.write("Temperature: {:5.2f}".format(bmp.temperature) + ",,,,,\n")
                f.write("Starting altitude: " + str(STARTING_ALTITUDE) + ",,,,,\n")
                f.write("Current Barometer pressure: {:5.2f}".format(bmp.pressure) + ",,,,,\n")
                f.write("Current accelerations: %.2f %.2f %.2f" % (icm.acceleration) + ",,,,,\n")
                f.write("Current weather API pressure: " + str(current_pressure) + ",,,,,\n")
                f.write("Pressure oversampling: " + str(bmp.pressure_oversampling) + ",,,,,\n")
                f.write(",,,,,,\n")
                f.write("Altitude (m), Accel on xyz (m/s^2), Gyro on xyz (deg/s), Time (s), Events\n")
                

            #t_parachute = threading.Thread(target=parachute)
            #t_parachute.start()


            led_neo.fill((20, 235, 35)) # indicates the motor has been fired and is waiting for liftoff detection to run log code 
            print(Fore.LIGHTGREEN_EX + "Motor Lit")
            motor_relay.on()    # launches the rocket 


            while True: # wait for liftoff then go to logging
                #motor_start_time += 1
                if logged_liftoff == 0: 
#NOTE                    
                    # disable this code if launching manually and not using the onboard relay
                    #if motor_start_time > 200: # time to wait until cancel (10ms. 100 = 1s)
                        #print(Fore.RED + "Motor not starting! Canceled launch")
                        #motor_relay.off()
                        #chute_relay.off()
                        #kr()
                        #led_neo.fill((255, 0, 0))
                        #input("Press enter to continue ")
                        #cc()
                        #main_menu()
                        #break

#NOTE
                    if bmp.altitude >= STARTING_ALTITUDE + 2:
                        log_list.extend(["Liftoff detected,"])
                        print(Fore.LIGHTGREEN_EX + "Liftoff detected")
                        print(Fore.LIGHTGREEN_EX + "Starting altitude: " + str(STARTING_ALTITUDE))
                        led_neo.fill((255, 255, 255))    # indicates liftoff has been detected and it passed to the logging code. 
                        motor_relay.off()
                        logged_liftoff += 1
                        break


############################### Test code ###############################
            """            
            this allows us to see the delay between ignition and liftoff detection
            
            initial_time_d = time.monotonic()
            motor_lit_d = 0
            while True: # wait for liftoff then go to logging
                current_time_d = time.monotonic()
                time_stamp = current_time_d - initial_time_d

                if motor_lit_d == 0:
                    led_neo.fill((20, 235, 35)) # indicates the motor has been fired and is waiting for liftoff detection to run log code 
                    print(Fore.LIGHTGREEN_EX + "Motor Lit")
                    motor_relay.on()  
                    log_list.extend([",,,Motor lit,"])
                    log_list.extend([str(time_stamp) + ","])
                    motor_lit_d = 1


                if bmp.altitude >= STARTING_ALTITUDE + 3:
                    log_list.extend([",,,Liftoff detected,"])
                    log_list.extend([str(time_stamp) + ","])
                    print(Fore.LIGHTGREEN_EX + "Liftoff detected")
                    print(Fore.LIGHTGREEN_EX + "Starting altitude: " + str(STARTING_ALTITUDE))
                    led_neo.fill((255, 255, 255))    # indicates liftoff has been detected and it passed to the logging code.
                    motor_relay.off()
                    logged_liftoff += 1
                    break
                """         
###############################


            #                          ------------------------ Main data logging code ------------------------
            initial_time = time.monotonic() # needs to be here and not in the time set ups bits code for reasons
            while True: 
                bmp_alt = bmp.altitude
                #bmp_press = bmp.pressure
                icm_accel = icm.acceleration
                current_time = time.monotonic()
                time_stamp = current_time - initial_time

                log_list.extend([
                "\n"
                #"{:5.2f}".format(bmp_alt),
                #"%.2f %.2f %.2f" % (icm.gyro),
                #"{:5.2f}".format(bmp.temperature),
                "%.2f %.2f %.2f" % (icm_accel),
                #"{:5.2f}".format(bmp_press),
                "{:5.2f}".format(time_stamp),
                ])

                print("Alt: {:5.2f}".format(bmp_alt) + "m", end = "   ")   
                print("Time: {:5.2f}".format(time_stamp) + "s", end = "   ")
                print("Data cycles: " + str(data_cycles))
                
#NOTE
                # Arm parachute
                if chute_armed == 0: # this is so the event isnt logged repeatedly
                    if bmp_alt >= STARTING_ALTITUDE + 40:  # 50 - arm altitude
                        log_list.extend(["Armed parachute,"])
                        print(Fore.LIGHTMAGENTA_EX + "Armed parachute")
                        chute_armed += 1
#NOTE
                # Deploy parachute
                if chute_armed == 1: 
                    if chute_deployed == 0: # prevents the event from being ran repeatedly 
                        if bmp_alt <= STARTING_ALTITUDE + 37:  #47 - deploy altitude
                            DATA_CYCLES_CHUTE = data_cycles 
                            chute_relay.on()
                            log_list.extend(["Deployed parachute,"])
                            print(Fore.LIGHTMAGENTA_EX + "Deployed parachute")
                            chute_deployed +=1

                    # Open chute relay
                    if chute_deployed == 1:   
                        if logged_chute_deploy == 0:  # prevents the event from being ran repeatedly
                            if data_cycles > DATA_CYCLES_CHUTE + 80:  # waits about a second before opening the relay. pure autism
                                chute_relay.off()
                                log_list.extend(["Parachute relay off,"])
                                print(Fore.LIGHTMAGENTA_EX + "Parachute relay off")
                                logged_chute_deploy += 1 
                    

#NOTE           # stops the logging of data
                if data_cycles > 300:  # ensures that the logging is not stopped on the pad  
                    if bmp_alt <= STARTING_ALTITUDE + 20:   # + 4 is incase it lands above the starting elevation or the sensor drifts
                        log_list.extend(["Stopped logging low alt met,"])
                        print(Fore.LIGHTCYAN_EX + "Stopped logging low alt met {:5.2f}".format(bmp.altitude) + "m")
                        print(Fore.LIGHTCYAN_EX + "Starting altitude: " + str(STARTING_ALTITUDE) + "m")
                        print(Fore.LIGHTGREEN_EX + "RESTART SOFTWARE TO LOG AGAIN")
                        break

                    if data_cycles >= 700: # Backup to the code above
                        log_list.extend(["Data cycles > 1000 stopping logging,"])
                        log_list.extend(["This means altitude code did not execute. Fix this,"])
                        print(Fore.LIGHTGREEN_EX + "Data cycles > 700 stopping logging. This means altitude code did not execute.")
                        print(Fore.LIGHTGREEN_EX + "INVESTIGATE ISSUE BEFORE RESTARTING SOFTWARE")
                        break

    
                data_cycles += 1 
            with open(file_location + FILE_NAME, "a") as f: 
                f.write(','.join(log_list))
                wrote_to_log_list += 1

        

        
        
        






            #                          ------------------------ End of main data logging code ------------------------
            post_flight()


        def post_flight():
            global kill_rgb
            kill_rgb = 1
            #stop camera
            while True: 
                r = random.randint(50,255)
                g = random.randint(50,255)
                b = random.randint(50,255)
                led_neo.fill((r, g, b))
                beeper(1)
                time.sleep(0.3)
                beeper(0)
                led_neo.fill((0, 0, 0))
                time.sleep(1.5)

        
        def axis(list_of_tuples, axis):
            specific_axis_list = []
            for i in range(len(list_of_tuples)):
                specific_axis_list.append(list_of_tuples[i][axis])
            return specific_axis_list


        def calibrate_sensors():
            kr()
            led_neo.fill((0, 0, 255))
            print("Calibrating Accelerometer...")
            accel_calibration = []
            for i in range(20):
                accel_calibration.append(icm.acceleration)
                time.sleep(0.05)
        
            # a_x stands for acceleration on the x axis
            a_x_axis_mean = np.mean(axis(accel_calibration, 0))  
            print(a_x_axis_mean)
            a_y_axis_mean = np.mean(axis(accel_calibration, 1))  
            print(a_y_axis_mean)
            a_z_axis_mean = np.mean(axis(accel_calibration, 2))  
            print(a_z_axis_mean)


        def preflight_checks():
            global preflight_errors
            print(Fore.LIGHTMAGENTA_EX + now.strftime("Time & date: %H:%M %m-%d-%Y"))
            print(Fore.LIGHTBLUE_EX + "Low battery warn: " + str(low_batt.is_active))

            print("fix parachute code")
            
            print(Fore.LIGHTGREEN_EX + "Countdown time: " + str(launch_countdown))
            print(Fore.LIGHTWHITE_EX + "Weather location: " + city_name)
            print(Fore.LIGHTCYAN_EX + "Main barometer altitude: {:5.2f}".format(bmp.altitude) + "m")
            #print(Fore.LIGHTCYAN_EX + "Aux barometer altitude: {:5.2f}".format(bmp_chute.altitude) + "m")
            #print(Fore.LIGHTMAGENTA_EX + "Fire chute altitude: " + fire_chute_alt + "m")
            print(Fore.LIGHTCYAN_EX + "Starting Altitude: " + str(STARTING_ALTITUDE) + "m")
            print(Fore.LIGHTMAGENTA_EX + "Main barometer pressure: {:5.2f}".format(bmp.pressure) + "mbar")
            print(Fore.LIGHTGREEN_EX + "Weather API pressure = " + str(current_pressure) + "mbar")
            print(Fore.LIGHTGREEN_EX + "Barometer calibration pressure = " + str(bmp.sea_level_pressure) + "mbar")
            print() # below is less important stuff that doesnt really need to be confirmed
            print("Temperature: {:5.2f}".format(bmp.temperature) + "°c")
            print("Acceration: %.2f %.2f %.2f" % icm.acceleration + " m/s²")
            print("Gyroscope: %.2f %.2f %.2f" % icm.gyro + " deg/s")
            print("Weather API URL sent: " + complete_url)
            print()

            error_list = [] # for debugging

            value_check = input("Are these values correct? y/n ")
            if value_check == "y":
                pass # autism
            else:
                preflight_errors += 1
                #error_list.append("Preflight not confirmed")


            # ----------------------Error checking----------------------
            if low_batt.is_active == True:
                print(Fore.YELLOW + "Low battery warning: " + str(low_batt.is_active))
                preflight_errors += 1
                #error_list.append("Low batt = true")
            
            #if camera == read_bytes

            if bmp.sea_level_pressure != current_pressure:
                print(Fore.YELLOW + "Barometer calibration pressure does not match weather API pressure")
                preflight_errors += 1
                #error_list.append("Baro calibration != API pressure")
                # this should theoretically never happen but I like to be safe. 
                # Its like writing => rather than >. It only needs to be >, but you
                # add the = just in case your code does the impossible or the
                # sun does a little trolling and screws with bits.

            if STARTING_ALTITUDE > bmp.altitude + 2 or STARTING_ALTITUDE < bmp.altitude - 2:
                print(Fore.YELLOW + "Starting altitude does not match barometer altitude")
                preflight_errors += 1
                #error_list.append("Starting altitude != barometer altitude")

            if launch_countdown <= 6:
                print(Fore.YELLOW + "Low countdown time (" + str(launch_countdown) + ")")
                preflight_errors += 1      
                #error_list.append("Low countdown time")         

            if  ran_launch == 1:
                print(Fore.YELLOW + "Software not rebooted after last launch")
                preflight_errors += 1
                #error_list.append("Software not rebooted after last launch")

            if  mute_beeper == 1:
                print(Fore.YELLOW + "Countdown beeper muted")
                preflight_errors += 1
                #error_list.append("Countdown beeper muted")
                
            if enable_camera == 0:
                print(Fore.YELLOW + "Camera disabled")
                preflight_errors += 1
            

            if preflight_errors > 0:
                print(Fore.RED + "Stopping the countdown. There are " + str(preflight_errors) + " preflight errors" )
                #print(Fore.RED + "Error list: " + str(error_list))
                continue_launch = input("Continue with the launch? y/n ")

                if continue_launch == "y":
                    cc()
                    begin_countdown("Launch")

                else:
                    cc()
                    print(Fore.YELLOW + "Launch aborted")
                    main_menu()

            elif preflight_errors == 0:
                begin_countdown("Launch")
    
        # ------------------------------- End Main flight code -------------------------------


        def begin_countdown(type):  # The type param is so other code can also use the countdown
            global launch_countdown
            global kill_rgb
            kill_rgb = 1
            led_neo.fill((0, 0, 255))
            cc()
            print("Countdown for " + Fore.GREEN + type)

            confirm_countdown = input("Are you sure you want to start the countdown? y/n ")
            if confirm_countdown == "y":
                cc()
                print(Fore.CYAN + "Starting " + type + " Countdown. Press CTRL + C to cancel")   
                print()
            
                if enable_camera == 1:
                    t_cam = threading.Thread(target=camera_func)
                    t_cam.start()
                print()

                for i in range(launch_countdown):
                    launch_countdown -= 1
                    print(Fore.LIGHTYELLOW_EX + str(launch_countdown))
                    led_neo.fill((255, 0, 0))
                    beeper(1)
                    time.sleep(0.5)
                    led_neo.fill((0, 0, 0))
                    beeper(0)
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
            kr()
            led_neo.fill((0, 0, 255))
            while view_sensor_count > 1:
                cc()
                print(now.strftime("Time & date:  %H:%M %m-%d-%Y"))
                print("Low battery warning: " + str(low_batt.is_active))
                print("Barometer altitude: {:5.2f}".format(bmp.altitude) + "m")
                print("Barometer pressure: {:5.2f}".format(bmp.pressure) + "mbar")
                print("Weather API pressure = " + str(current_pressure) + "mbar")   # this should match the baro calibration pressure
                print("Barometer calibration pressure = " + str(bmp.sea_level_pressure) + "mbar")
                print("Temperature: {:5.2f}".format(bmp.temperature) + "°c")
                print("Acceration: %.2f %.2f %.2f" % icm.acceleration + " m/s²")
                print("Gyroscope: %.2f %.2f %.2f" % icm.gyro + " deg/s")
                time.sleep(0.1)
                view_sensor_count -= 1
            view_sensor_count = 50
            main_menu()


        def rgb():
            i = 0
            global kill_rgb
            while kill_rgb == 0:     
                i = (i + 1) % 256  # run from 0 to 255
                led_neo.fill(colorwheel(i)) # Unicorn barf
                time.sleep(0.01)


        def main_menu(): 
            global kill_rgb
            kill_rgb = 1 # stops any previous RGB threads
            kill_rgb = 0 # allows new RGB thread
            t_rgb = threading.Thread(target=rgb)
            t_rgb.start()

            beeper(1)
            time.sleep(0.1)
            beeper(0)

            print("Chungus Aerospace Logic Controller By Besser and Joe Mamma")
            print(version, end=" ")
            print(code_revision_date)
            print("Time: " + global_current_time)


            """            #NOTE reads \desktop\ modified time, not this file
            abspath = os.path.abspath(sys.argv[0])
            dname = os.path.dirname(abspath)
            os.chdir(dname)
            # Get file's Last modification time stamp only in terms of seconds since epoch 
            modTimesinceEpoc = os.path.getmtime(dname)
            # Convert seconds since epoch to readable timestamp
            modificationTime = time.strftime("%H:%M", time.localtime(modTimesinceEpoc))
            print(Fore.MAGENTA + "Last Modified Time: ", modificationTime )
            #print("Confirm reload: " + str(RELOAD_RNG)) # for dev, makes sure the file is reloaded by seeing this number change
            """
            import datetime
            file = "CALCv2.py"
            print("last modified: %s" % time.ctime(os.path.getmtime(file)))
            #import os.path
            #print("Created: %s" % time.ctime(os.path.getctime("CALCv2.py")))

            cpu = CPUTemperature()
            print("Pi CPU Temp: " + str(cpu.temperature))

            print()
            print(Fore.CYAN + "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            print(Fore.LIGHTGREEN_EX + "Options:")
        
            # reorder this text in an order that makes sense
            print("1: Start launch wizard")     
            print("2: Start launch (no preflight check)")
            #print("2: Checklist")
            #print("3: Display last launch summary")
            #print("4. Push last launch folder to GitHub")
            print("5. View current sensor data")
            print("6. View weather")
            print("7. Test fire charges")
            #print("9. CSV Flight Data Analyzer") 
            print("9. Remux video")
            print("R: Rocket settings")
            print()
            print("L: Reload software")
            print("X: Shutdown")
            print("Q: Quit")

            which_option = input("What would you like to do? ")
            if "1" == which_option:
                kill_rgb = 1
                cc()
                preflight_checks()
            elif "2" == which_option:
                cc()
                begin_countdown("Launch")
            elif "3" == which_option:
                cc()
                main_menu()
            elif "4" == which_option:
                cc()
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
            elif "9" == which_option:
                cc()
                kr()
                led_neo.fill((0, 0, 255))
                print(Fore.GREEN +"Remuxing video")
                os.system("MP4Box -add video.h264 output.mp4")
                #cc()
                print(Fore.GREEN +"Video remuxed")
                main()
            elif "10" == which_option:
                cc()
                rocket_settings()
            elif "r" == which_option:   
                cc()
                rocket_settings()
            elif "d" == which_option:   # d is for development. I can just put whatever I want there to run it quickly
                cc()
                calibrate_sensors()
                main_menu()



            elif "l" == which_option:
                try:
                    camera.stop_preview()
                    camera.stop_recording()
                    camera.close()
                except:
                    print(Fore.RED + "Camera error")



                camera.close()



                print(Fore.GREEN + "Reloading...")
                os.execl(sys.executable, sys.executable, *sys.argv)


            elif "q" == which_option:
                cc()
                beeper(0)
                motor_relay.off()
                chute_relay.off()
                kill_rgb = 1
                led_neo.fill((0, 0, 0))
                sys.exit()
            elif "x" == which_option:
                cc()
                beeper(0)
                motor_relay.off()
                chute_relay.off()
                kill_rgb = 1
                led_neo.fill((0, 0, 0))
                shut = input("Are you sure you want to shutdown? y/n ")
                if shut == "y":
                    cc()
                    os.system("systemctl poweroff") 
                else:
                    cc()
                    main_menu()
            else:
                cc()
                print(Fore.RED + "Invalid input")
                main_menu()
        main_menu()

        
    except KeyboardInterrupt: 
        global kill_rgb
        try:
            camera.stop_recording()
            camera.stop_preview()
            #camera.close() 
        except:
            cc()
            print(Fore.RED + "Camera error")
            #print(Fore.RED + traceback.format_exc())

        if ran_launch == 1:
            if wrote_to_log_list == 0:
                with open(file_location + FILE_NAME, "a") as f: 
                    f.write(','.join(log_list))
            
            print(Fore.GREEN + " Reloading...")
            os.execl(sys.executable, sys.executable, *sys.argv)

        print()
        print()
        kill_rgb = 1
        led_neo.fill((0, 0, 0))

        beeper(0)
        motor_relay.off()
        chute_relay.off()
        print(Fore.YELLOW + "Keyboard Interrupt")
        main()     

    except Exception:
        print(traceback.format_exc())
        with open("last_error.txt", "a") as f: 
            f.write(str(time_and_date) + "\n" + str(traceback.format_exc()))
            f.write("\n" * 2)
main()


