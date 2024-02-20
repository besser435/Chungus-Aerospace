import busio
import digitalio
import time
import board
import neopixel
import adafruit_gps

# Configuration, in seconds
MESSAGE_SEND_RATE = 1
UPDATE_RATE = 0     # loop iteration rate


# Hardware setup
led_neo = neopixel.NeoPixel(board.NEOPIXEL, 1, brightness=1)

# NOTE On Rev 2 and later, use UART. On Rev 1, use I2C (hardware oopsie doopsie)
#gnss_uart = busio.UART(board.MISO, board.MOSI, baudrate=9600)
#gnss = adafruit_gps.GPS(gnss_uart, debug=False)
gnss = adafruit_gps.GPS_GtopI2C(board.I2C())

xbee_reset = digitalio.DigitalInOut(board.D3)
xbee_uart = busio.UART(board.TX, board.RX, baudrate=9600)


def reset_xbee():
    """ BUG XBee does not work without a reset.
    See page 189. https://www.digi.com/resources/documentation/digidocs/pdfs/90002173.pdf"""
    xbee_reset.direction = digitalio.Direction.OUTPUT
    xbee_reset.value = False    # Drive low to reset
    time.sleep(1)
    xbee_reset.direction = digitalio.Direction.INPUT # Set as input (pulling high might cause damage the XBee)
reset_xbee()

def get_gnss():
    if gnss.has_fix:    # TODO dangerous assumption. Ensure this will not prevent this from executing
        # ensure no precision errors with the float minutes. see GPS docs
        data = {
            #"latitude": gnss.latitude,
            #"latitude_mins": gnss.latitude_minutes,
            #"longitude": gnss.longitude,
            #"longitude_mins": gnss.longitude_minutes,
        
            "latitude": gnss.latitude + gnss.latitude_minutes,
            "longitude": gnss.longitude + gnss.longitude_minutes,

            "altitude": gnss.altitude_m,

            "speed": gnss.speed_knots,

            "time": gnss.timestamp_utc,

            "satellites": gnss.satellites,
            "fix_quality": gnss.fix_quality,
            "live_fix": "Test"
        }
        #raise Exception("Ensure minutes are not being returned twice")

        return data
    else:
        return False

def send_message(message):
    message = str(message + "\r")
    encoded_message = message.encode("utf-8")

    print(f"Sent message:  {message}")

    xbee_uart.write(encoded_message)    # encoding wrong maybe? should be hex

def get_gnss_SIL():
    import random

    rng_speed = random.randint(0, 100)
    rng_alt = random.randint(0, 1000)

    return {
        "latitude": 38.897957,
        "longitude": -77.036560,

        "altitude": rng_alt,

        "speed": rng_speed,

        "time": "Jan 1st 1970",

        "satellites": 4,
        "fix_quality": 1,
        "live_fix": "True"  # TODO this probably isnt needed
    }



telemetry = {   # outside of loop to not reset values
    "latitude": None,
    "longitude": None,

    "altitude": None,

    "speed": None,

    "time": None,

    "satellites": None,
    "fix_quality": None,
    "live_fix": None,
    
    "peak_speed_kts": None,
    "peak_alt_m": None
}


last_update = time.monotonic()
while True:
    try:
        gnss.update()
        gnss_data = get_gnss_SIL() #get_gnss_SIL()

        if gnss_data and gnss_data.get("live_fix") == "True":   # TODO verify live_fix correctly states when GNSS is healthy
            # do not overwrite existing keys, only update the key values that are present
            for key in telemetry.keys():
                if key in gnss_data:
                    telemetry[key] = gnss_data[key]
        else:
            telemetry["live_fix"] = "Unhealthy"






        if gnss_data.get("speed") > telemetry["peak_speed_kts"]:
            # Convert to m/s on the ground with round(float(telemetry["peak_speed_kts"] * 0.514444), 3)
            telemetry["peak_speed_kts"] = gnss_data.get("speed")


        if gnss_data.get("altitude") > telemetry["peak_alt_m"]:  # alt in m above earth ellipsoid
            # From what I have read, GNSS altitude is not terribly accurate
            peak_alt_m = gnss_data.get("altitude")
        



        # will reading fast adversely affect battery life?
        # TODO Test GPS, XBee, MCU, power sleep modes if not high enough, and only update every 10 seconds
        # see https://learn.adafruit.com/deep-sleep-with-circuitpython/alarms-and-sleep
        if time.monotonic() - last_update >= MESSAGE_SEND_RATE:
            last_update = time.monotonic()
            send_message(telemetry)

        time.sleep(UPDATE_RATE)
            


        print(f"Loop iteration took: {time.monotonic() - last_update}s")
        
        for data in telemetry.items():
            print(f"{data[0]}: {data[1]}")

    except Exception as e:
        print("Error occurred: \n")
        print(str(e))

        reset_xbee()


        time.sleep(1)