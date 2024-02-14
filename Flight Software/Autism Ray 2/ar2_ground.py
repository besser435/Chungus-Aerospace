from digitalio import DigitalInOut
#import time, busio, digitalio, board
#from digitalio import DigitalInOut, Direction, Pull
import traceback
# import RPi.GPIO as GPIO
# from gpiozero import CPUTemperature
from digi.xbee.devices import XBeeDevice
import time
import json

"""
NOTE: On chadpi, there is a cron job that runs this script on boot.
sh: crontab -e
@reboot python3 ~/Desktop/autism_ray_ground.py
"""

# Configuration
FILE_LOCATION = "/home/pi/Desktop/"



# Hardware setup
#xbee = XBeeDevice("/dev/ttyS0", 9600)

# Display


# import RPi.GPIO as GPIO

# GPIO.setmode(GPIO.BCM)  # Use Broadcom pin numbering
# GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # button_pin is the GPIO pin the button is connected to

# # Now, when you check the button state:
# button_state = GPIO.input(button_pin)
# # button_state will be False when pressed, True when not pressed.


#/dev/ttyAMA0
#/dev/ttyS0
xbee = XBeeDevice("COM7", 9600)
xbee.open()



# TODO send AK to see if Xbee is alive. if so do a beep sequence and update the display as a nice boot animation.
# maybe do this a few times while actively searching to ensure the connections are still alive.
# Maybe inpliment on the beacon. Should be a function.







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












def draw_screen(data: dict):
    pass


while True:
    try:
        message, rssi = get_message()


        if message is not None:
            print("Received: %s" % message)
            print("Last packet RSSI: -%d dBm" % rssi)
        else:
            print("No message received.")
            # add some sort of heartbeat to the GS to ensure its still searching

    except Exception as e:
        traceback.print_exc()
        break
        
    except KeyboardInterrupt:
        break












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
