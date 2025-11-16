"""Board encoder for converting chess positions to neural network input"""

import numpy as np
import chess
from abu.chess_engine import ChessBoard


class BoardEncoder:
    """Encodes chess board into neural network input format"""
    
    def encode(self, board: ChessBoard) -> np.ndarray:
        """
        Encode chess board as 8x8x14 tensor
        
        Planes:
        0-5: White pieces (pawn, knight, bishop, rook, queen, king)
        6-11: Black pieces (pawn, knight, bishop, rook, queen, king)
        12: Current player (1 if white to move, 0 if black)
        13: Castling rights and en passant
        
        Args:
            board: ChessBoard instance to encode
        
        Returns:
            8x8x14 numpy array
        """
        tensor = np.zeros((8, 8, 14), dtype=np.float32)
        
        # Piece type mapping
        piece_to_plane = {
            chess.PAWN: 0,
            chess.KNIGHT: 1,
            chess.BISHOP: 2,
            chess.ROOK: 3,
            chess.QUEEN: 4,
            chess.KING: 5
        }
        
        # Encode pieces
        for square in chess.SQUARES:
            piece = board.board.piece_at(square)
            if piece is not None:
                rank = chess.square_rank(square)
                file = chess.square_file(square)
                
                plane_offset = 0 if piece.color == chess.WHITE else 6
                plane = plane_offset + piece_to_plane[piece.piece_type]
                
                tensor[rank, file, plane] = 1.0
        
        # Encode current player (plane 12)
        if board.board.turn == chess.WHITE:
            tensor[:, :, 12] = 1.0
        
        # Encode castling rights and en passant (plane 13)
        # Castling rights: use corners for each castling right
        if board.board.has_kingside_castling_rights(chess.WHITE):
            tensor[0, 7, 13] = 1.0
        if board.board.has_queenside_castling_rights(chess.WHITE):
            tensor[0, 0, 13] = 1.0
        if board.board.has_kingside_castling_rights(chess.BLACK):
            tensor[7, 7, 13] = 1.0
        if board.board.has_queenside_castling_rights(chess.BLACK):
            tensor[7, 0, 13] = 1.0
        
        # En passant: mark the file where en passant is possible
        if board.board.ep_square is not None:
            ep_file = chess.square_file(board.board.ep_square)
            ep_rank = chess.square_rank(board.board.ep_square)
            tensor[ep_rank, ep_file, 13] = 0.5
        
        return tensor
