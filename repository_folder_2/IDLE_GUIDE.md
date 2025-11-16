# AbuLang in Python IDLE 3.13.5 - Quick Guide

A quick reference for using AbuLang in Python IDLE.

---

## Setup (Do This Once)

Open Python IDLE 3.13.5 and run:

```python
>>> from abulang import enable_abulang_mode
>>> enable_abulang_mode()
[AbuLang] Enabled! You can now use AbuLang syntax in Python IDLE
[AbuLang] Available commands: show, ask, libra
```

---

## Basic Commands

### Output with `show()`

```python
>>> show("Hello, World!")
Hello, World!

>>> show("The answer is:", 42)
The answer is: 42

>>> x = 10
>>> show(x)
10

>>> show("x =", x, "and x * 2 =", x * 2)
x = 10 and x * 2 = 20
```

### Input with `ask()`

```python
>>> name = ask("What's your name? ")
What's your name? Abu
>>> show("Hello,", name)
Hello, Abu

>>> age = ask("How old are you? ")
How old are you? 25
>>> age = int(age)
>>> show("Next year you'll be", age + 1)
Next year you'll be 26
```

### Import Libraries with `libra()`

```python
>>> libra("math")
>>> show(math.sqrt(16))
4.0
>>> show(math.pi)
3.141592653589793

>>> libra("random")
>>> show(random.randint(1, 10))
7

>>> libra("datetime")
>>> show(datetime.datetime.now())
2024-11-15 10:30:45.123456
```

---

## Working with Variables

```python
>>> x = 10
>>> y = 5
>>> show("x + y =", x + y)
x + y = 15

>>> name = "Abu"
>>> age = 25
>>> show(name, "is", age, "years old")
Abu is 25 years old

>>> numbers = [1, 2, 3, 4, 5]
>>> show("Numbers:", numbers)
Numbers: [1, 2, 3, 4, 5]
>>> show("Sum:", sum(numbers))
Sum: 15
```

---

## Using AbuLang Packages

### AbuSmart - System Utilities

```python
>>> libra("AbuSmart")
>>> show(smart.time())
10:30:45
>>> show(smart.date())
2024-11-15
>>> smart.system_info()
=== System Information ===
OS: Windows
...
```

### AbuFILES - File Operations

```python
>>> libra("AbuFILES")
>>> data = {"name": "Abu", "score": 100}
>>> files.save_data("mydata", data)
>>> loaded = files.load_data("mydata")
>>> show(loaded)
{'name': 'Abu', 'score': 100}
```

### AbuINSTALL - Package Manager

```python
>>> libra("AbuINSTALL")
>>> installer.check("requests")
True
>>> installer.list_installed()
[List of installed packages...]
```

### AbuChess - Chess AI

```python
>>> libra("AbuChess")
>>> chess.info()
[Chess AI information...]
>>> chess.AIweb()  # Opens web interface
```

---

## Math Operations

```python
>>> libra("math")

>>> show(math.sqrt(25))
5.0

>>> show(math.pow(2, 10))
1024.0

>>> show(math.sin(math.pi / 2))
1.0

>>> show(math.factorial(5))
120

>>> libra("stat")
>>> numbers = [10, 20, 30, 40, 50]
>>> show(stat.mean(numbers))
30.0
>>> show(stat.median(numbers))
30.0
```

---

## Complete Example Session

```python
>>> from abulang import enable_abulang_mode
>>> enable_abulang_mode()
[AbuLang] Enabled! You can now use AbuLang syntax in Python IDLE
[AbuLang] Available commands: show, ask, libra

>>> show("=== Calculator ===")
=== Calculator ===

>>> x = ask("Enter first number: ")
Enter first number: 10
>>> y = ask("Enter second number: ")
Enter second number: 5

>>> x = int(x)
>>> y = int(y)

>>> show("Sum:", x + y)
Sum: 15
>>> show("Difference:", x - y)
Difference: 5
>>> show("Product:", x * y)
Product: 50
>>> show("Division:", x / y)
Division: 2.0

>>> libra("math")
>>> show("Square root of x:", math.sqrt(x))
Square root of x: 3.1622776601683795
```

---

## Running .abu Files from IDLE

```python
>>> from abulang import run_file
>>> run_file("example.abu")
[Output from example.abu...]

>>> from abulang import run
>>> run('''
... show "Hello from AbuLang!"
... x = 10
... show "x * 2 = " + str(x * 2)
... ''')
Hello from AbuLang!
x * 2 = 20
```

---

## Important Syntax Differences

### In .abu Files (No Parentheses)
```abu
show "Hello"
ask "Name: "
libra math
```

### In Python IDLE (With Parentheses)
```python
show("Hello")
ask("Name: ")
libra("math")
```

**Why?** In IDLE, you're in a Python environment where function calls require parentheses. The `.abu` file syntax is processed by the AbuLang interpreter which allows the simplified syntax.

---

## Common Patterns

### Loop and Display

```python
>>> for i in range(5):
...     show("Count:", i)
... 
Count: 0
Count: 1
Count: 2
Count: 3
Count: 4
```

### Conditional Logic

```python
>>> score = 85
>>> if score >= 90:
...     show("Grade: A")
... elif score >= 80:
...     show("Grade: B")
... else:
...     show("Grade: C")
... 
Grade: B
```

### Working with Lists

```python
>>> fruits = ["apple", "banana", "orange"]
>>> for fruit in fruits:
...     show("I like", fruit)
... 
I like apple
I like banana
I like orange
```

### Using Dictionaries

```python
>>> person = {"name": "Abu", "age": 25, "city": "New York"}
>>> show("Name:", person["name"])
Name: Abu
>>> show("Age:", person["age"])
Age: 25
```

---

## Tips for IDLE Users

1. **Always use parentheses** for `show()`, `ask()`, and `libra()`
2. **Enable AbuLang mode once** at the start of your session
3. **Use Tab for autocomplete** - IDLE will show available methods
4. **Press Alt+P** to recall previous commands
5. **Use Ctrl+C** to interrupt long-running code
6. **Save your work** - Use File > Save to save your IDLE session

---

## Troubleshooting

### "NameError: name 'show' is not defined"

**Solution:** You forgot to enable AbuLang mode:
```python
>>> from abulang import enable_abulang_mode
>>> enable_abulang_mode()
```

### "SyntaxError: invalid syntax"

**Solution:** You're using .abu syntax in IDLE. Add parentheses:
```python
# Wrong in IDLE:
show "Hello"

# Correct in IDLE:
show("Hello")
```

### "ModuleNotFoundError: No module named 'abulang'"

**Solution:** Install AbuLang first:
```bash
pip install abulang
```

Then restart IDLE.

---

## Quick Reference Card

| Command | Example | Description |
|---------|---------|-------------|
| `show()` | `show("Hello")` | Display output |
| `ask()` | `name = ask("Name? ")` | Get user input |
| `libra()` | `libra("math")` | Import library |
| `enable_abulang_mode()` | `enable_abulang_mode()` | Enable AbuLang in IDLE |
| `run()` | `run('show "Hi"')` | Run AbuLang code |
| `run_file()` | `run_file("test.abu")` | Run .abu file |

---

## Next Steps

1. **Try the examples** above in IDLE
2. **Create .abu files** for more complex programs
3. **Explore packages** like AbuChess and AbuSmart
4. **Read the full guide**: `INSTALLATION_GUIDE.md`

---

**Happy coding in IDLE with AbuLang!** 🚀

*For more information, see INSTALLATION_GUIDE.md*
