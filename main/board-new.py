from player import Player
from typing import Optional
from constants import BOARD_X, BOARD_Y
from plotter_controller import PlotterController

DIRECTION_MAP = {
    "UP":    (False, False),
    "DOWN":  (False, True),
    "LEFT":  (True, True),
    "RIGHT": (True, False),
}

class board:
  def __init__(self):
    board: list[list[Optional[Player]]] = [[None] * BOARD_Y] * BOARD_X

  def side_perspective_transformation(player: Player) -> tuple[bool, bool]:
    """
    (swap x/y, swap sign)
    """
    pos = player.trackPos
    if (pos < BOARD_Y):
      return (False, False)
    elif (pos < BOARD_Y + BOARD_X - 1):
      return (True, True)
    elif (pos < 2 * BOARD_Y + BOARD_X - 2):
      return (True, False)
    else:
      return (False, True)
    

def direction_transformation(p_trans: tuple[bool, bool], direction: str) -> tuple[bool, bool]:
    try:
        d_trans = DIRECTION_MAP[direction]
    except KeyError:
        raise ValueError(f"Invalid direction: {direction}")

    return tuple(a ^ b for a, b in zip(p_trans, d_trans))


def low_level_move(player: Player, direction: str, step: int, p_trans: tuple[bool, bool], p: PlotterController):
    # calculate target
    trans = direction_transformation(p_trans, direction)
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