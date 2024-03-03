
import busio
import digitalio
import time
import board

#xbee_reset = digitalio.DigitalInOut(board.D3)
#xbee_uart = busio.UART(board.TX, board.RX, baudrate=9600)


# while True:
#     xbee_reset.direction = digitalio.Direction.OUTPUT # Set as output
#     xbee_reset.value = False    # Drive low to reset
#     time.sleep(1)
#     xbee_reset.direction = digitalio.Direction.INPUT # Set as input (pulling high might cause damage the XBee)
    
#     print("Waiting for data...")
#     data = xbee_uart.read(64)
#     if data is not None:
#         print(f"Received: {data}")
#     else:
#         print("Received nothing!")









xbee_reset = digitalio.DigitalInOut(board.D3)
def reset_xbee():
    """ BUG XBee does not work without a reset.
    See page 189. https://www.digi.com/resources/documentation/digidocs/pdfs/90002173.pdf"""
    print("Resetting XBee...")

    xbee_reset.direction = digitalio.Direction.OUTPUT
    xbee_reset.value = False    # Drive low to reset
    time.sleep(1)
    xbee_reset.direction = digitalio.Direction.INPUT # Set as input (pulling high might cause damage the XBee)
    time.sleep(1)
    print("XBee reset complete.")



reset_xbee()

import board
import busio

# Configure UART
uart = busio.UART(board.TX, board.RX, baudrate=9600)

# Construct the XBee API frame (example)
frame_data = [0x7E, 0x00, 0x12, 0x10, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xFF, 0xFF, 0xFF, 0xFE, 0x00, 0x00, 0x74, 0x65, 0x73, 0x74, 0x33]

uart.write(bytearray(frame_data))
print(f"wrote {frame_data}")

while True:
    data = uart.read(128)
    if data is not None:
        print(f"Received: {data}")
    else:
        print("Received nothing!")