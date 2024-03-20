import board
import digitalio

import traceback
import time
import json
import requests
from datetime import datetime
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

from digi.xbee.devices import XBeeDevice

from gpiozero import TonalBuzzer
from gpiozero.tones import Tone
from gpiozero import Button

from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306
from PIL import ImageFont


"""
NOTE: On chadpi, there is a cron job that runs this script on boot.
sh: crontab -e
@reboot python3 ~/Desktop/autism_ray_ground.py
"""

# Configuration
LOG_LOCATION = "/home/pi/Desktop/"
#OLED_INVERT = False # TODO

# Xbee
"""serial options on Pis include:
/dev/ttyAMA0
/dev/ttyS0
/dev/serial0
"""
xbee_reset = digitalio.DigitalInOut(board.D26)
def reset_xbee():
    print("Resetting XBee...")
    """ BUG XBee does not work without a reset.
    See page 189. https://www.digi.com/resources/documentation/digidocs/pdfs/90002173.pdf"""
    xbee_reset.direction = digitalio.Direction.OUTPUT
    xbee_reset.value = False    # Drive low to reset
    time.sleep(1)
    xbee_reset.direction = digitalio.Direction.INPUT # Set as input (pulling high might cause damage the XBee)
    time.sleep(1)   # Required
    print("XBee reset complete.")
xbee = XBeeDevice("/dev/serial0", 9600)

# Buttons
sw1 = Button(17)
sw2 = Button(27)
sw3 = Button(22)

# Buzzer
TonalBuzzer.max_tone = property(lambda self: Tone(4000))  # override default max of 880Hz
buzzer = TonalBuzzer(21)

# OLED
serial = i2c(port=1, address=0x3D)
oled = ssd1306(serial)
font_path = "droid-sans-mono.ttf"   # Use a monospace font
font_size = 10
font = ImageFont.truetype(font_path, size=font_size)

# Other stuff
enable_logging = True
enable_buzzer = False


