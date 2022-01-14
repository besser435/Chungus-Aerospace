"""
NOTE
---Chungus Aerospace Program---
https://github.com/besser435/Chungus-Aerospace

This is used to test ignition for the parachute charge.
The code used is similar to what is used in the real code, that
way bugs can hopefully be duplicated and discovered. Its not
a perfect copy, but it kind of works. Thats why there is some
code that isnt really needed here.
"""

version = "v1.0"
date = "January 2022"


import time
import board
import digitalio
import neopixel


# Setup Bits
# LED pins and setup
led_neo = neopixel.NeoPixel(board.NEOPIXEL, 1)        
led_neo.brightness = 1

# Relay to deploy chute
chute_relay = digitalio.DigitalInOut(board.A1)  # NOTE change this pin to whatever pin is good. 
chute_relay.direction = digitalio.Direction.OUTPUT

# storage
chute_armed = 0


def main():
    global chute_armed

    for x in range(10):
        led_neo[0] = (255, 255, 0)
        time.sleep(0.5)
        led_neo[0] = (0, 0, 0)
        time.sleep(0.5)
    

    chute_armed += 1
    if chute_armed == 1:
        for x in range(3):  # to ensure ignition
            chute_relay.value = True
            print("Relay on")
            led_neo[0] = (0, 0, 255)
            time.sleep(0.5) # on for 0.5 seconds

            led_neo[0] = (0, 0, 0)
            chute_relay.value = False
            print("Relay off")
            time.sleep(0.5) # delay between turning off and then on again
            
    led_neo[0] = (0, 255, 0)
    time.sleep(3)
                
main()


""" Main code used in the flight computer firmware

if bmp.altitude >= (STARTING_ALTITUDE + 50):  # arms at 50 meters. idk if the parenthisis are needed. ill try with and without
        if chute_armed == 0: # this is so the event isnt logged repeatedly
            f.write("Armed parachute. Current alt: " + str(bmp.altitude) + "\n")
            chute_armed += 1

    if chute_armed == 1:
        if bmp.altitude <= STARTING_ALTITUDE + 49:  # once the rocket sinks below 50 meters it fires the chute
            for x in range(3):  # to ensure ignition
                chute_relay.value = True
                time.sleep(0.5)
                chute_relay.value = False
                time.sleep(0.5)

            if logged_chute_deploy == 0:
                f.write("Deployed parachute. Current alt: " + str(bmp.altitude) + "\n")
                logged_chute_deploy +=1
"""