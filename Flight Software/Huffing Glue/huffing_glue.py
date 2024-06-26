"""
---Chungus Aerospace Program---
https://github.com/besser435/Chungus-Aerospace

Huffing Glue flight Software for a modified version of the CALC flight system by Joe Mama and besser.
This current code is meant to run on a Feather M4. Thats what the pinouts are configured for.

#NOTE This code doesnt work currently. The log list will also fill up the memory, causing an unhandled exception.
"""
version = "v1.0-alpha.1"
date = "January 2023"

#import adafruit_adxl34x
#import adafruit_icm20x
import adafruit_bmp3xx, adafruit_pcf8523, adafruit_sdcard, math
import time, gc, sys, traceback, neopixel, board, digitalio, storage
from rainbowio import colorwheel
from analogio import AnalogIn

import adafruit_icm20x # missing above

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
led_neo[0] = (0, 0, 0) 

# BMP388
bmp = adafruit_bmp3xx.BMP3XX_I2C(i2c)
bmp.pressure_oversampling = 4 # 8 by default
bmp.temperature_oversampling = 2

# Accelerometer go throughout the code and uncomment the NOTE lines to enable the accelerometer
#accel = adafruit_adxl34x.ADXL345(i2c)
#accel = adafruit_icm20x.ICM20649(i2c)
adafruit_icm20x.ICM20649.accelerometer_range = 30
adafruit_icm20x.ICM20649.accel_dlpf_cutoff.DISABLED #TODO Test this and see if it helps increase the sample rate. https://forums.adafruit.com/viewtopic.php?f=19&p=844371

# Real time clock
rtc = adafruit_pcf8523.PCF8523(i2c)
t = rtc.datetime

# Relay to deploy chute
chute_relay = digitalio.DigitalInOut(board.D9)  # NOTE change this pin to whatever pin is good. 
chute_relay.direction = digitalio.Direction.OUTPUT

# Beeper
beeper = digitalio.DigitalInOut(board.D5)
beeper.direction = digitalio.Direction.OUTPUT


# ------------------------- options ------------------------
development_mode = 1        # edits things like countdown so the code can be tested easier without having to change several other options
#CHUTE_DEPLOY_ALT = 50  #NOTE not used. This would be less prone to errors, maybe use it
#CHUTE_ARM_OFFSET = 5       # alt separation in meters between when the chute is armed and when it is deployed
mute_beeper = 1
bmp.sea_level_pressure = 1013
log_stop_count = 400        # when to stop logging after an amount of data points are collected, backup to low altitude condition
launch_countdown = 10       # Waits this many seconds before the logging starts. Delay so the rocket can be set up to launch before logging starts
chute_trigger_time = 2      # seconds the chute relay will be triggered for


 


FILE_NAME = "launch " + "%d-%d-%d" % (t.tm_mon, t.tm_mday, t.tm_year) + " %d;%02d;%02d" % (t.tm_hour, t.tm_min, t.tm_sec) + ".csv"  # pure stupidity

x_adjust = 4.014
y_adjust = 9.042
z_adjust = 3.141
g = 9.816

# ------------------------- storage ------------------------
landed = 0
STARTING_ALTITUDE = bmp.altitude
logged_liftoff = 0
data_cycles = 1
log_list = []
chute_armed = 0
chute_deployed = 0
logged_chute_deploy = 0 
chute_deploy_timestamp = None   # is this needed here, or can the vars access each other in the loop?


def beep(state):
    if not mute_beeper and not development_mode:
        if state:
            beeper.value = True
        else:
            beeper.value = False

def write(data):
    try:
        # write to SD card
        with open("/sd/" + FILE_NAME, "a") as f: 
            f.write(data)

        # write to built in flash
        with open(FILE_NAME, "a") as f: 
            f.write(data)

    except Exception as e:
        print("Write error in write() function")
        print(e)
        
def write_test():   
    """
    Will throw an error amd stop the countdown if something is bunged. boot.py should catch this, but this is here for reasons.
    
    Normally during .csv creation, the drive is written to, and if that failed it would throw an error. However
    I catch those errors incase they happen during the main loop, that way the main loop can continue.

    This will throw an uncaught error if the drive is bunged, so I know there is an issue before putting the computer in the rocket.
    """

    with open("write_test.txt", "a") as f: 
        f.write("write test success in huffing_glue.py at " + "%d-%d-%d" % (t.tm_mon, t.tm_mday, t.tm_year) + " %d:%02d:%02d" % (t.tm_hour, t.tm_min, t.tm_sec) + "\n\n")
write_test()

