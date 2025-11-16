# AbuLang Internal Modules - Developer Guide

## Module Structure

```
Module/
├── __init__.py          # Package initialization
├── runner.py            # Main interpreter (AbuRunner)
├── idle_gui.py          # IDLE GUI (AbuIDLEGUI)
├── abu_core.py          # Core language (AbuLang)
└── gui_aliases.py       # Syntax enhancements (GUIAliasManager)
```

---

## How to Import Internal Modules

### From Python

```python
# Import the runner
from Module.runner import AbuRunner

# Import IDLE GUI
from Module.idle_gui import AbuIDLEGUI

# Import core language
from Module.abu_core import AbuLang

# Import GUI aliases
from Module.gui_aliases import GUIAliasManager
```

### From AbuLang IDLE

You can't directly import these in IDLE (they're Python internals), but you can use them through the main API:

```python
from Module import run, run_file, idle

# Run code
run('show "Hello"')

# Run file
run_file("myprogram.abu")

# Launch IDLE
idle()
```

---

## Using Internal Modules Directly

### 1. AbuRunner - Main Interpreter

```python
from Module.runner import AbuRunner

# Create runner instance
runner = AbuRunner()

# Execute single line
runner.execute_line('show "Hello"')

# Run full program
code = '''
x = 10
show x
'''
runner.run(code)
```

### 2. AbuIDLEGUI - Interactive Shell

```python
from Module.idle_gui import AbuIDLEGUI
import tkinter as tk

# Create and run IDLE
root = tk.Tk()
idle = AbuIDLEGUI(root)
idle.run()
```

Or simpler:

```python
from Module.idle_gui import main
main()
```

### 3. AbuLang - Core Language

```python
from Module.abu_core import AbuLang

# Create language instance
lang = AbuLang()

# Get command info
print(lang.commands["show"])

# Explain command
print(lang.explain("show"))
```

### 4. GUIAliasManager - Syntax Enhancements

```python
from Module.gui_aliases import GUIAliasManager

# Create manager
manager = GUIAliasManager()

# Translate syntax
line = 'show "Hello"'
translated = manager.translate_syntax_enhancements(line)
print(translated)
```

---

## Complete Examples

### Example 1: Run AbuLang Code from Python

```python
from Module import run

# Simple code
run('show "Hello, World!"')

# With variables
run('''
x = 10
y = 20
show x + y
''')

# With functions
run('''
def greet(name):
    return "Hello, " + name

show greet("Abu")
''')
```

### Example 2: Create Custom Runner

```python
from Module.runner import AbuRunner

runner = AbuRunner()

# Add custom context
runner.context["custom_var"] = 42

# Execute code that uses custom context
runner.execute_line('show custom_var')
```

### Example 3: Launch IDLE Programmatically

```python
from Module.idle_gui import AbuIDLEGUI

# Create IDLE instance
idle = AbuIDLEGUI()

# Run it
idle.run()
```

### Example 4: Inspect Language Commands

```python
from Module.abu_core import AbuLang

lang = AbuLang()

# List all commands
for cmd, info in lang.commands.items():
    print(f"{cmd}: {info['desc']}")

# Get specific command
show_cmd = lang.commands["show"]
print(show_cmd)
```

### Example 5: Process AbuLang File

```python
from Module import run_file

# Run .abu file
run_file("myprogram.abu")
```

---

## Running from Command Line

### Run IDLE GUI
```bash
python -m Module.idle_gui
```

### Run AbuLang File
```bash
python -c "from Module import run_file; run_file('myprogram.abu')"
```

### Run Code Directly
```bash
python -c "from Module import run; run('show \"Hello\"')"
```

### Interactive Python with AbuLang
```bash
python
>>> from Module import run
>>> run('show "Hello"')
Hello
```

---

## Advanced Usage

### Custom AbuRunner with Extended Context

```python
from Module.runner import AbuRunner
import math

class CustomRunner(AbuRunner):
    def __init__(self):
        super().__init__()
        # Add custom functions
        self.context["custom_sqrt"] = math.sqrt
        self.context["PI"] = 3.14159

runner = CustomRunner()
runner.execute_line('show custom_sqrt(16)')
runner.execute_line('show PI')
```

