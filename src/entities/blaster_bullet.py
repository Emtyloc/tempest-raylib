from src.shared import EventManager
from src.worlds import WorldData
from src.utils import Vec2
from pyray import *
from src.shared import TempestColors


class BlasterBullet:
    def __init__(self, border_idx: int, world: WorldData, event_manager: EventManager):
        self.event_manager = event_manager
        self.border_idx = border_idx
        self.world = world
        self.velocity = 200
        self._init_pos()

    def _init_pos(self):
        border = Vec2(self.world.x[self.border_idx], self.world.y[self.border_idx])
        next_border = Vec2(self.world.x[self.border_idx - 1], self.world.y[self.border_idx - 1])
        self.position = border.lerp(next_border, 0.5)

    @property
    def collision_pos(self):
        return self.position

    def update(self):
        proyections = self.world.get_proyections()
        move_dis = self.velocity * get_frame_time()
        move_to = proyections[self.border_idx].lerp(proyections[self.border_idx - 1], 0.5)
        self.position = self.position.move_towards(move_to, move_dis)


    def draw(self):
        draw_circle_v(self.position, 3, TempestColors.YELLOW_NEON.rgba())


