from player import Player

class PlayerManager:
    """Manages players, turn order, and current player."""

    def __init__(self):
        self.players = []
        self.current_index = 0

    def create_players(self, config):
        """Return a list of player objects from config dict."""
        pass
        for c in config:
            if config[c]:
              self.players.append(Player(c, config[c]))

    def determine_order(self):
        """Determine first player by roll and update players list."""
        pass

    def next_player(self):
        """Advance to the next player and return it."""
        if not self.players:
            return None
        self.current_index = (self.current_index + 1) % len(self.players)
        return self.players[self.current_index]
