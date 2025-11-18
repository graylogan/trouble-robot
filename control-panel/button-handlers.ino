/* **************************
         PLAYER BUTTONS
************************** */

void handleBlue() {
  // advance player type and update LED
  players[BLUE_PLAYER] = (players[BLUE_PLAYER] + 1) % 5;
  updatePlayerTypeLED(BLUE_PLAYER);
  showPlayerTypeLCD(BLUE_PLAYER);
}

void handleRed() {
  players[RED_PLAYER] = (players[RED_PLAYER] + 1) % 5;
  updatePlayerTypeLED(RED_PLAYER);
  showPlayerTypeLCD(RED_PLAYER);
}

void handleGreen() {
  players[GREEN_PLAYER] = (players[GREEN_PLAYER] + 1) % 5;
  updatePlayerTypeLED(GREEN_PLAYER);
  showPlayerTypeLCD(GREEN_PLAYER);
}

void handleYellow() {
  players[YELLOW_PLAYER] = (players[YELLOW_PLAYER] + 1) % 5;
  updatePlayerTypeLED(YELLOW_PLAYER);
  showPlayerTypeLCD(YELLOW_PLAYER);
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
    // send players to main and change state
    sendPlayers();
    changeState(WAIT);
  } else {
    lcdBuffer[0] = "Need at Least";
    lcdBuffer[1] = "2 Players";
    printToLcd();
    errorSound();
  }
}

void handleTurnStart() {
  Serial.println("Human completed Turn!");
  changeState(WAIT);
}

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
  changeState(WAIT);
}