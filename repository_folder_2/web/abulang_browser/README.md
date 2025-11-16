# BrowserIOAdapter - Task 11 Implementation

## Overview

The BrowserIOAdapter is a Python module that redirects I/O operations in AbuLang to work seamlessly in a browser environment using Pyodide. It replaces Python's standard `print()` and `input()` functions with browser-compatible alternatives that integrate with the web UI.

## Requirements Addressed

- **5.1**: Input handling through browser dialog
- **5.2**: Output capture for display in results panel
- **5.3**: Integration with AbuLang's `show` command
- **5.4**: Integration with AbuLang's `ask` command

## Architecture

### Components

1. **BrowserIOAdapter**: Main adapter class that manages I/O redirection
2. **BrowserOutputStream**: Custom output stream that captures stdout/stderr to a buffer
3. **BrowserAbuRunner**: Modified AbuLang interpreter that uses the I/O adapter

### How It Works

```
┌─────────────────────────────────────────────────────────┐
│                  AbuLang Code                           │
│  show "Hello"  →  print("Hello")                        │
│  ask "Name?"   →  input("Name?")                        │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│              BrowserIOAdapter                           │
│  • Intercepts print() → BrowserOutputStream             │
│  • Intercepts input() → JavaScript InputManager         │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│              Browser Interface                          │
│  • Output → Results Panel                               │
│  • Input  → Modal Dialog                                │
└─────────────────────────────────────────────────────────┘
```

## API Reference

### BrowserIOAdapter

```python
class BrowserIOAdapter:
    """Adapter that redirects Python I/O to browser interface"""
    
    def __init__(self):
        """Initialize the adapter"""
        
    def activate(self):
        """Activate I/O redirection"""
        
    def deactivate(self):
        """Deactivate I/O redirection and restore original I/O"""
        
    def get_output(self) -> str:
        """Get all captured output as a string"""
        
    def clear_output(self):
        """Clear the output buffer"""
```

### Convenience Functions

```python
# Get or create global adapter instance
adapter = get_global_adapter()

# Activate browser I/O
activate_browser_io()

# Deactivate browser I/O
deactivate_browser_io()

# Get captured output
output = get_captured_output()

# Clear output buffer
clear_captured_output()
```

## Integration with RuntimeBridge

The BrowserIOAdapter is automatically integrated into the RuntimeBridge when AbuLang is initialized:

```javascript
// In runtime-bridge.js
async initializeAbuLang() {
    // Load BrowserIOAdapter
    await pyodide.runPythonAsync(`
        # BrowserIOAdapter code...
        _io_adapter = BrowserIOAdapter()
        _abu_runner = BrowserAbuRunner(_io_adapter)
    `);
    
    // Override Python's input() with JavaScript function
    pyodide.globals.set('__browser_input__', async (prompt) => {
        return await this.inputManager.showInputDialog(prompt);
    });
}
```

## Usage Examples

### Example 1: Simple Output

```python
# AbuLang code
show "Hello, World!"
show "This is captured by BrowserIOAdapter"

# Output appears in browser results panel
```

### Example 2: User Input

```python
# AbuLang code
name = ask "What is your name?"
show "Hello, " + name + "!"

# Input dialog appears in browser
# User enters name
# Greeting appears in results panel
```

### Example 3: Multiple I/O Operations

```python
# AbuLang code
show "Welcome to the calculator!"
num1 = ask "Enter first number:"
num2 = ask "Enter second number:"
result = int(num1) + int(num2)
show "Result: " + str(result)

# Multiple dialogs and outputs work seamlessly
```

## Testing

A comprehensive test suite is provided in `test-browser-io-adapter.html`:

### Test Cases

1. **Test 1**: Show command output capture
2. **Test 2**: Ask command input dialog
3. **Test 3**: Multiple show and ask commands
4. **Test 4**: Show with expressions
5. **Test 5**: Full integration test

### Running Tests

1. Open `test-browser-io-adapter.html` in a browser
2. Click "Run Test" buttons for each test
3. Interact with input dialogs when prompted
4. Verify output in results panels

## Implementation Details

### Output Capture

The adapter creates a custom `BrowserOutputStream` that implements Python's stream interface:

```python
class BrowserOutputStream(io.StringIO):
    def __init__(self, buffer):
        super().__init__()
        self.buffer = buffer
        
    def write(self, text):
        if text:
            self.buffer.append(text)
        return len(text)
```

This stream is assigned to `sys.stdout` and `sys.stderr`, capturing all print statements.

### Input Handling

The adapter provides a placeholder for `input()` that is overridden by JavaScript:

```python
def _browser_input_placeholder(self, prompt=''):
    raise RuntimeError("Browser input not initialized")
```

JavaScript replaces this with an async function that shows the input dialog:

```javascript
builtins.input = browser_input  // Async function from JavaScript
```

### Integration with AbuRunner

The `BrowserAbuRunner` class is initialized with the I/O adapter:

```python
class BrowserAbuRunner:
    def __init__(self, io_adapter=None):
        self.io_adapter = io_adapter or _io_adapter
        self.io_adapter.activate()  # Activate on initialization
```

## Benefits

1. **Seamless Integration**: AbuLang code works without modification
2. **Browser-Native**: Uses browser UI elements (modal dialogs)
3. **Async Support**: Handles async input operations correctly
4. **Error Handling**: Graceful handling of cancelled inputs
5. **Testable**: Comprehensive test suite included

## Future Enhancements

1. **File I/O**: Add support for file operations using browser storage
2. **Streaming Output**: Real-time output streaming for long-running code
3. **Input Validation**: Built-in validation for input dialogs
4. **Multiple Input Types**: Support for different input types (number, password, etc.)
5. **Output Formatting**: Rich text formatting in output panel

## Files

- `browser_io_adapter.py`: Main adapter implementation
- `__init__.py`: Package initialization and exports
- `README.md`: This documentation
- `../test-browser-io-adapter.html`: Test suite

## Dependencies

- Python 3.x (via Pyodide)
- JavaScript InputManager (from `lib/input-manager.js`)
- JavaScript OutputCapture (from `app.js`)
- RuntimeBridge (from `lib/runtime-bridge.js`)

## Status

✅ **Task 11 Complete**

All sub-tasks implemented:
- ✅ Build adapter class that replaces Python's print() with output capture
- ✅ Build adapter that replaces input() with input dialog
- ✅ Integrate adapter into AbuRunner initialization
- ✅ Test show and ask commands in browser environment
