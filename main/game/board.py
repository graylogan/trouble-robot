from game.player import Player
from typing import Optional
from game.game import ROLL_AGAIN
from game.plotter import Plotter

BOARD_X = 8
BOARD_Y = 5

DIRECTION_MAP = {
    "UP":    (False, False),
    "DOWN":  (False, True),
    "LEFT":  (True, True),
    "RIGHT": (True, False),
}

class board:
  def __init__(self):
    self.board: list[list[Optional[Player]]] = [[None] * BOARD_Y for _ in range(BOARD_X)]

  def populate(self, players: list[Player]):
    """Place all players on the board at their home positions."""
    for p in players:
      x, y = p.pos
      self.board[x][y] = p

  def get_move_desc(self, player: Player, roll: int) -> Optional[tuple[tuple[int, int], tuple[int, int]]]:
    """Calculate the move description (from position, to position) for a given roll."""
    if player.locked:
      player.locked = roll != ROLL_AGAIN
      return None
    # For 2D board, we need to implement the path logic
    # This is a simplified version - adjust based on your actual game rules
    from_pos = player.pos
    # Calculate next position based on roll (this depends on your board layout)
    to_pos = from_pos  # Placeholder - implement your movement logic
    return (from_pos, to_pos)

  def check_game_over(self, players: list[Player]) -> bool:
    """Return True if only 1 player remains."""
    return len(players) <= 1

  def side_perspective_transformation(player: Player) -> tuple[bool, bool]:
    """
    (swap x/y, swap sign)
    """
    x, y = player.pos
    if x == 0:  # Bottom
      return (False, False)
    elif x == BOARD_X - 1:  # Top
      return (False, True)
    elif y == BOARD_Y - 1:  # Right
      return (True, True)
    else:  # Left (y == 0)
      return (True, False)
  
  def direction_transformation(self, p_trans: tuple[bool, bool], direction: str) -> tuple[bool, bool]:
      try:
          d_trans = DIRECTION_MAP[direction]
      except KeyError:
          raise ValueError(f"Invalid direction: {direction}")

      return tuple(a ^ b for a, b in zip(p_trans, d_trans))


  def low_level_move(self, player: Player, direction: str, step: int, p_trans: tuple[bool, bool], p: Plotter):
      # calculate target
      trans = self.direction_transformation(p_trans, direction)
      sign = -1 if trans[1] else 1

      x = player.gridPos["x"]
      y = player.gridPos["y"]

      if trans[0]:  # move along y-axis
          target = (x, y + sign * step)
      else:         # move along x-axis
          target = (x + sign * step, y)

      # go to player
      p.go_to((x, y))

      # carry to target
      p.carry_to(target)