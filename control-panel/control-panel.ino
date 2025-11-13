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

// ******** LED SETUP ********
#define LED_PIN       8
#define NUM_LEDS      4
Adafruit_NeoPixel pixels(NUM_LEDS, LED_PIN, NEO_GRB + NEO_KHZ800);
uint32_t playerTypeLEDs[5] = {pixels.Color(0, 0, 0), pixels.Color(0, 0, 255), pixels.Color(0, 255, 0), pixels.Color(255, 128, 0), pixels.Color(255, 0, 0)};

bool mute = 0;
enum State { CONF, WAIT, BOT, HUMAN_ROLL };
State state = CONF;
int activePlayer;

enum playerType {
  NO_PLAYER,
  HUMAN,
  EASY,
  MEDIUM,
  HARD
};

enum playerColor {
  BLUE_PLAYER,
  RED_PLAYER,
  GREEN_PLAYER,
  YELLOW_PLAYER
};

playerType players[4] = {NO_PLAYER, NO_PLAYER, NO_PLAYER, NO_PLAYER};

void setup() {
  pixels.begin();
  Serial.begin(9600);
  Serial.setTimeout(0)
}

void loop() {
  // readSerial();  // may update state
  switch (state) {
    case CONF: configuration(); break;
    case WAIT: waiting(); break;
    case BOT: botTurn(); break;
  }
}

void readSerial() {
  if (Serial.available() > 0) {
    String input = Serial.readStringUntil('\n');
    input.trim(); // remove any \r or whitespace
    switch(state) {
      case WAIT: waitSerial(input);
    }
  }
}