from game.player import Player
from typing import Optional
from game.constants import ROLL_AGAIN, BOARD_X, BOARD_Y, DIRECTION_MAP
from game.plotter import Plotter

class Board:
    def __init__(self):
        self.board: list[list[Optional[Player]]] = [
            [None] * BOARD_Y for _ in range(BOARD_X)
        ]

    def populate(self, players: list[Player]):
        """Place all players on the board at their home positions."""
        for p in players:
            x, y = p.pos
            self.board[x][y] = p

    def _track_step(self, pos: tuple[int, int], roll: int) -> tuple[int, int]:
        x, y = pos
        while roll > 0:
            if x == 0 and 0 <= y < 4: # bottom
                move = min(roll, 4 - y)
                roll -= move
                y += move
            if y == 4 and 0 <= x < 7 and roll > 0: # left
                move = min(roll, 7 - x)
                roll -= move
                x += move
            if x == 7 and 0 < y <= 4 and roll > 0: # top
                move = min(roll, y)
                roll -= move
                y -= move
            if y == 0 and 0 < x <= 7 and roll > 0: # left
                move = min(roll, x)
                roll -= move
                x -= move
        return (x, y)

    def get_move_desc(
        self, player: Player, roll: int
    ) -> Optional[tuple[tuple[int, int], tuple[int, int]]]:
        """Calculate the move description (from position, to position) for a given roll."""
        if player.locked:
            player.locked = roll != ROLL_AGAIN
            return None
        target = self._track_step(player.pos, roll)
        t_piece = self.board[target[0]][target[1]]
        t_home = t_piece.home
        if t_piece and self.board[t_home[0]][t_home[1]]:
            # can't capture because home is blocked
            return None
        return (player.pos, target)

    def move(self) -> bool:
        """
        returns true if the player moved to new space
        """
        pass

    def check_game_over(self, players: list[Player]) -> bool:
        """Return True if only 1 player remains."""
        return len(players) <= 1

    def side_perspective_transformation(self, player: Player) -> tuple[bool, bool]:
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

    def direction_transformation(
        self, p_trans: tuple[bool, bool], direction: str
    ) -> tuple[bool, bool]:
        try:
            d_trans = DIRECTION_MAP[direction]
        except KeyError:
            raise ValueError(f"Invalid direction: {direction}")

        return tuple(a ^ b for a, b in zip(p_trans, d_trans))

    def low_level_move(
        self,
        player: Player,
        direction: str,
        step: int,
        p_trans: tuple[bool, bool],
        p: Plotter,
    ):
        # calculate target
        trans = self.direction_transformation(p_trans, direction)
        sign = -1 if trans[1] else 1

        x, y = player.pos

        if trans[0]:  # move along y-axis
            target = (x, y + sign * step)
        else:  # move along x-axis
            target = (x + sign * step, y)

        # go to player
        p.go_to((x, y))

        # carry to target
        p.carry_to(target)
