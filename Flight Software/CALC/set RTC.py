import time, board, adafruit_pcf8523

i2c = board.I2C() 
rtc = adafruit_pcf8523.PCF8523(i2c)

days = ("Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday")
#                     year, mon, date, hour, min, sec, wday, yday, isdst
t = time.struct_time((2022,  12,   23,   4,   8,   30,  6,    -1,  -1))
rtc.datetime = t