### Capture Output

```python
from Module.runner import AbuRunner
import io
import sys

runner = AbuRunner()

# Redirect stdout
old_stdout = sys.stdout
sys.stdout = io.StringIO()

runner.execute_line('show "Hello"')

# Get output
output = sys.stdout.getvalue()
sys.stdout = old_stdout

print(f"Captured: {output}")
```

### Execute Multiple Commands

```python
from Module.runner import AbuRunner

runner = AbuRunner()

commands = [
    'x = 10',
    'y = 20',
    'show x + y',
    'libra math',
    'show math.sqrt(16)'
]

for cmd in commands:
    runner.execute_line(cmd)
```

---

## Module API Reference

### AbuRunner

```python
runner = AbuRunner()

# Methods
runner.execute_line(line)       # Execute single line
runner.run(code)                # Run full program
runner.eval_expr(expr)          # Evaluate expression

# Properties
runner.context                  # Variable context
runner.constants                # Constant variables
runner.lang                     # AbuLang instance
runner.gui_aliases              # GUIAliasManager instance
```

### AbuIDLEGUI

```python
idle = AbuIDLEGUI()

# Methods
idle.run()                      # Start IDLE
idle.execute_shell_command()    # Execute shell command
idle.run_code()                 # Run editor code
idle.print_shell(text)          # Print to shell
idle.open_file()                # Open file dialog
idle.save_file()                # Save file
idle.new_file()                 # Create new file

# Properties
idle.runner                     # AbuRunner instance
idle.editor                     # Text editor widget
idle.shell_output               # Shell output widget
idle.current_file               # Current file path
```

### AbuLang

```python
lang = AbuLang()

# Methods
lang.translate(word)            # Translate keyword
lang.explain(word)              # Explain command

# Properties
lang.commands                   # Command dictionary
lang.lookup                     # Command lookup table
```

### GUIAliasManager

```python
manager = GUIAliasManager()

# Methods
manager.translate_syntax_enhancements(line)  # Translate syntax
manager.get_auto_aliases(module)             # Get aliases
manager.get_all_help_categories()            # Get help categories
manager.get_help_category(category)          # Get category help
```

---

## Integration Examples

### Integrate with Flask Web App

```python
from flask import Flask, request, jsonify
from Module import run
import io
import sys

app = Flask(__name__)

@app.route('/execute', methods=['POST'])
def execute():
    code = request.json.get('code')
    
    # Capture output
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    
    try:
        run(code)
        output = sys.stdout.getvalue()
        sys.stdout = old_stdout
        return jsonify({"output": output})
    except Exception as e:
        sys.stdout = old_stdout
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run()
```

### Integrate with Discord Bot

```python
import discord
from Module import run
import io
import sys

@bot.command()
async def abulang(ctx, *, code):
    # Capture output
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    
    try:
        run(code)
        output = sys.stdout.getvalue()
        sys.stdout = old_stdout
        await ctx.send(f"```\n{output}\n```")
    except Exception as e:
        sys.stdout = old_stdout
        await ctx.send(f"Error: {e}")
```

---

## Troubleshooting

### "ModuleNotFoundError: No module named 'Module'"

Make sure you're in the correct directory:
```bash
cd /path/to/abulang
python
>>> from Module import run
```

### "Cannot import from Module"

Install AbuLang first:
```bash
pip install abulang
```

Then use:
```python
from abulang import run
```

### IDLE GUI won't start

Make sure tkinter is installed:
```bash
pip install tk
```

---

## Summary

| Task | Code |
|------|------|
| Run code | `from Module import run; run('show "x"')` |
| Run file | `from Module import run_file; run_file('file.abu')` |
| Launch IDLE | `from Module import idle; idle()` |
| Custom runner | `from Module.runner import AbuRunner; runner = AbuRunner()` |
| Get commands | `from Module.abu_core import AbuLang; lang = AbuLang()` |

---

**For casual users**: Use `from Module import run, idle`

**For developers**: Import specific modules as needed

**For integration**: Use AbuRunner directly in your applications

---

**Happy coding!** 🚀
