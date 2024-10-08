from enum import Enum
from src.worlds import WorldData
from pyray import *
from src.shared import TempestColors, EventManager
from src.utils import Vec2
from src.entities import Flipper
import os, json
from importlib import import_module, resources


class Level:
    """
    Level class should handle:
    - Level states.
    - World drawing.
    - Enemies creations / deletions.
    """

    class States(Enum):
        LEVEL_BEGIN = 0
        LEVEL_COMPLETE = 1
        LEVEL_READY = 2
    

    def __init__(self, event_manager: EventManager):
        self.event_manager = (
            event_manager  # Common API to send/recibe data between objects.
        )
        self.event_manager.subscribe(EventManager.Topics.BLASTER_BORDER_UPDATE, self.blaster_border_update)
        self.enemies = []
        self.active_enemies = []
        self.time_last_spawn = 1

    def update_frame(self):
        self._spawn_enemy()
        self._update_enemies()
    
    def _spawn_enemy(self):
        self.time_last_spawn += get_frame_time()
        if self.time_last_spawn >= self.spawn_time:
            if not self.enemies: return
            random_enemy = self.enemies[get_random_value(0, len(self.enemies) - 1)]
            self.active_enemies.append(random_enemy)
            self.enemies.remove(random_enemy)
            self.time_last_spawn -= self.spawn_time
    
    def blaster_border_update(self, data: dict):
        self.blaster_border = data["border_idx"]
    
    # TODO: Use pydantic models to parse jsons
    def load_level_data(self, level_number: int):
        """
        Load level data extracted from levels.json.
        """
        with resources.open_text('src.levels', 'levels.json') as f:
            data = json.load(f).get(str(level_number))
            
            world_data = data.get("world")
            worlds_module = import_module("src.worlds")
            self.world = getattr(worlds_module, world_data["name"])
            
            shared_module = import_module("src.shared")
            tempest_colors = getattr(shared_module, "TempestColors")
            self.level_color = getattr(tempest_colors, world_data["color"]).rgba()
            
            enemies_data = data.get("enemies")
            entities_module = import_module("src.entities")
            for enemy_name in enemies_data:
                for _ in range(enemies_data[enemy_name]["quantity"]):
                    enemy = getattr(entities_module, enemy_name)(
                        border_idx = 0,
                        world = self.world,
                        velocity = enemies_data[enemy_name]["velocity"],
                        event_manager = self.event_manager
                    )
                    self.enemies.append(enemy)
            self.spawn_time = data["spawn_time"]


    def draw_frame(self):
        self._draw_world()
        self._draw_enemies()

    def _draw_world(self):
        proyections = self.world.proyections
        for i in range(16):
            draw_circle_v(self.world.borders[i], 2, self.level_color)
            draw_circle_v(proyections[i], 1, self.level_color)
            draw_line_ex(self.world.borders[i], proyections[i], 2, self.level_color)
            if i > 0:
                current_vec = self.world.borders[i]
                previous_vec = self.world.borders[i - 1]
                draw_line_ex(current_vec, previous_vec, 2, self.level_color)
                draw_line_ex(proyections[i], proyections[i - 1], 1, self.level_color)
        else:
            if self.world.is_loop:
                current_vec = self.world.borders[0]
                last_vec = self.world.borders[-1]
                draw_line_ex(current_vec, last_vec, 2, self.level_color)
                draw_line_ex(proyections[0], proyections[-1], 1, self.level_color)

        # Change color of blaster current border section  -> /_x_\ <-
        border = self.world.borders[self.blaster_border]
        # /__\* <- right border
        next_border = self.world.borders[self.blaster_border - 1]
        proyections = self.world.proyections
        draw_line_ex(
            border,
            proyections[self.blaster_border],
            2,
            TempestColors.YELLOW_NEON.rgba(),
        )
        draw_line_ex(
            next_border,
            proyections[self.blaster_border - 1],
            2,
            TempestColors.YELLOW_NEON.rgba(),
        )

    def _draw_enemies(self):
        for enemy in self.active_enemies:
            enemy.draw_frame()
    
    def _update_enemies(self):
        for enemy in self.active_enemies[:]:
            if not enemy.alive:
                self.active_enemies.remove(enemy)

        for enemy in self.active_enemies:
            enemy.update_frame()

    def is_over(self):
        return (not self.active_enemies and not self.enemies)
