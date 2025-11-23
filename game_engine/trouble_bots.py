"""
AI Bots for Trouble Game
Three difficulty levels: Easy, Medium, Hard
"""

import random
from typing import List, Tuple, Optional, Dict

class EasyBot:
    """
    Easy Bot - Completely Random
    Chooses any valid move with equal probability
    """
    
    def __init__(self, color: str):
        self.color = color
        self.name = f"Easy Bot ({color})"
    
    def choose_move(self, game, valid_moves: List[Tuple]) -> Optional[Tuple]:
        """
        Choose a completely random move
        
        Args:
            game: Game state object
            valid_moves: List of (piece, move_description) tuples
        
        Returns:
            Random move from valid moves
        """
        if not valid_moves:
            return None
        
        return random.choice(valid_moves)


class MediumBot:
    """
    Medium Bot - Prioritizes Getting Pieces Home
    Strategy:
    1. Move pieces closest to home first
    2. Get pieces out of start if possible
    3. Prefer safe moves over risky ones
    """
    
    def __init__(self, color: str):
        self.color = color
        self.name = f"Medium Bot ({color})"
    
    def choose_move(self, game, valid_moves: List[Tuple]) -> Optional[Tuple]:
        """
        Choose move prioritizing home advancement
        
        Args:
            game: Game state object
            valid_moves: List of (piece, move_description) tuples
        
        Returns:
            Best move based on medium strategy
        """
        if not valid_moves:
            return None
        
        # Score each move
        scored_moves = []
        for piece, move_desc in valid_moves:
            score = self._score_move(game, piece, move_desc)
            scored_moves.append((score, piece, move_desc))
        
        # Sort by score (highest first)
        scored_moves.sort(reverse=True, key=lambda x: x[0])
        
        # Return best move
        return (scored_moves[0][1], scored_moves[0][2])
    
    def _score_move(self, game, piece, move_desc: str) -> float:
        """
        Score a move based on medium bot priorities
        
        Higher score = better move
        """
        score = 0.0
        
        # Priority 1: Entering home (HIGHEST)
        if "entering home" in move_desc.lower():
            score += 1000
        
        # Priority 2: Moving in home stretch (very high)
        if "home stretch" in move_desc.lower():
            score += 500
            # Further in home stretch = better
            if hasattr(piece, 'position_in_home'):
                score += piece.position_in_home * 50
        
        # Priority 3: Getting out of start
        if "leaving start" in move_desc.lower():
            score += 300
        
        # Priority 4: Progress toward home
        # Pieces further along the board are prioritized
        if hasattr(piece, 'steps_from_start'):
            score += piece.steps_from_start * 2
        
        # Priority 5: Capturing opponent (bonus, not main goal)
        if self._would_capture(piece, move_desc):
            score += 100
        
        # Penalty: Being in danger (slight consideration)
        if self._is_vulnerable(game, piece):
            score -= 50
        
        # Add small random factor for variety
        score += random.uniform(-5, 5)
        
        return score
    
    def _would_capture(self, piece, move_desc: str) -> bool:
        """Check if move would capture an opponent"""
        return "capturing" in move_desc.lower() or "capture" in move_desc.lower()
    
    def _is_vulnerable(self, game, piece) -> bool:
        """
        Check if piece is vulnerable to capture
        Simplified check - just see if it's on main path
        """
        # Pieces in start or home are safe
        if hasattr(piece, 'in_start') and piece.in_start:
            return False
        if hasattr(piece, 'in_home') and piece.in_home:
            return False
        
        # On main path = potentially vulnerable
        return True


