# AbuLang V3 - Games Created! 🎮

## Three New Games

I've created three games showcasing different graphics libraries in AbuLang:

### 1. 🎲 3D Rotating Cube (Pygame) - `game_3d_cube.abu`
**Features:**
- 3D wireframe cube that rotates in real-time
- Manual rotation with arrow keys
- Auto-rotation mode (toggle with SPACE)
- Q/E keys for Z-axis rotation
- R to reset rotation
- Uses pygame (DISPLAY/ds alias)
- Demonstrates 3D projection and rotation matrices

**Controls:**
- Arrow Keys: Manual rotation
- Q/E: Rotate on Z-axis
- SPACE: Toggle auto-rotate
- R: Reset

### 2. 🍪 Cookie Clicker (Tkinter) - `game_tkinter_clicker.abu`
**Features:**
- Idle/clicker game mechanics
- Click the cookie to earn cookies
- Buy auto-clickers (earn cookies per second)
- Buy multipliers (earn more per click)
- Upgrade costs increase exponentially
- Beautiful GUI with colors and emojis
- Uses tkinter (UI/ui alias)

**Gameplay:**
- Click the big cookie button
- Earn cookies
- Buy upgrades to automate
- Build your cookie empire!

### 3. 🐢 Turtle Race (Turtle Graphics) - `game_turtle_race.abu`
**Features:**
- 6 colorful racing turtles
- Random movement for each turtle
- Finish line with checkered pattern
- Winner announcement with confetti
- Press SPACE to start
- Press R to reset and race again
- Uses turtle graphics (arrow/ar alias)

**Controls:**
- SPACE: Start race
- R: Reset race
- Watch the turtles race to the finish!

## How to Run

### Using CLI:
```bash
python essentials/python/cli.py game_3d_cube.abu
python essentials/python/cli.py game_tkinter_clicker.abu
python essentials/python/cli.py game_turtle_race.abu
```

### Using REPL:
```bash
python essentials/python/repl.py
```
Then type:
```abulang
libra DISPLAY
# ... game code ...
```

## Technical Details

### Libraries Used:
- **Pygame (DISPLAY/ds)**: 3D graphics, game loop, event handling
- **Tkinter (UI/ui)**: GUI widgets, buttons, labels, frames
- **Turtle (arrow/ar)**: Vector graphics, animations, simple drawing

### AbuLang Features Demonstrated:
- ✅ Auto-import aliases (ds, ui, ar)
- ✅ libra command for imports
- ✅ show command for output
- ✅ Function definitions
- ✅ Event handling
- ✅ Loops and conditionals
- ✅ Math operations
- ✅ GUI creation

## Notes

The games demonstrate AbuLang's capability to work with different Python graphics libraries using friendly aliases. Each game showcases a different style of programming:

- **3D Cube**: Mathematical/computational (3D transformations)
- **Cookie Clicker**: GUI/event-driven (buttons, callbacks)
- **Turtle Race**: Animation/graphics (drawing, movement)

## Status

✅ All three games created
✅ Different graphics libraries showcased
✅ AbuLang V3 aliases used throughout
✅ Ready to play!

---

**Enjoy the games!** 🎮🍪🐢
