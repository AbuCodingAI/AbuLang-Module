"""Stockfish integration for generating training data"""

import subprocess
import chess
import numpy as np
from typing import List, Tuple, Optional
from abu.chess_engine import ChessBoard
from abu.neural_network import BoardEncoder, MoveDecoder
from abu.training.collector import TrainingExample, GameRecord


class StockfishGenerator:
    """Generate training data using Stockfish engine"""
    
    def __init__(self, stockfish_path: str = "stockfish", depth: int = 10, 
                 exploration_noise: float = 0.0):
        """
        Initialize Stockfish generator
        
        Args:
            stockfish_path: Path to Stockfish executable
            depth: Search depth for Stockfish (higher = stronger but slower)
            exploration_noise: Probability of making a random move (0.0-1.0)
                             0.0 = perfect play, 0.2 = 20% random moves (blunders)
        """
        self.stockfish_path = stockfish_path
        self.depth = depth
        self.exploration_noise = exploration_noise
        self.encoder = BoardEncoder()
        self.decoder = MoveDecoder()
    
    def generate_position_data(self, board: ChessBoard, 
                              num_variations: int = 1) -> List[TrainingExample]:
        """
        Generate training data for a position using Stockfish
        
        Args:
            board: ChessBoard position to analyze
            num_variations: Number of top moves to consider
        
        Returns:
            List of TrainingExample instances
        """
        examples = []
        
        # Get Stockfish analysis
        analysis = self._analyze_position(board)
        
        if not analysis:
            return examples
        
        # Encode board
        board_tensor = self.encoder.encode(board)
        
        # Create policy target from Stockfish's top moves
        policy_target = self._create_policy_target(analysis, board)
        
        # Use Stockfish's evaluation as value target
        value_target = self._normalize_score(analysis['score'])
        
        example = TrainingExample(
            board_tensor=board_tensor,
            policy_target=policy_target,
            value_target=value_target,
            metadata={'stockfish_depth': self.depth}
        )
        
        examples.append(example)
        
        return examples
    
    def generate_game_data(self, num_games: int = 10, 
                          max_moves: int = 100) -> List[GameRecord]:
        """
        Generate complete games using Stockfish self-play with exploration noise
        
        Exploration noise adds random moves during play, but we ONLY collect
        positions where Stockfish made the move (not random blunders).
        This way Abu learns from good positions while still seeing varied games.
        
        Args:
            num_games: Number of games to generate
            max_moves: Maximum moves per game
        
        Returns:
            List of GameRecord instances
        """
        games = []
        
        # Statistics tracking
        stats = {
            'white_wins': 0,
            'black_wins': 0,
            'draws': 0,
            'checkmates': 0,
            'stalemates': 0,
            'max_moves': 0,
            'fifty_move': 0,
            'repetition': 0,
            'insufficient_material': 0,
            'stockfish_errors': 0
        }
        
        for game_num in range(num_games):
            board = ChessBoard()
            positions = []
            moves = []
            
            move_count = 0
            stockfish_error = False
            
            while not board.is_game_over() and move_count < max_moves:
                # Decide: use Stockfish or make random move (exploration noise)
                use_stockfish = np.random.random() >= self.exploration_noise
                
                if use_stockfish:
                    # Get Stockfish's best move
                    analysis = self._analyze_position(board)
                    if not analysis or 'bestmove' not in analysis:
                        stockfish_error = True
                        break
                    move = analysis['bestmove']
                    
                    # ONLY record position when Stockfish makes the move
                    board_tensor = self.encoder.encode(board)
                    positions.append(board_tensor)
                    moves.append(move)
                else:
                    # Make a random legal move (blunder/exploration)
                    # DON'T record this position - we don't want to learn from blunders!
                    legal_moves = board.get_legal_moves()
                    if not legal_moves:
                        break
                    move = np.random.choice(legal_moves)
                
                # Make the move
                if not board.make_move(move):
                    break
                
                move_count += 1
            
            # Determine result and reason
            result_str = board.get_game_result()
            reason = ""
            
            if stockfish_error:
                result = 0.0
                result_str = "1/2-1/2"
                reason = " (Stockfish error)"
                stats['draws'] += 1
                stats['stockfish_errors'] += 1
            elif move_count >= max_moves:
                result = 0.0
                result_str = "1/2-1/2"
                reason = " (Max moves)"
                stats['draws'] += 1
                stats['max_moves'] += 1
            elif result_str == '1-0':
                result = 1.0
                stats['white_wins'] += 1
                if board.is_checkmate():
                    reason = " (Checkmate)"
                    stats['checkmates'] += 1
                else:
                    reason = " (White wins)"
            elif result_str == '0-1':
                result = -1.0
                stats['black_wins'] += 1
                if board.is_checkmate():
                    reason = " (Checkmate)"
                    stats['checkmates'] += 1
                else:
                    reason = " (Black wins)"
            else:
                result = 0.0
                stats['draws'] += 1
                if board.is_stalemate():
                    reason = " (Stalemate)"
                    stats['stalemates'] += 1
                elif board.is_insufficient_material():
                    reason = " (Insufficient material)"
                    stats['insufficient_material'] += 1
                elif board.can_claim_fifty_moves():
                    reason = " (50-move rule)"
                    stats['fifty_move'] += 1
                elif board.can_claim_threefold_repetition():
                    reason = " (Repetition)"
                    stats['repetition'] += 1
                else:
                    reason = " (Draw)"
            
            game_record = GameRecord(
                positions=positions,
                moves=moves,
                result=result,
                metadata={
                    'stockfish_depth': self.depth, 
                    'game_num': game_num,
                    'reason': reason.strip(),
                    'num_moves': move_count
                }
            )
            
            games.append(game_record)
            print(f"Generated game {game_num + 1}/{num_games}: {result_str}{reason}")
        
        # Print statistics summary
        print("\n" + "=" * 50)
        print("Game Generation Statistics")
        print("=" * 50)
        print(f"Total Games: {num_games}")
        print(f"White Wins:  {stats['white_wins']} ({stats['white_wins']/num_games*100:.1f}%)")
        print(f"Black Wins:  {stats['black_wins']} ({stats['black_wins']/num_games*100:.1f}%)")
        print(f"Draws:       {stats['draws']} ({stats['draws']/num_games*100:.1f}%)")
        print("\nDraw Reasons:")
        if stats['stalemates'] > 0:
            print(f"  Stalemate: {stats['stalemates']}")
        if stats['max_moves'] > 0:
            print(f"  Max moves: {stats['max_moves']}")
        if stats['fifty_move'] > 0:
            print(f"  50-move rule: {stats['fifty_move']}")
        if stats['repetition'] > 0:
            print(f"  Repetition: {stats['repetition']}")
        if stats['insufficient_material'] > 0:
            print(f"  Insufficient material: {stats['insufficient_material']}")
        if stats['stockfish_errors'] > 0:
            print(f"  Stockfish errors: {stats['stockfish_errors']}")
        print(f"\nCheckmates: {stats['checkmates']}")
        print("=" * 50 + "\n")
        
        return games
    
    def _analyze_position(self, board: ChessBoard) -> Optional[dict]:
        """
        Analyze position with Stockfish
        
        Returns:
            Dictionary with 'score', 'bestmove', and 'pv' (principal variation)
        """
        try:
            # Start Stockfish process
            process = subprocess.Popen(
                [self.stockfish_path],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )
            
            # Send commands
            commands = [
                "uci",
                f"position fen {board.get_fen()}",
                f"go depth {self.depth}"
            ]
            
            for cmd in commands:
                process.stdin.write(cmd + "\n")
                process.stdin.flush()
            
            # Read output
            bestmove = None
            score = 0
            pv = []
            
            while True:
                line = process.stdout.readline().strip()
                
                if line.startswith('bestmove'):
                    parts = line.split()
                    if len(parts) >= 2:
                        bestmove = parts[1]
                    break
                
                if 'score cp' in line:
                    # Centipawn score
                    parts = line.split()
                    cp_idx = parts.index('cp') + 1
                    if cp_idx < len(parts):
                        score = int(parts[cp_idx])
                
                if 'score mate' in line:
                    # Mate score
                    parts = line.split()
                    mate_idx = parts.index('mate') + 1
                    if mate_idx < len(parts):
                        mate_in = int(parts[mate_idx])
                        score = 10000 if mate_in > 0 else -10000
            
            process.terminate()
            process.wait()
            
            return {
                'score': score,
                'bestmove': bestmove,
                'pv': pv
            }
        
        except Exception as e:
            print(f"Stockfish analysis error: {e}")
            return None
    
    def _create_policy_target(self, analysis: dict, board: ChessBoard) -> np.ndarray:
        """Create policy target from Stockfish analysis"""
        policy = np.zeros(4096, dtype=np.float32)
        
        if 'bestmove' in analysis and analysis['bestmove']:
            # One-hot encoding for best move
            move_idx = self.decoder.encode_move(analysis['bestmove'])
            policy[move_idx] = 1.0
        
        return policy
    
    def _normalize_score(self, centipawns: int) -> float:
        """
        Normalize centipawn score to [-1, 1] range
        
        Args:
            centipawns: Score in centipawns
        
        Returns:
            Normalized score between -1 and 1
        """
        # Use tanh to map to [-1, 1]
        # Divide by 400 so that ~4 pawn advantage = 0.99
        return np.tanh(centipawns / 400.0)
