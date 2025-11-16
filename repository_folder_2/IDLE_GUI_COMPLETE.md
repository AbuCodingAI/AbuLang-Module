# AbuLang IDLE GUI - Complete Python IDLE Clone

## Features ✨

### **Editor**
- ✅ Code editor with syntax highlighting
- ✅ Line numbers
- ✅ Undo/Redo (Ctrl+Z, Ctrl+Y)
- ✅ Cut/Copy/Paste
- ✅ File open/save/save as
- ✅ Auto-save detection

### **Shell**
- ✅ Interactive shell with `>>>` prompt
- ✅ Execute commands line by line
- ✅ Command history
- ✅ Clear shell output
- ✅ Error handling

### **Menu Bar**
- ✅ File: New, Open, Save, Save As, Exit
- ✅ Edit: Undo, Redo, Cut, Copy, Paste
- ✅ Run: Run Code, Clear Shell
- ✅ Help: About

### **Keyboard Shortcuts**
- `Ctrl+N` - New file
- `Ctrl+O` - Open file
- `Ctrl+S` - Save file
- `F5` - Run code
- `Ctrl+Z` - Undo
- `Ctrl+Y` - Redo

## File Structure

```
Module/
├── __init__.py          # Package initialization
├── runner.py            # Main interpreter
├── idle_gui.py          # IDLE GUI (NEW!)
├── abu_core.py          # Core language
└── gui_aliases.py       # Syntax enhancements

main.py                  # Entry point
```

## Usage

### Launch IDLE GUI
```bash
python main.py
```

### Run .abu File
```bash
python main.py myprogram.abu
```

## IDLE GUI Features

### **Editor Panel**
- Write AbuLang code
- Line numbers on left
- Syntax highlighting
- Undo/Redo support

### **Shell Panel**
- Execute commands interactively
- See output in real-time
- Type commands after `>>>`
- Press Enter to execute

### **File Operations**
- Create new files
- Open existing .abu files
- Save with Ctrl+S
- Save As with different names

### **Run Code**
- Press F5 to run all code in editor
- Output appears in shell
- Errors are displayed

## Example Session

```
1. Launch: python main.py
2. Type in editor:
   show "Hello, World!"
   x = 10
   show x
3. Press F5 to run
4. See output in shell:
   Hello, World!
   10
5. Or type in shell:
   >>> show "Interactive!"
   Interactive!
```

## GUI Layout

```
┌─────────────────────────────────────┐
│ File  Edit  Run  Help               │
├─────────────────────────────────────┤
│ │ 1 │ show "Hello"                  │
│ │ 2 │ x = 10                        │
│ │ 3 │ show x                        │
├─────────────────────────────────────┤
│ AbuLang IDLE v3.0.0                 │
│ >>> show "Interactive!"             │
│ Interactive!                        │
│ >>> exit                            │
│ >>> │                               │
├─────────────────────────────────────┤
│ Ready                               │
└─────────────────────────────────────┘
```

## Exactly Like Python IDLE

✅ Split editor/shell layout
✅ File menu with open/save
✅ Edit menu with undo/redo
✅ Run menu to execute code
✅ Line numbers in editor
✅ Interactive shell with prompt
✅ Keyboard shortcuts
✅ Status bar
✅ Error handling
✅ Command history

## Next Steps

1. Run: `python main.py`
2. Write code in editor
3. Press F5 to run
4. Or type commands in shell
5. Save files with Ctrl+S

---

**AbuLang now has a full Python IDLE clone!** 🚀
