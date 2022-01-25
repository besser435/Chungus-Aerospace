import board
import digitalio
import storage

switch = digitalio.DigitalInOut(board.D5) # D5 for testing on the Feather. Could bridge GND and D4 on the ruler
switch.direction = digitalio.Direction.INPUT
switch.pull = digitalio.Pull.UP

# If the D0 is connected to ground with a wire
# CircuitPython can write to the drive
storage.remount("/", switch.value)