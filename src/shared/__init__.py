from .event_manager import EventManager
from pyray import Color, RAYWHITE
from enum import Enum
from src.utils import Vec2


"""
NOTE: It is important that here you define constants only.
DO NOT import or initialize other python modules to avoid circular imports.
"""

SCREEN_WIDTH: int = 600
SCREEN_HEIGHT: int = 800
TARGET_FPS = 60
SCREEN_CENTER = Vec2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

class TempestColors(Enum):
    BLUE_NEON = Color(31, 81, 255, 255)
    RED_NEON = Color(255, 49, 49, 255)
    GREEN_NEON = Color(15, 255, 80, 255)
    YELLOW_NEON = Color(223, 255, 0, 255)
    TURQUOISE_NEON = Color(64, 224, 208, 255)
    PURPLE_NEON = Color(191, 64, 191, 255)
    WHITE_NEON = RAYWHITE

    def rgba(self) -> Color:
        return self.value