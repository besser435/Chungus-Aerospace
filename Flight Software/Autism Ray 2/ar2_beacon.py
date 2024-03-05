import busio
import digitalio
import time
import board
import neopixel
import adafruit_gps
import traceback
from datetime import datetime

# Configuration
# BUG acts weird when blow 1
MESSAGE_SEND_RATE = 1   # Seconds between messages
UPDATE_RATE = 0.5    # Seconds between loop iterations


_FRAME_ID = 0x01
_DESTINATION_ADDRESS = "00:00:00:00:00:00:FF:FF"  # 64 bit XBee address of the ground station. Or use broadcast address "00..FF:FF"
_BROADCAST_RADIUS = 0x00
_TRANSMIT_OPTIONS = 0x00

# Hardware setup
led_neo = neopixel.NeoPixel(board.NEOPIXEL, 1, brightness=0.3)

# https://learn.adafruit.com/todbot-circuitpython-tricks/i2c
# NOTE On Rev 2 and later, UART is properly connected (broken on R1), but I2C might be better. 
#gnss_uart = busio.UART(board.MISO, board.MOSI, baudrate=9600)
i2c = busio.I2C(board.SCL, board.SDA, frequency=400_000)    # SAM M10Q requires 400kHz
gnss = adafruit_gps.GPS_GtopI2C(i2c, debug=False, address=0x42)   # 0x42 is the default SAM M10Q address

xbee_reset = digitalio.DigitalInOut(board.D3)
xbee_uart = busio.UART(board.TX, board.RX, baudrate=9600)


def reset_xbee():
    """ BUG XBee does not work without a reset.
    See page 189. https://www.digi.com/resources/documentation/digidocs/pdfs/90002173.pdf"""
    print("Resetting XBee...")

    xbee_reset.direction = digitalio.Direction.OUTPUT
    xbee_reset.value = False    # Drive low to reset
    time.sleep(1)
    xbee_reset.direction = digitalio.Direction.INPUT # Set as input (pulling high might cause damage the XBee)
reset_xbee()


def get_gnss() -> dict:
    # The GPS library does not return all the minutes.
    # We need to manually add them together.    
    # The rest of the stuff is to avoid type errors from None values
    # TODO get rid of type fuckery. Keep the current types as they are, they work currently.
    latitude_int = int(gnss.latitude) if gnss.latitude is not None else 0
    latitude_minutes_str = str(gnss.latitude_minutes).replace(".", "") if gnss.latitude_minutes is not None else "0"

    longitude_int = int(gnss.longitude) if gnss.longitude is not None else 0
    longitude_minutes_str = str(gnss.longitude_minutes).replace(".", "") if gnss.longitude_minutes is not None else "0"

    altitude = gnss.altitude_m if gnss.altitude_m is not None else 0
    height_geoid = gnss.height_geoid if gnss.height_geoid is not None else 0

    speed = gnss.speed_knots if gnss.speed_knots is not None else 0

    #utc = str(gnss.timestamp_utc) if gnss.timestamp_utc is not None else 0
    time_utc = gnss.timestamp_utc.strftime("%H:%M:%S") if gnss.timestamp_utc is not None else 0

    satellites = gnss.satellites if gnss.satellites is not None else 0
    #has_fix = "true" if gnss.has_fix is not None else "false"   # JSON requires lowercase true and false # NOTE old line, may have caused a bug
    has_fix = "true" if gnss.has_fix is True else "false"   # JSON requires lowercase true and false
    print(f"has_fix (still broken): {gnss.has_fix}")

    data = {
        "latitude": f"{latitude_int}.{latitude_minutes_str}",
        "longitude": f"{longitude_int}.{longitude_minutes_str}",

        "altitude": altitude,
        "height_geoid": height_geoid, 

        "speed": speed,

        "utc": time_utc,

        "satellites": satellites,
        "has_fix": has_fix
    }

    return data


def format_message(message) -> str:
    """NOTE: Removes spaces from the message and adds a newline and carriage return to the end."""
    message = str(message)
    message = message.replace(" ", "")      # Remove spaces to bytes
    message = message.replace("'", "\"")    # JSON uses double quotes
    message += "\n\r"
    print(message)
    return message


