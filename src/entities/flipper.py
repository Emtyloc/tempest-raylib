from src.worlds.worlds import WorldData
from .enemy import Enemy
from src.utils import Vec2
from src.shared import TempestColors, EventManager
from pyray import *

class Flipper(Enemy):

    def __init__(self, border_idx: int, world: WorldData, velocity: float, event_manager: EventManager):
        super().__init__(border_idx, world, velocity, event_manager)
        if world.is_loop:
            self.border_idx = get_random_value(0, 15)
        else:
            self.border_idx = get_random_value(1, 15)
        self.alive = True
        proyections = self.world.proyections
        proy = proyections[self.border_idx]
        next_proy = proyections[self._next_border_idx]
        self.left_anchor = proy
        self.right_anchor = next_proy
        
    def update_frame(self):
        self.move_towards_player()

    def blaster_bullet_update(self, data: dict):
        bullet = data["bullet"]
        
        if (check_collision_point_line(bullet.position, self.left_anchor, self.right_anchor, 4) or self.left_anchor == self.border_v) and self.border_idx == bullet.border_idx:
            self.alive = False
            self.event_manager.notify(EventManager.Topics.BLASTER_BULLET_COLLIDE, {"bullet": bullet})
            self.event_manager.unsubscribe(EventManager.Topics.BLASTER_BULLET_UPDATE, self.blaster_bullet_update)

    @property    
    def _next_border_idx(self):
        if self.border_idx == 0:
            return 15
        return self.border_idx - 1
        
    @property
    def border_v(self):
        return self.world.borders[self.border_idx]

    @property
    def next_border_v(self):
        return self.world.borders[self._next_border_idx]

    def move_towards_player(self):
        proyections = self.world.proyections

        proy = proyections[self.border_idx]
        next_proy = proyections[self._next_border_idx]

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

    @property
    def position(self):
        return self.left_anchor
    
    def rotate_left(self):
        pass
    
    def rotate_right(self):
        pass


    def draw_frame(self):
        if not self.alive: return

        section_lenght = self.left_anchor.distance(self.right_anchor) #We use this to compute all others
        
        flipper_height = section_lenght / 4

        perp = (self.left_anchor - self.right_anchor).perp_norm()

        cross_right = self.left_anchor.lerp(self.right_anchor, 7/8) + perp * flipper_height
        cross_left = self.right_anchor.lerp(self.left_anchor, 7/8) + perp * flipper_height

        mid_cross_right = self.left_anchor.lerp(self.right_anchor, 6/8) + perp * flipper_height / 2
        mid_cross_left = self.right_anchor.lerp(self.left_anchor, 6/8) + perp * flipper_height / 2
        

        # Draw cross
        draw_line_ex(self.left_anchor, cross_right, 2, TempestColors.RED_NEON.rgba())
        draw_line_ex(self.right_anchor, cross_left, 2, TempestColors.RED_NEON.rgba())
        
        # Draw mid-cross
        draw_line_ex(self.left_anchor, mid_cross_left, 2, TempestColors.RED_NEON.rgba())
        draw_line_ex(cross_left, mid_cross_left, 2, TempestColors.RED_NEON.rgba())

        draw_line_ex(self.right_anchor, mid_cross_right, 2, TempestColors.RED_NEON.rgba())
        draw_line_ex(cross_right, mid_cross_right, 2, TempestColors.RED_NEON.rgba())



        
        
        




