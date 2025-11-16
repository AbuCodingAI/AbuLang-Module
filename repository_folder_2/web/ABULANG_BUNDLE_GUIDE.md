# AbuLang Browser Bundle Guide

This guide explains how the AbuLang interpreter has been bundled for use in web browsers via Pyodide.

## Overview

The AbuLang browser bundle is a self-contained Python package that can be loaded into Pyodide (Python compiled to WebAssembly) and executed entirely in the browser without any backend server.

## Package Structure

```
web/abulang_browser/
├── __init__.py          # Package initialization, exports, and convenience functions
├── runner.py            # Main AbuLang interpreter (browser-adapted)
├── abu_core.py          # Core language definitions and command registry
├── gui_aliases.py       # Syntax enhancement manager
├── setup.py             # Package setup configuration for Pyodide
├── test_imports.py      # Local Python test suite
└── README.md            # Package documentation
```

## Key Features

### 1. Browser-Compatible Module System

The `runner.py` has been adapted to work in the browser environment:

- **Available Modules**: math, statistics, json, random, re, datetime, collections, itertools, functools
- **Unavailable Modules**: os, sys, subprocess, socket, threading, tkinter, pygame (security/compatibility)
- **Smart Error Messages**: When users try to import unavailable modules, they get helpful feedback

### 2. Standalone Package

The package is completely self-contained:

- No external dependencies beyond Python standard library
- No file I/O operations (browser security)
- All code runs in-memory

### 3. Simple API

```python
# Import and use
from abulang_browser import run

# Execute AbuLang code
run('show "Hello, World!"')
```

## Loading in Pyodide

### Method 1: Direct File Loading (Recommended)

This method loads the package files directly from your web server:

```javascript
async function loadAbuLang(pyodide) {
    // Create package directory
    await pyodide.runPythonAsync(`
import sys
import os
os.makedirs('/abulang_browser', exist_ok=True)
    `);
    
    // Load each module file
    const modules = ['__init__.py', 'runner.py', 'abu_core.py', 'gui_aliases.py'];
    
    for (const module of modules) {
        const response = await fetch(`abulang_browser/${module}`);
        const content = await response.text();
        
        await pyodide.runPythonAsync(`
with open('/abulang_browser/${module}', 'w') as f:
    f.write('''${content.replace(/'/g, "\\'")}''')
        `);
    }
    
    // Add to Python path
    await pyodide.runPythonAsync(`sys.path.insert(0, '/')`);
}

// Usage
let pyodide = await loadPyodide();
await loadAbuLang(pyodide);

// Now you can use AbuLang
await pyodide.runPythonAsync(`
from abulang_browser import run
run('show "Hello from AbuLang!"')
`);
```

### Method 2: Using micropip (Future Enhancement)

Once the package is published to PyPI or a custom package index:

```javascript
let pyodide = await loadPyodide();
await pyodide.loadPackage("micropip");
await pyodide.runPythonAsync(`
    import micropip
    await micropip.install('abulang-browser')
`);
```

## Usage Examples

### Basic Execution

```python
from abulang_browser import run

# Simple output
run('show "Hello, World!"')

# Math operations
run('''
x = 10
y = 20
show x + y
''')
```

### Using the Runner Directly

```python
from abulang_browser import AbuRunner

# Create runner instance
runner = AbuRunner()

# Execute code
code = """
show "Welcome to AbuLang!"
libra math
show math.pi
show math.sqrt(16)
"""

runner.run(code)

# Access variables from context
print(runner.context['math'])  # Access imported modules
```

### Capturing Output

```python
from abulang_browser import AbuRunner
import io
import sys

runner = AbuRunner()

# Redirect stdout to capture output
captured = io.StringIO()
sys.stdout = captured

runner.run('show "Hello!"')

# Restore stdout
sys.stdout = sys.__stdout__

# Get captured output
output = captured.getvalue()
print(f"Captured: {output}")
```

### Resetting State

```python
from abulang_browser import reset

# Reset the global runner instance
# This clears all variables and imported modules
reset()
```

## Testing

### Local Python Testing

Run the test suite locally to verify the package structure:

```bash
cd web/abulang_browser
python test_imports.py
```