def create_csv():   # .csv creation and formatting
    #with open("/sd/" + FILE_NAME, "a") as f: 
    write(",,,,,\n")  # creates the right amount of columns 
    write("Date: %d/%d/%d" % (t.tm_mon, t.tm_mday, t.tm_year) + ",,,,,\n")   # The extra commas is is GitHub doesnt get cranky
    write("Time: %d:%02d:%02d" % (t.tm_hour, t.tm_min, t.tm_sec) + ",,,,,\n")
    write("Software version: " + version + ",,,,,\n")
    write("Voltage: {:.2f}".format(battery_voltage) + ",,,,,\n")   # If USB is connected it will read that voltage instead
    write("Starting altitude (const var): " + str(STARTING_ALTITUDE) + ",,,,,\n")
    write("Temp: " + str(bmp.temperature) + ",,,,,\n")
    write("Pressure: " + str(bmp.pressure) + ",,,,,\n")
    write("Data points cutoff: " + str(log_stop_count) + ",,,,,\n")
    write("Velocity cal nums: " + str(x_adjust) + ", " + str(y_adjust) + ", " + str(z_adjust) + ", " + str(g) + ",,,,,\n")
    write("Altitude (m),Accel on XYZ (m/s^2),Delta-v (m/s),Velocity (m/s),Time (s),Events\n")
create_csv()

def error(e):
    print(e)
    write(','.join(log_list))

    with open("/sd/" + "error.txt", "a") as f: 
        f.write("%d-%d-%d" % (t.tm_mon, t.tm_mday, t.tm_year) + " %d:%02d:%02d " % (t.tm_hour, t.tm_min, t.tm_sec))
        f.write(str(e) + "\n\n")

    with open("error.txt", "a") as f: 
        f.write("%d-%d-%d" % (t.tm_mon, t.tm_mday, t.tm_year) + " %d:%02d:%02d " % (t.tm_hour, t.tm_min, t.tm_sec))
        f.write(str(e) + "\n\n") 
  

if development_mode:
    print(version)
    led_neo.brightness = 0.05  # prevents flashbang   
    for i in range(3):
        led_neo[0] = (0, 255, 0)
        time.sleep(0.1)
        led_neo[0] = (0, 0, 0)
        time.sleep(0.1)
else:  # shows that the code is running 
    led_neo.brightness = 1
    print("Beginning countdown")
    for i in range(launch_countdown):
        launch_countdown -= 1
        print("T- " + str(launch_countdown))
        led_neo[0] = (255, 0, 0)
        beep(1)
        time.sleep(0.5)

        led_neo[0] = (0, 0, 0)
        beep(0)
        time.sleep(0.5)
    

# liftoff detection 
if not development_mode:
    print("Waiting for liftoff")
    led_neo[0] = (255, 69, 0)   # indicates waiting for liftoff 
    while True:
#NOTE This uses the baro, not accel. should be fine though.
        if bmp.altitude >= STARTING_ALTITUDE + 5:
            if not logged_liftoff:
                write("{:5.2f},".format(bmp.altitude,))
                logged_liftoff += 1
                break

#                          ------------------------ Main data logging code ------------------------
led.value = True  # turn on LED to indicate writing has started
initial_time = time.monotonic() # needs to be here and not in the time set ups bits code for reasons
def main_logging():
    global chute_armed, chute_deployed, logged_chute_deploy, data_cycles, landed, chute_deploy_timestamp, chute_trigger_time
    led_neo[0] = (0, 0, 255)
    beep(0)

    vel_0 = 0
    time_0 = 0
    accel_0 = g

    while True:   
        bmp_alt = bmp.altitude
        #accel_xyz = accel.acceleration
        #accel_x, accel_y, accel_z = accel_xyz   # unpacks the tuple
        accel_x, accel_y, accel_z = (9.811, 5.011, 0.311)  # unpacks the tuple

        current_time = time.monotonic()
        time_stamp = current_time - initial_time

        accel_mag = math.sqrt(pow(accel_x - x_adjust, 2) + pow(accel_y - y_adjust, 2) + pow(accel_z - z_adjust, 2))
        if accel_z < 0:
            accel_sign = -1
        else:
            accel_sign = 1

        accel_1 = accel_mag * accel_sign
        vel_1 = vel_0 + (accel_1 + accel_0 - 2 * g) * (time_stamp - time_0) * 0.5 #This is the integral of the magnitude of the acceleration vector.
        delta_v = vel_1 - vel_0
        time_0 = time_stamp
        vel_0 = vel_1
        accel_0 = accel_1


        log_list.extend([
        "\n"
        "{:5.2f}".format(bmp_alt),
        #NOTE "%.2f %.2f %.2f" % (accel_xyz),
        "%.2f %.2f %.2f" % (9.8169, 9.8169, 9.8169), # placeholder for acceleration
        "{:5.2f}".format(delta_v),
        "{:5.2f}".format(vel_1),
        "{:5.2f}".format(time_stamp)
        ])

