import board
import digitalio
import storage
import neopixel
import time
led_neo = neopixel.NeoPixel(board.NEOPIXEL, 1)

switch = digitalio.DigitalInOut(board.D13) # 
switch.direction = digitalio.Direction.INPUT
switch.pull = digitalio.Pull.UP


en_pin = digitalio.DigitalInOut(board.D5)
en_pin.direction = digitalio.Direction.OUTPUT
#pin = digitalio.DigitalInOut(board.D13)

# If D13 (board 11) is pulled high with D5 (board 33) CircuitPython can write to the drive
storage.remount("/", switch.value)

# if the write test is successful, the LED
try:
    with open("write_test.csv", "a") as f: 
        f.write("write success poggers\n")
    led_neo[0] = (0, 255, 0)
    time.sleep(1)
        
except Exception:
    led_neo[0] = (255, 0, 0)
    time.sleep(1)