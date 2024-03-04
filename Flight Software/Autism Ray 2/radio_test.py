
# import board
# import digitalio

# import traceback
# import time
# import json
# import random
# from digi.xbee.devices import XBeeDevice

# xbee_reset = digitalio.DigitalInOut(board.D26)
# def reset_xbee():
#     print("Resetting XBee...")
#     """ BUG XBee does not work without a reset.
#     See page 189. https://www.digi.com/resources/documentation/digidocs/pdfs/90002173.pdf"""
#     xbee_reset.direction = digitalio.Direction.OUTPUT
#     xbee_reset.value = False    # Drive low to reset
#     time.sleep(1)
#     xbee_reset.direction = digitalio.Direction.INPUT # Set as input (pulling high might cause damage the XBee)
#     time.sleep(1)
#     print("XBee reset complete.")
# reset_xbee()


# # /dev/ttyAMA0
# # /dev/ttyS0
# # /dev/serial0

# xbee = XBeeDevice("/dev/serial0", 9600)
# xbee.open()


# def get_message() -> tuple:
#     """Returns the message JSON and RSSI of the last received packet."""
#     print("Waiting for data in get_message()")
#     xbee_message = xbee.read_data(timeout=5)

#     # Get the RSSI value
#     rssi = xbee.get_parameter("DB")
#     rssi = int.from_bytes(rssi, byteorder='big')

#     if xbee_message is not None:
#         message_data = xbee_message.data.decode()

#         # Find the first newline or carriage return character to split the message
#         end_of_message = message_data.find('\n')
#         if end_of_message == -1:
#             end_of_message = message_data.find('\r')
        
#         if end_of_message != -1:
#             # Extract only the first message
#             message = message_data[:end_of_message]
#         else:
#             message = message_data

#         # # Convert the message to JSON
#         # try:
#         #     message_json = json.loads(message)
#         # except json.JSONDecodeError:
#         #     # Handle the case where the message cannot be converted to JSON
#         #     print(f"Received: {message}")
#         #     print("Error: Message is not in valid JSON format.")
#         #     return None, None

       
#         # return message_json, rssi
#         return message, rssi
#     else:
#         return None, None



def generate_transmit_request_frame(frame_id, destination_address, broadcast_radius, transmit_options, payload_data):
    # Start Delimiter
    start_delimiter = b'\x7E'

    # Calculate Frame Length
    frame_length = len(payload_data) + 14  # 14 bytes for fixed fields (excluding start delimiter, length, and checksum)

    # Frame Type
    frame_type = b'\x10'

    # Frame ID
    frame_id_byte = bytes([frame_id])

    # Destination Address
    destination_address_bytes = bytes.fromhex(destination_address.replace(':', ''))

    # Reserved Field
    reserved = b'\xFF\xFE' #NOTE reserved might be wrong, in XCTU is says 16 bit address, but in the documentation it says it is reserved and should be set to 0xFFFE

    # Broadcast Radius
    broadcast_radius_byte = bytes([broadcast_radius])

    # Transmit Options
    transmit_options_byte = bytes([transmit_options])

    # Payload Data
    payload_data_bytes = payload_data.encode('ascii')

    # Calculate Checksum
    checksum = 0xFF - (frame_type[0] + frame_id_byte[0] + sum(destination_address_bytes) + sum(reserved) + broadcast_radius_byte[0] + transmit_options_byte[0] + sum(payload_data_bytes)) & 0xFF

    # Construct the Frame
    frame = (
        start_delimiter +
        frame_length.to_bytes(2, byteorder='big') +
        frame_type +
        frame_id_byte +
        destination_address_bytes +
        reserved +
        broadcast_radius_byte +
        transmit_options_byte +
        payload_data_bytes +
        bytes([checksum])
    )

    return frame

# Example usage:
frame = generate_transmit_request_frame(0x01, '00:00:00:00:00:00:FF:FF', 0x00, 0x00, 'I will chung')
print(' '.join([format(byte, '02X') for byte in frame]))
# NOTE this was a GPT fuck
# TODO reserved might be wrong, in XCTU is says 16 bit address, but in the documentation it says it is reserved and should be set to 0xFFFE
# TODO ensure the data is being encoded as ASCII
# TODO ensure the length is being calculated correctly. docs say "Number of bytes between the length and checksum.", but the code just adds 14 for some reason