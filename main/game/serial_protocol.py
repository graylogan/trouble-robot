#!/usr/bin/env python3
"""
Control Panel Serial Protocol
Communicates with Logan's Arduino Control Panel
Based on actual Arduino implementation
"""

import serial
import time
from typing import Optional, Dict
from enum import Enum
from game.constants import PlayerColor


class PlayerType(Enum):
    """Player types matching Arduino enum"""

    NO_PLAYER = 0
    HUMAN = 1
    EASY = 2
    MEDIUM = 3
    HARD = 4


class ControlPanelProtocol:
    """
    Handles serial communication with the Control Panel Arduino.

    Protocol Details:
    - Baud rate: 9600
    - Messages are simple text (not JSON)
    - Line ending: \n
    """

    def __init__(
        self,
        port="rfc2217://localhost:4000",
        baud_rate=9600,
        timeout=5,
        simulation=True,
    ):
        """
        Initialize serial connection to Control Panel.

        Args:
            port: Serial port (e.g., '/dev/ttyACM0' or 'socket://localhost:4000' for Wokwi)
            baud_rate: Communication speed (default 9600)
            timeout: Read timeout in seconds
        """
        self.port = port
        self.baud_rate = baud_rate
        self.timeout = timeout
        self.simulation = simulation
        self.serial = None
        self.connected = False

    def connect(self):
        """Establish serial connection to Control Panel."""
        try:
            if self.simulation:
                self.serial = serial.serial_for_url(
                    url=self.port,
                    baudrate=self.baud_rate,
                    timeout=self.timeout,
                )
            else:
                self.serial = serial.Serial(
                    port=self.port,
                    baudrate=self.baud_rate,
                    timeout=self.timeout,
                    write_timeout=self.timeout,
                )
            self.connected = True
            time.sleep(2)  # Wait for Arduino to reset
            print(f"✅ Connected to Control Panel on {self.port}")
            return True
        except serial.SerialException as e:
            print(f"❌ Failed to connect to Control Panel: {e}")
            self.connected = False
            return False

    def disconnect(self):
        """Close serial connection."""
        if self.serial and self.serial.is_open:
            self.serial.close()
            self.connected = False
            print("🔌 Disconnected from Control Panel")

    def _send_message(self, message: str):
        """
        Send a message to the Control Panel.

        Args:
            message: String to send (newline will be added)
        """
        if not self.connected or not self.serial:
            raise RuntimeError("Not connected to Control Panel")

        # Ensure message ends with newline
        if not message.endswith("\n"):
            message += "\n"

        self.serial.write(message.encode("utf-8"))
        self.serial.flush()
        print(f"📤 Sent to Panel: {message.strip()}")

    def _read_message(self, timeout: Optional[float] = None) -> Optional[str]:
        """
        Read a message from the Control Panel.

        Args:
            timeout: Override default timeout

        Returns:
            Message string or None if timeout
        """
        if not self.connected or not self.serial:
            raise RuntimeError("Not connected to Control Panel")

        old_timeout = self.serial.timeout
        if timeout is not None:
            self.serial.timeout = timeout

        try:
            line = self.serial.readline()
            if line:
                message = line.decode("utf-8").strip()
                if message:  # Only log non-empty messages
                    print(f"📥 Received from Panel: {message}")
                return message
            return None
        finally:
            self.serial.timeout = old_timeout

    # ===== WAITING FOR MESSAGES =====

    def wait_for_config(
        self, timeout: float = 60.0
    ) -> Optional[Dict[str, Optional[str]]]:
        """
        Wait for player configuration from Control Panel.

        This is sent when the user presses START during game setup.
        Format: "1234\n" where each digit is a player type (0-4)

        Args:
            timeout: How long to wait in seconds

        Returns:
            Dictionary mapping color names to player types:
            {
                'BLUE': 'human',     # or 'easy', 'medium', 'hard', None
                'RED': 'easy',
                'GREEN': 'medium',
                'YELLOW': 'hard'
            }

        Example:
            config = panel.wait_for_config()
            if config:
                print(f"Blue player: {config['BLUE']}")
        """
        print("⏳ Waiting for game configuration from Control Panel...")
        start_time = time.time()

        while time.time() - start_time < timeout:
            message = self._read_message(timeout=1.0)
            if message and len(message) == 4 and message.isdigit():
                # This is the config message
                return self._parse_config(message)

        print("⏰ Timeout waiting for configuration")
        return None

    def wait_for_dice_complete(self, timeout: float = 35.0) -> bool:
        """
        Wait for dice roll to complete.

        The panel will send either:
        - "Bot rolled Dice!" (auto-roll complete)
        - "Human rolled Dice!" (human pressed dice button)

        Note: This does NOT tell you the dice value! You must read
        the physical dice using Computer Vision after this returns.

        Args:
            timeout: How long to wait (default 35s - 3s roll + 30s human)

        Returns:
            True if dice completed, False if timeout

        Example:
            if panel.wait_for_dice_complete():
                dice_value = vision.read_dice()  # Read actual value
        """
        print("⏳ Waiting for dice roll to complete...")
        start_time = time.time()

        while time.time() - start_time < timeout:
            message = self._read_message(timeout=1.0)
            if message and "rolled Dice" in message:
                return True

        print("⏰ Timeout waiting for dice roll")
        return False

    def wait_for_move_complete(self, timeout: float = 60.0) -> bool:
        """
        Wait for human player to complete their move.

        The panel will send "Human completed Turn!" when the human
        presses START after making their move.

        Note: This does NOT tell you what move was made! You must use
        Computer Vision to detect the board state after this returns.

        Args:
            timeout: How long to wait (default 60s)

        Returns:
            True if move completed, False if timeout

        Example:
            if panel.wait_for_move_complete():
                board_state = vision.get_board_state()  # Detect what moved
        """
        print("⏳ Waiting for human to complete move...")
        start_time = time.time()

        while time.time() - start_time < timeout:
            message = self._read_message(timeout=1.0)
            if message and "completed Turn" in message:
                return True

        print("⏰ Timeout waiting for move completion")
        return False

    # ===== SENDING COMMANDS =====

    def send_roll_request(self, color: PlayerColor):
        """
        Request a player to roll the dice.

        Behavior:
        - If player is HUMAN: Panel shows "Press Dice to roll" prompt
        - If player is BOT: Panel automatically rolls dice for 3 seconds

        You should call wait_for_dice_complete() after this.

        Args:
            color: Which player should roll (BLUE=0, RED=1, GREEN=2, YELLOW=3)

        Example:
            panel.send_roll_request(PlayerColor.BLUE)
            if panel.wait_for_dice_complete():
                dice_value = vision.read_dice()
        """
        print("!!!", type(color), color)
        player_index = color.value
        self._send_message(f"R{player_index}")

    def send_move_request(self, color: PlayerColor):
        """
        Request a human player to make their move.

        Panel shows "Make Your Move" and waits for player to:
        1. Move their piece physically
        2. Press START when done

        Only call this for HUMAN players!

        You should call wait_for_move_complete() after this.

        Args:
            color: Which player should move (BLUE=0, RED=1, GREEN=2, YELLOW=3)

        Example:
            panel.send_move_request(PlayerColor.RED)
            if panel.wait_for_move_complete():
                board_state = vision.get_board_state()
        """
        player_index = color.value
        self._send_message(f"T{player_index}")

    def send_victory(self, color: PlayerColor):
        """
        Announce that a player has finished the game.

        Panel will:
        - Play victory sound
        - Show "{Color} Has Finished!" on LCD
        - Block for 3.5 seconds for celebration

        Args:
            color: Which player finished (BLUE=0, RED=1, GREEN=2, YELLOW=3)

        Example:
            if player_finished_game:
                panel.send_victory(PlayerColor.GREEN)
                time.sleep(4)  # Wait for celebration to finish
        """
        player_index = color.value
        self._send_message(f"V{player_index}")
        time.sleep(3.5)  # Wait for victory sequence

    # ===== HELPER METHODS =====

    def _parse_config(self, message: str) -> Dict[str, Optional[str]]:
        """
        Parse player configuration message.

        Args:
            message: 4-digit string like "1234"

        Returns:
            Dictionary mapping color names to player types
        """
        type_map = {
            "0": None,  # NO_PLAYER
            "1": "human",  # HUMAN
            "2": "easy",  # EASY
            "3": "medium",  # MEDIUM
            "4": "hard",  # HARD
        }

        config = {
            "BLUE": type_map.get(message[0]),
            "RED": type_map.get(message[1]),
            "GREEN": type_map.get(message[2]),
            "YELLOW": type_map.get(message[3]),
        }

        print(f"✅ Game Configuration:")
        for color, player_type in config.items():
            if player_type:
                print(f"   {color}: {player_type.upper()}")

        return config

    def get_color_name(self, color: PlayerColor) -> str:
        """Get the string name of a color."""
        return ["Blue", "Red", "Green", "Yellow"][color.value]


