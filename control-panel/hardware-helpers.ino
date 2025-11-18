// updates the players LED to reflect current player type
void updatePlayerTypeLED(int player) {
  pixels.setPixelColor(3 - player, LED_COLORS[players[player]]);
  pixels.show();
}

// update LCD with current player turn
void showPlayerTurnLCD() {
  lcdBuffer[0] = prettyPlayerColors[activePlayer] + " Turn";
  lcdBuffer[1] = "";
  printToLcd();
}

// show player and type on LCD during configuration
void showPlayerTypeLCD(int playerIndex) {
  lcdBuffer[0] = prettyPlayerColors[playerIndex] + " Player";
  lcdBuffer[1] = prettyPlayerTypes[players[playerIndex]];
  printToLcd();
}

// prints lcdBuffer content to display
void printToLcd() {
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print(lcdBuffer[0]);
  lcd.setCursor(0, 1);
  lcd.print(lcdBuffer[1]);
}

// Start the non-blocking error sound sequence. This returns immediately
// and the sequence is driven by `handleErrorSound()` which should be
// called from `loop()` while `errorSoundActive` is true.
void errorSound() {
  if (!errorSoundActive) {
    errorSoundActive = true;
    errorSoundPhase = 0;
    errorSoundNextMillis = 0;
  }
}

// Drive the error sound sequence without blocking using millis().
// Phases:
// 0 - start first tone (100ms) and schedule second tone after 100+75 ms
// 1 - start second tone (200ms) and schedule end after 200 ms
// 2 - finish and deactivate
void handleErrorSound() {
  if (!errorSoundActive)
    return;

  unsigned long now = millis();
  if (errorSoundPhase == 0) {
    // start first tone for 100 ms
    tone(9, 100, 100);
    errorSoundNextMillis = now + 100UL + 75UL; // wait for tone + pause
    errorSoundPhase = 1;
  } else if (errorSoundPhase == 1) {
    if ((long)(now - errorSoundNextMillis) >= 0) {
      // start second tone for 200 ms
      tone(9, 100, 200);
      errorSoundNextMillis = now + 200UL;
      errorSoundPhase = 2;
    }
  } else if (errorSoundPhase == 2) {
    if ((long)(now - errorSoundNextMillis) >= 0) {
      // sequence complete
      errorSoundActive = false;
      errorSoundPhase = 0;
    }
  }
}