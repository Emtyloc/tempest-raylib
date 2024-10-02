from enum import Enum
from src.worlds import LevelData
from pyray import *
from src.shared import TempestColors

class Level:
    
    class States(Enum):
        LEVEL_BEGIN = 0
        LEVEL_COMPLETE = 1
        LEVEL_READY = 2

    def __init__(self) -> None:
        self._init_defaults()
    
    def _init_defaults(self):
        self._world = None
        self.state = self.States.LEVEL_BEGIN
        self.has_flippers = False
        self.has_tankers = False
        self.has_fuseballs = False
        self.has_spikers = False
        self.has_pulsars = False
        self.color = TempestColors.BLUE_NEON.rgba()
    
    @property
    def world(self) -> LevelData:
        return self._world

    @world.setter
    def world(self, value: LevelData):
        self._world = value

    def update(self):
        pass

    def draw(self):
        self._draw_world()

    def _draw_world(self):
        proyections = self.world.get_proyection()
        for i in range(16):
            draw_circle(int(self.world.x[i]), int(self.world.y[i]), 2, self.color)
            border_vec = Vector2(self.world.x[i], self.world.y[i])
            draw_circle_v(proyections[i], 1, self.color)
            draw_line_ex(border_vec, proyections[i], 2, self.color)
            if i > 0:
                current_vec = Vector2(self.world.x[i], self.world.y[i])
                previous_vec = Vector2(self.world.x[i-1], self.world.y[i-1])
                draw_line_ex(current_vec, previous_vec, 2, self.color)
                draw_line_ex(proyections[i], proyections[i-1], 1, self.color)
        else:
            if self.world.is_loop:
                current_vec = Vector2(self.world.x[0],self.world.y[0])
                last_vec = Vector2(self.world.x[-1], self.world.y[-1])
                draw_line_ex(current_vec, last_vec, 2, self.color)
                draw_line_ex(proyections[0], proyections[-1], 1, self.color)
    

    
