# Turtle Drawing Game

A pygame-based horror drawing game inspired by Python turtle graphics.

**Play Now:** https://moohoorama.github.io/kshdraw/

## Overview

Control the turtle with arrow keys (or touch controls on mobile) to draw along the dotted path. Reach the green goal box to clear each stage.
But beware - straying from the path costs lives, and special stages bring terrifying surprises...

## How to Run

### Local
```bash
pip install pygame
make run
# or
python main.py
```

### Web Build & Deploy
```bash
pip install pygbag
make deploy   # Build, patch, and push to GitHub Pages
```

## Controls

### Desktop
| Key | Action |
|---|---|
| Arrow Keys | Move turtle |
| SPACE | Start / Restart |
| ESC | Quit |

### Mobile (Touch)
- **D-Pad** (left side): Move turtle
- **Action Button** (right side): Start / Restart

## Game Rules

- **Lives**: 5
- **Path Deviation**: Lose 1 life if you stray more than 30 pixels
- **Stages**: 44+
- **Special Stages**: Stages containing the number 4 (4, 14, 24, 34, 44...)

## Special Stages (Numbers with 4)

On special stages:
1. "Press any key..." message appears
2. Creepy messages are auto-drawn in red
3. **Glitch effects** accumulate after clearing

### Creepy Messages
- "Why did you leave us?"
- "Why didn't you save us?"
- "We're still here..."
- "Behind you..."
- "You can't escape..."

## Glitch Effects (Cumulative)

Each special stage cleared adds random effects:

### Control Glitches
- Left/Right inverted
- Up/Down inverted
- Speed changes

### Visual Glitches
- **Darkness**: Screen gradually darkens
- **Skulls**: Realistic skulls appear randomly
- **Blood**: Blood drips down the screen
- **Static Noise**: TV static effect
- **Screen Shake**: Screen trembles
- **Flicker**: Screen flashes

### Sound Effects
- Drone sounds (low frequency)
- Whispers
- Heartbeat
- Screams
- Footsteps
- Breathing
- Jump scare sounds

## Enemy System

As glitch level increases, terrifying enemies appear:

| Enemy Type | Description |
|---|---|
| Shadow | Irregular dark form with red eyes |
| Crawler | Multi-legged crawling creature |
| Ghost | Translucent, wavy ghost form |
| Demon | Horns, yellow eyes, sharp teeth |

- Touching an enemy = **Instant Game Over**
- Higher glitch level = Faster enemies, more spawns

## Easter Egg

- **Sans (Undertale)**: 5% chance when skulls appear
  - Blue eye glow effect
  - "* You're gonna have a bad time." message

## Endings

### Stage 44 Clear - Hospital Ending
- Hospital room background (bed, medical equipment, window)
- Flatline on heart monitor
- "Beeeep..." sound
- Screen fades to black

### Game Over Screen
- Dark room background
- Teddy bear in spotlight at center
- Other dolls watching from around
- Clown doll
- Moonlit window
- Vignette effect

## File Structure

```
ksh/
├── main.py              # Main game loop, rendering, touch controls
├── utils.py             # Constants, utility functions
├── turtle_player.py     # TurtlePlayer, AutoDrawer classes
├── stage.py             # Stage class, 44+ stage path definitions
├── effects.py           # GlitchEffect, Enemy, SoundManager classes
├── Makefile             # Build automation
├── scripts/
│   └── patch_index.py   # iOS Safari fix patch script
├── docs/                # GitHub Pages deployment folder
│   ├── index.html
│   ├── favicon.png
│   └── ksh.apk
└── README.md
```

## Makefile Commands

```bash
make help     # Show available commands
make run      # Run locally with Python
make build    # Build with pygbag and apply patches
make deploy   # Build, patch, commit, and push to GitHub
make patch    # Apply iOS Safari fix only
make clean    # Remove build directory
```

## Key Classes

### `Game` (main.py)
Main game class. Handles game loop, state management, rendering, and touch controls.

### `VirtualDPad` / `ActionButton` (main.py)
Touch control classes for mobile devices.

### `TurtlePlayer` (turtle_player.py)
Player-controlled turtle. Handles movement and line drawing.

### `AutoDrawer` (turtle_player.py)
Auto-draws creepy messages on special stages.

### `Stage` (stage.py)
Stage path definitions. 44+ varied shapes:
- Lines, triangles, squares
- Stars, hearts, spirals
- Waves, zigzags, mazes
- Complex patterns

### `GlitchEffect` (effects.py)
Manages glitch effects. Visual/control glitches, enemy spawning.

### `Enemy` (effects.py)
Enemy class. 4 enemy types with AI movement.

### `SoundManager` (effects.py)
Procedural sound generation. No external audio files needed.

## Dependencies

- Python 3.x
- pygame
- pygbag (for web build)

## Web Version Notes

- **Touch Support**: Virtual D-Pad and action button for mobile
- **iOS Safari**: Auto-patched for touch event handling
- **Sound**: May be limited by browser autoplay policies
- **Performance**: May be slower than local execution

---

## License

Personal Project
