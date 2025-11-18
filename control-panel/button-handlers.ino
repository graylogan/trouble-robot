/* **************************
         PLAYER BUTTONS
************************** */

void handleBlue() {
  // advance player type and update LED
  players[BLUE_PLAYER] = (players[BLUE_PLAYER] + 1) % 5;
  updatePlayerLED(BLUE_PLAYER);
  playerLCD(BLUE_PLAYER);
}

void handleRed() {
  players[RED_PLAYER] = (players[RED_PLAYER] + 1) % 5;
  updatePlayerLED(RED_PLAYER);
  playerLCD(RED_PLAYER);
}

void handleGreen() {
  players[GREEN_PLAYER] = (players[GREEN_PLAYER] + 1) % 5;
  updatePlayerLED(GREEN_PLAYER);
  playerLCD(GREEN_PLAYER);
}

void handleYellow() {
  players[YELLOW_PLAYER] = (players[YELLOW_PLAYER] + 1) % 5;
  updatePlayerLED(YELLOW_PLAYER);
  playerLCD(YELLOW_PLAYER);
}

/* **************************
         START BUTTONS
************************** */

void handleConfStart() {
  // count players
  int numPlayers = 0;
  for (playerType p : players) {
    if (p != NO_PLAYER)
      numPlayers++;
  }
  if (numPlayers > 1) {
    // clear pixels, send to main, and change state
    pixels.clear();
    pixels.show();
    sendPlayers();
    changeState(WAIT);
  } else {
    // LCD logic here
    Serial.println("not enough players");
    errorSound();
  }
}

void handleTurnStart() {}

/* **************************
         MUTE BUTTON
************************** */

void handleMute() { mute = (mute ? 0 : 1); }

/* **************************
         DICE BUTTON
************************** */

void handleDice() {
  // dice roll logic here
  Serial.println("Human rolled dice!");
  changeState(HUMAN_TURN);
}