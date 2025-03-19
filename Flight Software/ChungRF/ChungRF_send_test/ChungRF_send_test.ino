#include <RadioLib.h>
#include <Adafruit_GPS.h>
#include <Adafruit_NeoPixel.h>

// Ebyte Module connets to the KB2040 as such (uses default SPI pins): 
// NSS pin:   D7 - 7
// DIO1 pin:  D2 - 2
// NRST pin:  D4 - 4
// BUSY pin:  D5 - 5
SX1262 radio = new Module(7, 2, 4, 5);
Adafruit_GPS GPS(&Wire1);
Adafruit_NeoPixel pixels(1, 17, NEO_GRB + NEO_KHZ800);


void setup() {
    Serial.begin(115200);
    delay(2000);

    Serial.println("ChungRF Transmit initializing...");

    pixels.begin();
    pixels.setBrightness(255);
    pixels.show();



    int state = radio.begin();
    if (state == RADIOLIB_ERR_NONE) {
        radio.setFrequency(868.0);	// the short whip antenna I have is for 868 MHz

        // Make sure this is set properly. Library max is 140ma, but module can go to 650ma.
        // 140 number for the SX1262, and the 650ma for the RF amplifier?
        radio.setCurrentLimit(140); 

        // Module can do 30dBm, so this is probably for the SX1262?
        radio.setOutputPower(22);

        Serial.println(F("Initialization done"));

        // some modules have an external RF switch
        // controlled via two pins (RX enable, TX enable)
        // to enable automatic control of the switch,
        // call the following method
        // RX enable:   9
        // TX enable:   8
        /*
            radio.setRfSwitchPins(9, 8);
        */

    } else {
        Serial.print("Failed to initialize radio, code " + String(state));
        pixels.setPixelColor(0, pixels.Color(255, 0, 0));
        pixels.show();

        while (true);
    }


    Wire1.setSDA(10);
    Wire1.setSCL(3);
    Wire1.begin();

    if (!GPS.begin(0x42)) {
        Serial.println(F("Failed to initialize GPS"));
        pixels.setPixelColor(0, pixels.Color(255, 0, 0));
        pixels.show();

        while (true);
    }

}

int i = 0;
void loop() {
    Serial.println(F("ChungRF Transmitting packet..."));

    pixels.setPixelColor(0, pixels.Color(0, 0, 255));
    pixels.show();

    // Can transmit up to 256 bytes, strings or byte arrays
    GPS.read();

    String message = "Heartbeat #" + String(i++) +
                 " GNSS sats: " + String(GPS.satellites) +
                 " Lat: " + String(GPS.latitude) +
                 " Lon: " + String(GPS.longitude) +
                 " Alt: " + String(GPS.altitude) + 

                 " NMEA: " + String(GPS.lastNMEA()) +


                 " Fix: " + String(GPS.fix);
                 
    int state = radio.transmit(message);


    char c = GPS.read();
    Serial.println(c);




    if (state == RADIOLIB_ERR_NONE) {
        Serial.print(F("Sent:\t"));
        Serial.print(message);
        Serial.println();


        Serial.print(F("Datarate:\t"));
        Serial.print(radio.getDataRate());
        Serial.println(F(" bps"));

        Serial.print(F("SNR:\t"));
        Serial.println(radio.getSNR());

        Serial.print(F("Current limit:\t"));
        Serial.println(radio.getCurrentLimit());
        Serial.println();

        Serial.println();

    } else if (state == RADIOLIB_ERR_PACKET_TOO_LONG) {
        //int overflowSize = radio.getPacketLength() - radio.getMaxPacketLength();
        Serial.println("Error: packet too long");
        pixels.setPixelColor(0, pixels.Color(255, 0, 0));
        pixels.show();


    } else if (state == RADIOLIB_ERR_TX_TIMEOUT) {
        Serial.println("Error: timed out");
        pixels.setPixelColor(0, pixels.Color(255, 0, 0));
        pixels.show();

    } else {
        Serial.print("Unknown error: ");
        Serial.println(state);
        pixels.setPixelColor(0, pixels.Color(255, 0, 0));
        pixels.show();
    }

    pixels.setPixelColor(0, pixels.Color(0, 0, 0));
    pixels.show();

    delay(1500);
}
