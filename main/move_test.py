#!/usr/bin/env python3
"""Interactive driver for Board.test_move()."""

from game.board import Board
from game.constants import PLAYER_TO_HOME
from game.player import Player
import RPi.GPIO as GPIO
from typing import Optional


def read_position(label: str) -> Optional[tuple[int, int]]:
    while True:
        raw = input(f"Enter {label} position as 'x y': ").strip()
        try:
            if raw == "":
                return None
            x_str, y_str = raw.split()
            return int(x_str), int(y_str)
        except ValueError:
            print("Invalid input. Please provide two integers separated by a space.")


def read_roll() -> int:
    while True:
        raw = input("Enter roll value: ").strip()
        try:
            return int(raw)
        except ValueError:
            print("Invalid roll. Please enter an integer.")


def main():
    GPIO.setmode(GPIO.BOARD)
    print("=== Board.test_move() interactive driver ===")
    players = [
        Player("BLUE", "test", PLAYER_TO_HOME["RED"]),
        Player("RED", "test", PLAYER_TO_HOME["BLUE"]),
        Player("GREEN", "test", PLAYER_TO_HOME["GREEN"]),
        Player("YELLOW", "test", PLAYER_TO_HOME["YELLOW"]),
    ]

    board = Board()

    try:
        while True:
            print("\n--- New test ---")
            for p in players:
                p.locked = False
                position = read_position(p.color)
                if position:
                    p.pos = position

            roll = read_roll()
            moved = board.test_move(players, roll, players[0])
            print(f"Result: moved={bool(moved)}, roll={roll}, target={players[0].pos}")
    except KeyboardInterrupt:
        print("\nExiting test driver.")
    finally:
        try:
            board.plotter.close()
            GPIO.cleanup()
        except Exception:
            pass


if __name__ == "__main__":
    main()
