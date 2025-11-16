"""Player implementations for game controller"""

from abc import ABC, abstractmethod
from abu.chess_engine import ChessBoard
from abu.ai_player import AbuPlayer


class Player(ABC):
    """Abstract base class for players"""
    
    @abstractmethod
    def get_move(self, board: ChessBoard) -> str:
        """
        Get a move from the player
        
        Args:
            board: Current board position
        
        Returns:
            Move in UCI format
        """
        pass


class HumanPlayer(Player):
    """Human player implementation"""
    
    def __init__(self, prompt_func=None):
        """
        Initialize human player
        
        Args:
            prompt_func: Function to prompt for move input
        """
        self.prompt_func = prompt_func or input
    
    def get_move(self, board: ChessBoard) -> str:
        """Prompt human for move"""
        while True:
            move = self.prompt_func("Enter your move: ").strip()
            if board.make_move(move):
                board.undo_move()  # Undo to let controller make the move
                return move
            else:
                print("Invalid move! Try again.")


class AIPlayer(Player):
    """AI player wrapper"""
    
    def __init__(self, abu_player: AbuPlayer):
        """
        Initialize AI player
        
        Args:
            abu_player: AbuPlayer instance
        """
        self.abu_player = abu_player
    
    def get_move(self, board: ChessBoard) -> str:
        """Get move from Abu"""
        return self.abu_player.select_move(board)