class HardBot:
    """
    Hard Bot - Aggressive and Smart
    Strategy:
    1. Aggressive captures - send opponents back
    2. Block opponent progress strategically
    3. Smart positioning - avoid danger
    4. Balanced offense and defense
    5. Endgame optimization
    """
    
    def __init__(self, color: str):
        self.color = color
        self.name = f"Hard Bot ({color})"
    
    def choose_move(self, game, valid_moves: List[Tuple]) -> Optional[Tuple]:
        """
        Choose move using advanced strategy
        
        Args:
            game: Game state object
            valid_moves: List of (piece, move_description) tuples
        
        Returns:
            Best move based on hard strategy
        """
        if not valid_moves:
            return None
        
        # Analyze game state
        game_phase = self._determine_game_phase(game)
        
        # Score each move
        scored_moves = []
        for piece, move_desc in valid_moves:
            score = self._score_move(game, piece, move_desc, game_phase)
            scored_moves.append((score, piece, move_desc))
        
        # Sort by score (highest first)
        scored_moves.sort(reverse=True, key=lambda x: x[0])
        
        # Return best move
        return (scored_moves[0][1], scored_moves[0][2])
    
    def _determine_game_phase(self, game) -> str:
        """
        Determine what phase of the game we're in
        Returns: 'early', 'mid', or 'end'
        """
        # Count pieces in various states
        my_pieces_home = 0
        my_pieces_out = 0
        
        if hasattr(game, 'players'):
            for player in game.players.values():
                if player.color == self.color:
                    for piece in player.pieces:
                        if hasattr(piece, 'finished') and piece.finished:
                            my_pieces_home += 1
                        elif hasattr(piece, 'in_start') and not piece.in_start:
                            my_pieces_out += 1
        
        # Determine phase
        if my_pieces_home >= 2:
            return 'end'
        elif my_pieces_out >= 3:
            return 'mid'
        else:
            return 'early'
    
    def _score_move(self, game, piece, move_desc: str, game_phase: str) -> float:
        """
        Score a move based on hard bot strategy
        
        Higher score = better move
        """
        score = 0.0
        
        # === HIGHEST PRIORITY: Winning moves ===
        if "entering home" in move_desc.lower():
            score += 10000
            # Check if this wins the game
            if self._would_win_game(game, piece):
                score += 50000
        
        # === HOME STRETCH: Very high priority ===
        if "home stretch" in move_desc.lower():
            score += 2000
            if hasattr(piece, 'position_in_home'):
                # Prioritize advancing further pieces in home
                score += piece.position_in_home * 100
        
        # === AGGRESSIVE CAPTURES: High priority ===
        if self._would_capture(piece, move_desc):
            capture_value = self._evaluate_capture(game, piece, move_desc)
            score += 800 + capture_value
        
        # === STRATEGIC BLOCKING ===
        if self._blocks_opponent(game, piece, move_desc):
            score += 400
        
        # === LEAVING START: Important but not critical ===
        if "leaving start" in move_desc.lower():
            # Early game: high priority to get pieces out
            if game_phase == 'early':
                score += 600
            # Later: still good but not as critical
            else:
                score += 300
        
        # === BOARD POSITION VALUE ===
        # Pieces further along = better (but not as important as other factors)
        if hasattr(piece, 'steps_from_start'):
            score += piece.steps_from_start * 3
        
        # === SAFETY EVALUATION ===
        # Heavily penalize moves into danger
        if self._is_vulnerable_after_move(game, piece, move_desc):
            if not self._is_safe_from_capture(game, piece, move_desc):
                score -= 500  # Big penalty for dangerous positions
        
        # === OPPONENT PRESSURE ===
        # Bonus for keeping pieces near opponents
        score += self._evaluate_pressure(game, piece) * 2
        
        # === ENDGAME OPTIMIZATION ===
        if game_phase == 'end':
            # Focus on finishing pieces in end game
            if "home stretch" in move_desc.lower() or "entering home" in move_desc.lower():
                score += 500
            # Don't worry as much about captures in endgame
            elif self._would_capture(piece, move_desc):
                score -= 100
        
        # === PIECE DISTRIBUTION ===
        # Slight bonus for spreading pieces out
        if self._improves_piece_distribution(game, piece):
            score += 50
        
        # Small random factor for unpredictability
        score += random.uniform(-10, 10)
        
        return score
    
    def _would_win_game(self, game, piece) -> bool:
        """Check if moving this piece home would win the game"""
        # Count how many pieces are already finished
        finished_count = 0
        if hasattr(game, 'players'):
            for player in game.players.values():
                if player.color == self.color:
                    for p in player.pieces:
                        if hasattr(p, 'finished') and p.finished:
                            finished_count += 1
        
        # If 3 pieces finished and this one can finish, we win!
        return finished_count >= 3
    
    def _would_capture(self, piece, move_desc: str) -> bool:
        """Check if move would capture an opponent"""
        return "capturing" in move_desc.lower() or "capture" in move_desc.lower()
    
    def _evaluate_capture(self, game, piece, move_desc: str) -> float:
        """
        Evaluate how valuable a capture is
        Returns bonus points for the capture
        """
        # Base capture value
        value = 200.0
        
        # Capturing pieces close to home is more valuable
        # (sends them further back)
        # This would need access to the target piece's position
        # For now, use base value
        
        return value
    
    def _blocks_opponent(self, game, piece, move_desc: str) -> bool:
        """
        Check if move blocks opponent progress
        Returns True if landing spot is strategic for blocking
        """
        # This would need to analyze opponent piece positions
        # and see if our piece landing blocks their path
        # Simplified: just return False for now
        # TODO: Implement blocking detection
        return False
    
    def _is_vulnerable_after_move(self, game, piece, move_desc: str) -> bool:
        """Check if piece would be vulnerable after this move"""
        # Pieces in home stretch or finished are never vulnerable
        if "home stretch" in move_desc.lower() or "entering home" in move_desc.lower():
            return False
        
        # Leaving start onto main path = vulnerable
        if "leaving start" in move_desc.lower():
            return True
        
        # On main path = vulnerable
        return True
    
    def _is_safe_from_capture(self, game, piece, move_desc: str) -> bool:
        """
        Check if piece is safe from capture after move
        Returns True if no opponent can capture on their next turn
        """
        # Home stretch and home are always safe
        if "home stretch" in move_desc.lower() or "entering home" in move_desc.lower():
            return True
        
        # This would need to simulate opponent moves
        # Simplified: assume vulnerable unless proven safe
        # TODO: Implement proper threat detection
        return False
    
    def _evaluate_pressure(self, game, piece) -> float:
        """
        Evaluate how much pressure piece puts on opponents
        Returns value based on proximity to opponent pieces
        """
        # This would need to check distance to opponent pieces
        # Simplified: return neutral value
        # TODO: Implement pressure evaluation
        return 0.0
    
    def _improves_piece_distribution(self, game, piece) -> bool:
        """
        Check if moving this piece improves overall distribution
        Good distribution = pieces spread out on board
        """
        # This would need to analyze positions of all pieces
        # Simplified: return False
        # TODO: Implement distribution analysis
        return False
    
    def _is_vulnerable(self, game, piece) -> bool:
        """Check if piece is currently vulnerable"""
        if hasattr(piece, 'in_start') and piece.in_start:
            return False
        if hasattr(piece, 'in_home') and piece.in_home:
            return False
        return True


