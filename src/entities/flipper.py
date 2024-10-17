from src.worlds.worlds import WorldData
from .enemy import Enemy
from src.utils import Vec2
from enum import IntEnum, auto
from src.shared import TempestColors, EventManager
from src.sounds import SoundManager
from pyray import *
import math

class Flipper(Enemy):

    class Position(IntEnum):
        UPRIGHT = auto()
        ROTATING_LEFT = auto()
        ROTATING_RIGHT = auto()

    def __init__(self, border_idx: int, world: WorldData, velocity: float, rotates: bool, event_manager: EventManager, sound_manager: SoundManager):
        super().__init__(border_idx, world, velocity, event_manager, sound_manager)
        self.alive = True
        self.active = False
        self.score = 150
        proyections = self.world.proyections
        proy = proyections[self.border_idx]
        next_proy = proyections[self.border_idx - 1]
        self.left_anchor = proy
        self.right_anchor = next_proy
        self.position = self.Position.UPRIGHT
        self.current_rotation = 0
        self.rotates = rotates
        self.blaster_border_v  = self.world.borders[0]
        self.next_blaster_border_v = self.world.borders[0]
        
    def update_frame(self):
        if (check_collision_circles(self.left_anchor, 3, self.blaster_border_v, 3) and 
            check_collision_circles(self.right_anchor, 3, self.next_blaster_border_v, 3)):
            self.event_manager.notify(EventManager.Topics.BLASTER_DEAD, {})
        match self.position:
            #TODO: make rotation while moving
            case self.Position.UPRIGHT:
                self.move_towards_player()
                if self.border_v == self.left_anchor and self.next_border_v == self.right_anchor:
                    rand_rotation = get_random_value(0, 1)
                    # RIGHT
                    if rand_rotation == 0:
                        if self.border_idx == 1 and not self.world.is_loop:
                            self.position = self.Position.ROTATING_LEFT
                        else:
                            self.position = self.Position.ROTATING_RIGHT
                    # LEFT
                    elif rand_rotation == 1:
                        if self.border_idx == 15 and not self.world.is_loop:
                            self.position = self.Position.ROTATING_RIGHT
                        else:
                            self.position = self.Position.ROTATING_LEFT

            case self.Position.ROTATING_RIGHT:
                self.rotate_right()

            case self.Position.ROTATING_LEFT:
                self.rotate_left()

            case _:
                raise Exception("Unknown flipper position")


    def blaster_bullet_update(self, data: dict):
        if not self.active:
            return
        bullet = data["bullet"]
        # TODO: check flipper collition when rotating
        if check_collision_circles(bullet.position, bullet.radio, self.left_anchor.lerp(self.right_anchor, 0.5), 2) and self.border_idx == bullet.border_idx:
            self.alive = False
            self.active = False
            self.event_manager.notify(EventManager.Topics.BLASTER_BULLET_COLLIDE, {"bullet": bullet})
            self.event_manager.unsubscribe(EventManager.Topics.BLASTER_BULLET_UPDATE, self.blaster_bullet_update)
            self.event_manager.notify(EventManager.Topics.SCORE_UPDATE, {"score": self.score})
            play_sound(self.sound_manager.get_sound("enemy_death"))


    def blaster_border_update(self, data: dict):
        blaster_border_idx = data["border_idx"]
        self.blaster_border_v = self.world.borders[blaster_border_idx]
        self.next_blaster_border_v = self.world.borders[blaster_border_idx - 1]
    
    def super_zapper(self, data):
        if not self.active:
            return
        self.alive = False
        self.active = False
        self.event_manager.notify(EventManager.Topics.SCORE_UPDATE, {"score": self.score})
        
    @property
    def border_v(self):
        return self.world.borders[self.border_idx]

    @property
    def next_border_v(self):
        return self.world.borders[self.border_idx - 1]
    
    @property
    def next_section_border_v(self):
        return self.world.borders[self.border_idx - 2]
    
    @property
    def prev_section_border_v(self):
        prev_idx = self.border_idx + 1 if self.border_idx + 1 <= 15 else 0
        return self.world.borders[prev_idx]

    def move_towards_player(self):
        proyections = self.world.proyections

        proy = proyections[self.border_idx]
        next_proy = proyections[self.border_idx - 1]

        # total perspective distance
        l_deep_distance = self.border_v.distance(proy)
        r_deep_distance = self.next_border_v.distance(next_proy)

        # current perspective distance
        l_anchor_dis = self.left_anchor.distance(proy)
        r_anchor_dis = self.right_anchor.distance(next_proy)

        pers_correction = 0.01 # fraction of deep_distance to avoid anchor_dis to be 0

        l_move_distance =  (l_anchor_dis + l_deep_distance * pers_correction) * self.velocity * get_frame_time()
        r_move_distance =  (r_anchor_dis + r_deep_distance * pers_correction) * self.velocity * get_frame_time()

        self.left_anchor = self.left_anchor.move_towards(self.border_v, l_move_distance)
        self.right_anchor = self.right_anchor.move_towards(self.next_border_v, r_move_distance)
    
    def rotate_right(self):
        border_line_v = self.border_v - self.next_border_v

        border_line_v_norm = border_line_v.normalize()
        
        next_section_border_v = self.next_section_border_v

        next_border_line_v = next_section_border_v - self.next_border_v

        next_section_len = next_border_line_v.length()

        border_line_to_rotate = border_line_v_norm * next_section_len

        total_rotation_angle = border_line_to_rotate.angle(next_border_line_v)
        
        self.current_rotation += get_frame_time() * math.pi * 2

        self.left_anchor = self.next_border_v

        if total_rotation_angle > 0:
            self.right_anchor = self.next_border_v + border_line_to_rotate.rotate(min(total_rotation_angle, self.current_rotation))
        else:
            self.right_anchor = self.next_border_v + border_line_to_rotate.rotate(max(total_rotation_angle, self.current_rotation))
        
        if check_collision_circles(self.right_anchor, 5, self.next_section_border_v, 5):
            self.border_idx = self.border_idx - 1 if self.border_idx - 1 >= 0 else 15
            self.current_rotation = 0

            if self.border_idx == 1 and not self.world.is_loop:
                self.position = self.Position.ROTATING_LEFT

    
    def rotate_left(self):

        border_line_v = self.next_border_v - self.border_v

        border_line_v_norm = border_line_v.normalize()
        
        prev_section_border_v = self.prev_section_border_v

        prev_border_line_v = prev_section_border_v - self.border_v

        prev_section_len = prev_border_line_v.length()

        border_line_to_rotate = border_line_v_norm * prev_section_len

        total_rotation_angle = border_line_to_rotate.angle(prev_border_line_v)
        
        self.current_rotation -= get_frame_time() * math.pi * 2

        if total_rotation_angle > 0:
            self.right_anchor = self.border_v + border_line_to_rotate.rotate(min(total_rotation_angle, self.current_rotation))
        else:
            self.right_anchor = self.border_v + border_line_to_rotate.rotate(max(total_rotation_angle, self.current_rotation))
        
        if check_collision_circles(self.right_anchor, 5, self.prev_section_border_v, 5):
            self.left_anchor = self.prev_section_border_v
            self.right_anchor = self.border_v
            self.border_idx = self.border_idx + 1 if self.border_idx + 1 <= 15 else 0
            self.current_rotation = 0
            
            if self.border_idx == 15 and not self.world.is_loop:
                self.position = self.Position.ROTATING_RIGHT




    def draw_frame(self):

        # SEPARATES DRAW LOGIC FROM MOVE/ROTATE LOGIC

        section_lenght = self.left_anchor.distance(self.right_anchor) #We use this to compute all others
        
        flipper_height = section_lenght / 4

        perp = (self.left_anchor - self.right_anchor).perp_norm()

        cross_right = self.left_anchor.lerp(self.right_anchor, 7/8) + perp * flipper_height
        cross_left = self.right_anchor.lerp(self.left_anchor, 7/8) + perp * flipper_height

        mid_cross_right = self.left_anchor.lerp(self.right_anchor, 6/8) + perp * flipper_height / 2
        mid_cross_left = self.right_anchor.lerp(self.left_anchor, 6/8) + perp * flipper_height / 2

        # Draw cross
        draw_line_ex(self.left_anchor, cross_right, 2, TempestColors.RED_NEON.rgba)
        draw_line_ex(self.right_anchor, cross_left, 2, TempestColors.RED_NEON.rgba)
        
        # Draw mid-cross
        draw_line_ex(self.left_anchor, mid_cross_left, 2, TempestColors.RED_NEON.rgba)
        draw_line_ex(cross_left, mid_cross_left, 2, TempestColors.RED_NEON.rgba)

        draw_line_ex(self.right_anchor, mid_cross_right, 2, TempestColors.RED_NEON.rgba)
        draw_line_ex(cross_right, mid_cross_right, 2, TempestColors.RED_NEON.rgba)



        
        
        




