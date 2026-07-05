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

## How I Would Explain This Project in an Interview

> I built a small 3D arcade game in Panda3D to demonstrate the fundamentals of a real-time game loop. The project uses Panda3D's `ShowBase` as the application base, NodePaths for scene graph organization, task-based updates for frame-by-frame logic, DirectGUI text for the HUD, and procedural geometry so the project does not depend on external assets.
>
> The core gameplay loop is simple: the player moves a courier ship, collects data capsules, avoids debris, and survives as the world speed increases. I separated the project into modules: constants for tunable game values, a mesh factory for procedural models, entities for moving objects, UI for screen text, and the main game class for state management.
>
> I also implemented basic difficulty scaling, collision checks, restart/pause states, and visual feedback when the player takes damage. The goal was not to make a huge game, but to show that I understand how to structure an interactive 3D application in Panda3D.

## Possible Improvements

- Add sound effects and background music
- Add a main menu with difficulty selection
- Add particle effects for collection and damage
- Add high-score saving with a local JSON file
- Replace procedural shapes with custom 3D models
- Add Panda3D collision solids as an alternative to radius-based collisions

## License

This project is released under the MIT License.
