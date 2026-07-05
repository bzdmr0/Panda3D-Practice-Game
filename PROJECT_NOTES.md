# Project Notes

## Goal

The goal of this project is to show practical Panda3D fundamentals in a small, readable game:

- scene setup
- camera control
- lighting
- update loop
- user input
- procedural objects
- UI text
- collision checks
- game states

## Why the Game Uses Procedural Shapes

The project creates cubes, ship parts, route markers, and star streaks in code. This keeps the repository lightweight and avoids asset path problems when the project is cloned on another computer.

## Game State Flow

```text
start -> playing -> paused -> playing
                 -> gameover -> restart -> playing
```

## Main Technical Decisions

### 1. Simple Entity Model

Each object is represented by a `GameEntity` dataclass. It stores the object's NodePath, type, collision radius, score value, and rotation speed.

### 2. Radius-Based Collision

For this project, collisions are calculated using distance between the player and each entity. This is easy to explain and works well for a small arcade game.

### 3. Difficulty Scaling

The world speed increases with both score and elapsed time. The spawn interval decreases as the player survives longer, which makes the game gradually harder.

### 4. Separate UI Module

The UI text is managed in a separate `GameUI` class so the main game class does not become too crowded.

## Interview Summary

This project is a small but complete real-time 3D game. It demonstrates that I can learn a new framework, organize code into modules, build a playable loop, handle input and UI, and explain the technical design clearly.
