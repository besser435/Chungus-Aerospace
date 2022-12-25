"""
---Chungus Aerospace Program---
https://github.com/besser435/Chungus-Aerospace

Flight Software for the CALC flight system by Joe Mama and besser.
This current code is meant to run on a Feather M4. Thats what the 
pinouts are configured for.

#NOTE This code doesnt work currently. The log list will also fill up the memory, causing an unhandled exception.
"""
version = "v1.15"
date = "December 2022"

#import adafruit_adxl34x
import adafruit_bmp3xx, adafruit_pcf8523, adafruit_sdcard
import time, gc, sys, traceback, neopixel, board, digitalio, storage
from rainbowio import colorwheel
from analogio import AnalogIn

#import adafruit_icm20x # missing above

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

# Accelerometer go thoughout the code and uncomment the NOTE lines to enable the accelerometer
#accel = adafruit_adxl34x.ADXL345(i2c)
#accel = adafruit_icm20x.ICM20649(i2c)

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
mute_beeper = 1
bmp.sea_level_pressure = 1013
log_stop_count = 400        # when to stop logging after an amount of data points are collected, backup to low altitude condition
log_delay = 2               # Waits this many seconds before the logging starts. Delay so the rocket can be set up to launch before logging starts
FILE_NAME = "launch " + "%d-%d-%d" % (t.tm_mon, t.tm_mday, t.tm_year) + " %d;%02d;%02d" % (t.tm_hour, t.tm_min, t.tm_sec) + ".csv"  # pure stupidity
event_comma_count = ",,," # makes sure events go in their own column on the far right 


# ------------------------- storage ------------------------
landed = 0
STARTING_ALTITUDE = bmp.altitude
launch_delay_count = 3
logged_liftoff = 0
data_cycles = 0
log_list = []
i = 0

def beep(state):
    if not mute_beeper:
        if not development_mode:
            if state:
                beeper.value = True
            else:
                beeper.value = False
        
# .csv creation and formatting
with open("/sd/" + FILE_NAME, "a") as f: 
    f.write(",,,,,\n")  # creates the right amount of columns 
    f.write("Date: %d/%d/%d" % (t.tm_mon, t.tm_mday, t.tm_year) + ",,,,,\n")   # The extra commas is is GitHub doesnt get cranky
    f.write("Time: %d:%02d:%02d" % (t.tm_hour, t.tm_min, t.tm_sec) + ",,,,,\n")
    f.write("Software version: " + version + ",,,,,\n")
    f.write("Voltage: {:.2f}".format(battery_voltage) + ",,,,,\n")   # If USB is connected it will read that voltage instead
    f.write("Starting altitude (const var): " + str(STARTING_ALTITUDE) + ",,,,,\n")
    f.write("Temp: " + str(bmp.temperature) + ",,,,,\n")
    f.write("Pressure: " + str(bmp.pressure) + ",,,,,\n")
    f.write("Data points cutoff: " + str(log_stop_count) + ",,,,,\n")
    #f.write("Pressure (mbar),Temperature (°c),Altitude (m),Accel on xyz (m/s^2),Elapsed Seconds,Events\n")
    f.write("Altitude (m),Accel on xyz (m/s^2),Time (s),Events\n")
    led_neo[0] = (20, 235, 35)    # indicates the motor has been fired and is waiting for liftoff detection to run log code
    f.write(event_comma_count + "\nGoing to liftoff detection\n")


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
    for i in range(3):
        led_neo[0] = (0, 255, 0)
        time.sleep(0.1)
        led_neo[0] = (0, 0, 0)
        time.sleep(0.1)

    while launch_delay_count <= log_delay: #TODO needs a new start thing. this is dumb and doesnt test write capability
        launch_delay_count += 1
        led_neo[0] = (255, 255, 0)
        time.sleep(0.5)
        beep(1)
        print("T-" + str(launch_delay_count))
        led_neo[0] = (0, 0, 0)
        time.sleep(0.5)
        beep(0)
    led_neo[0] = (0, 0, 0)    
    


    beep(1)
   
     
# liftoff detection 
if development_mode == 0:
    while True:
        if bmp.altitude >= STARTING_ALTITUDE + 5:
            if logged_liftoff == 0:
                with open("/sd/" + FILE_NAME, "a") as f:
                    #f.write("{:5.2f},{:5.2f},{:5.2f},".format(bmp.pressure, bmp.temperature, bmp.altitude,))
                    f.write("{:5.2f},".format(bmp.altitude,))
                    #NOTE f.write("%.2f %.2f %.2f," % accel.acceleration,)
                    f.write(",Liftoff detected\n")
                    led_neo[0] = (0, 0, 255)    # indicates liftoff has been detected and it passed to the logging code.
                    # this is for dev purposes, you wont see it because the rocket will be in the air already
                beep(0)
                logged_liftoff += 1
                break

