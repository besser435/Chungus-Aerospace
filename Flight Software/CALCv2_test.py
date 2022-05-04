version = "CALC v2.0-beta.5"
code_revision_date = "April 2022"

from random import randint
import board
import adafruit_icm20x
import adafruit_bmp3xx
from gpiozero import CPUTemperature
from gpiozero import DigitalOutputDevice
from gpiozero import InputDevice
import time
import threading
import sys
import os
from colorama import init
init()
from colorama import Fore
init(autoreset=True)
import requests
from requests.structures import CaseInsensitiveDict

from datetime import datetime
import random


# Setup Bits
# I2C Bus
i2c = board.I2C() 

# BMP390
bmp = adafruit_bmp3xx.BMP3XX_I2C(i2c)
bmp.pressure_oversampling = 2   #NOTE This was 8 by default
bmp.temperature_oversampling = 2
bmp._wait_time = 0


bmp_chute = adafruit_bmp3xx.BMP3XX_I2C(i2c, address=0x76)
bmp_chute.pressure_oversampling = 8   #NOTE This was 8 by default
bmp_chute.temperature_oversampling = 2
bmp_chute._wait_time = 0


# ICM20649
icm = adafruit_icm20x.ICM20649(i2c)
adafruit_icm20x.ICM20649.accelerometer_range = 16
adafruit_icm20x.ICM20649.gyro_range = 500

adafruit_icm20x.gyro_data_rate = 5000
adafruit_icm20x.accelerometer_data_rate = 5000



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

# general options
#debug = 0
launch_countdown = 11 # also acts as storage
mute_beeper = 0

# weather options
zip_code = "85054"
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


"""# rocket storage
fire_chute_alt = 100    # default value in m, changes based on user input
arm_chute_alt = fire_chute_alt - 2"""
loop_parachute = 1
did_deploy = 0

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
        bmp_chute.sea_level_pressure = current_pressure 
        STARTING_ALTITUDE = (round(bmp.altitude, 2)) # needs to be below the calibrated pressure so its accurate


        def parachute():
            global loop_parachute
            global did_deploy
            #time.sleep(3)
            print(Fore.LIGHTGREEN_EX + "Parachute thread created")
            while loop_parachute == 1:
#NOTE
                #if bmp.altitude < STARTING_ALTITUDE + 3: #NOTE race condition?
                    if did_deploy == 0:
                        chute_relay.on()
                        print(Fore.LIGHTMAGENTA_EX + "Deployed parachute")
                        log_list.extend(["Deployed parachute,"])
                        did_deploy = 1
                        time.sleep(1)

                        chute_relay.off()
                        print(Fore.LIGHTMAGENTA_EX + "Parachute relay off")
                        log_list.extend(["Parachute relay off,"]) 
                        loop_parachute = 0
                        print(Fore.LIGHTMAGENTA_EX + "Chute loop state: " + str(loop_parachute))


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
            global loop_parachute


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
                f.write("Altitude (m), Accel on xyz (m/s^2), Gyro on xyz (deg/s), Time (s), Events\n")
                #f.write(",,,,\n")  # creates the right amount of columns 
                f.write("Software version: " + version + ",,,,,\n")
                f.write("Date: " + global_current_date + ",,,,,\n")   # The extra commas is so GitHub doesnt get cranky
                f.write("Time: " + global_current_time + ",,,,,\n")
                f.write("Temperature: {:5.2f}".format(bmp.temperature) + ",,,,,\n")
                f.write("Starting altitude: " + str(STARTING_ALTITUDE) + ",,,,,\n")
                f.write("Current Barometer pressure: {:5.2f}".format(bmp.pressure) + ",,,,,\n")
                f.write("Current weather API pressure: " + str(current_pressure) + ",,,,,\n")
                f.write("Pressure oversampling: " + str(bmp.pressure_oversampling) + ",,,,,\n")
                f.write(",,,,,,\n")
                f.write("Altitude (m), Accel on xyz (m/s^2), Gyro on xyz (deg/s), Time (s), Events\n")
                
        
            print(Fore.LIGHTGREEN_EX + "Motor Lit")
            motor_relay.on()    # launches the rocket 

            loop_parachute = 1
            t_parachute = threading.Thread(target=parachute)
            t_parachute.start()

            while True: # wait for liftoff then go to logging
                motor_start_time += 1
                if logged_liftoff == 0: 
                    if motor_start_time > 200: # time to wait until cancel (10ms. 100 = 1s)
                        print(Fore.RED + "Motor not starting! Canceled launch")
                        motor_relay.off()
                        chute_relay.off()
                        loop_parachute = 0
                        main_menu()
                        break

#NOTE
                    if bmp.altitude >= STARTING_ALTITUDE + 0:
                        log_list.extend(["Liftoff detected,"])
                        print(Fore.LIGHTGREEN_EX + "Liftoff detected")
                        print(Fore.LIGHTGREEN_EX + "Starting altitude: " + str(STARTING_ALTITUDE))
                        # nice for night launches 
                        motor_relay.off()
                        logged_liftoff += 1
                        break


############################### Test code ###############################
            """            initial_time_d = time.monotonic()
            motor_lit_d = 0
            while True: # wait for liftoff then go to logging
                current_time_d = time.monotonic()
                time_stamp = current_time_d - initial_time_d

                if motor_lit_d == 0:
                    led_neo[0] = (20, 235, 35) # indicates the motor has been fired and is waiting for liftoff detection to run log code 
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
                    led_neo[0] = (255, 255, 255)    # indicates liftoff has been detected and it passed to the logging code.
                    motor_relay.off()
                    logged_liftoff += 1
                    break
                """         
