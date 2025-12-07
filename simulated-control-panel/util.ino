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

// display victory message on player finish
void victory(int player) {
  playSound(VICTORY_SOUND);
  lcdBuffer[0] = prettyPlayerColors[player] + " Has";
  lcdBuffer[1] = "Finished!";
  printToLcd();
  // block control for victory sequence
  unsigned long stopTime = millis() + 3500UL;
  while (millis() < stopTime) {
    rtttl::play();
  }
}

// called by handleConfStart
void sendPlayers() {
  for (playerType p : players) {
    Serial.print(p);
  }
  Serial.println();
}