"""Central gameplay constants for Orbital Courier.

Keeping values here makes the project easy to tune and easy to explain in an
interview: the code separates game design values from game logic.
"""

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

PLAYER_LIMIT_X = 5.5
PLAYER_MIN_Z = 0.6
PLAYER_MAX_Z = 5.2
PLAYER_SPEED = 8.0
PLAYER_RADIUS = 0.75

WORLD_BASE_SPEED = 12.0
WORLD_MAX_SPEED = 27.0
SPAWN_Y = 55.0
DESPAWN_Y = -12.0

BASE_SPAWN_INTERVAL = 0.95
MIN_SPAWN_INTERVAL = 0.38

STARTING_LIVES = 3
HIT_COOLDOWN = 1.0

STAR_COUNT = 120
STAR_RESET_Y = 58.0
STAR_DESPAWN_Y = -16.0
