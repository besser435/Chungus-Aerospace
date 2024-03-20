import busio
import digitalio
import time
import board
import neopixel
import adafruit_gps
import traceback

# Configuration
# BUG acts weird when blow 1
MESSAGE_SEND_RATE = 1   # Seconds between messages
UPDATE_RATE = 0    # Seconds between loop iterations


_FRAME_ID = 0x01
_DESTINATION_ADDRESS = "00:00:00:00:00:00:FF:FF"  # 64 bit address of the ground station. Or use broadcast address "00::FF:FF"
_BROADCAST_RADIUS = 0x00
_TRANSMIT_OPTIONS = 0x00

# Hardware setup
led_neo = neopixel.NeoPixel(board.NEOPIXEL, 1, brightness=0.2)

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

#TODO only show 5 decimal places for lat and long   
def get_gnss() -> dict:
    # The GPS library does not return all the minutes.
    # We need to manually add them together.    
    # The rest of the stuff is to avoid type errors from None values
    # TODO get rid of type fuckery. Keep the current types as they are, they work currently.
    latitude_int = int(gnss.latitude) if gnss.latitude is not None else 0
    latitude_minutes_str = str(gnss.latitude_minutes).replace(".", "") if gnss.latitude_minutes is not None else "0"

    longitude_int = int(gnss.longitude) if gnss.longitude is not None else 0
    longitude_minutes_str = str(gnss.longitude_minutes).replace(".", "") if gnss.longitude_minutes is not None else "0"

    altitude = int(gnss.altitude_m) if gnss.altitude_m is not None else 0
    height_geoid = gnss.height_geoid if gnss.height_geoid is not None else 0

    speed = int(gnss.speed_knots * 0.514444) if gnss.speed_knots is not None else 0

    time_utc = "{:02d}:{:02d}:{:02d}".format(gnss.timestamp_utc.tm_hour, gnss.timestamp_utc.tm_min, gnss.timestamp_utc.tm_sec) if gnss.timestamp_utc is not None else "0"

    satellites = gnss.satellites if gnss.satellites is not None else 0
    h_dilution = round(gnss.horizontal_dilution, 1) if gnss.horizontal_dilution is not None else 0
    #has_fix = "true" if gnss.has_fix is True else "false"   # JSON requires lowercase true and false
    fix_quality = gnss.fix_quality_3d if gnss.fix_quality_3d is not None else 0
    data = {
        "latitude": f"{latitude_int}.{latitude_minutes_str}",
        "longitude": f"{longitude_int}.{longitude_minutes_str}",

        "altitude": altitude,
        "height_geoid": height_geoid, 

        "speed": speed,

        "utc": time_utc,

        "satellites": satellites,
        "h_dilution": h_dilution,
        "fix_quality": fix_quality
    }

    return data


def format_message(message) -> str:
    """NOTE: Removes spaces from the message and adds a newline and carriage return to the end."""
    message = str(message)
    message = message.replace(" ", "")      # Remove spaces to bytes
    message = message.replace("'", "\"")    # JSON uses double quotes
    message += "\n\r"

    return message

# TODO ensure the frame isnt too long. It will get longer as the flight progresses, as speed, alt, and peak values increase
def generate_tx_request_frame(frame_id, destination_address, broadcast_radius, transmit_options, payload_data) -> bytes:
    """Generates a transmit request frame for an XBee in API 1 mode. Uses frame type 0x10.
    Raises a ValueError if the payload data is too long. The maximum length is 254 bytes."""
    # https://www.digi.com/resources/documentation/digidocs/pdfs/90002173.pdf#page=129&zoom=100,96,70

    start_delimiter = b"\x7E"

    frame_length = len(payload_data) + 14  # 14 bytes for fixed fields (excluding start delimiter, length, and checksum)

    frame_type = b"\x10"

    frame_id_byte = bytes([frame_id])

    destination_address_bytes = bytes.fromhex(destination_address.replace(":", ""))

    reserved = b"\xFF\xFE" # NOTE in XCTU this says it is the 16 bit address, but in the documentation it says it is reserved and should be set to 0xFFFE

    broadcast_radius_byte = bytes([broadcast_radius])

    transmit_options_byte = bytes([transmit_options])

    payload_data_bytes = str(payload_data).encode("ascii")  # kinda already done in frame_length, but whatever
    # TODO: dont rase value error, just send what we can. In the future, split the message into multiple frames.
    if len(payload_data_bytes) >= 254:
        raise ValueError(f"Payload data is too long. Maximum length is 254 bytes. Got: {len(payload_data_bytes)} bytes.")

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

    #print(f"Payload len: {len(payload_data_bytes)}, Total frame len: {frame_length}")
    #print(f"Generated frame. Checksum: {checksum}")

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
    "h_dilution": 0,
    "fix_quality": 0,
    
    "peak_speed": 0,
    "peak_alt": 0
}


last_update = time.monotonic()
while True:
    try:
        gnss.update()
        gnss_data = get_gnss()

        for key in telemetry.keys():
        # Do not overwrite existing key values, only update the key values that are present   
        # eg: if we had a location fix but lost it, dont overwrite the last known location with 0
        # get_gnss() returns 0 for a value if the fix is lost, so that will skip the conditional
            if key in gnss_data:
                telemetry[key] = gnss_data[key]


        if gnss_data.get("speed") > telemetry["peak_speed"]:
            telemetry["peak_speed"] = gnss_data.get("speed")

        if gnss_data.get("altitude") > telemetry["peak_alt"]:  # alt in m above earth ellipsoid
            telemetry["peak_alt"] = gnss_data.get("altitude")
    

        if telemetry["satellites"] < 4 or telemetry["fix_quality"] == 1:
            led_neo.fill((255, 0, 255))
        elif telemetry["satellites"] < 12:
            led_neo.fill((255, 255, 0))
        elif telemetry["satellites"] >= 12:
            led_neo.fill((0, 255, 0))


        if time.monotonic() - last_update >= MESSAGE_SEND_RATE:
            # Will reading fast adversely affect battery life?
            # TODO Test GPS, XBee, MCU, power sleep modes if not high enough, and only update every 10 seconds
            # see https://learn.adafruit.com/deep-sleep-with-circuitpython/alarms-and-sleep
            last_update = time.monotonic()

            # NOTE format and send the message
            message = format_message(telemetry)
            frame = generate_tx_request_frame(_FRAME_ID, _DESTINATION_ADDRESS, _BROADCAST_RADIUS, _TRANSMIT_OPTIONS, message)
            xbee_uart.write(frame)

            #print("Sent message")
            # message_bytes = ""
            # for byte in frame:
            #     message_bytes += "%02X " % byte
            # print(message_bytes)

        telemetry_print = "\n".join([f"{key}: {value}" for key, value in telemetry.items()]) # console flashes if we print too often
        print(telemetry_print + "\n\n")


        time.sleep(UPDATE_RATE)
    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        led_neo.fill((255, 0, 0))

        reset_xbee()
        time.sleep(1)