# ===== EXAMPLE USAGE =====


def example_bot_vs_bot():
    """Example: Bot vs Bot game"""
    panel = ControlPanelProtocol()

    try:
        # Connect to panel
        if not panel.connect():
            return

        # Wait for user to configure game
        config = panel.wait_for_config()
        if not config:
            print("Failed to get configuration")
            return

        print("\n🎮 Starting Bot vs Bot game...\n")

        # Simulate a few turns
        for turn in range(3):
            # Blue bot's turn
            print(f"\n--- Turn {turn + 1}: Blue Bot ---")
            panel.send_roll_request(PlayerColor.BLUE)
            if panel.wait_for_dice_complete():
                print("✅ Blue bot rolled dice")
                # In real game: read dice value, calculate move, execute move
                time.sleep(1)

            # Red bot's turn
            print(f"\n--- Turn {turn + 1}: Red Bot ---")
            panel.send_roll_request(PlayerColor.RED)
            if panel.wait_for_dice_complete():
                print("✅ Red bot rolled dice")
                # In real game: read dice value, calculate move, execute move
                time.sleep(1)

        print("\n✅ Game simulation complete!")

    finally:
        panel.disconnect()


def example_human_vs_bot():
    """Example: Human vs Bot game"""
    panel = ControlPanelProtocol()

    try:
        # Connect
        if not panel.connect():
            return

        # Wait for config
        config = panel.wait_for_config()
        if not config:
            return

        print("\n🎮 Starting Human vs Bot game...\n")

        # Human's turn
        print("\n--- Blue Human's Turn ---")
        panel.send_roll_request(PlayerColor.BLUE)
        if panel.wait_for_dice_complete():
            print("✅ Human rolled dice")
            # Read dice value with vision
            print("   (Read dice value: 4)")

            # Request move
            panel.send_move_request(PlayerColor.BLUE)
            if panel.wait_for_move_complete():
                print("✅ Human completed move")
                # Validate with vision

        # Bot's turn
        print("\n--- Red Bot's Turn ---")
        panel.send_roll_request(PlayerColor.RED)
        if panel.wait_for_dice_complete():
            print("✅ Bot rolled dice")
            # Read dice, calculate move, execute
            time.sleep(1)

        print("\n✅ Game simulation complete!")

    finally:
        panel.disconnect()


if __name__ == "__main__":
    print("=" * 60)
    print("CONTROL PANEL PROTOCOL - TEST")
    print("=" * 60)
    print("\nChoose example:")
    print("1. Bot vs Bot")
    print("2. Human vs Bot")

    choice = input("\nEnter choice (1 or 2): ")

    if choice == "1":
        example_bot_vs_bot()
    elif choice == "2":
        example_human_vs_bot()
    else:
        print("Invalid choice")