#                          ------------------------ Main data logging code ------------------------
led.value = True  # turn on LED to indicate writing has started
initial_time = time.monotonic() # needs to be here and not in the time set ups bits code for reasons


chute_armed = 0
chute_deployed = 0
logged_chute_deploy = 0 






chute_deploy_timestamp = None   # is this needed here, or can the vars access each other in the loop?
chute_trigger_time = 2 # seconds




def main_logging():
    global chute_armed, chute_deployed, logged_chute_deploy, data_cycles, landed, chute_deploy_timestamp, chute_trigger_time
    if development_mode: time.sleep(2)
    while True:   
        bmp_alt = bmp.altitude
        #NOTE accel_xyz = accel.acceleration
    
        current_time = time.monotonic()
        time_stamp = current_time - initial_time

        log_list.extend([
        "\n"
        "{:5.2f}".format(bmp_alt),
        #NOTE "%.2f %.2f %.2f" % (accel_xyz),
        "%.2f %.2f %.2f" % (0.000, 0.000, 0.000), # placeholder for acceleration
        "{:5.2f}".format(time_stamp)
        ])


        # Deploy parachute
        chute_armed = 1 #TODO this needs to be implemented properly
        if bmp_alt >= STARTING_ALTITUDE + 42:  # NOTE copilot code. check old code to see that it matches this to make sure it works
            chute_armed = 1

        if chute_armed: 
            if chute_deployed == 0: # prevents the event from being ran repeatedly 
                if bmp_alt <= STARTING_ALTITUDE + 40:  # deploy altitude
                    #NOTE DATA_CYCLES_CHUTE = data_cycles 

                    chute_deploy_timestamp = time_stamp

                    chute_relay.value = True
                    log_list.extend(["Deployed parachute,"])
                    print("Deployed parachute")
                    chute_deployed +=1

            # Open chute relay
            # This needs to be a thing, because when the chute deploys, the power source for the relay
            # might still be connected after the chute deploys. This dead short in the battery is obviously not great.
            if chute_deployed:   
                if logged_chute_deploy == 0:  # prevents the event from being ran repeatedly
                    #NOTE if data_cycles > DATA_CYCLES_CHUTE + 25:  # waits about a second before opening the relay. pure autism
                    if time_stamp >= chute_deploy_timestamp + chute_trigger_time: 
                        chute_relay.value = False
                        log_list.extend(["Parachute relay off,"])
                        print("Parachute relay off")
                        logged_chute_deploy += 1 
            

        # stops the logging of data
        if data_cycles >= 600:  # ensures that the logging is not stopped on the pad  
            if bmp_alt <= STARTING_ALTITUDE + 10:   # + 10 is incase it lands above the starting elevation or the sensor drifts
                log_list.extend(["Stopped logging low alt met,"])
                print("Stopped logging low alt met {:5.2f}".format(bmp.altitude) + "m")
                print("Starting altitude: " + str(STARTING_ALTITUDE) + "m")
                
                landed = 1
                break
            
            if data_cycles >= 1000: # Backup to the code above
                log_list.extend(["Data cycles > 1000 stopping logging,"])
                log_list.extend(["This means altitude code did not execute. Fix this,"])
                print("Data cycles > 1000 stopping logging. This means altitude code did not execute.")
                print("INVESTIGATE ISSUE BEFORE RESTARTING SOFTWARE")

                landed = 1
                break
       
        # this prevents the RAM from running out
        remainder = data_cycles % 70
        is_divisible = remainder == 0
        if is_divisible:   
            with open(FILE_NAME , "a") as f:
                f.write(','.join(log_list))
            log_list.clear()
            log_list.extend(["\n,,,RAM flushed at " + str("%.2f" % time_stamp) + "\n"])
            print("RAM flushed")


        data_cycles += 1 
        print("Data cycles: " + str(data_cycles) + "   Time: %.2f" % time_stamp + "   Free RAM: " + str(gc.mem_free()))

"""#NOTE this doesnt work. When it runs out of memory, it cant log the list and throws another error.
while not landed: # why are there two identical loops? I have no idea, but they are both need! Thank you programming.
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


main_logging()           

print("done, writing to file")
with open("/sd/" + FILE_NAME, "a") as f: 
    f.write(','.join(log_list))
    
#                          ------------------------ End of main data logging code ------------------------
led.value = False  # turn off LED to indicate writing is done


while development_mode == False:
    led_neo[0] = (255, 255, 255)
    beep(1)
    time.sleep(0.3)

    beep(0)
    led_neo[0] = (0, 0, 0)
    time.sleep(0.3)

