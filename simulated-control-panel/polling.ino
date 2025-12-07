// checks for key presses and calls handlers specified by state function
void pollKeys(void (*handlers[8])(void)) {
  // immediately return if key not pressed or not listening
  char key = keypad.getKey();
  if (key == NO_KEY)
    return;
  int index = encodeKey(key);
  if (handlers[index] == nullptr)
    return;

  // play sound unless start or mute button
  if (index < 4 || index == 5 || index == 7) {
    playSound(BUTTON_SOUND);
  }
  // call handler
  handlers[index]();
}

// handle incoming serial messages
void readSerial() {
  if (Serial.available() > 0) {
    String input = Serial.readStringUntil('\n');
    input.trim(); // remove any \r or whitespace
    // parse information
    char tag = input.charAt(0);
    int player = input.charAt(1) - '0';
    bool isBot = players[player] - 1;

    switch (tag) {
    case 'R':
      // roll state depends on player type
      activePlayer = player;
      changeState((isBot ? BOT : HUMAN_ROLL));
      break;
    case 'T':
      // only humans have turn state
      activePlayer = player;
      if (!isBot)
        changeState(HUMAN_TURN);
      break;
    case 'V':
      victory(player);
    }
  }
}