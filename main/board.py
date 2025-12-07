class Board:
    """Tracks and updates game board state."""

    def update(self):
        """Update digital board to reflect camera (source of truth)."""
        pass

    def move(self, player):
        """
        for human: sends move request to CP
        for bot: gets move desc from CPU and sends to plotter
        """
        pass

    def check_finish(self, player):
        """Determine if the player has finished based on piece pos"""
        pass

    def check_game_over(self, players):
        """Return True if only 1 player remains."""
        return len(players) <= 1
