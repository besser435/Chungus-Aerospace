#include <RadioLib.h>

// Ebyte Module connets to the KB2040 as such (uses default SPI pins): 
// NSS pin:   D7 - 7
// DIO1 pin:  D2 - 2
// NRST pin:  D4 - 4
// BUSY pin:  D5 - 5
SX1262 radio = new Module(7, 2, 4, 5);

void setup() {
    Serial.begin(115200);
    delay(2000);

    Serial.print(F("ChungRF Receive starting..."));
    int state = radio.begin();
    if (state == RADIOLIB_ERR_NONE) {
        radio.setFrequency(868.0);	// the short whip antenna I have is for 868 MHz

        // Make sure this is set properly. Library max is 140ma, but module can go to 650ma.
        // 140 number for the SX1262, and the 650ma for the RF amplifier?
        radio.setCurrentLimit(140); 

        // Module can do 30dBm, so this is probably for the SX1262?
        radio.setOutputPower(22);

        Serial.println(F("Initialization done"));

    } else {
        Serial.print(F("Failed to initialize radio, code " + String(state)));
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
    Serial.println(F("CRF Waiting for transmission ..."));

    String message;
    int state = radio.receive(message);


    if (state == RADIOLIB_ERR_NONE) {
        Serial.print(F("ChungRF Got:\t\t"));
        Serial.println(message);

        // RSSI (Received Signal Strength Indicator)
        Serial.print(F("RSSI:\t\t"));
        Serial.print(radio.getRSSI());
        Serial.println(F(" dBm"));

        // SNR (Signal-to-Noise Ratio)
        Serial.print(F("SNR:\t\t"));
        Serial.print(radio.getSNR());
        Serial.println(F(" dB"));


    } else if (state == RADIOLIB_ERR_RX_TIMEOUT) {
        Serial.println(F("Error: timed out"));

    } else if (state == RADIOLIB_ERR_CRC_MISMATCH) {
        Serial.println(F("Error: CRC mismatch"));

    } else {
        Serial.println(F("Unknown error: " + String(state)));
    }
}
