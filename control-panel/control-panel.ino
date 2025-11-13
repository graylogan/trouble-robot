#include <Adafruit_NeoPixel.h>
#include <Keypad.h>

/* **************************
         KEYPAD SETUP
************************** */

const uint8_t ROWS = 4;
const uint8_t COLS = 2;
char keys[ROWS][COLS] = {{'B', 'S'}, {'R', 'D'}, {'G', 'M'}, {'Y', 'F'}};
uint8_t colPins[COLS] = {3, 2};
uint8_t rowPins[ROWS] = {7, 6, 5, 4};
Keypad keypad = Keypad(makeKeymap(keys), rowPins, colPins, ROWS, COLS);

/* **************************
         NEOPIXEL SETUP
************************** */
#define LED_PIN 8
#define NUM_LEDS 4
Adafruit_NeoPixel pixels(NUM_LEDS, LED_PIN, NEO_GRB + NEO_KHZ800);
uint32_t playerTypeLEDs[5] = {
    pixels.Color(0, 0, 0), pixels.Color(0, 0, 255), pixels.Color(0, 255, 0),
    pixels.Color(255, 128, 0), pixels.Color(255, 0, 0)};

/* **************************
         ENUMS
************************** */

// indeces parallel with playerTypeLEDs
enum playerType { NO_PLAYER, HUMAN, EASY, MEDIUM, HARD };

enum playerColor { BLUE_PLAYER, RED_PLAYER, GREEN_PLAYER, YELLOW_PLAYER };

enum State { CONF, WAIT, BOT, HUMAN_ROLL, HUMAN_TURN };

/* **************************
      GLOBAL VARIABLES
************************** */
bool mute = 0;
State state = CONF;
int activePlayer;  // player whose turn it is
bool botReset = 0; // used when transitioning from BOT -> BOT
// holds type of each player; indeces parallel with playerColor
playerType players[4] = {NO_PLAYER, NO_PLAYER, NO_PLAYER, NO_PLAYER};

void setup() {
  pixels.begin();
  Serial.begin(9600);
}

// once a state is changed, its loop breaks and control returns here
void loop() {
  // update turn LED (will be overridden for conf)
  pixels.clear();
  updatePlayerLED(activePlayer);

  switch (state) {
  case CONF:
    configuration();
    break;
  case WAIT:
    waiting();
    break;
  case BOT:
    botTurn();
    break;
  case HUMAN_ROLL:
    humanRoll();
    break;
  case HUMAN_TURN:
    humanTurn();
    break;
  }
}