def create_bot(color: str, difficulty: str = "medium"):
    """
    Factory function to create a bot of specified difficulty
    
    Args:
        color: Player color for the bot
        difficulty: 'easy', 'medium', or 'hard'
    
    Returns:
        Bot instance
    """
    difficulty = difficulty.lower()
    
    if difficulty == "easy":
        return EasyBot(color)
    elif difficulty == "medium":
        return MediumBot(color)
    elif difficulty == "hard":
        return HardBot(color)
    else:
        raise ValueError(f"Unknown difficulty: {difficulty}. Use 'easy', 'medium', or 'hard'")


# Example usage and testing
if __name__ == "__main__":
    print("=== Trouble/Ludo Bot AI System ===\n")
    
    print("Bot Difficulties:\n")
    
    print("1. EASY BOT")
    print("   - Strategy: Completely random")
    print("   - Difficulty: Beginner friendly")
    print("   - Play style: Unpredictable, no strategy\n")
    
    print("2. MEDIUM BOT")
    print("   - Strategy: Prioritize getting pieces home")
    print("   - Difficulty: Balanced challenge")
    print("   - Play style: Defensive, focuses on finishing\n")
    
    print("3. HARD BOT")
    print("   - Strategy: Aggressive and smart")
    print("   - Difficulty: Challenging opponent")
    print("   - Play style: Captures opponents, blocks progress, smart positioning\n")
    
    # Create sample bots
    easy = create_bot("red", "easy")
    medium = create_bot("blue", "medium")
    hard = create_bot("green", "hard")
    
    print(f"Created: {easy.name}")
    print(f"Created: {medium.name}")
    print(f"Created: {hard.name}")
    
    print("\n=== Integration Instructions ===")
    print("1. Import: from trouble_bots import create_bot")
    print("2. Create bot: bot = create_bot('red', 'hard')")
    print("3. Get move: move = bot.choose_move(game, valid_moves)")
    print("4. Execute the returned move in your game logic")
