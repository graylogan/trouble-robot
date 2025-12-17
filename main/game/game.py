import time
import cv2

from game.serial_protocol import ControlPanelProtocol
from game.player_manager import PlayerManager
from game.board import Board
from game.player import Player
from game.constants import ROLL_AGAIN, ENCODE_PLAYER_COLOR
from game.camera import DiceCamera


class Game:
    """Main game loop orchestrator."""

    def __init__(self):
        # self.cp = ControlPanelProtocol()
        self.cp = ControlPanelProtocol(simulation=False, port="/dev/ttyACM0")
        self.board = Board()
        self.players_manager = PlayerManager()
        self.game_over: bool = False
        self.roll_value: int = 0

        # Camera handle lives on the instance so roll() can access it
        self.cam: DiceCamera | None = None

    def run(self) -> None:
        """Run the tabletop game."""
        self._establish_connections()

        # Start camera once, keep it running for the whole game
        self.cam = DiceCamera()
        self.cam.start()
        if not self.cam.wait_for_first_frame():
            raise RuntimeError("Camera never produced a frame")

        config: dict[str, str | None] = self.cp.wait_for_config()
        self.players_manager.create_players(config)
        self.board.populate(self.players_manager.players)

        print("GAME: created players. Determining order...")
        self.determine_order()
        print("GAME: order determined.")

        try:
            while not self.game_over and self.players_manager.players:
                frame = self.cam.get_latest_frame()
                if frame is None:
                    time.sleep(0.01)
                    continue

                print(self.board.board)
                player: Player = self.players_manager.players[
                    self.players_manager.current_index
                ]
                self.roll_value = ROLL_AGAIN

                moved = False
                while self.roll_value == ROLL_AGAIN:
                    print("GAME: rolling...")
                    self.roll_value = self.roll(player)
                    print("GAME: moving...")
                    moved = self.board.move(player, self.roll_value)
                    # self.board.update()  # would implement CV here
                if moved and player.isHome():
                    self.cp.send_victory(player)
                    self.players_manager.players.remove(player)
                    self.game_over = self.board.check_game_over(
                        self.players_manager.players
                    )

                self.players_manager.next_player()

        finally:
            if self.cam is not None:
                self.cam.stop()
                self.cam = None
            cv2.destroyAllWindows()
            self.board.plotter.close()

    def roll(self, player: Player) -> int:
        """Request roll from control panel, read value from camera, return value."""
        if self.cam is None:
            raise RuntimeError("Camera not initialized. Did you call run()?")
        self.cp.send_roll_request(ENCODE_PLAYER_COLOR[player.color])
        if self.cp.wait_for_dice_complete():
            count, mask, debug = self.cam.get_pips()
            # If something went wrong and we couldn't read a frame yet
            if count is None:
                raise RuntimeError("No camera frame available to read pips.")
            print("Pips:", count)
            if count < 1:
                count = 1
            elif count > 6:
                count = 6
            return count

        raise Exception("roll failed")

    def _establish_connections(self) -> None:
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
