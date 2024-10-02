from src.shared import TempestColors, SCREEN_CENTER
from pyray import *
from enum import Enum
from src.utils import vector2_perp
from src.utils import vector2_center_scale
from src.level import LEVEL


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

        def next_pos(self):
            next_idx = self.value + 1
            if next_idx < len(Blaster.Position):
                return Blaster.Position(next_idx)
            return Blaster.Position.LEFT

        def prev_pos(self):
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

    # NOTE: all levels were constructed clock-wise, and appended to the (x,y) list in that order
    # which means that border_idx + 1 jumps to left/clock-wise, and vice-versa.

    def _shift_left(self):
        # TODO: play movement sound
        if LEVEL.world.is_loop:
            if self.position is Blaster.Position.LEFT:
                if self.border_idx == 15:
                    self.border_idx = 0
                else:
                    self.border_idx += 1
            self.position = self.position.prev_pos()

        else:
            if self.position is Blaster.Position.LEFT:
                if self.border_idx < 15:
                    self.border_idx += 1
                    self.position = self.position.prev_pos()
            else:
                self.position = self.position.prev_pos()

    def _shift_right(self):
        # TODO: play movement sound
        if LEVEL.world.is_loop:
            if self.position is Blaster.Position.RIGHT:
                if self.border_idx == 0:
                    self.border_idx = 15
                else:
                    self.border_idx -= 1
            self.position = self.position.next_pos()
        else:
            if self.position is Blaster.Position.RIGHT:
                if self.border_idx > 1:
                    self.border_idx -= 1
                    self.position = self.position.next_pos()
            else:
                self.position = self.position.next_pos()

    def update(self):
        """
        Checks main loop events e.g. pressed keys.
        """

        if is_key_down(KeyboardKey.KEY_RIGHT):
            self._shift_left()

        if is_key_down(KeyboardKey.KEY_LEFT):
            self._shift_right()

    # TODO: Draw inside Blaster vectors.
    def draw(self):
        """
        Draw blaster in the world.
        """

        # left border -> */__\
        border = Vector2(LEVEL.world.x[self.border_idx], LEVEL.world.y[self.border_idx])
        # /__\* <- right border
        next_border = Vector2(
            LEVEL.world.x[self.border_idx - 1], LEVEL.world.y[self.border_idx - 1]
        )
        border_line = vector2_subtract(next_border, border)
        # distance from border line and blaster spike (highest point)
        blaster_height = vector_2distance(border, next_border) / 4
        tongs_height = blaster_height / 2

        def tong_vectors(
            out_left: Vector2, out_right: Vector2
        ) -> tuple[Vector2, Vector2]:
            """
            Compute Blaster tong vectors using out_left and out_right anchors.
            """

            perp = vector2_scale(vector2_perp(border_line), -tongs_height)

            if self.position is Blaster.Position.LEFT:
                left_quarter = vector2_lerp(out_left, out_right, 0.5)
                right_half_quarter = vector2_lerp(out_right, next_border, 0.5)
                left_tong = vector2_add(left_quarter, perp)
                right_tong = vector2_add(right_half_quarter, perp)

            elif self.position is Blaster.Position.RIGHT:
                left_quarter = vector2_lerp(out_left, border, 0.5)
                right_half_quarter = vector2_lerp(out_right, out_left, 0.5)
                left_tong = vector2_add(left_quarter, perp)
                right_tong = vector2_add(right_half_quarter, perp)

            else:
                left_quarter = vector2_lerp(out_left, out_right, 0.25)
                right_quarter = vector2_lerp(out_right, out_left, 0.25)
                left_tong = vector2_add(left_quarter, perp)
                right_tong = vector2_add(right_quarter, perp)

            return left_tong, right_tong


        # Compute anchors to draw within Blaster position. */__*__\ <-> */____\* <-> /__*__\*
        match self.position:
            case Blaster.Position.LEFT:
                out_left = border
                out_right = vector2_lerp(out_left, next_border, 0.5)
                perp = vector2_scale(vector2_perp(border_line), blaster_height)
                spike = vector2_add(border, perp)
                left_tong, right_tong = tong_vectors(out_left, out_right)

            case Blaster.Position.CENTER_LEFT:
                out_left = border
                out_right = next_border
                left_quarter = vector2_lerp(border, next_border, 0.25)
                perp = vector2_scale(vector2_perp(border_line), blaster_height)
                spike = vector2_add(left_quarter, perp)
                left_tong, right_tong = tong_vectors(out_left, out_right)

            case Blaster.Position.CENTER:
                out_left = border
                out_right = next_border
                middle = vector2_lerp(border, next_border, 0.5)
                perp = vector2_scale(vector2_perp(border_line), blaster_height)
                spike = vector2_add(middle, perp)
                left_tong, right_tong = tong_vectors(out_left, out_right)

            case Blaster.Position.CENTER_RIGHT:
                out_left = border
                out_right = next_border
                left_quarter = vector2_lerp(next_border, border, 0.25)
                perp = vector2_scale(vector2_perp(border_line), blaster_height)
                spike = vector2_add(left_quarter, perp)
                left_tong, right_tong = tong_vectors(out_left, out_right)

            case Blaster.Position.RIGHT:
                out_left = vector2_lerp(border, next_border, 0.5)
                out_right = next_border
                perp = vector2_scale(vector2_perp(border_line), blaster_height)
                spike = vector2_add(next_border, perp)
                left_tong, right_tong = tong_vectors(out_left, out_right)

            case _:
                raise ValueError("Unknown position.")

        # Draw outside lines
        # spike
        draw_line_ex(out_left, spike, 2, TempestColors.YELLOW_NEON.rgba())
        draw_line_ex(out_right, spike, 2, TempestColors.YELLOW_NEON.rgba())
        # tong
        draw_line_ex(out_left, left_tong, 2, TempestColors.YELLOW_NEON.rgba())
        draw_line_ex(out_right, right_tong, 2, TempestColors.YELLOW_NEON.rgba())

        # Change color of blaster current border section  -> /_x_\ <-
        proyections = LEVEL.world.get_proyection()
        draw_line_ex(border, proyections[self.border_idx], 2, TempestColors.YELLOW_NEON.rgba())
        draw_line_ex(next_border, proyections[self.border_idx - 1], 2, TempestColors.YELLOW_NEON.rgba())