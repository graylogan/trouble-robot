class Player:
    """Represents a player in the game."""

    def __init__(self, color: str, type: str, home: tuple[int, int]):
        """
        Initialize a Player
        """

        # Extract color and type
        self.color: str = color
        self.type: str = type
        self.home: tuple[int, int] = home
        self.pos: tuple[int, int] = home
        self.locked: bool = True
        self.finished = 0

    def isHome(self) -> bool:
        return self.pos == self.home

    def __repr__(self) -> str:
        return f"<Player color={self.color}, type={self.type}, pos={self.pos}>"
