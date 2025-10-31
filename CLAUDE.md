# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python Tetris game implementation using Pygame. The project includes both a playable game and a basic FastAPI web server (unrelated to the game).

## Running the Project

### Setup Environment
```bash
# Create and activate virtual environment
python3 -m venv tetris_env
source tetris_env/bin/activate  # On macOS/Linux
# tetris_env\Scripts\activate  # On Windows

# Install dependencies
pip install -r requirements.txt
```

### Run the Tetris Game
```bash
python play.py
```

### Run the FastAPI Server (separate utility)
```bash
python main.py
# Or with uvicorn directly:
uvicorn main:app --reload
```

## Game Controls (from play.py)

- **Arrow Up**: Rotate brick
- **Arrow Down**: Fast drop
- **Arrow Left**: Move brick left
- **Arrow Right**: Move brick right
- **P**: Pause/Resume game (NEW FEATURE)
- **D**: Toggle debug message display
- **ESC**: Exit game

## Recent Updates

### Enhancements Made:
1. **Fixed syntax error**: Corrected `pyggame` to `pygame` typo
2. **Internationalization**: Converted all Chinese text to English
3. **Pause functionality**: Added complete pause/resume feature with P key
4. **UI improvements**: Added pause status display and game area overlay

## Architecture

### Core Files

- **[play.py](play.py)**: Main game logic and entry point for Tetris (ENHANCED VERSION)
  - Game loop, event handling, rendering
  - Brick movement, rotation, collision detection
  - Pause functionality with visual feedback
  - English interface
  - Line clearing logic and scoring

- **[drew.py](drew.py)**: Graphics utility
  - `Box` class: Draws rectangles on canvas (used for rendering bricks)

- **[main.py](main.py)**: Independent FastAPI server (not related to game)

### Game State Architecture

The game uses several global 2D arrays to manage state:

- `bricks_array[10][20]`: The main game container (10 wide × 20 tall)
- `bricks[4][4]`: Current active brick being controlled
- `bricks_next[4][4]`: Preview of next brick
- `bricks_list[10][20]`: Array of Box objects for rendering

### Brick System

Bricks are defined in `brick_dict` with a two-part key system:
- First digit (1-7): Brick type (N1, N2, L1, L2, T, O, I)
- Second digit (0-3): Rotation state

Example: `"30"` = L1 brick at rotation state 0

Key functions:
- `transformToBricks(brickId, state)`: Converts brick definition to 4×4 array
- `ifCopyToBricksArray()`: Collision detection - checks if brick can be placed
- `copyToBricksArray()`: Commits brick to game container
- `ifClearBrick()`: Detects and marks full lines for clearing
- `clearBrick()`: Removes marked lines and drops bricks above

### Game Modes

`game_mode` variable controls game state:
- `0`: Normal gameplay - bricks falling
- `1`: Line clearing in progress

### Coordinate System

- `container_x`: Horizontal position of current brick (-2 to 6)
  - Can be negative to allow bricks to partially extend beyond left edge
  - Maximum 6 to prevent rotation issues at right boundary
- `container_y`: Vertical position (-4 to 16)
  - Starts at -4 so bricks appear to fall from above the visible area

## Code Conventions

- The codebase uses traditional Chinese comments (Traditional Chinese is used in comments)
- Global variables are used extensively for game state
- Pygame event loop pattern with clock-based timing
- Color definitions use RGB tuples as constants at top of file
