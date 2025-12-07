class Player:
    """Represents a player in the game."""

    def __init__(self, color, type):
        """
        Initialize a Player
        """

        # Extract color and type
        self.color = color
        self.type = type
        self.pieces = []  # Initialize an empty list of pieces

    def __repr__(self):
        return f"<Player color={self.color}, type={self.type}, pieces={len(self.pieces)}>"
