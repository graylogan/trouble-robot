#ifndef DICE_H
#define DICE_H

#include <Arduino.h>

class Dice {
  int PIN;
  bool active;
  unsigned long finishTime;
  bool settling;

  public:
  int numRolls = 0;
  Dice(int pin) {
    PIN = pin;
    active = 0;
    numRolls = 0;
    settling = 0;
  }

  bool isActive() {
    return active;
  }

  // roll for t ms
  void roll(unsigned long t) {
    if (active) return;
    digitalWrite(PIN, HIGH);
    active = 1;
    finishTime = millis() + t;
  }

  void tick() {
    if (!active) return;
    if (millis() < finishTime) return;
    if (!settling) {
      digitalWrite(PIN, LOW);
      settling = 1;
    }
    if (millis() > finishTime + 5000) {
      active = 0;
      settling = 0;
      numRolls++;
    }
  }
};

#endif