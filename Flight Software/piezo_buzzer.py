import pwmio
import board
import time

"""
CircuitPython's ways of playing tones with piezo buzzers are not very good.
They will not play the right sound, play inconsistently, and are not loud enough.

This fixes that by just driving the piezo buzzer with a PWM signal.
"""

class PiezoBuzzer:
    def __init__(self, pin1, pin2):
        """Initialize the PiezoBuzzer with two pins for differential PWM driving."""
        self.pwm1 = pwmio.PWMOut(pin1, duty_cycle=2**15, frequency=1, variable_frequency=True)
        self.pwm2 = pwmio.PWMOut(pin2, duty_cycle=65535 - 2**15, frequency=1, variable_frequency=True)  # Inverted duty cycle for louder sound

    def play_sound(self, hz_frequency: int, duration: float):
        """Play a sound at a given frequency and duration using differential PWM on two pins. 
        
        If the duration is 0, the sound will play indefinitely."""
        
        self.pwm1.frequency = hz_frequency
        self.pwm2.frequency = hz_frequency
        # Hackily reenable the PWM output
        self.pwm1.duty_cycle = 2**15  # 50% duty cycle
        self.pwm2.duty_cycle = 65535 - 2**15
        
        if hz_frequency is not self.pwm1.frequency:
            print(f"Frequency interpolated by MCU. New frequency: {self.pwm1.frequency} Hz. Old: {hz_frequency} Hz")
        else:
            print(f"Playing sound at {hz_frequency} Hz")

        if duration:
            time.sleep(duration)
        else:
            return

        # Since we can't set the frequency to 0 without a value error
        self.pwm1.duty_cycle = 0
        self.pwm2.duty_cycle = 0
        print("Sound stopped")


# Example usage of the PiezoBuzzer class
buzzer = PiezoBuzzer(board.D5, board.D6)

buzzer.play_sound(3000, 0.5)
time.sleep(1)

buzzer.play_sound(2000, 0.5)
time.sleep(1)

buzzer.play_sound(1, 0.5)
