from digitalio import DigitalInOut
import time, busio, digitalio, board, neopixel, adafruit_rfm9x, microcontroller
"""
Authored by besser435
Created February 2023
Revised May 2023

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
version = "Autism Ray v1.2 (Rocket)"

# Underclock to save power. USB requires > 48MHz; boot into safe mode by pressing reset on power on in case this is too low.
microcontroller.cpu.frequency = 50_000_000
print(f"CPU frequency: {microcontroller.cpu.frequency}")

# LEDs
led_neo = neopixel.NeoPixel(board.NEOPIXEL, 1, brightness=0.3)
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
mute_beeper = 1
beeper = digitalio.DigitalInOut(board.D1) 
beeper.direction = digitalio.Direction.OUTPUT
def beep(state):
    if not mute_beeper:
        if not state:
            beeper.value = False
        elif state:
            beeper.value = True
    else:
        #led_neo.brightness = 0.01
        pass


def error(e):

    #https://discord.com/channels/914767468331929653/938696892659929109/1083860244003831829
    #add proper redundancy, see message above

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

        """
        TODO should really separate send_data by new lines. Currently I just parse this on the
        the ground station by converting it to a list and chopping off certain characters. Its hard coded, 
        and not dynamic to changing string lengths. For example, a different version number might bung 
        with the formatting on the OLED display if its a character too long or too short for example.
        
        New lines would fix this, as I could just parse for new lines, rather that set char counts in a list.
        """ 
        send_data = bytes(version + " Beacon Heartbeat: " + str(heartbeat) + "      \r\n","utf-8")
        rfm.send(send_data)
        print("Sent the message: " + str(send_data))

        time.sleep(0.2)
        led_neo.fill((0, 0, 0))
        beep(0)
        heartbeat += 1

        #alarm/sleep
            
    except Exception as e:
        error(e)
