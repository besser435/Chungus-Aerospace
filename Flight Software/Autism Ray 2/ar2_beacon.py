import busio
import digitalio
import time
import board
import neopixel
import adafruit_gps


# Configuration
MESSAGE_SEND_RATE = 5 # How often to send 


# Hardware setup
led_neo = neopixel.NeoPixel(board.NEOPIXEL, 1, brightness=1)

gnss_uart = busio.UART(board.MISO, board.MOSI, baudrate=9600)
gnss = adafruit_gps.GPS(gnss_uart, debug=False)

xbee_uart = busio.UART(board.TX, board.RX, baudrate=9600)



def configure_xbee():
    # should encrypt data so there isnt any interference from other xbee devices
    # should also shift down to 900MHz for slightly better range
    pass

configure_xbee()







def get_gnss():
    if gnss.has_fix:
        # ensure no precision errors with the float minutes. see GPS docs
        data = {
            "latitude": gnss.latitude,
            "latitude_mins": gnss.latitude_minutes,

            "longitude": gnss.longitude,
            "longitude_mins": gnss.longitude_minutes,
        
            "altitude": gnss.altitude_m,

            "speed": gnss.speed_knots,

            "time": gnss.timestamp_utc,

            "satellites": gnss.satellites,
            "fix_quality": gnss.fix_quality,
            "live_fix": "True"
        }
        return data
    else:
        return False


def send_message(message):
    message = str(message + "\r")
    encoded_message = message.encode("utf-8")

    print(f"Sent message:  {message}")
    print(f"Sent message raw: {encoded_message} \n\n")

    xbee_uart.write(encoded_message)    # encoding wrong maybe? should be hex





heartbeat = 0
global peak_speed_kts
peak_speed_kts = 0

last_update = time.monotonic()
while True:
    try:
        gnss.update()
        gnss_data = get_gnss()

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



        if gnss_data:
            precise_lat = gnss_data.get("latitude") + gnss_data.get("latitude_mins")
            precise_lon = gnss_data.get("longitude") + gnss_data.get("longitude_mins")



            telemetry = {
                "latitude": precise_lat,
                "longitude": precise_lon,
                "altitude": gnss_data.get("altitude"),
                "speed": gnss_data.get("speed"),
                "satellites": gnss_data.get("satellites"),
                "time": gnss_data.get("time"),
                "fix_quality": gnss_data.get("fix_quality"),
                "live_fix": gnss_data.get("live_fix")
            }
        else:
            telemetry["live_fix"] = "Unhealthy"






        if gnss_data.get("speed") > peak_speed_kts:
            peak_speed_kts = gnss_data.get("speed")
        

        if time.monotonic() - last_update >= MESSAGE_SEND_RATE:
            heartbeat += 1
            last_update = time.monotonic()
            send_message(telemetry)













    except Exception as e:
        pass