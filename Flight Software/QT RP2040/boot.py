import board
import digitalio
import storage

switch = digitalio.DigitalInOut(board.A0) # 
#switch = digitalio.DigitalInOut(board.BUTTON) # doesnt work, enters bootloader :(
switch.direction = digitalio.Direction.INPUT
switch.pull = digitalio.Pull.UP

# If A0 is connected to ground with a wire CircuitPython can write to the drive
storage.remount("/", switch.value)

