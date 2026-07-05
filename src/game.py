"""Main Panda3D game class for Orbital Courier."""

from __future__ import annotations

import random
from dataclasses import dataclass

from direct.showbase.ShowBase import ShowBase
from direct.showbase.ShowBaseGlobal import globalClock
from panda3d.core import AmbientLight, DirectionalLight, Fog, NodePath, Vec3

from .constants import (
    BASE_SPAWN_INTERVAL,
    DESPAWN_Y,
    HIT_COOLDOWN,
    MIN_SPAWN_INTERVAL,
    PLAYER_LIMIT_X,
    PLAYER_MAX_Z,
    PLAYER_MIN_Z,
    PLAYER_RADIUS,
    PLAYER_SPEED,
    STAR_COUNT,
    STAR_DESPAWN_Y,
    STAR_RESET_Y,
    STARTING_LIVES,
    WORLD_BASE_SPEED,
    WORLD_MAX_SPEED,
)
from .entities import EntityFactory, GameEntity
from .mesh_factory import create_box, create_grid, create_player_ship, create_star
from .ui import GameUI


@dataclass
class InputState:
    left: bool = False
    right: bool = False
    up: bool = False
    down: bool = False

    def axis(self) -> Vec3:
        x = float(self.right) - float(self.left)
        z = float(self.up) - float(self.down)
        movement = Vec3(x, 0, z)
        if movement.length() > 0:
            movement.normalize()
        return movement


