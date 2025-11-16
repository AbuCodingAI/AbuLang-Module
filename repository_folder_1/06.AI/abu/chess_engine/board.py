"""Chess board wrapper around python-chess library"""

import chess
from typing import List, Optional


class ChessBoard:
    """Wrapper around chess board state"""
    
    def __init__(self):
        """Initialize a new chess board with standard starting position"""
        self.board = chess.Board()
    
    def make_move(self, move: str) -> bool:
        """
        Make a move on the board
        
        Args:
            move: Move in UCI format (e.g., 'e2e4') or SAN format (e.g., 'e4')
        
        Returns:
            True if move was successful, False otherwise
        """
        try:
            # Try parsing as UCI first
            chess_move = chess.Move.from_uci(move)
            if chess_move in self.board.legal_moves:
                self.board.push(chess_move)
                return True
        except ValueError:
            # Try parsing as SAN (algebraic notation)
            try:
                chess_move = self.board.parse_san(move)
                self.board.push(chess_move)
                return True
            except ValueError:
                pass
        
        return False
    
    def get_legal_moves(self) -> List[str]:
        """
        Get all legal moves in current position
        
        Returns:
            List of moves in UCI format
        """
        return [move.uci() for move in self.board.legal_moves]
    
    def is_game_over(self) -> bool:
        """
        Check if the game is over
        
        Returns:
            True if game is over (checkmate, stalemate, or draw)
        """
        return self.board.is_game_over()
    
    def get_game_result(self) -> Optional[str]:
        """
        Get the game result
        
        Returns:
            '1-0' for white win, '0-1' for black win, '1/2-1/2' for draw, None if game not over
        """
        if not self.is_game_over():
            return None
        
        result = self.board.result()
        return result
    
    def undo_move(self) -> bool:
        """
        Undo the last move
        
        Returns:
            True if undo was successful, False if no moves to undo
        """
        try:
            self.board.pop()
            return True
        except IndexError:
            return False
    
    def get_fen(self) -> str:
        """
        Get the current position in FEN notation
        
        Returns:
            FEN string representing current position
        """
        return self.board.fen()
    
    def from_fen(self, fen: str) -> bool:
        """
        Load a position from FEN notation
        
        Args:
            fen: FEN string representing a chess position
        
        Returns:
            True if FEN was valid and loaded, False otherwise
        """
        try:
            self.board = chess.Board(fen)
            return True
        except ValueError:
            return False
    
    def is_check(self) -> bool:
        """Check if current player is in check"""
        return self.board.is_check()
    
    def is_checkmate(self) -> bool:
        """Check if current position is checkmate"""
        return self.board.is_checkmate()
    
    def is_stalemate(self) -> bool:
        """Check if current position is stalemate"""
        return self.board.is_stalemate()
    
    def is_insufficient_material(self) -> bool:
        """Check if position has insufficient material for checkmate"""
        return self.board.is_insufficient_material()
    
    def can_claim_fifty_moves(self) -> bool:
        """Check if fifty-move rule can be claimed"""
        return self.board.can_claim_fifty_moves()
    
    def can_claim_threefold_repetition(self) -> bool:
        """Check if threefold repetition can be claimed"""
        return self.board.can_claim_threefold_repetition()
    
    def get_turn(self) -> str:
        """Get whose turn it is ('white' or 'black')"""
        return 'white' if self.board.turn == chess.WHITE else 'black'
    
    def copy(self) -> 'ChessBoard':
        """Create a copy of the current board"""
        new_board = ChessBoard()
        new_board.board = self.board.copy()
        return new_board
    
    def get_move_history(self) -> List[str]:
        """Get the move history in UCI format"""
        return [move.uci() for move in self.board.move_stack]
    
    def __str__(self) -> str:
        """String representation of the board"""
        return str(self.board)
