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

void playSound(char *sound) {
  if (!mute) {
    rtttl::begin(BUZZER_PIN, sound);
  }
}