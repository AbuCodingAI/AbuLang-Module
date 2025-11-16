# AbuLang PyPI - Internal Modules & Packages

For users who installed: `pip install abulang`

## Internal Modules List

### Core Modules

| Module | Import | Purpose |
|--------|--------|---------|
| **AbuRunner** | `from essentials.python.runner import AbuRunner` | Main interpreter |
| **AbuLang** | `from essentials.python.abu_core import AbuLang` | Core language definitions |

### Built-in Packages

| Package | Import | Purpose |
|---------|--------|---------|
| **AbuSmart** | `from essentials.python.abu_packages import AbuSmart` | System utilities |
| **AbuFILES** | `from essentials.python.abu_packages import AbuFILES` | File operations |
| **AbuINSTALL** | `from essentials.python.abu_packages import AbuINSTALL` | Package manager |
| **AbuChess** | `from essentials.python.abu_packages import AbuChess` | Chess AI |

---

## Quick Import Reference

### Main API (Recommended)
```python
from abulang import run, run_file
```

### Core Modules
```python
from essentials.python.runner import AbuRunner
from essentials.python.abu_core import AbuLang
```

### Built-in Packages
```python
from essentials.python.abu_packages import AbuSmart
from essentials.python.abu_packages import AbuFILES
from essentials.python.abu_packages import AbuINSTALL
from essentials.python.abu_packages import AbuChess
```

---

## Usage Examples

### Run AbuLang Code
```python
from abulang import run

run('show "Hello, World!"')
```

### Run AbuLang File
```python
from abulang import run_file

run_file("myprogram.abu")
```

### Create Custom Runner
```python
from essentials.python.runner import AbuRunner

runner = AbuRunner()
runner.execute_line('show "Hello"')
```

### Use Built-in Packages
```python
from essentials.python.abu_packages import AbuSmart

smart = AbuSmart()
print(smart.time())
```

---

## Module Details

### AbuRunner
- **Methods**: `execute_line()`, `run()`, `eval_expr()`
- **Properties**: `context`, `constants`, `lang`, `gui_aliases`

### AbuLang
- **Methods**: `translate()`, `explain()`
- **Properties**: `commands`, `lookup`

### GUIAliasManager
- **Methods**: `translate_syntax_enhancements()`, `get_auto_aliases()`, `get_all_help_categories()`, `get_help_category()`

### AbuSmart
- **Methods**: `time()`, `date()`, `datetime()`, `system_info()`, `webcam()`, `open_url()`, `notify()`, `shutdown()`, `restart()`

### AbuFILES
- **Methods**: `save_data()`, `load_data()`, `save_config()`, `load_config()`, `log()`, `read_log()`, `save_game()`, `load_game()`, `create()`, `read()`, `write()`, `append()`, `delete()`, `exists()`, `list_files()`, `info()`

### AbuINSTALL
- **Methods**: `install()`, `uninstall()`, `upgrade()`, `check()`, `show()`, `list_installed()`, `search()`, `requirements()`, `freeze()`

### AbuChess
- **Methods**: `AIweb()`, `play()`, `train()`, `info()`, `status()`

---

## Command Line Usage

```bash
# Run AbuLang file
abulang myprogram.abu

# Run code directly
python -c "from abulang import run; run('show \"Hello\"')"

# Interactive Python
python
>>> from abulang import run
>>> run('show "Hello"')
```

---

## Summary

**For casual users:**
```python
from abulang import run
run('show "Hello"')
```

**For developers:**
```python
from essentials.python.runner import AbuRunner
runner = AbuRunner()
runner.execute_line('show "Hello"')
```

**For package access:**
```python
from essentials.python.abu_packages import AbuSmart, AbuFILES, AbuINSTALL, AbuChess
```

---

**Happy coding with AbuLang!** 🚀
