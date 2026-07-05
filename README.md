# Orbital Courier

**Orbital Courier** is a small 3D arcade game built with **Panda3D** and Python with the help of AI. It is created to gain experience for Panda3D.

The player controls a courier ship, collects data capsules, avoids orbital debris, and tries to survive as the route becomes faster over time.

## Gameplay

You are piloting a small courier ship through a space route.

- Collect **blue data capsules** to increase your score.
- Avoid **red orbital debris** because it reduces your lives.
- Pick up rare **green repair cells** to recover one life.
- The game becomes faster as time passes and your score increases.

## Controls

| Action | Key |
|---|---|
| Move | `WASD` or `Arrow Keys` |
| Start | `Enter` |
| Pause / Resume | `P` |
| Restart | `R` |
| Quit | `Esc` |

## Features

- Panda3D `ShowBase` application structure
- Procedural 3D objects, so no external models are required
- Real-time game loop using Panda3D tasks
- Player movement with smooth visual tilt
- Collectibles, hazards, lives, score, and restart logic
- Difficulty scaling based on score and elapsed time
- Simple collision detection using bounding radii
- HUD and menu text using Panda3D DirectGUI
- Camera, lighting, fog, starfield, and route grid

## Project Structure

```text
orbital-courier-panda3d/
├── main.py
├── requirements.txt
├── README.md
├── LICENSE
└── src/
    ├── __init__.py
    ├── constants.py
    ├── entities.py
    ├── game.py
    ├── mesh_factory.py
    └── ui.py
```

## Installation

### 1. Create a virtual environment

```bash
python -m venv .venv
```

### 2. Activate the virtual environment

Windows:

```bash
.venv\Scripts\activate
```

macOS / Linux:

```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the game

```bash
python main.py
```
