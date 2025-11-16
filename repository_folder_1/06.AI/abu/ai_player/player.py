"""AI player using neural network for move selection"""

import torch
import numpy as np
from dataclasses import dataclass
from typing import List, Optional
import time

from abu.chess_engine import ChessBoard
from abu.neural_network import ChessNet, BoardEncoder, MoveDecoder


@dataclass
class MoveAnalysis:
    """Container for move analysis information"""
    move: str
    evaluation: float
    policy_score: float
    principal_variation: Optional[List[str]] = None


class AbuPlayer:
    """AI player that uses neural network for move selection"""
    
    def __init__(self, model: ChessNet, difficulty: str = "advanced", device: str = 'cpu'):
        """
        Initialize Abu player
        
        Args:
            model: ChessNet model for evaluation
            difficulty: Difficulty level ('beginner', 'intermediate', 'advanced')
            device: Device to run model on ('cpu' or 'cuda')
        """
        self.model = model.to(device)
        self.model.eval()
        self.device = device
        self.difficulty = difficulty
        
        self.encoder = BoardEncoder()
        self.decoder = MoveDecoder()
        
        # Timeout for move selection (seconds)
        self.timeout = 5.0
    
    def select_move(self, board: ChessBoard) -> str:
        """
        Select a move using the neural network
        
        Args:
            board: Current board position
        
        Returns:
            Selected move in UCI format
        """
        start_time = time.time()
        
        try:
            # Get move probabilities from network
            move_probs = self._get_move_probabilities(board)
            
            # Check timeout
            if time.time() - start_time > self.timeout:
                print("Warning: Move selection timeout, using fallback")
                return self._fallback_move(board)
            
            # Apply difficulty adjustment
            from abu.ai_player.difficulty import DifficultyController
            selected_move = DifficultyController.apply_difficulty(
                move_probs, self.difficulty
            )
            
            return selected_move
        
        except Exception as e:
            print(f"Error in move selection: {e}")
            return self._fallback_move(board)
    
    def get_move_analysis(self, board: ChessBoard, top_n: int = 3) -> List[MoveAnalysis]:
        """
        Get analysis of top moves
        
        Args:
            board: Current board position
            top_n: Number of top moves to return
        
        Returns:
            List of MoveAnalysis for top moves
        """
        move_probs = self._get_move_probabilities(board)
        
        # Get board evaluation
        board_tensor = self.encoder.encode(board)
        board_tensor = torch.FloatTensor(board_tensor).unsqueeze(0).to(self.device)
        board_tensor = board_tensor.permute(0, 3, 1, 2)
        
        with torch.no_grad():
            _, value = self.model(board_tensor)
            evaluation = value.item()
        
        # Create analysis for top moves
        analyses = []
        for i, (move, prob) in enumerate(move_probs[:top_n]):
            analysis = MoveAnalysis(
                move=move,
                evaluation=evaluation,
                policy_score=prob
            )
            analyses.append(analysis)
        
        return analyses
    
    def set_difficulty(self, difficulty: str):
        """
        Set difficulty level
        
        Args:
            difficulty: 'beginner', 'intermediate', or 'advanced'
        """
        if difficulty not in ['beginner', 'intermediate', 'advanced']:
            raise ValueError(f"Invalid difficulty: {difficulty}")
        self.difficulty = difficulty
    
    def _get_move_probabilities(self, board: ChessBoard) -> List[tuple]:
        """Get move probabilities from neural network"""
        # Encode board
        board_tensor = self.encoder.encode(board)
        board_tensor = torch.FloatTensor(board_tensor).unsqueeze(0).to(self.device)
        board_tensor = board_tensor.permute(0, 3, 1, 2)  # (1, 14, 8, 8)
        
        # Get legal moves
        legal_moves = board.get_legal_moves()
        
        # Forward pass
        with torch.no_grad():
            policy_logits, _ = self.model(board_tensor)
            policy_logits = policy_logits.cpu().numpy()[0]
        
        # Decode to move probabilities
        move_probs = self.decoder.decode_policy(policy_logits, legal_moves)
        
        return move_probs
    
    def _fallback_move(self, board: ChessBoard) -> str:
        """Fallback to random legal move if network fails"""
        legal_moves = board.get_legal_moves()
        if legal_moves:
            return np.random.choice(legal_moves)
        return None
