# AbuChess Integration Guide

## Overview

AbuChess is now fully integrated into AbuLang! It connects to the neural network chess AI in the `06.AI` directory, allowing you to play chess, train the AI, and use the web interface directly from AbuLang.

## Features

✅ **Neural Network Chess Engine** - Deep learning-based chess AI  
✅ **Web Interface** - Beautiful browser-based chess board  
✅ **CLI Interface** - Play in terminal  
✅ **Training System** - Train Abu with Stockfish  
✅ **Multiple Difficulty Levels** - Beginner, Intermediate, Advanced  
✅ **Move Analysis** - See Abu's top moves and evaluations  

## Quick Start

### 1. Play in Browser (Recommended) 🌐

```abu
libra AbuChess
chess.AIweb()
```

This will:
- Start the web server at `http://localhost:5000`
- Automatically open your browser
- Show a beautiful interactive chess board

**Or use direct import:**
```abu
from AbuChess import AIweb
AIweb()
```

### 2. Play in Terminal 💻

```abu
libra AbuChess
chess.play()
```

This launches the CLI interface where you can:
- Play against Abu
- View move history
- Get move analysis
- Use UCI or algebraic notation

**Or use direct import:**
```abu
from AbuChess import play
play()
```

### 3. Train Abu 🎓

```abu
libra AbuChess
chess.train()
```

This opens the training wizard where you can:
- Generate training data with Stockfish
- Train the neural network
- Save trained models
- Monitor training progress

## Usage Examples

### Example 1: Quick Game
```abu
libra AbuChess
chess.AIweb()  # Opens browser, ready to play!
```

### Example 2: Check Status
```abu
libra AbuChess
chess.status()  # Check if everything is installed
chess.info()    # Show features and usage
```

### Example 3: Direct Import
```abu
# Import and play immediately
from AbuChess import play
play()
```

### Example 4: Web Interface
```abu
# Import and launch web interface
from AbuChess import AIweb
AIweb()
```

## Available Methods

### Main Methods

| Method | Description |
|--------|-------------|
| `chess.AIweb()` | Launch web interface (opens browser) |
| `chess.play()` | Launch CLI game |
| `chess.train()` | Launch training wizard |
| `chess.info()` | Show information and features |
| `chess.status()` | Check installation status |

### Aliases

| Alias | Same As |
|-------|---------|
| `chess.web()` | `chess.AIweb()` |
| `chess.new_game()` | `chess.play()` |

## Direct Imports

You can import functions directly without using `libra`:

```abu
from AbuChess import play      # Import play function
from AbuChess import AIweb     # Import web function
from AbuChess import train     # Import train function
from AbuChess import info      # Import info function
from AbuChess import status    # Import status function
```

## Web Interface Features

When you run `chess.AIweb()`, you get:

- 🎨 **Beautiful UI** - Modern, clean interface
- ♟️ **Interactive Board** - Drag and drop pieces
- 📊 **Move Analysis** - See Abu's thinking
- 🎮 **Difficulty Levels** - Choose your challenge
- 📱 **Responsive** - Works on any screen size
- ⚡ **Real-time** - Instant move feedback

## CLI Interface Features

When you run `chess.play()`, you can:

- Enter moves in UCI format (`e2e4`) or algebraic (`e4`)
- Type `history` to see move history
- Type `analysis` to see Abu's move analysis
- Type `quit` to exit
- Choose difficulty level
- Play as White or Black

## Training Abu

To train Abu to play better:

1. Run `chess.train()`
2. Select "Generate with Stockfish"
3. Configure parameters:
   - **Stockfish path** (or press Enter for default)
   - **Depth** (10-15 recommended)
   - **Number of games** (100+ recommended)
   - **Epochs** (10-20 recommended)
4. Wait for training to complete
5. Save the trained model

## Installation Check

To verify everything is working:

```abu
libra AbuChess
chess.status()
```

This will show:
- ✓ Chess AI directory found
- ✓ Required files present
- ✓ Abu package installed
- ✓ Trained models available

## Troubleshooting

### "06.AI directory not found"
- Make sure the `06.AI` directory exists in your project
- Check that you're running from the correct directory

### "No trained models"
- This is normal for first-time use
- Run `chess.train()` to create a trained model
- Or play with the untrained model (it will make random moves)

### Web server won't start
- Check if port 5000 is already in use
- Try closing other applications using that port
- Check the terminal for error messages

### Can't find Stockfish
- Install Stockfish from [stockfishchess.org](https://stockfishchess.org/download/)
- Or provide the full path when prompted during training

## Architecture

AbuChess integrates with the `06.AI` directory structure:

```
06.AI/
├── main.py              # CLI interface
├── web_server.py        # Web interface
├── abu/                 # Chess engine package
│   ├── chess_engine/    # Board and move validation
│   ├── neural_network/  # Neural network model
│   ├── ai_player/       # AI player logic
│   └── training/        # Training system
├── models/              # Saved trained models
└── templates/           # Web interface HTML
```

## Technical Details

### Neural Network
- **Architecture**: CNN with residual blocks
- **Input**: 8x8x14 board tensor
- **Output**: Move probabilities + position evaluation
- **Training**: Supervised learning with Stockfish data

### Difficulty Levels
- **Beginner**: Makes occasional random moves
- **Intermediate**: Picks from top 3 moves
- **Advanced**: Always picks best move

### Move Format
- **UCI**: `e2e4`, `g1f3`, `e7e8q` (promotion)
- **Algebraic**: `e4`, `Nf3`, `e8=Q` (promotion)

## Performance

- **Web Interface**: Runs on Flask (localhost:5000)
- **Neural Network**: Uses PyTorch (GPU if available)
- **Move Time**: ~0.1-1 second depending on difficulty
- **Training Time**: Varies (10 games ≈ 5-10 minutes)

## Future Enhancements

Potential features to add:
- Opening book integration
- Endgame tablebase support
- Online multiplayer
- Puzzle mode
- ELO rating system
- Game analysis tools
- PGN import/export

## Credits

- **Chess Engine**: Based on `python-chess` library
- **Neural Network**: Inspired by AlphaZero architecture
- **Training Data**: Generated with Stockfish
- **Web Interface**: Built with Flask and JavaScript

## Support

For issues or questions:
1. Check `chess.status()` for installation issues
2. Run `chess.info()` for usage help
3. See `06.AI/README.md` for detailed documentation
4. Check `06.AI/WEB_INTERFACE.md` for web interface guide

---

**Ready to play?** Just run:
```abu
libra AbuChess
chess.AIweb()
```

Enjoy playing against Abu! 🎮♟️
