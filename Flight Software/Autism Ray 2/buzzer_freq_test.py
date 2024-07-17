
from gpiozero import TonalBuzzer
from gpiozero.tones import Tone

import board
import busio


import RPi.GPIO as GPIO

import traceback
import time
import json

# # Buzzer
TonalBuzzer.max_tone = property(lambda self: Tone(4000))
buzzer = TonalBuzzer(21)
enable_buzzer = True

# print("starting in 3")
# time.sleep(3)


# # stop with stop()
# buzzer.play(Tone(1000))
# time.sleep(0.5)
# buzzer.stop()

# print("buzzer.stop()")
# time.sleep(1)




# # stop with tone(0)
# buzzer.play(Tone(2000))
# time.sleep(0.5)
# buzzer.play(Tone(0))

# print("Tone(0)")
# time.sleep(1)






# if enable_buzzer:
#     buzzer.play(Tone(2000))
#     time.sleep(0.5)
#     buzzer.stop()

#     print(f"if enable_buzzer: {enable_buzzer}")

#     enable_buzzer = not enable_buzzer




# if enable_buzzer:
#     buzzer.play(Tone(2000))
#     time.sleep(0.5)
#     buzzer.stop()

#     print(f"if enable_buzzer: {enable_buzzer}")

#     enable_buzzer = not enable_buzzer




time.sleep(3)


def map_rssi_to_frequency(rssi):
    # Define the RSSI range and corresponding frequency range
    rssi_min = -170
    rssi_max = -15
    freq_min = 250
    freq_max = 2000

    # Perform linear mapping
    frequency = ((rssi - rssi_min) / (rssi_max - rssi_min)) * (freq_max - freq_min) + freq_min

    return int(frequency)

# Example usage
rssi_value = -170  # Example RSSI value
frequency = map_rssi_to_frequency(rssi_value)
print("Mapped frequency:", frequency, "Hz at RSSI:", rssi_value, "dBm")

buzzer.play(Tone(frequency=frequency))


time.sleep(3)