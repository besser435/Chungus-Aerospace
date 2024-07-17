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
sx = SX1262(spi_bus=1, clk=SCK, mosi=MOSI, miso=MISO, cs=CS, irq=IRQ, rst=RST, gpio=BUSY)

# LoRa
sx.begin(freq=868, bw=500.0, sf=12, cr=8, syncWord=0x12,
         power=22, currentLimit=100, preambleLength=8,
         implicit=False, implicitLen=0xFF,
         crcOn=True, txIq=False, rxIq=False,
         tcxoVoltage=1.7, useRegulatorLDO=False, blocking=True)



last_pkt_time = 0
packet_age = 0
while True:
    msg, err = sx.recv()
    if len(msg) > 0:
        error = SX1262.STATUS[err]
        pkt_timestamp = time.monotonic()

        print(msg)
        print(error)

    else:
        print(f"No message. Packet age: {packet_age}ms")


    if pkt_timestamp:
        packet_age = int((time.monotonic() - pkt_timestamp) * 1000)
        last_pkt_time = pkt_timestamp
    else:
        packet_age = int((time.monotonic() - last_pkt_time) * 1000)


    time.sleep(0.2)
