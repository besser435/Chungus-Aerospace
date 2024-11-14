#include <RadioLib.h>

// Ebyte Module connets to the KB2040 as such (uses default SPI pins): 
// NSS pin:   D7 - 7
// DIO1 pin:  D2 - 2
// NRST pin:  D4 - 4
// BUSY pin:  D5 - 5
SX1262 radio = new Module(7, 2, 4, 5);

void setup() {
  Serial.begin(9600);
  delay(2000);

  // initialize SX1262 with default settings
  Serial.print(F("[SX1262] Initializing ... "));
  int state = radio.begin();
  if (state == RADIOLIB_ERR_NONE) {
    radio.setFrequency(868.0);	// the short whip antenna I have is for 868 MHz

    // Make sure this is set properly. Max is 140, but module can go to 650.
    // 140 number for the SX1262, and the 650 for the RF amplifier?
    radio.setCurrentLimit(140); 

    // Module can do 30dBm, so this is probably for the SX1262?
    radio.setOutputPower(22);


    Serial.println(F("success!"));
  } else {
    Serial.print(F("failed, code "));
    Serial.println(state);
    while (true);
  }

  // some modules have an external RF switch
  // controlled via two pins (RX enable, TX enable)
  // to enable automatic control of the switch,
  // call the following method
  // RX enable:   9
  // TX enable:   8
  /*
    radio.setRfSwitchPins(9, 8);
  */
}

// counter to keep track of transmitted packets
int count = 0;

void loop() {
  Serial.print(F("[SX1262] Transmitting packet ... "));

  // you can transmit C-string or Arduino string up to
  // 256 characters long
  String str = "Hello World! #" + String(count++);
  int state = radio.transmit(str);

  // you can also transmit byte array up to 256 bytes long
  /*
    byte byteArr[] = {0x01, 0x23, 0x45, 0x56, 0x78, 0xAB, 0xCD, 0xEF};
    int state = radio.transmit(byteArr, 8);
  */

  if (state == RADIOLIB_ERR_NONE) {
    // the packet was successfully transmitted
    Serial.println(F("success!"));

    // print measured data rate
    Serial.print(F("[SX1262] Datarate:\t"));
    Serial.print(radio.getDataRate());
    Serial.println(F(" bps"));

    Serial.print(F("SNR: \t"));
    Serial.println(radio.getSNR());

    Serial.print(F("Current limit: \t"));
    Serial.println(radio.getCurrentLimit());
    Serial.println();



  } else if (state == RADIOLIB_ERR_PACKET_TOO_LONG) {
    // the supplied packet was longer than 256 bytes
    Serial.println(F("too long!"));

  } else if (state == RADIOLIB_ERR_TX_TIMEOUT) {
    // timeout occured while transmitting packet
    Serial.println(F("timeout!"));

  } else {
    // some other error occurred
    Serial.print(F("failed, code "));
    Serial.println(state);

  }

  // wait for a second before transmitting again
  delay(500);
}
