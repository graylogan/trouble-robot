from serial_protocol import ControlPanelProtocol
from player_manager import PlayerManager
from board import Board

class Game:
    """Main game loop orchestrator."""

    def __init__(self):
        self.cp = ControlPanelProtocol()
        self.board = Board()
        self.players_manager = PlayerManager()
        self.game_over = False
        self.roll_value = 0

    def run(self):
        """Run the tabletop game."""
        self.establish_connections()
        config = self.cp.wait_for_config()
        self.players_manager.create_players(config)
        for p in self.players_manager.players:
            print(p)
        self.players_manager.determine_order()

        while not self.game_over and self.players_manager.players:
            player = self.players_manager.players[self.players_manager.current_index]
            self.roll_value = 0

            while self.roll_value != 6:
                self.roll_value = self.roll(player)
                self.board.move(player)
                self.board.update()

            if self.board.check_finish(player):
                self.cp.send_victory(player)
                self.players_manager.players.remove(player)
                self.game_over = self.board.check_game_over(self.players_manager.players)

            if self.players_manager.players:  # Only advance if players remain
                self.players_manager.next_player()
    
    def roll(self, player):
        """request roll from cp, read value, return value"""

    def establish_connections(self):
        self.cp.connect()