"""
This is the flight software for the Adafruit Ruler
https://www.adafruit.com/product/4319

Its a stupid idea to control a rocket with a ruler,
but its too good to pass up. This code needs to be
simple as the ruler doesnt have a lot of storage 
or RAM.


"""
version = "v1.0"

import time
import board
import adafruit_bmp3xx
import touchio
import adafruit_dotstar
from rainbowio import colorwheel
import digitalio

#from adafruit_dps310.basic import DPS310
     
"""# Setup
# LED for capacitive button setup. There is probably a better way of doing this
led4 = digitalio.DigitalInOut(board.LED4)   # Ω
led4.direction = digitalio.Direction.OUTPUT    

led5 = digitalio.DigitalInOut(board.LED5)   # µ
led5.direction = digitalio.Direction.OUTPUT

led6 = digitalio.DigitalInOut(board.LED6)   # µ
led6.direction = digitalio.Direction.OUTPUT

led7 = digitalio.DigitalInOut(board.LED7)   # Digikeys
led7.direction = digitalio.Direction.OUTPUT

# RGB goodness
led_dotstar = adafruit_dotstar.DotStar(board.APA102_SCK, board.APA102_MOSI, 1)
"""
# Motor ignition relay
motor_relay = digitalio.DigitalInOut(board.A0)  # NOTE change this pin to whatever pin is good. 
motor_relay.direction = digitalio.Direction.OUTPUT

# BMP388
i2c = board.I2C() 
bmp = adafruit_bmp3xx.BMP3XX_I2C(i2c)
bmp.pressure_oversampling = 8
bmp.temperature_oversampling = 2


# ------------------------- options ------------------------
launch_delay = 2
#led_dotstar.brightness = 0.07
file_name = "RULER ROCKET.csv"  
bmp.sea_level_pressure = 1024
log_stop_count = 400         # when to stop logging after an amount of data points are collected, backup to low altitude condition
event_comma_count = ",,,," # makes sure events go in their own column on the far right 

# storage
STARTING_ALTITUDE = bmp.altitude
data_cycles = 0
logged_liftoff = 0

"""
# broken cap code
touch_pad0 = board.CAP0
touch_pad1 = board.CAP1
touch_pad2 = board.CAP2
touch_pad3 = board.CAP3

touch = touchio.TouchIn(touch_pad2)

touch_count = 0
while True:
    led7.value = False
    if touch.value:
        print("Touched! " + str(touch_count))
        touch_count += 1
        led7.value = True

    led4.value = False
    if touch.value:
        print("Touched! " + str(touch_count))
        touch_count += 1
        led4.value = True


    time.sleep(0.1)
    break


#if two caps pressed for 3 seconds:
for i in range(launch_delay):   # countdown
    led_dotstar[0] = (255, 255, 0)
    time.sleep(0.5)
    led_dotstar[0] = (0, 0, 0)
    time.sleep(0.5)"""


print("Ready")



class intitial_write:   
    with open(file_name, "a") as f:     # might need to be with open("/" + file_name, "a") as f:
        f.write("Software version: " + version + "\n")
        f.write("Data points cutoff: " + str(log_stop_count) + "\n")
        f.write("Starting altitude: " + str(STARTING_ALTITUDE) + "\n")
        f.write("Pressure (mbar),Temperature (°c),Altitude (m),Elapsed Seconds,Events\n")
        motor_relay.value = True    # lauches the rocket    

        f.write(event_comma_count + "Motor lit\n")
        


class lifoff_detection:
    global initial_time
    while True:
        if bmp.altitude >= STARTING_ALTITUDE + 3:
            if logged_liftoff == 0:

                initial_time = time.monotonic() # needs to be here and not in the time set ups bits code for reasons
                current_time = time.monotonic()
                time_stamp = current_time - initial_time     

                with open(file_name, "a") as f:
                    f.write(",,," + str(time_stamp) + ",Liftoff detected\n")
                motor_relay.value = False
                logged_liftoff += 1
                break



#                          ------------------------ Main data logging code ------------------------
while True:    
    current_time = time.monotonic()
    time_stamp = current_time - initial_time

    # open file for append
    with open(file_name, "a") as f:    
        f.write("{:5.2f},{:5.2f},{:5.2f},".format(bmp.pressure, bmp.temperature, bmp.altitude,)) 
        f.write("{:5.2f}".format(time_stamp) + "\n") # logs elapsed time 


        # stops the logging of data
        if data_cycles > 50 and (bmp.altitude <= STARTING_ALTITUDE + 5): 
            """if this and statement works, implent into main code"""
    # makes sure the code below isnt just executed on the pad  
        #if bmp.altitude <= STARTING_ALTITUDE + 5:   # + 5 is incase it lands above the starting elevation or the sensor drifts
            f.write("Stopped logging; low altitude met. (" + str(bmp.altitude) + "m)\n")
            break

        if data_cycles >= log_stop_count:   # backup to the code above  
                f.write("Stopped logging; writes to file met. (" + str(data_cycles) + " writes) ")
                f.write("This means altitude code did not execute.\n")
                break

    
    data_cycles += 1 
    print("Data cycles: " + str(data_cycles)) # for debugging while editing code

    
#                          ------------------------ End of main data logging code ------------------------


while True:     # indicates that the data recording is done
    i = (i + 1) % 256  # run from 0 to 255
    led_dotstar.fill(colorwheel(i)) # Unicorn barf
    time.sleep(0.01)
"""while True:
    led_dotstar[0] = (255, 0, 0)
    time.sleep(0.5)
    led_dotstar[0] = (0, 255, 0)
    time.sleep(0.5)
    led_dotstar[0] = (0, 0, 255)
    time.sleep(0.5)"""