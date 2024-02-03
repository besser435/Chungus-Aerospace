import board
import busio
import time

uart = busio.UART(board.TX, board.RX, baudrate=9600)

i = 0
while True:
    uart.write(bytearray("Hello, world! " + str(i) + "\r\n", "utf-8"))
    print("Sent: Hello, world! " + str(i))
    i += 1
    time.sleep(1)