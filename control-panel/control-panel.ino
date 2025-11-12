#include <Keypad.h>

const uint8_t ROWS = 4;
const uint8_t COLS = 2;
char keys[ROWS][COLS] = {
  { 'B', 'S' },
  { 'R', 'D' },
  { 'G', 'M' },
  { 'Y', 'F' }
};

uint8_t colPins[COLS] = { 3, 2 }; // Pins connected to C1, C2, C3, C4
uint8_t rowPins[ROWS] = { 7, 6, 5, 4 }; // Pins connected to R1, R2, R3, R4

Keypad keypad = Keypad(makeKeymap(keys), rowPins, colPins, ROWS, COLS);

void setup() {
  Serial.begin(9600);
}

void loop() {
  char key = keypad.getKey();

  if (key != NO_KEY) {
    Serial.println(key);
  }
}