###############################


            #                          ------------------------ Main data logging code ------------------------
            initial_time = time.monotonic() # needs to be here and not in the time set ups bits code for reasons
            while True: 
                current_time = time.monotonic()
                time_stamp = current_time - initial_time

                log_list.extend([
                "\n"
                "{:5.2f}".format(bmp.altitude),
                #"{:5.2f}chute".format(bmp_chute.altitude),
                #"%.2f %.2f %.2f" % (icm.acceleration),
                "%.2f %.2f %.2f" % (icm.gyro),
                "{:5.2f}".format(time_stamp),
                ])

                #print("Alt: {:5.2f}".format(bmp.altitude) + "m", end = "   ")   
                #print("Time: {:5.2f}".format(time_stamp) + "s")
                

                # NOTE this parachute code drastically slows down the code. if the Pi isnt controlling the chute comment out this code
                # Arm parachute
                """ if chute_armed == 0: # this is so the event isnt logged repeatedly
                    if bmp.altitude >= STARTING_ALTITUDE + 50:  # 50 # I know that and statements are a thing, but this is easier to read imo
                        log_list.extend(["Armed parachute,"])
                        print(Fore.LIGHTMAGENTA_EX + "Armed parachute")
                        chute_armed += 1
                    # the arm code could just be the deploy code. if bmp.altitude >= STARTING_ALTITUDE + 50: deploy
                    # keep for now for reasons

                # Deploy parachute
                if chute_armed == 1: #if bmp.altitude >= STARTING_ALTITUDE + 50:
                    if chute_deployed == 0: # prevents the event from being ran repeatedly 
                        if bmp.altitude <= STARTING_ALTITUDE + 47:  #47 # once the rocket sinks below this it fires the chute
                            DATA_CYCLES_CHUTE = data_cycles 
                            chute_relay.on()
                            log_list.extend(["Deployed parachute,"])
                            print(Fore.LIGHTMAGENTA_EX + "Deployed parachute")
                            chute_deployed +=1

                    # Open chute relay
                    if chute_deployed == 1:   
                        if logged_chute_deploy == 0:  # prevents the event from being ran repeatedly
                            if data_cycles > DATA_CYCLES_CHUTE + 15:  # waits data cycles before opening the relay. pure autism
                                chute_relay.off()
                                log_list.extend(["Parachute relay off,"])
                                print(Fore.LIGHTMAGENTA_EX + "Parachute relay off")
                                logged_chute_deploy += 1 """
               

#NOTE           # stops the logging of data
                if data_cycles > 100:  # ensures that the logging is not stopped on the pad  
                    if bmp.altitude <= STARTING_ALTITUDE + 4:   # + 4 is incase it lands above the starting elevation or the sensor drifts
                        log_list.extend(["Stopped logging low alt met,"])
                        loop_parachute = 0
                        print(Fore.LIGHTCYAN_EX + "Stopped logging low alt met {:5.2f}".format(bmp.altitude) + "m")
                        print(Fore.LIGHTCYAN_EX + "Starting altitude: " + str(STARTING_ALTITUDE) + "m")
                        print(Fore.LIGHTGREEN_EX + "RESTART SOFTWARE TO LOG AGAIN")
                        break

                    """if data_cycles > 500:
                        log_list.extend(["Data cycles > 500 stopping logging,"])
                        log_list.extend(["This means altitude code did not execute. Fix this,"])
                        break"""

       

                
                data_cycles += 1 
            with open(file_location + FILE_NAME, "a") as f: 
                f.write(','.join(log_list))
                wrote_to_log_list += 1
                print("Wrote to data log")

                
            #                          ------------------------ End of main data logging code ------------------------



        def main_menu():  
            global kill_rgb
            global loop_parachute
            kill_rgb = 1 # stops any previous RGB threads
            kill_rgb = 0 # allows new RGB thread"""


            print("Chungus Aerospace Logic Controller By Besser and Joe Mamma")
            print(version)
            print(code_revision_date)
            print("Time: " + global_current_time)
            print("Confirm reload: " + str(RELOAD_RNG)) # for dev, makes sure the file is reloaded by seeing this number change

            print()
            print(Fore.CYAN + "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            print(Fore.LIGHTGREEN_EX + "Options:")
        
            # reorder this text in an order that makes sense
            print("1: Start Launch Wizard")     
            print("L: Reload software")

            which_option = input("What would you like to do? ")
            if "1" == which_option:
                cc()
                flight_software()
          
            elif "q" == which_option:
                cc()
                motor_relay.off()
                chute_relay.off()
                kill_rgb = 1
                loop_parachute = 0
                sys.exit()
            elif "l" == which_option:
                print(Fore.GREEN + "Reloading...")
                os.execl(sys.executable, sys.executable, *sys.argv)
           
            else:
                cc()
                print(Fore.RED + "Invalid input")
                main_menu()
        main_menu()

        
    except KeyboardInterrupt:
        global kill_rgb
        if ran_launch == 1:
            if wrote_to_log_list == 0:
                with open(file_location + FILE_NAME, "a") as f: 
                    f.write(','.join(log_list))
            
            print(Fore.GREEN + " Rebooting...")
            os.execl(sys.executable, sys.executable, *sys.argv)

        print()
        print()
        kill_rgb = 1

        motor_relay.off()
        chute_relay.off()

        print(Fore.YELLOW + "Keyboard Interrupt")
        main()                
main()
