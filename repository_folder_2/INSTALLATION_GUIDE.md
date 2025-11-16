# AbuLang Installation & Usage Guide 🚀

A complete guide to installing, configuring, and using AbuLang - the friendly, Pythonic programming language for beginners and creative coders.

---

## Table of Contents

1. [System Requirements](#system-requirements)
2. [Installation Methods](#installation-methods)
3. [Verifying Installation](#verifying-installation)
4. [Getting Started](#getting-started)
5. [Running AbuLang Programs](#running-abulang-programs)
6. [Language Basics](#language-basics)
7. [Built-in Packages](#built-in-packages)
8. [Advanced Features](#advanced-features)
9. [IDE Integration](#ide-integration)
10. [Troubleshooting](#troubleshooting)
11. [Uninstallation](#uninstallation)

---

## System Requirements

### Minimum Requirements
- **Python**: 3.8 or higher
- **Operating System**: Windows, macOS, or Linux
- **Disk Space**: ~50MB
- **RAM**: 512MB minimum (1GB recommended)

### Check Your Python Version
```bash
python --version
```

If Python is not installed or version is below 3.8, download from [python.org](https://www.python.org/downloads/)

---

## Installation Methods

### Method 1: Install from PyPI (Recommended)

This is the easiest and recommended method for most users.

```bash
pip install abulang
```

**For Python 3 specifically:**
```bash
pip3 install abulang
```

**Upgrade to latest version:**
```bash
pip install --upgrade abulang
```

### Method 2: Install from Source

For developers or those who want the latest development version:

```bash
# Clone the repository
git clone https://github.com/AbuCodingAI/abulang.git
cd abulang

# Install in development mode
pip install -e .
```

### Method 3: Install with Optional Features

**With Chess AI support:**
```bash
pip install abulang[chess]
```

**With development tools:**
```bash
pip install abulang[dev]
```

**With everything:**
```bash
pip install abulang[chess,dev]
```

---

## Verifying Installation

### Check if AbuLang is installed:

```bash
abulang --version
```

### Test with a simple program:

Create a file called `test.abu`:
```abu
show "AbuLang is working!"
```

Run it:
```bash
abulang test.abu
```

You should see: `AbuLang is working!`

---

## Getting Started

### Your First AbuLang Program

Create a file called `hello.abu`:

```abu
show "Hello, World!"
```

Run it:
```bash
abulang hello.abu
```

### Interactive REPL

Start the interactive shell:
```bash
abulang
```

Try some commands:
```abu
>>> show "Hello!"
Hello!
>>> x = 10
>>> show x
10
>>> libra math
>>> show math.sqrt(16)
4.0
```

Exit with `Ctrl+C` or `Ctrl+D`

---

## Running AbuLang Programs

### From Command Line

```bash
# Run a .abu file
abulang myprogram.abu

# Run with Python directly
python -m abulang myprogram.abu
```

### From Python Code

```python
from abulang import run, run_file

# Run AbuLang code directly
run('show "Hello from Python!"')

# Run an AbuLang file
run_file("myprogram.abu")
```

### In Python IDLE

```python
from abulang import enable_abulang_mode

# Enable AbuLang syntax
enable_abulang_mode()

# Now you can use AbuLang commands (with parentheses in IDLE)
show("Hello!")
name = ask("What's your name? ")
show("Hello, " + name)

# Note: In IDLE, you must use parentheses: show("text")
# The no-parentheses syntax (show "text") only works in .abu files
```

### IDLE Quick Start Guide

**Step 1:** Open Python IDLE 3.13.5

**Step 2:** Enable AbuLang mode:
```python
>>> from abulang import enable_abulang_mode
>>> enable_abulang_mode()
[AbuLang] Enabled! You can now use AbuLang syntax in Python IDLE
[AbuLang] Available commands: show, ask, libra
```

**Step 3:** Use AbuLang commands (with parentheses):
```python
>>> show("Hello, World!")
Hello, World!

>>> x = 10
>>> y = 5
>>> show("Sum:", x + y)
Sum: 15

>>> name = ask("What's your name? ")
What's your name? Abu
>>> show("Hello,", name)
Hello, Abu

>>> libra("math")
>>> show(math.sqrt(16))
4.0
```

**Important Syntax Note:**

| In .abu Files | In Python IDLE |
|---------------|----------------|
| `show "text"` | `show("text")` |
| `ask "prompt"` | `ask("prompt")` |
| `libra math` | `libra("math")` |

In IDLE, you're running in a Python environment, so you must use Python's function call syntax with parentheses. The no-parentheses syntax only works in `.abu` files that are processed by the AbuLang interpreter.

---

## Language Basics

### 1. Output and Input

```abu
# Display output
show "Hello, World!"
show "The answer is: " + str(42)

# Get user input
name = ask "What's your name? "
show "Hello, " + name
```

### 2. Variables

```abu
# Numbers
x = 10
y = 3.14
z = -5

# Strings
name = "Abu"
message = "Hello, World!"

# Lists
numbers = [1, 2, 3, 4, 5]
names = ["Alice", "Bob", "Charlie"]

# Dictionaries
person = {"name": "Abu", "age": 25}
```

### 3. Math Operations

```abu
x = 10
y = 5

show x + y    # Addition: 15
show x - y    # Subtraction: 5
show x * y    # Multiplication: 50
show x / y    # Division: 2.0
show x ** y   # Power: 100000
show x % y    # Modulo: 0
```

### 4. Conditionals

```abu
score = 85

if score >= 90:
    show "Grade: A"
elif score >= 80:
    show "Grade: B"
elif score >= 70:
    show "Grade: C"
else:
    show "Grade: F"
```

### 5. Loops

```abu
# For loop
for i in range(5):
    show i

# While loop
count = 0
while count < 5:
    show count
    count = count + 1

# Loop through list
fruits = ["apple", "banana", "orange"]
for fruit in fruits:
    show fruit
```

### 6. Functions

```abu
# Define a function
def greet(name):
    return "Hello, " + name + "!"

# Call the function
message = greet("Abu")
show message

# Function with multiple parameters
def add(a, b):
    return a + b

result = add(10, 5)
show result
```

### 7. Importing Libraries

```abu
# Import Python standard library
libra math
show math.sqrt(16)
show math.pi

# Import with alias
libra stat
numbers = [1, 2, 3, 4, 5]
show stat.mean(numbers)

# Multiple imports
libra random
libra datetime
```

---

## Built-in Packages

AbuLang comes with specialized packages for common tasks.

### 1. AbuSmart - System Utilities

```abu
libra AbuSmart

# Time and date
show smart.time()           # Current time
show smart.date()           # Current date
show smart.datetime()       # Full datetime

# System control
smart.shutdown(5)           # Shutdown in 5 minutes
smart.cancel_shutdown()     # Cancel shutdown
smart.restart(0)            # Restart immediately

# System info
smart.system_info()         # Display system information
smart.battery()             # Battery status

# Utilities
smart.webcam()              # Open webcam
smart.open_url("https://github.com")  # Open URL
smart.notify("Title", "Message")      # Notification

# Clipboard
smart.clipboard_copy("text")
text = smart.clipboard_paste()
```

### 2. AbuFILES - File Operations

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

# Data files (.abudata)
data = {"name": "Abu", "score": 100}
files.save_data("mydata", data)
loaded = files.load_data("mydata")

# Config files (.abuconfig)
config = {"theme": "dark", "lang": "en"}
files.save_config("settings", config)
cfg = files.load_config("settings")

# Log files (.abulog)
files.log("mylog", "Application started")
logs = files.read_log("mylog")

# Save files (.abusave)
game_state = {"level": 5, "health": 100}
files.save_game("savefile", game_state)
state = files.load_game("savefile")
```

### 3. AbuINSTALL - Package Manager

```abu
libra AbuINSTALL

# Install packages
installer.install("requests")
installer.upgrade("pip")

# Check packages
installer.check("requests")
installer.show("requests")
installer.list_installed()

# Uninstall
installer.uninstall("package")

# Requirements files
installer.requirements("requirements.txt")
installer.freeze("requirements.txt")

# Search (opens browser)
installer.search("numpy")
```

### 4. AbuChess - Neural Chess AI

```abu
libra AbuChess

# Show information
chess.info()
chess.status()

# Play chess
chess.AIweb()    # Web interface (recommended!)
chess.play()     # CLI game
chess.train()    # Train the AI
```

**Web Interface** (opens in browser):
- Beautiful, modern interface
- Interactive drag-and-drop board
- Real-time move analysis
- Multiple difficulty levels

---

## Advanced Features

### Multi-Format Blocks

AbuLang supports embedding YAML, JSON, CSV, and other formats:

```abu
# YAML block
switch(yaml)
database:
  host: localhost
  port: 5432
  username: admin
save_as(config.yaml)

# Read it back
line = get_line 2 config.yaml
show line

# JSON block
switch(json)
{
  "name": "Abu",
  "version": "3.0"
}
save_as(data.json)
```

### GUI Programming

**With Tkinter:**
```abu
libra UI

window = ui.Tk()
window.title("My App")

btn = ui.Button(window, text="Click Me")
btn.pack(spacex=10, spacey=5)

window.mainloop()
```

**With Pygame:**
```abu
libra DISPLAY

ds.init()
screen = ds.display.set_mode((800, 600))
ds.display.set_caption("My Game")

running = True
while running:
    for event in ds.event.get():
        if event.type == ds.QUIT:
            running = False
    
    screen.fill((0, 0, 0))
    ds.display.flip()

ds.quit()
```

### Working with Data

```abu
libra stat
libra jsons

# Statistics
data = [10, 20, 30, 40, 50]
show "Mean: " + str(stat.mean(data))
show "Median: " + str(stat.median(data))
show "Stdev: " + str(stat.stdev(data))

# JSON handling
person = {"name": "Abu", "age": 25}
json_str = jsons.dumps(person)
show json_str

parsed = jsons.loads(json_str)
show parsed["name"]
```

---

## IDE Integration

### Visual Studio Code

1. Install the Python extension
2. Create `.vscode/tasks.json`:

```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Run AbuLang",
      "type": "shell",
      "command": "abulang",
      "args": ["${file}"],
      "group": {
        "kind": "build",
        "isDefault": true
      },
      "presentation": {
        "reveal": "always",
        "panel": "new"
      }
    }
  ]
}
```

3. Press `Ctrl+Shift+B` to run current .abu file

### Keyboard Shortcut

Create `.vscode/keybindings.json`:

```json
[
  {
    "key": "ctrl+alt+a",
    "command": "workbench.action.tasks.runTask",
    "args": "Run AbuLang",
    "when": "editorTextFocus && resourceExtname == '.abu'"
  }
]
```

Now press `Ctrl+Alt+A` to run AbuLang files!

### Kiro IDE

If using Kiro, AbuLang is already integrated. Just open any `.abu` file and run it.

---

## Troubleshooting

### Problem: "abulang: command not found"

**Solution:**
```bash
# Try with python -m
python -m abulang myfile.abu

# Or add Python Scripts to PATH
# Windows: Add C:\Python3X\Scripts to PATH
# Linux/Mac: Add ~/.local/bin to PATH
```

### Problem: "ModuleNotFoundError: No module named 'abulang'"

**Solution:**
```bash
# Reinstall
pip uninstall abulang
pip install abulang

# Or install from source
pip install -e .
```

### Problem: "ImportError: Could not import AbuRunner"

**Solution:**
```bash
# Make sure you're in the right directory
cd /path/to/abulang

# Reinstall with dependencies
pip install -e . --force-reinstall
```

### Problem: Chess AI not working

**Solution:**
```bash
# Install chess dependencies
pip install abulang[chess]

# Or manually
pip install python-chess torch flask flask-cors
```

### Problem: Permission denied on Linux/Mac

**Solution:**
```bash
# Use --user flag
pip install --user abulang

# Or use sudo (not recommended)
sudo pip install abulang
```

### Problem: Slow installation

**Solution:**
```bash
# Use a faster mirror
pip install abulang -i https://pypi.tuna.tsinghua.edu.cn/simple

# Or upgrade pip first
pip install --upgrade pip
```

---

## Uninstallation

### Remove AbuLang

```bash
pip uninstall abulang
```

### Remove all dependencies

```bash
pip uninstall abulang PyYAML psutil pyperclip
```

### Remove development installation

```bash
cd /path/to/abulang
pip uninstall abulang
```

---

## Example Programs

### 1. Guessing Game

```abu
libra random

secret = random.randint(1, 100)
guesses = 0

show "I'm thinking of a number between 1 and 100"

while True:
    guess = ask "Your guess: "
    guess = int(guess)
    guesses = guesses + 1
    
    if guess < secret:
        show "Too low!"
    elif guess > secret:
        show "Too high!"
    else:
        show "Correct! You got it in " + str(guesses) + " guesses!"
        break
```

### 2. Todo List

```abu
libra AbuFILES

todos = []

while True:
    show "\n=== Todo List ==="
    show "1. Add task"
    show "2. View tasks"
    show "3. Save and exit"
    
    choice = ask "Choose: "
    
    if choice == "1":
        task = ask "Enter task: "
        todos.append(task)
        show "Task added!"
    
    elif choice == "2":
        if len(todos) == 0:
            show "No tasks yet!"
        else:
            for i in range(len(todos)):
                show str(i + 1) + ". " + todos[i]
    
    elif choice == "3":
        files.save_data("todos", {"tasks": todos})
        show "Saved! Goodbye!"
        break
```

### 3. System Monitor

```abu
libra AbuSmart
libra AbuFILES

show "=== System Monitor ==="
show ""

# Display system info
smart.system_info()

# Log to file
files.log("monitor", "=== System Check ===")
files.log("monitor", "Time: " + smart.time())
files.log("monitor", "Date: " + smart.date())

# Battery status
battery = smart.battery()
if battery:
    show "Battery: " + str(battery) + "%"

show "\nLog saved to monitor.abulog"
```

### 4. Web Scraper

```abu
libra req
libra jsons

url = "https://api.github.com/users/github"
response = req.get(url)

if response.status_code == 200:
    data = response.json()
    show "Name: " + data["name"]
    show "Bio: " + data["bio"]
    show "Followers: " + str(data["followers"])
else:
    show "Error: " + str(response.status_code)
```

---

## Additional Resources

### Documentation
- [Quick Start Guide](ABULANG_QUICKSTART.md)
- [Complete Language Reference](ABULANG_V3_COMPLETE.md)
- [Package Documentation](ABU_PACKAGES.md)
- [Chess AI Guide](ABUCHESS_INTEGRATION.md)

### Community
- **GitHub**: [github.com/AbuCodingAI/abulang](https://github.com/AbuCodingAI/abulang)
- **Issues**: Report bugs and request features
- **Discussions**: Ask questions and share projects

### Support
- **Email**: abu.shariffaiml@gmail.com
- **GitHub Issues**: For bug reports
- **GitHub Discussions**: For questions and help

---

## Quick Reference Card

### Basic Commands
```abu
show "text"              # Print output
ask "prompt"             # Get input
libra module             # Import library
```

### Variables
```abu
x = 10                   # Number
name = "Abu"             # String
items = [1, 2, 3]        # List
data = {"key": "value"}  # Dictionary
```

### Control Flow
```abu
if condition:            # If statement
    # code
elif condition:          # Else if
    # code
else:                    # Else
    # code

for i in range(10):      # For loop
    # code

while condition:         # While loop
    # code
```

### Functions
```abu
def function_name(param):
    return value
```

### Packages
```abu
libra AbuSmart           # System utilities
libra AbuFILES           # File operations
libra AbuINSTALL         # Package manager
libra AbuChess           # Chess AI
```

---

## Tips and Best Practices

1. **Use meaningful variable names**: `user_age` instead of `x`
2. **Comment your code**: Use `#` for comments
3. **Test incrementally**: Run your code frequently while developing
4. **Use the REPL**: Great for testing small snippets
5. **Read error messages**: They usually tell you what's wrong
6. **Start simple**: Begin with basic programs and build up
7. **Use packages**: Don't reinvent the wheel
8. **Save often**: Use AbuFILES to save your data
9. **Explore examples**: Learn from the example programs
10. **Have fun**: Programming should be enjoyable!

---

## What's Next?

Now that you have AbuLang installed, try:

1. **Run the examples**: Start with `example.abu`
2. **Build a project**: Create something you're interested in
3. **Explore packages**: Try AbuChess or AbuSmart
4. **Join the community**: Share your projects on GitHub
5. **Contribute**: Help improve AbuLang

---

**Happy coding with AbuLang!** 🚀

*Made with ❤️ by Abu*
