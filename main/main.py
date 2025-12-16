#!/usr/bin/env python3
from game.game import Game
import RPi.GPIO as GPIO


def run() -> None:
    GPIO.setmode(GPIO.BOARD)
    game = Game()
    game.run()
    GPIO.cleanup()


if __name__ == "__main__":
    run()
