#!/usr/bin/env python3
"""
Trouble Board Game Engine
Core game state representation and rules implementation
Complete implementation with all official Trouble rules
"""

import random
from enum import Enum
from typing import List, Optional, Tuple


class Color(Enum):
    """Player colors in Trouble"""
    RED = 0
    BLUE = 1
    GREEN = 2
    YELLOW = 3


class Piece:
    """
    Represents a single game piece.
    
    Position tracking:
    - track_position = -1: In START area
    - track_position = 0-15: On main track
    - track_position = -1 AND home_position = 0-3: In home stretch
    - finished = True: Reached final position
    """
    
    def __init__(self, color: Color, piece_id: int):
        self.color = color
        self.piece_id = piece_id  # 0-3 for each player's 4 pieces
        self.track_position = -1  # -1 = START, 0-15 = on track
        self.home_position = -1   # -1 = not in home, 0-3 = home position
        self.finished = False
    
    def is_in_start(self) -> bool:
        """Check if piece is in START area"""
        return self.track_position == -1 and self.home_position == -1
    
    def is_on_track(self) -> bool:
        """Check if piece is on main track"""
        return 0 <= self.track_position < 16
    
    def is_in_home(self) -> bool:
        """Check if piece is in home stretch"""
        return self.home_position >= 0
    
    def __repr__(self):
        return f"{self.color.name}_{self.piece_id}"


