"""User interface helpers built with Panda3D DirectGUI text."""

from __future__ import annotations

from direct.gui.OnscreenText import OnscreenText
from panda3d.core import TextNode


class GameUI:
    """Owns all screen text so the main game class stays focused on logic."""

    def __init__(self) -> None:
        self.title = OnscreenText(
            text="ORBITAL COURIER",
            pos=(0, 0.72),
            scale=0.095,
            fg=(0.85, 0.95, 1.0, 1.0),
            align=TextNode.ACenter,
            mayChange=True,
        )
        self.subtitle = OnscreenText(
            text="Collect data capsules, avoid debris, and keep the courier route alive.",
            pos=(0, 0.60),
            scale=0.039,
            fg=(0.78, 0.88, 1.0, 1.0),
            align=TextNode.ACenter,
            mayChange=True,
        )
        self.prompt = OnscreenText(
            text="Press ENTER to start",
            pos=(0, -0.65),
            scale=0.05,
            fg=(1.0, 0.86, 0.25, 1.0),
            align=TextNode.ACenter,
            mayChange=True,
        )
        self.score = OnscreenText(
            text="Score: 0",
            pos=(-1.28, 0.92),
            scale=0.045,
            fg=(0.86, 0.95, 1.0, 1.0),
            align=TextNode.ALeft,
            mayChange=True,
        )
        self.lives = OnscreenText(
            text="Lives: 3",
            pos=(-1.28, 0.86),
            scale=0.045,
            fg=(0.86, 1.0, 0.86, 1.0),
            align=TextNode.ALeft,
            mayChange=True,
        )
        self.speed = OnscreenText(
            text="Speed: 0",
            pos=(1.28, 0.92),
            scale=0.045,
            fg=(0.86, 0.95, 1.0, 1.0),
            align=TextNode.ARight,
            mayChange=True,
        )
        self.help = OnscreenText(
            text="WASD / Arrow Keys: Move   P: Pause   R: Restart   ESC: Quit",
            pos=(0, -0.93),
            scale=0.033,
            fg=(0.75, 0.82, 0.95, 1.0),
            align=TextNode.ACenter,
            mayChange=True,
        )

    def update_hud(self, score: int, lives: int, speed: float) -> None:
        self.score.setText(f"Score: {score}")
        self.lives.setText(f"Lives: {lives}")
        self.speed.setText(f"Speed: {speed:.1f}")

    def show_start(self) -> None:
        self.title.show()
        self.subtitle.show()
        self.prompt.setText("Press ENTER to start")
        self.prompt.show()

    def show_playing(self) -> None:
        self.title.hide()
        self.subtitle.hide()
        self.prompt.hide()

    def show_paused(self) -> None:
        self.title.setText("PAUSED")
        self.subtitle.setText("Press P to continue")
        self.prompt.setText("R: Restart   ESC: Quit")
        self.title.show()
        self.subtitle.show()
        self.prompt.show()

    def show_game_over(self, score: int) -> None:
        self.title.setText("ROUTE FAILED")
        self.subtitle.setText(f"Final score: {score}")
        self.prompt.setText("Press R to restart or ESC to quit")
        self.title.show()
        self.subtitle.show()
        self.prompt.show()

    def set_hit_feedback(self, active: bool) -> None:
        if active:
            self.lives["fg"] = (1.0, 0.35, 0.25, 1.0)
        else:
            self.lives["fg"] = (0.86, 1.0, 0.86, 1.0)
