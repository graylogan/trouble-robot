from game.player import Player

PLAYER_TO_HOME = {"BLUE": (0, 0), "RED": (0, 4), "GREEN": (7, 4), "YELLOW": (7, 0)}

class PlayerManager:
    """Manages players, turn order, and current player."""

    def __init__(self):
        self.players: list[Player] = []
        self.current_index: int = 0

    def create_players(self, config: dict[str, str | None]) -> list[Player]:
        """Return a list of player objects from config dict."""
        for c in config:
            if config[c]:
              self.players.append(Player(c, config[c], PLAYER_TO_HOME[c]))

    def next_player(self) -> Player:
        """Advance to the next player and return it."""
        if not self.players:
            return None
        self.current_index = (self.current_index + 1) % len(self.players)
        return self.players[self.current_index]
