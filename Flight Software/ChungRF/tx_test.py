from sx1262 import SX1262   # https://github.com/ehong-tl/micropySX126X/tree/master
import time
import digitalio
import board


CS = board.SCL
SCK = board.SCK
MOSI = board.MOSI
MISO = board.MISO
BUSY = board.D13
RST = board.D11




IRQ = board.D9

# https://ebyteiot.com/collections/lora-module/products/sx1262-lora-module-e22-900m30s-868mhz-wireless-module-30dbm-12km-range-ipex-antenna-spi-interface-low-power-consumption-ebyte
sx = SX1262(spi_bus=1, clk=CLK, mosi=MOSI, miso=MISO, cs=CS, irq=IRQ, rst=RST, gpio=BUSY)

# LoRa
sx.begin(freq=868, bw=500.0, sf=12, cr=8, syncWord=0x12,
         power=22, currentLimit=1000, preambleLength=8,
         implicit=False, implicitLen=0xFF,
         crcOn=True, txIq=False, rxIq=False,
         tcxoVoltage=1.7, useRegulatorLDO=False, blocking=True)


i = 0
while True:
    message = b"ChungRF test, i= " + str(i)
    sx.send(message)
    print(f"Sent: {message}")

    i = i + 1
    time.sleep(1)
