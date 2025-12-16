/* **************************
         PLAYER BUTTONS
************************** */

void handleBlue() {
  // advance player type and update LED
  players[BLUE_PLAYER] = (players[BLUE_PLAYER] + 1) % 5;
  showPlayerTypeLCD(BLUE_PLAYER);
}

void handleRed() {
  players[RED_PLAYER] = (players[RED_PLAYER] + 1) % 5;
  showPlayerTypeLCD(RED_PLAYER);
}

void handleGreen() {
  players[GREEN_PLAYER] = (players[GREEN_PLAYER] + 1) % 5;
  showPlayerTypeLCD(GREEN_PLAYER);
}

void handleYellow() {
  players[YELLOW_PLAYER] = (players[YELLOW_PLAYER] + 1) % 5;
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
    playSound(BUTTON_SOUND);
    sendPlayers();
    changeState(WAIT);
  } else {
    lcdBuffer[0] = "Need at Least";
    lcdBuffer[1] = "2 Players";
    printToLcd();
    playSound(ERROR_SOUND);
  }
}

void handleTurnStart() {
  playSound(BUTTON_SOUND);
  Serial.println("Human completed Turn!");
  changeState(WAIT);
}

/* **************************
         MUTE BUTTON
************************** */

void handleMute() {
  (mute ? rtttl::begin(BUZZER_PIN, UNMUTE_SOUND)
        : rtttl::begin(BUZZER_PIN, MUTE_SOUND));
  mute = !mute;
}

/* **************************
         DICE BUTTON
************************** */

void handleDice() { dice.roll(1000); }