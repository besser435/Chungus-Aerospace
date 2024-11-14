import qrcode
from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306
from luma.core.render import canvas
from PIL import Image
import time

import os 
# cd to current dir
os.chdir(os.path.dirname(os.path.abspath(__file__)))



# Function to generate and display QR code on OLED
def generate_and_display_qr(data, width=64, height=64):
    # Generate QR code image
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=1,
    )
    qr.add_data(data)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white")

    # Resize QR code image to fit OLED dimensions
    qr_img_resized = qr_img.resize((width, height))

    # Initialize OLED device
    serial = i2c(port=1, address=0x3D)
    device = ssd1306(serial)

    # Display QR code on OLED
    with canvas(device) as draw:
        draw.bitmap((0, 0), qr_img_resized, fill="white")

    # save image
    qr_img_resized.save("qr.png")

# Example usage
data_to_encode = "https://www.google.com/maps/@33.68136,-111.9786004,15.5z?entry=ttu"
generate_and_display_qr(data_to_encode)
time.sleep(100)