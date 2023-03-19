from digitalio import DigitalInOut
import time, busio, digitalio, board, neopixel, adafruit_rfm9x
"""
Authored by besser435
Created February 2023
Revised March 2023

Autism Ray is Chungus Aerospace's system to locate a rocket
using LoRa 915MHz radios. Once the rocket lands, we will
scan the area for the radio beacon using a directional antenna.
We will keep moving the antenna back and forth until the signal
strength is the strongest. Then we will know what direction
to head in to find the rocket. Not sure if this will even work, 
but we might as well try.

This is the rocket code. It will broadcast the radio signal, and
will also beep for when we get close to finding it.
"""
version = "Autism Ray v1.0.1 (Rocket)"


"""TODO Pin numbers are not set correctly."""
# LEDs
led_neo = neopixel.NeoPixel(board.NEOPIXEL, 1, brightness=1)
led = digitalio.DigitalInOut(board.LED_GREEN)
led.direction = digitalio.Direction.OUTPUT
led.value = True


# RFM95
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
cs = digitalio.DigitalInOut(board.D7)
reset = digitalio.DigitalInOut(board.D0)
rfm = adafruit_rfm9x.RFM9x(spi, cs, reset, 900.0) # NOTE 900MHz
rfm.tx_power = 23
prev_packet = None

# Beeper
mute_beeper = 0
beeper = digitalio.DigitalInOut(board.D1) 
beeper.direction = digitalio.Direction.OUTPUT
def beep(state):
    if mute_beeper == 0:
        if state == 0:
            beeper.value = True 
        elif state == 1:
            beeper.value = False
    else:
        led_neo.brightness = 0.01


def error(e):
    print("Error occurred: \n", e)
    
    for i in range(120):    # wait 2 minutes for the issue to magically disappear before trying one last time
        led_neo.fill((255, 0, 0))
        beep(1)
        time.sleep(0.5)
        led_neo.fill((0, 0, 0))
        beep(0)
        time.sleep(0.5)

        print("Error, will try again when i is 120. i = " + str(i))

    while True:
        send_data = bytes("Error occurred: \n" + e + "\r\n","utf-8")
        rfm.send(send_data)
        print("Sent the message: " + str(send_data))
        time.sleep(1)

heartbeat = 0
while True:
    try:
        time.sleep(0.2)
        led_neo.fill((255, 255, 255))
        beep(1)

        send_data = bytes(version + " Beacon. Heartbeat: " + str(heartbeat) + "\r\n","utf-8")
        rfm.send(send_data)
        print("Sent the message: " + str(send_data))

        time.sleep(0.2)
        led_neo.fill((0, 0, 0))
        beep(0)
        heartbeat += 1
            
    except Exception as e:
        error(e)
