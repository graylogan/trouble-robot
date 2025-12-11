import random
import time
from magnet import turn_on_magnet, turn_off_magnet
from player import Player
from plotter_helpers import send_grbl

BOARD = [
    ["X13", "Y30"], ["X55", "Y30"], ["X90", "Y30"], ["X122", "Y30"], ["X154", "Y30"], ["X186", "Y30"], ["X218", "Y30"], ["X255", "Y30"],
    ["X255", "Y72"], ["X255", "Y104"], ["X255", "Y136"], ["X255", "Y170"],
    ["X255", "Y170"], ["X210", "Y170"], ["X178", "Y170"], ["X146", "Y170"], ["X114", "Y170"], ["X82", "Y170"], ["X43", "Y170"],
    ["X8", "Y170"], ["X8", "Y126"], ["X13", "Y94"], ["X13", "Y62"]
]

def get_players():
    """
    For now: hard-coded four players (Green, Blue, Yellow, Red).
    Later this can ask the Arduino / control panel.
    """
    green_player = Player(team="Green")
    blue_player = Player(team="Blue")
    yellow_player = Player(team="Yellow")
    red_player = Player(team="Red")
    return [blue_player, green_player, red_player, yellow_player]


def roll():
    """Roll a simple test die (1–3)."""
    return random.randint(1, 3)


def map_roll_to_g_code(player: Player, roll_value: int):
    """
    Given a player and a roll, return the next board position [X, Y].

    Wraps around the BOARD list if needed.
    """
    index_of_current_location = BOARD.index(player.current_location)
    next_index = index_of_current_location + roll_value
    if next_index < len(BOARD):
        return BOARD[next_index]
    else:
        return BOARD[next_index - len(BOARD)]


def move_roll(ser, new_pos: list, player: Player):
    magnet_on = False
    try:
        # Make sure we’re at the current location first (magnet OFF)
        send_grbl(ser, "G0 " + player.current_location[0])
        time.sleep(5)
        send_grbl(ser, "G0 " + player.current_location[1])
        time.sleep(5)

        # Turn magnet ON to pick up the piece
        turn_on_magnet()
        magnet_on = True
        time.sleep(3)  # small settle

        # Move to new X and Y with magnet ON
        send_grbl(ser, "G0 " + new_pos[0])
        time.sleep(5)
        send_grbl(ser, "G0 " + new_pos[1])
        time.sleep(5)

        # Update logical position
        player.current_location = new_pos

    finally:
        if magnet_on:
            turn_off_magnet()
            time.sleep(0.2)

