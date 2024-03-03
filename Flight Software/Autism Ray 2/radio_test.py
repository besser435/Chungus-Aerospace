
import board
import digitalio

import traceback
import time
import json
import random
from digi.xbee.devices import XBeeDevice

xbee_reset = digitalio.DigitalInOut(board.D26)
def reset_xbee():
    print("Resetting XBee...")
    """ BUG XBee does not work without a reset.
    See page 189. https://www.digi.com/resources/documentation/digidocs/pdfs/90002173.pdf"""
    xbee_reset.direction = digitalio.Direction.OUTPUT
    xbee_reset.value = False    # Drive low to reset
    time.sleep(1)
    xbee_reset.direction = digitalio.Direction.INPUT # Set as input (pulling high might cause damage the XBee)
    time.sleep(1)
    print("XBee reset complete.")
reset_xbee()


# /dev/ttyAMA0
# /dev/ttyS0
# /dev/serial0

xbee = XBeeDevice("/dev/serial0", 9600)
xbee.open()


def get_message() -> tuple:
    """Returns the message JSON and RSSI of the last received packet."""
    print("Waiting for data in get_message()")
    xbee_message = xbee.read_data(timeout=5)

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

        # # Convert the message to JSON
        # try:
        #     message_json = json.loads(message)
        # except json.JSONDecodeError:
        #     # Handle the case where the message cannot be converted to JSON
        #     print(f"Received: {message}")
        #     print("Error: Message is not in valid JSON format.")
        #     return None, None

       
        # return message_json, rssi
        return message, rssi
    else:
        return None, None



# import serial
# xbee = serial.Serial("/dev/ttyS0", 9600, timeout=2)


# def get_message_ser():
#     """Returns the message JSON and RSSI of the last received packet."""
#     xbee_message = xbee.readline()
    
#     if len(xbee_message) > 2:
#         # convert to string
#         xbee_message = xbee_message.decode("utf-8")

#         # remove newline and carriage return
#         xbee_message = xbee_message.replace("\n", "")
#         xbee_message = xbee_message.replace("\r", "")
#         xbee_message = json.loads(xbee_message)
#         return xbee_message  
#     else:
#         return None  






#read raw serial data after circuitpy ar2_test. maybe the xctu softare didnt see manual packets

while True:
    print(f"{get_message()}")
    print("\n" * 7)