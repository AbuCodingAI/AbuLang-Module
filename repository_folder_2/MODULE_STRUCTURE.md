# AbuLang Module Structure

## New Organization

```
AbuLang/
├── Module/                    # Main module folder
│   ├── __init__.py           # Package initialization
│   ├── runner.py             # Main interpreter
│   ├── idle.py               # Interactive shell
│   ├── abu_core.py           # Core language
│   └── gui_aliases.py        # Syntax enhancements
│
├── main.py                   # Entry point
├── setup.py                  # Package config
├── README.md                 # Documentation
├── LICENSE                   # MIT License
└── requirements.txt          # Dependencies
```

## Features

### 1. **Module-Based Structure**
Everything is organized in the `Module/` folder for clean separation.

### 2. **IDLE Shell** (Like Python)
Interactive shell with:
- `>>>` prompt
- Command history
- `exit` command
- `history` command
- `clear` command
- Error handling

### 3. **Same AbuLang Syntax**
- `show` - Display output
- `ask` - Get input
- `libra` - Import libraries
- `if/for/while` - Control flow
- `def` - Functions
- Math operations

## Usage

### Launch IDLE Shell
```bash
python main.py
```

Then type commands:
```
>>> show "Hello, World!"
Hello, World!
>>> x = 10
>>> show x
10
>>> libra math
[libra] imported math
>>> show math.sqrt(16)
4.0
>>> exit
```

### Run .abu File
```bash
python main.py myprogram.abu
```

### Use as Module
```python
from Module import run, idle

# Run code
run('show "Hello!"')

# Launch IDLE
idle()
```

## IDLE Commands

| Command | Action |
|---------|--------|
| `exit` | Exit IDLE |
| `history` | Show command history |
| `clear` | Clear screen |
| `help` | Show help |

## File Descriptions

| File | Purpose |
|------|---------|
| `Module/__init__.py` | Package exports |
| `Module/runner.py` | Main interpreter |
| `Module/idle.py` | Interactive shell |
| `Module/abu_core.py` | Language definitions |
| `Module/gui_aliases.py` | Syntax enhancements |
| `main.py` | Entry point |

## Example IDLE Session

```
============================================================
  AbuLang IDLE v3.0.0
  Interactive Shell
============================================================

Type 'help' for help, 'exit' to quit

>>> show "Welcome to AbuLang!"
Welcome to AbuLang!
>>> x = 5
>>> y = 10
>>> show x + y
15
>>> libra math
[libra] imported math
>>> show math.sqrt(25)
5.0
>>> def greet(name):
...     return "Hello, " + name
>>> show greet("Abu")
Hello, Abu
>>> history
  1. show "Welcome to AbuLang!"
  2. x = 5
  3. y = 10
  4. show x + y
  5. libra math
  6. show math.sqrt(25)
  7. def greet(name):
  8. return "Hello, " + name
  9. show greet("Abu")
 10. history
>>> exit

============================================================
  Thanks for using AbuLang!
============================================================
```

## Next Steps

1. ✅ Module structure created
2. ✅ IDLE shell implemented
3. ✅ Same AbuLang syntax
4. Test IDLE: `python main.py`
5. Run files: `python main.py example.abu`

---

**AbuLang now has an interactive IDLE shell!** 🚀
