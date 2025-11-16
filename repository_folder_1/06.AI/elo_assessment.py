"""ELO Assessment - Test Abu against Stockfish at different levels"""

import torch
import os
from datetime import datetime
from abu.chess_engine import ChessBoard
from abu.neural_network import ChessNet, BoardEncoder
from abu.ai_player import AbuPlayer
from abu.persistence import ModelPersistence
from abu.training.stockfish_generator import StockfishGenerator
import subprocess
import chess


def play_abu_vs_stockfish(abu_player: AbuPlayer, stockfish_path: str, 
                          stockfish_depth: int, abu_plays_white: bool,
                          game_num: int, exploration_noise: float = 0.0,
                          max_moves: int = 150) -> dict:
    """
    Play one game: Abu vs Stockfish
    
    Args:
        abu_player: Abu AI player
        stockfish_path: Path to Stockfish executable
        stockfish_depth: Stockfish search depth
        abu_plays_white: True if Abu plays white
        game_num: Game number
        exploration_noise: Stockfish exploration noise (0.0 = perfect play)
        max_moves: Maximum moves per game
    
    Returns:
        dict with game info
    """
    board = ChessBoard()
    moves_san = []
    
    move_count = 0
    while not board.is_game_over() and move_count < max_moves:
        is_abu_turn = (board.get_turn() == 'white') == abu_plays_white
        
        if is_abu_turn:
            # Abu's move
            move_uci = abu_player.select_move(board)
        else:
            # Stockfish's move
            if exploration_noise > 0 and __import__('random').random() < exploration_noise:
                # Random move (noisy Stockfish)
                legal_moves = board.get_legal_moves()
                move_uci = __import__('random').choice(legal_moves)
            else:
                # Stockfish best move
                move_uci = get_stockfish_move(board, stockfish_path, stockfish_depth)
        
        if not move_uci:
            break
        
        # Convert to SAN before making move
        try:
            move_san = board.board.san(board.board.parse_uci(move_uci))
        except:
            move_san = move_uci
        
        # Make move
        if not board.make_move(move_uci):
            break
        
        moves_san.append(move_san)
        move_count += 1
    
    # Get result
    result_str = board.get_game_result() or "*"
    
    # Determine winner from Abu's perspective
    if result_str == "*":
        abu_result = "Draw"
    elif (result_str == '1-0' and abu_plays_white) or (result_str == '0-1' and not abu_plays_white):
        abu_result = "Win"
    elif (result_str == '0-1' and abu_plays_white) or (result_str == '1-0' and not abu_plays_white):
        abu_result = "Loss"
    else:
        abu_result = "Draw"
    
    return {
        'moves_san': moves_san,
        'result_str': result_str,
        'abu_result': abu_result,
        'num_moves': len(moves_san),
        'game_num': game_num,
        'abu_plays_white': abu_plays_white
    }


def get_stockfish_move(board: ChessBoard, stockfish_path: str, depth: int) -> str:
    """Get best move from Stockfish"""
    try:
        process = subprocess.Popen(
            [stockfish_path],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )
        
        commands = [
            "uci",
            f"position fen {board.get_fen()}",
            f"go depth {depth}"
        ]
        
        for cmd in commands:
            process.stdin.write(cmd + "\n")
            process.stdin.flush()
        
        bestmove = None
        while True:
            line = process.stdout.readline().strip()
            if line.startswith('bestmove'):
                parts = line.split()
                if len(parts) >= 2:
                    bestmove = parts[1]
                break
        
        process.terminate()
        process.wait()
        
        return bestmove
    except Exception as e:
        print(f"Stockfish error: {e}")
        return None


def save_game_pgn(game_data: dict, filepath: str, white_name: str, black_name: str, event: str):
    """Save game in PGN format"""
    with open(filepath, 'w') as f:
        f.write(f'[Event "{event}"]\n')
        f.write(f'[Date "{datetime.now().strftime("%Y.%m.%d")}"]\n')
        f.write(f'[White "{white_name}"]\n')
        f.write(f'[Black "{black_name}"]\n')
        f.write(f'[Result "{game_data["result_str"]}"]\n')
        f.write(f'[PlyCount "{game_data["num_moves"]}"]\n')
        f.write('\n')
        
        for i in range(0, len(game_data['moves_san']), 2):
            move_num = i // 2 + 1
            white_move = game_data['moves_san'][i]
            black_move = game_data['moves_san'][i + 1] if i + 1 < len(game_data['moves_san']) else ''
            
            if black_move:
                f.write(f'{move_num}. {white_move} {black_move} ')
            else:
                f.write(f'{move_num}. {white_move} ')
            
            if move_num % 5 == 0:
                f.write('\n')
        
        f.write(f'{game_data["result_str"]}\n')


