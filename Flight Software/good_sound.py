import pwmio
import board
import time

"""
CircuitPython's ways of playing tones with piezo buzzers are not very good.
They will not play the right sound, play inconsistently, and are not loud enough.

This fixes that by just driving the piezo buzzer with a PWM signal.

"""



pwm1 = pwmio.PWMOut(board.D5, duty_cycle=2**15, frequency=1, variable_frequency=True)
# inverted duty cycle so its louder (NOTE: still very quiet, cannot tell a difference vs GND ref)
pwm2 = pwmio.PWMOut(board.D6, duty_cycle=65535 - 2**15, frequency=1, variable_frequency=True)

def play_sound(hz_frequency: int, duration: float):
    """Play a sound at a given frequency and duration using differential PWM on two pins. 
    
    If the duration is 0, the sound will play indefinitely."""
    
    pwm1.frequency = hz_frequency
    pwm2.frequency = hz_frequency
    # Hackily reenable the PWM output
    pwm1.duty_cycle = 2**15  # 50% duty cycle
    pwm2.duty_cycle = 65535 - 2**15
    
    
    if hz_frequency is not pwm1.frequency:
        print(f"Frequency interpolated by MCU for PWM. New frequency: {pwm1.frequency} Hz")
    else:
        print(f"Playing sound at {hz_frequency} Hz")


    if duration:
        time.sleep(duration)
    else:
        return
    

    # Since we can't set the frequency to 0 without a value error
    pwm1.duty_cycle = 0
    pwm2.duty_cycle = 0
    print("Sound stopped")




play_sound(3000, 0.5)
time.sleep(1)

play_sound(2000, 0.5)
time.sleep(1)

play_sound(1, 0.5)




# NOTE Old test code below:


# import pwmio
# import board
# import time


# pwm1 = pwmio.PWMOut(board.D5, duty_cycle=2**15, frequency=1, variable_frequency=True)

# # inverted duty cycle so its louder (NOTE: still very quet, cannot tell a difference vs GND)
# pwm2 = pwmio.PWMOut(board.D6, duty_cycle=65535 - 2**15, frequency=1, variable_frequency=True)  

# print("\n" * 10)

# def beep_loop():
#     pwm1.frequency = 3_500
#     pwm2.frequency = 3_500
    
#     pwm1.duty_cycle = 2**15  # 50% duty cycle
#     pwm2.duty_cycle = 65535 - 2**15  # inverted 50% duty cycle
    
#     print(f"PWM1 frequency: {pwm1.frequency}, PWM2 frequency: {pwm2.frequency}")
#     time.sleep(0.2)
    
#     for i in range(3):
#         time.sleep(0.2)
        
#         # hackily renable the PWM output
#         pwm1.duty_cycle = 2**15
#         pwm2.duty_cycle = 65535 - 2**15
        
#         pwm1.frequency = 2_000
#         pwm2.frequency = 2_000
#         # the MCU will round round the set frequency to what it can achieve, not what we set
#         print(f"PWM1 frequency: {pwm1.frequency}, PWM2 frequency: {pwm2.frequency}")
#         time.sleep(0.2)
        
#         # since we can't set the frequency to 0 without a value error
#         pwm1.duty_cycle = 0
#         pwm2.duty_cycle = 0
#         print("PWM disabled")

# while True:
#     beep_loop()
#     time.sleep(1)

    




