from constants import BOARD_SIZE, ROLL_AGAIN, encode_player_color
from typing import Optional
from player import Player

class Board:
    """Tracks and updates game board state."""
    def __init__(self):
        board: list[Optional[Player]] = [None] * BOARD_SIZE

    def update(self) -> None:
        """Update digital board to reflect camera (source of truth)."""
        pass

    def get_move_desc(self, player: Player, roll: int) -> Optional[tuple[int, int]]:
        if player.locked:
            player.locked = roll != ROLL_AGAIN
            return None
        if player.traveled + roll > 22:
            return None
        return (player.pos, (player.pos + roll) % BOARD_SIZE)
    
    def move(self, player: Player, desc: Optional[tuple[int, int]], cp):
        """
        for human: sends move request to CP
        for bot: gets move desc from CPU and sends to plotter
        """
        if not desc:
            return
        if player.type == "human":
            cp.send_move_request(encode_player_color[player.color])
            if cp.wait_for_move_complete():
                print("✅ Human completed move")
                return
        # ELSE EXECUTE MOVE WITH PLOTTER

    def check_finish(self, player: Player):
        """Determine if the player has finished based on piece pos"""
        pass

    def check_game_over(self, players: list[Player]) -> bool:
        """Return True if only 1 player remains."""
        return len(players) <= 1
