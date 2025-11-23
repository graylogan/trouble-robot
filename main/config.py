#!/usr/bin/env python3
"""
Configuration for Trouble Makers Robot System
"""

# ===== SERIAL PORTS =====
# Control Panel connection (Wokwi simulator)
CONTROL_PANEL_PORT = "rfc2217://localhost:4000"
# For real hardware, use: CONTROL_PANEL_PORT = "/dev/ttyACM0"

# XY Plotter connection
PLOTTER_PORT = "/dev/ttyACM1"

# Baud rates
CONTROL_PANEL_BAUD = 9600
PLOTTER_BAUD = 115200

# ===== BOARD DIMENSIONS =====
# Physical board size in millimeters
BOARD_SIZE = 200  # ~A4 paper size (210mm)
PIECE_DIAMETER = 20  # Size of game pieces

# Game layout
TRACK_POSITIONS = 64  # Total positions on main track (16 per side × 4)
HOME_POSITIONS_PER_PLAYER = 4  # Each player has 4 home spots
PIECES_PER_PLAYER = 4  # Each player has 4 pieces

# ===== TIMEOUTS =====
# Communication timeouts in seconds
SERIAL_TIMEOUT = 5
PLOTTER_TIMEOUT = 10
VISION_TIMEOUT = 3

# Game interaction timeouts
DICE_ROLL_TIMEOUT = 35  # 3s auto-roll + 30s for human
MOVE_TIMEOUT = 60  # Time for human to make move
CONFIG_TIMEOUT = 120  # Time to wait for game configuration

# ===== PLAYER CONFIGURATION =====
# Player colors and their starting track positions
COLORS = ["BLUE", "RED", "GREEN", "YELLOW"]

STARTING_POSITIONS = {
    "BLUE": 0,
    "RED": 16,
    "GREEN": 32,
    "YELLOW": 48
}

# Color to index mapping (matches Control Panel Arduino)
COLOR_TO_INDEX = {
    "BLUE": 0,
    "RED": 1,
    "GREEN": 2,
    "YELLOW": 3
}

# ===== DEBUG SETTINGS =====
DEBUG_MODE = True  # Set to False for production
SIMULATE_VISION = True  # Use random dice values when testing
SIMULATE_PLOTTER = True  # Don't send real plotter commands when testing