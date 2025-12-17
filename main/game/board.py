from game.player import Player
from typing import Optional
from game.constants import ROLL_AGAIN, BOARD_X, BOARD_Y, DIRECTION_MAP, MAGNET_PIN
from game.plotter import Plotter


class Board:
    def __init__(self):
        self.board: list[list[Optional[Player]]] = [
            [None] * BOARD_Y for _ in range(BOARD_X)
        ]
        self.plotter = Plotter(magnet_pin=MAGNET_PIN)
        self.plotter.go_to((0, 0))

    def populate(self, players: list[Player]):
        """Place all players on the board at their home positions."""
        for p in players:
            x, y = p.pos
            self.board[x][y] = p

    def test_move(self, players: list[Player], roll: int, player: Player) -> int:
        """Test helper: reset board to provided state, then move the selected player."""
        if player not in players:
            raise ValueError("player must be one of the provided players")

        # reset board then place each player at its current coordinates
        self.board = [[None for _ in range(BOARD_Y)] for _ in range(BOARD_X)]
        for p in players:
            x, y = p.pos
            if not (0 <= x < BOARD_X and 0 <= y < BOARD_Y):
                raise ValueError(f"player {p} position {p.pos} out of bounds")
            if self.board[x][y] is not None:
                raise ValueError(
                    f"multiple players share position {p.pos}: {self.board[x][y]} and {p}"
                )
            self.board[x][y] = p

        return self.move(player, roll)

    def _track_step(self, pos: tuple[int, int], roll: int) -> tuple[int, int]:
        x, y = pos
        while roll > 0:
            if x == 0 and 0 <= y < 4:  # bottom
                move = min(roll, 4 - y)
                roll -= move
                y += move
            if y == 4 and 0 <= x < 7 and roll > 0:  # left
                move = min(roll, 7 - x)
                roll -= move
                x += move
            if x == 7 and 0 < y <= 4 and roll > 0:  # top
                move = min(roll, y)
                roll -= move
                y -= move
            if y == 0 and 0 < x <= 7 and roll > 0:  # left
                move = min(roll, x)
                roll -= move
                x -= move
        return (x, y)

    def _track_move(self, p: Player, roll: int) -> None:
        x, y = p.pos
        while roll > 0:
            if x == 0 and 0 <= y < 4:  # bottom
                move = min(roll, 4 - y)
                roll -= move
                self.low_level_move(p, "LEFT", move)
                x, y = p.pos
            if y == 4 and 0 <= x < 7 and roll > 0:  # left
                move = min(roll, 7 - x)
                roll -= move
                self.low_level_move(p, "LEFT", move)
                x, y = p.pos
            if x == 7 and 0 < y <= 4 and roll > 0:  # top
                move = min(roll, y)
                roll -= move
                self.low_level_move(p, "LEFT", move)
                x, y = p.pos
            if y == 0 and 0 < x <= 7 and roll > 0:  # left
                move = min(roll, x)
                roll -= move
                self.low_level_move(p, "LEFT", move)
                x, y = p.pos

    def _calc_distance(self, start, stop) -> int:
        distance = 0
        while start != stop:
            start = self._track_step(start, 1)
            distance += 1
        return distance

    def get_move_desc(
        self, player: Player, roll: int
    ) -> Optional[tuple[tuple[int, int], tuple[int, int]]]:
        """Calculate the move description (from position, to position) for a given roll."""
        if player.locked:
            player.locked = roll != ROLL_AGAIN
            return None
        target = self._track_step(player.pos, roll)
        t_piece = self.board[target[0]][target[1]]
        if t_piece and self.board[t_piece.home[0]][t_piece.home[1]]:
            # can't capture because home is blocked
            return None
        return (player.pos, target)

    def move(self, p: Player, roll: int, captured: bool = False) -> int:
        """
        returns true if the player moved to new space
        """
        desc = self.get_move_desc(p, roll)
        if not desc:
            return 0
        target = desc[1]

        # can decrease captured step until clear
        if captured:
            while self.board[target[0]][target[1]]:
                roll -= 1
                target = self._track_step(p.pos, roll)

        # is piece on target (never true for captured piece)?
        piece = self.board[target[0]][target[1]]
        if piece:
            # move target home (garunteed empty)
            distance = self._calc_distance(piece.pos, piece.home)
            while distance > 6:
                traveled = self.move(piece, 6, captured=True)
                distance -= traveled
            if distance > 0:
                self.move(piece, distance, captured=True)
            piece.locked = True

        # can now move the current piece
        # start by identifying scenario
        blockers = []
        sides: set[int] = set()
        corners: int = 0
        i: int = 1
        t = None
        while t != target:
            t = self._track_step(p.pos, i)
            piece = self.board[t[0]][t[1]]
            if piece:
                blockers.append(piece)
                if self._onCorner(piece):
                    corners += 1
                else:
                    # value doesn't matter here, just uniqueness
                    sides.add(self.side_perspective_transformation(piece))
            i += 1
        if not blockers:
            self._move_alpha(p, roll)
        elif len(sides) == 1 and corners == 0:
            self._move_A(p, roll, blockers)
        elif len(sides) == 2 and corners == 0:
            self._move_F(p, roll, blockers)
        elif len(blockers) == 1 and corners == 1:
            self._move_corner(p, roll, blockers[0])
        else:
            raise RuntimeError("Cannot handle scenario with blockers")

    def _move_alpha(self, p: Player, roll: int):
        self._track_move(p, roll)

    def _move_A(self, p: Player, roll: int, blockers: list[Player]):
        for b in blockers:
            p_trans = self.side_perspective_transformation(b)
            self.low_level_move(b, "UP", 2, p_trans)
        self._track_move(p, roll)
        for b in blockers:
            self.low_level_move(b, "DOWN", 2, p_trans)

    def _move_F(self, p: Player, roll: int, blockers: list[Player]):
        undo = []
        for b in blockers:
            p_trans = self.side_perspective_transformation(b)
            self.low_level_move(b, "UP", 3, p_trans)
            undo.append((b, "DOWN", p_trans))

        self._track_move(p, roll)

        for b, direction, p_trans in undo:
            self.low_level_move(b, direction, 3, p_trans)

    def _move_corner(self, p: Player, roll: int, b: Player):
        p_trans = self.side_perspective_transformation(b)
        self.low_level_move(b, "LEFT", 1, p_trans) # left
        self.low_level_move(b, "UP", 2, p_trans) # UP

        self._track_move(p, roll)

        # return
        self.low_level_move(b, "DOWN", 1, p_trans) # left
        self.low_level_move(b, "RIGHT", 1, p_trans) # up
        self.low_level_move(b, "DOWN", 1, p_trans) # left

    def _onCorner(self, p: Player) -> bool:
        return p.pos in [(0, 0), (0, 4), (7, 4), (7, 0)]

    def check_game_over(self, players: list[Player]) -> bool:
        """Return True if only 1 player remains."""
        return len(players) <= 1

    def side_perspective_transformation(self, player: Player) -> tuple[bool, bool]:
        """
        (swap x/y, swap sign)
        """
        x, y = player.pos
        if x == 0 and y < 4:  # Bottom
            return (False, False)
        elif x == 7 and y > 0:  # Top
            return (False, True)
        elif y == 0 and x > 0:  # Right
            return (True, False)
        else:  # Left (y == 0)
            return (True, True)

    def direction_transformation(
        self, p_trans: tuple[bool, bool], direction: str
    ) -> tuple[bool, bool]:
        try:
            d_trans = DIRECTION_MAP[direction]
        except KeyError:
            raise ValueError(f"Invalid direction: {direction}")
        # A'B'D+A'BD'+AB'CD'+ABCD+B'C'D+BC'D'
        a, b = p_trans
        c, d = d_trans
        x = a ^ c
        s = (
            not a
            and not b
            and d
            or not a
            and b
            and not d
            or a
            and not b
            and c
            and not d
            or a
            and b
            and c
            and d
            or not b
            and not c
            and d
            or b
            and not c
            and not d
        )
        return (x, s)

    def low_level_move(
        self,
        player: Player,
        direction: str,
        step: int,
        p_trans: Optional[tuple[bool, bool]] = None,
    ):
        if not p_trans:
            p_trans = self.side_perspective_transformation(player)
        # calculate target
        trans = self.direction_transformation(p_trans, direction)
        sign = -1 if trans[1] else 1

        x, y = player.pos

        if trans[0]:  # move along y-axis
            target = (x, y + sign * step)
        else:  # move along x-axis
            target = (x + sign * step, y)

        p = self.plotter
        # go to player
        print("PLOTTER: moving to player at", player.pos)
        p.go_to((x, y))

        # carry to target
        print("PLOTTER: carrying to", target)
        self.board[x][y] = None
        p.carry_to(target)
        player.pos = target
        self.board[target[0]][target[1]] = player
