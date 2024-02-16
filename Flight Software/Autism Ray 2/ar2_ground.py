from digi.xbee.devices import XBeeDevice

import adafruit_ssd1306
from PIL import Image, ImageDraw, ImageFont
from gpiozero import TonalBuzzer
from gpiozero.tones import Tone
from gpiozero import Button

import board
import busio

import traceback
import time
import json

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
xbee = XBeeDevice("COM7", 9600)
xbee.open()

# Display
#pip3 install adafruit-circuitpython-ssd1306
i2c = busio.I2C(board.SCL, board.SDA)
oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)

# Buttons
sw1 = Button(17)
sw2 = Button(27)
sw3 = Button(22)

# Buzzer
buzzer = TonalBuzzer(21)
enable_buzzer = False




# TODO send AK to see if Xbee is alive. if so do a beep sequence and update the display as a nice boot animation.
# maybe do this a few times while actively searching to ensure the connections are still alive.
# Maybe implement on the beacon. Should be a function.


def boot():
    image = Image.new("1", (oled.width, oled.height))
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, oled.width, oled.height), outline=255, fill=255)

    font = ImageFont.load_default()
    text = "AR2"
    (font_width, font_height) = font.getsize(text)
    draw.text(
        (oled.width // 2 - font_width // 2, oled.height // 2 - font_height // 2),
        text,
        font=font,
        fill=255,
    )
    oled.image(image)
    oled.show()



    buzzer.play(Tone(1000))
    time.sleep(0.1)
    buzzer.play(Tone(400))
    time.sleep(0.1)
    buzzer.play(Tone(400))
    time.sleep(0.1)
    buzzer.stop()

    oled.fill(0)
    oled.show()
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


def get_message(data) -> tuple:
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
    pass


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








        if sw1.is_pressed: # Toggle buzzer mute
            enable_buzzer = not enable_buzzer
            if enable_buzzer:
                buzzer.stop()



            print("Toggled buzzer mute to: %s" % enable_buzzer)

        if sw2.is_pressed: # Toggle logging
            enable_logging = not enable_logging
            print("Toggled logging to: %s" % enable_logging)

        if sw3.is_pressed: # restart the script
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
