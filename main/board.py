from constants import BOARD_SIZE
from typing import Optional
from player import Player

class Board:
    """Tracks and updates game board state."""
    def __init__(self):
        board: list[Optional[Player]] = [None] * BOARD_SIZE

    def update(self):
        """Update digital board to reflect camera (source of truth)."""
        pass

    def move(self, player: Player):
        """
        for human: sends move request to CP
        for bot: gets move desc from CPU and sends to plotter
        """
        pass

    def check_finish(self, player: Player):
        """Determine if the player has finished based on piece pos"""
        pass

    def check_game_over(self, players: list[Player]):
        """Return True if only 1 player remains."""
        return len(players) <= 1
