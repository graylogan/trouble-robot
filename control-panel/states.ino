/*
States are split into a one-time setup function and a recurring
tick function. The loop() the tick each iteration.
*/

/* **************************
         HANDLER ARRAYS
************************** */
static void (*confHandlers[])(void) = {
    handleBlue,      handleRed, handleGreen, handleYellow,
    handleConfStart, nullptr,   handleMute,  nullptr};

static void (*humanRollHandlers[])(void) = {nullptr,    nullptr, nullptr,
                                            nullptr,    nullptr, handleDice,
                                            handleMute, nullptr};

static void (*humanTurnHandlers[])(void) = {
    nullptr,         nullptr, nullptr,    nullptr,
    handleTurnStart, nullptr, handleMute, nullptr};

/* **************************
         CONFIGURATION STATE
************************** */
void configuration_setup() {
  // LCD
  lcdBuffer[0] = "Game Setup: Use";
  lcdBuffer[1] = "Player Buttons";
  printToLcd();
}

void configuration_tick() { pollKeys(confHandlers); }

/* **************************
         WAITING
************************** */
void waiting_setup() {
  // could show a waiting message
  lcdBuffer[0] = "Waiting for";
  lcdBuffer[1] = "controller...";
  printToLcd();
}

void waiting_tick() { readSerial(); }

/* **************************
         BOT
************************** */
// no key input, just listen to serial
void bot_setup() {
  pixels.clear();
  updatePlayerLED(activePlayer);
  updateTurnLCD();
  // always roll dice at start of bot turn
  // dice logic here
  Serial.println("dice rolled");
}

void bot_tick() {
  // During bot turns we just read serial updates
  readSerial();
}

/* **************************
         HUMAN ROLL
************************** */
// no serial, just wait for dice press
void humanRoll_setup() {
  pixels.clear();
  updatePlayerLED(activePlayer);
  // show prompt to press dice
  lcdBuffer[0] = "Press Dice";
  lcdBuffer[1] = "to roll";
  printToLcd();
}

void humanRoll_tick() { pollKeys(humanRollHandlers); }

/* **************************
         HUMAN TURN
************************** */
void humanTurn_setup() {
  // indicate player's turn
  lcdBuffer[0] = "Make Your";
  lcdBuffer[1] = "Move";
  printToLcd();
}

void humanTurn_tick() { pollKeys(humanTurnHandlers); }