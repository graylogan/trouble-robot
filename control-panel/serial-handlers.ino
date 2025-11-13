// expecting to recieve next turn (encoded)
void waitSerial(String input) {
  // char -> int
  char c = input.charAt(0);
  activePlayer = c - '0';
  if (players[activePlayer] == HUMAN) {
    state =
        HUMAN_ROLL; //!!! NEED TO DISTINGUISH BETWEEN FIRST AND SUBSEQUENT TURNS
  } else {
    state = BOT;
  }
}

// REDUNDANT???
// expecting to recieve next turn (encoded)
void botSerial(String input) {
  char c = input.charAt(0);
  activePlayer = c - '0';
  if (players[activePlayer] == HUMAN) {
    state = HUMAN_ROLL;
  } else {
    botReset = 1;
  }
}