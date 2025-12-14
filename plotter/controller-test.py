#!/usr/bin/env python3

import time
from magnet import initialize_magnet, cleanup_magnet, turn_off_magnet
from plotter_helpers import open_plotter, close_plotter, plotter_initialization
from plotter_controller import PlotterController

def main():
    # Set up magnet and plotter
    initialize_magnet()
    ser = open_plotter()
    plotter_initialization(ser)
    plotter = PlotterController(ser)
    try:
        while (1):
            x = input("x: ")
            y = input("y: ")
            plotter.go_to_grbl("X"+x, "Y"+y)
    finally:
        # Make sure magnet is off and GPIO is cleaned up
        turn_off_magnet()
        cleanup_magnet()
        close_plotter(ser)



if __name__ == "__main__":
    main()
