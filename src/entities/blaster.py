from src.shared import TempestColors, EventManager
from pyray import *
from enum import IntEnum
from src.utils import Vec2
from src.worlds import WorldData
from src.sounds import SoundManager
from .blaster_bullet import BlasterBullet


class Blaster:
    """
    Player's shooter.
    """

    class Position(IntEnum):
        """
        Position inside a border section.
        """

        LEFT = 0
        CENTER_LEFT = 1
        CENTER = 2
        CENTER_RIGHT = 3
        RIGHT = 4

        def next_pos(self):
            next_idx = self + 1 
            if next_idx < len(Blaster.Position):
                return Blaster.Position(next_idx)
            return Blaster.Position.LEFT

        def prev_pos(self):
            prev_idx = self - 1
            if prev_idx >= 0:
                return Blaster.Position(prev_idx)
            return Blaster.Position.RIGHT

    def __init__(self, world: WorldData, event_manager: EventManager, sound_manager: SoundManager) -> None:
        self._init_defaults()
        self.event_manager = event_manager
        self.sound_manager = sound_manager
        self.world = world
        self.border_idx = world.start_idx
        event_manager.notify(EventManager.Topics.BLASTER_BORDER_UPDATE, {"border_idx": self.border_idx})
        event_manager.subscribe(EventManager.Topics.BLASTER_DEAD, self.blaster_dead)

    def _init_defaults(self) -> None:
        self.lives = 3
        self.alive = True
        self.position = Blaster.Position.CENTER
        self.velocity = 60 #Steps for iteration (steps/second)
        self.remain_steps = 0 #Remaining steps for next iteration
        
        self.bullets = []
        self.mag_size = 5 #max acummulated bullets
        self.current_mag = self.mag_size #bullets in magazine
        self.reload_time = 0.3 
        self.accum_reload_time = 0
        self.time_btwn_shoots = 0.05
        self.last_shoot_time = 0

        self.zapper_count = 1
    
    def blaster_dead(self, data: dict):
        self.lives -= 1
        if self.lives == 0:
            self.alive = False

    @property
    def border_idx(self):
        return self._border_idx

    @border_idx.setter
    def border_idx(self, value: int):
        if value < 0 or value > 15:
            raise ValueError("Border index cannot be less than 0 or greater than 15.")
        self._border_idx = value

    
    def shoot(self):
        bullet = BlasterBullet(self.border_idx, self.world, self.event_manager)
        self.bullets.append(bullet)
        play_sound(self.sound_manager.get_sound("shot"))

    def update_bullets_frame(self):
        for bullet in self.bullets:
            bullet.update_frame()
        
        for bullet in self.bullets[:]:
            if not bullet.alive:
                self.bullets.remove(bullet)
    
    def draw_bullets_frame(self):
        for bullet in self.bullets:
            bullet.draw_frame()
    
    # NOTE: all levels were constructed clock-wise, and appended to the (x,y) list in that order
    # which means that border_idx + 1 jumps to left/clock-wise, and vice-versa.
    def _shift_left(self):
        # TODO: play movement sound
        if self.world.is_loop:
            if self.position is Blaster.Position.LEFT:
                if self.border_idx == 15:
                    self.border_idx = 0
                else:
                    self.border_idx += 1
                self.event_manager.notify(
                    EventManager.Topics.BLASTER_BORDER_UPDATE, {"border_idx": self.border_idx}
                )
                play_sound(self.sound_manager.get_sound("blaster_move"))
            self.position = self.position.prev_pos()

        else:
            if self.position is Blaster.Position.LEFT:
                if self.border_idx < 15:
                    self.border_idx += 1
                    self.position = self.position.prev_pos()
                    self.event_manager.notify(
                        EventManager.Topics.BLASTER_BORDER_UPDATE, {"border_idx": self.border_idx}
                    )
                    play_sound(self.sound_manager.get_sound("blaster_move"))
            else:
                self.position = self.position.prev_pos()

    def _shift_right(self):
        # TODO: play movement sound
        if self.world.is_loop:
            if self.position is Blaster.Position.RIGHT:
                if self.border_idx == 0:
                    self.border_idx = 15
                else:
                    self.border_idx -= 1
                self.event_manager.notify(
                    EventManager.Topics.BLASTER_BORDER_UPDATE, {"border_idx": self.border_idx}
                )
                play_sound(self.sound_manager.get_sound("blaster_move"))
            self.position = self.position.next_pos()
        else:
            if self.position is Blaster.Position.RIGHT:
                if self.border_idx > 1:
                    self.border_idx -= 1
                    self.position = self.position.next_pos()
                    self.event_manager.notify(
                        EventManager.Topics.BLASTER_BORDER_UPDATE, {"border_idx": self.border_idx}
                    )
                    play_sound(self.sound_manager.get_sound("blaster_move"))
            else:
                self.position = self.position.next_pos()

    def move_left(self, full_steps: int):
        for _ in range(full_steps):
            self._shift_left()
        
    def move_right(self, full_steps: int):
        for _ in range(full_steps):
            self._shift_right()
    
    def bullets_reloading(self):
        self.last_shoot_time += get_frame_time()
        self.accum_reload_time += get_frame_time()
        bullets_to_reload = self.accum_reload_time // self.reload_time
        if bullets_to_reload > 0:
            self.current_mag = min(self.current_mag + bullets_to_reload, self.mag_size)
            self.accum_reload_time %= self.reload_time
    
    def update_frame(self):
        """
        Checks main loop events e.g. pressed keys.
        """
        # Blaster movement
        move_steps: float = self.velocity * get_frame_time() + self.remain_steps
        full_steps: int = int(move_steps)
        self.remain_steps = move_steps - full_steps #Save remainder
        # Bullet movement
        self.update_bullets_frame()
        self.bullets_reloading()


        if is_key_down(KeyboardKey.KEY_RIGHT):
            self.move_left(full_steps)

        if is_key_down(KeyboardKey.KEY_LEFT):
            self.move_right(full_steps)

        if is_key_down(KeyboardKey.KEY_A):
            if self.current_mag >= 0 and self.last_shoot_time >= self.time_btwn_shoots:
                self.shoot()
                self.current_mag -= 1
                self.last_shoot_time = 0
        
        if is_key_pressed(KeyboardKey.KEY_SPACE):
            if self.zapper_count > 0:
                self.event_manager.notify(EventManager.Topics.SUPER_ZAPPER, {})
                self.zapper_count -= 1

    # TODO: Draw inside Blaster vectors.
    def draw_frame(self):
        """
        Draw blaster in the world.
        """

        # left border -> */__\
        border = self.world.borders[self.border_idx]
        # /__\* <- right border
        next_border = self.world.borders[self.border_idx - 1]
        border_line = next_border - border

        # distance from border line and blaster spike (highest point)
        blaster_height = border.distance(next_border) / 4
        tongs_height = blaster_height / 2

        def tong_vectors(
            out_left: Vec2, out_right: Vec2
        ) -> tuple[Vec2, Vec2]:
            """
            Compute Blaster tong vectors using out_left and out_right anchors.
            """

            perp = border_line.perp_norm() * -tongs_height

            if self.position is Blaster.Position.LEFT:
                left_quarter = out_left.lerp(out_right, 0.5)
                right_half_quarter = out_right.lerp(next_border, 0.5)
                left_tong = left_quarter + perp
                right_tong = right_half_quarter + perp

            elif self.position is Blaster.Position.RIGHT:
                left_quarter = out_left.lerp(border, 0.5)
                right_half_quarter = out_right.lerp(out_left, 0.5)
                left_tong = left_quarter + perp
                right_tong = right_half_quarter + perp

            else:
                left_quarter = out_left.lerp(out_right, 0.25)
                right_quarter = out_right.lerp(out_left, 0.25)
                left_tong = left_quarter + perp
                right_tong = right_quarter + perp

            return left_tong, right_tong


        # Compute anchors to draw within Blaster position. */__*__\ <-> */____\* <-> /__*__\*
        match self.position:
            case Blaster.Position.LEFT:
                out_left = border
                out_right = out_left.lerp(next_border, 0.5)
                perp = border_line.perp_norm() * blaster_height
                spike = border + perp
                left_tong, right_tong = tong_vectors(out_left, out_right)

            case Blaster.Position.CENTER_LEFT:
                out_left = border
                out_right = next_border
                left_quarter = border.lerp(next_border, 0.25)
                perp = border_line.perp_norm() * blaster_height
                spike = left_quarter + perp
                left_tong, right_tong = tong_vectors(out_left, out_right)

            case Blaster.Position.CENTER:
                out_left = border
                out_right = next_border
                middle = border.lerp(next_border, 0.5)
                perp = border_line.perp_norm() * blaster_height
                spike = middle + perp
                left_tong, right_tong = tong_vectors(out_left, out_right)

            case Blaster.Position.CENTER_RIGHT:
                out_left = border
                out_right = next_border
                left_quarter = next_border.lerp(border, 0.25)
                perp = border_line.perp_norm() * blaster_height
                spike = left_quarter + perp
                left_tong, right_tong = tong_vectors(out_left, out_right)

            case Blaster.Position.RIGHT:
                out_left = border.lerp(next_border, 0.5)
                out_right = next_border
                perp = border_line.perp_norm() * blaster_height
                spike = next_border + perp
                left_tong, right_tong = tong_vectors(out_left, out_right)

            case _:
                raise ValueError("Unknown position.")

        # Draw outside lines
        # spike
        draw_line_ex(out_left, spike, 2, TempestColors.YELLOW_NEON.rgba)
        draw_line_ex(out_right, spike, 2, TempestColors.YELLOW_NEON.rgba)
        # tong
        draw_line_ex(out_left, left_tong, 2, TempestColors.YELLOW_NEON.rgba)
        draw_line_ex(out_right, right_tong, 2, TempestColors.YELLOW_NEON.rgba)

        # Draw bullets
        self.draw_bullets_frame()
