"""Move decoder for converting neural network output to chess moves"""

import numpy as np
import chess
from typing import List, Tuple


class MoveDecoder:
    """Decodes neural network output into chess moves"""
    
    def __init__(self):
        """Initialize move decoder with move mapping"""
        self._build_move_mapping()
    
    def _build_move_mapping(self):
        """Build mapping from policy index to move"""
        # Simplified move encoding: from_square (64) * to_square (64) = 4096
        # This covers all possible from-to combinations
        # Promotions are handled by checking if move is a promotion
        self.index_to_move = {}
        self.move_to_index = {}
        
        idx = 0
        for from_square in range(64):
            for to_square in range(64):
                if from_square != to_square:
                    self.index_to_move[idx] = (from_square, to_square)
                    self.move_to_index[(from_square, to_square)] = idx
                idx += 1
    
    def decode_policy(self, policy_logits: np.ndarray, legal_moves: List[str]) -> List[Tuple[str, float]]:
        """
        Decode policy output to legal moves with probabilities
        
        Args:
            policy_logits: Array of shape (4096,) with policy logits
            legal_moves: List of legal moves in UCI format
        
        Returns:
            List of (move, probability) tuples sorted by probability (highest first)
        """
        # Apply softmax to get probabilities
        policy_probs = self._softmax(policy_logits)
        
        # Map legal moves to their probabilities
        move_probs = []
        for move_uci in legal_moves:
            move = chess.Move.from_uci(move_uci)
            from_square = move.from_square
            to_square = move.to_square
            
            # Get index for this move
            key = (from_square, to_square)
            if key in self.move_to_index:
                idx = self.move_to_index[key]
                prob = policy_probs[idx]
                move_probs.append((move_uci, float(prob)))
            else:
                # Fallback for moves not in mapping
                move_probs.append((move_uci, 0.0))
        
        # Sort by probability (highest first)
        move_probs.sort(key=lambda x: x[1], reverse=True)
        
        return move_probs
    
    def _softmax(self, x: np.ndarray) -> np.ndarray:
        """Apply softmax to convert logits to probabilities"""
        # Subtract max for numerical stability
        exp_x = np.exp(x - np.max(x))
        return exp_x / np.sum(exp_x)
    
    def encode_move(self, move_uci: str) -> int:
        """
        Encode a move to policy index
        
        Args:
            move_uci: Move in UCI format
        
        Returns:
            Policy index for this move
        """
        move = chess.Move.from_uci(move_uci)
        key = (move.from_square, move.to_square)
        return self.move_to_index.get(key, 0)
