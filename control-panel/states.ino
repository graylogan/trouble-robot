/*
States are split into a one-time setup function and a recurring
tick function.
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
void waiting_setup() {}

void waiting_tick() { readSerial(); }

/* **************************
         BOT
************************** */
void bot_setup() {
  pixels.clear();
  updatePlayerTypeLED(activePlayer);
  showPlayerTurnLCD();
  // always roll dice at start of bot turn
  // dice logic here
  Serial.println("Bot rolled Dice!");
  changeState(WAIT);
}

void bot_tick() {}

/* **************************
         HUMAN ROLL
************************** */
void humanRoll_setup() {
  pixels.clear();
  updatePlayerTypeLED(activePlayer);
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
  pixels.clear();
  updatePlayerTypeLED(activePlayer);
  // indicate player's turn
  lcdBuffer[0] = "Make Your";
  lcdBuffer[1] = "Move";
  printToLcd();
}

void humanTurn_tick() { pollKeys(humanTurnHandlers); }