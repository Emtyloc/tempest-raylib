from pyray import Vector2, Color, RAYWHITE
from src.level import Level
from enum import Enum

SCREEN_WIDTH: int = 600
SCREEN_HEIGHT: int = 800
TARGET_FPS = 60
SCREEN_CENTER = Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
LEVEL = Level()




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