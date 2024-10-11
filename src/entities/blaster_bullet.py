from src.shared import EventManager
from src.worlds import WorldData
from pyray import *
from src.shared import TempestColors


class BlasterBullet:
    def __init__(self, border_idx: int, world: WorldData, event_manager: EventManager):
        self.event_manager = event_manager
        self.border_idx = border_idx
        self.world = world
        self.velocity = 2
        self.init_radio = 6
        self.radio = self.init_radio
        self.alive = True
        self.event_manager.subscribe(EventManager.Topics.BLASTER_BULLET_COLLIDE, self.blaster_bullet_collide)
        self._init_pos()

    def _init_pos(self):
        border = self.world.borders[self.border_idx]
        next_border = self.world.borders[self.border_idx - 1]
        self.position = border.lerp(next_border, 0.5)

    def check_proyection_collision(self):
        proy = self.world.proyections[self.border_idx]
        next_proy = self.world.proyections[self.border_idx - 1]

        if self.position == proy.lerp(next_proy, 0.5):
            self.alive = False
    
    def blaster_bullet_collide(self, data: dict):
        bullet = data["bullet"]
        if self is bullet: 
            self.alive = False
            self.event_manager.unsubscribe(EventManager.Topics.BLASTER_BULLET_COLLIDE, self.blaster_bullet_collide)

    def move_bullet(self):
        proyections = self.world.proyections
        
        border = self.world.borders[self.border_idx]
        next_border = self.world.borders[self.border_idx - 1]

        proyection = proyections[self.border_idx]
        next_proyection = proyections[self.border_idx - 1]

        border_pos = border.lerp(next_border, 0.5)
        proy_pos = proyection.lerp(next_proyection, 0.5)
        
        deep_distance = border_pos.distance(proy_pos)

        current_deep_distance = self.position.distance(proy_pos)

        pers_correction = 0.01

        move_distance = (current_deep_distance + deep_distance * pers_correction) * self.velocity * get_frame_time()

        self.position = self.position.move_towards(proy_pos, move_distance)

        self.radio = max(round(self.init_radio * current_deep_distance / deep_distance, 3), 2)
    
    
    def update_frame(self):
        self.event_manager.notify(EventManager.Topics.BLASTER_BULLET_UPDATE, {"bullet": self})
        self.check_proyection_collision()
        self.move_bullet()

    def draw_frame(self):
        if self.alive:
            draw_circle_v(self.position, self.radio, TempestColors.YELLOW_NEON.rgba())


