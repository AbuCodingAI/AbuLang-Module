# AbuLang v3.0.0 - New Imports & Usage Guide

## Installation

```bash
pip install abulang
```

## How to Use AbuLang

### 1. Run AbuLang Files

```bash
abulang myprogram.abu
```

### 2. Use in Python

```python
from abulang import run, run_file

# Run code directly
run('show "Hello, World!"')

# Run from file
run_file("myprogram.abu")
```

### 3. Launch IDLE Shell (Interactive)

```bash
python -c "from abulang import idle; idle()"
```

Or in Python:
```python
from abulang import idle
idle()
```

---

## New Imports for Casual Users

### Standard Python Libraries (via `libra`)

```abu
libra math              # Math functions
libra stat              # Statistics
libra random            # Random numbers
libra os                # Operating system
libra json              # JSON handling
libra requests          # HTTP requests
```

### Visual/UI Engines

```abu
libra UI                # Tkinter (GUI)
libra DISPLAY           # Pygame (graphics)
libra arrow             # Turtle graphics
```

### AbuLang Built-in Packages

#### **AbuSmart** - System Utilities
```abu
libra AbuSmart

smart.time()            # Current time
smart.date()            # Current date
smart.datetime()        # Full datetime
smart.system_info()     # System information
smart.webcam()          # Open webcam
smart.open_url(url)     # Open URL in browser
smart.notify(title, msg) # System notification
smart.shutdown(minutes) # Shutdown computer
smart.restart(minutes)  # Restart computer
```

#### **AbuFILES** - File Operations
```abu
libra AbuFILES

files.save_data(name, data)     # Save as JSON
files.load_data(name)           # Load JSON
files.save_config(name, config) # Save config
files.load_config(name)         # Load config
files.log(name, message)        # Write to log
files.read_log(name)            # Read log
files.save_game(name, state)    # Save game state
files.load_game(name)           # Load game state
files.create(name, type)        # Create file
files.read(name)                # Read file
files.write(name, content)      # Write file
files.append(name, content)     # Append to file
files.delete(name)              # Delete file
files.exists(name)              # Check if exists
files.list_files(dir, ext)      # List files
files.info(name)                # Get file info
```

#### **AbuINSTALL** - Package Manager
```abu
libra AbuINSTALL

installer.install(package)      # Install package
installer.uninstall(package)    # Uninstall package
installer.upgrade(package)      # Upgrade package
installer.check(package)        # Check if installed
installer.show(package)         # Show package info
installer.list_installed()      # List all packages
installer.search(query)         # Search packages
installer.requirements(file)    # Install from file
installer.freeze(file)          # Save requirements
```

#### **AbuChess** - Chess AI
```abu
libra AbuChess

chess.AIweb()           # Launch web interface
chess.play()            # Launch CLI game
chess.train()           # Train the AI
chess.info()            # Show information
chess.status()          # Check installation
```

---

## Complete Example Programs

### Example 1: Hello World
```abu
show "Hello, World!"
```

### Example 2: Using Math
```abu
libra math

x = 16
result = math.sqrt(x)
show "Square root of " + str(x) + " is " + str(result)
```

### Example 3: Random Choice
```abu
libra random

options is ["Python", "AbuLang", "JavaScript"]
choice = random.choice(options)
show "Random choice: " + choice
```

### Example 4: File Operations
```abu
libra AbuFILES

data is {"name": "Abu", "version": 3.0}
files.save_data("mydata", data)

loaded = files.load_data("mydata")
show loaded
```

### Example 5: System Info
```abu
libra AbuSmart

show "Current time: " + smart.time()
show "Current date: " + smart.date()
smart.system_info()
```

### Example 6: Chess Game
```abu
libra AbuChess

chess.AIweb()  # Opens browser with chess interface
```

### Example 7: Interactive Shell
```abu
libra random

show "Welcome to AbuLang!"
show "Type commands below:"

libra random
numbers is [1, 2, 3, 4, 5]
show "Random number: " + str(random.choice(numbers))
```

---

## File Types Supported

AbuLang can work with multiple file formats:

| Extension | Type | Usage |
|-----------|------|-------|
| `.abu` | AbuLang Script | Main program files |
| `.abudata` | Data File (JSON) | Store data |
| `.abuconfig` | Config File | Store settings |
| `.abulog` | Log File | Store logs |
| `.abusave` | Save File | Store game state |
| `.abudb` | Database | Store database |
| `.abutest` | Test File | Test scripts |

---

## Quick Reference

### Variables
```abu
x = 10
name is "Abu"
```

### Functions
```abu
def greet(name):
    return "Hello, " + name

show greet("World")
```

### Loops
```abu
for i in range(5):
    show i

while x > 0:
    show x
    x = x - 1
```

### Conditionals
```abu
if x > 5:
    show "Big"
elif x > 0:
    show "Small"
else:
    show "Zero"
```

### Lists
```abu
items is [1, 2, 3, 4, 5]
show items[0]
show len(items)
```

### Dictionaries
```abu
person is {"name": "Abu", "age": 3}
show person["name"]
```

---

## Keyboard Shortcuts (IDLE)

| Shortcut | Action |
|----------|--------|
| `Ctrl+N` | New file |
| `Ctrl+O` | Open file |
| `Ctrl+S` | Save file |
| `F5` | Run code |
| `Ctrl+Z` | Undo |
| `Ctrl+Y` | Redo |

---

## Common Tasks

### Task 1: Save and Load Data
```abu
libra AbuFILES

# Save
data is {"score": 100, "level": 5}
files.save_data("progress", data)

# Load
progress = files.load_data("progress")
show progress
```

### Task 2: Get Random Item
```abu
libra random

items is ["apple", "banana", "orange"]
picked = random.choice(items)
show "You picked: " + picked
```

### Task 3: Get System Time
```abu
libra AbuSmart

show "Time: " + smart.time()
show "Date: " + smart.date()
```

### Task 4: Install a Package
```abu
libra AbuINSTALL

installer.install("requests")
installer.check("requests")
```

### Task 5: Play Chess
```abu
libra AbuChess

chess.AIweb()  # Opens in browser
```

---

## Troubleshooting

### "Module not found"
Make sure you have the package installed:
```bash
pip install abulang
```

### "Command not recognized"
Make sure AbuLang is in your PATH:
```bash
pip install --upgrade abulang
```

### "Import error"
Try importing from the module directly:
```python
from abulang import run
run('show "test"')
```

---

## Next Steps

1. **Create your first program**: `myprogram.abu`
2. **Run it**: `abulang myprogram.abu`
3. **Use IDLE**: `python -c "from abulang import idle; idle()"`
4. **Explore packages**: Try `libra AbuSmart`, `libra AbuFILES`, etc.
5. **Build something**: Games, tools, utilities!

---

## Resources

- **GitHub**: https://github.com/AbuCodingAI/abulang
- **PyPI**: https://pypi.org/project/abulang/
- **Documentation**: See README.md

---

**Happy coding with AbuLang!** 🚀
