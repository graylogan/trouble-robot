import time
import serial
from game.magnet import Magnet
from game.constants import GRBL_COORDINATES, BASE_SLEEP, UNIT_SLEEP


class Plotter:
    def __init__(
        self,
        ser: serial.Serial | None = None,
        start_index: tuple[int, int] = (0, 0),
        magnet_pin: int | None = None,
        port: str = "/dev/ttyUSB0",
        baud: int = 115200,
    ):
        """
        Unified plotter controller.

        Parameters:
        - ser: existing open GRBL serial connection. If None, a new one is opened.
        - start_index: starting (x, y) board index.
        - magnet_pin: optional GPIO pin to control an electromagnet; if provided, a `Magnet` is created.
        - port, baud: serial settings used when opening a new connection.
        """
        self.port = port
        self.baud = baud
        self.ser = ser if ser is not None else self._open_plotter()
        self.board = GRBL_COORDINATES
        self.current_index = start_index
        self.magnet = Magnet(magnet_pin) if magnet_pin is not None else None
        self.plotter_initialization()

    # -------------------------
    # Serial helpers (merged from plotter_helpers.py)
    # -------------------------

    def _open_plotter(self) -> serial.Serial:
        print(f"[PLOTTER] Opening {self.port} @ {self.baud} baud")
        return serial.Serial(self.port, self.baud, timeout=1)

    def close(self):
        """
        Safely close the plotter serial port, returning to (0,0).
        """
        if self.ser is not None and self.ser.is_open:
            distances = self._target_distance((0, 0))
            # Return to (0,0) at the end
            self.send_grbl("G0 X0")
            time.sleep(BASE_SLEEP + distances[0] * UNIT_SLEEP)
            self.send_grbl("G0 Y0")
            time.sleep(BASE_SLEEP + distances[1] * UNIT_SLEEP)
            print("[PLOTTER] Closing serial port")
            self.ser.close()

    def send_grbl(self, command: str):
        """
        Send one line of G-code and print GRBL's response.
        """
        line = command.strip()
        print(f"> {line}")

        if self.ser is None or not self.ser.is_open:
            raise RuntimeError("send_grbl called with a closed or None serial port")

        self.ser.write((line + "\n").encode("ascii"))

        # Read lines until we see 'ok' or 'error'
        while True:
            response = self.ser.readline().decode("ascii", errors="ignore").strip()
            if response:
                print("GRBL:", response)
                if response == "ok" or response.startswith("error"):
                    break

    def report_position(self, label: str = "Position"):
        """
        Ask GRBL for its current reported machine status/position.
        """
        print(f"\n--- {label} ---")

        if self.ser is None or not self.ser.is_open:
            raise RuntimeError(
                "report_position called with a closed or None serial port"
            )

        self.ser.write(b"?")
        time.sleep(0.2)  # wait for GRBL to respond
        resp = self.ser.read_all().decode("ascii", errors="ignore")
        print(resp.strip())

    def plotter_initialization(self):
        """
        Wake up GRBL, unlock, and set coordinate mode.
        """
        if self.ser is None or not self.ser.is_open:
            raise RuntimeError(
                "plotter_initialization called with a closed or None serial port"
            )

        # Wake up GRBL
        self.ser.write(b"\r\n\r\n")
        time.sleep(2)
        self.ser.reset_input_buffer()

        # Unlock GRBL and set coordinates
        self.send_grbl("$X")  # unlock
        self.send_grbl("G92 X0 Y0")  # set current pos as (0,0)
        self.send_grbl("G90")  # absolute positioning
        home = self._index_to_grbl((0, 0))
        self.send_grbl("G0 " + home[0])
        time.sleep(BASE_SLEEP + 100 * UNIT_SLEEP)
        self.send_grbl("G0 " + home[1])
        time.sleep(BASE_SLEEP + 100 * UNIT_SLEEP)

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
        FOR DEBUGGING ONLY
        Move plotter directly to explicit GRBL coordinates with magnet OFF.

        Example:
            go_to_grbl("X120.0", "Y45.0")
            go_to_grbl(x_grbl="X120.0")
            go_to_grbl(y_grbl="Y45.0")
        """
        if x_grbl is None and y_grbl is None:
            return

        if x_grbl is not None:
            self.send_grbl("G0 " + x_grbl)
            print("MOVE CALL RETURNED")
            time.sleep(5)

        if y_grbl is not None:
            self.send_grbl("G0 " + y_grbl)
            time.sleep(5)

    def _target_distance(self, target_index: tuple[int, int]) -> tuple[float, float]:
        """
        Calculate the absolute distance between current and target GRBL coordinates.

        Returns:
            tuple of (distance_x, distance_y)
        """
        target_x, target_y = self._index_to_grbl(target_index)
        current_x, current_y = self._index_to_grbl(self.current_index)
        return (
            abs(float(target_x[1:]) - float(current_x[1:])),
            abs(float(target_y[1:]) - float(current_y[1:])),
        )

    def go_to(self, target_index: tuple[int, int]):
        """
        Move plotter to a board index with magnet OFF.
        No axis restrictions.
        """
        if target_index == self.current_index:
            return

        target_x, target_y = self._index_to_grbl(target_index)
        distances = self._target_distance(target_index)
        self.send_grbl("G0 " + target_x)
        time.sleep(BASE_SLEEP + distances[0] * UNIT_SLEEP)

        self.send_grbl("G0 " + target_y)
        time.sleep(BASE_SLEEP + distances[1] * UNIT_SLEEP)

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
        distances = self._target_distance(target_index)
        x_grbl, y_grbl = self._index_to_grbl(target_index)

        if self.magnet is not None:
            self.magnet.on()
            time.sleep(0.2)

        try:
            # Y movement only
            if current_x == target_x and current_y != target_y:
                self.send_grbl("G0 " + y_grbl)
                time.sleep(BASE_SLEEP + distances[1] * UNIT_SLEEP)

            # X movement only
            elif current_y == target_y and current_x != target_x:
                self.send_grbl("G0 " + x_grbl)
                time.sleep(BASE_SLEEP + distances[0] * UNIT_SLEEP)

            else:
                raise RuntimeError(
                    f"Illegal carry_to move: "
                    f"current_index={self.current_index}, "
                    f"target_index={target_index}. "
                    f"Can only move along one axis."
                )

            self.current_index = target_index

        finally:
            if self.magnet is not None:
                self.magnet.off()
                time.sleep(0.2)
