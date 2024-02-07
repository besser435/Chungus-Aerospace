from digitalio import DigitalInOut
#import time, busio, digitalio, board
#from digitalio import DigitalInOut, Direction, Pull
import traceback
# import RPi.GPIO as GPIO
# from gpiozero import CPUTemperature
from digi.xbee.devices import XBeeDevice
import time

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


# Button A
# btnA = DigitalInOut(board.D5)
# btnA.direction = Direction.INPUT
# btnA.pull = Pull.UP

# # Button B
# btnB = DigitalInOut(board.D6)
# btnB.direction = Direction.INPUT
# btnB.pull = Pull.UP



#         if not btnA.value:
#             beeper_toggle = not beeper_toggle
#             print("Beeper toggled: ", beeper_toggle)


# from digi.xbee.devices import XBeeDevice

# # Configure your device's serial port and baud rate
# xbee = XBeeDevice("COM7", 9600)
# try:
#     print("Waiting for data...\n")
#     xbee.open(force_settings=True)


#     while True:
#         xbee_message = xbee.read_data()
#         if xbee_message is not None:
#             print("Received: %s" % xbee_message.data.decode())
#             # After receiving, you might want to get the last RSSI
#             rssi = xbee.get_parameter("DB")
#             print("Last packet RSSI: -%d dBm" % int.from_bytes(rssi, byteorder='big'))
#             time.sleep(1)
# except KeyboardInterrupt:
#     pass
# finally:
#     if xbee is not None and xbee.is_open():
#         xbee.close()






xbee = XBeeDevice("COM7", 9600)
xbee.open()

def get_message() -> tuple:
    """Returns the message and RSSI of the last received packet."""

    xbee_message = xbee.read_data()
    rssi = xbee.get_parameter("DB")
    rssi = int.from_bytes(rssi, byteorder='big')

    if xbee_message is not None:
        return xbee_message.data.decode(), rssi
    else:
        return None, None



while True:
    try:
        message, rssi = get_message()


        if message is not None:
            print("Received: %s" % message)
            print("Last packet RSSI: -%d dBm" % rssi)
        else:
            print("No message received.")

    except Exception as e:
        traceback.print_exc()
        break
        
    except KeyboardInterrupt:
        pass




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
