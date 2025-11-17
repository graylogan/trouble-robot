/*
States define a list of handlers to pass to pollKeys
because key behavior is dependent on state. All handlers
must have no parameters and no return value.
*/

// not expecting serial comms, just buttons
void configuration() {
  // override default turn LED
  pixels.clear();
  pixels.show();

  // LCD
  lcdBuffer[0] = "Game Setup: Use";
  lcdBuffer[1] = "Player Buttons";
  printToLcd();

  void (*handlers[])(void) = {handleBlue,   handleRed,       handleGreen,
                              handleYellow, handleConfStart, nullptr,
                              handleMute,   nullptr};
  while (state == CONF) {
    pollKeys(handlers);
  }
}

// only used between states. Waiting for directions over serial
void waiting() {
  while (state == WAIT) {
    readSerial();
  }
}

// no key input, just listen to serial
void botTurn() {
  botReset = 0; // restore to prevent fall-through
  // always roll dice at start of bot turn
  // dice logic here
  Serial.println("dice rolled");
  while (state == BOT && !botReset) {
    readSerial();
  }
}

// no serial, just wait for dice press
void humanRoll() {
  void (*handlers[])(void) = {nullptr, nullptr,    nullptr,    nullptr,
                              nullptr, handleDice, handleMute, nullptr};
  while (state == HUMAN_ROLL) {
    pollKeys(handlers);
  }
}

// TODO!!!
void humanTurn() {
  void (*handlers[])(void) = {nullptr,         nullptr, nullptr,    nullptr,
                              handleTurnStart, nullptr, handleMute, nullptr};
  while (state == HUMAN_TURN) {
    pollKeys(handlers);
  }
}