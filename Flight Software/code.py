"""
NOTE
---Chungus Aerospace Program---
https://github.com/besser435/Chungus-Aerospace

Flight Software for the CALC flight system by Joe Mama and besser.
This current code is meant to run on a Feather M4. Thats what the 
pinouts are configured for.

In the future this might run off of a Raspberry Pi Zero
for better I/O, camera support, and a few other things.


"""
version = "v1.12"
date = "March 2022"


import adafruit_bmp3xx
import adafruit_adxl34x
import adafruit_pcf8523
import adafruit_sdcard
import neopixel
import board
import digitalio
import storage
import time
from rainbowio import colorwheel
from analogio import AnalogIn


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
rtc = adafruit_pcf8523.PCF8523(i2c)
t = rtc.datetime

# Relay to deploy chute
chute_relay = digitalio.DigitalInOut(board.A1)  # NOTE change this pin to whatever pin is good. 
chute_relay.direction = digitalio.Direction.OUTPUT

# Motor ignition relay
motor_relay = digitalio.DigitalInOut(board.A0)  # NOTE change this pin to whatever pin is good. 
motor_relay.direction = digitalio.Direction.OUTPUT

# Beeper
beeper = digitalio.DigitalInOut(board.D4)
beeper.direction = digitalio.Direction.OUTPUT


# ------------------------- options ------------------------
development_mode = 0        # edits things like countdown so the code can be tested easier without having to change several other options
bmp.sea_level_pressure = 1013
log_stop_count = 400        # when to stop logging after an amount of data points are collected, backup to low altitude condition
log_delay = 60              # Waits this many seconds before the logging starts. Delay so the rocket can be set up to launch before logging starts
FILE_NAME = "launch " + str(t.tm_mon) + "-" + str(t.tm_mday) + "-" + str(t.tm_year) + ".csv"  # pure stupidity
event_comma_count = ",,," # makes sure events go in their own column on the far right 


# ------------------------- storage ------------------------
#launched = 0
STARTING_ALTITUDE = bmp.altitude
launch_delay_count = 0
logged_liftoff = 0
data_cycles = 0
i = 0


def emergency_chute_deploy():   # Not implemented yet
    # The feather might be too weak to do the math on the fly for determing a changng velocity,
    # but hopefully the Pi wont.
    """ if the sensors dont see the velocty slowing down after closing the relay for a second
    it will run this code. It will pulse the relay in order to try to ignite the charge.
    The chute deploy just used to do this, but it would lose logging data because of the delay.

    Im not sure how to do continuity detection on the Pi. I would just use that if possible """
    # log emergency deploy
    for i in range (5):             # motor ignition (loops to ensure it happens)
        chute_relay.value = True
        time.sleep(1)
        chute_relay.value = False
        time.sleep(0.5)
    # if deploy is detected by a reduction in velocity return to the logging code
    

if development_mode == 1:
    print("v" + str(version))
    led_neo.brightness = 0.05  # prevents flashbang   
    while launch_delay_count <= 2:
        launch_delay_count += 1
        led_neo[0] = (255, 255, 0)
        time.sleep(0.5)
        led_neo[0] = (0, 0, 0)
        time.sleep(0.5)

else:  # shows that the code is running 
    led_neo.brightness = 1
    for i in range(3):
        led_neo[0] = (0, 255, 0)
        time.sleep(0.1)
        led_neo[0] = (0, 0, 0)
        time.sleep(0.1)

    while launch_delay_count <= log_delay:
        launch_delay_count += 1
        led_neo[0] = (255, 255, 0)
        time.sleep(0.5)
        led_neo[0] = (0, 0, 0)
        time.sleep(0.5)
    led_neo[0] = (0, 0, 0)    
    

"""
# Sets the real time clock if enabled. Maybe make this a seperate script to clean up this one and so the time isnt reset by accident
days = ("Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday")
if False:   # change to True to write the time. remember to set to false before running the code again
    #                     year, mon, date, hour, min, sec, wday, yday, isdst
    t = time.struct_time((2022,  1,   7,   15,   43,   0,  5,    -1,  -1))
    rtc.datetime = t
"""


# .csv creation and formatting
with open("/sd/" + FILE_NAME, "a") as f: 
    f.write(",,,,,\n")  # creates the right amount of columns 
    f.write(str("Date: %d/%d/%d" % (t.tm_mon, t.tm_mday, t.tm_year) + ",,,,,\n"))   # The extra commas is is GitHub doesnt get cranky
    f.write("Time: %d:%02d:%02d" % (t.tm_hour, t.tm_min, t.tm_sec) + ",,,,,\n")
    f.write("Software version: " + version + ",,,,,\n")
    f.write("Voltage: {:.2f}".format(battery_voltage) + ",,,,,\n")   # If USB is connected it will read that voltage instead
    f.write("Starting altitude: " + str(STARTING_ALTITUDE) + ",,,,,\n")
    f.write("Data points cutoff: " + str(log_stop_count) + ",,,,,\n")
    #f.write("Pressure (mbar),Temperature (°c),Altitude (m),Accel on xyz (m/s^2),Elapsed Seconds,Events\n")
    f.write("Altitude (m),Accel on xyz (m/s^2),Elapsed Seconds,Events\n")

