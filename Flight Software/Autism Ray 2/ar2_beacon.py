import busio
import digitalio
import time
import board
import neopixel
import adafruit_gps

# Configuration, in seconds
MESSAGE_SEND_RATE = 2
UPDATE_RATE = 1    # Effectively, loop iteration rate


# Hardware setup
led_neo = neopixel.NeoPixel(board.NEOPIXEL, 1, brightness=0.3)

# https://learn.adafruit.com/todbot-circuitpython-tricks/i2c
# NOTE On Rev 2 and later, UART is properly connected (broken on R1), but I2C might be better. 
#gnss_uart = busio.UART(board.MISO, board.MOSI, baudrate=9600)
i2c = busio.I2C(board.SCL, board.SDA, frequency=400_000)    # SAM M10Q requires 400kHz
gnss = adafruit_gps.GPS_GtopI2C(i2c, debug=False, address=0x42)   # 0x42 is the default address

"""import board
i2c = board.I2C() # or busio.I2C(pin_scl,pin_sda)
while not i2c.try_lock():  pass
print("I2C addresses found:", [hex(device_address)
    for device_address in i2c.scan()])
i2c.unlock()"""

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


def get_gnss():
    # The GPS library does not return all the minutes.
    # We need to manually add them together.    
    # The rest of the stuff is to avoid type errors from None values
    latitude_int = int(gnss.latitude) if gnss.latitude is not None else 0
    latitude_minutes_str = str(gnss.latitude_minutes).replace(".", "") if gnss.latitude_minutes is not None else "0"

    longitude_int = int(gnss.longitude) if gnss.longitude is not None else 0
    longitude_minutes_str = str(gnss.longitude_minutes).replace(".", "") if gnss.longitude_minutes is not None else "0"

    altitude = gnss.altitude_m if gnss.altitude_m is not None else 0
    height_geoid = gnss.height_geoid if gnss.height_geoid is not None else 0

    speed = gnss.speed_knots if gnss.speed_knots is not None else 0

    utc = gnss.timestamp_utc if gnss.timestamp_utc is not None else 0

    satellites = gnss.satellites if gnss.satellites is not None else 0
    has_fix = gnss.has_fix if gnss.has_fix is not None else False

    data = {
        "latitude": f"{latitude_int}.{latitude_minutes_str}",
        "longitude": f"{longitude_int}.{longitude_minutes_str}",

        "altitude": altitude,
        "height_geoid": height_geoid, 

        "speed": speed,

        "utc": utc,

        "satellites": satellites,
        "has_fix": has_fix
    }
    return data


def send_message(message):
    """NOTE: removes spaces from the message and adds a newline and carriage return to the end."""
    message = str(message)
    message = message.replace(" ", "") + "\n\r"
    encoded_message = message.encode("utf-8")

    print(f"Sent message:  {message}")

    xbee_uart.write(encoded_message)    # encoding wrong maybe? should be hex


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
    #try:
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
            telemetry["peak_speed_kts"] = gnss_data.get("speed")

        if gnss_data.get("altitude") > telemetry["peak_alt_m"]:  # alt in m above earth ellipsoid
            telemetry["peak_alt_m"] = gnss_data.get("altitude")
    

        # NOTE Update LED status
        if telemetry["satellites"] is None or telemetry["has_fix"] == False:
            led_neo.fill((255, 0, 0))
        elif telemetry["satellites"] < 10:
            led_neo.fill((255, 255, 0))
        elif telemetry["satellites"] >= 10:
            led_neo.fill((0, 255, 0))


        # NOTE update as often as configured
        if time.monotonic() - last_update >= MESSAGE_SEND_RATE:
            # Will reading fast adversely affect battery life?
            # TODO Test GPS, XBee, MCU, power sleep modes if not high enough, and only update every 10 seconds
            # see https://learn.adafruit.com/deep-sleep-with-circuitpython/alarms-and-sleep
            last_update = time.monotonic()

            send_message(telemetry)

            
        # NOTE Debugging
        for data in telemetry.items():
            print(f"{data[0]}: {data[1]}")
        print("\n" * 2)

        print(f"loop took {time.monotonic() - last_update} seconds")

        

        time.sleep(UPDATE_RATE)


    #except Exception as e:
        #print("Error occurred: \n")
        #print(str(e))

        #reset_xbee()


        #time.sleep(1)