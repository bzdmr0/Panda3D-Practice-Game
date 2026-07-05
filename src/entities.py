"""Entity definitions for Orbital Courier."""

from __future__ import annotations

from dataclasses import dataclass, field
from random import choice, uniform

from panda3d.core import NodePath, Vec3

from .mesh_factory import create_box


@dataclass
class GameEntity:
    """A moving object in the world.

    The game uses a lightweight entity model instead of a full ECS. For a small
    portfolio project, this keeps the code readable while still showing clear
    separation between data and behavior.
    """

    node: NodePath
    kind: str
    radius: float
    value: int = 0
    rotation_speed: Vec3 = field(default_factory=lambda: Vec3(0, 0, 0))

    def update(self, dt: float, world_speed: float) -> None:
        self.node.setY(self.node.getY() - world_speed * dt)
        self.node.setHpr(self.node.getHpr() + self.rotation_speed * dt)

    def destroy(self) -> None:
        self.node.removeNode()


class EntityFactory:
    """Creates collectible and hazard entities."""

    def create_data_capsule(self) -> GameEntity:
        node = create_box("data_capsule", (0.62, 0.62, 0.62), (0.2, 0.9, 1.0, 1.0))
        node.setPos(uniform(-5.0, 5.0), 55.0, uniform(0.8, 5.0))
        return GameEntity(node=node, kind="data", radius=0.58, value=10, rotation_speed=Vec3(45, 90, 30))

    def create_repair_cell(self) -> GameEntity:
        node = create_box("repair_cell", (0.54, 0.54, 0.54), (0.3, 1.0, 0.35, 1.0))
        node.setPos(uniform(-5.0, 5.0), 55.0, uniform(0.8, 5.0))
        return GameEntity(node=node, kind="repair", radius=0.52, value=0, rotation_speed=Vec3(70, 40, 25))

    def create_debris(self) -> GameEntity:
        size = choice([(1.0, 0.8, 0.65), (0.75, 1.25, 0.55), (1.25, 0.65, 0.75)])
        node = create_box("orbital_debris", size, (1.0, 0.25, 0.18, 1.0))
        node.setPos(uniform(-5.0, 5.0), 55.0, uniform(0.8, 5.0))
        node.setHpr(uniform(0, 360), uniform(0, 360), uniform(0, 360))
        return GameEntity(node=node, kind="debris", radius=0.78, value=0, rotation_speed=Vec3(35, 55, 75))