This runs 5 comprehensive tests:
1. Import verification
2. Runner instance creation
3. Simple code execution
4. Variable assignment
5. Library import (libra command)

### Browser Testing

Open `web/test-abulang-bundle.html` in a web browser to test the package in a real Pyodide environment. This test suite includes:

1. **Pyodide Initialization**: Verifies Pyodide loads correctly
2. **Package Loading**: Loads all AbuLang modules into Pyodide
3. **Import Tests**: Verifies all modules can be imported
4. **Runner Creation**: Tests creating AbuRunner instances
5. **Code Execution**: Tests running AbuLang code
6. **Variable Assignment**: Tests variable storage and retrieval
7. **Library Import**: Tests the `libra` command
8. **Help System**: Tests the `help` command

## Browser Compatibility

The package works in any browser that supports:

- **WebAssembly**: All modern browsers (Chrome 90+, Firefox 88+, Safari 14+, Edge 90+)
- **ES6+ JavaScript**: For the loading code
- **Fetch API**: For loading module files

## Differences from Desktop Version

| Feature | Desktop | Browser |
|---------|---------|---------|
| File I/O | ✓ Supported | ✗ Not available |
| OS Module | ✓ Available | ✗ Restricted |
| GUI (tkinter) | ✓ Available | ✗ Not available |
| Math/Statistics | ✓ Available | ✓ Available |
| JSON/YAML | ✓ Available | ✓ JSON only |
| Network (requests) | ✓ Available | ⚠️ Limited |
| Threading | ✓ Available | ✗ Not available |

## Performance Considerations

1. **Initial Load**: Pyodide takes 2-5 seconds to load initially
2. **Caching**: Pyodide is cached by the browser after first load
3. **Execution Speed**: ~50-70% of native Python speed
4. **Memory**: Runs in browser memory, limited by browser constraints

## Security

The browser bundle is secure by design:

1. **Sandboxed**: All code runs in WebAssembly sandbox
2. **No File Access**: Cannot access user's file system
3. **No Network**: Cannot make arbitrary network requests
4. **No System Calls**: Cannot execute system commands

## Integration with Web UI

The bundle is designed to integrate with the web playground UI:

```javascript
// In your web app
class AbuLangPlayground {
    async init() {
        this.pyodide = await loadPyodide();
        await this.loadAbuLang();
    }
    
    async loadAbuLang() {
        // Load package (see Method 1 above)
    }
    
    async executeCode(code) {
        // Capture output
        const output = await this.pyodide.runPythonAsync(`
import io
import sys
from abulang_browser import AbuRunner

runner = AbuRunner()
captured = io.StringIO()
sys.stdout = captured

try:
    runner.run('''${code}''')
    sys.stdout = sys.__stdout__
    captured.getvalue()
except Exception as e:
    sys.stdout = sys.__stdout__
    str(e)
        `);
        
        return output;
    }
}
```

## Troubleshooting

### Import Errors

**Problem**: `ModuleNotFoundError: No module named 'abulang_browser'`

**Solution**: Ensure the package files are loaded and the path is set:
```python
import sys
sys.path.insert(0, '/')
```

### Module Not Available

**Problem**: `[libra] Module 'os' is not available in browser version`

**Solution**: This is expected. Use only browser-compatible modules (math, statistics, json, random, etc.)

### Syntax Errors

**Problem**: Code works in desktop Python but fails in browser

**Solution**: Check for:
- File I/O operations (not supported)
- OS-specific operations (not supported)
- GUI operations (not supported)

## Future Enhancements

1. **YAML Support**: Add PyYAML to Pyodide environment
2. **Package Publishing**: Publish to PyPI for easier installation
3. **Enhanced Error Messages**: Better error formatting for browser
4. **Debugging Tools**: Step-through debugger for browser
5. **Code Completion**: Autocomplete for AbuLang commands

## Version History

- **4.0.0** (Current): Initial browser bundle with Pyodide support
- **3.1**: Desktop version with IDLE GUI
- **3.0**: Major refactor with module system

## Support

For issues or questions:
- GitHub: https://github.com/AbuCodingAI/abulang
- Email: abu.shariffaiml@gmail.com

## License

MIT License - See LICENSE file for details
