"""Game controller for orchestrating gameplay"""

from dataclasses import dataclass
from typing import List, Optional
from abu.chess_engine import ChessBoard
from abu.game_controller.players import Player


@dataclass
class GameState:
    """Represents current game state"""
    board: ChessBoard
    move_history: List[str]
    current_turn: str
    game_status: str


class GameController:
    """Main game controller"""
    
    def __init__(self, white_player: Player, black_player: Player):
        """
        Initialize game controller
        
        Args:
            white_player: Player instance for white
            black_player: Player instance for black
        """
        self.white_player = white_player
        self.black_player = black_player
        self.board = ChessBoard()
        self.move_history = []
    
    def start_game(self):
        """Start a new game"""
        self.board = ChessBoard()
        self.move_history = []
    
    def play_turn(self) -> bool:
        """
        Play one turn
        
        Returns:
            True if game continues, False if game is over
        """
        if self.board.is_game_over():
            return False
        
        # Get current player
        current_player = self.white_player if self.board.get_turn() == 'white' else self.black_player
        
        # Get move
        move = current_player.get_move(self.board)
        
        # Make move
        if self.board.make_move(move):
            self.move_history.append(move)
            return not self.board.is_game_over()
        
        return False
    
    def get_current_state(self) -> GameState:
        """Get current game state"""
        if self.board.is_game_over():
            status = "Game Over"
        elif self.board.is_check():
            status = "Check"
        else:
            status = "In Progress"
        
        return GameState(
            board=self.board,
            move_history=self.move_history.copy(),
            current_turn=self.board.get_turn(),
            game_status=status
        )
