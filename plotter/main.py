#!/usr/bin/env python3

import time
from magnet import initialize_magnet, cleanup_magnet, turn_off_magnet
from plotter_helpers import open_plotter, close_plotter, plotter_initialization
from utils import get_players, roll, map_roll_to_g_code, move_roll

def main():
    # Set up magnet and plotter
    initialize_magnet()
    ser = open_plotter()
    plotter_initialization(ser)
    turn_off_magnet()
    try:
        players = get_players()
        for player in players:
            r = roll()
            new_pos = map_roll_to_g_code(player, r)
            print(f"{player.team} rolled {r}: {player.current_location} -> {new_pos}")
            move_roll(ser, new_pos, player)
    finally:
        # Make sure magnet is off and GPIO is cleaned up
        turn_off_magnet()
        cleanup_magnet()
        ser.close()



if __name__ == "__main__":
    main()
