#include <Keypad.h>
#include <Adafruit_NeoPixel.h>

// ******** KEYPAD SETUP ********
const uint8_t ROWS = 4;
const uint8_t COLS = 2;
char keys[ROWS][COLS] = {
  { 'B', 'S' },
  { 'R', 'D' },
  { 'G', 'M' },
  { 'Y', 'F' }
};
uint8_t colPins[COLS] = { 3, 2 };
uint8_t rowPins[ROWS] = { 7, 6, 5, 4 };
Keypad keypad = Keypad(makeKeymap(keys), rowPins, colPins, ROWS, COLS);

#define LED_PIN       8
#define NUM_LEDS      4
Adafruit_NeoPixel pixels(NUM_LEDS, LED_PIN, NEO_GRB + NEO_KHZ800);
uint32_t COLOR_NONE   = pixels.Color(0, 0, 0);
uint32_t COLOR_HUMAN  = pixels.Color(0, 0, 255);   // Blue
uint32_t COLOR_EASY   = pixels.Color(0, 255, 0);   // Green
uint32_t COLOR_MEDIUM = pixels.Color(255, 128, 0); // Orange
uint32_t COLOR_HARD   = pixels.Color(255, 0, 0);   // Red

bool mute = 0;
enum State { ALPHA, BETA, GAMMA };
State state = ALPHA;

void setup() {
  pixels.begin();
  Serial.begin(9600);
}

void loop() {
  readSerial();  // may update state
  switch (state) {
    case ALPHA: alpha(); break;
    case BETA:  beta();  break;
    case GAMMA: gamma(); break;
  }
}

void readSerial() {
  if (Serial.available() > 0) {
    String input = Serial.readStringUntil('\n');
    input.trim(); // remove any \r or whitespace

    if (input == "alpha") {
      state = ALPHA;
    } else if (input == "beta") {
      state = BETA;
    } else if (input == "gamma") {
      state = GAMMA;
    }
  }
}