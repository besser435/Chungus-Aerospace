from digi.xbee.devices import XBeeDevice

import displayio
import terminalio
from adafruit_display_text import label
import adafruit_displayio_ssd1306

from gpiozero import TonalBuzzer
from gpiozero.tones import Tone
from gpiozero import Button

import board

import traceback
import time
import json
import random

"""
NOTE: On chadpi, there is a cron job that runs this script on boot.
sh: crontab -e
@reboot python3 ~/Desktop/autism_ray_ground.py
"""

# Configuration
LOG_LOCATION = "/home/pi/Desktop/"
enable_logging = False


# XBee
#/dev/ttyAMA0
#/dev/ttyS0
#xbee = XBeeDevice("/dev/ttyS0", 9600)
#xbee.open()

# Display
i2c = board.I2C()
oled_reset = board.D9
display_bus = displayio.I2CDisplay(i2c, device_address=0x3D, reset=oled_reset)

WIDTH = 128
HEIGHT = 64

display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=WIDTH, height=HEIGHT)

background_bitmap = displayio.Bitmap(WIDTH, HEIGHT, 1)
background_palette = displayio.Palette(1)
background_palette[0] = 0xfffff #0x000000
background_sprite = displayio.TileGrid(background_bitmap, pixel_shader=background_palette)
splash = displayio.Group()
splash.append(background_sprite)
display.root_group = splash

text_labels = []
for i in range(6):
    text_area = label.Label(terminalio.FONT, text='', color=0x000000, x=1, y=5 + i*10)  #0xfffff
    splash.append(text_area)
    text_labels.append(text_area)


# Buttons
sw1 = Button(17)
sw2 = Button(27)
sw3 = Button(22)

# Buzzer
TonalBuzzer.max_tone = property(lambda self: Tone(4000))  # override default max of 880Hz
buzzer = TonalBuzzer(21)
enable_buzzer = False




# TODO send AK to see if Xbee is alive. if so do a beep sequence and update the display as a nice boot animation.
# maybe do this a few times while actively searching to ensure the connections are still alive.
# Maybe implement on the beacon. Should be a function.


def boot():
    buzzer.play(Tone(frequency=800))
    time.sleep(0.1)
    buzzer.stop()
    time.sleep(0.2)

    buzzer.play(Tone(frequency=400))
    time.sleep(0.1)
    buzzer.stop()
    time.sleep(0.2)

    buzzer.play(Tone(frequency=400))
    time.sleep(0.1)
    buzzer.stop()
    time.sleep(0.2)
boot()



def xbee_is_alive() -> bool:
    """Returns True if the Xbee is alive, False if not. Tests the connection by sending a command to the Xbee and 
    checking if it returns a value."""
    
    hardware_series = xbee.get_parameter("HS")
    hardware_to_string = hardware_series.decode("utf-8")
    
    print(hardware_to_string)
    print(f"Hardware is: {hardware_series} delete this debug line")

    if hardware_series is not None:
        return True
    else:
        return False


def get_message() -> tuple:
    """Returns the message JSON and RSSI of the last received packet.
    TODO should maybe read in main loop, then pass that to this function"""

    xbee_message = xbee.read_data()


    # Get the RSSI value
    rssi = xbee.get_parameter("DB")
    rssi = int.from_bytes(rssi, byteorder='big')

    if xbee_message is not None:
        message_data = xbee_message.data.decode()

        # Find the first newline or carriage return character to split the message
        end_of_message = message_data.find('\n')
        if end_of_message == -1:
            end_of_message = message_data.find('\r')
        
        if end_of_message != -1:
            # Extract only the first message
            message = message_data[:end_of_message]
        else:
            message = message_data

        # Convert the message to JSON
        try:
            message_json = json.loads(message)
        except json.JSONDecodeError:
            # Handle the case where the message cannot be converted to JSON
            print(f"Received: {message}")
            print("Error: Message is not in valid JSON format.")
            return None, None

       
        return message_json, rssi
    else:
        return None, None


def log_data(data: dict):
    """Logs GPS and RSSI data to a file."""
    if enable_logging:
        with open(LOG_LOCATION + "ar2_ground_log.txt", "a") as f:
            f.write(json.dumps(data) + "\n")


def draw_screen(data: dict):
    """Updates the display with the data from the beacon."""
    packet_age = data["packet_age"]
    if packet_age < 1000:
        packet_age = f"{packet_age}ms"
    elif packet_age < 60000:
        packet_age = f"{packet_age // 1000}s!"
    elif packet_age < 3600000:
        packet_age = f"{packet_age // 60000}m!"

    print(data)
    text_lines = [
        f"RSSI: {data['rssi']},  Sats: {data['sats']}",
        f"P: {packet_age}, U: {data['utc']}",
        f"Lat: {data['lat']}",
        f"Lon: {data['lon']}",
        f"Alt: {data['alt']}m",
        f"PA: {data['peak_alt']}m, PS: {data['peak_speed']}m/s",
    ]

    for label, new_text in zip(text_labels, text_lines):
        label.text = new_text



data = {
    "rssi": -random.randint(0, 100),
    "sats": random.randint(3, 20),
    "packet_age": 420,
    "lat": 72.145265,
    "lon": 0,
    "alt": 0,
    "utc": "20:24:58",
    "peak_alt": 1568,
    "peak_speed": 500
}




while True:
    try:
        message, rssi = get_message()

        if message is not None:
            print("Received: %s" % message)
            print("Last packet RSSI: -%d dBm" % rssi)
            buzzer_freq = 2**(rssi / 20) * 10000
            buzzer.play(Tone(frequency=buzzer_freq))
            print("Buzzer frequency: %d" % buzzer_freq)
        else:
            print("No message received.")
            buzzer.stop()
            # add some sort of heartbeat to the GS to ensure its still searching


        draw_screen(data)





        if sw1.is_pressed: # Toggle buzzer mute
            enable_buzzer = not enable_buzzer
            if enable_buzzer:
                buzzer.stop()



            print("Toggled buzzer mute to: %s" % enable_buzzer)

        if sw2.is_pressed: # Toggle logging
            enable_logging = not enable_logging
            print("Toggled logging to: %s" % enable_logging)

        if sw3.is_pressed: # Cycle through display modes
            pass



    except Exception as e:
        traceback.print_exc()
        
    except KeyboardInterrupt:
        buzzer.stop()












"""NOTE Pyserial implementation incase of issues with digi.xbee"""
# import serial
# #with serial.Serial("COM7", 9600, timeout=0.1) as xbee:
# xbee = serial.Serial("COM7", 9600, timeout=0.1)

# i = 0
# while True:
#     i += 1
#     print(i)

#     # BUG if the beacon sends too many packets, the ground station will read them all at once
#     xbee_message = xbee.readline()
#     xbee_message = xbee_message.decode("utf-8")
#     xbee_message = None if xbee_message == "" else xbee_message # If the message is empty, set it to None



#     if xbee_message is not None:
#         print(f"Received: {xbee_message}")
#         time.sleep(1)
#     else:
#         print("No message received.")

#     # else:
#     #     print("No message received.")
