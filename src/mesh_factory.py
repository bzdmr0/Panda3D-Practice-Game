"""Small procedural mesh helpers.

The project intentionally does not depend on external 3D models. This makes the
repository portable: cloning the GitHub repo and installing Panda3D is enough to
run the game.
"""

from __future__ import annotations

from panda3d.core import (
    Geom,
    GeomNode,
    GeomTriangles,
    GeomVertexData,
    GeomVertexFormat,
    GeomVertexWriter,
    LineSegs,
    NodePath,
    Vec3,
)


def create_box(name: str, size: tuple[float, float, float], color: tuple[float, float, float, float]) -> NodePath:
    """Create a lit colored box as a Panda3D NodePath."""
    sx, sy, sz = size
    hx, hy, hz = sx / 2.0, sy / 2.0, sz / 2.0

    # Each face has its own vertices so every face can have a correct normal.
    faces = [
        # normal, four corners
        (Vec3(0, -1, 0), [(-hx, -hy, -hz), (hx, -hy, -hz), (hx, -hy, hz), (-hx, -hy, hz)]),
        (Vec3(0, 1, 0), [(-hx, hy, -hz), (-hx, hy, hz), (hx, hy, hz), (hx, hy, -hz)]),
        (Vec3(-1, 0, 0), [(-hx, -hy, -hz), (-hx, -hy, hz), (-hx, hy, hz), (-hx, hy, -hz)]),
        (Vec3(1, 0, 0), [(hx, -hy, -hz), (hx, hy, -hz), (hx, hy, hz), (hx, -hy, hz)]),
        (Vec3(0, 0, -1), [(-hx, -hy, -hz), (-hx, hy, -hz), (hx, hy, -hz), (hx, -hy, -hz)]),
        (Vec3(0, 0, 1), [(-hx, -hy, hz), (hx, -hy, hz), (hx, hy, hz), (-hx, hy, hz)]),
    ]

    vertex_data = GeomVertexData(name, GeomVertexFormat.getV3n3c4(), Geom.UHStatic)
    vertex_writer = GeomVertexWriter(vertex_data, "vertex")
    normal_writer = GeomVertexWriter(vertex_data, "normal")
    color_writer = GeomVertexWriter(vertex_data, "color")

    triangles = GeomTriangles(Geom.UHStatic)
    vertex_index = 0

    for normal, corners in faces:
        for corner in corners:
            vertex_writer.addData3f(*corner)
            normal_writer.addData3f(normal)
            color_writer.addData4f(*color)

        triangles.addVertices(vertex_index, vertex_index + 1, vertex_index + 2)
        triangles.addVertices(vertex_index, vertex_index + 2, vertex_index + 3)
        vertex_index += 4

    geom = Geom(vertex_data)
    geom.addPrimitive(triangles)
    node = GeomNode(name)
    node.addGeom(geom)
    return NodePath(node)


def create_player_ship() -> NodePath:
    """Create a small stylized courier ship from simple boxes."""
    root = NodePath("player_ship")

    body = create_box("ship_body", (0.7, 1.45, 0.35), (0.25, 0.70, 1.0, 1.0))
    body.reparentTo(root)

    cockpit = create_box("ship_cockpit", (0.42, 0.48, 0.26), (0.9, 0.95, 1.0, 1.0))
    cockpit.setPos(0, 0.10, 0.32)
    cockpit.reparentTo(root)

    nose = create_box("ship_nose", (0.48, 0.42, 0.24), (1.0, 0.85, 0.25, 1.0))
    nose.setPos(0, 0.94, 0.03)
    nose.reparentTo(root)

    left_wing = create_box("ship_left_wing", (0.85, 0.48, 0.12), (0.12, 0.35, 0.75, 1.0))
    left_wing.setPos(-0.73, -0.18, -0.03)
    left_wing.reparentTo(root)

    right_wing = create_box("ship_right_wing", (0.85, 0.48, 0.12), (0.12, 0.35, 0.75, 1.0))
    right_wing.setPos(0.73, -0.18, -0.03)
    right_wing.reparentTo(root)

    engine = create_box("ship_engine", (0.42, 0.18, 0.22), (1.0, 0.45, 0.12, 1.0))
    engine.setPos(0, -0.83, 0.0)
    engine.reparentTo(root)

    root.setHpr(0, 0, 0)
    return root


def create_grid(size_x: int = 12, length_y: int = 70, z: float = 0.0) -> NodePath:
    """Create a simple runway grid using Panda3D line geometry."""
    lines = LineSegs("runway_grid")
    lines.setThickness(1.0)
    lines.setColor(0.15, 0.45, 0.75, 0.38)

    for x in range(-size_x, size_x + 1, 2):
        lines.moveTo(x, -8, z)
        lines.drawTo(x, length_y, z)

    for y in range(-8, length_y + 1, 4):
        lines.moveTo(-size_x, y, z)
        lines.drawTo(size_x, y, z)

    return NodePath(lines.create())


def create_star(name: str) -> NodePath:
    """Create a tiny star streak."""
    lines = LineSegs(name)
    lines.setThickness(1.5)
    lines.setColor(0.75, 0.90, 1.0, 0.55)
    lines.moveTo(0, 0, 0)
    lines.drawTo(0, -0.55, 0)
    return NodePath(lines.create())
