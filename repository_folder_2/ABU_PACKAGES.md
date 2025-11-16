# AbuLang Package System

## Overview

AbuLang now has an official package system with specialized modules for different purposes!

## Current AbuLang Imports (via `libra`)

### Standard Python Modules
```abu
libra math          # Math functions (also: maths)
libra stat          # Statistics module
libra osys          # Operating system functions
libra req           # HTTP requests (also: web)
libra jsons         # JSON handling
libra path          # Path operations
```

### Visual/UI Engines
```abu
libra DISPLAY       # Pygame (shortcut: ds)
libra UI            # Tkinter (shortcut: ui)
libra arrow         # Turtle graphics (shortcut: ar)
```

## New Abu Packages

### 1. AbuSmart - System Utilities

**Purpose**: System operations like time, shutdown, webcam, notifications, etc.

**Usage**:
```abu
libra AbuSmart

# Time and date
show smart.time()           # Current time
show smart.date()           # Current date
show smart.datetime()       # Full datetime
show smart.timestamp()      # Unix timestamp

# System control
smart.shutdown(5)           # Shutdown in 5 minutes
smart.cancel_shutdown()     # Cancel shutdown
smart.restart(0)            # Restart immediately

# System info
smart.system_info()         # Display system information
smart.battery()             # Battery status (requires psutil)

# Utilities
smart.webcam()              # Open webcam
smart.open_url("https://github.com")  # Open URL in browser
smart.notify("Title", "Message")      # System notification

# Clipboard
smart.clipboard_copy("text")  # Copy to clipboard
text = smart.clipboard_paste()  # Paste from clipboard
```

**Dependencies** (optional):
- `psutil` - For battery info
- `pyperclip` - For clipboard operations
- `win10toast` - For Windows notifications

---

### 2. AbuINSTALL - Package Manager

**Purpose**: Install Python packages (pip wrapper)

**Usage**:
```abu
libra AbuINSTALL

# Install packages
from AbuINSTALL install requests
installer.install("numpy")
installer.upgrade("pip")

# Check packages
installer.check("requests")     # Check if installed
installer.show("requests")      # Show package info
installer.list_installed()      # List all packages

# Uninstall
installer.uninstall("package")

# Requirements files
installer.requirements("requirements.txt")  # Install from file
installer.freeze("requirements.txt")        # Save current packages

# Search (opens browser)
installer.search("numpy")
```

---

### 3. AbuFILES - File System

**Purpose**: File operations and specialized .abu file types

**File Types**:
- `.abu` - AbuLang Script
- `.abudata` - Data File (JSON)
- `.abuconfig` - Config File (JSON)
- `.abulog` - Log File
- `.abusave` - Save File (Pickle)
- `.abudb` - Database File
- `.abutest` - Test File

**Usage**:
```abu
libra AbuFILES

# Basic file operations
files.create("myfile", ".abu", "show 'hello'")
content = files.read("myfile.abu")
files.write("myfile.abu", "new content")
files.append("myfile.abu", "more content")
files.delete("myfile.abu")

# Check files
files.exists("myfile.abu")
files.list_files(".", ".abu")
files.info("myfile.abu")

# Specialized file types
data = {"name": "Abu", "score": 100}
files.save_data("mydata", data)      # Creates mydata.abudata
loaded = files.load_data("mydata")   # Loads from mydata.abudata

config = {"theme": "dark", "lang": "en"}
files.save_config("settings", config)
cfg = files.load_config("settings")

files.log("mylog", "Application started")  # Appends to mylog.abulog
logs = files.read_log("mylog")

game_state = {"level": 5, "health": 100}
files.save_game("savefile", game_state)    # Creates savefile.abusave
state = files.load_game("savefile")

# List all file types
files.list_types()
```

---

### 4. AbuChess - Neural Chess AI

**Purpose**: Neural network-based chess AI (integrates with 06.AI)

**Features**:
- Neural network chess engine
- Multiple difficulty levels (Beginner, Intermediate, Advanced)
- Beautiful web interface
- Command-line interface
- Training with Stockfish
- Move analysis and evaluation

**Usage**:
```abu
libra AbuChess

# Show information
chess.info()                  # Display features and usage
chess.status()                # Check installation status

# Play chess
chess.AIweb()                 # Launch web interface (recommended!)
chess.play()                  # Launch CLI game
chess.train()                 # Train the AI

# Direct imports
from AbuChess import play     # Import play function directly
from AbuChess import AIweb    # Import web function directly
```

**Web Interface** (Recommended):
```abu
libra AbuChess
chess.AIweb()                 # Opens http://localhost:5000 in browser
```

Features:
- 🎨 Beautiful, modern interface
- ♟️ Interactive drag-and-drop chess board
- 📊 Real-time move analysis
- 🎮 Multiple difficulty levels
- 📱 Responsive design

**CLI Interface**:
```abu
libra AbuChess
chess.play()                  # Launch terminal game
```

Features:
- Play against Abu in terminal
- Move history
- Move analysis
- UCI and algebraic notation support

**Training**:
```abu
libra AbuChess
chess.train()                 # Launch training wizard
```

- Generate training data with Stockfish
- Train neural network
- Save trained models
- Monitor training progress

---

## How to Use

### Import a package:
```abu
libra AbuSmart
libra AbuINSTALL
libra AbuFILES
libra AbuChess
```

### Use shortcuts:
```abu
libra AbuSmart
show smart.time()    # Use 'smart' shortcut

libra AbuFILES
files.create("test.abu")  # Use 'files' shortcut

libra AbuINSTALL
installer.check("requests")  # Use 'installer' shortcut
# OR
from AbuINSTALL install requests  # Direct install
```

---

## Examples

### Example 1: System Info Logger
```abu
libra AbuSmart
libra AbuFILES

# Log system info
files.log("system", "=== System Check ===")
files.log("system", "Time: " + smart.time())
files.log("system", "Date: " + smart.date())

smart.system_info()
```

### Example 2: Data Persistence
```abu
libra AbuFILES

# Save game progress
progress = {
    "level": 10,
    "score": 5000,
    "items": ["sword", "shield", "potion"]
}

files.save_data("progress", progress)
show "Game saved!"

# Load later
loaded = files.load_data("progress")
show "Level: " + str(loaded["level"])
```

### Example 3: Package Management
```abu
libra AbuINSTALL

# Check and install if needed
if not installer.check("requests"):
    show "Installing requests..."
    installer.install("requests")

show "Ready to use requests!"
```

### Example 4: Play Chess
```abu
libra AbuChess

# Show info
chess.info()

# Play in browser (recommended!)
chess.AIweb()

# Or play in terminal
# chess.play()

# Or train Abu
# chess.train()
```

### Example 5: Direct Import
```abu
# Import play function directly
from AbuChess import play
play()

# Or import web function
from AbuChess import AIweb
AIweb()
```

---

## Testing

Run the test file:
```bash
python essentials/python/cli.py test_abu_packages.abu
```

---

## Next Steps

**For AbuChess**, tell me what features you want:
- What kind of chess game? (2-player, vs AI, puzzles?)
- What notation? (algebraic, coordinate?)
- GUI or text-based?
- Difficulty levels?
- Special features?

**For other packages**, let me know if you want:
- More file types?
- More system utilities?
- More package management features?

---

## File Structure

```
essentials/python/abu_packages/
├── __init__.py
├── AbuSmart.py      # System utilities
├── AbuINSTALL.py    # Package manager
├── AbuFILES.py      # File system
└── AbuChess.py      # Chess engine (placeholder)
```

All packages are automatically available when you use `libra`!
