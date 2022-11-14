import sys#, neopixel, board



""" 
# total arguments
n = len(sys.argv)

print("\nArguments passed:", end = " ")
for i in range(1, n):
    print(sys.argv[i], end = " ")
print()
"""



# red
if sys.argv[1]:
    red = int(sys.argv[1])
    print("red " + str(red))

# green
if sys.argv[2]:
    green = int(sys.argv[2])
    print("green " + str(green))

# blue
if sys.argv[3]:
    blue = int(sys.argv[3])
    print("blue " + str(blue))

# brightness
if sys.argv[4]:
    brightness = float(sys.argv[4])
    print("brightness " + str(brightness))

# index
if sys.argv[5]:
    index = int(sys.argv[5])
    print("index " + str(index))

#                         R   G   B   B   I
# python neopixel_args.py 255 255 255 0.4 0

try:
    led_neo = neopixel.NeoPixel(board.D12, 10)     # 10 pixels on pin D12
    led_neo.brightness = brightness
    led_neo[index] = (red, green, blue)
except Exception as e:
    print(e)