void configuration() {
  void (*handlers[])(void) = { handleBlue, handleRed, handleGreen, handleYellow, handleConfStart, nullptr, handleMute, nullptr };
  while (state == CONF) {
    pollKeys(handlers);
  }
}

void waiting() {
  Serial.println("entering waiting");
  while(1);
}