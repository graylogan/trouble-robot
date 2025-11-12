void alpha() {
  bool activeButton[8] = {1, 0, 0, 0, 0, 0, 1, 0}; // local array

  Serial.println("Entering state: alpha");

  while (state == ALPHA) {
    readSerial();
    pollKeys(activeButton); // pass the array to your function
  }
}

void beta() {
  bool activeButton[8] = {1, 1, 0, 0, 0, 0, 1, 0};

  Serial.println("Entering state: beta");

  while (state == BETA) {
    readSerial();
    pollKeys(activeButton);
  }
}

void gamma() {
  bool activeButton[8] = {1, 1, 1, 0, 0, 0, 1, 0};

  Serial.println("Entering state: gamma");

  while (state == GAMMA) {
    readSerial();
    pollKeys(activeButton);
  }
}