def run_assessment(abu_player: AbuPlayer, stockfish_path: str, 
                   assessment_name: str, stockfish_depth: int, 
                   exploration_noise: float, num_games: int):
    """Run one ELO assessment"""
    print(f"\n{'=' * 60}")
    print(f"{assessment_name}")
    print(f"{'=' * 60}")
    print(f"Stockfish Depth: {stockfish_depth}")
    print(f"Exploration Noise: {exploration_noise * 100:.0f}%")
    print(f"Number of Games: {num_games}")
    print(f"{'=' * 60}\n")
    
    # Create directory
    dir_name = assessment_name.lower().replace(' ', '_').replace(':', '')
    os.makedirs(dir_name, exist_ok=True)
    
    results = {'Win': 0, 'Loss': 0, 'Draw': 0}
    
    for game_num in range(num_games):
        abu_plays_white = game_num % 2 == 0  # Alternate colors
        
        print(f"Game {game_num + 1}/{num_games} ", end='', flush=True)
        print(f"(Abu plays {'White' if abu_plays_white else 'Black'})...", end=' ', flush=True)
        
        game_data = play_abu_vs_stockfish(
            abu_player, stockfish_path, stockfish_depth,
            abu_plays_white, game_num + 1, exploration_noise
        )
        
        results[game_data['abu_result']] += 1
        print(f"{game_data['abu_result']} ({game_data['num_moves']} moves)")
        
        # Save game
        white_name = "Abu" if abu_plays_white else f"Stockfish (Depth {stockfish_depth})"
        black_name = f"Stockfish (Depth {stockfish_depth})" if abu_plays_white else "Abu"
        
        pgn_path = f"{dir_name}/game_{game_num + 1:03d}.pgn"
        save_game_pgn(game_data, pgn_path, white_name, black_name, assessment_name)
    
    # Calculate statistics
    total = num_games
    win_rate = (results['Win'] / total) * 100
    draw_rate = (results['Draw'] / total) * 100
    loss_rate = (results['Loss'] / total) * 100
    score = results['Win'] + (results['Draw'] * 0.5)
    score_percentage = (score / total) * 100
    
    print(f"\n{'=' * 60}")
    print(f"Results Summary")
    print(f"{'=' * 60}")
    print(f"Wins:  {results['Win']:2d} ({win_rate:5.1f}%)")
    print(f"Draws: {results['Draw']:2d} ({draw_rate:5.1f}%)")
    print(f"Losses: {results['Loss']:2d} ({loss_rate:5.1f}%)")
    print(f"{'=' * 60}")
    print(f"Score: {score:.1f}/{total} ({score_percentage:.1f}%)")
    print(f"Games saved to: {dir_name}/")
    print(f"{'=' * 60}")
    
    return results, score_percentage


def main():
    print("=" * 60)
    print("Abu ELO Assessment")
    print("=" * 60)
    print("Testing Abu against Stockfish at different levels")
    print("All games will be saved in PGN format for review")
    print("=" * 60)
    
    # Configuration
    MODEL_PATH = "models/abu_model"
    STOCKFISH_PATH = "stockfish-windows-x86-64-avx2.exe"
    
    # Load Abu
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    print(f"\nUsing device: {device}")
    
    if not ModelPersistence.model_exists(MODEL_PATH):
        print("ERROR: No trained model found!")
        print("Please train Abu first using: python train_example.py")
        return
    
    print("Loading Abu model...")
    model, metadata = ModelPersistence.load_model(MODEL_PATH, device)
    abu_player = AbuPlayer(model, difficulty='advanced', device=device)
    
    # Assessment 1: Abu vs Noisy Stockfish
    results1, score1 = run_assessment(
        abu_player=abu_player,
        stockfish_path=STOCKFISH_PATH,
        assessment_name="ELO Assessment 1: Abu vs Noisy Stockfish",
        stockfish_depth=10,
        exploration_noise=0.15,  # 15% random moves
        num_games=20
    )
    
    # Assessment 2: Abu vs Normal Stockfish
    results2, score2 = run_assessment(
        abu_player=abu_player,
        stockfish_path=STOCKFISH_PATH,
        assessment_name="ELO Assessment 2: Abu vs Normal Stockfish",
        stockfish_depth=10,
        exploration_noise=0.0,  # Perfect play
        num_games=20
    )
    
    # Final Summary
    print(f"\n{'=' * 60}")
    print("FINAL ASSESSMENT SUMMARY")
    print(f"{'=' * 60}")
    print(f"Assessment 1 (Noisy Stockfish):  {score1:.1f}%")
    print(f"Assessment 2 (Normal Stockfish): {score2:.1f}%")
    print(f"{'=' * 60}")
    print("\nAll games saved in PGN format:")
    print("- elo_assessment_1_abu_vs_noisy_stockfish/")
    print("- elo_assessment_2_abu_vs_normal_stockfish/")
    print("\nYou can review these games with any chess software!")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
