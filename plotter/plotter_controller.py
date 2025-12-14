import time
from plotter_helpers import send_grbl
from magnet import turn_on_magnet, turn_off_magnet
# from constants import GRBL_COORDINATES

GRBL_COORDINATES = []

class PlotterController:
    def __init__(self, ser, start_index: tuple[int, int] = (0, 0)):
        """
        ser: open GRBL serial connection
        board: 2D array mapping (x, y) -> ("Xnnn", "Ynnn")
        start_index: (x, y)
        """
        self.ser = ser
        self.board = GRBL_COORDINATES
        self.current_index = start_index

    # -------------------------
    # Internal helpers
    # -------------------------

    def _index_to_grbl(self, index: tuple[int, int]) -> tuple[str, str]:
        x, y = index
        return self.board[x][y]

    # -------------------------
    # Public movement API
    # -------------------------

    def go_to_grbl(self, x_grbl: str | None = None, y_grbl: str | None = None):
      """
      Move plotter directly to explicit GRBL coordinates with magnet OFF.

      Example:
          go_to_grbl("X120.0", "Y45.0")
          go_to_grbl(x_grbl="X120.0")
          go_to_grbl(y_grbl="Y45.0")
      """
      if x_grbl is None and y_grbl is None:
          return

      if x_grbl is not None:
          send_grbl(self.ser, "G0 " + x_grbl)
          time.sleep(5)

      if y_grbl is not None:
          send_grbl(self.ser, "G0 " + y_grbl)
          time.sleep(5)


    def go_to(self, target_index: tuple[int, int]):
        """
        Move plotter to a board index with magnet OFF.
        No axis restrictions.
        """
        if target_index == self.current_index:
            return

        target_x, target_y = self._index_to_grbl(target_index)

        send_grbl(self.ser, "G0 " + target_x)
        time.sleep(5)

        send_grbl(self.ser, "G0 " + target_y)
        time.sleep(5)

        self.current_index = target_index

    def carry_to(self, target_index: tuple[int, int]):
        """
        Move plotter to a board index with magnet ON.
        Enforces single-axis movement.
        """
        if target_index == self.current_index:
            return

        current_x, current_y = self.current_index
        target_x, target_y = target_index
        x_grbl, y_grbl = self._index_to_grbl(target_index)

        turn_on_magnet()
        time.sleep(0.5)

        try:
            # Y movement only
            if current_x == target_x and current_y != target_y:
                send_grbl(self.ser, "G0 " + y_grbl)
                time.sleep(5)

            # X movement only
            elif current_y == target_y and current_x != target_x:
                send_grbl(self.ser, "G0 " + x_grbl)
                time.sleep(5)

            else:
                raise RuntimeError(
                    f"Illegal carry_to move: "
                    f"current_index={self.current_index}, "
                    f"target_index={target_index}. "
                    f"Can only move along one axis."
                )

            self.current_index = target_index

        finally:
            turn_off_magnet()
            time.sleep(0.2)
