# AbuLang Quick Start Guide

## Running AbuLang Files

```bash
python cli.py example.abu
```

## Kiro Shortcut Setup

To add a keyboard shortcut for running AbuLang files in Kiro:

### Option 1: Command Palette
1. Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on Mac)
2. Type "Preferences: Open Keyboard Shortcuts"
3. Search for "Run Task"
4. Add a custom keybinding (e.g., `Ctrl+Alt+A`)

### Option 2: tasks.json
Create `.vscode/tasks.json`:

```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Run AbuLang",
      "type": "shell",
      "command": "python",
      "args": ["cli.py", "${file}"],
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

Then press `Ctrl+Shift+B` to run the current .abu file.

### Option 3: keybindings.json
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

## Quick Examples

### Hello World
```abu
show "Hello, World!"
```

### Variables and Math
```abu
x = 10
y = 5
show "Sum: " + str(x + y)
```

### Using Libraries
```abu
libra math
result = math.sqrt(16)
show result
```

### Functions
```abu
def greet(name):
    return "Hello, " + name

show greet("Abu")
```

### Loops
```abu
for i in range(5):
    show i
```

### AbuLang Packages
```abu
# System utilities
libra AbuSmart
show smart.time()

# File operations
libra AbuFILES
files.save_data("data", {"key": "value"})

# Chess AI
libra AbuChess
chess.AIweb()  # Launch web interface
```

## File Structure

```
AbuLang/
├── cli.py              # Main CLI runner
├── example.abu         # Simple example
├── essentials/
│   └── python/
│       ├── runner.py   # AbuLang interpreter
│       ├── abu_core.py # Core language
│       └── abu_packages/
│           ├── AbuSmart.py
│           ├── AbuFILES.py
│           ├── AbuINSTALL.py
│           └── AbuChess.py
└── 06.AI/              # Chess AI engine
```

## Cleanup

To remove all test files, run:
```bash
cleanup_tests.bat
```

## Documentation

- `ABU_PACKAGES.md` - Package documentation
- `ABUCHESS_INTEGRATION.md` - Chess AI guide
- `ABULANG_V3_COMPLETE.md` - Complete language reference

## Support

For issues or questions, check the documentation files or create an issue.

---

**Happy coding with AbuLang!** 🚀
