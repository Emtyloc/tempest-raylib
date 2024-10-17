from src.worlds.worlds import WorldData
from .enemy import Enemy
from src.utils import Vec2
from enum import IntEnum, auto
from src.shared import TempestColors, EventManager
from src.sounds import SoundManager
from pyray import *
import math
from .flipper import Flipper

class Tanker(Enemy):

    class Position(IntEnum):
        UPRIGHT = auto()

    def __init__(self, border_idx: int, world: WorldData, velocity: float, event_manager: EventManager, sound_manager: SoundManager):
        super().__init__(border_idx, world, velocity, event_manager, sound_manager)
        self.alive = True
        self.active = False
        self.score = 200
        proyections = self.world.proyections
        proy = proyections[self.border_idx]
        next_proy = proyections[self.border_idx - 1]
        self.left_anchor = proy
        self.right_anchor = next_proy
        self.position = self.Position.UPRIGHT


    def update_frame(self):
        if (check_collision_circles(self.left_anchor, 3, self.blaster_border_v, 3) and 
            check_collision_circles(self.right_anchor, 3, self.next_blaster_border_v, 3)):
            self.event_manager.notify(EventManager.Topics.BLASTER_DEAD, {})
        match self.position:
            case self.Position.UPRIGHT:
                self.move_towards_player()
                if self.border_v == self.left_anchor and self.next_border_v == self.right_anchor:
                    self.death_by_border_colision()
            case _:
                raise Exception("Invalid position")
            
    def death_by_border_colision(self):
        self.alive = False
        self.active = False
        self.event_manager.unsubscribe(EventManager.Topics.BLASTER_BULLET_UPDATE, self.blaster_bullet_update)
        self.spawn_flippers_proyections()

        
    def death_by_blaster_colision(self):
        self.alive = False
        self.active = False
        self.spawn_flippers_proyections()
        self.event_manager.notify(EventManager.Topics.BLASTER_DEAD, {})


    def spawn_flippers_proyections(self):
        if self.world.is_loop:
            if self.border_idx == 0:
                self.event_manager.notify(EventManager.Topics.SPAWN_ENEMY, {"enemy_type": Flipper, "border_idx": 15, "velocity": self.velocity, "rotates": True, "left_anchor": self.left_anchor, "right_anchor": self.right_anchor})
                self.event_manager.notify(EventManager.Topics.SPAWN_ENEMY, {"enemy_type": Flipper, "border_idx": 1, "velocity": self.velocity, "rotates": True, "left_anchor": self.left_anchor, "right_anchor": self.right_anchor})
            elif self.border_idx == 15:
                self.event_manager.notify(EventManager.Topics.SPAWN_ENEMY, {"enemy_type": Flipper, "border_idx": 14, "velocity": self.velocity, "rotates": True, "left_anchor": self.left_anchor, "right_anchor": self.right_anchor})
                self.event_manager.notify(EventManager.Topics.SPAWN_ENEMY, {"enemy_type": Flipper, "border_idx": 0, "velocity": self.velocity, "rotates": True, "left_anchor": self.left_anchor, "right_anchor": self.right_anchor})
            else:
                self.event_manager.notify(EventManager.Topics.SPAWN_ENEMY, {"enemy_type": Flipper, "border_idx": self.border_idx - 1, "velocity": self.velocity, "rotates": True, "left_anchor": self.left_anchor, "right_anchor": self.right_anchor})
                self.event_manager.notify(EventManager.Topics.SPAWN_ENEMY, {"enemy_type": Flipper, "border_idx": self.border_idx + 1, "velocity": self.velocity, "rotates": True, "left_anchor": self.left_anchor, "right_anchor": self.right_anchor})
        else:
            if self.border_idx == 0:
                self.event_manager.notify(EventManager.Topics.SPAWN_ENEMY, {"enemy_type": Flipper, "border_idx": 1, "velocity": self.velocity, "rotates": True, "left_anchor": self.left_anchor, "right_anchor": self.right_anchor})
                self.event_manager.notify(EventManager.Topics.SPAWN_ENEMY, {"enemy_type": Flipper, "border_idx": 2, "velocity": self.velocity, "rotates": True, "left_anchor": self.left_anchor, "right_anchor": self.right_anchor})
            elif self.border_idx == 15:
                self.event_manager.notify(EventManager.Topics.SPAWN_ENEMY, {"enemy_type": Flipper, "border_idx": 14, "velocity": self.velocity, "rotates": True, "left_anchor": self.left_anchor, "right_anchor": self.right_anchor})
                self.event_manager.notify(EventManager.Topics.SPAWN_ENEMY, {"enemy_type": Flipper, "border_idx": 13, "velocity": self.velocity, "rotates": True, "left_anchor": self.left_anchor, "right_anchor": self.right_anchor})
            else:
                self.event_manager.notify(EventManager.Topics.SPAWN_ENEMY, {"enemy_type": Flipper, "border_idx": self.border_idx - 1, "velocity": self.velocity, "rotates": True, "left_anchor": self.left_anchor, "right_anchor": self.right_anchor})
                self.event_manager.notify(EventManager.Topics.SPAWN_ENEMY, {"enemy_type": Flipper, "border_idx": self.border_idx + 1, "velocity": self.velocity, "rotates": True, "left_anchor": self.left_anchor, "right_anchor": self.right_anchor})


    def blaster_bullet_update(self, data: dict):
        if not self.active:
            return
        bullet = data["bullet"]
        if check_collision_circles(bullet.position, bullet.radio, self.left_anchor.lerp(self.right_anchor, 0.5), 2) and self.border_idx == bullet.border_idx:
        
            self.alive = False
            self.active = False
            self.event_manager.notify(EventManager.Topics.BLASTER_BULLET_COLLIDE, {"bullet": bullet})
            self.event_manager.unsubscribe(EventManager.Topics.BLASTER_BULLET_UPDATE, self.blaster_bullet_update)
            self.event_manager.notify(EventManager.Topics.SCORE_UPDATE, {"score": self.score})
            play_sound(self.sound_manager.get_sound("enemy_death"))
            #generate two new enemies 
            #TODO refactor this
            self.spawn_flippers_proyections()


    def blaster_border_update(self, data: dict):
        blaster_border_idx = data["border_idx"]
        self.blaster_border_v = self.world.borders[blaster_border_idx]
        self.next_blaster_border_v = self.world.borders[blaster_border_idx - 1]


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


    def draw_frame(self):

        # SEPARATES DRAW LOGIC FROM MOVE/ROTATE LOGIC

        side_length = self.left_anchor.distance(self.right_anchor)
        
        perp = (self.left_anchor - self.right_anchor).perp_norm()
        center = (self.left_anchor + self.right_anchor) * 0.5 + perp * (side_length * 0.5)
     

        
        # Calculate the inner square vertices
        inner_offset = side_length * 0.2  # Adjust this factor to control the size of the inner square

        # Calculate the inner square vertices rotated by 45 degrees
        inner_top = center + perp * inner_offset
        inner_right = center + (self.right_anchor - self.left_anchor).normalize() * inner_offset
        inner_bottom = center - perp * inner_offset
        inner_left = center - (self.right_anchor - self.left_anchor).normalize() * inner_offset

        # Calculate the outer square vertices rotated by 45 degrees
        outer_top = center + perp * (side_length * 0.5)
        outer_right = center + (self.right_anchor - self.left_anchor).normalize() * (side_length * 0.5)
        outer_bottom = center - perp * (side_length * 0.5)
        outer_left = center - (self.right_anchor - self.left_anchor).normalize() * (side_length * 0.5)

        # Draw the outer square
        draw_line_ex(outer_top, outer_right, 2, TempestColors.TURQUOISE_NEON.rgba)
        draw_line_ex(outer_right, outer_bottom, 2, TempestColors.TURQUOISE_NEON.rgba)
        draw_line_ex(outer_bottom, outer_left, 2, TempestColors.TURQUOISE_NEON.rgba)
        draw_line_ex(outer_left, outer_top, 2, TempestColors.TURQUOISE_NEON.rgba)

        # Draw the inner square
        draw_line_ex(inner_top, inner_right, 2, TempestColors.TURQUOISE_NEON.rgba)
        draw_line_ex(inner_right, inner_bottom, 2, TempestColors.TURQUOISE_NEON.rgba)
        draw_line_ex(inner_bottom, inner_left, 2, TempestColors.TURQUOISE_NEON.rgba)
        draw_line_ex(inner_left, inner_top, 2, TempestColors.TURQUOISE_NEON.rgba)


        # Now the diagonals

        draw_line_ex(outer_top, inner_top, 2, TempestColors.TURQUOISE_NEON.rgba)
        draw_line_ex(outer_top, inner_right, 2, TempestColors.TURQUOISE_NEON.rgba)
        draw_line_ex(outer_right, inner_right, 2, TempestColors.TURQUOISE_NEON.rgba)
        draw_line_ex(outer_right, inner_bottom, 2, TempestColors.TURQUOISE_NEON.rgba)
        draw_line_ex(outer_bottom, inner_bottom, 2, TempestColors.TURQUOISE_NEON.rgba)
        draw_line_ex(outer_bottom, inner_left, 2, TempestColors.TURQUOISE_NEON.rgba)
        draw_line_ex(outer_left, inner_left, 2, TempestColors.TURQUOISE_NEON.rgba)
        draw_line_ex(outer_left, inner_top, 2, TempestColors.TURQUOISE_NEON.rgba)




        
 
