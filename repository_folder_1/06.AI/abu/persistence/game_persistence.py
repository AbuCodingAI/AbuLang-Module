"""Game persistence for saving and loading games"""

import json
import os
from typing import List, Optional
from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass
class GameMetadata:
    """Metadata for a saved game"""
    filename: str
    date: str
    white_player: str
    black_player: str
    result: Optional[str]
    num_moves: int


class GamePersistence:
    """Handles game save/load operations"""
    
    @staticmethod
    def save_game(board_fen: str, move_history: List[str], 
                  filepath: str, metadata: dict = None):
        """
        Save game state to JSON file
        
        Args:
            board_fen: Current board position in FEN notation
            move_history: List of moves in UCI format
            filepath: Path to save the game
            metadata: Optional metadata dictionary
        """
        game_data = {
            'fen': board_fen,
            'moves': move_history,
            'date': datetime.now().isoformat(),
            'metadata': metadata or {}
        }
        
        os.makedirs(os.path.dirname(filepath) if os.path.dirname(filepath) else '.', exist_ok=True)
        
        with open(filepath, 'w') as f:
            json.dump(game_data, f, indent=2)
    
    @staticmethod
    def load_game(filepath: str) -> tuple:
        """
        Load game state from JSON file
        
        Args:
            filepath: Path to the saved game
        
        Returns:
            Tuple of (fen, move_history, metadata)
        """
        with open(filepath, 'r') as f:
            game_data = json.load(f)
        
        return (
            game_data['fen'],
            game_data['moves'],
            game_data.get('metadata', {})
        )
    
    @staticmethod
    def list_saved_games(directory: str = 'saved_games') -> List[GameMetadata]:
        """
        List all saved games in directory
        
        Args:
            directory: Directory to search for saved games
        
        Returns:
            List of GameMetadata objects
        """
        if not os.path.exists(directory):
            return []
        
        games = []
        for filename in os.listdir(directory):
            if filename.endswith('.json'):
                filepath = os.path.join(directory, filename)
                try:
                    fen, moves, metadata = GamePersistence.load_game(filepath)
                    
                    game_meta = GameMetadata(
                        filename=filename,
                        date=metadata.get('date', 'Unknown'),
                        white_player=metadata.get('white_player', 'Unknown'),
                        black_player=metadata.get('black_player', 'Unknown'),
                        result=metadata.get('result'),
                        num_moves=len(moves)
                    )
                    games.append(game_meta)
                except Exception:
                    continue
        
        return games
    
    @staticmethod
    def export_pgn(move_history: List[str], filepath: str, 
                   white_player: str = "White", black_player: str = "Black",
                   result: str = "*"):
        """
        Export game to PGN format
        
        Args:
            move_history: List of moves in UCI format
            filepath: Path to save PGN file
            white_player: White player name
            black_player: Black player name
            result: Game result (1-0, 0-1, 1/2-1/2, or *)
        """
        pgn_lines = [
            f'[Event "Abu Chess Game"]',
            f'[Date "{datetime.now().strftime("%Y.%m.%d")}"]',
            f'[White "{white_player}"]',
            f'[Black "{black_player}"]',
            f'[Result "{result}"]',
            ''
        ]
        
        # Format moves in PGN style
        move_text = []
        for i in range(0, len(move_history), 2):
            move_num = i // 2 + 1
            white_move = move_history[i]
            black_move = move_history[i + 1] if i + 1 < len(move_history) else ""
            
            if black_move:
                move_text.append(f"{move_num}. {white_move} {black_move}")
            else:
                move_text.append(f"{move_num}. {white_move}")
        
        pgn_lines.append(' '.join(move_text) + f" {result}")
        
        with open(filepath, 'w') as f:
            f.write('\n'.join(pgn_lines))
