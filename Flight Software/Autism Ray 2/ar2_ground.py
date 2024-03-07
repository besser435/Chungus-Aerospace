import board
import digitalio

import traceback
import time
import json
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
    time.sleep(1)
    print("XBee reset complete.")
reset_xbee()
xbee = XBeeDevice("/dev/serial0", 9600)
xbee.open()

# Buttons
sw1 = Button(17)
sw2 = Button(27)
sw3 = Button(22)

# Buzzer
TonalBuzzer.max_tone = property(lambda self: Tone(4000))  # override default max of 880Hz
buzzer = TonalBuzzer(21)
enable_buzzer = False

# OLED
serial = i2c(port=1, address=0x3D)
oled = ssd1306(serial)
font_path = "droid-sans-mono.ttf"
font_size = 10
font = ImageFont.truetype(font_path, size=font_size)  # Specify the path to your font file and the font size


# Other stuff
enable_logging = True


# TODO send AK to see if Xbee is alive. if so do a beep sequence and update the display as a nice boot animation.
# maybe do this a few times while actively searching to ensure the connections are still alive.
# Maybe implement on the beacon. Should be a function.


def boot():
    # Use a monospace font
    font_path = "Ubuntu-Bold.ttf"
    font_size = 60
    font = ImageFont.truetype(font_path, size=font_size)

    text_box = font.getbbox("AR2")
    text_width = text_box[2] - text_box[0]

    x = (oled.width - text_width) // 2
    y = ((oled.height - font_size) // 2) - 5

    from luma.core.sprite_system import framerate_regulator
    regulator = framerate_regulator(fps=5)
    with regulator:
        with canvas(oled) as draw:
            draw.rectangle(oled.bounding_box, outline="white", fill="black")
            draw.text((x, y), text="AR2", fill="white", font=font)
    time.sleep(1)


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
boot()


def xbee_is_alive() -> bool:
    """Returns True if the Xbee is alive, False if not. Tests the connection by sending a command to the Xbee and 
    checking if it returns a value"""
    
    hardware_series = xbee.get_parameter("HS")
    hardware_to_string = hardware_series.decode("ascii")
    
    print(hardware_to_string)
    print(f"Hardware is: {hardware_series} delete this debug line")

    if hardware_series is not None:
        return True
    else:
        return False


def get_message() -> tuple:
    """Returns the message JSON and RSSI of the last received packet."""

    xbee_message = xbee.read_data()

    # Get RSSI from the message
    rssi = xbee.get_parameter("DB")
    rssi = -int.from_bytes(rssi, byteorder='big')

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

        pkt_timestamp = time.monotonic()


        # Convert the message to JSON
        try:
            message_json = json.loads(message)
        except json.JSONDecodeError:
            # Handle the case where the message cannot be converted to JSON
            print("Error: Message is not in valid JSON format.")
            print(f"Received: {message}")
            return xbee_message, None, None
        return message_json, rssi, pkt_timestamp
    else:
        return None, None, None


def log_data(data: dict):
    """Logs GPS and RSSI data to a file in LOG_LOCATION if enable_logging is True."""
    if enable_logging:
        with open(LOG_LOCATION + "ar2_log.txt", "a") as f:
            f.write(json.dumps(data) + "\n")


def draw_screen(data: dict):
    """Updates the display with the data from the telemetry variable."""
    packet_age = data["packet_age"]
    if packet_age < 1000:
        packet_age = f"{packet_age}ms"
    elif packet_age < 60000:
        packet_age = f"{packet_age // 1000}s!"
    elif packet_age < 3600000:
        packet_age = f"{packet_age // 60000}m!"

    text_lines = [
        f"R: {data['rssi']}, S: {data['satellites']}, D: {data['h_dilution']}",
        f"P: {data['packet_age']}ms, U: {data['utc']}",
        f"Lat: {data['latitude']}°",
        f"Lon: {data['longitude']}°",
        f"Alt: {data['altitude']}m, S: {data['speed']}kts",
        f"PA: {data['peak_alt_m']}m, PS: {data['peak_speed_kts']}kts",
    ]

    with canvas(oled) as draw:
        for i, line in enumerate(text_lines):
            draw.text((0, i * 10), line, fill="white", font=font)

        
        draw.line((3, 22, 120, 22), fill="white")   # Health separator 
        draw.line((3, 42, 120, 42), fill="white")   # Position separator


def rssi_to_hz(rssi) -> int:
    """Maps the RSSI value to a frequency in Hz for the buzzer"""
    rssi_min = -170
    rssi_max = -15
    freq_min = 250
    freq_max = 2000

    frequency = ((rssi - rssi_min) / (rssi_max - rssi_min)) * (freq_max - freq_min) + freq_min

    return int(frequency)


telemetry = {
    # Values from the beacon
    "latitude": 0,
    "longitude": 0,

    "altitude": 0,

    "speed": 0,

    "utc": 0,

    "satellites": 0,
    "h_dilution": 0,
    "has_fix": 0,
    
    "peak_speed_kts": 0,
    "peak_alt_m": 0,

    # Metadata values from the ground
    "rssi": 0,
    "packet_age": 0
}


error_count = 0
while True:
    try:
        message, rssi, pkt_timestamp = get_message()

        if message is not None:
            if telemetry["satellites"] >= 4 or telemetry["has_fix"] == True:    # Don't log if no fix. Only used on startup when values are 0 
                log_data(telemetry)

            for key, value in message.items():
                telemetry[key] = value
            telemetry["rssi"] = rssi

            # should be outside the if statement, but then it flashes, so its here for now
            # could print every 5 seconds, and on each update or something
            print("\n" * 2)
            print("\n".join([f"{key}: {value}" for key, value in telemetry.items()]))
            print(datetime.now())


            if enable_buzzer:
                freq = rssi_to_hz(rssi)
                buzzer.play(Tone(frequency=freq))
                print("Mapped frequency:", freq, "Hz at RSSI:", rssi, "dBm")
        else:
            pass
            #buzzer.stop()
            # add some sort of heartbeat to the GS to ensure its still searching
        

        # TODO get working
        # if pkt_timestamp or telemetry["packet_age"] is not 0:
        #     packet_age = int((time.monotonic() - pkt_timestamp) * 1000)
        #     telemetry["packet_age"] = packet_age



        draw_screen(telemetry)


        if sw1.is_pressed: # Toggle buzzer mute
            enable_buzzer = not enable_buzzer
            print(f"Toggled buzzer mute to: {enable_buzzer}")
            time.sleep(0.5) # Debounce

        if sw2.is_pressed: # Toggle logging
            enable_logging = not enable_logging
            print(f"Toggled logging to: {enable_logging}")
            time.sleep(0.5) # Debounce
            #display_message("Logging {enable_logging}")

        if sw3.is_pressed: # Cycle through display modes
            pass
            time.sleep(0.5) # Debounce
            #display_message("Display mode {mode}")

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
