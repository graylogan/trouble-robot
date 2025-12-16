#!/usr/bin/env python3
"""
Test driver script for testing player movement using the game classes.
"""

from game.player import Player
from game.plotter import Plotter
from game.board import Board

def main():
    print("=== Game Movement Test Driver ===\n")
    
    # Create some hardcoded player objects
    print("Creating hardcoded player objects...")
    player1 = Player(color="RED", type="easy", home=(3, 0))
    player2 = Player(color="BLUE", type="easy", home=(0, 2))
    player3 = Player(color="GREEN", type="easy", home=(0, 0))
    
    print(f"  {player1}")
    print(f"  {player2}")
    print(f"  {player3}\n")
    
    # Initialize plotter with magnet pin=11
    print("Initializing plotter with magnet pin=11...")
    try:
        plotter = Plotter(magnet_pin=11)
        print("  Plotter initialized successfully\n")
    except Exception as e:
        print(f"  Warning: Could not initialize plotter: {e}")
        print("  Continuing with mock plotter...\n")
        plotter = None
    
    # Initialize board object
    print("Initializing board...")
    test_board = Board()
    print("  Board initialized (8x5 grid)\n")
    
    # Manually put players on the board at their home positions
    print("Populating board with players at home positions...")
    test_board.populate([player1, player2, player3])
    print(f"  Player 1 ({player1.color}) at {player1.pos}")
    print(f"  Player 2 ({player2.color}) at {player2.pos}")
    print(f"  Player 3 ({player3.color}) at {player3.pos}\n")
    
    # Display board state
    print("Board state:")
    for x in range(8):
        for y in range(5):
            if test_board.board[x][y] is not None:
                print(f"  Position ({x}, {y}): {test_board.board[x][y].color} player")
    print()
    
    # Test low_level_move() function
    print("Testing low_level_move()...\n")

    # Unlock player1 so it can move
    player1.locked = False

    try:
        # Prepare transformation for player1 from this board's perspective
        p_trans = test_board.side_perspective_transformation(player1)
        print(f"Player1 transformation: {p_trans}")

        if plotter is None:
            print("\nPlotter not available; skipping low_level_move test.")
        else:
            # Move two steps to the right relative to the player's side
            print("\nCalling test_board.low_level_move(player1, 'RIGHT', 2, p_trans, plotter)")
            test_board.low_level_move(player1, "RIGHT", 2, p_trans, plotter)
            print("low_level_move() completed")
        
    except Exception as e:
        print(f"Error during movement test: {e}\n")
        import traceback
        traceback.print_exc()
    
    print("\n=== Test Complete ===")

if __name__ == "__main__":
    main()
