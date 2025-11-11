/*
  Trouble Bot - Game Setup Controller
  -----------------------------------
  Hardware:
    - 4 WS2812B LEDs (1 per player) on pin 6
    - 5 pushbuttons (to GND, using INPUT_PULLUP)
      Blue: 2, Red: 3, Green: 4, Yellow: 5, Start: 7
    - 16x2 I2C LCD
    - Uses Bounce2, Adafruit_NeoPixel, and LiquidCrystal_I2C libraries
*/

#include <Bounce2.h>
#include <Adafruit_NeoPixel.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>

// ====== CONFIG ======
#define LED_PIN       6
#define NUM_LEDS      4
#define LCD_ADDR      0x27   // Common I2C LCD address; change if needed
#define LCD_COLS      16
#define LCD_ROWS      2

// Player buttons
#define BTN_BLUE      2
#define BTN_RED       3
#define BTN_GREEN     4
#define BTN_YELLOW    5
#define BTN_START     7

// ====== ENUMS / CONSTANTS ======
enum PlayerType { NONE, HUMAN, EASY, MEDIUM, HARD };
const char* PLAYER_TYPE_NAMES[] = { "None", "Human", "Easy", "Medium", "Hard" };

// LED colors (RGB)
uint32_t COLOR_NONE, COLOR_HUMAN, COLOR_EASY, COLOR_MEDIUM, COLOR_HARD;

// ====== GLOBALS ======
Bounce btnBlue = Bounce();
Bounce btnRed = Bounce();
Bounce btnGreen = Bounce();
Bounce btnYellow = Bounce();
Bounce btnStart = Bounce();

Adafruit_NeoPixel pixels(NUM_LEDS, LED_PIN, NEO_GRB + NEO_KHZ800);
LiquidCrystal_I2C lcd(LCD_ADDR, LCD_COLS, LCD_ROWS);

PlayerType playerStates[NUM_LEDS] = { NONE, NONE, NONE, NONE };

// ====== FUNCTIONS ======
void setupLEDColors() {
  COLOR_NONE   = pixels.Color(0, 0, 0);
  COLOR_HUMAN  = pixels.Color(0, 0, 255);   // Blue
  COLOR_EASY   = pixels.Color(0, 255, 0);   // Green
  COLOR_MEDIUM = pixels.Color(255, 128, 0); // Orange
  COLOR_HARD   = pixels.Color(255, 0, 0);   // Red
}

void updateLEDs() {
  for (int i = 0; i < NUM_LEDS; i++) {
    switch (playerStates[i]) {
      case HUMAN:  pixels.setPixelColor(i, COLOR_HUMAN);  break;
      case EASY:   pixels.setPixelColor(i, COLOR_EASY);   break;
      case MEDIUM: pixels.setPixelColor(i, COLOR_MEDIUM); break;
      case HARD:   pixels.setPixelColor(i, COLOR_HARD);   break;
      default:     pixels.setPixelColor(i, COLOR_NONE);   break;
    }
  }
  pixels.show();
}

void showLCDMessage(int playerIndex) {
  lcd.clear();
  String playerName;
  switch (playerIndex) {
    case 0: playerName = "Blue"; break;
    case 1: playerName = "Red"; break;
    case 2: playerName = "Green"; break;
    case 3: playerName = "Yellow"; break;
  }
  lcd.setCursor(0, 0);
  lcd.print(playerName + " Player");
  lcd.setCursor(0, 1);
  lcd.print(PLAYER_TYPE_NAMES[playerStates[playerIndex]]);
}

void cyclePlayerType(int playerIndex) {
  playerStates[playerIndex] = (PlayerType)((playerStates[playerIndex] + 1) % 5);
  updateLEDs();
  showLCDMessage(playerIndex);
}

int countActivePlayers() {
  int count = 0;
  for (int i = 0; i < NUM_LEDS; i++) {
    if (playerStates[i] != NONE) count++;
  }
  return count;
}

// ====== SETUP ======
void setup() {
  Serial.begin(9600);

  pixels.begin();
  setupLEDColors();
  updateLEDs();

  lcd.init();
  lcd.backlight();
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Game Setup Mode");

  // Configure buttons
  pinMode(BTN_BLUE, INPUT_PULLUP);
  pinMode(BTN_RED, INPUT_PULLUP);
  pinMode(BTN_GREEN, INPUT_PULLUP);
  pinMode(BTN_YELLOW, INPUT_PULLUP);
  pinMode(BTN_START, INPUT_PULLUP);

  btnBlue.attach(BTN_BLUE);    btnBlue.interval(20);
  btnRed.attach(BTN_RED);      btnRed.interval(20);
  btnGreen.attach(BTN_GREEN);  btnGreen.interval(20);
  btnYellow.attach(BTN_YELLOW);btnYellow.interval(20);
  btnStart.attach(BTN_START);  btnStart.interval(20);
}

// ====== LOOP ======
void loop() {
  btnBlue.update();
  btnRed.update();
  btnGreen.update();
  btnYellow.update();
  btnStart.update();

  if (btnBlue.fell())   cyclePlayerType(0);
  if (btnRed.fell())    cyclePlayerType(1);
  if (btnGreen.fell())  cyclePlayerType(2);
  if (btnYellow.fell()) cyclePlayerType(3);

  // Start button pressed
  if (btnStart.fell()) {
    int active = countActivePlayers();
    lcd.clear();
    if (active >= 2) {
      lcd.setCursor(0, 0);
      lcd.print("Starting Game...");
      Serial.println("start");
      delay(1000);
      lcd.clear();
      lcd.print("Game Started!");
    } else {
      lcd.setCursor(0, 0);
      lcd.print("Need 2 Players!");
      lcd.setCursor(0, 1);
      lcd.print("Currently: " + String(active));
      delay(1500);
      lcd.clear();
      lcd.print("Game Setup Mode");
    }
  }
}
