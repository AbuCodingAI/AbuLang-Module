"""Command-line interface for Abu Chess AI"""

from typing import List, Optional
from abu.chess_engine import ChessBoard
from abu.ui.renderer import BoardRenderer
from abu.ai_player.player import MoveAnalysis


class CLI:
    """Command-line interface"""
    
    def __init__(self, use_unicode: bool = True):
        """
        Initialize CLI
        
        Args:
            use_unicode: Whether to use Unicode chess symbols
        """
        self.renderer = BoardRenderer()
        self.use_unicode = use_unicode
    
    def display_board(self, board: ChessBoard):
        """
        Display the chess board
        
        Args:
            board: ChessBoard to display
        """
        if self.use_unicode:
            print(self.renderer.render_unicode(board))
        else:
            print(self.renderer.render_ascii(board))
        
        print(f"\nTurn: {board.get_turn().capitalize()}")
        
        if board.is_check():
            print("CHECK!")
    
    def prompt_move(self) -> str:
        """
        Prompt user for a move
        
        Returns:
            Move string entered by user
        """
        return input("\nEnter your move (e.g., 'e2e4' or 'e4'): ").strip()
    
    def display_message(self, message: str):
        """
        Display a message to the user
        
        Args:
            message: Message to display
        """
        print(f"\n{message}")
    
    def display_move_analysis(self, analysis: List[MoveAnalysis]):
        """
        Display move analysis
        
        Args:
            analysis: List of MoveAnalysis objects
        """
        print("\n=== Move Analysis ===")
        for i, move_analysis in enumerate(analysis, 1):
            print(f"{i}. {move_analysis.move}")
            print(f"   Evaluation: {move_analysis.evaluation:.3f}")
            print(f"   Policy Score: {move_analysis.policy_score:.3f}")
    
    def show_menu(self) -> str:
        """
        Show main menu and get user choice
        
        Returns:
            User's menu choice
        """
        print("\n" + "="*50)
        print("Abu Chess AI - Main Menu")
        print("="*50)
        print("1. New Game (Human vs Abu)")
        print("2. New Game (Abu vs Abu)")
        print("3. Load Game")
        print("4. Train Model")
        print("5. Generate Training Data (Stockfish)")
        print("6. Quit")
        print("="*50)
        
        return input("Enter your choice (1-6): ").strip()
    
    def show_move_history(self, moves: List[str]):
        """
        Display move history
        
        Args:
            moves: List of moves in UCI format
        """
        print("\n=== Move History ===")
        if not moves:
            print("No moves yet")
            return
        
        # Display in pairs (white, black)
        for i in range(0, len(moves), 2):
            move_num = i // 2 + 1
            white_move = moves[i]
            black_move = moves[i + 1] if i + 1 < len(moves) else ""
            
            print(f"{move_num}. {white_move:8} {black_move}")
    
    def prompt_difficulty(self) -> str:
        """
        Prompt user to select difficulty level
        
        Returns:
            Difficulty level ('beginner', 'intermediate', 'advanced')
        """
        print("\nSelect difficulty level:")
        print("1. Beginner")
        print("2. Intermediate")
        print("3. Advanced")
        
        choice = input("Enter your choice (1-3): ").strip()
        
        difficulty_map = {
            '1': 'beginner',
            '2': 'intermediate',
            '3': 'advanced'
        }
        
        return difficulty_map.get(choice, 'intermediate')
    
    def prompt_yes_no(self, question: str) -> bool:
        """
        Prompt user with yes/no question
        
        Args:
            question: Question to ask
        
        Returns:
            True for yes, False for no
        """
        response = input(f"\n{question} (y/n): ").strip().lower()
        return response in ['y', 'yes']
    
    def clear_screen(self):
        """Clear the terminal screen"""
        import os
        os.system('cls' if os.name == 'nt' else 'clear')
