from src.shared import LEVEL, TempestColors
from pyray import *

class Blaster:
    """
    Player's shooter.
    """
    def __init__(self) -> None:
        self._init_defaults()
    
    def _init_defaults(self) -> None:
        self.border_idx = 0

    
    @property
    def border_idx(self):
        return self._border_idx
    
    @border_idx.setter
    def border_idx(self, value: int):
        if value < 0 or value > 15:
            raise ValueError("Border index cannot be less than 0 or greater than 15.")
        self._border_idx = value

    #TODO: fix movement and drawing system

    def _shift_left(self):
        # TODO: play movement sound
        if LEVEL.world.is_loop:
            if self.border_idx == 15:
                self.border_idx = 0
            else:
                self.border_idx += 1
        else:
            if self.border_idx < 15:
                self.border_idx += 1
    
    def _shift_right(self):
        # TODO: play movement sound
        if LEVEL.world.is_loop:
            if self.border_idx == 0:
                self.border_idx = 15
            else:
                self.border_idx -= 1
        else:
            if self.border_idx > 1:
                self.border_idx -= 1
    
    def update(self):
        """
        Checks main loop events e.g. pressed keys.
        """

        if is_key_pressed(KeyboardKey.KEY_RIGHT):
            self._shift_left()
        
        if is_key_pressed(KeyboardKey.KEY_LEFT):
            self._shift_right()
        
    
    def draw(self):
        """
        Draw blaster in the world.
        """


        current_pos = Vector2(LEVEL.world.x[self.border_idx], LEVEL.world.y[self.border_idx])
        anchor = Vector2(LEVEL.world.x[self.border_idx - 1], LEVEL.world.y[self.border_idx - 1]) #We always anchor to right

        draw_circle_v(current_pos, 2.0, TempestColors.GREEN_NEON.rgba())
        draw_circle_v(anchor, 2.0, TempestColors.PURPLE_NEON.rgba())


        anchor_middle_dis = vector_2distance(current_pos, anchor) / 2

        circle_pos = vector2_move_towards(current_pos, anchor, anchor_middle_dis)

        draw_circle_v(circle_pos, 3.0, TempestColors.YELLOW_NEON.rgba())

    

    





