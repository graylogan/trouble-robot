from serial_protocol import ControlPanelProtocol
from player_manager import PlayerManager
from board import Board
from player import Player

encode_player_color = {"BLUE": PlayerColor.BLUE, "RED": PlayerColor.RED, "GREEN": PlayerColor.GREEN, "YELLOW": PlayerColor.YELLOW}
ROLL_AGAIN: int = 6

class Game:
    """Main game loop orchestrator."""

    def __init__(self):
        self.cp = ControlPanelProtocol()
        self.board = Board()
        self.players_manager = PlayerManager()
        self.game_over: bool = False
        self.roll_value: int = 0

    def run(self) -> None:
        """Run the tabletop game."""
        self.establish_connections()
        config: dict[str, str | None] = self.cp.wait_for_config()
        self.players_manager.create_players(config)
        self.board.populate(self.players_manager.players)
        self.determine_order()

        while not self.game_over and self.players_manager.players:
            player: Player = self.players_manager.players[self.players_manager.current_index]
            self.roll_value = 0

            while self.roll_value != ROLL_AGAIN:
                self.roll_value = self.roll(player)
                self.board.move(player)
                self.board.update()

            if player.finished:
                self.cp.send_victory(player)
                self.players_manager.players.remove(player)
                self.game_over = self.board.check_game_over(self.players_manager.players)

            self.players_manager.next_player()
    
    def roll(self, player) -> int:
        """request roll from cp, read value, return value"""
        self.cp.send_roll_request(encode_player_color[player.color])
        if self.cp.wait_for_dice_complete():
            return int(input("Enter roll: ")) # READ WITH CV HERE
        else:
            raise Exception("roll failed")

    def establish_connections(self) -> None:
        self.cp.connect()

    def determine_order(self) -> None:
      """Determine first player by roll and update players list."""
      # get player with highest roll (handles ties)
      remaining: list[Player] = [p for p in self.players_manager.players]
      while len(remaining) > 1:
          rolls: list[tuple[Player, int]] = []
          for p in remaining:
              roll = self.roll(p)
              if not rolls or rolls[0][1] == roll:
                  rolls.append((p, roll))
              elif roll > rolls[0][1]:
                  rolls = [(p, roll)]
              # else do nothing
          remaining = [r[0] for r in rolls]
      
      # remaining order goes clockwise starting from winner
      ordered: list[Player] = []
      i: int = self.players_manager.players.index(remaining[0])
      numPlayers: int = len(self.players_manager.players)
      for _j in range(numPlayers):
          ordered.append(self.players_manager.players[i])
          i = (i + 1) % numPlayers
      self.players_manager.players = ordered