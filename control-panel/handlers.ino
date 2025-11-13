void handleBlue() {
  players[BLUE_PLAYER] = (players[BLUE_PLAYER] + 1) % 5;
  updatePlayerLED(BLUE_PLAYER);
}

void handleRed() {
  players[RED_PLAYER] = (players[RED_PLAYER] + 1) % 5;
  updatePlayerLED(RED_PLAYER);
}

void handleGreen() {
  players[GREEN_PLAYER] = (players[GREEN_PLAYER] + 1) % 5;
  updatePlayerLED(GREEN_PLAYER);
}

void handleYellow() {
  players[YELLOW_PLAYER] = (players[YELLOW_PLAYER] + 1) % 5;
  updatePlayerLED(YELLOW_PLAYER);
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
    sendPlayers();
    state = WAIT;
  }
  else {
    Serial.println("not enough players");
  }
}

void sendPlayers() {
  for (playerType p : players) {
    Serial.print(p);
  }
  Serial.println();
}

void updatePlayerLED(int player) {
  pixels.setPixelColor(3 - player, playerTypeLEDs[players[player]]);
  pixels.show();
}

void waitSerial(String input) {
  Serial.println("wait serial");
  char c = input.charAt(0);
  activePlayer = c - '0';
  Serial.print(activePlayer);
  Serial.print(players[activePlayer]);
  Serial.println(players[activePlayer] == HUMAN);
  if (players[activePlayer] == HUMAN) {
    state = HUMAN_ROLL;
  }
  else {
    state = BOT;
  }
}