with open("/sd/" + FILE_NAME, "a") as f:   
    led_neo[0] = (20, 235, 35)    # indicates the motor has been fired and is waiting for liftoff detection to run log code
    f.write(event_comma_count + "Motor lit\n")
    beeper.value = True
    motor_relay.value = True    # lauches the rocket 
     

# potential way of starting the logging in the future. needs to be proven to work tho, which is what this is
# this should be in the main loop for now, but should be above it if this works.  
if development_mode == 0:
    while True:
        if bmp.altitude >= STARTING_ALTITUDE + 4.2:
            if logged_liftoff == 0:
                with open("/sd/" + FILE_NAME, "a") as f:
                    #f.write("{:5.2f},{:5.2f},{:5.2f},".format(bmp.pressure, bmp.temperature, bmp.altitude,))
                    f.write("{:5.2f},".format(bmp.altitude,))
                    f.write("%.2f %.2f %.2f," % accel.acceleration,)
                    f.write(",Liftoff detected\n")
            

                    led_neo[0] = (0, 0, 255)    # indicates liftoff has been detected and it passed to the logging code.
                    # this is for dev purposes, you wont see it because the rocket will be in the air already
                beeper.value = False
                motor_relay.value = False
                logged_liftoff += 1
                break

#                          ------------------------ Main data logging code ------------------------
led.value = True  # turn on LED to indicate writting has started
initial_time = time.monotonic() # needs to be here and not in the time set ups bits code for reasons

while True:   
    chute_armed = 0
    logged_chute_deploy = 0 

    # open file for append
    with open("/sd/" + FILE_NAME, "a") as f:    
        current_time = time.monotonic()
        time_stamp = current_time - initial_time

        #f.write("{:5.2f},{:5.2f},{:5.2f},".format(bmp.pressure, bmp.temperature, bmp.altitude,))
        f.write("{:5.2f},".format(bmp.altitude,))
        f.write("%.2f %.2f %.2f," % accel.acceleration,)
        f.write("{:5.2f}".format(time_stamp) + ",\n") # logs elapsed time 
        """

        # Arm
        if bmp.altitude >= STARTING_ALTITUDE + 50:  # I know that <and> statements are a thing, but this is easier to read imo
            if chute_armed == 0: # this is so the event isnt logged repeatedly
                f.write(event_comma_count + "Armed parachute. Current alt: " + str(bmp.altitude) +  "m . Current time: " + str(time_stamp) + "m\n")
                chute_armed += 1
                print("Armed parachute")

        # Deploy - close relay
        if chute_armed == 1:
            if bmp.altitude <= STARTING_ALTITUDE + 49:  # once the rocket sinks below 50 meters it fires the chute
                DATA_CYCLES_CHUTE = data_cycles 
                chute_relay.value = True

                if logged_chute_deploy == 0:
                    f.write(event_comma_count + "Deployed parachute. Current alt: " + str(bmp.altitude) + "m. Current time: " + str(time_stamp) + "\n")
                    logged_chute_deploy +=1

            # Open relay
            if logged_chute_deploy == 1:    # this might not work. 
                if DATA_CYCLES_CHUTE >= 10: # waits 10 data cyles before opening the relay
                    chute_relay.value = False   # this was True before and idk why. Does it actually need to be True?
                    f.write(event_comma_count + "Parachute relay off. Current time: " + str(time_stamp) + "\n")
                    print("Parachute relay off")"""


    # stops the logging of data
    if data_cycles > 200:    
    # makes sure the code below isnt just executed on the pad
        if bmp.altitude <= STARTING_ALTITUDE + 5:   # + 5 is incase it lands above the starting elevation or the sensor drifts
            with open("/sd/" + FILE_NAME, "a") as f:
                f.write(event_comma_count + "Stopped logging; low altitude met. (" + str(bmp.altitude) + "m)\n")
                break

    if data_cycles >= log_stop_count:   # backup to the code above
        if logged_chute_deploy == 1:    # ensures the chute deployed before breaking
            with open("/sd/" + FILE_NAME, "a") as f:
                f.write(event_comma_count + "Stopped logging; writes to file met. (" + str(data_cycles) + " writes) ")
                f.write(event_comma_count + "This means altitude code did not execute.\n")
                break

    data_cycles += 1 # this seems simple but its crucial to some things so dont mess with it
    #print("Data cycles: " + str(data_cycles)) # for debugging while editing code


#                          ------------------------ End of main data logging code ------------------------
led.value = False  # turn off LED to indicate writting is done


while development_mode == False:
    led_neo[0] = (255, 255, 255)
    beeper.value = True
    time.sleep(0.2)

    beeper.value = False
    led_neo[0] = (0, 0, 0)
    time.sleep(1)

while True:   
    led_neo[0] = (0, 255, 255)  


"""while True:     # indicates that the data recording is done
    i = (i + 1) % 256  
    led_neo.fill(colorwheel(i)) # Unicorn barf
    time.sleep(0.01)"""
