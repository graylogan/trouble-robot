void handleBlue() {
  players[BLUE_PLAYER] = (players[BLUE_PLAYER] + 1) % 5;
  updatePixels();
}

void handleRed() {
  players[RED_PLAYER] = (players[RED_PLAYER] + 1) % 5;
  updatePixels();
}

void handleGreen() {
  players[GREEN_PLAYER] = (players[GREEN_PLAYER] + 1) % 5;
  updatePixels();
}

void handleYellow() {
  players[YELLOW_PLAYER] = (players[YELLOW_PLAYER] + 1) % 5;
  updatePixels();
}

int encodeKey(char key) {
  switch (key) {
    case 'B': return 0;
    case 'R': return 1;
    case 'G': return 2;
    case 'Y': return 3;
    case 'S': return 4;
    case 'D': return 5;
    case 'M': return 6;
    case 'F': return 7;
    default: return -1;
  }
}

void pollKeys(void (*handlers[8])(void)) {
  char key = keypad.getKey();
  if (key == NO_KEY) return;
  int index = encodeKey(key);
  if (handlers[index] == nullptr) return;
  if (!mute || key == 'M') tone(9, 300, 100);
  handlers[index]();
}

void handleMute() {
  mute = (mute ? 0 : 1);
}

void handleConfStart() {
  // count players
  int numPlayers = 0;
  for (playerType p : players) {
    if (p != NO_PLAYER) numPlayers++;
  }
  if (numPlayers > 1) {
    pixels.clear();
    pixels.show();
    state = WAIT;
  }
  else {
    Serial.println("not enough players");
  }
}

void updatePixels() {
  for (int i = 0; i < 4; i++) {
    pixels.setPixelColor(3 - i, playerTypeLEDs[players[i]]);
  }
  pixels.show();
}