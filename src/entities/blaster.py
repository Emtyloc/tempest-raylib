from src.shared import LEVEL, TempestColors
from pyray import *
from enum import Enum

class Blaster:
    """
    Player's shooter.
    """

    class Position(Enum):
        """
        Position inside a border section.
        """
        LEFT = 0
        CENTER_LEFT = 1
        CENTER = 2 
        CENTER_RIGHT = 3
        RIGHT = 4

        def next_value(self):
            """
            Returns the next enum value.
            """
            next_idx = self.value + 1
            if next_idx < len(Blaster.Position):
                return Blaster.Position(next_idx)
            return Blaster.Position.LEFT

        def prev_value(self):
            """
            Returns the previous enum value.
            """
            prev_idx = self.value - 1
            if prev_idx >= 0:
                return Blaster.Position(prev_idx)
            return Blaster.Position.RIGHT



    def __init__(self) -> None:
        self._init_defaults()
    
    def _init_defaults(self) -> None:
        self.border_idx = LEVEL.world.start_idx
        self.position = Blaster.Position.CENTER

    @property
    def border_idx(self):
        return self._border_idx
    
    @border_idx.setter
    def border_idx(self, value: int):
        if value < 0 or value > 15:
            raise ValueError("Border index cannot be less than 0 or greater than 15.")
        self._border_idx = value

    def _shift_left(self):
        # TODO: play movement sound
        if LEVEL.world.is_loop:
            if self.border_idx == 15:
                if self.position is Blaster.Position.LEFT:
                    self.border_idx = 0
            else:
                if self.position is Blaster.Position.LEFT:
                    self.border_idx += 1
            self.position = self.position.prev_value()
        else:
            if self.border_idx < 15:
                if self.position is Blaster.Position.LEFT:
                    self.border_idx += 1
                self.position = self.position.prev_value()
            elif self.position != Blaster.Position.LEFT:
                self.position = self.position.prev_value()

    
    def _shift_right(self):
        # TODO: play movement sound
        if LEVEL.world.is_loop:
            if self.border_idx == 0:
                if self.position is Blaster.Position.RIGHT:
                    self.border_idx = 15
            else:
                if self.position is Blaster.Position.RIGHT:
                    self.border_idx -= 1
            self.position = self.position.next_value()
        else:
            if self.border_idx > 1:
                if self.position is Blaster.Position.RIGHT:
                    self.border_idx -= 1
                self.position = self.position.next_value()
            elif self.position != Blaster.Position.RIGHT:
                self.position = self.position.next_value()

    # TODO: fix shift when on last position and last border
    
    def update(self):
        """
        Checks main loop events e.g. pressed keys.
        """

        if is_key_down(KeyboardKey.KEY_RIGHT):
            self._shift_left()
        
        if is_key_down(KeyboardKey.KEY_LEFT):
            self._shift_right()
        
    
    def draw(self):
        """
        Draw blaster in the world.
        """

        border_idx = Vector2(LEVEL.world.x[self.border_idx], LEVEL.world.y[self.border_idx])

        match self.position:
            case Blaster.Position.LEFT:
                out_left = border_idx
                next_border = Vector2(LEVEL.world.x[self.border_idx - 1], LEVEL.world.y[self.border_idx - 1])
                middle_dis = vector_2distance(out_left, next_border) / 2
                out_right = vector2_move_towards(out_left, next_border, middle_dis)
            
            case Blaster.Position.CENTER_LEFT:
                out_left = border_idx
                out_right = Vector2(LEVEL.world.x[self.border_idx - 1], LEVEL.world.y[self.border_idx - 1])
            
            case Blaster.Position.CENTER:
                out_left = border_idx
                out_right = Vector2(LEVEL.world.x[self.border_idx - 1], LEVEL.world.y[self.border_idx - 1])
                
            case Blaster.Position.CENTER_RIGHT:
                out_left = border_idx
                out_right = Vector2(LEVEL.world.x[self.border_idx - 1], LEVEL.world.y[self.border_idx - 1])

            case Blaster.Position.RIGHT:
                next_border = Vector2(LEVEL.world.x[self.border_idx - 1], LEVEL.world.y[self.border_idx - 1])
                middle_dis = vector_2distance(border_idx, next_border) / 2
                out_left = vector2_move_towards(border_idx, next_border, middle_dis)
                out_right = next_border

            case _:
                raise ValueError("Unknown position.")


        # This is constant between blaster inside position
            
        draw_circle_v(out_left, 4.0, TempestColors.YELLOW_NEON.rgba())
        draw_circle_v(out_right, 4.0, TempestColors.YELLOW_NEON.rgba())


        # anchor_middle_dis = vector_2distance(out_left, out_right) / 2

        # circle_pos = vector2_move_towards(out_left, , anchor_middle_dis)

        # draw_circle_v(circle_pos, 3.0, TempestColors.YELLOW_NEON.rgba())

    





