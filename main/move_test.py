from player import Player
from board_new import board
from plotter_controller import PlotterController
from plotter_helpers import open_plotter, plotter_initialization, close_plotter
import serial

# Create a player
player = Player(color="BLUE", type="easy", home=0)
# Set initial grid position for the player
# player.gridPos = {"x": 3, "y": 2}

# Create a mock serial connection (you'll need to replace this with actual serial port)
# For testing, you might need to comment this out or use a real serial device
ser = open_plotter()  # Adjust port as needed
plotter_initialization(ser)

# Create PlotterController
plotter = PlotterController(ser)

# Calculate player transformation
# For a player at the bottom (home=0), transformation is (False, False)
p_trans = 

# Move the player up 2 spaces
low_level_move(player, "UP", 2, p_trans, plotter)

print(f"Player moved from {player.gridPos} to new position")
