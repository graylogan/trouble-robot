#include "Dice.h"
#include <Adafruit_NeoPixel.h>
#include <Keypad.h>
#include <LiquidCrystal.h>
#include <NonBlockingRtttl.h>

/* **************************
         KEYPAD SETUP
************************** */
const uint8_t KEY_ROWS = 4;
const uint8_t KEY_COLS = 2;
const char KEY_LABELS[KEY_ROWS][KEY_COLS] = {
    {'B', 'S'}, {'R', 'D'}, {'G', 'M'}, {'Y', 'F'}};
const uint8_t KEY_COL_PINS[KEY_COLS] = {13, 12};
const uint8_t KEY_ROW_PINS[KEY_ROWS] = {11, 10, 9, 8};
Keypad keypad = Keypad(makeKeymap(KEY_LABELS), KEY_ROW_PINS, KEY_COL_PINS,
                       KEY_ROWS, KEY_COLS);

/* **************************
         LCD SETUP
************************** */
LiquidCrystal lcd(7, 6, 5, 4, 3, 2);
String lcdBuffer[2]; // store 2 lines

/* **************************
         ENUMS
************************** */

// indeces parallel with LED_COLORS
enum playerType { NO_PLAYER, HUMAN, EASY, MEDIUM, HARD };
String prettyPlayerTypes[] = {"None", "Human", "Easy", "Medium", "Hard"};

enum playerColor { BLUE_PLAYER, RED_PLAYER, GREEN_PLAYER, YELLOW_PLAYER };
String prettyPlayerColors[] = {"Blue", "Red", "Green", "Yellow"};

enum State { CONF, WAIT, BOT, HUMAN_ROLL, HUMAN_TURN };

/* **************************
      SOUND VARS
************************** */
const int BUZZER_PIN = A5;
const char *ERROR_SOUND = "error:d=4,o=7,b=600:c,8P,16P,2c";
const char *MUTE_SOUND = "mute:d=4,o=7,b=600:f,8P,c";
const char *UNMUTE_SOUND = "unmute:d=4,o=7,b=600:c,8P,f";
const char *BUTTON_SOUND = "unmute:d=4,o=7,b=600:a";
const char *VICTORY_SOUND =
    "victory:d=4,o=8,b=280:16d5,16p,32p,16d5,16p,32p,16d5,"
    "16p,32p,2d5,2a#4,2c5,8d5,4p,8c5,1d5";

/* **************************
      DICE SETUP
************************** */
const int DICE_PIN = A3;
Dice dice(DICE_PIN);
// check increase in count to determine roll complettion
int rollCount;

/* **************************
      GLOBAL VARIABLES
************************** */
bool mute = 0;
State state = CONF;
int activePlayer; // player whose turn it is
// holds type of each player; indeces parallel with playerColor
playerType players[4] = {NO_PLAYER, NO_PLAYER, NO_PLAYER, NO_PLAYER};

void setup() {
  pinMode(BUZZER_PIN, OUTPUT);
  pinMode(DICE_PIN, OUTPUT);
  Serial.begin(9600);
  lcd.begin(16, 2);
  lcd.clear();
  configuration_setup();
}

void loop() {
  // tick the current state once per loop iteration
  switch (state) {
  case CONF:
    configuration_tick();
    break;
  case WAIT:
    waiting_tick();
    break;
  case BOT:
    bot_tick();
    break;
  case HUMAN_ROLL:
    humanRoll_tick();
    break;
  case HUMAN_TURN:
    humanTurn_tick();
    break;
  }
  rtttl::play(); // play current sound
}

// changes the state and calls the setup function for that state
void changeState(int newState) {
  state = newState;
  switch (newState) {
  case CONF:
    configuration_setup();
    break;
  case WAIT:
    waiting_setup();
    break;
  case BOT:
    bot_setup();
    break;
  case HUMAN_ROLL:
    humanRoll_setup();
    break;
  case HUMAN_TURN:
    humanTurn_setup();
    break;
  }
}