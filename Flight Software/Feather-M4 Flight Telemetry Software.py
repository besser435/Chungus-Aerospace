def main_notes():   # to collapse the text below in the IDE  
    """
    Flight Telemetry Software for the CircuitPython platform by Joe Mama and besser
    Made for the Chungus Aerospace Program
    
    https://github.com/besser435?tab=repositories
    """

version = "v0.2"
date = "December 2022"

# idea: add wifi module so it can fetch the current pressure in phoenix. this way we
# dont have to get it manually then update the code or whateverD
import adafruit_bmp3xx
import time
import analogio
import board
import digitalio
import storage
import adafruit
import adafruit_sdcard
from rainbowio import colorwheel
import adafruit_dotstar
import neopixel
import microcontroller
def main():



    vbat_voltage = analogio.AnalogIn(board.D9)

    i2c = board.I2C() # uses board.SCL and board.SDA

    SD_CS = board.D10
    spi = board.SPI()
    cs = digitalio.DigitalInOut(SD_CS)
    
    sdcard = adafruit_sdcard.SDCard(spi, cs)
    vfs = storage.VfsFat(sdcard)
    storage.mount(vfs, "/sd")


    # For Feather M0 Express, Metro M0 Express, Metro M4 Express, Circuit Playground Express, QT Py M0
    led = neopixel.NeoPixel(board.NEOPIXEL, 1)
    
    #led = digitalio.DigitalInOut(board.D13)
    led.direction = digitalio.Direction.OUTPUT

    print("Logging temperature to filesystem")
    # append to the file!
    while True:
        # open file for append
        with open("/sd/temperature.txt", "a") as f:
            led.value = True  # turn on LED to indicate we're writing to the file
            t = microcontroller.cpu.temperature
            print("Temperature = %0.1f" % t)
            f.write("%0.1f\n" % t)
            led.value = False  # turn off LED to indicate we're done
        # file is saved
        time.sleep(1)

    print("Logging to log file")

    initial_time = time.monotonic()





    def get_voltage(pin):
        return (pin.value * 3.3) / 65536 * 2
    
# BMP388
# I2C setup
i2c = board.I2C()  # uses board.SCL and board.SDA
bmp = adafruit_bmp3xx.BMP3XX_I2C(i2c)

# SPI setup
# from digitalio import DigitalInOut, Direction
# spi = board.SPI()
# cs = DigitalInOut(board.D5)
# bmp = adafruit_bmp3xx.BMP3XX_SPI(spi, cs)



bmp.sea_level_pressure = 1008
bmp.pressure_oversampling = 8
bmp.temperature_oversampling = 2

while True:
    print(
        "Pressure: {:6.4f}  Temperature: {:5.2f}".format(bmp.pressure, bmp.temperature, bmp.altitude)
    )
    print('Altitude: {} meters'.format(bmp.altitude))
    time.sleep(0.5)










main()