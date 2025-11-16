"""Board renderer for displaying chess positions"""

from abu.chess_engine import ChessBoard


class BoardRenderer:
    """Renders chess board for display"""
    
    # Unicode chess pieces
    UNICODE_PIECES = {
        'P': '♙', 'N': '♘', 'B': '♗', 'R': '♖', 'Q': '♕', 'K': '♔',
        'p': '♟', 'n': '♞', 'b': '♝', 'r': '♜', 'q': '♛', 'k': '♚'
    }
    
    # ASCII chess pieces
    ASCII_PIECES = {
        'P': 'P', 'N': 'N', 'B': 'B', 'R': 'R', 'Q': 'Q', 'K': 'K',
        'p': 'p', 'n': 'n', 'b': 'b', 'r': 'r', 'q': 'q', 'k': 'k'
    }
    
    def render_unicode(self, board: ChessBoard) -> str:
        """
        Render board with Unicode chess symbols
        
        Args:
            board: ChessBoard to render
        
        Returns:
            String representation with Unicode pieces
        """
        return self._render(board, self.UNICODE_PIECES)
    
    def render_ascii(self, board: ChessBoard) -> str:
        """
        Render board with ASCII characters
        
        Args:
            board: ChessBoard to render
        
        Returns:
            String representation with ASCII pieces
        """
        return self._render(board, self.ASCII_PIECES)
    
    def _render(self, board: ChessBoard, piece_set: dict) -> str:
        """Internal rendering method"""
        lines = []
        lines.append("  +---+---+---+---+---+---+---+---+")
        
        # Render from rank 8 to rank 1 (top to bottom)
        for rank in range(7, -1, -1):
            line = f"{rank + 1} |"
            for file in range(8):
                square = rank * 8 + file
                piece = board.board.piece_at(square)
                
                if piece:
                    symbol = piece.symbol()
                    piece_char = piece_set.get(symbol, symbol)
                else:
                    piece_char = ' '
                
                line += f" {piece_char} |"
            
            lines.append(line)
            lines.append("  +---+---+---+---+---+---+---+---+")
        
        # Add file labels
        lines.append("    a   b   c   d   e   f   g   h")
        
        return '\n'.join(lines)
