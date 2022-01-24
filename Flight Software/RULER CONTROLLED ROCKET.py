"""
This is the flight software for the Adafruit Ruler
https://www.adafruit.com/product/4319

Its a stupid idea to control a rocket with a ruler,
but its too good to pass up. This code needs to be
simple as the ruler doesnt have a lot of storage 
or RAM.


"""
version = "v0.1"

import time
import board
import touchio
import adafruit_dotstar
from rainbowio import colorwheel
import digitalio
     
# Setup
# LED for capacitive button setup
led4 = digitalio.DigitalInOut(board.LED4)   # Ω
led4.direction = digitalio.Direction.OUTPUT    

led5 = digitalio.DigitalInOut(board.LED5)   # µ
led5.direction = digitalio.Direction.OUTPUT

led6 = digitalio.DigitalInOut(board.LED6)   # µ
led6.direction = digitalio.Direction.OUTPUT

led7 = digitalio.DigitalInOut(board.LED7)   # Digikey
led7.direction = digitalio.Direction.OUTPUT

# RGB Goodness
led_dotstar = adafruit_dotstar.DotStar(board.APA102_SCK, board.APA102_MOSI, 1)

# Motor ignition relay
motor_relay = digitalio.DigitalInOut(board.A0)  # NOTE change this pin to whatever pin is good. 
motor_relay.direction = digitalio.Direction.OUTPUT

# ------------------------- options ------------------------
launch_delay = 2
led_dotstar.brightness = 0.1

# storage
#STARTING_ALTITUDE = bmp.altitude
motor_lit = 0





# broken cap code
touch_pad0 = board.CAP0
touch_pad1 = board.CAP1
touch_pad2 = board.CAP2
touch_pad3 = board.CAP3

touch = touchio.TouchIn(touch_pad2)

touch_count = 0
"""while True:
    led7.value = False
    if touch.value:
        print("Touched! " + str(touch_count))
        touch_count += 1
        led7.value = True
    time.sleep(0.1)
"""


#if two caps pressed for 3 seconds:
for i in range(launch_delay):   # countdown
    led_dotstar[0] = (255, 255, 0)
    time.sleep(0.5)
    led_dotstar[0] = (0, 0, 0)
    time.sleep(0.5)


for i in range (3):             # motor ignition (loops to ensure it happens)
    time.sleep(0.3)
    motor_relay.value = True
    time.sleep(0.5)
    motor_relay.value = False









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