void configuration() {
  void (*handlers[])(void) = { handleBlue, handleRed, handleGreen, handleYellow, handleConfStart, nullptr, handleMute, nullptr };
  while (state == CONF) {
    pollKeys(handlers);
  }
}

void waiting() {
  while (state == WAIT) {
    readSerial();
  }
}

void botTurn() {
  Serial.println("bots be like");
  updatePlayerLED(activePlayer);
  pixels.show();
  while(true);
}