class TroubleGame:
    """
    Main game engine for Trouble board game.
    
    Board Layout:
    - Each player has 4 pieces
    - START area: Pieces begin here (off the board)
    - Main track: 16-space circular track (positions 0-15)
    - Home stretch: Each color has their OWN 4-space home (positions 0-3)
    - Finish: Piece at home position 3
    
    Rules:
    - Roll 6 to exit START
    - Roll 6 = extra turn
    - Land on opponent = capture (send back to START)
    - Cannot land on own piece (on track)
    - CAN share spaces in home stretch
    - Must reach exact count to finish
    """
    
    PIECES_PER_PLAYER = 4
    TRACK_LENGTH = 16
    HOME_LENGTH = 4
    
    # Starting positions on the main track for each color
    STARTING_POSITIONS = {
        Color.RED: 0,
        Color.BLUE: 4,
        Color.GREEN: 8,
        Color.YELLOW: 12
    }
    
    # Home entry positions (where pieces leave track to enter home)
    HOME_ENTRY_POSITIONS = {
        Color.RED: 15,    # RED enters home after position 15
        Color.BLUE: 3,    # BLUE enters home after position 3
        Color.GREEN: 7,   # GREEN enters home after position 7
        Color.YELLOW: 11  # YELLOW enters home after position 11
    }
    
    def __init__(self, num_players: int = 2, player_colors: List[Color] = None):
        """
        Initialize a new Trouble game.
        
        Args:
            num_players: Number of players (2-4)
            player_colors: List of colors for each player (default: first N colors)
        """
        if num_players < 2 or num_players > 4:
            raise ValueError("Trouble requires 2-4 players")
        
        self.num_players = num_players
        
        # Set player colors
        if player_colors is None:
            default_colors = [Color.RED, Color.BLUE, Color.GREEN, Color.YELLOW]
            self.player_colors = default_colors[:num_players]
        else:
            if len(player_colors) != num_players:
                raise ValueError("Number of colors must match number of players")
            self.player_colors = player_colors
        
        # Initialize pieces for each player
        self.pieces = {}
        for color in self.player_colors:
            self.pieces[color] = [
                Piece(color, i) for i in range(self.PIECES_PER_PLAYER)
            ]
        
        # Game state
        self.current_player_idx = 0
        self.current_dice_roll = 0
        self.game_over = False
        self.winner = None
    
    @property
    def current_player_color(self) -> Color:
        """Get the color of the current player."""
        return self.player_colors[self.current_player_idx]
    
    def roll_dice(self) -> int:
        """Roll the dice (1-6) and store the result."""
        self.current_dice_roll = random.randint(1, 6)
        return self.current_dice_roll
    
    def get_valid_moves(self, color: Color) -> List[Tuple[Piece, str]]:
        """
        Get all valid moves for a color given the current dice roll.
        
        Returns:
            List of (piece, move_description) tuples
        """
        if self.current_dice_roll == 0:
            return []
        
        valid_moves = []
        dice = self.current_dice_roll
        
        for piece in self.pieces[color]:
            # Case 1: Piece in START - can only move with a 6
            if piece.is_in_start():
                if dice == 6:
                    # Check if starting position is blocked by own piece
                    start_pos = self.STARTING_POSITIONS[color]
                    if not self._is_position_blocked_by_own(color, start_pos):
                        valid_moves.append((piece, f"Move {piece} from START to position {start_pos}"))
            
            # Case 2: Piece on track
            elif piece.is_on_track():
                new_pos = (piece.track_position + dice) % self.TRACK_LENGTH
                
                # Check if this move would pass home entry
                home_entry = self.HOME_ENTRY_POSITIONS[color]
                will_enter_home = self._will_enter_home(piece.track_position, dice, home_entry)
                
                if will_enter_home:
                    # Calculate home position
                    home_pos = self._calculate_home_position(piece.track_position, dice, home_entry)
                    if home_pos <= 3:  # Valid home position
                        valid_moves.append((piece, f"Move {piece} to HOME position {home_pos}"))
                else:
                    # Regular track movement - check if blocked by own piece
                    if not self._is_position_blocked_by_own(color, new_pos):
                        valid_moves.append((piece, f"Move {piece} to position {new_pos}"))
            
            # Case 3: Piece in home stretch
            elif piece.is_in_home() and not piece.finished:
                new_home_pos = piece.home_position + dice
                # Can only move if exact count or less than finish
                if new_home_pos <= 3:
                    valid_moves.append((piece, f"Move {piece} to HOME position {new_home_pos}"))
        
        return valid_moves
    
    def make_move(self, piece: Piece, move_description: str) -> bool:
        """
        Execute a move.
        
        Args:
            piece: The piece to move
            move_description: Description of the move (for validation)
        
        Returns:
            bool: True if move was successful
        """
        if self.game_over:
            return False
        
        dice = self.current_dice_roll
        color = piece.color
        
        # Move from START
        if piece.is_in_start() and dice == 6:
            start_pos = self.STARTING_POSITIONS[color]
            piece.track_position = start_pos
            self._check_capture(piece, start_pos)
            return True
        
        # Move on track
        elif piece.is_on_track():
            home_entry = self.HOME_ENTRY_POSITIONS[color]
            will_enter_home = self._will_enter_home(piece.track_position, dice, home_entry)
            
            if will_enter_home:
                # Enter home stretch
                home_pos = self._calculate_home_position(piece.track_position, dice, home_entry)
                piece.track_position = -1
                piece.home_position = home_pos
                
                # Check if finished
                if home_pos == 3:
                    piece.finished = True
                    self._check_win_condition(color)
                return True
            else:
                # Regular track movement
                new_pos = (piece.track_position + dice) % self.TRACK_LENGTH
                piece.track_position = new_pos
                self._check_capture(piece, new_pos)
                return True
        
        # Move in home
        elif piece.is_in_home() and not piece.finished:
            new_home_pos = piece.home_position + dice
            if new_home_pos <= 3:
                piece.home_position = new_home_pos
                
                # Check if finished
                if new_home_pos == 3:
                    piece.finished = True
                    self._check_win_condition(color)
                return True
        
        return False
    
    def _will_enter_home(self, current_pos: int, dice: int, home_entry: int) -> bool:
        """Check if a move will cause piece to enter home stretch."""
        # Calculate the path the piece will take
        for step in range(1, dice + 1):
            pos = (current_pos + step) % self.TRACK_LENGTH
            if pos == home_entry:
                return True
        return False
    
    def _calculate_home_position(self, current_pos: int, dice: int, home_entry: int) -> int:
        """Calculate which home position piece will land on."""
        steps_to_entry = 0
        for step in range(1, dice + 1):
            pos = (current_pos + step) % self.TRACK_LENGTH
            if pos == home_entry:
                steps_to_entry = step
                break
        
        steps_into_home = dice - steps_to_entry
        return steps_into_home
    
    def _is_position_blocked_by_own(self, color: Color, position: int) -> bool:
        """Check if a track position is blocked by own piece."""
        for piece in self.pieces[color]:
            if piece.is_on_track() and piece.track_position == position:
                return True
        return False
    
    def _check_capture(self, moving_piece: Piece, position: int):
        """Check if landing on this position captures an opponent piece."""
        for color in self.player_colors:
            if color == moving_piece.color:
                continue  # Skip own pieces
            
            for piece in self.pieces[color]:
                if piece.is_on_track() and piece.track_position == position:
                    # Capture! Send opponent back to START
                    piece.track_position = -1
                    piece.home_position = -1
                    print(f"💥 {moving_piece} captured {piece}!")
    
    def _check_win_condition(self, color: Color):
        """Check if a player has won."""
        finished_count = sum(1 for p in self.pieces[color] if p.finished)
        if finished_count == self.PIECES_PER_PLAYER:
            self.game_over = True
            self.winner = color
    
    def has_player_won(self, color: Color) -> bool:
        """Check if a specific player has won."""
        return all(p.finished for p in self.pieces[color])
    
    def is_game_over(self) -> bool:
        """Check if the game is over."""
        return self.game_over
    
    def next_turn(self):
        """Advance to next player's turn."""
        if not self.game_over:
            self.current_player_idx = (self.current_player_idx + 1) % self.num_players
            self.current_dice_roll = 0
    
    def get_state(self) -> dict:
        """
        Get current game state as dictionary.
        
        Returns:
            Dictionary with complete game state
        """
        state = {
            'current_player': self.current_player_color.name,
            'dice_roll': self.current_dice_roll,
            'game_over': self.game_over,
            'winner': self.winner.name if self.winner else None,
            'pieces': {}
        }
        
        for color in self.player_colors:
            state['pieces'][color.name] = []
            for piece in self.pieces[color]:
                piece_state = {
                    'id': piece.piece_id,
                    'track_position': piece.track_position,
                    'home_position': piece.home_position,
                    'finished': piece.finished
                }
                state['pieces'][color.name].append(piece_state)
        
        return state
    
    def display_board(self):
        """Print text representation of board state."""
        print("\n" + "=" * 60)
        print(f"TROUBLE GAME - Turn: {self.current_player_color.name}")
        if self.current_dice_roll > 0:
            print(f"Dice Roll: {self.current_dice_roll}")
        print("=" * 60)
        
        for color in self.player_colors:
            pieces = self.pieces[color]
            finished_count = sum(1 for p in pieces if p.finished)
            
            print(f"\n{color.name}:")
            for piece in pieces:
                if piece.finished:
                    status = "✓ FINISHED"
                elif piece.is_in_start():
                    status = "START"
                elif piece.is_on_track():
                    status = f"Track position {piece.track_position}"
                elif piece.is_in_home():
                    status = f"Home position {piece.home_position}"
                else:
                    status = "UNKNOWN"
                print(f"  {piece}: {status}")
        
        print("\n" + "=" * 60)


# Example usage
if __name__ == "__main__":
    print("Trouble Game Engine - Test")
    print("=" * 60)
    
    # Create a 2-player game
    game = TroubleGame(num_players=2)
    game.display_board()
    
    # Simulate a few turns
    for turn in range(5):
        print(f"\n--- Turn {turn + 1} ---")
        current_color = game.current_player_color
        
        # Roll dice
        roll = game.roll_dice()
        print(f"{current_color.name} rolled: {roll}")
        
        # Get valid moves
        moves = game.get_valid_moves(current_color)
        print(f"Valid moves: {len(moves)}")
        
        if moves:
            # Make first valid move
            piece, description = moves[0]
            print(f"Moving: {description}")
            game.make_move(piece, description)
        
        # Check for extra turn (rolled 6)
        if roll != 6:
            game.next_turn()
        else:
            print("🎲 Rolled 6! Extra turn!")
        
        if game.is_game_over():
            print(f"\n🏆 {game.winner.name} WINS!")
            break
