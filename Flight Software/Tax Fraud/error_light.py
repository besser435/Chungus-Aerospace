import neopixel, board, time


# Neopixel

led_neo = neopixel.NeoPixel(board.NEOPIXEL, 1)

while True:
    led_neo.fill((255, 0, 0))
    time.sleep(0.15)
    led_neo.fill((0, 0, 0))
    print("error")
    time.sleep(0.15)