def boot():
    font_path = "Ubuntu-Bold.ttf"   # Use a monospace font
    font_size = 60
    font = ImageFont.truetype(font_path, size=font_size)

    text_box = font.getbbox("AR2")
    text_width = text_box[2] - text_box[0]

    x = (oled.width - text_width) // 2
    y = ((oled.height - font_size) // 2) - 5

    with canvas(oled) as draw:
        draw.rectangle(oled.bounding_box, outline="white", fill="black")
        draw.text((x, y), text="AR2", fill="white", font=font)

    reset_xbee()
    xbee.open()     #TODO fix could not determine operating mode error


    buzzer.play(Tone(frequency=1200))
    time.sleep(0.1)
    buzzer.stop()
    time.sleep(0.1)

    buzzer.play(Tone(frequency=600))
    time.sleep(0.1)
    buzzer.stop()
    time.sleep(0.1)

    buzzer.play(Tone(frequency=600))
    time.sleep(0.1)
    buzzer.stop()
    time.sleep(0.1)
boot()


def api_send(data: dict):
    """Sends the data to a website so it can be easily viewable on a phone's map."""
    URL = "https://chugnus.space/api/ground_station"


def show_alert(message):
    # Alert font
    alert_font_path = "Ubuntu-Bold.ttf"
    alert_font_size = 22
    alert_font = ImageFont.truetype(alert_font_path, size=alert_font_size)

    # Message font, use a monospace one
    msg_font_path = "droid-sans-mono.ttf"
    msg_font_size = 14
    msg_font = ImageFont.truetype(msg_font_path, size=msg_font_size)

    oled_width_center = oled.width // 2

    # Alert box size and position
    alert_box_width = 60
    alert_box_height = 22
    alert_box_x = oled_width_center - (alert_box_width // 2)
    alert_box_y = 0

    # Alert Text positioning
    alert_text_x = alert_box_x + 3
    alert_text_y = alert_box_y - 2

    # Draw alert box and text
    with canvas(oled) as draw:
        _, _, text_width, _ = draw.textbbox((0, 0), message, font=msg_font)  # Calculate text width
        message_x = (oled.width - text_width) // 2  # Calculate x-coordinate for centering
        
        draw.rectangle((alert_box_x, alert_box_y, alert_box_x + alert_box_width, alert_box_y + alert_box_height), outline="white", fill="white")
        draw.text((alert_text_x, alert_text_y), "Alert", fill="black", align="center", font=alert_font)
        draw.text((message_x, alert_box_height), message, fill="white", align="center", font=msg_font)

        print(f"\n{message}\n")

    time.sleep(2)


def xbee_is_alive() -> bool:    # NOTE not implemented, but maybe should be tested periodically in the main loop
    """Returns True if the Xbee is alive, False if not. Tests the connection by sending a command to the Xbee and 
    checking if it returns an expected value"""
    
    hardware_series = xbee.get_parameter("HS")
    hardware_to_string = hardware_series.decode("ascii")
    
    print(hardware_to_string)
    print(f"Hardware is: {hardware_series} delete this debug line")

    if hardware_series is not None:
        return True
    else:
        return False


def get_message() -> tuple:
    """Returns a message as JSON, RSSI, and timestamp of the last received packet."""

    xbee_message = xbee.read_data()

    # Get RSSI from the message
    rssi = xbee.get_parameter("DB")
    rssi = -int.from_bytes(rssi, byteorder="big")

    if xbee_message is not None:
        message_data = xbee_message.data.decode()

        # Find the first newline or carriage return character to split the message
        end_of_message = message_data.find("\n")
        if end_of_message == -1:
            end_of_message = message_data.find("\r")
        
        if end_of_message != -1:
            # Extract only the first message
            message = message_data[:end_of_message]
        else:
            message = message_data

        pkt_timestamp = time.monotonic()


        # Convert the message to JSON
        try:
            message_json = json.loads(message)
        except json.JSONDecodeError:
            print("Error: Message is not in valid JSON format.")
            print(f"Received: {message}")
            return xbee_message, None, None
        return message_json, rssi, pkt_timestamp    # TODO message will not be logged on json decode error. Make sure it shows 
                                                    # shows up in error log as a partial message
    else:
        return None, None, None


def log_data(data: dict):
    """Logs GPS and RSSI data to a file in LOG_LOCATION if enable_logging is True."""
    if enable_logging:
        with open(LOG_LOCATION + "ar2_log.txt", "a") as f:
            f.write(str(data) + "\n")


def draw_screen(data: dict):
    """Updates the display with the data from the telemetry variable."""
    packet_age = data["packet_age"]
    if packet_age < 1000:
        packet_age = f"{packet_age:03}ms"
    elif packet_age < 60_000:
        packet_age = f"{packet_age // 1000}s!"
    elif packet_age < 3_600_000:
        packet_age = f"{packet_age // 60_000}m!"


    text_lines = [
        f"R: {data['rssi']}, S: {data['satellites']}, D: {data['h_dilution']}",
        f"P: {packet_age}, U: {data['utc']}",
        f"Lat: {data['latitude']}°",
        f"Lon: {data['longitude']}°",
        f"Alt: {data['altitude']}m, S: {data['speed']}m/s",
        f"PA: {data['peak_alt']}m, PS: {data['peak_speed']}m/s",
    ]

    with canvas(oled) as draw:
        for i, line in enumerate(text_lines):
            draw.text((0, i * 10), line, fill="white", font=font)


# TODO ask adafruit discord on why the beep sounds terrible. Probably some PWN issue.
# Maybe try on a different board like the RP2040
def rssi_to_hz(rssi) -> int:
    """Maps the RSSI value to a frequency in Hz for the buzzer"""
    rssi_min = -170
    rssi_max = -15
    freq_min = 250
    freq_max = 2000

    frequency = ((rssi - rssi_min) / (rssi_max - rssi_min)) * (freq_max - freq_min) + freq_min

    print(f"Freq: {int(frequency)}Hz, RSSI: {rssi}dBm")

    return int(frequency)


def generate_qr_code(data: dict):   # also print a link, and a tinyurl link if there is internet
    """Generates a QR code with a Google Maps link to the current beacon's location."""
    pass


telemetry = {
    # Values from the beacon
    "latitude": 0,
    "longitude": 0,

    "altitude": 0,

    "speed": 0,

    "utc": 0,

    "satellites": 0,
    "h_dilution": 0,
    "fix_quality": 0,
    
    "peak_speed": 0,
    "peak_alt": 0,

    # Metadata values from the ground
    "rssi": 0,
    "packet_age": 0
}


error_count = 0
last_pkt_time = 0
while True:
    try:
        message, rssi, pkt_timestamp = get_message()

        # TODO only logs if there is a fix. should it log if there is no fix?
        if message:
            if telemetry["satellites"] >= 4 or telemetry["fix_quality"] >= 2:    # Don't log if no fix. Only used on startup when values are 0 
                log_data(telemetry)

            for key, value in message.items():
                    telemetry[key] = value
            telemetry["rssi"] = rssi


            if enable_buzzer:
                freq = rssi_to_hz(rssi)
                buzzer.play(Tone(frequency=freq))
        else:
            pass
            buzzer.stop()
            # xbee_is_alive() # TODO test this periodically

        if pkt_timestamp:
            telemetry["packet_age"] = int((time.monotonic() - pkt_timestamp) * 1000)
            last_pkt_time = pkt_timestamp
        else:
            telemetry["packet_age"] = int((time.monotonic() - last_pkt_time) * 1000)
            

        draw_screen(telemetry)


        print("\n" * 2)
        print("\n".join([f"{key}: {value}" for key, value in telemetry.items()]))
        print(datetime.now())


        if sw1.is_pressed: # Toggle buzzer mute
            enable_buzzer = not enable_buzzer
            buzzer.stop()
            show_alert(f"Buzzer\n{'Enabled' if enable_buzzer else 'Disabled'}")
            
        if sw2.is_pressed: # Toggle logging
            enable_logging = not enable_logging
            buzzer.stop()
            show_alert(f"Logging\n{'Enabled' if enable_logging else 'Disabled'}")

        if sw3.is_pressed: # Cycle through display modes
            pass


        time.sleep(0.1)
    except Exception:
        print(traceback.format_exc())
        with open("ar2_error.txt", "a") as f: 
            f.write(f"{datetime.now()} (could be wrong if no internet)\n{traceback.format_exc()}")
            f.write("\n" * 2)

        error_count += 1
        if error_count > 10:
            # Prevents error file from getting too large, and also good practice kinda not really
            print("Too many errors, exiting...")
            break   # BUG wont run finally block
        
    except KeyboardInterrupt:
        break

    # NOTE finally will run after each loop iteration.
    # finally:
    #     buzzer.stop()
    #     print("Exiting...")
