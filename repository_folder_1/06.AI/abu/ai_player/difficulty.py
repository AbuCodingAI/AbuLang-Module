"""Difficulty controller for adjusting AI strength"""

import numpy as np
from typing import List, Tuple


class DifficultyController:
    """Adjusts AI strength based on difficulty setting"""
    
    @staticmethod
    def apply_difficulty(move_scores: List[Tuple[str, float]], difficulty: str) -> str:
        """
        Apply difficulty adjustment to move selection
        
        Args:
            move_scores: List of (move, score) tuples sorted by score
            difficulty: 'beginner', 'intermediate', or 'advanced'
        
        Returns:
            Selected move in UCI format
        """
        if not move_scores:
            raise ValueError("No moves provided")
        
        if difficulty == 'advanced':
            # Always pick best move
            return move_scores[0][0]
        
        elif difficulty == 'intermediate':
            # Pick from top 3 moves with weighted probability
            top_moves = move_scores[:min(3, len(move_scores))]
            moves, scores = zip(*top_moves)
            
            # Normalize scores to probabilities
            scores = np.array(scores)
            if scores.sum() > 0:
                probs = scores / scores.sum()
            else:
                probs = np.ones(len(scores)) / len(scores)
            
            # Select with probability
            selected_idx = np.random.choice(len(moves), p=probs)
            return moves[selected_idx]
        
        elif difficulty == 'beginner':
            # 30% chance to pick random move, 70% chance to pick from top 5
            if np.random.random() < 0.3:
                # Random move
                return np.random.choice([m for m, _ in move_scores])
            else:
                # Pick from top 5 with uniform probability
                top_moves = move_scores[:min(5, len(move_scores))]
                return np.random.choice([m for m, _ in top_moves])
        
        else:
            raise ValueError(f"Invalid difficulty: {difficulty}")
