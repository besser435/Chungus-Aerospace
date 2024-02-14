import busio
import digitalio
import time
import board
import neopixel
import adafruit_gps

# Configuration
MESSAGE_SEND_RATE = 5 # How often to send, not update


# Hardware setup
led_neo = neopixel.NeoPixel(board.NEOPIXEL, 1, brightness=1)

# NOTE On Rev B, use UART. On Rev A, use I2C (hardware oopsie doopsie)
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
    if gnss.has_fix:    #TODO dangerous assumption. Ensure this will not prevent this from executing
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

    #print(f"Sent message:  {message}")

    xbee_uart.write(encoded_message)    # encoding wrong maybe? should be hex





global peak_speed_kts   # TODO globals bad for some reason, get rid of them
global peak_alt_m
global telemetry
peak_speed_kts = 0
peak_alt_m = 0



telemetry = {
    "latitude", None,
    "longitude", None,
    "altitude", None,
    "speed", None,
    "satellites", None,
    "time", None,
    "fix_quality", None,
    "live_fix", None,
    "peak_speed_kts", peak_speed_kts
}


last_update = time.monotonic()
while True:
    try:
        gnss.update()
        gnss_data = get_gnss()

        if gnss_data and gnss_data.get("live_fix") == "True":   # TODO verify live_fix correctly states when GNSS is healthy
            telemetry = {
                "latitude", gnss_data.get("latitude"),
                "longitude", gnss_data.get("longitude"),
                "altitude", gnss_data.get("altitude"),
                "speed", gnss_data.get("speed"),
                "satellites", gnss_data.get("satellites"),
                "time", gnss_data.get("time"),
                "fix_quality", gnss_data.get("fix_quality"),
                "live_fix", gnss_data.get("live_fix"),
                "peak_speed_kts", peak_speed_kts
            }
        else:
            telemetry["live_fix"] = "Unhealthy"






        if gnss_data.get("speed") > peak_speed_kts: # convert to f/s maybe
            peak_speed_kts = gnss_data.get("speed")

        if gnss_data.get("altitude") > peak_alt_m:  # alt in m above earth ellipsoid
            # From what I have read, GNSS altitude is not terribly accurate
            peak_alt_m = gnss_data.get("altitude")
        



        # will reading fast adversely affect battery life?
        # TODO Test GPS, XBee, MCU, power sleep modes if not high enough, and only update every 10 seconds
        # see https://learn.adafruit.com/deep-sleep-with-circuitpython/alarms-and-sleep
        if time.monotonic() - last_update >= MESSAGE_SEND_RATE:
            last_update = time.monotonic()
            send_message(telemetry)













    except Exception as e:
        print("Error occurred: \n")
        print(str(e))

        reset_xbee()


        time.sleep(1)