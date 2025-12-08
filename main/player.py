class Player:
    """Represents a player in the game."""

    def __init__(self, color: str, type: str, home: int):
        """
        Initialize a Player
        """

        # Extract color and type
        self.color: str = color
        self.type: str = type
        self.pos: int = home
        self.locked: bool = True
        self.traveled: int = 0

    def __repr__(self) -> str:
        return f"<Player color={self.color}, type={self.type}, pos={self.pos}>"
