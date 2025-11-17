// used to acquire index of appropriate handler
int encodeKey(char key) {
  switch (key) {
  case 'B':
    return 0;
  case 'R':
    return 1;
  case 'G':
    return 2;
  case 'Y':
    return 3;
  case 'S':
    return 4;
  case 'D':
    return 5;
  case 'M':
    return 6;
  case 'F':
    return 7;
  default:
    return -1;
  }
}

// checks for key presses and calls handlers specified by state function
void pollKeys(void (*handlers[8])(void)) {
  // immediately return if key not pressed or not listening
  char key = keypad.getKey();
  if (key == NO_KEY)
    return;
  int index = encodeKey(key);
  if (handlers[index] == nullptr)
    return;

  // play sound on keypress if not muted (unless mute button)
  if (!mute || key == 'M')
    tone(9, 300, 100);

  // call handler
  handlers[index]();
}

// if serial msg waiting, forward input to appropriate handler
void readSerial() {
  if (Serial.available() > 0) {
    String input = Serial.readStringUntil('\n');
    input.trim(); // remove any \r or whitespace
    switch (state) {
    case WAIT:
      waitSerial(input);
      break;
    case BOT:
      botSerial(input);
      break;
    }
  }
}

// called by handleConfStart
void sendPlayers() {
  for (playerType p : players) {
    Serial.print(p);
  }
  Serial.println();
}

//
void updatePlayerLED(int player) {
  pixels.setPixelColor(3 - player, playerTypeLEDs[players[player]]);
  pixels.show();
}

void updateTurnLCD(int playerIndex) {
  lcdBuffer[0] = prettyPlayerColor[playerIndex] + " Turn";
  lcdBuffer[1] = "";
  printToLcd();
}

void errorSound() {
  tone(9, 100, 100); // 100 Hz for 100 ms
  delay(100);
  delay(75);         // pause 50 ms
  tone(9, 100, 200); // 100 Hz for 200 ms
  delay(200);
}

void playerLCD(int playerIndex) {
  lcdBuffer[0] = prettyPlayerColor[playerIndex] + " Player";
  lcdBuffer[1] = prettyPlayerType[players[playerIndex]];
  printToLcd();
}

void printToLcd() {
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print(lcdBuffer[0]);
  lcd.setCursor(0, 1);
  lcd.print(lcdBuffer[1]);
}