def main_notes():   # to collapse the text below in the IDE  
    """
    Flight Telemetry Software for the CircuitPython platform by Joe Mama and besser
    Made for the Chungus Aerospace Program
    
    https://github.com/besser435?tab=repositories
    """

version = "v0.1"
date = "December 2022"

# idea: add wifi module so it can fetch the current pressure in phoenix. this way we
# dont have to get it manually then update the code or whateverD

def main():
    import adafruit_bmp3xx
    import time
    import analogio
    import board
    import digitalio
    import storage
    import adafruit
    import adafruit_sdcard

    vbat_voltage = analogio.AnalogIn(board.D9)

    i2c = board.I2C() # uses board.SCL and board.SDA
    am2320 = adafruit_am2320.AM2320(i2c)

    SD_CS = board.D10
    spi = board.SPI()
    cs = digitalio.DigitalInOut(SD_CS)
    sd_card = adafruit_sdcard.SDCard(spi, cs)
    vfs = storage.VfsFat(sd_card)
    storage.mount(vfs, "/sd_card")

    def get_voltage(pin):
        return (pin.value * 3.3) / 65536 * 2


    print("Logging temperature and humidity to log file")

    initial_time = time.monotonic()










# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import board
import adafruit_bmp3xx

# I2C setup
i2c = board.I2C()  # uses board.SCL and board.SDA
bmp = adafruit_bmp3xx.BMP3XX_I2C(i2c)

# SPI setup
# from digitalio import DigitalInOut, Direction
# spi = board.SPI()
# cs = DigitalInOut(board.D5)
# bmp = adafruit_bmp3xx.BMP3XX_SPI(spi, cs)


bmp.altitude
bmp.sea_level_pressure
bmp.sea_level_pressure
bmp.pressure_oversampling = 8
bmp.temperature_oversampling = 2

while True:
    print(
        "Pressure: {:6.4f}  Temperature: {:5.2f}".format(bmp.pressure, bmp.temperature)
    )
    time.sleep(1)













main()