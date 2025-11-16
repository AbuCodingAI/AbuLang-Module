"""Main entry point for Abu Chess AI"""

import torch
import os
from abu.chess_engine import ChessBoard
from abu.neural_network import ChessNet, BoardEncoder
from abu.ai_player import AbuPlayer
from abu.ui import CLI
from abu.persistence import ModelPersistence
from abu.training import Trainer, GameDataCollector
from abu.training.stockfish_generator import StockfishGenerator


def play_game(cli: CLI, abu_player: AbuPlayer, human_plays_white: bool = True):
    """Play a game between human and Abu"""
    board = ChessBoard()
    
    cli.clear_screen()
    cli.display_message("Game started! Enter moves in UCI format (e.g., 'e2e4') or algebraic notation (e.g., 'e4')")
    cli.display_message("Type 'quit' to exit, 'history' to see moves, 'analysis' for move analysis")
    
    while not board.is_game_over():
        cli.display_board(board)
        
        current_turn_white = board.get_turn() == 'white'
        is_human_turn = (human_plays_white and current_turn_white) or (not human_plays_white and not current_turn_white)
        
        if is_human_turn:
            # Human's turn
            while True:
                move = cli.prompt_move()
                
                if move.lower() == 'quit':
                    return
                elif move.lower() == 'history':
                    cli.show_move_history(board.get_move_history())
                    continue
                elif move.lower() == 'analysis':
                    analysis = abu_player.get_move_analysis(board, top_n=3)
                    cli.display_move_analysis(analysis)
                    continue
                
                if board.make_move(move):
                    break
                else:
                    cli.display_message("Invalid move! Try again.")
        else:
            # Abu's turn
            cli.display_message("Abu is thinking...")
            move = abu_player.select_move(board)
            board.make_move(move)
            cli.display_message(f"Abu plays: {move}")
    
    # Game over
    cli.display_board(board)
    result = board.get_game_result()
    cli.display_message(f"Game Over! Result: {result}")
    
    if board.is_checkmate():
        winner = "Black" if board.get_turn() == 'white' else "White"
        cli.display_message(f"Checkmate! {winner} wins!")
    elif board.is_stalemate():
        cli.display_message("Stalemate!")
    else:
        cli.display_message("Draw!")


def train_model(cli: CLI, model: ChessNet, model_path: str):
    """Train the model"""
    cli.display_message("=== Training Mode ===")
    
    # Ask for training data source
    cli.display_message("\nTraining data source:")
    cli.display_message("1. Generate with Stockfish")
    cli.display_message("2. Load existing data")
    
    choice = input("Enter choice (1-2): ").strip()
    
    collector = GameDataCollector()
    
    if choice == '1':
        # Generate data with Stockfish
        stockfish_path = input("Enter Stockfish path (or press Enter for 'stockfish'): ").strip()
        if not stockfish_path:
            stockfish_path = "stockfish"
        
        depth = input("Enter Stockfish depth (default 10): ").strip()
        depth = int(depth) if depth else 10
        
        num_games = input("Enter number of games to generate (default 10): ").strip()
        num_games = int(num_games) if num_games else 10
        
        cli.display_message(f"\nGenerating {num_games} games with Stockfish (depth {depth})...")
        
        try:
            generator = StockfishGenerator(stockfish_path, depth)
            games = generator.generate_game_data(num_games)
            
            # Convert games to training examples
            encoder = BoardEncoder()
            for game in games:
                for i, (position, move) in enumerate(zip(game.positions, game.moves)):
                    # Determine value based on game result and position
                    # Alternate sign based on whose turn it was
                    value = game.result if i % 2 == 0 else -game.result
                    
                    collector.record_position(
                        board_tensor=position,
                        move=move,
                        value_target=value
                    )
            
            cli.display_message(f"Generated {len(collector)} training examples")
            
            # Save training data
            data_path = "training_data/stockfish_games.pkl"
            os.makedirs("training_data", exist_ok=True)
            collector.save_training_data(data_path)
            cli.display_message(f"Saved training data to {data_path}")
            
        except Exception as e:
            cli.display_message(f"Error generating data: {e}")
            return
    
    elif choice == '2':
        # Load existing data
        data_path = input("Enter path to training data: ").strip()
        try:
            collector.load_training_data(data_path)
            cli.display_message(f"Loaded {len(collector)} training examples")
        except Exception as e:
            cli.display_message(f"Error loading data: {e}")
            return
    else:
        cli.display_message("Invalid choice")
        return
    
    if len(collector) == 0:
        cli.display_message("No training data available")
        return
    
    # Training parameters
    epochs = input("Enter number of epochs (default 10): ").strip()
    epochs = int(epochs) if epochs else 10
    
    batch_size = input("Enter batch size (default 32): ").strip()
    batch_size = int(batch_size) if batch_size else 32
    
    # Train
    cli.display_message(f"\nTraining for {epochs} epochs...")
    
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    cli.display_message(f"Using device: {device}")
    
    trainer = Trainer(model, learning_rate=0.001, weight_decay=1e-4, device=device)
    
    try:
        history = trainer.train_on_games(
            collector.get_training_examples(),
            epochs=epochs,
            batch_size=batch_size,
            validation_split=0.1
        )
        
        cli.display_message("\nTraining complete!")
        cli.display_message(f"Final train loss: {history['final_train_loss']:.4f}")
        cli.display_message(f"Final val loss: {history['final_val_loss']:.4f}")
        
        # Save model
        if cli.prompt_yes_no("Save trained model?"):
            ModelPersistence.save_model(model, model_path, {
                'training_history': history,
                'num_examples': len(collector)
            })
            cli.display_message(f"Model saved to {model_path}.pth")
    
    except Exception as e:
        cli.display_message(f"Error during training: {e}")


def main():
    """Main application entry point"""
    cli = CLI(use_unicode=True)
    
    # Model path
    model_path = "models/abu_model"
    os.makedirs("models", exist_ok=True)
    
    # Load or create model
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    
    if ModelPersistence.model_exists(model_path):
        cli.display_message("Loading existing model...")
        model, metadata = ModelPersistence.load_model(model_path, device)
        cli.display_message("Model loaded successfully!")
    else:
        cli.display_message("Creating new model...")
        model = ChessNet(num_residual_blocks=5, num_filters=128)
        cli.display_message("New model created (untrained)")
    
    # Create Abu player
    abu_player = AbuPlayer(model, device=device)
    
    # Main loop
    while True:
        choice = cli.show_menu()
        
        if choice == '1':
            # Human vs Abu
            difficulty = cli.prompt_difficulty()
            abu_player.set_difficulty(difficulty)
            human_white = cli.prompt_yes_no("Do you want to play as White?")
            play_game(cli, abu_player, human_white)
        
        elif choice == '2':
            # Abu vs Abu
            cli.display_message("Abu vs Abu not yet implemented")
        
        elif choice == '3':
            # Load game
            cli.display_message("Load game not yet implemented")
        
        elif choice == '4':
            # Train model
            train_model(cli, model, model_path)
        
        elif choice == '5':
            # Generate training data
            cli.display_message("Use option 4 (Train Model) and select 'Generate with Stockfish'")
        
        elif choice == '6':
            # Quit
            cli.display_message("Thanks for playing Abu Chess AI!")
            break
        
        else:
            cli.display_message("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
