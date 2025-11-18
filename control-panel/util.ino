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

void updateTurnLCD() {
  lcdBuffer[0] = prettyPlayerColor[activePlayer] + " Turn";
  lcdBuffer[1] = "";
  printToLcd();
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

void changeState(int newState) {
  switch (newState) {
  case CONF:
    configuration_setup();
    break;
  case WAIT:
    waiting_setup();
    break;
  case BOT:
    bot_setup();
    break;
  case HUMAN_ROLL:
    humanRoll_setup();
    break;
  case HUMAN_TURN:
    humanTurn_setup();
    break;
  }
  state = newState;
}