#NOTE 
        # Arm parachute
        #if bmp_alt >= STARTING_ALTITUDE + (CHUTE_DEPLOY_ALT - CHUTE_ARM_OFFSET):  # NOTE copilot code. check old code to see that it matches this to make sure it works
        if not chute_armed: # prevents the event from being ran repeatedly
            if bmp_alt >= STARTING_ALTITUDE + 50:  # arm altitude. should be a few meters above the deploy altitude so ensure the rocket is descending
                log_list.extend(["Armed parachute,"])
                print("Armed parachute")
                chute_armed += 1
#NOTE 
        # Deploy parachute
        if chute_armed and not chute_deployed: 
            
            #velocity trigger, needs to be written better
            if vel_1 <= 3:
                pass


                


#NOTE
                if bmp_alt <= STARTING_ALTITUDE + 45:  # barometer deploy altitude, this is a backup to the velocity code
                    chute_deploy_timestamp = time_stamp
                    chute_relay.value = True
                    log_list.extend(["Deployed parachute from barometer,"])
                    print("Deployed parachute from barometer")
                    chute_deployed +=1







            # Open chute relay
            # This needs to be a thing, because when the chute deploys, the power source for the relay
            # might still be connected after the chute deploys. This dead short in the battery is obviously not great.
            if chute_deployed and not logged_chute_deploy:  # prevents the event from being ran repeatedly
                if time_stamp >= chute_deploy_timestamp + chute_trigger_time: 
                    chute_relay.value = False
                    log_list.extend(["Parachute relay off,"])
                    print("Parachute relay off")
                    logged_chute_deploy += 1 
        
#NOTE
        # stops the logging of data
        if data_cycles >= log_stop_count:  # ensures that the logging is not stopped on the pad  
            if bmp_alt <= STARTING_ALTITUDE + 15:   # +15 is incase it lands above the starting elevation or the sensor drifts
                log_list.extend(["Stopped logging low alt met,"])
                print("Stopped logging, low alt met {:5.2f}".format(bmp.altitude) + "m")
                print("Starting altitude: " + str(STARTING_ALTITUDE) + "m")
                break
            
            if data_cycles >= 800: # Backup to the code above
                log_list.extend(["Data cycles > 800 stopping logging,"])
                log_list.extend(["This means altitude code did not execute. Fix this,"])
                print("Data cycles > 800 stopping logging. This means altitude code did not execute.")
                break
       
        # this prevents the RAM from running out
#NOTE the added weight of the velocity code might lower the usable RAM. Make sure this number is low enough
        remainder = data_cycles % 45
        is_divisible = remainder == 0
        if is_divisible:   
            #with open(FILE_NAME , "a") as f:
            print("Storing log")
            write(','.join(log_list))
            log_list.clear()
            log_list.extend([",RAM flushed \n"])
            print("RAM flushed")

        data_cycles += 1 
        print("Data cycles: " + str(data_cycles) + 
        "   Velocity: %.2f" % vel_1 + 
        "   Delta-v: %.2f" % delta_v + 
        "   Time: %.2f" % time_stamp + 
        "   Free RAM: " + str(gc.mem_free()))

        #raise Exception("error handle test")

"""#NOTE this doesnt work. When it runs out of memory, it cant log the list and throws another error.
while not landed: # why are there two identical loops? I have no idea, but they are both needed! Thank you programming.
    while not landed:
        try:
            main_logging()
        except MemoryError as e: 
            print("Memory full, restarting logging code")
            print(e)
            with open("/sd/" + FILE_NAME, "a") as f: 
                f.write(','.join(log_list))
                log_list.clear()

        except Exception as e:
            print(e)
            with open("/sd/" + FILE_NAME, "a") as f:
                f.write(','.join(log_list))
                log_list.clear()
            print("Exception, restarting logging code")
            
            # this error log shouldnt be in the mem error, as that needs to be fast, and is expected to happen.
            with open("/sd/" + "error.txt", "a") as f: 
                f.write(str(e) + "\n")"""

#try:
main_logging()  

#except OSError as e:
    #error(e)

#except Exception as e:
    #error(e)


print("done, writing to file")
write(','.join(log_list))

#                          ------------------------ End of main data logging code ------------------------
led.value = False  # turn off LED to indicate writing is done

print("In recovery mode")
while True:
    led_neo.brightness = 1
    led_neo[0] = (255, 255, 255)
    beep(1)
    time.sleep(0.3)

    beep(0)
    led_neo[0] = (0, 0, 0)
    time.sleep(0.3)

