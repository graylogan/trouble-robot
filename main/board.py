from constants import BOARD_SIZE, ROLL_AGAIN, encode_player_color
from typing import Optional
from player import Player

class Board:
    """Tracks and updates game board state."""
    def __init__(self):
        board: list[Optional[Player]] = [None] * BOARD_SIZE

    def populate(self, players: list[Player]):
        for p in players:
            self.board[p.pos] = p

    def update(self) -> None: # CV IMPLEMENTATION HERE
        """Update digital board to reflect camera (source of truth)."""
        pass

    def get_move_desc(self, player: Player, roll: int) -> Optional[tuple[int, int]]:
        if player.locked:
            player.locked = roll != ROLL_AGAIN
            return None
        if player.traveled + roll > BOARD_SIZE:
            return None
        return (player.pos, (player.pos + roll) % BOARD_SIZE)
    
    def move(self, player: Player, desc: Optional[tuple[int, int]], cp):
        """
        for human: sends move request to CP
        for bot: gets move desc from CPU and sends to plotter
        """
        if not desc:
            print("No moves available")
            return
        if player.type == "human":
            cp.send_move_request(encode_player_color[player.color])
            if cp.wait_for_move_complete():
                print("✅ Human completed move")
                return
        # ELSE EXECUTE MOVE WITH PLOTTER
        # move blocking pieces
        i = desc[0]
        traveled = 0
        while i != desc[1]:
            if self.board[i]:
                print("temporarily moving", self.board[i])
            i = (i + 1) % BOARD_SIZE
            traveled += 1
        # send target home
        if self.board[desc[1]]:
            print("sending home:", self.board[desc[1]])
            self.board[desc[1]].locked = 1
            # SEND HOME CODE
        # move piece
        print("moving piece...")
        # MOVE CODE
        player.pos = desc[1]
        player.traveled += traveled
        if (player.traveled == BOARD_SIZE):
            player.finished = 1
        


    def check_game_over(self, players: list[Player]) -> bool:
        """Return True if only 1 player remains."""
        return len(players) <= 1
