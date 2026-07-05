"""Entry point for Orbital Courier.

Run with:
    python main.py
"""

from panda3d.core import loadPrcFileData

from src.constants import WINDOW_HEIGHT, WINDOW_WIDTH

loadPrcFileData(
    "",
    f"""
    window-title Orbital Courier
    win-size {WINDOW_WIDTH} {WINDOW_HEIGHT}
    framebuffer-multisample 1
    multisamples 4
    sync-video 1
    show-frame-rate-meter 1
    """,
)

from src.game import OrbitalCourierGame  # noqa: E402  # Panda3D config must load first.


if __name__ == "__main__":
    game = OrbitalCourierGame()
    game.run()
