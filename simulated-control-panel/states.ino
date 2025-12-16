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
  playSound(UNMUTE_SOUND);
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
  playSound(UNMUTE_SOUND);
  pixels.clear();
  updatePlayerTypeLED(activePlayer);
  showPlayerTurnLCD();
  rollCount = dice.numRolls;
  dice.roll(100);
}

void bot_tick() {
  dice.tick();
  // check if dice has been rolled this turn
  if (dice.numRolls > rollCount) {
    Serial.println("Bot rolled Dice!");
    changeState(WAIT);
  }
}

/* **************************
         HUMAN ROLL
************************** */
void humanRoll_setup() {
  playSound(UNMUTE_SOUND);
  pixels.clear();
  updatePlayerTypeLED(activePlayer);
  // show prompt to press dice
  lcdBuffer[0] = "Press Dice";
  lcdBuffer[1] = "to roll";
  printToLcd();
  rollCount = dice.numRolls;
}

void humanRoll_tick() {
  pollKeys(humanRollHandlers);
  dice.tick();
  // check if dice has been rolled this turn
  if (dice.numRolls > rollCount) {
    Serial.println("Human rolled Dice!");
    changeState(WAIT);
  }
}

/* **************************
         HUMAN TURN
************************** */
void humanTurn_setup() {
  playSound(UNMUTE_SOUND);
  pixels.clear();
  updatePlayerTypeLED(activePlayer);
  // indicate player's turn
  lcdBuffer[0] = "Make Your";
  lcdBuffer[1] = "Move";
  printToLcd();
}

void humanTurn_tick() { pollKeys(humanTurnHandlers); }