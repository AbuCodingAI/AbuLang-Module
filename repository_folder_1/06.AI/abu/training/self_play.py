"""Self-play generator for creating training data"""

import numpy as np
from typing import List
from abu.chess_engine import ChessBoard
from abu.neural_network import ChessNet, BoardEncoder
from abu.ai_player import AbuPlayer
from abu.training.collector import GameRecord


class SelfPlayGenerator:
    """Generates training data through self-play"""
    
    def __init__(self, model: ChessNet, device: str = 'cpu'):
        """
        Initialize self-play generator
        
        Args:
            model: ChessNet model to use for self-play
            device: Device to run on ('cpu' or 'cuda')
        """
        self.model = model
        self.device = device
        self.encoder = BoardEncoder()
    
    def generate_games(self, num_games: int, max_moves: int = 100) -> List[GameRecord]:
        """
        Generate games through self-play
        
        Args:
            num_games: Number of games to generate
            max_moves: Maximum moves per game
        
        Returns:
            List of GameRecord instances
        """
        games = []
        
        # Create AI player
        player = AbuPlayer(self.model, difficulty='advanced', device=self.device)
        
        for game_num in range(num_games):
            board = ChessBoard()
            positions = []
            moves = []
            
            move_count = 0
            while not board.is_game_over() and move_count < max_moves:
                # Encode current position
                board_tensor = self.encoder.encode(board)
                positions.append(board_tensor)
                
                # Get move from AI
                move = player.select_move(board)
                if not move or not board.make_move(move):
                    break
                
                moves.append(move)
                move_count += 1
            
            # Determine result
            result_str = board.get_game_result()
            if result_str == '1-0':
                result = 1.0
            elif result_str == '0-1':
                result = -1.0
            else:
                result = 0.0
            
            game_record = GameRecord(
                positions=positions,
                moves=moves,
                result=result,
                metadata={'game_num': game_num, 'self_play': True}
            )
            
            games.append(game_record)
            print(f"Self-play game {game_num + 1}/{num_games}: {result_str} ({len(moves)} moves)")
        
        return games
