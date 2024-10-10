import pwmio
import board
import time

"""
CircuitPython's ways of playing tones with piezo buzzers are not very good.
They will not play the right sound, play inconsistently, and are not loud enough.

This fixes that by just driving the piezo buzzer with a PWM signal.
"""

class PiezoBuzzer:
    def __init__(self, pwm_pin, pwm_pin_inverted=None):
        """Initialize the piezo buzzer.
        `pwm_pin` is required, `pwm_pin_inverted` is optional for differential drive.

        Takes a CircuitPython board pin object for each pin."""

        self.pwm_pin = pwmio.PWMOut(pwm_pin, duty_cycle=2**15, frequency=1, variable_frequency=True)
        # Inverted duty cycle so its louder (NOTE: still quiet, cannot tell a real difference vs GND ref. But maybe its there, idk.)
        if pwm_pin_inverted:
            self.pwm_inverted = pwmio.PWMOut(pwm_pin_inverted, duty_cycle=65535 - 2**15, frequency=1, variable_frequency=True)
        else:
            self.pwm_inverted = None


    def play_sound(self, hz_frequency: int, duration: float=None):
        """Play a sound at a given frequency and duration using differential PWM on two pins. 
        
        If the duration is 0, the sound will play indefinitely."""
        
        # Hackily reenable the PWM output if disabled by the end part
        self.pwm_pin.frequency = hz_frequency
        self.pwm_pin.duty_cycle = 2**15  # 50% duty cycle

        if self.pwm_inverted:
            self.pwm_inverted.frequency = hz_frequency
            self.pwm_inverted.duty_cycle = 65535 - 2**15  # Inverted 50% duty cycle

        
        if hz_frequency is not self.pwm_pin.frequency:
            print(f"Frequency interpolated by MCU. New frequency: {self.pwm_pin.frequency} Hz. Old: {hz_frequency} Hz")
        else:
            print(f"Playing sound at {hz_frequency} Hz")

        if duration:
            time.sleep(duration)
        else:
            return


        # Since we can't set the frequency to 0 without a value error.
        # We do this to stop the sound, otherwise we get funny noises when idle.
        self.pwm_pin.duty_cycle = 0
        if self.pwm_inverted: self.pwm_inverted.duty_cycle = 0
        print("Sound stopped")


    def stop_sound(self):   # In case the sound was set to play indefinitely
        """Stop the sound by setting the duty cycle to 0."""
        self.pwm_pin.duty_cycle = 0
        if self.pwm_inverted: self.pwm_inverted.duty_cycle = 0
        print("Sound stopped")




buzzer = PiezoBuzzer(board.D5, board.D6)

while True:
    buzzer.play_sound(262)
    time.sleep(1)

    buzzer.play_sound(494)
    time.sleep(1)

    buzzer.stop_sound()
    time.sleep(1)