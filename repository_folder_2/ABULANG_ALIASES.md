# AbuLang Library Aliases 📚

AbuLang provides convenient aliases for commonly used Python libraries, making your code more intuitive and readable!

## 🎨 Visual/UI Engine Aliases

### DISPLAY → pygame
```abulang
libra DISPLAY

# Now use DISPLAY instead of pygame
DISPLAY.init()
screen = DISPLAY.display.set_mode((800, 600))
DISPLAY.draw.rect(screen, (255, 0, 0), (10, 10, 50, 50))
```

**Why?** "DISPLAY" is more descriptive for visual/graphics operations!

### UI → tkinter
```abulang
libra UI

# Use UI for GUI applications
window = UI.Tk()
button = UI.Button(window, text="Click me!")
```

**Why?** "UI" is clearer than "tkinter" for user interface code!

### arrow → turtle
```abulang
libra arrow

# Use arrow for turtle graphics
arrow.forward(100)
arrow.right(90)
```

**Why?** "arrow" describes what the turtle cursor looks like!

## 📊 Data & Math Aliases

### stat → statistics
```abulang
libra stat

# Use stat for statistical operations
mean_value = stat.mean([1, 2, 3, 4, 5])
```

**Why?** Shorter and more convenient!

### maths → math
```abulang
libra maths

# Use maths for mathematical operations
result = maths.sqrt(16)
```

**Why?** Alternative spelling for international users!

## 🌐 Web & System Aliases

### web → requests
```abulang
libra web

# Use web for HTTP requests
response = web.get("https://api.example.com")
```

**Why?** "web" is more intuitive for web operations!

### req → requests
```abulang
libra req

# Shorter alias for requests
data = req.post(url, json=payload)
```

**Why?** Quick and convenient!

### osys → os
```abulang
libra osys

# Use osys for operating system operations
files = osys.listdir(".")
```

**Why?** More descriptive than just "os"!

### jsons → json
```abulang
libra jsons

# Use jsons for JSON operations
data = jsons.loads(json_string)
```

**Why?** Clearer that you're working with JSON!

### path → os.path
```abulang
libra path

# Use path for file path operations
full_path = path.join(directory, filename)
```

**Why?** Direct access to path operations!

## 🎮 Snake Game Example

The Snake game uses these aliases:

```abulang
# Import using AbuLang aliases
libra DISPLAY    # Instead of: libra pygame
libra random
libra time

# Use DISPLAY throughout the code
DISPLAY.init()
screen = DISPLAY.display.set_mode((800, 600))
DISPLAY.draw.rect(screen, color, rect)
DISPLAY.display.flip()
```

## 💡 Benefits of Using Aliases

1. **More Readable**: `DISPLAY` is clearer than `pygame` for graphics
2. **Intuitive**: Names describe what they do
3. **Consistent**: AbuLang style throughout your code
4. **Shorter**: Some aliases are more concise
5. **Flexible**: Use either the alias or original name

## 📝 How Aliases Work

When you use `libra DISPLAY`, AbuLang's runner automatically:
1. Maps `DISPLAY` to `pygame`
2. Imports the actual `pygame` module
3. Makes it available as both `DISPLAY` and `pygame`
4. Adds convenient shortcuts (like `ds` for DISPLAY)

## 🔍 Finding More Aliases

Check `runner.py` in the `_handle_libra()` method to see all available aliases:

```python
module_aliases = {
    "stat": "statistics",
    "maths": "math",
    "osys": "os",
    "req": "requests",
    "jsons": "json",
    "path": "os.path",
    "web": "requests",
    "DISPLAY": "pygame",
    "UI": "tkinter",
    "arrow": "turtle",
}
```

## ✨ Pro Tip

You can still use the original module names if you prefer:
```abulang
libra pygame    # Works fine!
libra DISPLAY   # Also works, more AbuLang style!
```

Both work, but using aliases makes your code more "AbuLang-ish"! 🚀
