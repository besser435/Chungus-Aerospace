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

void loop() {
  Serial.print(F("[SX1262] Waiting for incoming transmission ... "));

  String message;
  int state = radio.receive(message);

  // you can also receive data as byte array
  /*
    byte byteArr[8];
    int state = radio.receive(byteArr, 8);
  */

  if (state == RADIOLIB_ERR_NONE) {
    // packet was successfully received
    Serial.println(F("success!"));

    // print the data of the packet
    Serial.print(F("[SX1262] Data:\t\t"));
    Serial.println(message);

    // print the RSSI (Received Signal Strength Indicator)
    // of the last received packet
    Serial.print(F("[SX1262] RSSI:\t\t"));
    Serial.print(radio.getRSSI());
    Serial.println(F(" dBm"));

    // print the SNR (Signal-to-Noise Ratio)
    // of the last received packet
    Serial.print(F("[SX1262] SNR:\t\t"));
    Serial.print(radio.getSNR());
    Serial.println(F(" dB"));

    // print frequency error
    Serial.print(F("[SX1262] Frequency error:\t"));
    Serial.print(radio.getFrequencyError());
    Serial.println(F(" Hz"));



  } else if (state == RADIOLIB_ERR_RX_TIMEOUT) {
    // timeout occurred while waiting for a packet
    Serial.println(F("timeout!"));

  } else if (state == RADIOLIB_ERR_CRC_MISMATCH) {
    // packet was received, but is malformed
    Serial.println(F("CRC error!"));

  } else {
    // some other error occurred
    Serial.print(F("failed, code "));
    Serial.println(state);

  }
}
