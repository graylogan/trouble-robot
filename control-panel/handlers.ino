void handleRed() {
  Serial.println("Red LED toggled");
}

void handleGreen() {

  Serial.println("Green LED toggled");
}

void handleBlue() {
  Serial.println("Blue LED toggled");
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

void pollKeys(bool buttonActive[8]) {
  char key = keypad.getKey();
  if (key == NO_KEY) return;
  if (!buttonActive[encodeKey(key)]) return;
  if (!mute || key == 'M') tone(9, 300, 100);
  switch (key) {
    case 'B':
      handleBlue();
      break;
    case 'R':
      handleRed();
      break;
    case 'G':
      handleGreen();
      break;
    case 'Y':
      // placeholder: handleYellow();
      break;
    case 'S':
      // placeholder: handleStart();
      break;
    case 'D':
      // placeholder: handleDice();
      break;
    case 'M':
      mute = (mute ? 0 : 1);
      break;
    case 'F':
      // placeholder: handleFix();
      break;
  }
}