class OrbitalCourierGame(ShowBase):
    """A compact 3D arcade game built with Panda3D.

    The class demonstrates several Panda3D basics that are useful in a job
    application project:
    - ShowBase application setup
    - scene graph organization with NodePath
    - task-based update loop
    - camera, lighting, fog, and UI text
    - procedural mesh creation
    - simple collision and game-state management
    """

    def __init__(self) -> None:
        super().__init__()

        self.disableMouse()
        self.setBackgroundColor(0.01, 0.02, 0.06, 1)

        self.input_state = InputState()
        self.ui = GameUI()
        self.factory = EntityFactory()

        self.world = NodePath("world")
        self.world.reparentTo(self.render)

        self.entities: list[GameEntity] = []
        self.stars: list[NodePath] = []
        self.player = create_player_ship()
        self.player.reparentTo(self.world)

        self.score = 0
        self.lives = STARTING_LIVES
        self.elapsed = 0.0
        self.spawn_timer = 0.0
        self.hit_cooldown = 0.0
        self.state = "start"

        self._setup_camera()
        self._setup_lighting()
        self._setup_environment()
        self._setup_controls()
        self._reset_world()

        self.ui.show_start()
        self.taskMgr.add(self._update, "main_update")

    def _setup_camera(self) -> None:
        self.camera.setPos(0, -17.5, 7.2)
        self.camera.lookAt(0, 15, 2.6)
        self.camLens.setFov(72)

    def _setup_lighting(self) -> None:
        ambient = AmbientLight("ambient")
        ambient.setColor((0.28, 0.33, 0.45, 1))
        ambient_np = self.render.attachNewNode(ambient)
        self.render.setLight(ambient_np)

        key_light = DirectionalLight("key_light")
        key_light.setColor((0.95, 0.95, 1.0, 1))
        key_np = self.render.attachNewNode(key_light)
        key_np.setHpr(-35, -55, 0)
        self.render.setLight(key_np)

        fog = Fog("space_fog")
        fog.setColor(0.01, 0.02, 0.06)
        fog.setExpDensity(0.022)
        self.render.setFog(fog)

    def _setup_environment(self) -> None:
        grid = create_grid()
        grid.reparentTo(self.world)

        left_rail = create_box("left_route_marker", (0.08, 68, 0.08), (0.15, 0.55, 1.0, 1.0))
        left_rail.setPos(-6.1, 26, 0.05)
        left_rail.reparentTo(self.world)

        right_rail = create_box("right_route_marker", (0.08, 68, 0.08), (0.15, 0.55, 1.0, 1.0))
        right_rail.setPos(6.1, 26, 0.05)
        right_rail.reparentTo(self.world)

        for index in range(STAR_COUNT):
            star = create_star(f"star_{index}")
            star.setPos(random.uniform(-18, 18), random.uniform(-10, STAR_RESET_Y), random.uniform(1, 12))
            star.reparentTo(self.render)
            self.stars.append(star)

    def _setup_controls(self) -> None:
        self.accept("escape", self.userExit)
        self.accept("enter", self._start_game)
        self.accept("p", self._toggle_pause)
        self.accept("r", self._restart_game)

        key_bindings = {
            "a": "left",
            "arrow_left": "left",
            "d": "right",
            "arrow_right": "right",
            "w": "up",
            "arrow_up": "up",
            "s": "down",
            "arrow_down": "down",
        }

        for key, action in key_bindings.items():
            self.accept(key, self._set_key, [action, True])
            self.accept(f"{key}-up", self._set_key, [action, False])

    def _set_key(self, action: str, is_pressed: bool) -> None:
        setattr(self.input_state, action, is_pressed)

    def _start_game(self) -> None:
        if self.state == "start":
            self.state = "playing"
            self.ui.show_playing()

    def _toggle_pause(self) -> None:
        if self.state == "playing":
            self.state = "paused"
            self.ui.show_paused()
        elif self.state == "paused":
            self.state = "playing"
            self.ui.show_playing()

    def _restart_game(self) -> None:
        if self.state in {"playing", "paused", "gameover"}:
            self._reset_world()
            self.state = "playing"
            self.ui.show_playing()

    def _reset_world(self) -> None:
        for entity in self.entities:
            entity.destroy()
        self.entities.clear()

        self.player.setPos(0, 0, 2.6)
        self.player.setHpr(0, 0, 0)
        self.player.setColorScale(1, 1, 1, 1)

        self.score = 0
        self.lives = STARTING_LIVES
        self.elapsed = 0.0
        self.spawn_timer = 0.25
        self.hit_cooldown = 0.0
        self.ui.update_hud(self.score, self.lives, self._world_speed())
        self.ui.set_hit_feedback(False)

    def _world_speed(self) -> float:
        score_bonus = self.score * 0.035
        time_bonus = self.elapsed * 0.055
        return min(WORLD_MAX_SPEED, WORLD_BASE_SPEED + score_bonus + time_bonus)

    def _spawn_interval(self) -> float:
        pressure = min(0.57, self.elapsed * 0.006 + self.score * 0.0018)
        return max(MIN_SPAWN_INTERVAL, BASE_SPAWN_INTERVAL - pressure)

    def _spawn_entity(self) -> None:
        roll = random.random()
        if roll < 0.58:
            entity = self.factory.create_data_capsule()
        elif roll < 0.92:
            entity = self.factory.create_debris()
        else:
            entity = self.factory.create_repair_cell()

        entity.node.reparentTo(self.world)
        self.entities.append(entity)

    def _update(self, task):
        dt = min(globalClock.getDt(), 1 / 20)
        self._update_stars(dt)

        if self.state != "playing":
            return task.cont

        self.elapsed += dt
        self.hit_cooldown = max(0.0, self.hit_cooldown - dt)

        self._update_player(dt)
        self._update_spawning(dt)
        self._update_entities(dt)
        self._update_hit_feedback()

        self.ui.update_hud(self.score, self.lives, self._world_speed())
        return task.cont

    def _update_player(self, dt: float) -> None:
        movement = self.input_state.axis()
        new_pos = self.player.getPos() + movement * PLAYER_SPEED * dt
        new_pos.x = max(-PLAYER_LIMIT_X, min(PLAYER_LIMIT_X, new_pos.x))
        new_pos.z = max(PLAYER_MIN_Z, min(PLAYER_MAX_Z, new_pos.z))
        new_pos.y = 0
        self.player.setPos(new_pos)

        # Small visual tilt makes movement feel responsive without physics.
        target_roll = -movement.x * 13.0
        target_pitch = movement.z * 7.0
        current_hpr = self.player.getHpr()
        self.player.setHpr(current_hpr.x, current_hpr.y + (target_pitch - current_hpr.y) * 0.16, current_hpr.z + (target_roll - current_hpr.z) * 0.16)

    def _update_spawning(self, dt: float) -> None:
        self.spawn_timer -= dt
        if self.spawn_timer <= 0:
            self._spawn_entity()
            self.spawn_timer = self._spawn_interval()

    def _update_entities(self, dt: float) -> None:
        world_speed = self._world_speed()
        player_pos = self.player.getPos(self.world)
        survivors: list[GameEntity] = []

        for entity in self.entities:
            entity.update(dt, world_speed)

            if entity.node.getY() < DESPAWN_Y:
                entity.destroy()
                continue

            distance = (entity.node.getPos(self.world) - player_pos).length()
            if distance <= entity.radius + PLAYER_RADIUS:
                self._handle_collision(entity)
                entity.destroy()
                continue

            survivors.append(entity)

        self.entities = survivors

    def _handle_collision(self, entity: GameEntity) -> None:
        if entity.kind == "data":
            self.score += entity.value
        elif entity.kind == "repair":
            self.lives = min(STARTING_LIVES, self.lives + 1)
            self.score += 5
        elif entity.kind == "debris" and self.hit_cooldown <= 0:
            self.lives -= 1
            self.hit_cooldown = HIT_COOLDOWN
            if self.lives <= 0:
                self.state = "gameover"
                self.ui.show_game_over(self.score)

    def _update_hit_feedback(self) -> None:
        if self.hit_cooldown > 0:
            blink = int(self.hit_cooldown * 12) % 2 == 0
            self.player.setColorScale(1.0, 0.45, 0.45, 1.0) if blink else self.player.setColorScale(1, 1, 1, 1)
            self.ui.set_hit_feedback(True)
        else:
            self.player.setColorScale(1, 1, 1, 1)
            self.ui.set_hit_feedback(False)

    def _update_stars(self, dt: float) -> None:
        speed = self._world_speed() * 1.25 if self.state == "playing" else WORLD_BASE_SPEED * 0.25
        for star in self.stars:
            star.setY(star.getY() - speed * dt)
            if star.getY() < STAR_DESPAWN_Y:
                star.setPos(random.uniform(-18, 18), STAR_RESET_Y, random.uniform(1, 12))
