"""Game data collector for training data management"""

import numpy as np
import pickle
import json
from dataclasses import dataclass, asdict
from typing import List, Optional
from abu.chess_engine import ChessBoard


@dataclass
class TrainingExample:
    """Single training example"""
    board_tensor: np.ndarray  # 8x8x14
    policy_target: np.ndarray  # 4096-dim
    value_target: float  # -1 to +1
    metadata: dict = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


@dataclass
class GameRecord:
    """Record of a complete game"""
    positions: List[np.ndarray]  # Board tensors
    moves: List[str]  # UCI format
    result: float  # 1.0 (white wins), 0.0 (draw), -1.0 (black wins)
    metadata: dict = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


class GameDataCollector:
    """Collects training data from games"""
    
    def __init__(self):
        """Initialize data collector"""
        self.training_examples: List[TrainingExample] = []
        self.game_records: List[GameRecord] = []
    
    def record_position(self, board_tensor: np.ndarray, move: str, 
                       policy_target: Optional[np.ndarray] = None,
                       value_target: Optional[float] = None,
                       metadata: dict = None):
        """
        Record a single position for training
        
        Args:
            board_tensor: Encoded board state (8x8x14)
            move: Move made in UCI format
            policy_target: Target policy distribution (4096-dim), optional
            value_target: Target value (-1 to +1), optional
            metadata: Optional metadata dictionary
        """
        # Create default policy target if not provided (one-hot for the move)
        if policy_target is None:
            policy_target = np.zeros(4096, dtype=np.float32)
        
        # Create default value target if not provided
        if value_target is None:
            value_target = 0.0
        
        example = TrainingExample(
            board_tensor=board_tensor,
            policy_target=policy_target,
            value_target=value_target,
            metadata=metadata or {}
        )
        
        self.training_examples.append(example)
    
    def record_game(self, game_record: GameRecord):
        """
        Record a complete game
        
        Args:
            game_record: GameRecord instance
        """
        self.game_records.append(game_record)
    
    def save_training_data(self, filepath: str):
        """
        Save training data to disk
        
        Args:
            filepath: Path to save the data
        """
        data = {
            'training_examples': self.training_examples,
            'game_records': self.game_records
        }
        
        with open(filepath, 'wb') as f:
            pickle.dump(data, f)
    
    def load_training_data(self, filepath: str):
        """
        Load training data from disk
        
        Args:
            filepath: Path to load the data from
        """
        with open(filepath, 'rb') as f:
            data = pickle.load(f)
        
        self.training_examples = data.get('training_examples', [])
        self.game_records = data.get('game_records', [])
    
    def get_training_examples(self) -> List[TrainingExample]:
        """Get all training examples"""
        return self.training_examples
    
    def get_game_records(self) -> List[GameRecord]:
        """Get all game records"""
        return self.game_records
    
    def clear(self):
        """Clear all collected data"""
        self.training_examples.clear()
        self.game_records.clear()
    
    def __len__(self) -> int:
        """Return number of training examples"""
        return len(self.training_examples)