def generate_tx_request_frame(frame_id, destination_address, broadcast_radius, transmit_options, payload_data) -> bytes:
    """Generates a transmit request frame for an XBee in API 1 mode. Uses frame type 0x10.
    Raises a ValueError if the payload data is too long. The maximum length is 254 bytes."""
    # https://www.digi.com/resources/documentation/digidocs/pdfs/90002173.pdf#page=129&zoom=100,96,70

    encoded_message = message.encode('ascii')  # Encode the message to ASCII bytes
    if len(encoded_message) >= 254:
        raise ValueError("Payload data is too long. Maximum length is 254 bytes.")

    start_delimiter = b"\x7E"

    frame_length = len(payload_data) + 14  # 14 bytes for fixed fields (excluding start delimiter, length, and checksum)

    frame_type = b"\x10"

    frame_id_byte = bytes([frame_id])

    destination_address_bytes = bytes.fromhex(destination_address.replace(":", ""))

    reserved = b"\xFF\xFE" # NOTE in XCTU this says it is the 16 bit address, but in the documentation it says it is reserved and should be set to 0xFFFE

    broadcast_radius_byte = bytes([broadcast_radius])

    transmit_options_byte = bytes([transmit_options])

    payload_data_bytes = str(payload_data).encode("ascii")

    checksum = 0xFF - (frame_type[0] + frame_id_byte[0] + sum(destination_address_bytes) + sum(reserved) + broadcast_radius_byte[0] + transmit_options_byte[0] + sum(payload_data_bytes)) & 0xFF


    frame = (
        start_delimiter +
        frame_length.to_bytes(2, "big") +
        frame_type +
        frame_id_byte +
        destination_address_bytes +
        reserved +
        broadcast_radius_byte +
        transmit_options_byte +
        payload_data_bytes +
        bytes([checksum])
    )
    print(f"checksum: {checksum}")

    return frame


def send_status() -> bytearray:
    """Checks if the XBee sent the message successfully. Returns the status code."""
    # TODO Implement this
    return False

# Outside of loop as to not reset values. 
# We dont want to reset them incase we loose a GNSS fix.
telemetry = {   
    "latitude": 0,
    "longitude": 0,

    "altitude": 0,
    "height_geoid": 0,

    "speed": 0,

    "utc": 0,

    "satellites": 0,
    "has_fix": 0,
    
    "peak_speed_kts": 0,
    "peak_alt_m": 0
}


last_update = time.monotonic()
while True:
    try:
        # NOTE Update telemetry data from GNSS data
        gnss.update()
        gnss_data = get_gnss()
        for key in telemetry.keys():
        # Do not overwrite existing key values, only update the key values that are present   
            if key in gnss_data:
                telemetry[key] = gnss_data[key]


        # NOTE Update peak values. Keep in mind they are not very accurate
        if gnss_data.get("speed") > telemetry["peak_speed_kts"]:
            # Convert to m/s on the ground with round(float(telemetry["peak_speed_kts"] * 0.514444), 3)
            # We dont do that here, because we want to keep the peak speed in knots to be consistent with the GNSS data
            telemetry["peak_speed_kts"] = gnss_data.get("speed")

        if gnss_data.get("altitude") > telemetry["peak_alt_m"]:  # alt in m above earth ellipsoid
            telemetry["peak_alt_m"] = gnss_data.get("altitude")
    

        # NOTE Update LED status
        if telemetry["satellites"] < 4 or telemetry["has_fix"] == False:
            led_neo.fill((255, 0, 255))
        elif telemetry["satellites"] < 12:
            led_neo.fill((255, 255, 0))
        elif telemetry["satellites"] >= 12:
            led_neo.fill((0, 255, 0))


        # NOTE update as often as configured
        if time.monotonic() - last_update >= MESSAGE_SEND_RATE:
            # Will reading fast adversely affect battery life?
            # TODO Test GPS, XBee, MCU, power sleep modes if not high enough, and only update every 10 seconds
            # see https://learn.adafruit.com/deep-sleep-with-circuitpython/alarms-and-sleep
            last_update = time.monotonic()

            # NOTE format and send the message
            message = format_message(telemetry)
            frame = generate_tx_request_frame(_FRAME_ID, _DESTINATION_ADDRESS, _BROADCAST_RADIUS, _TRANSMIT_OPTIONS, message)
            xbee_uart.write(frame)
            
            # print each byte of the frame, keep it compatible with circuitpython
            message_bytes = ""
            for byte in frame:
                message_bytes += "%02X " % byte
            print(message_bytes)
                        

            
        # NOTE Debugging
        for data in telemetry.items():
            print(f"{data[0]}: {data[1]}")
        print("\n" * 2)
        time.sleep(UPDATE_RATE)

    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        led_neo.fill((255, 0, 0))

        reset_xbee()
        time.sleep(1)
