from digitalio import DigitalInOut
import time, busio, digitalio, board, neopixel, adafruit_rfm9x, storage
import analogio, traceback

"""
Authored by besser435, March 2023

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
version = "Autism Ray v0.1 (Rocket)"

# I2C
i2c = busio.I2C(board.SCL, board.SDA)

# Neopixel
led_neo = neopixel.NeoPixel(board.NEOPIXEL, 1)



"""TODO Pin numbers are not set correctly."""


# RFM95
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
cs = digitalio.DigitalInOut(board.D18)
reset = digitalio.DigitalInOut(board.D19)
rfm9x = adafruit_rfm9x.RFM9x(spi, cs, reset, 915.0)
rfm9x.tx_power = 23
prev_packet = None

# Beeper
mute_beeper = 0
beeper = digitalio.DigitalInOut(board.D5) 
def beep(state):
    if mute_beeper == 0:
        if state == 0:
            beeper.value = True 
        elif state == 1:
            beeper.value = False


def error(e):
    print("Error occurred: \n")
    print(e)
    
    storage.remount("/", True)  # untested, might need to be set to False. just test it in general
    with open("error.txt", "a") as f: 
        f.write(e, "\n")

    for i in range(120):
        led_neo.fill((255, 0, 0))
        beeper(1)
        time.sleep(0.5)
        led_neo.fill((0, 0, 0))
        beeper(0)
        time.sleep(0.5)

    while True:
        send_data = bytes("Error occurred: \n" + str(e) + "\r\n","utf-8")
        rfm9x.send(send_data)
        print("Sent the message: " + send_data)
        time.sleep(1)


try:
    heartbeat = 0
    while True:
        time.sleep(0.5)
        led_neo.fill((255, 255, 255))
        beeper(1)

        send_data = bytes("AR Beacon. Heartbeat: " + str(heartbeat) + "\r\n","utf-8")
        rfm9x.send(send_data)
        print("Sent the message: " + send_data)

        time.sleep(0.5)
        led_neo.fill((0, 0, 0))
        beeper(0)
        heartbeat += 1
        

except OSError as e:
    error(e)
except Exception as e:
    error(e)

    