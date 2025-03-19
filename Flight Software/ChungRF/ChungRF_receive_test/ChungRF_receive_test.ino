#include <RadioLib.h>
#include <Adafruit_NeoPixel.h>

// Ebyte Module connections (default SPI pins):
#define NSS_PIN  7
#define DIO1_PIN 2  // Interrupt Pin
#define NRST_PIN 4
#define BUSY_PIN 5

SX1262 radio = new Module(NSS_PIN, DIO1_PIN, NRST_PIN, BUSY_PIN);
Adafruit_NeoPixel pixels(1, 17, NEO_GRB + NEO_KHZ800);

volatile bool receivedFlag = false;  // Flag to indicate message received
String receivedMessage = "";         // Stores received message

void setFlag(void) {
    receivedFlag = true; // Interrupt function - triggers when a message is received
}

void setup() {
    Serial.begin(115200);
    delay(2000);

    Serial.println(F("ChungRF Receiver initializing..."));

    pixels.begin();
    pixels.setBrightness(255);
    pixels.show();

    int state = radio.begin();
    if (state == RADIOLIB_ERR_NONE) {
        radio.setFrequency(868.0);
        radio.setCurrentLimit(140);
        radio.setOutputPower(22);

        Serial.println(F("Initialization done"));

        // Attach interrupt on DIO1 (pin 2) when a message is received
        radio.setDio1Action(setFlag);

        // Start receiving in continuous mode
        radio.startReceive();

    } else {
        Serial.print(F("Failed to initialize radio, code "));
        Serial.println(state);
        pixels.setPixelColor(0, pixels.Color(255, 0, 0));
        pixels.show();

        while (true);
    }
}

void loop() {
    if (receivedFlag) {  // If message received
        receivedFlag = false;  // Reset flag

        int state = radio.readData(receivedMessage);

        if (state == RADIOLIB_ERR_NONE) {
            pixels.setPixelColor(0, pixels.Color(0, 255, 0)); // Green for success
            pixels.show();

            Serial.print(F("ChungRF Got:\t\t"));
            Serial.println(receivedMessage);

            // Print RSSI and SNR
            Serial.print(F("RSSI:\t\t"));
            Serial.print(radio.getRSSI());
            Serial.println(F(" dBm"));

            Serial.print(F("SNR:\t\t"));
            Serial.print(radio.getSNR());
            Serial.println(F(" dB"));

            pixels.setPixelColor(0, pixels.Color(0, 0, 0)); // Turn off LED
            pixels.show();

        } else {
            Serial.println(F("Receive failed!"));
            pixels.setPixelColor(0, pixels.Color(255, 0, 0)); // Red for failure
            pixels.show();
        }

        // Resume listening for next transmission
        radio.startReceive();
    }
}
